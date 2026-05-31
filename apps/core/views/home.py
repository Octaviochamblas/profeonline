from django.db.models import Case, IntegerField, Value, When
from django.views.generic import TemplateView

from apps.content.models import Area, Level, Resource, Subject
from apps.content.selectors import get_resume_resource


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # "Continuar donde quedaste" para usuarios autenticados
        last_resource, last_resource_completed = get_resume_resource(self.request.user)
        context["last_resource"] = last_resource
        context["last_resource_completed"] = last_resource_completed
        context["featured_areas"] = Area.objects.filter(is_active=True).order_by("order", "name")[:3]
        priority_subjects = ["Matemática", "Física", "Química"]
        context["featured_subjects"] = (
            Subject.objects.filter(is_active=True)
            .select_related("area")
            .order_by(
                Case(
                    *[
                        When(name=subject_name, then=Value(position))
                        for position, subject_name in enumerate(priority_subjects)
                    ],
                    default=Value(len(priority_subjects)),
                    output_field=IntegerField(),
                ),
                "name",
            )[:3]
        )
        context["featured_levels"] = Level.objects.filter(is_active=True).order_by("order", "name")[:3]
        context["featured_resources"] = Resource.objects.filter(is_published=True).select_related(
            "subject",
            "topic",
        ).prefetch_related(
            "levels",
        ).order_by("-created_at", "title")[:3]
        return context
