"""Tests del comando autónomo generate_pending_questions.

Se mockea ``fetch_transcript`` para no tocar la red. La generación usa el camino
*mock* del servicio (activo bajo el test runner), así que cada celda devuelve
exactamente ``count`` preguntas de forma determinista.
"""

from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from apps.content.management.commands.generate_pending_questions import Command
from apps.content.models import Question, Resource, ResourceQuizConfig, Subject, Topic

# Matriz chica para tests rápidos: solo N1 tiene pool (2 práctica + 1 evaluación).
SMALL_COUNTS = {
    "1": {"practice": {"pool": 2, "shown": 2}, "eval": {"pool": 1, "shown": 1}},
    "2": {"practice": {"pool": 0, "shown": 0}, "eval": {"pool": 0, "shown": 0}},
    "3": {"practice": {"pool": 0, "shown": 0}, "eval": {"pool": 0, "shown": 0}},
}

CMD = "generate_pending_questions"
FETCH_PATH = "apps.content.management.commands.generate_pending_questions.fetch_transcript"


class GeneratePendingQuestionsTests(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(name="Matemáticas")
        self.topic = Topic.objects.create(name="Números", subject=self.subject)
        self.resource = Resource.objects.create(
            title="Conjuntos numéricos",
            subject=self.subject,
            topic=self.topic,
            description="Qué son los conjuntos numéricos.",
            content="Los números naturales, enteros, racionales...",
            video_url="https://www.youtube.com/watch?v=abc12345678",
            is_published=True,
        )
        ResourceQuizConfig.objects.create(resource=self.resource, counts=SMALL_COUNTS)

    def _run(self, **kwargs):
        out = StringIO()
        call_command(CMD, stdout=out, stderr=StringIO(), **kwargs)
        return out.getvalue()

    def _count(self, mode, level=1):
        return Question.objects.filter(resource=self.resource, level=level, mode=mode).count()

    @patch(FETCH_PATH)
    def test_fills_pool_per_cell(self, mock_fetch):
        """Genera exactamente el pool de cada celda (con el mapeo de modos correcto)."""
        mock_fetch.return_value = "Transcripción real del video sobre conjuntos numéricos."

        self._run(resource=self.resource.slug, publish=True)

        self.assertEqual(self._count("preparacion"), 2)
        self.assertEqual(self._count("evaluacion"), 1)
        # No genera nada en celdas con pool 0.
        self.assertEqual(self._count("preparacion", level=2), 0)
        self.assertEqual(Question.objects.filter(resource=self.resource).count(), 3)
        # Se usó el transcript (una sola vez por recurso).
        mock_fetch.assert_called_once()

    @patch(FETCH_PATH)
    def test_is_idempotent(self, mock_fetch):
        """Una segunda corrida no crea duplicados: el déficit ya es 0."""
        mock_fetch.return_value = "Transcripción de prueba."

        self._run(resource=self.resource.slug, publish=True)
        total_after_first = Question.objects.filter(resource=self.resource).count()

        self._run(resource=self.resource.slug, publish=True)
        total_after_second = Question.objects.filter(resource=self.resource).count()

        self.assertEqual(total_after_first, 3)
        self.assertEqual(total_after_second, 3)

    @patch(FETCH_PATH)
    def test_respects_existing_deficit(self, mock_fetch):
        """Si ya existen algunas preguntas, solo genera las que faltan."""
        mock_fetch.return_value = "Transcripción de prueba."
        # Ya hay 1 de práctica N1 (pool=2) -> debería generar solo 1 más.
        Question.objects.create(
            resource=self.resource, level=1, mode="preparacion",
            text="Pregunta preexistente", status="publicada",
        )

        self._run(resource=self.resource.slug, publish=True)

        self.assertEqual(self._count("preparacion"), 2)  # 1 previa + 1 generada
        self.assertEqual(self._count("evaluacion"), 1)

    @patch(FETCH_PATH)
    def test_skips_when_no_transcript(self, mock_fetch):
        """Sin transcript y sin --allow-without-transcript, el recurso se omite."""
        mock_fetch.return_value = None

        self._run(resource=self.resource.slug, publish=True)

        self.assertEqual(Question.objects.filter(resource=self.resource).count(), 0)

    @patch(FETCH_PATH)
    def test_generates_without_transcript_when_allowed(self, mock_fetch):
        """Con --allow-without-transcript genera aunque no haya subtítulos."""
        mock_fetch.return_value = None

        self._run(resource=self.resource.slug, publish=True, allow_without_transcript=True)

        self.assertEqual(Question.objects.filter(resource=self.resource).count(), 3)

    @patch(FETCH_PATH)
    def test_default_publish_summary_does_not_claim_questions_are_drafts(self, mock_fetch):
        mock_fetch.return_value = "Transcripción de prueba."

        output = self._run(resource=self.resource.slug)

        self.assertEqual(
            Question.objects.filter(resource=self.resource, status="publicada").count(),
            3,
        )
        self.assertNotIn("esperan tu revisión", output)

    @patch(FETCH_PATH)
    def test_draft_summary_reports_pending_review(self, mock_fetch):
        mock_fetch.return_value = "Transcripción de prueba."

        output = self._run(resource=self.resource.slug, draft=True)

        self.assertEqual(
            Question.objects.filter(resource=self.resource, status="borrador").count(),
            3,
        )
        self.assertIn("esperan tu revisión", output)


class RequestPacingTests(TestCase):
    @patch("apps.content.management.commands.generate_pending_questions.time.sleep")
    @patch("apps.content.management.commands.generate_pending_questions.time.monotonic")
    def test_waits_only_for_remaining_interval(self, mock_monotonic, mock_sleep):
        mock_monotonic.return_value = 12.5

        Command()._wait_for_request_slot(last_request_at=10.0, interval=6.0)

        mock_sleep.assert_called_once_with(3.5)

    @patch("apps.content.management.commands.generate_pending_questions.time.sleep")
    @patch("apps.content.management.commands.generate_pending_questions.time.monotonic")
    def test_does_not_wait_when_interval_elapsed(self, mock_monotonic, mock_sleep):
        mock_monotonic.return_value = 17.0

        Command()._wait_for_request_slot(last_request_at=10.0, interval=6.0)

        mock_sleep.assert_not_called()
