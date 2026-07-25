from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.content.models import KnowledgeNode, ResourceNodeSuggestion
from apps.content.views.permissions import is_admin


@user_passes_test(is_admin)
def node_suggestions_review(request):
    pending = (
        ResourceNodeSuggestion.objects.filter(
            status__in=[
                ResourceNodeSuggestion.STATUS_SUGERIDO,
                ResourceNodeSuggestion.STATUS_SIN_BLOQUE,
            ]
        )
        .select_related("resource", "node")
        .order_by("-created_at")
    )
    return render(
        request, "pages/node_suggestions_review.html", {"suggestions": pending},
    )


@user_passes_test(is_admin)
@require_POST
def confirm_node_suggestion(request, suggestion_id):
    suggestion = get_object_or_404(ResourceNodeSuggestion, pk=suggestion_id)
    manual_node_id = request.POST.get("node_id")

    if manual_node_id:
        node = get_object_or_404(
            KnowledgeNode, pk=manual_node_id, node_type=KnowledgeNode.NODE_RECURSO,
        )
        suggestion.node = node
        suggestion.origen = ResourceNodeSuggestion.ORIGEN_MANUAL
    elif suggestion.node:
        suggestion.origen = ResourceNodeSuggestion.ORIGEN_IA
    else:
        return HttpResponse("No hay nodo para confirmar sin selección manual.", status=400)

    suggestion.status = ResourceNodeSuggestion.STATUS_CONFIRMADO
    suggestion.confirmed_at = timezone.now()
    suggestion.save()
    return HttpResponse("")


@user_passes_test(is_admin)
@require_POST
def discard_node_suggestion(request, suggestion_id):
    suggestion = get_object_or_404(ResourceNodeSuggestion, pk=suggestion_id)
    suggestion.status = ResourceNodeSuggestion.STATUS_DESCARTADO
    suggestion.save()
    return HttpResponse("")


@user_passes_test(is_admin)
def node_options(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"nodes": []})

    nodes = KnowledgeNode.objects.filter(
        node_type=KnowledgeNode.NODE_RECURSO,
    ).filter(
        Q(name__icontains=query) | Q(code__icontains=query)
    )[:20]

    data = [{"id": n.id, "label": f"{n.code} — {n.name}"} for n in nodes]
    return JsonResponse({"nodes": data})
