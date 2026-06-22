from django.db import models

from .question import Question


class ExerciseItem(models.Model):
    """Ítem de aprendizaje dentro de un tema (objetivo evaluable).

    Lo propone la IA a partir de una guía privada y lo aprueba el profesor
    (flujo editorial en fases posteriores). En Fase 0 solo existe el esquema.
    """

    STATUS_CHOICES = [
        ("propuesto", "Propuesto"),
        ("aprobado", "Aprobado"),
        ("archivado", "Archivado"),
    ]

    topic = models.ForeignKey(
        "content.Topic",
        on_delete=models.CASCADE,
        related_name="exercise_items",
        verbose_name="tema",
    )
    title = models.CharField(max_length=200, verbose_name="título")
    level = models.PositiveSmallIntegerField(
        choices=Question.LEVEL_CHOICES, verbose_name="nivel"
    )
    difficulty = models.CharField(
        max_length=12,
        choices=Question.DIFFICULTY_CHOICES,
        blank=True,
        default="",
        verbose_name="dificultad",
    )
    objective = models.TextField(verbose_name="objetivo")
    recommendation = models.TextField(blank=True, verbose_name="recomendación")
    common_errors = models.TextField(blank=True, verbose_name="errores frecuentes")
    detected_exercise_count = models.PositiveIntegerField(
        default=0,
        verbose_name="ejercicios detectados",
        help_text="Cantidad de ejercicios de este ítem detectados por la IA en la guía de origen.",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="orden")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="propuesto",
        verbose_name="estado",
    )
    learning_guide = models.ForeignKey(
        "content.LearningGuide",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
        verbose_name="guía de origen",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["topic", "level", "order"]
        verbose_name = "ítem de aprendizaje"
        verbose_name_plural = "ítems de aprendizaje"

    def __str__(self) -> str:
        return f"[N{self.level}] {self.title[:80]}"

    def get_unlinked_resources(self, topic_resources=None):
        """Recursos del tema aún no vinculados a este ítem.

        Si se pasa ``topic_resources`` (lista ya cargada) y ``resource_links`` viene
        prefetcheado, no ejecuta consultas extra — evita el N+1 al renderizar la lista.
        """
        linked_ids = {link.resource_id for link in self.resource_links.all()}
        if topic_resources is None:
            topic_resources = self.topic.resources.order_by("title")
        return [r for r in topic_resources if r.id not in linked_ids]

    def get_linked_resources(self):
        """Recursos asociados a este ítem (usa ``resource_links`` prefetcheado si existe)."""
        return [link.resource for link in self.resource_links.all()]


class ResourceExerciseItem(models.Model):
    """Vínculo ítem ↔ recurso, con cuotas de práctica y evaluación."""

    exercise_item = models.ForeignKey(
        "content.ExerciseItem",
        on_delete=models.CASCADE,
        related_name="resource_links",
    )
    resource = models.ForeignKey(
        "content.Resource",
        on_delete=models.CASCADE,
        related_name="exercise_item_links",
    )
    practice_quota = models.PositiveSmallIntegerField(
        default=0, verbose_name="cuota de práctica"
    )
    evaluation_quota = models.PositiveSmallIntegerField(
        default=0, verbose_name="cuota de evaluación"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="orden")

    class Meta:
        ordering = ["exercise_item", "order"]
        verbose_name = "ítem por recurso"
        verbose_name_plural = "ítems por recurso"
        constraints = [
            models.UniqueConstraint(
                fields=["exercise_item", "resource"], name="unique_item_resource"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.exercise_item_id} ↔ {self.resource_id}"
