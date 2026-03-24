from django.views.generic import ListView
from apps.content.models import Resource
from apps.content.selectors import get_published_resources


class ResourceListView(ListView):
    model = Resource
    template_name = "pages/resource_list.html"
    context_object_name = "resources"

    def get_queryset(self):
        return get_published_resources()