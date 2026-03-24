from django.views.generic import ListView
from apps.content.models import Level


class LevelListView(ListView):
    model = Level
    template_name = "pages/level_list.html"
    context_object_name = "levels"

    def get_queryset(self):
        return Level.objects.filter(is_active=True).order_by("order", "name")