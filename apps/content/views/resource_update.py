from django.urls import reverse_lazy
from django.views.generic import UpdateView
from apps.content.forms import ResourceForm
from apps.content.models import Resource
from .mixins import AdminRequiredMixin


class ResourceUpdateView(AdminRequiredMixin, UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = "pages/resource_form.html"
    success_url = reverse_lazy("content:resource_list")