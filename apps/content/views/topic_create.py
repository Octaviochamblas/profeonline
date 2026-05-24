from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.content.forms import TopicForm
from .mixins import AdminRequiredMixin


class TopicCreateView(AdminRequiredMixin, CreateView):
    form_class = TopicForm
    template_name = "pages/topic_form.html"
    success_url = reverse_lazy("content:topic_list")
    
