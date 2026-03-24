from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.content.models import Topic


class TopicCreateView(CreateView):
    model = Topic
    fields = ["subject", "name", "description", "is_active"]
    template_name = "pages/topic_form.html"
    success_url = reverse_lazy("content:topic_list")
    