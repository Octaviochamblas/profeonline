from django.urls import path
from apps.content.views import AreaListView

urlpatterns = [
    path("areas/", AreaListView.as_view(), name="area_list"),
]
