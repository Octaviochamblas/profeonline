from django.urls import path
from apps.content.views import (
    ResourceCreateView,
    ResourceDeleteView,
    ResourceDetailView,
    ResourceListView,
    ResourceUpdateView,
    resource_options,
    create_resource_from_video,
    toggle_resource_completion,
)

urlpatterns = [
    path("recursos/", ResourceListView.as_view(), name="resource_list"),
    path("recursos/crear/", ResourceCreateView.as_view(), name="resource_create"),
    path("recursos/opciones/", resource_options, name="resource_options"),
    path("recursos/<slug:slug>/", ResourceDetailView.as_view(), name="resource_detail"),
    path("recursos/<slug:slug>/completar/", toggle_resource_completion, name="resource_toggle_completion"),
    path("recursos/<int:pk>/editar/", ResourceUpdateView.as_view(), name="resource_update"),
    path("recursos/<int:pk>/eliminar/", ResourceDeleteView.as_view(), name="resource_delete"),
    path("api/recursos/crear-video/", create_resource_from_video, name="api_create_resource_from_video"),
]
