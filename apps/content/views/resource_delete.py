from django.urls import reverse_lazy
from django.views.generic import DeleteView
from apps.content.models import Resource


class ResourceDeleteView(DeleteView):
    model = Resource
    template_name = "pages/resource_confirm_delete.html"
    success_url = reverse_lazy("content:resource_list")