import re
from django.db.models import Q
from django.views.generic import DetailView

from apps.content.models import Resource
from apps.content.views._seo import article_schema, breadcrumb_schema, build_breadcrumbs


def get_youtube_id(url):
    if not url:
        return None
    regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(regex, url)
    return match.group(1) if match else None


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
        context["youtube_id"] = get_youtube_id(resource.video_url)
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
        related_resources = Resource.objects.filter(is_published=True).exclude(pk=resource.pk)

        related_filters = Q()
        has_related_filters = False
        if resource.subject_id:
            related_filters |= Q(subject=resource.subject)
            has_related_filters = True
        if resource.topic_id:
            related_filters |= Q(topic=resource.topic)
            has_related_filters = True

        level_ids = list(resource.levels.values_list("id", flat=True))
        if level_ids:
            related_filters |= Q(levels__in=level_ids)
            has_related_filters = True

        if has_related_filters:
            related_resources = related_resources.filter(related_filters)
        else:
            related_resources = related_resources.none()

        context["related_resources"] = related_resources.select_related(
            "subject",
            "topic",
        ).prefetch_related(
            "levels",
        ).distinct().order_by("-created_at", "title")[:6]
        context["structured_data_json_list"] = [
            breadcrumb_schema(breadcrumbs),
            article_schema(
                resource,
                self.request.build_absolute_uri(self.request.path),
                resource.subject.name if resource.subject else None,
            ),
        ]
        return context
