from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.content.models import Subject
from .mixins import AdminRequiredMixin


class SubjectCreateView(AdminRequiredMixin, CreateView):
    model = Subject
    fields = ["name", "description", "is_active"]
    template_name = "pages/subject_form.html"
    success_url = reverse_lazy("content:subject_list")