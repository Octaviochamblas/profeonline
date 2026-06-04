from django.db import models
from django.utils.text import slugify


class Subject(models.Model):
    area = models.ForeignKey(
        "content.Area",
        on_delete=models.SET_NULL,
        related_name="subjects",
        verbose_name="área",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    levels = models.ManyToManyField(
        "content.Level",
        blank=True,
        related_name="subjects",
        verbose_name="niveles",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "asignatura"
        verbose_name_plural = "asignaturas"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Subject.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
