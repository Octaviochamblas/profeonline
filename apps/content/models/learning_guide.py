from django.db import models
from django.utils.text import slugify


class LearningGuide(models.Model):
    """Guía ProfeOnline generada (original) a partir de fuentes privadas.

    Parte del sistema de banco estandarizado por ítems (epic "Guías
    interactivas"). En Fase 0 solo existe el esquema; la generación, la
    validación de originalidad y la publicación llegan en fases posteriores.
    """

    VISIBILITY_CHOICES = [
        ("interna", "Interna"),
        ("publica", "Pública"),
    ]
    STATUS_CHOICES = [
        ("borrador", "Borrador"),
        ("publicada", "Publicada"),
    ]

    topic = models.ForeignKey(
        "content.Topic",
        on_delete=models.CASCADE,
        related_name="learning_guides",
        verbose_name="tema",
    )
    title = models.CharField(max_length=200, verbose_name="título")
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    structured_content = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="contenido estructurado",
        help_text=(
            "Intro, resumen, fórmulas, ejemplos resueltos, ejercicios por "
            "ítem/dificultad, desafíos y solucionario."
        ),
    )
    resources = models.ManyToManyField(
        "content.Resource",
        blank=True,
        related_name="learning_guides",
        verbose_name="recursos",
    )
    private_sources = models.ManyToManyField(
        "content.QuizGuide",
        blank=True,
        related_name="derived_guides",
        verbose_name="fuentes privadas utilizadas",
    )
    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default="interna",
        verbose_name="visibilidad",
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="borrador",
        verbose_name="estado",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["topic", "title"]
        verbose_name = "guía ProfeOnline"
        verbose_name_plural = "guías ProfeOnline"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "guia"
            slug = base_slug
            counter = 1
            while LearningGuide.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
