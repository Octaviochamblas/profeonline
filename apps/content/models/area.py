from django.db import models
from django.utils.text import slugify


class Area(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="nombre")
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, verbose_name="descripción")
    is_active = models.BooleanField(default=True, verbose_name="activa")
    order = models.PositiveIntegerField(default=0, verbose_name="orden")

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "área"
        verbose_name_plural = "áreas"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Area.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
