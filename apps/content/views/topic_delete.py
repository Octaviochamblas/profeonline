from django.urls import reverse_lazy
from django.views.generic import DeleteView
from apps.content.models import Topic
from .mixins import AdminRequiredMixin


class TopicDeleteView(AdminRequiredMixin, DeleteView):
    model = Topic
    template_name = "pages/topic_confirm_delete.html"
    success_url = reverse_lazy("content:topic_list")