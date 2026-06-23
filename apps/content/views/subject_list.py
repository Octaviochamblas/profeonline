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

        normalized_query = remove_accents(search_query).lower() if search_query else ""

        # Todas las asignaturas activas en UNA consulta, con el área y los niveles
        # precargados. Así el agrupado por nivel y el render (subject.area) no
        # disparan N+1 (antes: una query por nivel + una por tarjeta de asignatura).
        subjects_qs = (
            Subject.objects.filter(is_active=True)
            .select_related("area")
            .prefetch_related("levels")
            .order_by("name")
        )
        if context["selected_area"]:
            subjects_qs = subjects_qs.filter(area_id=context["selected_area"])

        subjects = list(subjects_qs)
        if normalized_query:
            # Filtrado en Python para sortear la insensibilidad a acentos del motor.
            subjects = [
                s for s in subjects
                if normalized_query in remove_accents(s.name).lower()
                or normalized_query in remove_accents(s.description or "").lower()
            ]

        # Niveles ordenados (1 query). Agrupamos en memoria sobre la lista ya
        # cargada: una asignatura aparece bajo cada uno de sus niveles. Los
        # `prefetch` evitan tocar la base dentro del loop.
        levels = list(Level.objects.filter(is_active=True).order_by("order"))
        levels_data = []
        for level in levels:
            group_subjects = [s for s in subjects if level in s.levels.all()]
            if group_subjects:
                levels_data.append({"level": level, "subjects": group_subjects})

        # Asignaturas sin ningún nivel (p. ej. recién creadas) van a un grupo
        # final para no ocultarlas del listado.
        orphan_subjects = [s for s in subjects if not s.levels.all()]
        if orphan_subjects:
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
        # El template usa `levels_data`, no `object_list`; mantenemos la consulta
        # mínima y perezosa (con `area` precargada por si se itera).
        return (
            Subject.objects.filter(is_active=True)
            .select_related("area")
            .order_by("name")
        )
