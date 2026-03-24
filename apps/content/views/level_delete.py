from django.urls import reverse_lazy
from django.views.generic import DeleteView
from apps.content.models import Level


class LevelDeleteView(DeleteView):
    model = Level
    template_name = "pages/level_confirm_delete.html"
    success_url = reverse_lazy("content:level_list")