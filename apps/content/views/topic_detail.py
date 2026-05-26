from django.db.models import Min, Value
from django.db.models.functions import Coalesce
from django.views.generic import DetailView

from apps.content.models import Topic
from apps.content.views._seo import breadcrumb_schema, build_breadcrumbs


class TopicDetailView(DetailView):
    model = Topic
    template_name = "pages/topic_detail.html"
    context_object_name = "topic"

    def get_queryset(self):
        return Topic.objects.filter(is_active=True).select_related("subject")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.object

        # Breadcrumbs and structured data for SEO
        breadcrumb_items = []
        subject = topic.subject
        if subject and (subject.is_active or self.request.user.is_superuser):
            breadcrumb_items.append(
                (subject.name, "content:subject_detail", {"slug": subject.slug})
            )
        breadcrumb_items.append((topic.name, None, None))
        breadcrumbs = build_breadcrumbs(self.request, *breadcrumb_items)
        context["breadcrumbs"] = breadcrumbs
        context["structured_data_json_list"] = [breadcrumb_schema(breadcrumbs)]

        # Order resources based on the topic's selected ordering method
        context["resources"] = topic.get_ordered_resources()
        return context
