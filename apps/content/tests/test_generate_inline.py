"""Tests de la generación por sección (botones video / documento) en la revisión."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Question, QuizGuide, Resource, Subject

User = get_user_model()


class GenerateInlineTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "a@a.com", "pw")
        self.subject = Subject.objects.create(name="Matemáticas")
        self.resource = Resource.objects.create(
            title="R", subject=self.subject, description="d", content="c", is_published=True,
        )
        self.url = reverse("content:generate_questions_inline", args=[self.resource.id])

    def test_rechaza_no_admin(self):
        student = User.objects.create_user("s", password="pw")
        self.client.force_login(student)
        self.assertIn(self.client.post(self.url, {"source": "video"}).status_code, (302, 403))

    def test_modo_video_genera(self):
        self.client.force_login(self.admin)
        resp = self.client.post(self.url, {
            "level": "1", "mode": "preparacion", "source": "video", "count": "3",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            Question.objects.filter(resource=self.resource, level=1, mode="preparacion").count(), 3
        )

    def test_modo_documento_sin_guia_avisa(self):
        self.client.force_login(self.admin)
        resp = self.client.post(self.url, {
            "level": "1", "mode": "preparacion", "source": "document",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "No hay guía")
        self.assertEqual(Question.objects.filter(resource=self.resource).count(), 0)

    def test_modo_documento_con_guia_genera(self):
        self.client.force_login(self.admin)
        guide = QuizGuide.objects.create(title="G", content_text="Ejemplo de pregunta tipo.")
        guide.subjects.add(self.subject)
        resp = self.client.post(self.url, {
            "level": "1", "mode": "evaluacion", "source": "document", "count": "2",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Question.objects.filter(resource=self.resource).count(), 2)

    def test_count_se_limita_a_5(self):
        self.client.force_login(self.admin)
        self.client.post(self.url, {
            "level": "1", "mode": "preparacion", "source": "video", "count": "50",
        })
        self.assertEqual(Question.objects.filter(resource=self.resource).count(), 5)
