"""Tests del comando backfill_transcripts (FASE 2): baja y guarda transcripts.

Se mockea fetch_transcript para no tocar la red.
"""

from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from apps.content.models import Resource, Subject

CMD = "backfill_transcripts"
FETCH = "apps.content.management.commands.backfill_transcripts.fetch_transcript"


class BackfillTranscriptsTests(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(name="Matemáticas")

    def _resource(self, n, transcript=""):
        return Resource.objects.create(
            title=f"Recurso {n}",
            subject=self.subject,
            video_url=f"https://youtu.be/vid{n:08d}",
            transcript=transcript,
            is_published=True,
        )

    def _run(self, **kwargs):
        kwargs.setdefault("delay", 0)
        out = StringIO()
        call_command(CMD, stdout=out, stderr=StringIO(), **kwargs)
        return out.getvalue()

    @mock.patch(FETCH)
    def test_guarda_los_que_faltan(self, mock_fetch):
        mock_fetch.return_value = "TRANSCRIPT REAL DEL VIDEO"
        r1, r2 = self._resource(1), self._resource(2)

        self._run(limit=10)

        r1.refresh_from_db(); r2.refresh_from_db()
        self.assertEqual(r1.transcript, "TRANSCRIPT REAL DEL VIDEO")
        self.assertEqual(r2.transcript, "TRANSCRIPT REAL DEL VIDEO")

    @mock.patch(FETCH)
    def test_no_pisa_los_que_ya_tienen(self, mock_fetch):
        mock_fetch.return_value = "NUEVO"
        con = self._resource(1, transcript="YA EXISTENTE")
        sin = self._resource(2)

        self._run(limit=10)

        con.refresh_from_db(); sin.refresh_from_db()
        self.assertEqual(con.transcript, "YA EXISTENTE")  # intacto
        self.assertEqual(sin.transcript, "NUEVO")
        # Solo se bajó 1 (el que faltaba).
        self.assertEqual(mock_fetch.call_count, 1)

    @mock.patch(FETCH)
    def test_respeta_limit(self, mock_fetch):
        mock_fetch.return_value = "T"
        for i in range(1, 4):
            self._resource(i)

        self._run(limit=2)

        self.assertEqual(mock_fetch.call_count, 2)

    @mock.patch(FETCH)
    def test_aborta_tras_fallos_seguidos(self, mock_fetch):
        mock_fetch.return_value = None  # siempre falla (simula bloqueo)
        for i in range(1, 6):
            self._resource(i)

        self._run(limit=10, max_fails=3)

        # Se detiene tras 3 fallos seguidos (no procesa los 5).
        self.assertEqual(mock_fetch.call_count, 3)
        self.assertEqual(Resource.objects.exclude(transcript="").count(), 0)
