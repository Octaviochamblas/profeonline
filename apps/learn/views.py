import re

from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from apps.content.models import (
    KnowledgeNode,
    NodeExercise,
    NodeMedia,
    NodePrerequisite,
)


def _youtube_id(url):
    if not url:
        return None
    m = re.search(
        r"(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)([^\"&?/\s]{11})",
        url,
    )
    return m.group(1) if m else None


def _ancestor_chain(node):
    """Lista de ancestros del más raíz al nodo actual, incluido el nodo."""
    chain = []
    cur = node
    while cur:
        chain.append(cur)
        cur = cur.parent
    chain.reverse()
    return chain


def _build_breadcrumbs(chain):
    """Construye la lista de breadcrumbs a partir de la cadena raíz→nodo."""
    crumbs = [{"label": "Inicio", "url": "/"}, {"label": "Aprender", "url": "/aprender/"}]
    for i, node in enumerate(chain):
        url = "/aprender/" + "/".join(a.slug for a in chain[: i + 1]) + "/"
        is_current = i == len(chain) - 1
        crumbs.append({"label": node.name, "url": None if is_current else url})
    return crumbs


def _node_url(node):
    """URL pública /aprender/… de un nodo, recorriendo sus ancestros."""
    chain = _ancestor_chain(node)
    return "/aprender/" + "/".join(n.slug for n in chain) + "/"


def _build_prerequisites(node):
    """Prerrequisitos publicados del nodo (requeridos primero), como enlaces.

    Sin estado por alumno todavía (F5 diferida): solo informativo, nunca bloquea.
    Omite prerrequisitos cuyo nodo destino no está publicado (evita enlaces rotos).
    """
    order_map = {
        NodePrerequisite.KIND_REQUERIDO: 0,
        NodePrerequisite.KIND_RECOMENDADO: 1,
    }
    prereqs = sorted(
        node.prerequisites.select_related("requires"),
        key=lambda pr: (order_map.get(pr.kind, 9), pr.requires.name),
    )
    return [
        {
            "node": pr.requires,
            "url": _node_url(pr.requires),
            "kind": pr.kind,
            "kind_display": pr.get_kind_display(),
        }
        for pr in prereqs
        if pr.requires.is_published
    ]


def learn_home(request):
    asignaturas = KnowledgeNode.objects.filter(
        node_type=KnowledgeNode.NODE_ASIGNATURA,
        is_published=True,
    )
    return render(request, "learn/home.html", {"asignaturas": asignaturas})


def node_view(request, **kwargs):
    # Resuelve el nodo desde el slug más profundo disponible en la URL.
    slug = None
    for key in ("recurso_slug", "tema_slug", "bloque_slug", "eje_slug", "asignatura_slug"):
        if key in kwargs:
            slug = kwargs[key]
            break

    node = get_object_or_404(KnowledgeNode, slug=slug)

    if not node.is_published and not request.user.is_staff:
        raise Http404

    chain = _ancestor_chain(node)
    breadcrumbs = _build_breadcrumbs(chain)

    prerequisites = _build_prerequisites(node)
    if node.is_leaf:
        return _recurso_view(request, node, breadcrumbs, prerequisites)
    return _list_view(request, node, chain, breadcrumbs, prerequisites)


def _related_items(node, user):
    """Temas y recursos que apuntan a este nodo, para el bloque "Ver también"."""
    items = [
        {"label": topic.name, "url": reverse("content:topic_detail", args=[topic.slug])}
        for topic in node.linked_topics.all()
    ]
    resources = node.linked_resources.all()
    if not user.is_staff:
        resources = resources.filter(is_published=True)
    items += [
        {"label": resource.title, "url": reverse("content:resource_detail", args=[resource.slug])}
        for resource in resources
    ]
    return items


def _list_view(request, node, chain, breadcrumbs, prerequisites):
    children = node.children.order_by("order", "code")
    if not request.user.is_staff:
        children = children.filter(is_published=True)

    return render(
        request,
        "learn/node_list.html",
        {
            "node": node,
            "children": children,
            "breadcrumbs": breadcrumbs,
            "prerequisites": prerequisites,
            "noindex": not node.is_published,
            "related_items": _related_items(node, request.user),
        },
    )


def _build_practice_bank(node):
    """Grupos de ítems publicados con sus ejercicios publicados, en orden.

    Solo se muestran ejercicios `status=published`. Devuelve una lista de
    `{"group": ItemGroup, "exercises": [...]}`; omite grupos sin ejercicios.
    """
    groups = (
        node.item_groups.filter(is_published=True)
        .order_by("order")
        .prefetch_related(
            Prefetch(
                "exercises",
                queryset=NodeExercise.objects.filter(
                    status=NodeExercise.STATUS_PUBLISHED
                ).order_by("order"),
                to_attr="published_exercises",
            )
        )
    )
    return [
        {"group": g, "exercises": g.published_exercises}
        for g in groups
        if g.published_exercises
    ]


def _recurso_view(request, node, breadcrumbs, prerequisites):
    from apps.content.services.node_assessment_service import get_node_mastery

    content = getattr(node, "content", None)
    noindex = not node.is_published or content is None or content.is_draft

    youtube_id = None
    other_media = []
    for m in node.media.all():
        if (
            m.kind == NodeMedia.KIND_VIDEO_YOUTUBE
            and m.video_kind == NodeMedia.VIDEO_KIND_EXPLICACION
            and youtube_id is None
        ):
            youtube_id = _youtube_id(m.url)
        else:
            other_media.append(m)

    previous_node = None
    next_node = None
    if node.parent:
        siblings = node.parent.children.order_by("order", "code")
        if not request.user.is_staff:
            siblings = siblings.filter(is_published=True)
        siblings = list(siblings)
        try:
            idx = siblings.index(node)
            if idx > 0:
                previous_node = siblings[idx - 1]
            if idx + 1 < len(siblings):
                next_node = siblings[idx + 1]
        except ValueError:
            pass

    return render(
        request,
        "learn/node_detail.html",
        {
            "node": node,
            "content": content,
            "youtube_id": youtube_id,
            "other_media": other_media,
            "practice_bank": _build_practice_bank(node),
            "prerequisites": prerequisites,
            "breadcrumbs": breadcrumbs,
            "noindex": noindex,
            "mastery": get_node_mastery(request.user, node),
            "related_items": _related_items(node, request.user),
            "previous_node": previous_node,
            "next_node": next_node,
        },
    )
