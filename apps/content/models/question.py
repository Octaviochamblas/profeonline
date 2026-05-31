from django.db import models


class Question(models.Model):
    """Pregunta de evaluación o preparación asociada a un recurso."""

    LEVEL_CHOICES = [
        (1, "Nivel 1 — Definición"),
        (2, "Nivel 2 — Ejercicios simples"),
        (3, "Nivel 3 — Problemas de aplicación"),
    ]
    MODE_CHOICES = [
        ("preparacion", "Preparación"),
        ("evaluacion", "Evaluación"),
        ("ambas", "Ambas"),
    ]
    STATUS_CHOICES = [
        ("borrador", "Borrador"),
        ("publicada", "Publicada"),
        ("archivada", "Archivada"),
    ]

    resource = models.ForeignKey(
        "content.Resource",
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="recurso",
    )
    level = models.PositiveSmallIntegerField(
        choices=LEVEL_CHOICES,
        verbose_name="nivel",
    )
    mode = models.CharField(
        max_length=15,
        choices=MODE_CHOICES,
        default="ambas",
        verbose_name="modo",
    )
    text = models.TextField(verbose_name="enunciado")
    explanation = models.TextField(
        blank=True,
        verbose_name="explicación",
        help_text="Explicación breve que se muestra tras responder.",
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="borrador",
        verbose_name="estado",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="orden")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["resource", "level", "order"]
        verbose_name = "pregunta"
        verbose_name_plural = "preguntas"

    def __str__(self) -> str:
        return f"[N{self.level}] {self.text[:80]}"


class Choice(models.Model):
    """Alternativa de selección múltiple para una pregunta."""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name="pregunta",
    )
    text = models.CharField(max_length=500, verbose_name="texto")
    is_correct = models.BooleanField(default=False, verbose_name="es correcta")
    order = models.PositiveIntegerField(default=0, verbose_name="orden")

    class Meta:
        ordering = ["question", "order"]
        verbose_name = "alternativa"
        verbose_name_plural = "alternativas"

    def __str__(self) -> str:
        mark = "✓" if self.is_correct else "✗"
        return f"{mark} {self.text[:60]}"
