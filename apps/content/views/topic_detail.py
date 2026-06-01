from django.db.models import Min, Value
from django.db.models.functions import Coalesce
from django.views.generic import DetailView

from apps.content.models import ResourceCompletion, Topic
from apps.content.selectors.evaluation_selectors import get_resource_progress_map
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

        # Progreso del usuario autenticado dentro de la ruta
        total = len(resources)
        completed_ids = set()
        if self.request.user.is_authenticated and total:
            completed_ids = set(
                ResourceCompletion.objects.filter(
                    user=self.request.user,
                    resource__in=resources,
                ).values_list("resource_id", flat=True)
            )
        context["completed_ids"] = completed_ids
        context["completed_count"] = len(completed_ids)
        context["approved_count"] = sum(
            1 for progress in progress_map.values() if progress["max_level"] > 0
        )
        context["stars_count"] = sum(
            progress["stars"] for progress in progress_map.values()
        )
        context["total_count"] = total

        # Calcular el total de estrellas realmente alcanzables (según niveles publicados por recurso)
        from apps.content.models import Question
        published_levels_data = Question.objects.filter(
            resource__in=resources,
            status="publicada"
        ).values("resource_id", "level").distinct()

        from collections import defaultdict
        published_levels_by_resource = defaultdict(set)
        for item in published_levels_data:
            published_levels_by_resource[item["resource_id"]].add(item["level"])

        stars_total = sum(len(published_levels_by_resource[r.id]) for r in resources)
        context["stars_total"] = stars_total

        # Porcentajes para las barras de progreso
        context["completed_percent"] = (
            int(len(completed_ids) / total * 100) if total else 0
        )
        context["approved_percent"] = (
            int(context["approved_count"] / total * 100) if total else 0
        )
        context["stars_percent"] = (
            int(context["stars_count"] / stars_total * 100) if stars_total else 0
        )
        context["progress_percent"] = context["stars_percent"]

        # Evaluación final del tema (Fase 7)
        context["topic_exam_info"] = get_topic_exam_info(self.request.user, topic)
        return context
