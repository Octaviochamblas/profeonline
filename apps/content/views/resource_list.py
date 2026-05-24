from django.views.generic import ListView
from apps.content.models import Level, Resource, Subject, Topic
from apps.content.selectors import get_published_resources


class ResourceListView(ListView):
    model = Resource
    template_name = "pages/resource_list.html"
    context_object_name = "resources"
    paginate_by = 20

    def _clean_id(self, name):
        value = self.request.GET.get(name, "")
        return value if value.isdigit() else ""

    def get_selected_filters(self):
        if hasattr(self, "_selected_filters"):
            return self._selected_filters

        subject_id = self._clean_id("subject")
        topic_id = self._clean_id("topic")
        level_id = self._clean_id("level")

        if topic_id:
            topics = Topic.objects.filter(pk=topic_id, is_active=True)
            if subject_id:
                topics = topics.filter(subject_id=subject_id)

            if not topics.exists():
                topic_id = ""

        self._selected_filters = {
            "subject": subject_id,
            "topic": topic_id,
            "level": level_id,
        }
        return self._selected_filters

    def get_queryset(self):
        selected_filters = self.get_selected_filters()
        return get_published_resources(
            subject_id=selected_filters["subject"] or None,
            topic_id=selected_filters["topic"] or None,
            level_id=selected_filters["level"] or None,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_filters = self.get_selected_filters()
        selected_subject = selected_filters["subject"]

        context["subjects"] = Subject.objects.filter(is_active=True)

        if selected_subject:
            context["topics"] = Topic.objects.filter(
                is_active=True,
                subject_id=selected_subject,
            ).select_related("subject")
        else:
            context["topics"] = Topic.objects.filter(
                is_active=True
            ).select_related("subject")

        context["levels"] = Level.objects.filter(is_active=True).order_by("order", "name")
        context["selected_subject"] = selected_subject
        context["selected_topic"] = selected_filters["topic"]
        context["selected_level"] = selected_filters["level"]
        return context
