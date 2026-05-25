from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView, TemplateView
from django.contrib.sitemaps.views import sitemap
from apps.core.views import HomeView, robots_txt
from apps.core.sitemaps import StaticViewSitemap, SubjectSitemap, LevelSitemap, ResourceSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "subjects": SubjectSitemap,
    "levels": LevelSitemap,
    "resources": ResourceSitemap,
}

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("favicon.ico", RedirectView.as_view(url=static("img/favicon.svg")), name="favicon"),
    path("robots.txt", robots_txt, name="robots"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("terminos/", TemplateView.as_view(template_name="pages/terminos.html"), name="terminos"),
    path("privacidad/", TemplateView.as_view(template_name="pages/privacidad.html"), name="privacidad"),
    path("contacto/", TemplateView.as_view(template_name="pages/contacto.html"), name="contacto"),
]
