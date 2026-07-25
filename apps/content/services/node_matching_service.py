"""Matching entre Resource (Sistema A) y KnowledgeNode (Sistema B).

Pipeline de 3 pasos, sin dependencias nuevas: paso 1 y 2 usan difflib
(stdlib, portable entre SQLite y Postgres); paso 3 reusa
ai_generation_service.call_ai_structured_json como corroboración acotada.
"""
from difflib import SequenceMatcher

from apps.content.models import KnowledgeNode
from apps.content.services.ai_generation_service import call_ai_structured_json

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


def _node_summary(node) -> str:
    content = getattr(node, "content", None)
    objetivo = (content.objetivo if content else "") or ""
    return f"{node.code} — {node.name}: {objetivo}".strip()


def corroborate_with_ai(resource, candidate_leaf, alternatives):
    """Paso 3: le pide a la IA confirmar o corregir el candidato del paso 2.

    alternatives: lista de 0 a 2 KnowledgeNode. Devuelve
    {'node': KnowledgeNode, 'ai_corrigio': bool, 'ai_rationale': str}, o None
    si la IA no está disponible o falla (se degrada al candidato de texto).
    """
    transcript_excerpt = (resource.transcript or "").strip()[:800]
    alt_lines = "\n".join(f"- id={n.id}: {_node_summary(n)}" for n in alternatives)

    prompt = (
        "Un video educativo necesita conectarse al nodo de conocimiento correcto.\n\n"
        f'Video: "{resource.title}"\n'
        + (f"Extracto de la transcripción: {transcript_excerpt}\n" if transcript_excerpt else "")
        + "\nCandidato sugerido por búsqueda de texto:\n"
        f"- id={candidate_leaf.id}: {_node_summary(candidate_leaf)}\n\n"
        "Alternativas cercanas:\n"
        f"{alt_lines if alt_lines else '(ninguna)'}\n\n"
        "¿Es el candidato sugerido el más adecuado para este video? Si no, ¿cuál de "
        "las alternativas calza mejor? Responde en JSON exacto:\n"
        '{"chosen_id": <id del nodo elegido>, "corrected": <true si elegiste una '
        'alternativa en vez del candidato, false si confirmaste el candidato>, '
        '"rationale": "<razón breve, 1-2 oraciones>"}'
    )

    try:
        data = call_ai_structured_json(prompt)
    except (ValueError, RuntimeError):
        return None

    chosen_id = data.get("chosen_id")
    rationale = str(data.get("rationale", ""))[:500]
    corrected = bool(data.get("corrected", False))

    options = {n.id: n for n in [candidate_leaf, *alternatives]}
    chosen_node = options.get(chosen_id, candidate_leaf)

    return {
        "node": chosen_node,
        "ai_corrigio": corrected and chosen_node.id != candidate_leaf.id,
        "ai_rationale": rationale,
    }


def generate_suggestion(resource):
    """Corre el pipeline de 3 pasos y crea el ResourceNodeSuggestion del recurso.

    Idempotente: si ya existe una fila para este recurso, la devuelve sin
    reprocesar (nunca crea una segunda).
    """
    from apps.content.models import ResourceNodeSuggestion

    existing = ResourceNodeSuggestion.objects.filter(resource=resource).first()
    if existing:
        return existing

    block_node = find_matching_block(resource)
    if block_node is None:
        return ResourceNodeSuggestion.objects.create(
            resource=resource, node=None, status=ResourceNodeSuggestion.STATUS_SIN_BLOQUE,
        )

    scored_candidates = find_candidate_leaf_nodes(block_node, resource)
    if not scored_candidates:
        return ResourceNodeSuggestion.objects.create(
            resource=resource, node=None, status=ResourceNodeSuggestion.STATUS_SIN_BLOQUE,
        )

    top_candidate = scored_candidates[0][0]
    alternatives = [pair[0] for pair in scored_candidates[1:3]]

    ai_result = corroborate_with_ai(resource, top_candidate, alternatives)
    if ai_result:
        node = ai_result["node"]
        ai_corrigio = ai_result["ai_corrigio"]
        ai_rationale = ai_result["ai_rationale"]
    else:
        node = top_candidate
        ai_corrigio = False
        ai_rationale = ""

    return ResourceNodeSuggestion.objects.create(
        resource=resource,
        node=node,
        status=ResourceNodeSuggestion.STATUS_SUGERIDO,
        ai_rationale=ai_rationale,
        ai_corrigio=ai_corrigio,
        origen=ResourceNodeSuggestion.ORIGEN_IA,
    )
