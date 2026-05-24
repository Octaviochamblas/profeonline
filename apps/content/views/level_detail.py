from django.db.models import Prefetch
from django.views.generic import DetailView

from apps.content.models import Level, Resource, Subject
from apps.content.views._seo import breadcrumb_schema, build_breadcrumbs


class LevelDetailView(DetailView):
    model = Level
    template_name = "pages/level_detail.html"
    context_object_name = "level"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        queryset = Level.objects.prefetch_related(
            Prefetch(
                "resources",
                queryset=Resource.objects.filter(is_published=True).select_related(
                    "subject",
                    "topic",
                ).prefetch_related("levels"),
                to_attr="published_resources",
            )
        )

        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return queryset

        return queryset.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        level = self.object
        breadcrumbs = build_breadcrumbs(
            self.request,
            ("Niveles", "content:level_list", None),
            (level.name, None, None),
        )

        context["breadcrumbs"] = breadcrumbs
        context["resources"] = getattr(level, "published_resources", [])
        context["subjects"] = Subject.objects.filter(
            is_active=True,
            resources__levels=level,
            resources__is_published=True,
        ).distinct().order_by("name")
        context["structured_data_json_list"] = [breadcrumb_schema(breadcrumbs)]
        return context
