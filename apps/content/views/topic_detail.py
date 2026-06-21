from django.db.models import Min, Value
from django.db.models.functions import Coalesce
from django.views.generic import DetailView

from apps.content.models import Topic
from apps.content.selectors.evaluation_selectors import (
    get_resource_progress_map,
    get_topics_progress_map,
)
from apps.content.services.evaluation_service import get_topic_exam_info
from apps.content.views._seo import breadcrumb_schema, build_breadcrumbs


class TopicDetailView(DetailView):
    model = Topic
    template_name = "pages/topic_detail.html"
    context_object_name = "topic"

    def get_queryset(self):
        return Topic.objects.filter(is_active=True).select_related("subject")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.object

        # Breadcrumbs and structured data for SEO
        breadcrumb_items = []
        subject = topic.subject
        if subject and (subject.is_active or self.request.user.is_superuser):
            breadcrumb_items.append(
                (subject.name, "content:subject_detail", {"slug": subject.slug})
            )
        breadcrumb_items.append((topic.name, None, None))
        breadcrumbs = build_breadcrumbs(self.request, *breadcrumb_items)
        context["breadcrumbs"] = breadcrumbs
        context["structured_data_json_list"] = [breadcrumb_schema(breadcrumbs)]

        # Order resources based on the topic's selected ordering method
        resources = list(topic.get_ordered_resources())
        context["resources"] = resources
        progress_map = get_resource_progress_map(
            self.request.user,
            [resource.id for resource in resources],
        )
        for resource in resources:
            resource.quiz_progress = progress_map.get(
                resource.id,
                {"viewed": False, "max_level": 0, "stars": 0},
            )

        # Progreso del usuario autenticado dentro de la ruta. El progreso del
        # tema ya no depende de "Comprendido": usa el progreso ponderado
        # (práctica 30% / evaluación 70%) promediado sobre los recursos trabajados.
        total = len(resources)
        topic_progress = get_topics_progress_map(
            self.request.user, [topic.id]
        ).get(topic.id, {})
        context["weighted_percent"] = topic_progress.get("weighted_progress", 0)
        context["worked_count"] = topic_progress.get("worked", 0)
        context["approved_count"] = sum(
            1 for progress in progress_map.values() if progress["max_level"] > 0
        )
        context["total_count"] = total

        # Estrellas alcanzables = niveles con preguntas publicadas por recurso.
        from collections import defaultdict
        from apps.content.models import Question

        published_levels_data = (
            Question.objects.filter(resource__in=resources, status="publicada")
            .values("resource_id", "level")
            .distinct()
        )
        published_levels_by_resource = defaultdict(set)
        for item in published_levels_data:
            published_levels_by_resource[item["resource_id"]].add(item["level"])

        achievable_by_resource = {
            r.id: len(published_levels_by_resource[r.id]) for r in resources
        }
        stars_total = sum(achievable_by_resource.values())

        # Estrellas obtenidas, topadas al máximo alcanzable de cada recurso para que el
        # numerador nunca supere al denominador (evita "3/1" y porcentajes > 100% cuando
        # un nivel aprobado dejó de tener preguntas publicadas).
        stars_count = sum(
            min(progress.get("stars", 0), achievable_by_resource.get(rid, 0))
            for rid, progress in progress_map.items()
        )
        context["stars_count"] = stars_count
        context["stars_total"] = stars_total

        # Porcentajes para las barras de progreso
        context["approved_percent"] = (
            int(context["approved_count"] / total * 100) if total else 0
        )
        context["stars_percent"] = (
            int(stars_count / stars_total * 100) if stars_total else 0
        )
        context["progress_percent"] = context["stars_percent"]

        # Evaluación final del tema (Fase 7)
        context["topic_exam_info"] = get_topic_exam_info(self.request.user, topic)
        return context
