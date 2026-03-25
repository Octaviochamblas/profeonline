from django.urls import reverse_lazy
from django.views.generic import UpdateView
from apps.content.models import Subject
from .mixins import AdminRequiredMixin


class SubjectUpdateView(AdminRequiredMixin, UpdateView):
    model = Subject
    fields = ["name", "description", "is_active"]
    template_name = "pages/subject_form.html"
    success_url = reverse_lazy("content:subject_list")