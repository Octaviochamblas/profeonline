from django.urls import path
from apps.content.views import (
    SubjectCreateView,
    SubjectDeleteView,
    SubjectListView,
    SubjectUpdateView,
)

urlpatterns = [
    path("asignaturas/", SubjectListView.as_view(), name="subject_list"),
    path("asignaturas/crear/", SubjectCreateView.as_view(), name="subject_create"),
    path("asignaturas/<int:pk>/editar/", SubjectUpdateView.as_view(), name="subject_update"),
    path("asignaturas/<int:pk>/eliminar/", SubjectDeleteView.as_view(), name="subject_delete"),
]
