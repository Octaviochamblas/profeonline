import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from apps.content.models import Resource
from apps.content.views._seo import article_schema, breadcrumb_schema, build_breadcrumbs


def get_youtube_id(url):
    if not url:
        return None
    regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(regex, url)
    return match.group(1) if match else None


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resource
    template_name = "pages/resource_detail.html"
    context_object_name = "resource"

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            "subject",
            "topic",
            "topic__subject",
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
        breadcrumb_items = []
        subject = resource.subject
        topic = resource.topic
        if subject and (subject.is_active or self.request.user.is_superuser):
            breadcrumb_items.append(
                (subject.name, "content:subject_detail", {"slug": subject.slug})
            )
        if topic and (topic.is_active or self.request.user.is_superuser):
            breadcrumb_items.append(
                (topic.name, "content:topic_detail", {"slug": topic.slug})
            )
        breadcrumb_items.append((resource.title, None, None))
        breadcrumbs = build_breadcrumbs(self.request, *breadcrumb_items)

        context["breadcrumbs"] = breadcrumbs

        # Determine previous and next resources correlative to the topic's ordering
        previous_resource = None
        next_resource = None
        topic = resource.topic
        if topic:
            ordered_resources = list(topic.get_ordered_resources())
            try:
                current_index = ordered_resources.index(resource)
                if current_index > 0:
                    previous_resource = ordered_resources[current_index - 1]
                if current_index < len(ordered_resources) - 1:
                    next_resource = ordered_resources[current_index + 1]
            except ValueError:
                # If current resource is draft and not in public ordered list
                pass

        context["previous_resource"] = previous_resource
        context["next_resource"] = next_resource

        context["structured_data_json_list"] = [
            breadcrumb_schema(breadcrumbs),
            article_schema(
                resource,
                self.request.build_absolute_uri(self.request.path),
                resource.subject.name if resource.subject else None,
            ),
        ]
        return context
