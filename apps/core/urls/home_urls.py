from django.urls import path
from apps.core.views import HomeView, robots_txt, sitemap_xml

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("robots.txt", robots_txt, name="robots"),
    path("sitemap.xml", sitemap_xml, name="sitemap"),
]
