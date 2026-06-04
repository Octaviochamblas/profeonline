from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.content.forms import AreaForm
from .mixins import AdminRequiredMixin


class AreaCreateView(AdminRequiredMixin, CreateView):
    form_class = AreaForm
    template_name = "pages/area_form.html"
    success_url = reverse_lazy("content:area_list")
