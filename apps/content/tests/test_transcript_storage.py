"""Transcript guardado en el recurso: webhook lo persiste y la generación lo prefiere.

Esto evita scrapear YouTube en cada generación (que YouTube bloquea por volumen):
el transcript se baja aparte desde una IP residencial y se guarda vía webhook.
"""

import json
import os
from unittest import mock

from django.test import TestCase, override_settings
from django.urls import reverse

from apps.content.models import Resource, Subject
from apps.content.services.ai_generation_service import generate_questions_for_resource

TOKEN = "tok-test-123"
VIDEO_ID = "abcd1234XYZ"  # 11 caracteres válidos


class WebhookTranscriptTests(TestCase):

    def setUp(self):
        self.url = reverse("content:api_create_resource_from_video")

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": TOKEN})
    def test_webhook_guarda_y_actualiza_transcript(self):
        # Crear con transcript.
        resp = self.client.post(
            self.url,
            data=json.dumps({
                "title": "Mi video",
                "video_url": f"https://www.youtube.com/watch?v={VIDEO_ID}",
                "transcript": "PRIMER TRANSCRIPT",
            }),
            content_type="application/json",
            HTTP_X_API_TOKEN=TOKEN,
        )
        self.assertEqual(resp.status_code, 201)
        resource = Resource.objects.get(id=resp.json()["resource_id"])
        self.assertEqual(resource.transcript, "PRIMER TRANSCRIPT")

        # Reenviar el mismo video (otra forma de URL) con un transcript nuevo -> actualiza.
        resp2 = self.client.post(
            self.url,
            data=json.dumps({
                "title": "Mi video",
                "video_url": f"https://youtu.be/{VIDEO_ID}",
                "transcript": "SEGUNDO TRANSCRIPT",
            }),
            content_type="application/json",
            HTTP_X_API_TOKEN=TOKEN,
        )
        self.assertEqual(resp2.status_code, 200)
        resource.refresh_from_db()
        self.assertEqual(resource.transcript, "SEGUNDO TRANSCRIPT")

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": TOKEN})
    def test_webhook_no_borra_transcript_si_no_viene(self):
        """Re-procesar una subida SIN transcript no debe borrar el ya guardado."""
        self.client.post(
            self.url,
            data=json.dumps({
                "title": "V", "video_url": f"https://youtu.be/{VIDEO_ID}",
                "transcript": "ALGO",
            }),
            content_type="application/json", HTTP_X_API_TOKEN=TOKEN,
        )
        # Segunda llamada sin transcript.
        self.client.post(
            self.url,
            data=json.dumps({"title": "V", "video_url": f"https://youtu.be/{VIDEO_ID}"}),
            content_type="application/json", HTTP_X_API_TOKEN=TOKEN,
        )
        resource = Resource.objects.get(video_url__icontains=VIDEO_ID)
        self.assertEqual(resource.transcript, "ALGO")


class GenerationPrefersStoredTranscriptTests(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(name="Matemáticas")
        self.resource = Resource.objects.create(
            title="Recurso",
            subject=self.subject,
            description="d",
            content="c",
            video_url=f"https://youtu.be/{VIDEO_ID}",
            transcript="MARCADOR_GUARDADO_XYZ",
            is_published=True,
        )

    @mock.patch("apps.content.services.transcript_service.fetch_transcript")
    @mock.patch("apps.content.services.ai_generation_service._call_gemini_api")
    @override_settings(GEMINI_API_KEY="fake-key")
    def test_usa_transcript_guardado_sin_tocar_youtube(self, mock_call, mock_fetch):
        mock_call.return_value = [{
            "text": "q",
            "explanation": "e",
            "choices": [
                {"text": "a", "is_correct": True},
                {"text": "b", "is_correct": False},
                {"text": "c", "is_correct": False},
                {"text": "d", "is_correct": False},
            ],
        }]

        generate_questions_for_resource(
            resource=self.resource, level=1, mode="evaluacion", count=1,
        )

        prompt = mock_call.call_args[0][0]
        self.assertIn("MARCADOR_GUARDADO_XYZ", prompt)
        mock_fetch.assert_not_called()  # no se scrapeó YouTube
