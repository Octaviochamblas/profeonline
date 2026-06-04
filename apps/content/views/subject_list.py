import unicodedata
from django.db.models import Q
from django.views.generic import ListView
from apps.content.models import Area, Subject, Level


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
        area_id = self.request.GET.get("area", "").strip()
        context["search_query"] = search_query
        context["selected_area"] = area_id if area_id.isdigit() else ""
        context["areas"] = Area.objects.filter(is_active=True).order_by("order", "name")

        # Fetch levels ordered by 'order'
        levels = Level.objects.filter(is_active=True).order_by("order")

        normalized_query = remove_accents(search_query).lower() if search_query else ""

        levels_data = []
        for level in levels:
            # Filter subjects that contain resources belonging to this specific level
            level_subjects = Subject.objects.filter(
                is_active=True,
                levels=level
            ).distinct()
            if context["selected_area"]:
                level_subjects = level_subjects.filter(area_id=context["selected_area"])

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

        # Asignaturas activas que no aparecen en ningún nivel (p. ej. una recién
        # creada, sin recursos asociados a un nivel todavía) deben verse igual,
        # en un grupo final, para no ocultarlas del listado.
        orphan_subjects = (
            Subject.objects.filter(is_active=True, levels__isnull=True)
            .distinct()
        )
        if context["selected_area"]:
            orphan_subjects = orphan_subjects.filter(area_id=context["selected_area"])
        if normalized_query:
            matched_ids = []
            for subj in orphan_subjects:
                name_norm = remove_accents(subj.name).lower()
                desc_norm = remove_accents(subj.description or "").lower()
                if normalized_query in name_norm or normalized_query in desc_norm:
                    matched_ids.append(subj.id)
            orphan_subjects = orphan_subjects.filter(id__in=matched_ids)
        orphan_subjects = orphan_subjects.order_by("name")

        if orphan_subjects.exists():
            levels_data.append({
                "level": {
                    "name": "Otras asignaturas",
                    "description": "Asignaturas sin recursos asociados a un nivel todavía.",
                },
                "subjects": orphan_subjects,
            })

        context["levels_data"] = levels_data
        return context

    def get_queryset(self):
        queryset = Subject.objects.filter(is_active=True)
        area_id = self.request.GET.get("area", "").strip()
        if area_id.isdigit():
            queryset = queryset.filter(area_id=area_id)
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
