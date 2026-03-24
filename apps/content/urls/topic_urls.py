from django.urls import path
from apps.content.views import (
    TopicCreateView,
    TopicDeleteView,
    TopicListView,
    TopicUpdateView,
)

urlpatterns = [
    path("topics/", TopicListView.as_view(), name="topic_list"),
    path("topics/create/", TopicCreateView.as_view(), name="topic_create"),
    path("topics/<int:pk>/edit/", TopicUpdateView.as_view(), name="topic_update"),
    path("topics/<int:pk>/delete/", TopicDeleteView.as_view(), name="topic_delete"),
]