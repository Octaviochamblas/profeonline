from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import LearningGuide, Subject, Topic

User = get_user_model()


class LearningGuidePrintTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="print-student", password="x")
        subject = Subject.objects.create(name="Matemática PDF")
        self.topic = Topic.objects.create(
            name="Álgebra PDF",
            subject=subject,
            structured_bank_enabled=True,
        )
        self.guide = LearningGuide.objects.create(
            topic=self.topic,
            title="Guía PDF con fórmulas",
            status="publicada",
            visibility="publica",
            structured_content={
                "introduction": "Trabajaremos con $x^2$.",
                "summary": "Resumen con $\\frac{1}{2}$.",
                "formulas": [
                    {
                        "latex": "$$x = \\frac{-b}{2a}$$",
                        "explanation": "Fórmula de ejemplo.",
                    }
                ],
                "items": [],
                "challenges": [],
                "answer_key": [
                    {"exercise_id": "E1", "solution": "$x = 2$"}
                ],
            },
        )
        self.client.force_login(self.user)

    def test_public_guide_exposes_native_print_contract(self):
        response = self.client.get(
            reverse("content:learning_guide_detail", args=[self.guide.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="print-cover"')
        self.assertContains(response, "Guía oficial ProfeOnline")
        self.assertContains(response, "Descargar PDF")
        self.assertContains(response, "Guardar como PDF")
        self.assertContains(response, "screen-answer-key")
        self.assertContains(response, 'class="print-solution-block"')
        self.assertContains(response, "Ejercicios de la guía")
        self.assertContains(response, "learning-guide-print.css")
        self.assertContains(response, "?v=3")
        self.assertNotContains(response, "html2pdf")
