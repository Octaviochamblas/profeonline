from django.urls import reverse_lazy
from django.views.generic import DeleteView
from apps.content.models import Resource
from .mixins import AdminRequiredMixin


class ResourceDeleteView(AdminRequiredMixin, DeleteView):
    model = Resource
    template_name = "pages/resource_confirm_delete.html"
    success_url = reverse_lazy("content:resource_list")