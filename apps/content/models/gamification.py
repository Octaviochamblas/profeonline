from django.conf import settings
from django.db import models


class XPEvent(models.Model):
    """Evento auditable de XP otorgado a un usuario."""

    EVENT_CHOICES = [
        ("practice", "Practica"),
        ("resource_level_pass", "Nivel de recurso aprobado"),
        ("topic_exam_pass", "Evaluacion final de tema aprobada"),
        ("skill_unlock", "Skill desbloqueada"),
        ("streak_bonus", "Bonus de racha"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="xp_events",
    )
    event_type = models.CharField(max_length=30, choices=EVENT_CHOICES)
    amount = models.PositiveSmallIntegerField()
    event_key = models.CharField(
        max_length=160,
        unique=True,
        help_text="Clave idempotente para no duplicar XP por refrescos o reenvios.",
    )
    resource = models.ForeignKey(
        "content.Resource",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="xp_events",
    )
    topic = models.ForeignKey(
        "content.Topic",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="xp_events",
    )
    quiz_attempt = models.ForeignKey(
        "content.QuizAttempt",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="xp_events",
    )
    topic_attempt = models.ForeignKey(
        "content.TopicEvaluationAttempt",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="xp_events",
    )
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "evento de XP"
        verbose_name_plural = "eventos de XP"

    def __str__(self) -> str:
        return f"+{self.amount} XP {self.user} ({self.event_type})"


class UserSkill(models.Model):
    """Skill desbloqueada por aprobar la evaluacion final de un tema."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="skills",
    )
    topic = models.ForeignKey(
        "content.Topic",
        on_delete=models.CASCADE,
        related_name="unlocked_skills",
    )
    name = models.CharField(max_length=160)
    unlocked_by_attempt = models.ForeignKey(
        "content.TopicEvaluationAttempt",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="unlocked_skills",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "topic"],
                name="unique_skill_per_user_topic",
            )
        ]
        ordering = ["-created_at"]
        verbose_name = "skill desbloqueada"
        verbose_name_plural = "skills desbloqueadas"

    def __str__(self) -> str:
        return f"{self.name} - {self.user}"


class UserStreak(models.Model):
    """Racha de actividad con XP del usuario."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_streak",
    )
    current_count = models.PositiveSmallIntegerField(default=0)
    longest_count = models.PositiveSmallIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "racha de aprendizaje"
        verbose_name_plural = "rachas de aprendizaje"

    def __str__(self) -> str:
        return f"{self.user}: {self.current_count} dias"
