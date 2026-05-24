from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.content.forms import SubjectForm
from .mixins import AdminRequiredMixin


class SubjectCreateView(AdminRequiredMixin, CreateView):
    form_class = SubjectForm
    template_name = "pages/subject_form.html"
    success_url = reverse_lazy("content:subject_list")
