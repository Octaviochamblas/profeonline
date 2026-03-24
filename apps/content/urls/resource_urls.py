from django.urls import path
from apps.content.views import ResourceListView

urlpatterns = [
    path("resources/", ResourceListView.as_view(), name="resource_list"),
]