from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.content.models import (
    Choice,
    EvaluationSession,
    EvaluationSessionAnswer,
    ExerciseItem,
    LearningGuide,
    Question,
    Resource,
    ResourceExerciseItem,
    Subject,
    Topic,
    TopicBankConfig,
)
from apps.content.services.evaluation_assembly_service import (
    assemble_final_evaluation,
    assemble_level_evaluation,
)
from apps.content.services.evaluation_bank_service import (
    generate_evaluation_bank_questions,
)
from apps.content.services.evaluation_session_service import (
    create_evaluation_session,
    finalize_session,
)
from apps.content.services.structured_progress_service import (
    get_structured_topic_domain,
)

User = get_user_model()


class StructuredEvaluationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="f5-student", password="x")
        self.subject = Subject.objects.create(name="F5 Matemática")
        self.topic = Topic.objects.create(
            name="F5 Álgebra",
            subject=self.subject,
            structured_bank_enabled=True,
        )
        self.config = TopicBankConfig.objects.create(
            topic=self.topic,
            level_eval_minutes=10,
            level_eval_attempts=3,
            final_minutes=10,
            final_attempts=2,
            duration_tolerance_pct=0,
        )
        self.resource = Resource.objects.create(
            title="F5 Recurso",
            subject=self.subject,
            topic=self.topic,
            is_published=True,
        )
        self.item = ExerciseItem.objects.create(
            topic=self.topic,
            title="F5 Ítem",
            level=1,
            objective="Resolver",
            status="aprobado",
            detected_exercise_count=2,
        )
        self.link = ResourceExerciseItem.objects.create(
            exercise_item=self.item,
            resource=self.resource,
            evaluation_quota=2,
        )
        self.guide = LearningGuide.objects.create(
            topic=self.topic,
            title="F5 Guía",
            status="publicada",
            visibility="publica",
        )

    def question(self, *, scope, level=1, points=1, minutes=1, suffix=""):
        question = Question.objects.create(
            resource=self.resource,
            exercise_item=self.item,
            learning_guide=self.guide,
            level=level,
            mode="evaluacion",
            text=f"Pregunta {scope} {level} {suffix}",
            explanation="Explicación",
            hint="Pista",
            difficulty="intermedia",
            question_type="alternativa",
            canonical_answer="Correcta",
            points=points,
            estimated_minutes=minutes,
            scope=scope,
            status="publicada",
        )
        Choice.objects.create(
            question=question, text="Correcta", is_correct=True, order=1
        )
        Choice.objects.create(
            question=question, text="Incorrecta", is_correct=False, order=2
        )
        return question

    def test_hidden_pool_generation_reuses_generation_and_quota(self):
        generated = generate_evaluation_bank_questions(
            exercise_item=self.item,
            resource=self.resource,
            learning_guide=self.guide,
            scope="evaluacion_nivel",
        )
        self.assertEqual(len(generated), 2)
        self.assertTrue(all(q.scope == "evaluacion_nivel" for q in generated))
        self.assertTrue(all(q.status == "borrador" for q in generated))
        self.assertTrue(all(q.estimated_minutes > 0 for q in generated))

    def test_level_assembly_respects_quota_scope_and_no_repeat_then_resets(self):
        questions = [
            self.question(scope="evaluacion_nivel", suffix=str(index))
            for index in range(4)
        ]
        self.question(scope="banco_visible", suffix="legacy-isolation")
        first = assemble_level_evaluation(
            user=self.user, topic=self.topic, resource=self.resource, level=1, seed=1
        )
        session = EvaluationSession.objects.create(
            user=self.user,
            topic=self.topic,
            resource=self.resource,
            kind="evaluacion_nivel",
            level=1,
            attempt_number=1,
            started_at=timezone.now(),
            expires_at=timezone.now() + timedelta(minutes=10),
        )
        session.questions.add(*first)
        second = assemble_level_evaluation(
            user=self.user, topic=self.topic, resource=self.resource, level=1, seed=2
        )
        self.assertEqual(len(first), 2)
        self.assertEqual(len(second), 2)
        self.assertTrue(set(first).isdisjoint(second))
        session2 = EvaluationSession.objects.create(
            user=self.user,
            topic=self.topic,
            resource=self.resource,
            kind="evaluacion_nivel",
            level=1,
            attempt_number=2,
            started_at=timezone.now(),
            expires_at=timezone.now() + timedelta(minutes=10),
        )
        session2.questions.add(*second)
        reset = assemble_level_evaluation(
            user=self.user, topic=self.topic, resource=self.resource, level=1, seed=3
        )
        self.assertEqual(len(reset), 2)
        self.assertTrue(set(reset).issubset(set(questions)))

    def test_final_distribution_by_points_and_duration(self):
        self.link.evaluation_quota = 10
        self.link.save(update_fields=["evaluation_quota"])
        for level, count in ((1, 2), (2, 5), (3, 3)):
            for index in range(count):
                self.question(
                    scope="prueba_final", level=level, suffix=f"{level}-{index}"
                )
        selected = assemble_final_evaluation(
            user=self.user, topic=self.topic, config=self.config, seed=1
        )
        points = {
            level: sum(q.points for q in selected if q.level == level)
            for level in (1, 2, 3)
        }
        self.assertEqual(points, {1: 2, 2: 5, 3: 3})
        self.assertEqual(sum(q.estimated_minutes for q in selected), 10)

    def test_timer_attempts_finalize_grace_and_idempotency(self):
        q1 = self.question(scope="evaluacion_nivel", suffix="1")
        q2 = self.question(scope="evaluacion_nivel", suffix="2")
        now = timezone.now()
        session = create_evaluation_session(
            user=self.user,
            topic=self.topic,
            resource=self.resource,
            kind="evaluacion_nivel",
            level=1,
            now=now,
            seed=1,
        )
        self.assertEqual(session.attempt_number, 1)
        self.assertEqual(session.expires_at, now + timedelta(minutes=10))
        same = create_evaluation_session(
            user=self.user,
            topic=self.topic,
            resource=self.resource,
            kind="evaluacion_nivel",
            level=1,
            now=now,
        )
        self.assertEqual(same.pk, session.pk)
        correct = q1.choices.get(is_correct=True)
        submitted = finalize_session(
            session=session,
            answers={q1.id: str(correct.id)},
            now=session.expires_at + timedelta(seconds=10),
        )
        self.assertEqual(submitted.status, "enviada")
        self.assertEqual(submitted.answers.count(), 2)
        self.assertEqual(
            submitted.answers.get(question=q2).points_awarded, 0
        )
        finalize_session(session=submitted, answers={}, now=timezone.now())
        self.assertEqual(submitted.answers.count(), 2)

        late = create_evaluation_session(
            user=self.user,
            topic=self.topic,
            resource=self.resource,
            kind="evaluacion_nivel",
            level=1,
            now=now,
            seed=2,
        )
        late = finalize_session(
            session=late,
            answers={q1.id: str(correct.id)},
            now=late.expires_at + timedelta(seconds=16),
        )
        self.assertEqual(late.status, "vencida")
        self.assertFalse(late.answers.filter(is_correct=True).exists())

    def test_attempt_limit_and_flag_isolation(self):
        self.question(scope="evaluacion_nivel", suffix="1")
        self.question(scope="evaluacion_nivel", suffix="2")
        self.config.level_eval_attempts = 1
        self.config.save(update_fields=["level_eval_attempts"])
        session = create_evaluation_session(
            user=self.user,
            topic=self.topic,
            resource=self.resource,
            kind="evaluacion_nivel",
            level=1,
        )
        finalize_session(session=session, answers={})
        with self.assertRaisesMessage(ValueError, "No quedan intentos"):
            create_evaluation_session(
                user=self.user,
                topic=self.topic,
                resource=self.resource,
                kind="evaluacion_nivel",
                level=1,
            )
        self.topic.structured_bank_enabled = False
        self.topic.save(update_fields=["structured_bank_enabled"])
        self.assertIsNone(get_structured_topic_domain(self.user, self.topic))

    def test_structured_domain_uses_latest_attempt_and_final_gate(self):
        # One resource, three required levels. Missing levels count as zero.
        level_question = self.question(scope="evaluacion_nivel", points=1)
        for attempt, correct in ((1, True), (2, False)):
            session = EvaluationSession.objects.create(
                user=self.user,
                topic=self.topic,
                resource=self.resource,
                kind="evaluacion_nivel",
                level=1,
                attempt_number=attempt,
                started_at=timezone.now(),
                expires_at=timezone.now(),
                status="enviada",
            )
            EvaluationSessionAnswer.objects.create(
                session=session,
                question=level_question,
                is_correct=correct,
                points_awarded=1 if correct else 0,
            )
        final_question = self.question(scope="prueba_final", points=1)
        final = EvaluationSession.objects.create(
            user=self.user,
            topic=self.topic,
            kind="prueba_final",
            level=0,
            attempt_number=1,
            started_at=timezone.now(),
            expires_at=timezone.now(),
            status="enviada",
        )
        EvaluationSessionAnswer.objects.create(
            session=final,
            question=final_question,
            is_correct=True,
            points_awarded=1,
        )
        domain = get_structured_topic_domain(self.user, self.topic)
        self.assertEqual(domain["levels_average"], 0)
        self.assertEqual(domain["final_score"], 100)
        self.assertEqual(domain["weighted_score"], 40)
        self.assertFalse(domain["dominated"])

    def test_student_views_require_login_and_reject_foreign_answers(self):
        self.question(scope="evaluacion_nivel", suffix="1")
        self.question(scope="evaluacion_nivel", suffix="2")
        start_url = reverse(
            "content:start_structured_evaluation", args=[self.topic.id]
        )
        response = self.client.post(
            start_url,
            {"kind": "evaluacion_nivel", "resource_id": self.resource.id, "level": 1},
        )
        self.assertEqual(response.status_code, 302)
        self.client.force_login(self.user)
        response = self.client.post(
            start_url,
            {"kind": "evaluacion_nivel", "resource_id": self.resource.id, "level": 1},
        )
        self.assertEqual(response.status_code, 200)
        session = EvaluationSession.objects.get(user=self.user, status="en_curso")
        foreign = self.question(scope="evaluacion_nivel", suffix="foreign")
        submit_url = reverse(
            "content:submit_structured_evaluation", args=[session.id]
        )
        response = self.client.post(
            submit_url, {f"question_{foreign.id}": foreign.choices.first().id}
        )
        self.assertEqual(response.status_code, 400)
        session.refresh_from_db()
        self.assertEqual(session.status, "en_curso")

    def test_admin_pool_publication_requires_positive_duration(self):
        admin = User.objects.create_superuser(
            username="f5-admin", email="f5@example.com", password="x"
        )
        question = self.question(scope="prueba_final", minutes=1)
        question.status = "borrador"
        question.estimated_minutes = 0
        question.save(update_fields=["status", "estimated_minutes"])
        self.client.force_login(admin)
        response = self.client.post(
            reverse("content:bulk_action_questions", args=[self.resource.id]),
            {
                "action": "publicar",
                "scope": "prueba_final",
                "exercise_item_id": self.item.id,
                "learning_guide_id": self.guide.id,
                "selected_questions": [question.id],
            },
        )
        self.assertEqual(response.status_code, 400)
        question.refresh_from_db()
        self.assertEqual(question.status, "borrador")
