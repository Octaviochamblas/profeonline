from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.content.models import Level
from .mixins import AdminRequiredMixin


class LevelCreateView(AdminRequiredMixin, CreateView):
    model = Level
    fields = ["name", "description", "order", "is_active"]
    template_name = "pages/level_form.html"
    success_url = reverse_lazy("content:level_list")