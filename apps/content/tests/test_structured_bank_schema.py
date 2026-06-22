"""Fase 0 del epic "Guías interactivas": esquema y flag por tema.

Verifica que los modelos nuevos existen y funcionan, que los constraints
aplican, y —clave— que la ampliación es **aditiva**: las preguntas existentes
quedan "sin clasificar" (`scope=""`) y los temas con el sistema actual.
"""
from datetime import timedelta

from django.db import IntegrityError, transaction
from django.test import TestCase
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
from django.contrib.auth import get_user_model

User = get_user_model()


class StructuredBankSchemaTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Matemáticas banco")
        self.topic = Topic.objects.create(name="Álgebra banco", subject=self.subject)
        self.resource = Resource.objects.create(
            title="Recurso banco", subject=self.subject, topic=self.topic, is_published=True
        )

    def test_topic_flag_defaults_off(self):
        self.assertFalse(self.topic.structured_bank_enabled)
        self.topic.structured_bank_enabled = True
        self.topic.save(update_fields=["structured_bank_enabled"])
        self.topic.refresh_from_db()
        self.assertTrue(self.topic.structured_bank_enabled)

    def test_topic_bank_config_defaults(self):
        cfg = TopicBankConfig.objects.create(topic=self.topic)
        self.assertEqual(cfg.level_eval_minutes, 10)
        self.assertEqual(cfg.level_eval_attempts, 3)
        self.assertEqual(cfg.final_minutes, 45)
        self.assertEqual(cfg.final_attempts, 2)
        self.assertEqual(
            cfg.final_distribution,
            {"conceptual": 20, "mecanico": 50, "aplicacion": 30},
        )
        self.assertEqual(self.topic.bank_config, cfg)

    def test_new_question_fields_are_additive_defaults(self):
        """Una pregunta creada sin tocar los campos nuevos queda sin clasificar."""
        q = Question.objects.create(resource=self.resource, level=1, text="¿Qué es x?")
        self.assertEqual(q.scope, "")  # sin clasificar → no entra al sistema nuevo
        self.assertEqual(q.question_type, "alternativa")
        self.assertEqual(q.difficulty, "")
        self.assertIsNone(q.exercise_item)
        self.assertIsNone(q.learning_guide)
        self.assertEqual(q.points, 1)
        self.assertEqual(q.canonical_answer, "")
        self.assertIsNone(q.answer_tolerance)

    def test_learning_guide_autoslug(self):
        g = LearningGuide.objects.create(topic=self.topic, title="Guía de Álgebra")
        self.assertEqual(g.slug, "guia-de-algebra")
        g2 = LearningGuide.objects.create(topic=self.topic, title="Guía de Álgebra")
        self.assertEqual(g2.slug, "guia-de-algebra-1")
        self.assertEqual(g.visibility, "interna")
        self.assertEqual(g.status, "borrador")

    def test_exercise_item_and_resource_link_quota(self):
        item = ExerciseItem.objects.create(
            topic=self.topic, title="Reducir términos", level=2, objective="Reducir."
        )
        self.assertEqual(item.status, "propuesto")
        link = ResourceExerciseItem.objects.create(
            exercise_item=item, resource=self.resource, practice_quota=5, evaluation_quota=3
        )
        self.assertEqual(link.practice_quota, 5)
        self.assertEqual(link.evaluation_quota, 3)

    def test_resource_exercise_item_unique(self):
        item = ExerciseItem.objects.create(
            topic=self.topic, title="Item", level=1, objective="x"
        )
        ResourceExerciseItem.objects.create(exercise_item=item, resource=self.resource)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ResourceExerciseItem.objects.create(
                    exercise_item=item, resource=self.resource
                )

    def test_evaluation_session_with_answer(self):
        user = User.objects.create_user(username="alu", password="x")
        now = timezone.now()
        session = EvaluationSession.objects.create(
            user=user,
            topic=self.topic,
            kind="prueba_final",
            level=0,
            attempt_number=1,
            started_at=now,
            expires_at=now + timedelta(minutes=45),
        )
        self.assertEqual(session.status, "en_curso")
        q = Question.objects.create(resource=self.resource, level=1, text="P")
        ch = Choice.objects.create(question=q, text="ok", is_correct=True)
        ans = EvaluationSessionAnswer.objects.create(
            session=session, question=q, selected_choice=ch, is_correct=True, points_awarded=1
        )
        self.assertTrue(ans.is_correct)
        # No se puede responder dos veces la misma pregunta en una sesión.
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                EvaluationSessionAnswer.objects.create(session=session, question=q)
