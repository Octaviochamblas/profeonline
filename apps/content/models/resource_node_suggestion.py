from django.db import models


class ResourceNodeSuggestion(models.Model):
    """Sugerencia (o confirmación) de a qué KnowledgeNode corresponde un Resource.

    Puente de navegación entre Sistema A (Resource, video) y Sistema B
    (KnowledgeNode, /aprender/). No fusiona datos: solo habilita un enlace
    cruzado "Ver también" una vez confirmada.
    """

    STATUS_SUGERIDO = "sugerido"
    STATUS_CONFIRMADO = "confirmado"
    STATUS_DESCARTADO = "descartado"
    STATUS_SIN_BLOQUE = "sin_bloque"
    STATUS_CHOICES = [
        (STATUS_SUGERIDO, "Sugerido"),
        (STATUS_CONFIRMADO, "Confirmado"),
        (STATUS_DESCARTADO, "Descartado"),
        (STATUS_SIN_BLOQUE, "Sin bloque encontrado"),
    ]

    ORIGEN_IA = "ia"
    ORIGEN_MANUAL = "manual"
    ORIGEN_CHOICES = [
        (ORIGEN_IA, "IA"),
        (ORIGEN_MANUAL, "Manual"),
    ]

    resource = models.OneToOneField(
        "content.Resource",
        on_delete=models.CASCADE,
        related_name="node_suggestion",
        verbose_name="recurso",
    )
    node = models.ForeignKey(
        "content.KnowledgeNode",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resource_suggestions",
        verbose_name="nodo",
    )
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default=STATUS_SUGERIDO,
        verbose_name="estado",
    )
    origen = models.CharField(
        max_length=8, choices=ORIGEN_CHOICES, blank=True, verbose_name="origen",
    )
    ai_rationale = models.TextField(blank=True, verbose_name="razón de la IA")
    ai_corrigio = models.BooleanField(
        default=False, verbose_name="la IA corrigió el candidato",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "sugerencia de nodo para recurso"
        verbose_name_plural = "sugerencias de nodo para recursos"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        target = self.node.name if self.node else "(sin bloque)"
        return f"{self.resource.title} -> {target} [{self.status}]"
