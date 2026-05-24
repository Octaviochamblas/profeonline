from django.views.generic import DetailView

from apps.content.models import Resource
from apps.content.views._seo import article_schema, breadcrumb_schema, build_breadcrumbs


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.object
        breadcrumb_items = [
            ("Recursos", "content:resource_list", None),
        ]
        if resource.subject and (resource.subject.is_active or self.request.user.is_superuser):
            breadcrumb_items.append(
                (
                    resource.subject.name,
                    "content:subject_detail",
                    {"slug": resource.subject.slug},
                )
            )
        breadcrumb_items.append((resource.title, None, None))
        breadcrumbs = build_breadcrumbs(self.request, *breadcrumb_items)

        context["breadcrumbs"] = breadcrumbs
        context["structured_data_json_list"] = [
            breadcrumb_schema(breadcrumbs),
            article_schema(
                resource,
                self.request.build_absolute_uri(self.request.path),
                resource.subject.name if resource.subject else None,
            ),
        ]
        return context
