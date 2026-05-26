from urllib.parse import urlencode

from django.db.models import Q
from django.views.generic import ListView

from apps.content.models import Subject, Topic


class TopicListView(ListView):
    model = Topic
    template_name = "pages/topic_list.html"
    context_object_name = "topics"
    paginate_by = 20

    def get_queryset(self):
        queryset = Topic.objects.filter(is_active=True).select_related("subject").order_by("name")

        # Search keyword query
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(subject__name__icontains=q)
            )

        # Subject filter query
        subject_id = self.request.GET.get("subject", "").strip()
        if subject_id and subject_id.isdigit():
            queryset = queryset.filter(subject_id=subject_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_q"] = self.request.GET.get("q", "").strip()

        subject_id = self.request.GET.get("subject", "").strip()
        selected_subject = int(subject_id) if subject_id.isdigit() else ""
        context["selected_subject"] = selected_subject
        context["subjects"] = Subject.objects.filter(is_active=True)
        context["has_active_filters"] = bool(context["selected_q"] or selected_subject)

        # Build filter querystring for pagination
        filters = {}
        if context["selected_q"]:
            filters["q"] = context["selected_q"]
        if selected_subject:
            filters["subject"] = selected_subject
        context["filter_querystring"] = urlencode(filters)

        return context
