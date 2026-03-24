from django.urls import reverse_lazy
from django.views.generic import UpdateView
from apps.content.models import Subject


class SubjectUpdateView(UpdateView):
    model = Subject
    fields = ["name", "description", "is_active"]
    template_name = "pages/subject_form.html"
    success_url = reverse_lazy("content:subject_list")