from django.db.models import Q
from django.views.generic import DetailView

from apps.content.models import Level, Resource, Subject, Topic
from apps.content.views._seo import breadcrumb_schema, build_breadcrumbs


class LevelDetailView(DetailView):
    model = Level
    template_name = "pages/level_detail.html"
    context_object_name = "level"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        queryset = Level.objects.all()
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
        context["subjects"] = Subject.objects.filter(
            is_active=True,
            resources__levels=level,
            resources__is_published=True,
        ).distinct().order_by("name")

        # Query topics that have active/published resources in this level
        q = self.request.GET.get("q", "").strip()
        topics_qs = Topic.objects.filter(
            is_active=True,
            resources__levels=level,
            resources__is_published=True,
        ).distinct().select_related("subject")

        if q:
            topics_qs = topics_qs.filter(name__icontains=q)

        topics = list(topics_qs.order_by("subject__name", "name"))

        # Batch query progress for all topics to avoid N+1
        topic_ids = [t.id for t in topics]
        from apps.content.selectors.evaluation_selectors import get_topics_progress_map
        progress_map = get_topics_progress_map(self.request.user, topic_ids)

        for t in topics:
            t.progress = progress_map.get(t.id, {
                "total": 0, "viewed": 0, "approved": 0, "stars": 0, "completed": 0, "percentage": 0
            })

        context["topics"] = topics
        context["q"] = q
        context["structured_data_json_list"] = [breadcrumb_schema(breadcrumbs)]
        return context
