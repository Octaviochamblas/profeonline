from django.views.generic import DetailView
from apps.content.models import Resource


class ResourceDetailView(DetailView):
    model = Resource
    template_name = "pages/resource_detail.html"
    context_object_name = "resource"