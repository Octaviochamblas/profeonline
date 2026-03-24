from django.urls import reverse_lazy
from django.views.generic import UpdateView
from apps.content.forms import ResourceForm
from apps.content.models import Resource


class ResourceUpdateView(UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = "pages/resource_form.html"
    success_url = reverse_lazy("content:resource_list")