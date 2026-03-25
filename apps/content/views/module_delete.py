from django.urls import reverse_lazy
from django.views.generic import DeleteView
from apps.content.models import Module


class ModuleDeleteView(DeleteView):
    model = Module
    template_name = "pages/module_confirm_delete.html"
    success_url = reverse_lazy("content:module_list")