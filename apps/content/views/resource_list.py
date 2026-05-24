from urllib.parse import urlencode

from django.views.generic import ListView
from apps.content.models import Level, Resource, Subject, Topic
from apps.content.selectors import get_published_resources


class ResourceListView(ListView):
    model = Resource
    template_name = "pages/resource_list.html"
    context_object_name = "resources"
    paginate_by = 20

    def _clean_id(self, name):
        value = self.request.GET.get(name, "")
        return value if value.isdigit() else ""

    def get_selected_filters(self):
        if hasattr(self, "_selected_filters"):
            return self._selected_filters

        subject_id = self._clean_id("subject")
        topic_id = self._clean_id("topic")
        level_id = self._clean_id("level")

        if subject_id and not Subject.objects.filter(pk=subject_id, is_active=True).exists():
            subject_id = ""

        if level_id and not Level.objects.filter(pk=level_id, is_active=True).exists():
            level_id = ""

        if topic_id:
            topics = Topic.objects.filter(pk=topic_id, is_active=True)
            if subject_id:
                topics = topics.filter(subject_id=subject_id)

            if not topics.exists():
                topic_id = ""

        q = self.request.GET.get("q", "").strip()

        self._selected_filters = {
            "subject": subject_id,
            "topic": topic_id,
            "level": level_id,
            "q": q,
        }
        return self._selected_filters

    def get_queryset(self):
        selected_filters = self.get_selected_filters()
        return get_published_resources(
            subject_id=selected_filters["subject"] or None,
            topic_id=selected_filters["topic"] or None,
            level_id=selected_filters["level"] or None,
            q=selected_filters["q"] or None,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_filters = self.get_selected_filters()
        selected_subject = selected_filters["subject"]
        selected_topic = selected_filters["topic"]
        selected_level = selected_filters["level"]
        selected_q = selected_filters["q"]

        selected_subject_obj = (
            Subject.objects.filter(pk=selected_subject, is_active=True).first()
            if selected_subject
            else None
        )
        selected_topic_obj = (
            Topic.objects.select_related("subject")
            .filter(pk=selected_topic, is_active=True)
            .first()
            if selected_topic
            else None
        )
        selected_level_obj = (
            Level.objects.filter(pk=selected_level, is_active=True).first()
            if selected_level
            else None
        )

        active_filters = []
        if selected_q:
            active_filters.append({"label": "Búsqueda", "value": selected_q})
        if selected_subject_obj:
            active_filters.append(
                {"label": "Asignatura", "value": selected_subject_obj.name}
            )
        if selected_topic_obj:
            active_filters.append(
                {
                    "label": "Tema",
                    "value": f"{selected_topic_obj.subject.name} - {selected_topic_obj.name}",
                }
            )
        if selected_level_obj:
            active_filters.append({"label": "Nivel", "value": selected_level_obj.name})

        filter_querystring = urlencode(
            {key: value for key, value in selected_filters.items() if value}
        )

        context["subjects"] = Subject.objects.filter(is_active=True)

        if selected_subject:
            context["topics"] = Topic.objects.filter(
                is_active=True,
                subject_id=selected_subject,
            ).select_related("subject")
        else:
            context["topics"] = Topic.objects.filter(
                is_active=True
            ).select_related("subject")

        context["levels"] = Level.objects.filter(is_active=True).order_by("order", "name")
        context["selected_subject"] = selected_subject
        context["selected_topic"] = selected_topic
        context["selected_level"] = selected_level
        context["selected_q"] = selected_q
        context["active_filters"] = active_filters
        context["has_active_filters"] = bool(active_filters)
        context["filter_querystring"] = filter_querystring
        return context
