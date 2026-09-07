from django.db import models


class ContentSyncState(models.Model):
    """Último hash de `docs/conocimiento/` sincronizado a la BD.

    Lo usa el comando `sync_knowledge_content` para saltarse los loaders
    (`import_knowledge_tree`, `load_node_content`, `load_exercise_bank`,
    `publish_knowledge_nodes`) cuando el contenido del repo no cambió desde el
    deploy anterior — que es el caso de la mayoría de los deploys.
    """

    key = models.CharField(max_length=64, primary_key=True)
    content_hash = models.CharField(max_length=64, blank=True, default="")
    synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "estado de sincronización de contenido"
        verbose_name_plural = "estados de sincronización de contenido"

    def __str__(self) -> str:
        return f"{self.key}={self.content_hash[:12]}"
