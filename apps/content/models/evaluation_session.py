from django.conf import settings
from django.db import models


class EvaluationSession(models.Model):
    """Sesión de evaluación por nivel o prueba final.

    El servidor controla el tiempo (`started_at`/`expires_at`) y el estado. En
    Fase 0 solo existe el esquema; el ensamblado, los timers y la corrección
    llegan en Fase 5.
    """

    KIND_CHOICES = [
        ("evaluacion_nivel", "Evaluación por nivel"),
        ("prueba_final", "Prueba final"),
    ]
    STATUS_CHOICES = [
        ("en_curso", "En curso"),
        ("enviada", "Enviada"),
        ("vencida", "Vencida"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="evaluation_sessions",
    )
    topic = models.ForeignKey(
        "content.Topic",
        on_delete=models.CASCADE,
        related_name="evaluation_sessions",
    )
    resource = models.ForeignKey(
        "content.Resource",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="evaluation_sessions",
        help_text="Solo para evaluaciones por nivel.",
    )
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, verbose_name="tipo")
    # 0 = no aplica (prueba final); 1/2/3 = nivel para evaluaciones por nivel.
    level = models.PositiveSmallIntegerField(default=0, verbose_name="nivel")
    attempt_number = models.PositiveSmallIntegerField(verbose_name="nº de intento")
    started_at = models.DateTimeField(verbose_name="inicio")
    expires_at = models.DateTimeField(verbose_name="vencimiento")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="en_curso",
        verbose_name="estado",
    )
    questions = models.ManyToManyField(
        "content.Question",
        through="content.EvaluationSessionQuestion",
        related_name="evaluation_sessions",
        verbose_name="preguntas seleccionadas",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "sesión de evaluación"
        verbose_name_plural = "sesiones de evaluación"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "topic", "kind", "level", "attempt_number"],
                name="unique_evaluation_session",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} — {self.topic} ({self.kind}) #{self.attempt_number}"


class EvaluationSessionQuestion(models.Model):
    """Pregunta seleccionada dentro de una sesión, con su orden de presentación."""

    session = models.ForeignKey(
        "content.EvaluationSession",
        on_delete=models.CASCADE,
        related_name="session_questions",
    )
    question = models.ForeignKey("content.Question", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["session", "order"]
        verbose_name = "pregunta de sesión"
        verbose_name_plural = "preguntas de sesión"
        constraints = [
            models.UniqueConstraint(
                fields=["session", "question"], name="unique_session_question"
            ),
        ]

    def __str__(self) -> str:
        return f"S{self.session_id} · Q{self.question_id}"


class EvaluationSessionAnswer(models.Model):
    """Respuesta detallada dentro de una sesión (sirve nivel y prueba final)."""

    session = models.ForeignKey(
        "content.EvaluationSession",
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question = models.ForeignKey("content.Question", on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(
        "content.Choice",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evaluation_session_answers",
    )
    text_answer = models.TextField(blank=True, verbose_name="texto ingresado")
    is_correct = models.BooleanField(default=False, verbose_name="es correcta")
    points_awarded = models.FloatField(default=0, verbose_name="puntaje otorgado")

    class Meta:
        verbose_name = "respuesta de sesión de evaluación"
        verbose_name_plural = "respuestas de sesión de evaluación"
        constraints = [
            models.UniqueConstraint(
                fields=["session", "question"], name="unique_session_answer"
            ),
        ]

    def __str__(self) -> str:
        mark = "✓" if self.is_correct else "✗"
        return f"{mark} S{self.session_id} · Q{self.question_id}"
