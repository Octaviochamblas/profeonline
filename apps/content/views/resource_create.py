from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.content.forms import ResourceForm
from apps.content.models import Resource
from .mixins import AdminRequiredMixin


class ResourceCreateView(AdminRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm
    template_name = "pages/resource_form.html"
    success_url = reverse_lazy("content:resource_list")