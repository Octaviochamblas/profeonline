from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView, TemplateView
from django.contrib.sitemaps.views import sitemap
from apps.core.views import HomeView, robots_txt
from apps.core.sitemaps import (
    AreaSitemap,
    StaticViewSitemap,
    SubjectSitemap,
    LevelSitemap,
    ResourceSitemap,
    TopicSitemap,
)

sitemaps = {
    "static": StaticViewSitemap,
    "areas": AreaSitemap,
    "subjects": SubjectSitemap,
    "topics": TopicSitemap,
    "levels": LevelSitemap,
    "resources": ResourceSitemap,
}


class FaviconRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return static("img/favicon.svg")


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("favicon.ico", FaviconRedirectView.as_view(), name="favicon"),
    path("robots.txt", robots_txt, name="robots"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("terminos/", TemplateView.as_view(template_name="pages/terminos.html"), name="terminos"),
    path("privacidad/", TemplateView.as_view(template_name="pages/privacidad.html"), name="privacidad"),
    path("contacto/", TemplateView.as_view(template_name="pages/contacto.html"), name="contacto"),
]
