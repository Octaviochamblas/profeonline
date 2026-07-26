from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.content.models import KnowledgeNode, Topic
from apps.content.services.node_matching_service import find_matching_block
from apps.content.views.permissions import is_admin

NODE_TYPES_LINKABLE = [
    KnowledgeNode.NODE_BLOQUE,
    KnowledgeNode.NODE_TEMA,
    KnowledgeNode.NODE_RECURSO,
]


@user_passes_test(is_admin)
def topic_node_links_review(request):
    topics = (
        Topic.objects.select_related("related_node", "subject")
        .annotate(resource_count=Count("resources", filter=Q(resources__is_published=True)))
        .order_by("subject__name", "name")
    )
    rows = []
    for topic in topics:
        suggestion = None
        if topic.related_node is None:
            suggestion = find_matching_block(topic)
        rows.append({"topic": topic, "suggestion": suggestion})

    return render(
        request, "pages/topic_node_links_review.html", {"rows": rows},
    )


@user_passes_test(is_admin)
@require_POST
def set_topic_node_link(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    node = get_object_or_404(
        KnowledgeNode, pk=request.POST.get("node_id"), node_type__in=NODE_TYPES_LINKABLE,
    )
    topic.related_node = node
    topic.save(update_fields=["related_node"])
    return redirect(f"/publicar/vinculos-tema/#topic-{topic.pk}")


@user_passes_test(is_admin)
@require_POST
def clear_topic_node_link(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    topic.related_node = None
    topic.save(update_fields=["related_node"])
    return redirect(f"/publicar/vinculos-tema/#topic-{topic.pk}")


@user_passes_test(is_admin)
def node_options(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"nodes": []})

    nodes = KnowledgeNode.objects.filter(
        node_type__in=NODE_TYPES_LINKABLE,
    ).filter(
        Q(name__icontains=query) | Q(code__icontains=query)
    )[:20]

    data = [{"id": n.id, "label": f"{n.code} — {n.name}"} for n in nodes]
    return JsonResponse({"nodes": data})
