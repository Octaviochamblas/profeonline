from django.urls import reverse_lazy
from django.views.generic import UpdateView
from apps.content.models import Topic
from .mixins import AdminRequiredMixin


class TopicUpdateView(AdminRequiredMixin, UpdateView):
    model = Topic
    fields = ["subject", "name", "description", "is_active"]
    template_name = "pages/topic_form.html"
    success_url = reverse_lazy("content:topic_list")
    