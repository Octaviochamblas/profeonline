from django.urls import reverse_lazy
from django.views.generic import UpdateView
from apps.content.forms import TopicForm
from apps.content.models import Topic
from .mixins import AdminRequiredMixin


class TopicUpdateView(AdminRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = "pages/topic_form.html"
    success_url = reverse_lazy("content:topic_list")
    
