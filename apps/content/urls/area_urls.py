from django.urls import path
from apps.content.views import AreaDetailView, AreaListView

urlpatterns = [
    path("areas/", AreaListView.as_view(), name="area_list"),
    path("areas/<slug:slug>/", AreaDetailView.as_view(), name="area_detail"),
]
