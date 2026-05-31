"""Tests para el sistema de evaluación gamificada."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.content.models import (
    Choice,
    Question,
    QuestionErrorReport,
    QuizAttempt,
    QuizAttemptAnswer,
    Resource,
    ResourceView,
    Subject,
    Topic,
)
from apps.content.services.evaluation_service import (
    MAX_EVAL_ATTEMPTS,
    QUESTIONS_PER_LEVEL,
    get_attempts_info,
    get_questions_for_quiz,
    get_resource_mastery,
    recover_attempt,
    submit_quiz,
)


class EvaluationModelTests(TestCase):
    """Tests para los modelos de evaluación."""

    def setUp(self):
        self.user = User.objects.create_user("alumno", password="test1234")
        self.subject = Subject.objects.create(name="Física", slug="fisica")
        self.topic = Topic.objects.create(
            name="Cinemática", slug="cinematica", subject=self.subject
        )
        self.resource = Resource.objects.create(
            title="MRU", slug="mru", subject=self.subject,
            topic=self.topic, is_published=True,
        )

    def _create_question(self, level=1, mode="ambas", status="publicada"):
        q = Question.objects.create(
            resource=self.resource, level=level, mode=mode,
            text=f"Pregunta N{level}", explanation="Explicación.",
            status=status,
        )
        Choice.objects.create(question=q, text="Correcta", is_correct=True, order=0)
        Choice.objects.create(question=q, text="Incorrecta A", order=1)
        Choice.objects.create(question=q, text="Incorrecta B", order=2)
        Choice.objects.create(question=q, text="Incorrecta C", order=3)
        return q

    def test_question_str(self):
        q = self._create_question()
        self.assertIn("[N1]", str(q))

    def test_choice_str_correct(self):
        q = self._create_question()
        correct = q.choices.get(is_correct=True)
        self.assertTrue(str(correct).startswith("✓"))

    def test_choice_str_incorrect(self):
        q = self._create_question()
        incorrect = q.choices.filter(is_correct=False).first()
        self.assertTrue(str(incorrect).startswith("✗"))

    def test_quiz_attempt_str(self):
        attempt = QuizAttempt.objects.create(
            user=self.user, resource=self.resource,
            level=1, mode="evaluacion", score=5, total=5,
            passed=True, attempt_number=1,
        )
        self.assertIn("✓", str(attempt))
        self.assertIn("5/5", str(attempt))

    def test_error_report_str(self):
        q = self._create_question()
        report = QuestionErrorReport.objects.create(
            user=self.user, question=q,
            reason="enunciado_confuso",
        )
        self.assertIn("Enunciado confuso", str(report))


class EvaluationServiceTests(TestCase):
    """Tests para la lógica de negocio del servicio de evaluación."""

    def setUp(self):
        self.user = User.objects.create_user("alumno", password="test1234")
        self.subject = Subject.objects.create(name="Física", slug="fisica")
        self.topic = Topic.objects.create(
            name="Cinemática", slug="cinematica", subject=self.subject
        )
        self.resource = Resource.objects.create(
            title="MRU", slug="mru", subject=self.subject,
            topic=self.topic, is_published=True,
        )

    def _create_questions(self, level=1, count=5, mode="ambas"):
        questions = []
        for i in range(count):
            q = Question.objects.create(
                resource=self.resource, level=level, mode=mode,
                text=f"Pregunta {i+1} N{level}",
                explanation=f"Explicación {i+1}",
                status="publicada", order=i,
            )
            Choice.objects.create(question=q, text="Correcta", is_correct=True, order=0)
            Choice.objects.create(question=q, text="Incorrecta", order=1)
            Choice.objects.create(question=q, text="Incorrecta 2", order=2)
            Choice.objects.create(question=q, text="Incorrecta 3", order=3)
            questions.append(q)
        return questions

    def test_get_questions_returns_correct_count_level1(self):
        self._create_questions(level=1, count=10)
        questions = get_questions_for_quiz(self.resource, 1, "evaluacion")
        self.assertEqual(len(questions), 5)

    def test_get_questions_returns_correct_count_level3(self):
        self._create_questions(level=3, count=10)
        questions = get_questions_for_quiz(self.resource, 3, "evaluacion")
        self.assertEqual(len(questions), 3)

    def test_get_questions_excludes_drafts(self):
        self._create_questions(level=1, count=5)
        Question.objects.create(
            resource=self.resource, level=1, mode="ambas",
            text="Borrador", status="borrador",
        )
        questions = get_questions_for_quiz(self.resource, 1, "evaluacion")
        texts = [q.text for q in questions]
        self.assertNotIn("Borrador", texts)

    def test_get_questions_filters_by_mode(self):
        self._create_questions(level=1, count=3, mode="preparacion")
        questions = get_questions_for_quiz(self.resource, 1, "evaluacion")
        self.assertEqual(len(questions), 0)

    def test_get_questions_includes_ambas_mode(self):
        self._create_questions(level=1, count=3, mode="ambas")
        questions = get_questions_for_quiz(self.resource, 1, "evaluacion")
        self.assertEqual(len(questions), 3)

    def test_submit_quiz_perfect_score_passes(self):
        questions = self._create_questions(level=1, count=5)
        answers = {}
        for q in questions:
            correct = q.choices.get(is_correct=True)
            answers[q.pk] = correct.pk

        attempt = submit_quiz(self.user, self.resource, 1, "evaluacion", answers)
        self.assertTrue(attempt.passed)
        self.assertEqual(attempt.score, 5)
        self.assertEqual(attempt.total, 5)
        self.assertEqual(attempt.answers.count(), 5)

    def test_submit_quiz_imperfect_score_fails(self):
        questions = self._create_questions(level=1, count=5)
        answers = {}
        for i, q in enumerate(questions):
            if i < 4:
                answers[q.pk] = q.choices.get(is_correct=True).pk
            else:
                answers[q.pk] = q.choices.filter(is_correct=False).first().pk

        attempt = submit_quiz(self.user, self.resource, 1, "evaluacion", answers)
        self.assertFalse(attempt.passed)
        self.assertEqual(attempt.score, 4)

    def test_submit_quiz_rejects_choice_from_another_question(self):
        questions = self._create_questions(level=1, count=5)
        answers = {q.pk: q.choices.get(is_correct=True).pk for q in questions}
        answers[questions[0].pk] = questions[1].choices.get(is_correct=True).pk

        attempt = submit_quiz(self.user, self.resource, 1, "evaluacion", answers)

        self.assertFalse(attempt.passed)
        self.assertEqual(attempt.score, 4)
        first_answer = attempt.answers.get(question=questions[0])
        self.assertIsNone(first_answer.selected_choice)
        self.assertFalse(first_answer.is_correct)

    def test_submit_quiz_level3_passes_with_3_of_3(self):
        questions = self._create_questions(level=3, count=3)
        answers = {q.pk: q.choices.get(is_correct=True).pk for q in questions}
        attempt = submit_quiz(self.user, self.resource, 3, "evaluacion", answers)
        self.assertTrue(attempt.passed)
        self.assertEqual(attempt.score, 3)
        self.assertEqual(attempt.total, 3)

    def test_attempt_number_increments(self):
        questions = self._create_questions(level=1, count=5)
        answers = {q.pk: q.choices.filter(is_correct=False).first().pk for q in questions}

        a1 = submit_quiz(self.user, self.resource, 1, "evaluacion", answers)
        self.assertEqual(a1.attempt_number, 1)

        a2 = submit_quiz(self.user, self.resource, 1, "evaluacion", answers)
        self.assertEqual(a2.attempt_number, 2)

    def test_max_attempts_blocks_evaluation(self):
        questions = self._create_questions(level=1, count=5)
        wrong_answers = {q.pk: q.choices.filter(is_correct=False).first().pk for q in questions}

        for _ in range(MAX_EVAL_ATTEMPTS):
            submit_quiz(self.user, self.resource, 1, "evaluacion", wrong_answers)

        with self.assertRaises(ValueError):
            submit_quiz(self.user, self.resource, 1, "evaluacion", wrong_answers)

    def test_get_attempts_info(self):
        questions = self._create_questions(level=1, count=5)
        wrong_answers = {q.pk: q.choices.filter(is_correct=False).first().pk for q in questions}
        submit_quiz(self.user, self.resource, 1, "evaluacion", wrong_answers)

        info = get_attempts_info(self.user, self.resource, 1)
        self.assertEqual(info["used"], 1)
        self.assertEqual(info["remaining"], 2)
        self.assertFalse(info["passed"])
        self.assertFalse(info["max_reached"])

    def test_practice_does_not_count_as_eval_attempt(self):
        questions = self._create_questions(level=1, count=5)
        answers = {q.pk: q.choices.filter(is_correct=False).first().pk for q in questions}
        submit_quiz(self.user, self.resource, 1, "preparacion", answers)

        info = get_attempts_info(self.user, self.resource, 1)
        self.assertEqual(info["used"], 0)

    def test_recovery_after_practice(self):
        questions = self._create_questions(level=1, count=5)
        wrong = {q.pk: q.choices.filter(is_correct=False).first().pk for q in questions}

        # Use up all attempts
        for _ in range(MAX_EVAL_ATTEMPTS):
            submit_quiz(self.user, self.resource, 1, "evaluacion", wrong)

        info = get_attempts_info(self.user, self.resource, 1)
        self.assertTrue(info["max_reached"])
        self.assertFalse(info["can_recover"])

        # Practice with 100% (≥80%)
        correct = {q.pk: q.choices.get(is_correct=True).pk for q in questions}
        submit_quiz(self.user, self.resource, 1, "preparacion", correct)

        info = get_attempts_info(self.user, self.resource, 1)
        self.assertTrue(info["can_recover"])

        # Recover
        self.assertTrue(recover_attempt(self.user, self.resource, 1))

        info = get_attempts_info(self.user, self.resource, 1)
        self.assertEqual(info["remaining"], 1)

    def test_mastery_zero_without_attempts(self):
        mastery = get_resource_mastery(self.user, self.resource)
        self.assertEqual(mastery["max_level_passed"], 0)
        self.assertEqual(mastery["stars"], 0)

    def test_mastery_increases_with_levels(self):
        for level in (1, 2, 3):
            count = QUESTIONS_PER_LEVEL[level]
            questions = self._create_questions(level=level, count=count)
            correct = {q.pk: q.choices.get(is_correct=True).pk for q in questions}
            submit_quiz(self.user, self.resource, level, "evaluacion", correct)

        mastery = get_resource_mastery(self.user, self.resource)
        self.assertEqual(mastery["max_level_passed"], 3)
        self.assertEqual(mastery["stars"], 3)

    def test_already_passed_raises(self):
        questions = self._create_questions(level=1, count=5)
        correct = {q.pk: q.choices.get(is_correct=True).pk for q in questions}
        submit_quiz(self.user, self.resource, 1, "evaluacion", correct)

        with self.assertRaises(ValueError):
            submit_quiz(self.user, self.resource, 1, "evaluacion", correct)


class EvaluationViewTests(TestCase):
    """Tests para las vistas HTMX de evaluación."""

    def setUp(self):
        self.user = User.objects.create_user("alumno", password="test1234")
        self.subject = Subject.objects.create(name="Física", slug="fisica")
        self.topic = Topic.objects.create(
            name="Cinemática", slug="cinematica", subject=self.subject
        )
        self.resource = Resource.objects.create(
            title="MRU", slug="mru", subject=self.subject,
            topic=self.topic, is_published=True,
        )
        # Create 5 published questions for level 1
        self.questions = []
        for i in range(5):
            q = Question.objects.create(
                resource=self.resource, level=1, mode="ambas",
                text=f"¿Pregunta {i+1}?", explanation=f"Explica {i+1}",
                status="publicada", order=i,
            )
            Choice.objects.create(question=q, text="Sí (correcta)", is_correct=True, order=0)
            Choice.objects.create(question=q, text="No", order=1)
            Choice.objects.create(question=q, text="Quizás", order=2)
            Choice.objects.create(question=q, text="Nunca", order=3)
            self.questions.append(q)

    def test_quiz_start_requires_login(self):
        url = reverse("content:quiz_start", args=[self.resource.slug, 1, "evaluacion"])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("login", resp.url)

    def test_quiz_start_returns_form(self):
        self.client.force_login(self.user)
        url = reverse("content:quiz_start", args=[self.resource.slug, 1, "evaluacion"])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Enviar respuestas")

    def test_quiz_start_invalid_level(self):
        self.client.force_login(self.user)
        url = reverse("content:quiz_start", args=[self.resource.slug, 9, "evaluacion"])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 400)

    def test_quiz_submit_creates_attempt(self):
        self.client.force_login(self.user)
        # Start quiz first to populate session
        start_url = reverse("content:quiz_start", args=[self.resource.slug, 1, "evaluacion"])
        self.client.get(start_url)

        # Build correct answers
        session = self.client.session
        session_key = f"quiz_{self.resource.pk}_1_evaluacion"
        question_ids = session[session_key]

        post_data = {}
        for q_id in question_ids:
            q = Question.objects.get(pk=q_id)
            correct = q.choices.get(is_correct=True)
            post_data[f"question_{q_id}"] = str(correct.pk)

        submit_url = reverse("content:quiz_submit", args=[self.resource.slug, 1, "evaluacion"])
        resp = self.client.post(submit_url, post_data, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Aprobado")
        self.assertTrue(QuizAttempt.objects.filter(user=self.user, passed=True).exists())

    def test_quiz_submit_unanswered_question_counts_as_wrong(self):
        self.client.force_login(self.user)
        start_url = reverse("content:quiz_start", args=[self.resource.slug, 1, "evaluacion"])
        self.client.get(start_url)

        session = self.client.session
        session_key = f"quiz_{self.resource.pk}_1_evaluacion"
        question_ids = session[session_key]

        post_data = {}
        for q_id in question_ids[:-1]:
            q = Question.objects.get(pk=q_id)
            correct = q.choices.get(is_correct=True)
            post_data[f"question_{q_id}"] = str(correct.pk)

        submit_url = reverse("content:quiz_submit", args=[self.resource.slug, 1, "evaluacion"])
        resp = self.client.post(submit_url, post_data, HTTP_HX_REQUEST="true")

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Sin responder")
        attempt = QuizAttempt.objects.get(user=self.user)
        self.assertFalse(attempt.passed)
        self.assertEqual(attempt.score, 4)
        self.assertEqual(attempt.answers.count(), 5)

    def test_quiz_start_already_passed_returns_section(self):
        self.client.force_login(self.user)
        attempt = QuizAttempt.objects.create(
            user=self.user,
            resource=self.resource,
            level=1,
            mode="evaluacion",
            score=5,
            total=5,
            passed=True,
            attempt_number=1,
        )
        QuizAttemptAnswer.objects.create(
            attempt=attempt,
            question=self.questions[0],
            selected_choice=self.questions[0].choices.get(is_correct=True),
            is_correct=True,
        )

        url = reverse("content:quiz_start", args=[self.resource.slug, 1, "evaluacion"])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Demuestra lo aprendido")
        self.assertContains(resp, "Aprobado")

    def test_quiz_status_returns_section(self):
        self.client.force_login(self.user)
        url = reverse("content:quiz_status", args=[self.resource.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Demuestra lo aprendido")

    def test_report_error_creates_report(self):
        self.client.force_login(self.user)
        url = reverse("content:quiz_report_error", args=[self.questions[0].pk])
        resp = self.client.post(url, {
            "reason": "enunciado_confuso",
            "comment": "No entendí",
        }, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            QuestionErrorReport.objects.filter(
                user=self.user,
                question=self.questions[0],
            ).exists()
        )

    def test_report_error_invalid_reason(self):
        self.client.force_login(self.user)
        url = reverse("content:quiz_report_error", args=[self.questions[0].pk])
        resp = self.client.post(url, {"reason": "inventado"})
        self.assertEqual(resp.status_code, 400)

    def test_resource_detail_shows_quiz_section(self):
        self.client.force_login(self.user)
        url = reverse("content:resource_detail", args=[self.resource.slug])
        resp = self.client.get(url)
        self.assertContains(resp, "Demuestra lo aprendido")

    def test_resource_detail_no_quiz_without_questions(self):
        """Sin preguntas publicadas no debe aparecer la sección."""
        Question.objects.all().delete()
        self.client.force_login(self.user)
        url = reverse("content:resource_detail", args=[self.resource.slug])
        resp = self.client.get(url)
        self.assertNotContains(resp, "Demuestra lo aprendido")

    def test_resource_detail_anonymous_no_quiz(self):
        url = reverse("content:resource_detail", args=[self.resource.slug])
        resp = self.client.get(url)
        self.assertNotContains(resp, "Demuestra lo aprendido")

    def test_resource_list_shows_viewed_badge(self):
        ResourceView.objects.create(user=self.user, resource=self.resource)
        self.client.force_login(self.user)

        resp = self.client.get(reverse("content:resource_list"))

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Visto")

    def test_resource_list_shows_approved_stars(self):
        QuizAttempt.objects.create(
            user=self.user,
            resource=self.resource,
            level=2,
            mode="evaluacion",
            score=5,
            total=5,
            passed=True,
            attempt_number=1,
        )
        self.client.force_login(self.user)

        resp = self.client.get(reverse("content:resource_list"))

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Aprobado")
        self.assertContains(resp, "Aprobado con 2 de 3 estrellas")
        self.assertContains(resp, "quiz-badge--stars-2")

    def test_topic_detail_shows_evaluation_summary(self):
        ResourceView.objects.create(user=self.user, resource=self.resource)
        QuizAttempt.objects.create(
            user=self.user,
            resource=self.resource,
            level=3,
            mode="evaluacion",
            score=3,
            total=3,
            passed=True,
            attempt_number=1,
        )
        self.client.force_login(self.user)

        resp = self.client.get(reverse("content:topic_detail", args=[self.topic.slug]))

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "1 aprobados")
        self.assertContains(resp, "3 estrellas")
        self.assertContains(resp, "topic-resource-card--mastery-3")
