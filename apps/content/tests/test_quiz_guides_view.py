"""Tests de la página de gestión de guías (solo-admin): subir, vincular, borrar."""

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.content.models import QuizGuide, Subject

User = get_user_model()


class QuizGuidesViewTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "a@a.com", "pw")
        self.student = User.objects.create_user("stud", password="pw")
        self.subject = Subject.objects.create(name="Matemáticas")
        self.url = reverse("content:quiz_guides")

    def test_rechaza_no_admin(self):
        self.client.force_login(self.student)
        self.assertIn(self.client.get(self.url).status_code, (302, 403))

    def test_renderiza_para_admin(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_crear_desde_texto_y_vincular(self):
        self.client.force_login(self.admin)
        resp = self.client.post(self.url, {
            "title": "Estilo PAES",
            "text": "Item 1: resolver 2x+3=7.",
            "subjects": [self.subject.id],
        })
        self.assertEqual(resp.status_code, 302)
        guide = QuizGuide.objects.get(title="Estilo PAES")
        self.assertIn("2x+3", guide.content_text)
        self.assertIn(self.subject, list(guide.subjects.all()))

    def test_crear_desde_archivo(self):
        self.client.force_login(self.admin)
        archivo = SimpleUploadedFile(
            "guia.txt", "Pregunta de ejemplo: factoriza x^2-1".encode("utf-8"),
            content_type="text/plain",
        )
        self.client.post(self.url, {"title": "Desde archivo", "file": archivo})
        guide = QuizGuide.objects.get(title="Desde archivo")
        self.assertIn("factoriza", guide.content_text)
        self.assertEqual(guide.source_filename, "guia.txt")

    def test_requiere_titulo(self):
        self.client.force_login(self.admin)
        self.client.post(self.url, {"text": "algo sin titulo"})
        self.assertEqual(QuizGuide.objects.count(), 0)

    def test_borrar(self):
        self.client.force_login(self.admin)
        guide = QuizGuide.objects.create(title="Borrar", content_text="x")
        resp = self.client.post(reverse("content:delete_quiz_guide", args=[guide.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(QuizGuide.objects.filter(id=guide.id).exists())
