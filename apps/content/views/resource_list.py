from django.views.generic import ListView
from apps.content.models import Level, Resource, Subject, Topic
from apps.content.selectors import get_published_resources


class ResourceListView(ListView):
    model = Resource
    template_name = "pages/resource_list.html"
    context_object_name = "resources"
    paginate_by = 20

    def get_queryset(self):
        subject_id = self.request.GET.get("subject")
        topic_id = self.request.GET.get("topic")
        level_id = self.request.GET.get("level")

        return get_published_resources(
            subject_id=subject_id or None,
            topic_id=topic_id or None,
            level_id=level_id or None,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_subject = self.request.GET.get("subject", "")
        selected_topic = self.request.GET.get("topic", "")
        selected_level = self.request.GET.get("level", "")

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
        context["selected_topic"] = selected_topic
        context["selected_level"] = selected_level
        return context