from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from apps.content.models import (
    Choice,
    EvaluationSessionAnswer,
    ExerciseItem,
    LearningGuide,
    Question,
    QuizAttempt,
    QuizAttemptAnswer,
    Resource,
    ResourceExerciseItem,
    Subject,
    Topic,
)
from apps.content.services.progress_service import get_resource_progress

User = get_user_model()


class DirectAnswerIntegrationTests(TestCase):
    def setUp(self):
        subject = Subject.objects.create(
            name="Matemática",
            education_level="media",
        )
        self.topic = Topic.objects.create(
            name="Álgebra directa",
            subject=subject,
            structured_bank_enabled=True,
        )
        self.resource = Resource.objects.create(
            title="Expresiones",
            subject=subject,
            topic=self.topic,
            is_published=True,
        )
        self.item = ExerciseItem.objects.create(
            topic=self.topic,
            title="Expresiones equivalentes",
            level=2,
            objective="Reconocer expresiones equivalentes.",
            status="aprobado",
            detected_exercise_count=3,
        )
        ResourceExerciseItem.objects.create(
            exercise_item=self.item,
            resource=self.resource,
            practice_quota=3,
        )
        self.guide = LearningGuide.objects.create(
            topic=self.topic,
            title="Guía de respuestas directas",
            status="publicada",
            visibility="publica",
            structured_content={"schema_version": 1},
        )
        self.guide.resources.add(self.resource)
        self.admin = User.objects.create_superuser(
            username="admin-direct",
            email="admin-direct@example.com",
            password="password",
        )
        self.student = User.objects.create_user(
            username="student-direct",
            email="student-direct@example.com",
            password="password",
        )
        self.client = Client()

    def create_question(self, *, question_type, canonical_answer, status="publicada"):
        return Question.objects.create(
            resource=self.resource,
            level=2,
            mode="preparacion",
            text=f"Pregunta {question_type}",
            explanation="Explicación paso a paso.",
            status=status,
            exercise_item=self.item,
            question_type=question_type,
            difficulty="intermedia",
            hint="Usa las propiedades básicas.",
            canonical_answer=canonical_answer,
            scope="banco_visible",
            learning_guide=self.guide,
        )

    def test_mixed_practice_grades_all_types_without_academic_writes(self):
        alternative = self.create_question(
            question_type="alternativa",
            canonical_answer="Correcta",
        )
        correct_choice = Choice.objects.create(
            question=alternative,
            text="Correcta",
            is_correct=True,
            order=1,
        )
        Choice.objects.create(
            question=alternative,
            text="Incorrecta",
            is_correct=False,
            order=2,
        )
        numeric = self.create_question(
            question_type="numerica",
            canonical_answer="1/2",
        )
        algebraic = self.create_question(
            question_type="algebraica",
            canonical_answer="2*x+2",
        )

        self.client.force_login(self.student)
        progress_before = get_resource_progress(self.student, self.resource)
        response = self.client.post(
            reverse("content:start_visible_practice", args=[self.topic.id]),
            {"count": 3},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'name="question_{numeric.id}"',
        )
        self.assertContains(response, 'type="text"')
        self.assertContains(response, "data-quiz-answer")
        self.assertNotContains(response, "1/2")
        self.assertNotContains(response, "2*x+2")

        response = self.client.post(
            reverse("content:submit_visible_practice", args=[self.topic.id]),
            {
                f"question_{alternative.id}": str(correct_choice.id),
                f"question_{numeric.id}": "0,5",
                f"question_{algebraic.id}": "2(x+1)",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["score"], 3)
        self.assertEqual(response.context["total"], 3)
        self.assertContains(response, "0,5")
        self.assertContains(response, "2(x+1)")
        self.assertEqual(QuizAttempt.objects.count(), 0)
        self.assertEqual(QuizAttemptAnswer.objects.count(), 0)
        self.assertEqual(EvaluationSessionAnswer.objects.count(), 0)
        self.assertEqual(
            get_resource_progress(self.student, self.resource),
            progress_before,
        )

    def test_submit_rejects_duplicate_and_foreign_answer_parameters(self):
        numeric = self.create_question(
            question_type="numerica",
            canonical_answer="2",
        )
        foreign = self.create_question(
            question_type="numerica",
            canonical_answer="3",
        )
        self.client.force_login(self.student)
        self.client.post(
            reverse("content:start_visible_practice", args=[self.topic.id]),
            {"count": 1, "item_id": self.item.id},
        )
        session_key = f"visible_practice_{self.student.id}_{self.topic.id}"
        session = self.client.session
        session[session_key] = {
            "question_ids": [numeric.id],
            "filters": {},
            "order": [numeric.id],
        }
        session.save()

        submit_url = reverse(
            "content:submit_visible_practice",
            args=[self.topic.id],
        )
        duplicate_body = (
            f"question_{numeric.id}=2&question_{numeric.id}=2"
        )
        response = self.client.post(
            submit_url,
            duplicate_body,
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            submit_url,
            {f"question_{foreign.id}": "3"},
        )
        self.assertEqual(response.status_code, 400)

    def test_editor_can_convert_publish_and_revert_direct_question(self):
        draft = self.create_question(
            question_type="alternativa",
            canonical_answer="A",
            status="borrador",
        )
        choices = [
            Choice.objects.create(
                question=draft,
                text=text,
                is_correct=index == 0,
                order=index + 1,
            )
            for index, text in enumerate(("A", "B", "C", "D"))
        ]
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("content:edit_question_inline", args=[draft.id]),
            {
                "text": "Escribe un medio.",
                "explanation": "Un medio equivale a 0,5.",
                "order": "1",
                "difficulty": "basica",
                "hint": "Divide uno por dos.",
                "question_type": "numerica",
                "canonical_answer": "1/2",
                "answer_tolerance": "0,01",
            },
        )
        self.assertEqual(response.status_code, 302)
        draft.refresh_from_db()
        self.assertEqual(draft.question_type, "numerica")
        self.assertEqual(draft.canonical_answer, "1/2")
        self.assertEqual(draft.answer_tolerance, 0.01)
        self.assertEqual(draft.status, "borrador")
        self.assertEqual(draft.choices.count(), 4)

        response = self.client.post(
            reverse("content:bulk_action_questions", args=[self.resource.id]),
            {
                "action": "publicar",
                "scope": "banco_visible",
                "exercise_item_id": self.item.id,
                "learning_guide_id": self.guide.id,
                "selected_questions": [draft.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        draft.refresh_from_db()
        self.assertEqual(draft.status, "publicada")

        response = self.client.post(
            reverse("content:add_choice_inline", args=[draft.id])
        )
        self.assertEqual(response.status_code, 400)
        draft.refresh_from_db()
        self.assertEqual(draft.status, "publicada")
        self.assertEqual(draft.choices.count(), 4)

        response = self.client.post(
            reverse("content:edit_choice_inline", args=[choices[0].id]),
            {"text": "Alterada", "is_correct": "on"},
        )
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            reverse("content:delete_choice", args=[choices[0].id])
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue(Choice.objects.filter(id=choices[0].id).exists())

        response = self.client.post(
            reverse("content:edit_question_inline", args=[draft.id]),
            {
                "text": "Escribe un medio de otra forma.",
                "explanation": "Un medio equivale a 0,5.",
                "order": "1",
                "difficulty": "basica",
                "hint": "Usa un decimal.",
                "question_type": "numerica",
                "canonical_answer": "0.5",
                "answer_tolerance": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        draft.refresh_from_db()
        self.assertEqual(draft.status, "borrador")
        self.assertEqual(draft.canonical_answer, "0.5")

    def test_invalid_direct_canonical_blocks_publication(self):
        draft = self.create_question(
            question_type="algebraica",
            canonical_answer="sqrt(x)",
            status="borrador",
        )
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("content:bulk_action_questions", args=[self.resource.id]),
            {
                "action": "publicar",
                "scope": "banco_visible",
                "exercise_item_id": self.item.id,
                "learning_guide_id": self.guide.id,
                "selected_questions": [draft.id],
            },
        )
        self.assertEqual(response.status_code, 400)
        draft.refresh_from_db()
        self.assertEqual(draft.status, "borrador")

    def test_direct_editorial_mutations_require_enabled_topic(self):
        draft = self.create_question(
            question_type="numerica",
            canonical_answer="2",
            status="borrador",
        )
        self.topic.structured_bank_enabled = False
        self.topic.save(update_fields=["structured_bank_enabled"])
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("content:edit_question_inline", args=[draft.id]),
            {
                "text": "No debe cambiar",
                "explanation": "No debe cambiar",
                "order": "1",
                "difficulty": "basica",
                "hint": "No debe cambiar",
                "question_type": "numerica",
                "canonical_answer": "3",
                "answer_tolerance": "",
            },
        )
        self.assertEqual(response.status_code, 400)
        draft.refresh_from_db()
        self.assertEqual(draft.canonical_answer, "2")

    def test_public_guide_hides_preserved_choices_for_direct_questions(self):
        direct = self.create_question(
            question_type="algebraica",
            canonical_answer="x+1",
        )
        Choice.objects.create(
            question=direct,
            text="Preserved hidden choice",
            is_correct=True,
        )
        self.client.force_login(self.student)
        response = self.client.get(
            reverse("content:learning_guide_detail", args=[self.guide.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Preserved hidden choice")
        self.assertContains(response, "Respuesta algebraica")

    def test_direct_answer_is_autoescaped_in_results(self):
        direct = self.create_question(
            question_type="algebraica",
            canonical_answer="x+1",
        )
        self.client.force_login(self.student)
        session_key = f"visible_practice_{self.student.id}_{self.topic.id}"
        session = self.client.session
        session[session_key] = {
            "question_ids": [direct.id],
            "filters": {},
            "order": [direct.id],
        }
        session.save()
        payload = "<img src=x onerror=alert(1)>"
        response = self.client.post(
            reverse("content:submit_visible_practice", args=[self.topic.id]),
            {f"question_{direct.id}": payload},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, payload)
        self.assertContains(response, "&lt;img src=x onerror=alert(1)&gt;")
