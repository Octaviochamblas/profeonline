from django.db import models
from django.conf import settings


class AnalyticsEvent(models.Model):
    """
    Registra eventos de analítica interna para mediciones de conversión
    y vistas de páginas. Cumple con políticas de privacidad: no guarda IPs ni PII.
    """
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analytics_events"
    )
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Evento de analítica"
        verbose_name_plural = "Eventos de analítica"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} - {self.path} ({self.created_at})"
