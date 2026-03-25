from django.urls import reverse
from django.views.generic import CreateView
from apps.content.forms import ModuleForm
from apps.content.models import Module
from .mixins import AdminRequiredMixin


class ModuleCreateView(AdminRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = "pages/module_form.html"

    def get_success_url(self):
        return reverse("content:module_update", kwargs={"pk": self.object.pk})