from django.urls import path
from apps.content.views import ContentHomeView

urlpatterns = [
    path("", ContentHomeView.as_view(), name="home"),
]