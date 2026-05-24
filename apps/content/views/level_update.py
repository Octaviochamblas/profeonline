from django.urls import reverse_lazy
from django.views.generic import UpdateView
from apps.content.forms import LevelForm
from .mixins import AdminRequiredMixin


class LevelUpdateView(AdminRequiredMixin, UpdateView):
    form_class = LevelForm
    template_name = "pages/level_form.html"
    success_url = reverse_lazy("content:level_list")
