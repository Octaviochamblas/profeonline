from django.urls import path
from apps.content.views import (
    LevelCreateView,
    LevelDeleteView,
    LevelListView,
    LevelUpdateView,
)

urlpatterns = [
    path("levels/", LevelListView.as_view(), name="level_list"),
    path("levels/create/", LevelCreateView.as_view(), name="level_create"),
    path("levels/<int:pk>/edit/", LevelUpdateView.as_view(), name="level_update"),
    path("levels/<int:pk>/delete/", LevelDeleteView.as_view(), name="level_delete"),
]