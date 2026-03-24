from django.urls import reverse_lazy
from django.views.generic import UpdateView
from apps.content.models import Module


class ModuleUpdateView(UpdateView):
    model = Module
    fields = [
        "title",
        "subject",
        "topic",
        "levels",
        "resources",
        "objective",
        "description",
        "order",
        "is_published",
    ]
    template_name = "pages/module_form.html"
    success_url = reverse_lazy("content:module_list")
    