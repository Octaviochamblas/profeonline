from django.views.generic import ListView
from apps.content.models import Module


class ModuleListView(ListView):
    model = Module
    template_name = "pages/module_list.html"
    context_object_name = "modules"

    def get_queryset(self):
        return Module.objects.filter(is_published=True).select_related(
            "subject",
            "topic",
        ).prefetch_related(
            "levels",
        )