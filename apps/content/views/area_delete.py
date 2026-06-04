from django.urls import reverse_lazy
from django.views.generic import DeleteView
from apps.content.models import Area
from .mixins import AdminRequiredMixin


class AreaDeleteView(AdminRequiredMixin, DeleteView):
    model = Area
    template_name = "pages/area_confirm_delete.html"
    success_url = reverse_lazy("content:area_list")
