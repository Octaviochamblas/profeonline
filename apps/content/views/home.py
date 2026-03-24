from django.views.generic import TemplateView


class ContentHomeView(TemplateView):
    template_name = "pages/home.html"