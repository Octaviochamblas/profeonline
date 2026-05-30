from django.conf import settings
from django.db import models


class ResourceCompletion(models.Model):
    """Marca que un usuario completó un recurso."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resource_completions",
    )
    resource = models.ForeignKey(
        "content.Resource",
        on_delete=models.CASCADE,
        related_name="completions",
    )
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "resource"],
                name="unique_user_resource_completion",
            )
        ]
        ordering = ["-completed_at"]
        verbose_name = "recurso completado"
        verbose_name_plural = "recursos completados"

    def __str__(self) -> str:
        return f"{self.user} → {self.resource}"
