"""Matching entre Resource (Sistema A) y KnowledgeNode (Sistema B).

Un solo paso, determinístico, sin IA ni dependencias nuevas: compara el
nombre del Topic legacy contra los bloques/temas del árbol nuevo por
similitud de texto (difflib, stdlib). El destino es el bloque o tema que
mejor calza — no un recurso atómico — porque un video normalmente cubre
varios recursos de un mismo tema, no uno solo.
"""
from difflib import SequenceMatcher

from apps.content.models import KnowledgeNode

BLOCK_MATCH_THRESHOLD = 0.5


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower().strip(), (b or "").lower().strip()).ratio()


def find_matching_block(resource) -> KnowledgeNode | None:
    """Encuentra el bloque/tema de KnowledgeNode que mejor calza con el Topic
    del recurso, por similitud de nombre. None si no hay Topic o no hay match
    razonable (bajo BLOCK_MATCH_THRESHOLD)."""
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


def generate_suggestion(resource):
    """Crea el ResourceNodeSuggestion del recurso a partir del match de texto.

    Idempotente: si ya existe una fila para este recurso, la devuelve sin
    reprocesar (nunca crea una segunda).
    """
    from apps.content.models import ResourceNodeSuggestion

    existing = ResourceNodeSuggestion.objects.filter(resource=resource).first()
    if existing:
        return existing

    node = find_matching_block(resource)
    if node is None:
        return ResourceNodeSuggestion.objects.create(
            resource=resource, node=None, status=ResourceNodeSuggestion.STATUS_SIN_BLOQUE,
        )

    return ResourceNodeSuggestion.objects.create(
        resource=resource,
        node=node,
        status=ResourceNodeSuggestion.STATUS_SUGERIDO,
        origen=ResourceNodeSuggestion.ORIGEN_IA,
    )
