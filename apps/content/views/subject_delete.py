from django.urls import reverse_lazy
from django.views.generic import DeleteView
from apps.content.models import Subject


class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = "pages/subject_confirm_delete.html"
    success_url = reverse_lazy("content:subject_list")