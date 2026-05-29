import unicodedata
from django.db.models import Q
from django.views.generic import ListView
from apps.content.models import Subject, Level


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


class SubjectListView(ListView):
    model = Subject
    template_name = "pages/subject_list.html"
    context_object_name = "subjects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("q", "").strip()
        context["search_query"] = search_query

        # Fetch levels ordered by 'order'
        levels = Level.objects.filter(is_active=True).order_by("order")

        normalized_query = remove_accents(search_query).lower() if search_query else ""

        levels_data = []
        for level in levels:
            # Filter subjects that contain resources belonging to this specific level
            level_subjects = Subject.objects.filter(
                is_active=True,
                resources__levels=level
            ).distinct()

            if normalized_query:
                # Filter in Python to bypass database collation limitations (especially SQLite accent-insensitivity)
                matched_ids = []
                for subj in level_subjects:
                    name_norm = remove_accents(subj.name).lower()
                    desc_norm = remove_accents(subj.description or "").lower()
                    if normalized_query in name_norm or normalized_query in desc_norm:
                        matched_ids.append(subj.id)
                level_subjects = level_subjects.filter(id__in=matched_ids)

            if level_subjects.exists():
                levels_data.append({
                    "level": level,
                    "subjects": level_subjects
                })

        context["levels_data"] = levels_data
        return context

    def get_queryset(self):
        queryset = Subject.objects.filter(is_active=True)
        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            normalized_query = remove_accents(search_query).lower()
            matched_ids = []
            for subj in queryset:
                name_norm = remove_accents(subj.name).lower()
                desc_norm = remove_accents(subj.description or "").lower()
                if normalized_query in name_norm or normalized_query in desc_norm:
                    matched_ids.append(subj.id)
            queryset = queryset.filter(id__in=matched_ids)
        return queryset
