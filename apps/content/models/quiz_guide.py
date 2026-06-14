from django.db import models


class QuizGuide(models.Model):
    """Guía/material de referencia reutilizable para mimetizar ejercicios.

    El profesor sube un material (PDF, Word, texto…); se extrae y normaliza su
    contenido a ``content_text`` (compacto, barato en tokens). La guía se vincula a
    recursos, temas o asignaturas, de modo que una misma guía sirva para muchos
    recursos. Al generar preguntas, su texto se inyecta en el prompt como ejemplar
    de estilo y como fuente de contenido.
    """

    title = models.CharField(max_length=200, verbose_name="título")
    description = models.CharField(max_length=300, blank=True, verbose_name="descripción")
    source_filename = models.CharField(
        max_length=255, blank=True, verbose_name="archivo de origen"
    )
    content_text = models.TextField(
        verbose_name="texto normalizado",
        help_text="Texto limpio y compacto extraído del material; es lo que lee la IA.",
    )
    is_active = models.BooleanField(default=True, verbose_name="activa")

    # Vínculos reutilizables: la guía aplica a estos recursos, temas o asignaturas.
    resources = models.ManyToManyField(
        "content.Resource", blank=True, related_name="quiz_guides", verbose_name="recursos"
    )
    topics = models.ManyToManyField(
        "content.Topic", blank=True, related_name="quiz_guides", verbose_name="temas"
    )
    subjects = models.ManyToManyField(
        "content.Subject", blank=True, related_name="quiz_guides", verbose_name="asignaturas"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "guía de referencia"
        verbose_name_plural = "guías de referencia"

    def __str__(self) -> str:
        return self.title
