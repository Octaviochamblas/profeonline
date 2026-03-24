from django.views.generic import ListView
from apps.content.models import Topic


class TopicListView(ListView):
    model = Topic
    template_name = "pages/topic_list.html"
    context_object_name = "topics"

    def get_queryset(self):
        return Topic.objects.filter(is_active=True).select_related("subject")
    