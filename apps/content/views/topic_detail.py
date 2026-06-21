from django.views.generic import DetailView

from apps.content.models import Topic
from apps.content.services.evaluation_service import get_topic_exam_info
from apps.content.services.progress_service import (
    get_resources_progress,
    summarize_topic_progress,
)
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
        progress_map = get_resources_progress(
            self.request.user,
            [resource.id for resource in resources],
        )
        for resource in resources:
            progress = progress_map.get(resource.id, {})
            levels = progress.get("levels_list", [])
            if any(level.get("passed") for level in levels):
                resource.academic_status = "approved"
            elif any(level.get("practice_ready") for level in levels):
                resource.academic_status = "prepared"
            elif progress.get("worked_levels"):
                resource.academic_status = "in_progress"
            else:
                resource.academic_status = ""

        context["topic_progress"] = summarize_topic_progress(
            [resource.id for resource in resources],
            progress_map,
        )

        if topic.education_level:
            context["topic_level_label"] = topic.get_education_level_display()
        elif topic.subject and topic.subject.education_level:
            context["topic_level_label"] = topic.subject.get_education_level_display()
        elif resources:
            common_levels = None
            for resource in resources:
                resource_levels = {level.name for level in resource.levels.all()}
                common_levels = (
                    resource_levels
                    if common_levels is None
                    else common_levels & resource_levels
                )
            context["topic_level_label"] = ", ".join(sorted(common_levels or []))
        else:
            context["topic_level_label"] = ""

        # Evaluación final del tema (Fase 7)
        context["topic_exam_info"] = get_topic_exam_info(self.request.user, topic)
        return context
