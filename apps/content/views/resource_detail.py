from django.views.generic import DetailView
from apps.content.models import Resource


class ResourceDetailView(DetailView):
    model = Resource
    template_name = "pages/resource_detail.html"
    context_object_name = "resource"

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            "subject",
            "topic",
        ).prefetch_related(
            "levels",
        )

        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return queryset

        return queryset.filter(is_published=True)
