from django.views.generic import ListView
from apps.content.models import Subject


class SubjectListView(ListView):
    model = Subject
    template_name = "pages/subject_list.html"
    context_object_name = "subjects"

    def get_queryset(self):
        return Subject.objects.filter(is_active=True)