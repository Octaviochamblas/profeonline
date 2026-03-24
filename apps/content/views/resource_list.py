from django.views.generic import ListView
from apps.content.models import Resource, Subject, Topic
from apps.content.selectors import get_published_resources


class ResourceListView(ListView):
    model = Resource
    template_name = "pages/resource_list.html"
    context_object_name = "resources"

    def get_queryset(self):
        subject_slug = self.request.GET.get("subject")
        topic_slug = self.request.GET.get("topic")
        return get_published_resources(subject_slug=subject_slug, topic_slug=topic_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subjects"] = Subject.objects.filter(is_active=True)
        context["topics"] = Topic.objects.filter(is_active=True).select_related("subject")
        context["selected_subject"] = self.request.GET.get("subject", "")
        context["selected_topic"] = self.request.GET.get("topic", "")
        return context