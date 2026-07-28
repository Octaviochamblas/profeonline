import os
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Question, Resource


class _BucketBody:
    def iter_chunks(self):
        yield b"image-bytes"


class ResourceInfographicTests(TestCase):
    def setUp(self):
        self.resource = Resource.objects.create(
            title="Orden de enteros",
            slug="orden-de-enteros",
            is_published=True,
            infographic_key="editorial-infographics/1/example.png",
        )

    @mock.patch("apps.content.views.resource_detail.get_infographic_object")
    def test_detail_route_serves_infographic_asset(self, get_object):
        get_object.return_value = {
            "Body": _BucketBody(),
            "ContentType": "image/png",
            "ContentLength": 11,
            "CacheControl": "public, max-age=31536000, immutable",
        }

        url = reverse("content:resource_detail", kwargs={"slug": self.resource.slug})
        response = self.client.get(url, {"asset": "infographic"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")
        self.assertEqual(b"".join(response.streaming_content), b"image-bytes")

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": "test-token"})
    @mock.patch("apps.content.views.api_video._store_infographic_for_resource")
    def test_upload_api_can_resolve_direct_resource_by_slug(self, store):
        url = reverse(
            "content:api_resource_infographic_upload_by_slug",
            kwargs={"slug": self.resource.slug},
        )
        response = self.client.post(
            url,
            data={
                "image": SimpleUploadedFile(
                    "infografia.png",
                    b"\x89PNG\r\n\x1a\ncontenido",
                    content_type="image/png",
                ),
                "alt_text": "Resumen visual",
            },
            HTTP_X_API_TOKEN="test-token",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["resource_id"], self.resource.id)
        store.assert_called_once()

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": "test-token"})
    def test_editorial_api_replaces_direct_resource_by_slug(self):
        guide = "\n\n".join(
            [
                "## Resumen inicial\nResumen concreto del orden de enteros.",
                "## Explicación completa\nLos enteros se comparan por su posición.",
                "## Definiciones clave\nUn entero puede ser negativo, cero o positivo.",
                "## Diferencias que no debes confundir\nValor y valor absoluto no son lo mismo.",
                "## Ejemplo guiado\n$-5<-2$ porque $-5$ queda a la izquierda.",
                "## Procedimiento\nUbica, compara y escribe el signo correcto.",
                "## Errores frecuentes\nNo compares negativos ignorando su signo.",
                (
                    "## Al terminar debes poder\nUbicar enteros en una recta numérica, "
                    "comparar negativos, cero y positivos, seleccionar el signo de orden "
                    "correcto y comprobar cada respuesta verificando que el menor quede "
                    "a la izquierda y el mayor a la derecha."
                ),
            ]
        )
        questions = []
        for level in (1, 2, 3):
            for number in range(1, 11):
                correct = f"Respuesta correcta N{level}-{number}"
                questions.append(
                    {
                        "level": level,
                        "mode": "ambas",
                        "text": f"Pregunta única N{level}-{number}",
                        "explanation": f"La alternativa correcta es: {correct}",
                        "cognitive_type": "comprension",
                        "choices": [
                            {"text": correct, "is_correct": True},
                            {"text": f"Distractor A N{level}-{number}", "is_correct": False},
                            {"text": f"Distractor B N{level}-{number}", "is_correct": False},
                            {"text": f"Distractor C N{level}-{number}", "is_correct": False},
                        ],
                    }
                )
        url = reverse(
            "content:api_resource_editorial_refresh_by_slug",
            kwargs={"slug": self.resource.slug},
        )
        response = self.client.post(
            url,
            data={
                "metadata": {"resource_description": "Descripción renovada."},
                "guide": {"content": guide},
                "questions": questions,
            },
            content_type="application/json",
            HTTP_X_API_TOKEN="test-token",
        )

        self.assertEqual(response.status_code, 200)
        self.resource.refresh_from_db()
        self.assertTrue(self.resource.content.startswith("## Resumen inicial"))
        self.assertEqual(self.resource.questions.count(), 30)

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": "test-token"})
    def test_editorial_api_can_update_content_without_replacing_questions(self):
        Question.objects.create(
            resource=self.resource,
            level=1,
            mode="ambas",
            text="Pregunta histórica",
            explanation="Explicación histórica",
            status="publicada",
        )
        guide = "\n\n".join(
            [
                "## Resumen inicial\nResumen concreto.",
                "## Explicación completa\nExplicación concreta.",
                "## Definiciones clave\nDefinición concreta.",
                "## Diferencias que no debes confundir\nDiferencia concreta.",
                "## Ejemplo guiado\nEjemplo concreto.",
                "## Procedimiento\nProcedimiento concreto.",
                "## Errores frecuentes\nError concreto.",
                (
                    "## Al terminar debes poder\nComparar enteros negativos, cero y "
                    "positivos mediante su posición en la recta numérica, escoger el "
                    "signo de orden adecuado y comprobar el resultado verificando cuál "
                    "valor queda a la izquierda y cuál queda a la derecha."
                ),
            ]
        )
        url = reverse(
            "content:api_resource_editorial_refresh_by_slug",
            kwargs={"slug": self.resource.slug},
        )
        response = self.client.post(
            url,
            data={
                "replace_questions": False,
                "metadata": {"resource_description": "Descripción renovada."},
                "guide": {"content": guide},
            },
            content_type="application/json",
            HTTP_X_API_TOKEN="test-token",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["questions"], "preserved")
        self.assertEqual(self.resource.questions.count(), 1)
