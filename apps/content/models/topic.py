from django.db import models
from django.utils.text import slugify


class Topic(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ("escolar", "Escolar (hasta 13 años)"),
        ("media", "Media preuniversitaria (14-17 años)"),
        ("universitaria", "Universitaria (18+)"),
    ]

    subject = models.ForeignKey(
        "content.Subject",
        on_delete=models.CASCADE,
        related_name="topics",
        verbose_name="asignatura",
    )
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    resource_ordering_method = models.CharField(
        max_length=20,
        choices=[
            ("level", "Nivel educativo (básico a avanzado)"),
            ("alphabetical", "Alfabético-numérico por título"),
            ("created_asc", "Fecha de creación (antiguo primero)"),
            ("created_desc", "Fecha de creación (reciente primero)"),
            ("manual", "Orden manual (por índice de orden)"),
        ],
        default="level",
        verbose_name="método de ordenación de recursos",
    )
    education_level = models.CharField(
        max_length=20,
        choices=EDUCATION_LEVEL_CHOICES,
        default="",
        blank=True,
        verbose_name="nivel educativo",
    )
    is_active = models.BooleanField(default=True)
    structured_bank_enabled = models.BooleanField(
        default=False,
        verbose_name="banco estandarizado activado",
        help_text="Si está apagado, el tema usa el sistema de evaluación actual.",
    )
    levels = models.ManyToManyField(
        "content.Level",
        blank=True,
        related_name="topics",
        verbose_name="niveles",
    )

    class Meta:
        ordering = ["subject__name", "name"]
        verbose_name = "tema"
        verbose_name_plural = "temas"
        constraints = [
            models.UniqueConstraint(
                fields=["subject", "name"],
                name="unique_topic_name_per_subject",
            )
        ]

    def __str__(self) -> str:
        return f"{self.subject.name} - {self.name}"

    def get_ordered_resources(self):
        from django.db.models import Min, Value
        from django.db.models.functions import Coalesce

        queryset = self.resources.filter(is_published=True).prefetch_related("levels")

        if self.resource_ordering_method == "level":
            return queryset.annotate(
                min_level_order=Coalesce(Min("levels__order"), Value(9999))
            ).order_by("min_level_order", "title")
        elif self.resource_ordering_method == "alphabetical":
            return queryset.order_by("title")
        elif self.resource_ordering_method == "created_asc":
            return queryset.order_by("created_at", "title")
        elif self.resource_ordering_method == "created_desc":
            return queryset.order_by("-created_at", "title")
        elif self.resource_ordering_method == "manual":
            return queryset.order_by("order", "title")

        return queryset.order_by("title")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Topic.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
