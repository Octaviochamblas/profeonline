import json
import os
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Resource
from apps.content.services.reading_checkpoint_service import (
    normalize_reading_checkpoints,
)


def _checkpoints():
    return [
        {
            "placement": "after_concept_image",
            "question": "Si $x=-7$, ¿qué resultado entrega $|x|$?",
            "choices": [
                {"text": "$7$", "is_correct": True},
                {"text": "$-7$", "is_correct": False},
                {"text": "$0$", "is_correct": False},
                {"text": "$14$", "is_correct": False},
            ],
            "explanation": "La alternativa correcta es $7$, porque el valor absoluto mide distancia al cero.",
            "reinforcement_section": "Explicación formal",
        },
        {
            "placement": "after_guided_example",
            "question": "¿Cuál es el resultado de $-|6|$?",
            "choices": [
                {"text": "$-6$", "is_correct": True},
                {"text": "$6$", "is_correct": False},
                {"text": "$0$", "is_correct": False},
                {"text": "$12$", "is_correct": False},
            ],
            "explanation": "La alternativa correcta es $-6$: primero se calcula $|6|=6$ y luego se aplica el signo.",
            "reinforcement_section": "Ejemplo guiado",
        },
        {
            "placement": "after_errors",
            "question": "¿Qué expresión calcula la distancia entre $-3$ y $5$?",
            "choices": [
                {"text": "$|-3-5|=8$", "is_correct": True},
                {"text": "$|-3+5|=2$", "is_correct": False},
                {"text": "$-3-5=-8$", "is_correct": False},
                {"text": "$|5|=5$", "is_correct": False},
            ],
            "explanation": "La alternativa correcta es $|-3-5|=8$, pues la distancia es el valor absoluto de la diferencia.",
            "reinforcement_section": "Procedimiento",
        },
    ]


def _guide():
    return "\n\n".join(
        [
            "## Resumen inicial\nResumen suficientemente concreto.",
            "## Explicación en palabras simples\nDistancia al cero.",
            "## Explicación formal\nDefinición matemática por casos.",
            "## Definiciones clave\nValor absoluto y número opuesto.",
            "## Propiedades y relaciones importantes\nEl valor absoluto no es negativo.",
            "## Ejemplo guiado\nSe calcula primero el contenido de las barras.",
            "## Procedimiento\nIdentifica, calcula, aplica signos y comprueba.",
            "## Errores frecuentes y cómo corregirlos\nNo confundas un signo exterior con las barras.",
            (
                "## Al terminar debes poder\nIdentificar el argumento del valor absoluto, "
                "calcular su distancia al cero, aplicar signos externos, comparar los "
                "resultados y comprobar que todo valor absoluto aislado sea no negativo "
                "antes de interpretar la relación de orden obtenida."
            ),
        ]
    )


class ReadingCheckpointTests(TestCase):
    def setUp(self):
        self.resource = Resource.objects.create(
            title="Valor absoluto",
            slug="valor-absoluto",
            description="Descripción.",
            content=_guide(),
            is_published=True,
        )

    def test_validator_accepts_three_canonical_checkpoints(self):
        normalized = normalize_reading_checkpoints(_checkpoints())

        self.assertEqual(len(normalized), 3)
        self.assertEqual(
            [item["placement"] for item in normalized],
            ["after_concept_image", "after_guided_example", "after_errors"],
        )

    def test_validator_rejects_multiple_correct_choices(self):
        checkpoints = _checkpoints()
        checkpoints[0]["choices"][1]["is_correct"] = True

        with self.assertRaisesRegex(ValueError, "exactamente una alternativa correcta"):
            normalize_reading_checkpoints(checkpoints)

    def test_detail_exposes_checkpoint_json_to_authenticated_reader(self):
        self.resource.reading_checkpoints = _checkpoints()
        self.resource.save(update_fields=["reading_checkpoints"])
        user = get_user_model().objects.create_user(username="reader-checkpoints")
        self.client.force_login(user)

        response = self.client.get(
            reverse("content:resource_detail", kwargs={"slug": self.resource.slug})
        )

        self.assertContains(response, 'id="resource-reading-checkpoints"')
        self.assertContains(response, "after_concept_image")

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": "test-token"})
    def test_direct_editorial_api_updates_checkpoints_without_touching_questions(self):
        response = self.client.post(
            reverse(
                "content:api_resource_editorial_refresh_by_slug",
                kwargs={"slug": self.resource.slug},
            ),
            data=json.dumps(
                {
                    "replace_questions": False,
                    "metadata": {"resource_description": "Descripción renovada."},
                    "guide": {"content": _guide(), "checkpoints": _checkpoints()},
                }
            ),
            content_type="application/json",
            HTTP_X_API_TOKEN="test-token",
        )

        self.assertEqual(response.status_code, 200)
        self.resource.refresh_from_db()
        self.assertEqual(len(self.resource.reading_checkpoints), 3)
        self.assertEqual(response.json()["questions"], "preserved")

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": "test-token"})
    def test_direct_editorial_api_dry_run_does_not_write(self):
        response = self.client.post(
            reverse(
                "content:api_resource_editorial_refresh_by_slug",
                kwargs={"slug": self.resource.slug},
            ),
            data=json.dumps(
                {
                    "dry_run": True,
                    "replace_questions": False,
                    "metadata": {"resource_description": "No debe persistirse."},
                    "guide": {"content": _guide(), "checkpoints": _checkpoints()},
                }
            ),
            content_type="application/json",
            HTTP_X_API_TOKEN="test-token",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["dry_run"])
        self.resource.refresh_from_db()
        self.assertEqual(self.resource.description, "Descripción.")
        self.assertEqual(self.resource.reading_checkpoints, [])
