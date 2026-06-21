"""Tests del motor de progreso académico (progress_service / selectores)."""

from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import SimpleTestCase, TestCase

from apps.content.models import (
    Question,
    QuizAttempt,
    Resource,
    Subject,
    Topic,
)
from apps.content.selectors.evaluation_selectors import (
    get_available_levels_map,
    get_question_availability_map,
    get_recent_attempts_by_resource,
    get_topics_progress_map,
)
from apps.content.services.progress_service import (
    get_profile_progress,
    get_resource_progress,
    select_initial_level,
)

User = get_user_model()


class ProgressTestBase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alumno", password="x")
        self.subject = Subject.objects.create(name="Mate", slug="mate")
        self.topic = Topic.objects.create(name="Enteros", slug="enteros", subject=self.subject)
        self.resource = Resource.objects.create(
            title="Suma", slug="suma", subject=self.subject,
            topic=self.topic, is_published=True,
        )

    def add_questions(self, resource, levels, mode="ambas"):
        for level in levels:
            Question.objects.create(
                resource=resource, level=level, mode=mode,
                text=f"P{level}", status="publicada", order=0,
            )

    def attempt(self, level, mode, pct, passed=False, resource=None):
        """Crea un intento con total=10 → score = pct/10."""
        resource = resource or self.resource
        n = QuizAttempt.objects.filter(
            user=self.user, resource=resource, level=level, mode=mode
        ).count()
        return QuizAttempt.objects.create(
            user=self.user, resource=resource, level=level, mode=mode,
            score=round(pct / 10), total=10, passed=passed, attempt_number=n + 1,
        )


class AveragesTests(ProgressTestBase):
    def test_no_attempts_gives_none_average_and_zero_progress(self):
        self.add_questions(self.resource, [1])
        progress = get_resource_progress(self.user, self.resource)
        lvl = progress["levels"][1]
        self.assertIsNone(lvl["practice_average"])
        self.assertIsNone(lvl["evaluation_average"])
        self.assertEqual(lvl["weighted_progress"], 0)
        self.assertEqual(progress["weighted_progress"], 0)
        self.assertEqual(progress["worked_levels"], [])

    def test_one_and_two_attempts_use_only_available(self):
        self.add_questions(self.resource, [1])
        self.attempt(1, "preparacion", 40)
        self.attempt(1, "preparacion", 60)
        progress = get_resource_progress(self.user, self.resource)
        self.assertEqual(progress["levels"][1]["practice_average"], 50)

    def test_only_last_three_attempts_count(self):
        self.add_questions(self.resource, [1])
        # 4 intentos; los 3 más recientes son 60, 80, 100 -> media 80
        for pct in (10, 60, 80, 100):
            self.attempt(1, "preparacion", pct)
        progress = get_resource_progress(self.user, self.resource)
        self.assertEqual(progress["levels"][1]["practice_average"], 80)
        self.assertEqual(progress["levels"][1]["practice_recent"], [100, 80, 60])


class WeightingTests(ProgressTestBase):
    def test_30_70_weighting(self):
        self.add_questions(self.resource, [1])
        self.attempt(1, "preparacion", 80)
        self.attempt(1, "evaluacion", 50)
        lvl = get_resource_progress(self.user, self.resource)["levels"][1]
        # 80*0.3 + 50*0.7 = 24 + 35 = 59
        self.assertEqual(lvl["weighted_progress"], 59)

    def test_mode_without_attempts_contributes_zero(self):
        self.add_questions(self.resource, [1])
        self.attempt(1, "preparacion", 100)  # sin evaluación
        lvl = get_resource_progress(self.user, self.resource)["levels"][1]
        self.assertEqual(lvl["weighted_progress"], 30)  # 100*0.3 + 0*0.7

    def test_resource_progress_averages_only_worked_levels(self):
        self.add_questions(self.resource, [1, 2, 3])
        self.attempt(1, "evaluacion", 100)   # nivel 1 trabajado -> 70
        # niveles 2 y 3 sin intentos -> excluidos
        progress = get_resource_progress(self.user, self.resource)
        self.assertEqual(progress["worked_levels"], [1])
        self.assertEqual(progress["weighted_progress"], 70)


class HistoricalStateTests(ProgressTestBase):
    def test_passed_persists_even_if_recent_average_drops(self):
        self.add_questions(self.resource, [1])
        self.attempt(1, "evaluacion", 100, passed=True)   # aprobó alguna vez
        for pct in (20, 20, 20):                            # luego bajó
            self.attempt(1, "evaluacion", pct)
        lvl = get_resource_progress(self.user, self.resource)["levels"][1]
        self.assertTrue(lvl["passed"])
        self.assertEqual(lvl["evaluation_average"], 20)

    def test_practice_ready_at_threshold(self):
        self.add_questions(self.resource, [1])
        self.attempt(1, "preparacion", 80)
        lvl = get_resource_progress(self.user, self.resource)["levels"][1]
        self.assertTrue(lvl["practice_ready"])


class AvailabilityTests(ProgressTestBase):
    def test_levels_without_questions_not_shown(self):
        self.add_questions(self.resource, [1, 2])  # nivel 3 sin preguntas
        progress = get_resource_progress(self.user, self.resource)
        self.assertEqual(progress["available_levels"], [1, 2])
        self.assertNotIn(3, progress["levels"])

    def test_available_levels_map(self):
        self.add_questions(self.resource, [1, 3])
        self.assertEqual(
            get_available_levels_map([self.resource.id])[self.resource.id], [1, 3]
        )

    def test_only_practice_question_disables_evaluation_action(self):
        self.add_questions(self.resource, [1], mode="preparacion")
        progress = get_resource_progress(self.user, self.resource)

        self.assertTrue(progress["levels"][1]["practice_available"])
        self.assertFalse(progress["levels"][1]["evaluation_available"])

    def test_only_evaluation_question_disables_practice_action(self):
        self.add_questions(self.resource, [1], mode="evaluacion")
        progress = get_resource_progress(self.user, self.resource)

        self.assertFalse(progress["levels"][1]["practice_available"])
        self.assertTrue(progress["levels"][1]["evaluation_available"])

    def test_both_mode_enables_both_actions(self):
        self.add_questions(self.resource, [1], mode="ambas")
        availability = get_question_availability_map([self.resource.id])

        self.assertEqual(
            availability[self.resource.id][1],
            {"practice": True, "evaluation": True},
        )


class InitialLevelTests(ProgressTestBase):
    def test_initial_is_first_not_passed(self):
        self.add_questions(self.resource, [1, 2, 3])
        self.attempt(1, "evaluacion", 100, passed=True)
        progress = get_resource_progress(self.user, self.resource)
        self.assertEqual(select_initial_level(progress), 2)

    def test_initial_is_highest_when_all_passed(self):
        self.add_questions(self.resource, [1, 2])
        self.attempt(1, "evaluacion", 100, passed=True)
        self.attempt(2, "evaluacion", 100, passed=True)
        progress = get_resource_progress(self.user, self.resource)
        self.assertEqual(select_initial_level(progress), 2)


class BatchQueryTests(ProgressTestBase):
    def test_recent_attempts_batch_is_single_query(self):
        self.add_questions(self.resource, [1, 2])
        other = Resource.objects.create(
            title="Resta", slug="resta", subject=self.subject,
            topic=self.topic, is_published=True,
        )
        self.add_questions(other, [1])
        self.attempt(1, "preparacion", 50)
        self.attempt(2, "evaluacion", 80, passed=True)
        self.attempt(1, "preparacion", 70, resource=other)
        with self.assertNumQueries(1):
            get_recent_attempts_by_resource(self.user, [self.resource.id, other.id])

    def test_topics_progress_uses_weighted_not_completion(self):
        self.add_questions(self.resource, [1])
        self.attempt(1, "evaluacion", 100, passed=True)  # 70 ponderado
        result = get_topics_progress_map(self.user, [self.topic.id])
        self.assertEqual(result[self.topic.id]["weighted_progress"], 70)
        self.assertEqual(result[self.topic.id]["percentage"], 70)
        self.assertEqual(result[self.topic.id]["worked"], 1)

    def test_topics_progress_includes_unstarted_published_resources(self):
        self.add_questions(self.resource, [1], mode="preparacion")
        self.attempt(1, "preparacion", 100)  # recurso iniciado = 30%
        for index in range(2, 20):
            Resource.objects.create(
                title=f"Recurso {index}",
                slug=f"recurso-{index}",
                subject=self.subject,
                topic=self.topic,
                is_published=True,
            )

        result = get_topics_progress_map(self.user, [self.topic.id])[self.topic.id]

        self.assertEqual(result["weighted_progress"], 2)
        self.assertEqual(result["worked"], 1)
        self.assertEqual(result["total"], 19)
        self.assertEqual(result["practice_ready"], 1)
        self.assertEqual(result["practice_total"], 1)
        self.assertEqual(result["evaluation_total"], 0)


class ProfileCoverageTests(ProgressTestBase):
    def test_profile_coverage_counts_all_published_topic_resources(self):
        self.add_questions(self.resource, [1])
        self.attempt(1, "evaluacion", 100, passed=True)
        Resource.objects.create(
            title="Resta",
            slug="resta",
            subject=self.subject,
            topic=self.topic,
            is_published=True,
        )

        groups = get_profile_progress(self.user)

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["worked_count"], 1)
        self.assertEqual(groups[0]["total_count"], 2)
        self.assertEqual(len(groups[0]["resources"]), 1)


class MobileTabsCssTests(SimpleTestCase):
    def test_mobile_tabs_use_three_column_grid_without_horizontal_scroll(self):
        css = (settings.BASE_DIR / "static" / "css" / "estilos.css").read_text(
            encoding="utf-8"
        )

        self.assertIn("grid-template-columns: repeat(3, minmax(0, 1fr));", css)
        self.assertIn("overflow: visible;", css)
        self.assertIn("min-height: 44px;", css)
