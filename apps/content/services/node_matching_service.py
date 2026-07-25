"""Matching entre Resource (Sistema A) y KnowledgeNode (Sistema B).

Pipeline de 3 pasos, sin dependencias nuevas: paso 1 y 2 usan difflib
(stdlib, portable entre SQLite y Postgres); paso 3 reusa
ai_generation_service.call_ai_structured_json como corroboración acotada.
"""
from difflib import SequenceMatcher

from apps.content.models import KnowledgeNode

BLOCK_MATCH_THRESHOLD = 0.5
MAX_LEAF_CANDIDATES = 20


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower().strip(), (b or "").lower().strip()).ratio()


def find_matching_block(resource) -> KnowledgeNode | None:
    """Paso 1: encuentra el bloque/tema de KnowledgeNode que mejor calza con el
    Topic del recurso, por similitud de nombre. None si no hay Topic o no hay
    match razonable (bajo BLOCK_MATCH_THRESHOLD)."""
    topic = resource.topic
    if topic is None:
        return None

    candidates = KnowledgeNode.objects.filter(
        node_type__in=[KnowledgeNode.NODE_BLOQUE, KnowledgeNode.NODE_TEMA],
    )
    best_node = None
    best_score = 0.0
    for node in candidates:
        score = _similarity(topic.name, node.name)
        if score > best_score:
            best_score = score
            best_node = node

    if best_score < BLOCK_MATCH_THRESHOLD:
        return None
    return best_node


def find_candidate_leaf_nodes(block_node, resource):
    """Paso 2: dentro de block_node (bloque o tema), busca los nodos hoja
    ('recurso') mas parecidos al titulo del recurso, via similitud de texto.
    Devuelve hasta 3 pares (node, score) ordenados de mayor a menor score.
    """
    leaves = list(
        KnowledgeNode.objects.filter(
            node_type=KnowledgeNode.NODE_RECURSO,
            code__startswith=f"{block_node.code}.",
        ).order_by("code")[:MAX_LEAF_CANDIDATES]
    )
    if not leaves:
        return []

    scored = [(leaf, _similarity(resource.title, leaf.name)) for leaf in leaves]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:3]
