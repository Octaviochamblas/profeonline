from django.urls import path
from apps.content.views import (
    TopicCreateView,
    TopicDeleteView,
    TopicDetailView,
    TopicListView,
    TopicUpdateView,
    topic_options_by_subject,
)

urlpatterns = [
    path("temas/", TopicListView.as_view(), name="topic_list"),
    path("temas/crear/", TopicCreateView.as_view(), name="topic_create"),
    path("temas/<slug:slug>/", TopicDetailView.as_view(), name="topic_detail"),
    path("temas/<int:pk>/editar/", TopicUpdateView.as_view(), name="topic_update"),
    path("temas/<int:pk>/eliminar/", TopicDeleteView.as_view(), name="topic_delete"),
    path("temas/opciones/", topic_options_by_subject, name="topic_options"),
]
