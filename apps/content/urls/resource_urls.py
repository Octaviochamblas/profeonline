from django.urls import path
from apps.content.views import (
    ResourceCreateView,
    ResourceDeleteView,
    ResourceDetailView,
    ResourceListView,
    ResourceUpdateView,
)

urlpatterns = [
    path("resources/", ResourceListView.as_view(), name="resource_list"),
    path("resources/create/", ResourceCreateView.as_view(), name="resource_create"),
    path("resources/<int:pk>/", ResourceDetailView.as_view(), name="resource_detail"),
    path("resources/<int:pk>/edit/", ResourceUpdateView.as_view(), name="resource_update"),
    path("resources/<int:pk>/delete/", ResourceDeleteView.as_view(), name="resource_delete"),
]