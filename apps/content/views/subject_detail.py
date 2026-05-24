from django.db.models import Prefetch
from django.views.generic import DetailView

from apps.content.models import Resource, Subject, Topic
from apps.content.views._seo import breadcrumb_schema, build_breadcrumbs


class SubjectDetailView(DetailView):
    model = Subject
    template_name = "pages/subject_detail.html"
    context_object_name = "subject"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        queryset = Subject.objects.select_related("area").prefetch_related(
            Prefetch(
                "resources",
                queryset=Resource.objects.filter(is_published=True).select_related(
                    "subject",
                    "topic",
                ).prefetch_related("levels"),
                to_attr="published_resources",
            ),
            Prefetch(
                "topics",
                queryset=Topic.objects.filter(is_active=True).order_by("name"),
                to_attr="active_topics",
            ),
        )

        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return queryset

        return queryset.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.object
        breadcrumbs = build_breadcrumbs(
            self.request,
            ("Asignaturas", "content:subject_list", None),
            (subject.name, None, None),
        )

        context["breadcrumbs"] = breadcrumbs
        context["resources"] = getattr(subject, "published_resources", [])
        context["topics"] = getattr(subject, "active_topics", [])
        context["structured_data_json_list"] = [breadcrumb_schema(breadcrumbs)]
        return context
