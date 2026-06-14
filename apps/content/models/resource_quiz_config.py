from django.db import models


def default_quiz_counts():
    return {
        "1": {"practice": {"pool": 15, "shown": 5}, "eval": {"pool": 10, "shown": 5}},
        "2": {"practice": {"pool": 15, "shown": 5}, "eval": {"pool": 10, "shown": 5}},
        "3": {"practice": {"pool": 15, "shown": 5}, "eval": {"pool": 10, "shown": 3}}
    }


class ResourceQuizConfig(models.Model):
    """Configuración personalizada de evaluación y práctica por recurso."""

    RECOVERY_CHOICES = [
        ("practice_5_5", "Práctica perfecta 5/5"),
        ("none", "Ninguna"),
    ]

    resource = models.OneToOneField(
        "content.Resource",
        on_delete=models.CASCADE,
        related_name="quiz_config",
        verbose_name="recurso",
    )
    counts = models.JSONField(
        default=default_quiz_counts,
        verbose_name="matriz de preguntas",
        help_text="Configuración de pool y mostradas por nivel y modo.",
    )
    pass_threshold = models.FloatField(
        default=1.0,
        verbose_name="umbral de aprobación",
        help_text="Porcentaje mínimo de respuestas correctas para aprobar (1.0 = 100%).",
    )
    max_attempts = models.PositiveSmallIntegerField(
        default=3,
        verbose_name="intentos máximos",
        help_text="Número máximo de intentos permitidos para la evaluación del nivel.",
    )
    recovery_rule = models.CharField(
        max_length=20,
        choices=RECOVERY_CHOICES,
        default="practice_5_5",
        verbose_name="regla de recuperación",
        help_text="Regla que permite recuperar un intento de evaluación.",
    )
    allow_retake_passed = models.BooleanField(
        default=True,
        verbose_name="permitir repetir aprobado",
        help_text="Permite al alumno volver a rendir la evaluación si ya está aprobada (sin volver a dar estrellas/XP).",
    )
    autopublish = models.BooleanField(
        default=False,
        verbose_name="autopublicar al generar",
        help_text="Si está activo, las preguntas generadas por IA se publican directamente en vez de guardarse en borrador.",
    )

    class Meta:
        verbose_name = "configuración de quiz de recurso"
        verbose_name_plural = "configuraciones de quiz de recurso"

    def __str__(self) -> str:
        return f"Configuración de Quiz para {self.resource.title}"

    def clean(self):
        super().clean()
        # Validación de que counts tiene la estructura correcta y shown <= pool
        from django.core.exceptions import ValidationError

        if not isinstance(self.counts, dict):
            raise ValidationError("La estructura de 'matriz de preguntas' debe ser un diccionario.")

        for level in ["1", "2", "3"]:
            if level not in self.counts:
                raise ValidationError(f"Falta el nivel {level} en la configuración de conteos.")
            level_data = self.counts[level]
            if not isinstance(level_data, dict):
                raise ValidationError(f"Los datos del nivel {level} deben ser un diccionario.")

            for mode in ["practice", "eval"]:
                if mode not in level_data:
                    raise ValidationError(f"Falta el modo {mode} en el nivel {level}.")
                mode_data = level_data[mode]
                if not isinstance(mode_data, dict) or "pool" not in mode_data or "shown" not in mode_data:
                    raise ValidationError(f"El modo {mode} en el nivel {level} debe contener 'pool' y 'shown'.")

                try:
                    pool = int(mode_data["pool"])
                    shown = int(mode_data["shown"])
                except (ValueError, TypeError):
                    raise ValidationError(f"Los conteos de pool y shown para nivel {level} modo {mode} deben ser enteros.")

                if pool < 0 or shown < 0:
                    raise ValidationError(f"Los conteos para nivel {level} modo {mode} no pueden ser negativos.")
                if shown > pool:
                    raise ValidationError(f"En nivel {level} modo {mode}, la cantidad de preguntas a mostrar ({shown}) no puede superar el tamaño del pool ({pool}).")
