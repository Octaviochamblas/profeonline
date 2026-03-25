from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.content.forms import ModuleForm
from apps.content.models import Level, Module, Subject, Topic


class ModuleCreateView(CreateView):
    model = Module
    form_class = ModuleForm
    template_name = "pages/module_form.html"
    success_url = reverse_lazy("content:module_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subjects"] = Subject.objects.filter(is_active=True)
        context["topics"] = Topic.objects.filter(is_active=True).select_related("subject")
        context["levels_filter"] = Level.objects.filter(is_active=True).order_by("order", "name")
        context["selected_resource_ids"] = []
        return context