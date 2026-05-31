from django.conf import settings
from django.db import models


class QuestionErrorReport(models.Model):
    """Reporte de error en una pregunta, enviado por un alumno."""

    REASON_CHOICES = [
        ("respuesta_incorrecta", "Respuesta correcta equivocada"),
        ("enunciado_confuso", "Enunciado confuso"),
        ("alternativas_ambiguas", "Alternativas ambiguas"),
        ("error_redaccion", "Error de redacción/formato"),
        ("explicacion_insuficiente", "Explicación insuficiente"),
    ]
    STATUS_CHOICES = [
        ("nuevo", "Nuevo"),
        ("revisando", "Revisando"),
        ("resuelto", "Resuelto"),
        ("descartado", "Descartado"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="question_error_reports",
    )
    question = models.ForeignKey(
        "content.Question",
        on_delete=models.CASCADE,
        related_name="error_reports",
    )
    attempt = models.ForeignKey(
        "content.QuizAttempt",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="error_reports",
    )
    reason = models.CharField(
        max_length=30,
        choices=REASON_CHOICES,
        verbose_name="motivo",
    )
    comment = models.TextField(
        blank=True,
        verbose_name="comentario",
    )
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default="nuevo",
        verbose_name="estado",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "reporte de error"
        verbose_name_plural = "reportes de error"

    def __str__(self) -> str:
        return f"Reporte #{self.pk} — {self.get_reason_display()}"
