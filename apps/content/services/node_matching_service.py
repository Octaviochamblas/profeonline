"""Matching entre Topic (Sistema A, legacy) y KnowledgeNode (Sistema B).

Un solo paso, determinístico, sin IA: compara el nombre del Topic legacy
contra los bloques/temas del árbol nuevo por similitud de texto (difflib,
stdlib). El resultado es solo una sugerencia de punto de partida — la
página de revisión de Temas la calcula al vuelo, nunca se persiste.
"""
from difflib import SequenceMatcher

from apps.content.models import KnowledgeNode

BLOCK_MATCH_THRESHOLD = 0.5


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower().strip(), (b or "").lower().strip()).ratio()


def find_matching_block(topic) -> KnowledgeNode | None:
    """Encuentra el bloque/tema de KnowledgeNode que mejor calza con el
    nombre del Topic, por similitud de texto. None si no hay match
    razonable (bajo BLOCK_MATCH_THRESHOLD)."""
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
