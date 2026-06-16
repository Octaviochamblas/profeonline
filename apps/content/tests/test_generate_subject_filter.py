"""El comando generate_pending_questions puede acotarse a una asignatura (--subject)."""

from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from apps.content.models import Question, Resource, ResourceQuizConfig, Subject

SMALL = {
    "1": {"practice": {"pool": 1, "shown": 1}, "eval": {"pool": 0, "shown": 0}},
    "2": {"practice": {"pool": 0, "shown": 0}, "eval": {"pool": 0, "shown": 0}},
    "3": {"practice": {"pool": 0, "shown": 0}, "eval": {"pool": 0, "shown": 0}},
}
FETCH = "apps.content.management.commands.generate_pending_questions.fetch_transcript"


class SubjectFilterTests(TestCase):

    def setUp(self):
        self.s1 = Subject.objects.create(name="Mate Escolar")  # slug: mate-escolar
        self.s2 = Subject.objects.create(name="Física")
        self.r1 = Resource.objects.create(
            title="R1", subject=self.s1, video_url="https://youtu.be/aaaaaaaaaaa", is_published=True,
        )
        self.r2 = Resource.objects.create(
            title="R2", subject=self.s2, video_url="https://youtu.be/bbbbbbbbbbb", is_published=True,
        )
        ResourceQuizConfig.objects.create(resource=self.r1, counts=SMALL)
        ResourceQuizConfig.objects.create(resource=self.r2, counts=SMALL)

    @mock.patch(FETCH)
    def test_subject_acota_a_esa_asignatura(self, mock_fetch):
        mock_fetch.return_value = "transcript de prueba"
        call_command(
            "generate_pending_questions", subject=self.s1.slug, publish=True,
            stdout=StringIO(), stderr=StringIO(),
        )
        self.assertEqual(Question.objects.filter(resource=self.r1).count(), 1)
        self.assertEqual(Question.objects.filter(resource=self.r2).count(), 0)
