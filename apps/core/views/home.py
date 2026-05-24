from django.views.generic import TemplateView

from apps.content.models import Area, Level, Resource, Subject


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_areas"] = Area.objects.filter(is_active=True).order_by("order", "name")[:3]
        context["featured_subjects"] = Subject.objects.filter(is_active=True).select_related("area").order_by("name")[:4]
        context["featured_levels"] = Level.objects.filter(is_active=True).order_by("order", "name")[:4]
        context["featured_resources"] = Resource.objects.filter(is_published=True).select_related(
            "subject",
            "topic",
        ).prefetch_related(
            "levels",
        ).order_by("-created_at", "title")[:4]
        return context
