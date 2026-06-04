import unicodedata
from urllib.parse import urlencode

from django.db.models import Q
from django.views.generic import ListView

from apps.content.models import Subject, Topic, Level


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


class TopicListView(ListView):
    model = Topic
    template_name = "pages/topic_list.html"
    context_object_name = "topics"
    paginate_by = 20

    def get_queryset(self):
        queryset = Topic.objects.filter(is_active=True).select_related("subject").order_by("name")

        q = self.request.GET.get("q", "").strip()
        if q:
            normalized_q = remove_accents(q).lower()
            matched_ids = []
            for t in queryset:
                name_norm = remove_accents(t.name).lower()
                desc_norm = remove_accents(t.description or "").lower()
                subj_norm = remove_accents(t.subject.name if t.subject else "").lower()
                if normalized_q in name_norm or normalized_q in desc_norm or normalized_q in subj_norm:
                    matched_ids.append(t.id)
            queryset = queryset.filter(id__in=matched_ids)

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

        # Group the filtered topics by their subject. A subject is shown whenever
        # it has at least one (active) topic — independent of whether it has
        # resources linked to a level. Previously the subjects were derived from
        # ``resources__levels``, which silently hid every topic of a subject that
        # had no leveled resources (e.g. a brand-new subject/topic).
        filtered_topics = list(self.get_queryset())

        # Sort order per subject = order of its lowest associated level. Subjects
        # without leveled resources still appear, sorted last. This is a constant
        # number of queries (one per level), independent of the topic count, so
        # the listing stays O(1) w.r.t. the number of topics.
        levels = list(Level.objects.filter(is_active=True).order_by("order"))
        fallback_order = (levels[-1].order + 1) if levels else 0
        subject_level_order = {}
        for lvl in levels:
            for subject_id in (
                Subject.objects.filter(is_active=True, levels=lvl)
                .values_list("id", flat=True)
                .distinct()
            ):
                subject_level_order.setdefault(subject_id, lvl.order)

        groups_by_subject = {}
        for topic in filtered_topics:
            group = groups_by_subject.get(topic.subject_id)
            if group is None:
                group = {"subject": topic.subject, "topics": []}
                groups_by_subject[topic.subject_id] = group
            group["topics"].append(topic)

        subjects_data = sorted(
            groups_by_subject.values(),
            key=lambda g: (
                subject_level_order.get(g["subject"].id, fallback_order),
                g["subject"].name,
            ),
        )

        # Batch query progress for all topics to avoid N+1
        topic_ids = [t.id for t in filtered_topics]
        from apps.content.selectors.evaluation_selectors import get_topics_progress_map
        progress_map = get_topics_progress_map(self.request.user, topic_ids)

        for group in subjects_data:
            for t in group["topics"]:
                t.progress = progress_map.get(t.id, {
                    "total": 0, "viewed": 0, "approved": 0, "stars": 0, "completed": 0, "percentage": 0
                })

        context["subjects_data"] = subjects_data
        return context
