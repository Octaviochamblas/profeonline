from django.db import models
from django.utils.text import slugify


class Subject(models.Model):
    # Mismo conjunto que Topic.EDUCATION_LEVEL_CHOICES; se duplica a propósito para
    # evitar un import cruzado entre modelos.
    EDUCATION_LEVEL_CHOICES = [
        ("escolar", "Escolar (hasta 13 años)"),
        ("media", "Media preuniversitaria (14-17 años)"),
        ("universitaria", "Universitaria (18+)"),
    ]

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
    education_level = models.CharField(
        max_length=20,
        choices=EDUCATION_LEVEL_CHOICES,
        default="",
        blank=True,
        verbose_name="nivel educativo",
        help_text="Nivel por defecto que heredan los temas/recursos sin nivel propio.",
    )
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
