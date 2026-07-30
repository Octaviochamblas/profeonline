import os
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Choice, Question, Resource
from apps.content.services.editorial_guide_service import (
    insert_concept_image_after_explanations,
)


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
            concept_image_key="editorial-concept-images/1/example.png",
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
        self.assertEqual(response["Cache-Control"], "no-cache, must-revalidate")

    @mock.patch("apps.content.views.resource_detail.get_concept_image_object")
    def test_detail_route_serves_concept_image_asset(self, get_object):
        get_object.return_value = {
            "Body": _BucketBody(),
            "ContentType": "image/png",
            "ContentLength": 11,
            "CacheControl": "public, max-age=31536000, immutable",
        }

        url = reverse("content:resource_detail", kwargs={"slug": self.resource.slug})
        response = self.client.get(url, {"asset": "concept"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")
        self.assertEqual(b"".join(response.streaming_content), b"image-bytes")
        self.assertEqual(response["Cache-Control"], "no-cache, must-revalidate")

    @mock.patch("apps.content.views.resource_detail.get_infographic_object")
    def test_versioned_asset_can_be_cached_immutably(self, get_object):
        get_object.return_value = {
            "Body": _BucketBody(),
            "ContentType": "image/png",
            "ContentLength": 11,
        }
        url = reverse("content:resource_detail", kwargs={"slug": self.resource.slug})

        response = self.client.get(url, {"asset": "infographic", "v": "content-hash"})

        self.assertEqual(
            response["Cache-Control"],
            "public, max-age=31536000, immutable",
        )

    def test_resource_detail_enables_semantic_content_blocks(self):
        user = get_user_model().objects.create_user(
            username="reader",
            password="safe-test-password",
        )
        self.resource.content = "## Resumen inicial\nContenido de prueba."
        self.resource.save(update_fields=["content"])
        self.client.force_login(user)

        response = self.client.get(
            reverse("content:resource_detail", kwargs={"slug": self.resource.slug})
        )

        self.assertContains(response, "data-resource-content")
        self.assertContains(response, 'class="container resource-page-shell"')
        self.assertNotContains(response, 'class="container content-wrapper"')
        self.assertContains(response, "css/estilos.css?v=43")
        self.assertContains(response, "js/quiz-player.js?v=3")
        self.assertContains(response, "js/resource-detail.js?v=8")

    def test_concept_image_is_inserted_between_explanations_and_definitions(self):
        content = (
            "## Explicación formal\nDefinición por casos.\n\n"
            "## Explicación en palabras simples\nDistancia al cero.\n\n"
            "## Definiciones clave\nValor absoluto."
        )

        updated = insert_concept_image_after_explanations(content, self.resource)

        self.assertIn("?asset=concept", updated)
        self.assertLess(
            updated.index("?asset=concept"),
            updated.index("## Definiciones clave"),
        )

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
    @mock.patch("apps.content.views.api_video._store_concept_image_for_resource")
    def test_concept_image_upload_can_resolve_direct_resource_by_slug(self, store):
        url = reverse(
            "content:api_resource_concept_image_upload_by_slug",
            kwargs={"slug": self.resource.slug},
        )
        response = self.client.post(
            url,
            data={
                "image": SimpleUploadedFile(
                    "concepto.png",
                    b"\x89PNG\r\n\x1a\ncontenido",
                    content_type="image/png",
                ),
                "alt_text": "Definición formal y explicación sencilla",
            },
            HTTP_X_API_TOKEN="test-token",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["resource_id"], self.resource.id)
        self.assertTrue(response.json()["concept_image_ready"])
        store.assert_called_once()

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": "test-token"})
    def test_editorial_api_replaces_direct_resource_by_slug(self):
        guide = "\n\n".join(
            [
                "## Resumen inicial\nResumen concreto del orden de enteros.",
                (
                    "## Explicación formal\n"
                    "Los enteros se comparan por su posición.\n"
                    "## Explicación en palabras simples\n"
                    "Más a la derecha significa mayor."
                ),
                "## Definiciones clave\nUn entero puede ser negativo, cero o positivo.",
                "## Propiedades y relaciones importantes\nValor y valor absoluto no son lo mismo.",
                "## Ejemplo guiado\n$-5<-2$ porque $-5$ queda a la izquierda.",
                "## Procedimiento\nUbica, compara y escribe el signo correcto.",
                "## Errores frecuentes y cómo corregirlos\nNo compares negativos ignorando su signo.",
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
                (
                    "## Explicación formal\n"
                    "Explicación concreta.\n## Explicación en palabras simples\n"
                    "Lectura cotidiana concreta."
                ),
                "## Definiciones clave\nDefinición concreta.",
                "## Propiedades y relaciones importantes\nPropiedad concreta.",
                "## Ejemplo guiado\nEjemplo concreto.",
                "## Procedimiento\nProcedimiento concreto.",
                "## Errores frecuentes y cómo corregirlos\nError concreto.",
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

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": "test-token"})
    def test_editorial_api_accepts_prose_between_separate_math_spans(self):
        guide = "\n\n".join(
            [
                r"## Resumen inicial\nCompara $<$ o $>$ sin mezclar delimitadores.",
                (
                    "## Explicación formal\n"
                    r"También distingue $\leq$ o $\geq$."
                    "\n## Explicación en palabras simples\n"
                    "Compara límites en lenguaje cotidiano."
                ),
                "## Definiciones clave\nOrden y comparación.",
                "## Propiedades y relaciones importantes\nLos símbolos tienen usos distintos.",
                "## Ejemplo guiado\nCompara dos enteros.",
                "## Procedimiento\nEvalúa y luego compara.",
                "## Errores frecuentes y cómo corregirlos\nNo inviertas el signo.",
                (
                    "## Al terminar debes poder\nComparar enteros mediante su posición, "
                    "elegir el símbolo adecuado y comprobar el resultado verificando "
                    "qué valor queda a la izquierda y cuál queda a la derecha en la "
                    "recta numérica antes de concluir."
                ),
            ]
        ).replace("\\n", "\n")
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

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": "test-token"})
    def test_repair_api_preserves_question_ids_and_fixes_malformed_math(self):
        self.resource.content = r"Usa $leq$ o $geq$. Conserva $$a = b \text{ y } c = d$$."
        self.resource.save(update_fields=["content"])
        question = Question.objects.create(
            resource=self.resource,
            level=1,
            mode="ambas",
            text="Una cuenta tiene saldo $-7.000 y otra -12.000$. ¿Cuál es mayor?",
            explanation="Compara $-7.000 y otra -12.000$ en la recta.",
            status="publicada",
        )
        choice = Choice.objects.create(
            question=question,
            text="$-7.000 y otra -12.000$",
            is_correct=True,
        )
        url = reverse(
            "content:api_resource_editorial_repair_by_slug",
            kwargs={"slug": self.resource.slug},
        )
        response = self.client.post(url, HTTP_X_API_TOKEN="test-token")

        self.assertEqual(response.status_code, 200)
        self.resource.refresh_from_db()
        question.refresh_from_db()
        choice.refresh_from_db()
        self.assertEqual(
            self.resource.content,
            r"Usa $\leq$ o $\geq$. Conserva $$a = b \text{ y } c = d$$.",
        )
        self.assertEqual(
            question.text,
            "Una cuenta tiene saldo -7.000 y otra -12.000. ¿Cuál es mayor?",
        )
        self.assertEqual(choice.text, "-7.000 y otra -12.000")
