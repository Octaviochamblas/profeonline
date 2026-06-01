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

        # Group filtered topics by subject, sorted by Level order (Escolar -> Media/Preuni -> Universitario)
        filtered_topics = self.get_queryset()
        subjects_data = []

        # We query levels ordered by 'order'
        levels = Level.objects.filter(is_active=True).order_by("order")

        # Keep track of subjects already added to avoid duplication
        added_subject_ids = set()

        for lvl in levels:
            # Get subjects matching selected_subject if filtered, otherwise all subjects under this level
            level_subjects = Subject.objects.filter(
                is_active=True,
                resources__levels=lvl
            ).distinct().order_by("name")

            if selected_subject:
                level_subjects = level_subjects.filter(id=selected_subject)

            for subj in level_subjects:
                if subj.id in added_subject_ids:
                    continue

                subj_topics = filtered_topics.filter(subject=subj)
                if subj_topics.exists():
                    subjects_data.append({
                        "subject": subj,
                        "topics": subj_topics,
                        "level": lvl
                    })
                    added_subject_ids.add(subj.id)

        # Batch query progress for all topics to avoid N+1
        topic_ids = [t.id for t in filtered_topics]
        from apps.content.selectors.evaluation_selectors import get_topics_progress_map
        progress_map = get_topics_progress_map(self.request.user, topic_ids)

        for group in subjects_data:
            decorated = []
            for t in group["topics"]:
                t.progress = progress_map.get(t.id, {
                    "total": 0, "viewed": 0, "approved": 0, "stars": 0, "completed": 0, "percentage": 0
                })
                decorated.append(t)
            group["topics"] = decorated

        context["subjects_data"] = subjects_data
        return context
