"""Tests para el sistema de evaluación gamificada."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

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
    TopicEvaluationAttempt,
    UserSkill,
    UserStreak,
    XPEvent,
)
from apps.content.services.gamification_service import (
    award_quiz_attempt_xp,
    award_xp,
    get_gamification_summary,
    get_user_rank,
)
from apps.content.services.evaluation_service import (
    MAX_EVAL_ATTEMPTS,
    QUESTIONS_PER_LEVEL,
    TOPIC_EXAM_QUESTION_COUNT,
    get_attempts_info,
    get_questions_for_quiz,
    get_resource_mastery,
    get_topic_exam_info,
    get_topic_exam_questions,
    recover_attempt,
    submit_quiz,
    submit_topic_exam,
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


class TopicExamServiceTests(TestCase):
    """Tests para la evaluación final por tema (Fase 7)."""

    def setUp(self):
        self.user = User.objects.create_user("alumno", password="test1234")
        self.subject = Subject.objects.create(name="Física", slug="fisica")
        self.topic = Topic.objects.create(
            name="Cinemática", slug="cinematica", subject=self.subject
        )
        self.other_topic = Topic.objects.create(
            name="Dinámica", slug="dinamica", subject=self.subject
        )

    def _make_resource(self, slug, topic=None, is_published=True):
        return Resource.objects.create(
            title=slug.upper(), slug=slug, subject=self.subject,
            topic=topic or self.topic, is_published=is_published,
        )

    def _add_questions(self, resource, count, level=1, mode="evaluacion",
                       status="publicada"):
        questions = []
        for i in range(count):
            q = Question.objects.create(
                resource=resource, level=level, mode=mode,
                text=f"{resource.slug} P{i+1}", explanation=f"Exp {i+1}",
                status=status, order=i,
            )
            Choice.objects.create(question=q, text="Correcta", is_correct=True, order=0)
            Choice.objects.create(question=q, text="Mala 1", order=1)
            Choice.objects.create(question=q, text="Mala 2", order=2)
            questions.append(q)
        return questions

    def test_exam_questions_compiled_from_topic_resources(self):
        r1 = self._make_resource("mru")
        r2 = self._make_resource("mruv")
        self._add_questions(r1, 5)
        self._add_questions(r2, 5)
        questions = get_topic_exam_questions(self.topic)
        self.assertEqual(len(questions), 10)

    def test_exam_caps_at_question_count(self):
        r1 = self._make_resource("mru")
        self._add_questions(r1, TOPIC_EXAM_QUESTION_COUNT + 5)
        questions = get_topic_exam_questions(self.topic)
        self.assertEqual(len(questions), TOPIC_EXAM_QUESTION_COUNT)

    def test_exam_excludes_drafts_and_prep_only_and_other_topics(self):
        r1 = self._make_resource("mru")
        self._add_questions(r1, 3)  # válidas
        self._add_questions(r1, 2, status="borrador")
        self._add_questions(r1, 2, mode="preparacion")
        other = self._make_resource("calor", topic=self.other_topic)
        self._add_questions(other, 4)
        questions = get_topic_exam_questions(self.topic)
        self.assertEqual(len(questions), 3)

    def test_submit_passes_at_threshold(self):
        r1 = self._make_resource("mru")
        questions = self._add_questions(r1, 10)
        answers = {q.pk: q.choices.get(is_correct=True).pk for q in questions[:8]}
        answers.update({q.pk: q.choices.filter(is_correct=False).first().pk
                        for q in questions[8:]})
        attempt, results = submit_topic_exam(self.user, self.topic, answers)
        self.assertEqual(attempt.score, 8)
        self.assertEqual(attempt.total, 10)
        self.assertEqual(attempt.percentage, 80)
        self.assertTrue(attempt.passed)
        self.assertEqual(len(results), 10)

    def test_submit_fails_below_threshold(self):
        r1 = self._make_resource("mru")
        questions = self._add_questions(r1, 10)
        answers = {q.pk: q.choices.get(is_correct=True).pk for q in questions[:7]}
        answers.update({q.pk: None for q in questions[7:]})
        attempt, _ = submit_topic_exam(self.user, self.topic, answers)
        self.assertEqual(attempt.score, 7)
        self.assertEqual(attempt.percentage, 70)
        self.assertFalse(attempt.passed)

    def test_submit_rejects_choice_from_another_question(self):
        r1 = self._make_resource("mru")
        questions = self._add_questions(r1, 10)
        answers = {q.pk: q.choices.get(is_correct=True).pk for q in questions}
        # Inyectar una alternativa de otra pregunta en la primera
        answers[questions[0].pk] = questions[1].choices.get(is_correct=True).pk
        attempt, results = submit_topic_exam(self.user, self.topic, answers)
        self.assertEqual(attempt.score, 9)
        first = next(r for r in results if r["question"].pk == questions[0].pk)
        self.assertIsNone(first["selected"])
        self.assertFalse(first["is_correct"])

    def test_info_tracks_best_and_brilliance(self):
        r1 = self._make_resource("mru")
        questions = self._add_questions(r1, 10)
        # Intento 1: 80% (aprueba, brillo 1)
        a1 = {q.pk: q.choices.get(is_correct=True).pk for q in questions[:8]}
        a1.update({q.pk: None for q in questions[8:]})
        submit_topic_exam(self.user, self.topic, a1)
        # Intento 2: 100% (brillo 3)
        a2 = {q.pk: q.choices.get(is_correct=True).pk for q in questions}
        submit_topic_exam(self.user, self.topic, a2)

        info = get_topic_exam_info(self.user, self.topic)
        self.assertTrue(info["passed"])
        self.assertEqual(info["used"], 2)
        self.assertEqual(info["best_percentage"], 100)
        self.assertEqual(info["brilliance"], 3)
        self.assertEqual(info["threshold"], 80)

    def test_attempt_number_increments(self):
        r1 = self._make_resource("mru")
        questions = self._add_questions(r1, 10)
        answers = {q.pk: q.choices.get(is_correct=True).pk for q in questions}
        a1, _ = submit_topic_exam(self.user, self.topic, answers)
        a2, _ = submit_topic_exam(self.user, self.topic, answers)
        self.assertEqual(a1.attempt_number, 1)
        self.assertEqual(a2.attempt_number, 2)

    def test_info_no_exam_without_questions(self):
        info = get_topic_exam_info(self.user, self.topic)
        self.assertFalse(info["has_exam"])
        self.assertEqual(info["available_questions"], 0)


class TopicExamViewTests(TestCase):
    """Tests para las vistas HTMX de la evaluación final por tema."""

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
        self.questions = []
        for i in range(6):
            q = Question.objects.create(
                resource=self.resource, level=1, mode="evaluacion",
                text=f"¿Pregunta {i+1}?", explanation=f"Explica {i+1}",
                status="publicada", order=i,
            )
            Choice.objects.create(question=q, text="Sí (correcta)", is_correct=True, order=0)
            Choice.objects.create(question=q, text="No", order=1)
            self.questions.append(q)

    def test_exam_start_requires_login(self):
        url = reverse("content:topic_exam_start", args=[self.topic.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("login", resp.url)

    def test_exam_start_returns_form(self):
        self.client.force_login(self.user)
        url = reverse("content:topic_exam_start", args=[self.topic.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Enviar evaluación")

    def test_exam_start_empty_without_questions(self):
        Question.objects.all().delete()
        self.client.force_login(self.user)
        url = reverse("content:topic_exam_start", args=[self.topic.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Aún no hay preguntas")

    def test_exam_submit_creates_attempt_and_passes(self):
        self.client.force_login(self.user)
        start_url = reverse("content:topic_exam_start", args=[self.topic.slug])
        self.client.get(start_url)

        session = self.client.session
        question_ids = session[f"topic_exam_{self.topic.pk}"]
        post_data = {
            f"question_{q_id}": str(
                Question.objects.get(pk=q_id).choices.get(is_correct=True).pk
            )
            for q_id in question_ids
        }

        submit_url = reverse("content:topic_exam_submit", args=[self.topic.slug])
        resp = self.client.post(submit_url, post_data, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Tema aprobado")
        self.assertTrue(
            TopicEvaluationAttempt.objects.filter(
                user=self.user, topic=self.topic, passed=True
            ).exists()
        )

    def test_exam_submit_without_active_session(self):
        self.client.force_login(self.user)
        submit_url = reverse("content:topic_exam_submit", args=[self.topic.slug])
        resp = self.client.post(submit_url, {}, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 400)

    def test_topic_detail_shows_exam_section(self):
        self.client.force_login(self.user)
        resp = self.client.get(
            reverse("content:topic_detail", args=[self.topic.slug])
        )
        self.assertContains(resp, "Evaluación final del tema")

    def test_topic_detail_anonymous_no_exam_section(self):
        resp = self.client.get(
            reverse("content:topic_detail", args=[self.topic.slug])
        )
        self.assertNotContains(resp, "Evaluación final del tema")

    def test_topic_detail_shows_mastery_badge_when_passed(self):
        TopicEvaluationAttempt.objects.create(
            user=self.user, topic=self.topic, score=6, total=6,
            percentage=100, passed=True, attempt_number=1,
        )
        self.client.force_login(self.user)
        resp = self.client.get(
            reverse("content:topic_detail", args=[self.topic.slug])
        )
        self.assertContains(resp, "Tema dominado")


class GamificationTests(TestCase):
    """Tests para XP, skills, rangos y rachas (Fase 8)."""

    def setUp(self):
        self.user = User.objects.create_user("alumno", password="test1234")
        self.subject = Subject.objects.create(name="Fisica", slug="fisica")
        self.topic = Topic.objects.create(
            name="Cinematica", slug="cinematica", subject=self.subject
        )
        self.resource = Resource.objects.create(
            title="MRU", slug="mru", subject=self.subject,
            topic=self.topic, is_published=True,
        )

    def _add_questions(self, count=5, level=1, mode="evaluacion"):
        questions = []
        for i in range(count):
            q = Question.objects.create(
                resource=self.resource,
                level=level,
                mode=mode,
                text=f"Pregunta {i + 1}",
                explanation="Explicacion",
                status="publicada",
                order=i,
            )
            Choice.objects.create(question=q, text="Correcta", is_correct=True, order=0)
            Choice.objects.create(question=q, text="Incorrecta", order=1)
            questions.append(q)
        return questions

    def _correct_answers(self, questions):
        return {q.pk: q.choices.get(is_correct=True).pk for q in questions}

    def test_practice_awards_xp_and_reduces_repeated_section(self):
        questions = self._add_questions(count=5, level=1, mode="preparacion")

        for _ in range(4):
            submit_quiz(
                self.user,
                self.resource,
                1,
                "preparacion",
                self._correct_answers(questions),
            )

        amounts = list(
            XPEvent.objects.filter(user=self.user, event_type="practice")
            .order_by("created_at")
            .values_list("amount", flat=True)
        )
        self.assertEqual(amounts, [15, 15, 15, 5])

    def test_resource_level_pass_xp_is_idempotent(self):
        questions = self._add_questions(count=5, level=1, mode="evaluacion")
        answers = self._correct_answers(questions)

        attempt = submit_quiz(self.user, self.resource, 1, "evaluacion", answers)
        award_quiz_attempt_xp(attempt)

        events = XPEvent.objects.filter(
            user=self.user,
            event_type="resource_level_pass",
            resource=self.resource,
        )
        self.assertEqual(events.count(), 1)
        self.assertEqual(events.get().amount, 25)

    def test_topic_exam_pass_unlocks_skill_and_xp_once(self):
        questions = self._add_questions(count=10, level=1, mode="evaluacion")
        answers = self._correct_answers(questions)

        submit_topic_exam(self.user, self.topic, answers)
        submit_topic_exam(self.user, self.topic, answers)

        self.assertEqual(UserSkill.objects.filter(user=self.user, topic=self.topic).count(), 1)
        self.assertEqual(
            XPEvent.objects.filter(user=self.user, event_type="topic_exam_pass").count(),
            1,
        )
        self.assertEqual(
            XPEvent.objects.filter(user=self.user, event_type="skill_unlock").count(),
            1,
        )
        summary = get_gamification_summary(self.user)
        self.assertEqual(summary["total_xp"], 150)
        self.assertEqual(summary["skill_count"], 1)

    def test_rank_uses_xp_and_skills(self):
        rank = get_user_rank(total_xp=450, skill_count=2)
        self.assertEqual(rank["name"], "Practico")
        gated_rank = get_user_rank(total_xp=450, skill_count=0)
        self.assertEqual(gated_rank["name"], "Explorador")

    def test_streak_continues_and_awards_bonus(self):
        yesterday = timezone.localdate() - timezone.timedelta(days=1)
        UserStreak.objects.create(
            user=self.user,
            current_count=2,
            longest_count=2,
            last_activity_date=yesterday,
        )

        award_xp(
            user=self.user,
            amount=5,
            event_type="practice",
            event_key="manual-practice",
        )

        streak = UserStreak.objects.get(user=self.user)
        self.assertEqual(streak.current_count, 3)
        self.assertEqual(streak.longest_count, 3)
        self.assertTrue(
            XPEvent.objects.filter(user=self.user, event_type="streak_bonus").exists()
        )

    def test_profile_shows_gamification_summary(self):
        award_xp(
            user=self.user,
            amount=25,
            event_type="resource_level_pass",
            event_key="manual-pass",
            resource=self.resource,
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse("profile"))

        self.assertContains(response, "Progreso gamificado")
        self.assertContains(response, "25 XP")
