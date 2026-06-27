import re

from django.http import Http404
from django.shortcuts import get_object_or_404, render

from apps.content.models import KnowledgeNode, NodeContent, NodeMedia


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

    if node.is_leaf:
        return _recurso_view(request, node, breadcrumbs)
    return _list_view(request, node, chain, breadcrumbs)


def _list_view(request, node, chain, breadcrumbs):
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
            "noindex": not node.is_published,
        },
    )


def _recurso_view(request, node, breadcrumbs):
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

    return render(
        request,
        "learn/node_detail.html",
        {
            "node": node,
            "content": content,
            "youtube_id": youtube_id,
            "other_media": other_media,
            "breadcrumbs": breadcrumbs,
            "noindex": noindex,
        },
    )
