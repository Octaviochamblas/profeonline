from django.db import models


def default_final_distribution():
    """Distribución por puntaje de la prueba final (conceptual/mecánico/aplicación)."""
    return {"conceptual": 20, "mecanico": 50, "aplicacion": 30}


class TopicBankConfig(models.Model):
    """Configuración del banco estandarizado para un tema.

    Se edita antes de activar el tema (`Topic.structured_bank_enabled`). En
    Fase 0 solo existe el esquema con los valores por defecto del epic.
    """

    topic = models.OneToOneField(
        "content.Topic",
        on_delete=models.CASCADE,
        related_name="bank_config",
        verbose_name="tema",
    )
    level_eval_minutes = models.PositiveSmallIntegerField(
        default=10, verbose_name="minutos por evaluación de nivel"
    )
    level_eval_attempts = models.PositiveSmallIntegerField(
        default=3, verbose_name="intentos por evaluación de nivel"
    )
    final_minutes = models.PositiveSmallIntegerField(
        default=45, verbose_name="minutos de la prueba final"
    )
    final_attempts = models.PositiveSmallIntegerField(
        default=2, verbose_name="intentos de la prueba final"
    )
    final_distribution = models.JSONField(
        default=default_final_distribution,
        verbose_name="distribución de la prueba final",
    )
    network_tolerance_seconds = models.PositiveSmallIntegerField(
        default=15, verbose_name="tolerancia de red (s)"
    )
    duration_tolerance_pct = models.PositiveSmallIntegerField(
        default=10, verbose_name="tolerancia de duración (%)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "configuración de banco por tema"
        verbose_name_plural = "configuraciones de banco por tema"

    def __str__(self) -> str:
        return f"Config banco — {self.topic}"
