from django.views.generic import DetailView

from apps.content.models import Area, Resource, Subject, Topic
from apps.content.views._seo import breadcrumb_schema, build_breadcrumbs


class AreaDetailView(DetailView):
    model = Area
    template_name = "pages/area_detail.html"
    context_object_name = "area"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        queryset = Area.objects.all()
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return queryset
        return queryset.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area = self.object

        breadcrumbs = build_breadcrumbs(
            self.request,
            ("Areas", "content:area_list", None),
            (area.name, None, None),
        )
        context["breadcrumbs"] = breadcrumbs

        subjects = Subject.objects.filter(area=area, is_active=True).order_by("name")
        context["subjects"] = subjects
        context["topics"] = Topic.objects.filter(
            subject__area=area,
            is_active=True,
        ).select_related("subject").order_by("subject__name", "name")
        context["resources"] = Resource.objects.filter(
            subject__area=area,
            is_published=True,
        ).select_related("subject", "topic").prefetch_related("levels").order_by("title")
        context["structured_data_json_list"] = [breadcrumb_schema(breadcrumbs)]
        return context
