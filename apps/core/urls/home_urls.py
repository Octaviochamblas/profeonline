from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from apps.core.views import HomeView, robots_txt, sitemap_xml

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("favicon.ico", RedirectView.as_view(url=static("img/favicon.svg")), name="favicon"),
    path("robots.txt", robots_txt, name="robots"),
    path("sitemap.xml", sitemap_xml, name="sitemap"),
]
