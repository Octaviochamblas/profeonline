import json
import re

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.db.models import Prefetch
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_POST

from apps.content.models import (
    KnowledgeNode,
    NodeContent,
    NodeExercise,
    NodeMedia,
    NodePrerequisite,
)
from apps.learn.forms import NodeContentEditorForm


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
            "practice_bank": _build_practice_bank(node),
            "prerequisites": prerequisites,
            "breadcrumbs": breadcrumbs,
            "noindex": noindex,
        },
    )


@require_POST
@login_required
def edit_node_content(request, node_id):
    node = get_object_or_404(
        KnowledgeNode,
        pk=node_id,
        node_type=KnowledgeNode.NODE_RECURSO,
    )
    permission = (
        "content.change_nodecontent"
        if NodeContent.objects.filter(node=node).exists()
        else "content.add_nodecontent"
    )
    if not request.user.has_perm(permission):
        raise PermissionDenied

    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"ok": False, "errors": {"__all__": ["JSON inválido."]}},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"ok": False, "errors": {"__all__": ["Datos inválidos."]}},
            status=400,
        )

    form = NodeContentEditorForm(payload)
    if not form.is_valid():
        return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)

    try:
        with transaction.atomic():
            content = NodeContent.objects.select_for_update().filter(node=node).first()
            permission = (
                "content.change_nodecontent" if content else "content.add_nodecontent"
            )
            if not request.user.has_perm(permission):
                raise PermissionDenied

            expected_updated_at = form.cleaned_data["updated_at"]
            if content:
                expected = (
                    parse_datetime(expected_updated_at) if expected_updated_at else None
                )
                if expected is None or expected != content.updated_at:
                    return JsonResponse(
                        {
                            "ok": False,
                            "error": "El recurso fue modificado en otra sesión. Recarga la página antes de guardar.",
                        },
                        status=409,
                    )
            elif expected_updated_at:
                return JsonResponse(
                    {
                        "ok": False,
                        "error": "El recurso fue creado en otra sesión. Recarga la página antes de guardar.",
                    },
                    status=409,
                )

            if content is None:
                content = NodeContent(node=node)

            for field in (
                "objetivo",
                "introduccion",
                "resumen",
                "explicacion",
                "procedimiento",
                "ejemplos",
                "errores_frecuentes",
                "fuente",
                "estado",
            ):
                setattr(content, field, form.cleaned_data[field])
            content.manual_override = True
            content.manual_edited_at = timezone.now()
            content.manual_edited_by = request.user
            content.save()
    except IntegrityError:
        return JsonResponse(
            {
                "ok": False,
                "error": "El recurso fue creado en otra sesión. Recarga la página antes de guardar.",
            },
            status=409,
        )

    return JsonResponse({"ok": True, "updated_at": content.updated_at.isoformat()})
