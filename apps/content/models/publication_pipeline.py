from django.db import models


class PublicationItem(models.Model):
    """Estado durable de un video dentro del pipeline de publicación."""

    STATE_UPLOADED = "uploaded"
    STATE_TRANSCRIPT_PENDING = "transcript_pending"
    STATE_CONTEXT_READY = "context_ready"
    STATE_METADATA_READY = "metadata_ready"
    STATE_QUESTIONS_READY = "questions_ready"
    STATE_PUBLISHED = "published"
    STATE_FAILED = "failed"

    STATE_CHOICES = [
        (STATE_UPLOADED, "Subido"),
        (STATE_TRANSCRIPT_PENDING, "Transcripción pendiente"),
        (STATE_CONTEXT_READY, "Contexto listo"),
        (STATE_METADATA_READY, "Metadatos listos"),
        (STATE_QUESTIONS_READY, "Preguntas listas"),
        (STATE_PUBLISHED, "Publicado"),
        (STATE_FAILED, "Fallido"),
    ]

    batch_id = models.CharField(max_length=64)
    source_filename = models.CharField(max_length=255)
    youtube_video_id = models.CharField(max_length=32, blank=True)
    youtube_url = models.URLField(blank=True)
    youtube_privacy = models.CharField(max_length=20, default="unlisted")
    state = models.CharField(
        max_length=24,
        choices=STATE_CHOICES,
        default=STATE_UPLOADED,
    )
    resume_state = models.CharField(max_length=24, blank=True)
    resource = models.ForeignKey(
        "content.Resource",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="publication_items",
    )
    canonical_guide = models.OneToOneField(
        "content.QuizGuide",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="publication_item",
    )
    taxonomy = models.JSONField(default=dict, blank=True)
    instructions = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    target_counts = models.JSONField(default=dict, blank=True)
    last_error = models.TextField(blank=True)
    attempts = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["batch_id", "source_filename"],
                name="unique_publication_batch_file",
            ),
        ]
        ordering = ["created_at", "id"]

    def __str__(self):
        return f"{self.batch_id}:{self.source_filename} [{self.state}]"
