from django.urls import path
from apps.content.views import (
    LevelCreateView,
    LevelDeleteView,
    LevelListView,
    LevelUpdateView,
)

urlpatterns = [
    path("niveles/", LevelListView.as_view(), name="level_list"),
    path("niveles/crear/", LevelCreateView.as_view(), name="level_create"),
    path("niveles/<int:pk>/editar/", LevelUpdateView.as_view(), name="level_update"),
    path("niveles/<int:pk>/eliminar/", LevelDeleteView.as_view(), name="level_delete"),
]
