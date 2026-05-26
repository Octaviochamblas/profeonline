from django.db.models import Q
from django.views.generic import DetailView

from apps.content.models import Level, Resource, Subject, Topic
from apps.content.views._seo import breadcrumb_schema, build_breadcrumbs


class SubjectDetailView(DetailView):
    model = Subject
    template_name = "pages/subject_detail.html"
    context_object_name = "subject"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        queryset = Subject.objects.select_related("area")

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

        # Resource search within this subject
        q = self.request.GET.get("q", "").strip()
        context["selected_q"] = q
        resources_qs = Resource.objects.filter(
            subject=subject,
            is_published=True,
        ).select_related("topic").prefetch_related("levels").order_by("title")
        if q:
            resources_qs = resources_qs.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        context["resources"] = resources_qs

        # Active topics for this subject
        context["topics"] = Topic.objects.filter(
            subject=subject, is_active=True
        ).order_by("name")

        # Levels that have resources in this subject
        context["levels"] = Level.objects.filter(
            is_active=True,
            resources__subject=subject,
            resources__is_published=True,
        ).distinct().order_by("order", "name")

        context["structured_data_json_list"] = [breadcrumb_schema(breadcrumbs)]
        return context
