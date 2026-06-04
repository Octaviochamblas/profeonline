from django.urls import reverse_lazy
from django.views.generic import UpdateView
from apps.content.forms import AreaForm
from apps.content.models import Area
from .mixins import AdminRequiredMixin


class AreaUpdateView(AdminRequiredMixin, UpdateView):
    model = Area
    form_class = AreaForm
    template_name = "pages/area_form.html"
    success_url = reverse_lazy("content:area_list")
