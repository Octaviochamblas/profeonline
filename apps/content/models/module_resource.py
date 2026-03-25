from django.db import models


class ModuleResource(models.Model):
    module = models.ForeignKey(
        "content.Module",
        on_delete=models.CASCADE,
        related_name="module_resources",
        verbose_name="módulo",
    )
    resource = models.ForeignKey(
        "content.Resource",
        on_delete=models.CASCADE,
        related_name="module_resources",
        verbose_name="recurso",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="orden")
    is_required = models.BooleanField(default=True, verbose_name="obligatorio")
    note = models.TextField(blank=True, verbose_name="nota")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "recurso del módulo"
        verbose_name_plural = "recursos del módulo"
        constraints = [
            models.UniqueConstraint(
                fields=["module", "resource"],
                name="unique_resource_per_module",
            )
        ]

    def __str__(self) -> str:
        return f"{self.module.title} -> {self.resource.title}"