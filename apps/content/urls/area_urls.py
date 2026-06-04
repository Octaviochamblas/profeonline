from django.urls import path
from apps.content.views import (
    AreaCreateView,
    AreaDeleteView,
    AreaDetailView,
    AreaListView,
    AreaUpdateView,
)

urlpatterns = [
    path("areas/", AreaListView.as_view(), name="area_list"),
    path("areas/crear/", AreaCreateView.as_view(), name="area_create"),
    path("areas/<slug:slug>/", AreaDetailView.as_view(), name="area_detail"),
    path("areas/<int:pk>/editar/", AreaUpdateView.as_view(), name="area_update"),
    path("areas/<int:pk>/eliminar/", AreaDeleteView.as_view(), name="area_delete"),
]
