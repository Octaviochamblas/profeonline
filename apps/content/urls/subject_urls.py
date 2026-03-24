from django.urls import path
from apps.content.views import (
    SubjectCreateView,
    SubjectDeleteView,
    SubjectListView,
    SubjectUpdateView,
)

urlpatterns = [
    path("subjects/", SubjectListView.as_view(), name="subject_list"),
    path("subjects/create/", SubjectCreateView.as_view(), name="subject_create"),
    path("subjects/<int:pk>/edit/", SubjectUpdateView.as_view(), name="subject_update"),
    path("subjects/<int:pk>/delete/", SubjectDeleteView.as_view(), name="subject_delete"),
]