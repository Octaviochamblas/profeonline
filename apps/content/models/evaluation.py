from django.conf import settings
from django.db import models


class QuizAttempt(models.Model):
    """Registro de un intento de evaluación o preparación."""

    MODE_CHOICES = [
        ("preparacion", "Preparación"),
        ("evaluacion", "Evaluación"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
    )
    resource = models.ForeignKey(
        "content.Resource",
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
    )
    level = models.PositiveSmallIntegerField(
        verbose_name="nivel",
        help_text="1=Definición, 2=Ejercicios simples, 3=Problemas de aplicación",
    )
    mode = models.CharField(
        max_length=15,
        choices=MODE_CHOICES,
        verbose_name="modo",
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="aciertos",
        help_text="Número de respuestas correctas.",
    )
    total = models.PositiveSmallIntegerField(
        verbose_name="total de preguntas",
        help_text="Total de preguntas en el intento.",
    )
    passed = models.BooleanField(verbose_name="aprobado")
    attempt_number = models.PositiveSmallIntegerField(
        verbose_name="nº de intento",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "resource", "level", "mode", "attempt_number"],
                name="unique_quiz_attempt",
            )
        ]
        ordering = ["-created_at"]
        verbose_name = "intento de evaluación"
        verbose_name_plural = "intentos de evaluación"

    def __str__(self) -> str:
        result = "✓" if self.passed else "✗"
        return (
            f"{result} {self.user} — {self.resource} "
            f"N{self.level} ({self.mode}) {self.score}/{self.total}"
        )


class TopicEvaluationAttempt(models.Model):
    """Intento de la evaluación final de un tema.

    Compila preguntas de los recursos del tema. A diferencia de QuizAttempt
    (5/5 por nivel de recurso), aquí se aprueba con un umbral porcentual.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="topic_eval_attempts",
    )
    topic = models.ForeignKey(
        "content.Topic",
        on_delete=models.CASCADE,
        related_name="eval_attempts",
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="aciertos",
        help_text="Número de respuestas correctas.",
    )
    total = models.PositiveSmallIntegerField(
        verbose_name="total de preguntas",
    )
    percentage = models.PositiveSmallIntegerField(
        verbose_name="porcentaje",
        help_text="Porcentaje de acierto (0-100).",
    )
    passed = models.BooleanField(verbose_name="aprobado")
    attempt_number = models.PositiveSmallIntegerField(
        verbose_name="nº de intento",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "topic", "attempt_number"],
                name="unique_topic_eval_attempt",
            )
        ]
        ordering = ["-created_at"]
        verbose_name = "intento de evaluación de tema"
        verbose_name_plural = "intentos de evaluación de tema"

    def __str__(self) -> str:
        result = "✓" if self.passed else "✗"
        return f"{result} {self.user} — {self.topic} {self.percentage}%"


class QuizAttemptAnswer(models.Model):
    """Respuesta individual dentro de un intento de evaluación."""

    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question = models.ForeignKey(
        "content.Question",
        on_delete=models.CASCADE,
        related_name="attempt_answers",
    )
    selected_choice = models.ForeignKey(
        "content.Choice",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attempt_answers",
    )
    is_correct = models.BooleanField(verbose_name="es correcta")
    text_answer = models.TextField(
        blank=True,
        verbose_name="texto ingresado",
        help_text="Respuesta escrita en preguntas numéricas/algebraicas.",
    )

    class Meta:
        verbose_name = "respuesta de intento"
        verbose_name_plural = "respuestas de intento"

    def __str__(self) -> str:
        mark = "✓" if self.is_correct else "✗"
        return f"{mark} Q{self.question_id}"
