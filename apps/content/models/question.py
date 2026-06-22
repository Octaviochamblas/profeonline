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
    # --- Banco estandarizado por ítems (epic "Guías interactivas", aditivo) ---
    QUESTION_TYPE_CHOICES = [
        ("alternativa", "Alternativa"),
        ("numerica", "Numérica"),
        ("algebraica", "Algebraica"),
    ]
    DIFFICULTY_CHOICES = [
        ("basica", "Básica"),
        ("intermedia", "Intermedia"),
        ("avanzada", "Avanzada"),
        ("desafio", "Desafío"),
    ]
    SCOPE_CHOICES = [
        ("banco_visible", "Banco visible"),
        ("evaluacion_nivel", "Evaluación de nivel"),
        ("prueba_final", "Prueba final"),
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
    publication_item = models.ForeignKey(
        "content.PublicationItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="questions",
    )
    generation_key = models.CharField(max_length=64, blank=True)
    audit_data = models.JSONField(default=dict, blank=True)

    # --- Banco estandarizado por ítems (todo aditivo: nullable o con default) ---
    exercise_item = models.ForeignKey(
        "content.ExerciseItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="questions",
        verbose_name="ítem",
    )
    question_type = models.CharField(
        max_length=12,
        choices=QUESTION_TYPE_CHOICES,
        default="alternativa",
        verbose_name="tipo",
    )
    difficulty = models.CharField(
        max_length=12,
        choices=DIFFICULTY_CHOICES,
        blank=True,
        default="",
        verbose_name="dificultad",
    )
    canonical_answer = models.TextField(blank=True, verbose_name="respuesta canónica")
    answer_tolerance = models.FloatField(null=True, blank=True, verbose_name="tolerancia")
    hint = models.TextField(blank=True, verbose_name="pista")
    points = models.PositiveSmallIntegerField(default=1, verbose_name="puntaje")
    estimated_minutes = models.PositiveSmallIntegerField(
        default=0, verbose_name="minutos estimados"
    )
    scope = models.CharField(
        max_length=20,
        choices=SCOPE_CHOICES,
        blank=True,
        default="",
        verbose_name="ámbito",
        help_text="Vacío = sin clasificar; no entra al sistema nuevo.",
    )
    learning_guide = models.ForeignKey(
        "content.LearningGuide",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bank_questions",
        verbose_name="guía de origen",
    )

    class Meta:
        ordering = ["resource", "level", "order"]
        verbose_name = "pregunta"
        verbose_name_plural = "preguntas"
        constraints = [
            models.UniqueConstraint(
                fields=["publication_item", "generation_key"],
                condition=~models.Q(generation_key=""),
                name="unique_pipeline_question_key",
            ),
        ]

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
