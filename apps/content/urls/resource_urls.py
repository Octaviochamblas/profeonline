from django.urls import path
from apps.content.views import ResourceDetailView, ResourceListView

urlpatterns = [
    path("resources/", ResourceListView.as_view(), name="resource_list"),
    path("resources/<int:pk>/", ResourceDetailView.as_view(), name="resource_detail"),
]