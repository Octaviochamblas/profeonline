from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.content.models import Subject, Level, Resource


class SubjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Subject.objects.filter(is_active=True).exclude(slug__isnull=True).exclude(slug="")

    def location(self, item):
        return reverse("content:subject_detail", kwargs={"slug": item.slug})


class LevelSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Level.objects.filter(is_active=True).exclude(slug__isnull=True).exclude(slug="")

    def location(self, item):
        return reverse("content:level_detail", kwargs={"slug": item.slug})


class ResourceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Resource.objects.filter(is_published=True).exclude(slug__isnull=True).exclude(slug="")

    def location(self, item):
        return reverse("content:resource_detail", kwargs={"slug": item.slug})


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return [
            "core:home",
            "content:resource_list",
            "content:area_list",
            "content:subject_list",
            "content:topic_list",
            "content:level_list",
            "content:module_list",
            "core:terminos",
            "core:privacidad",
            "core:contacto",
        ]

    def location(self, item):
        return reverse(item)
