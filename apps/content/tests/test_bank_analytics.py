from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import (
    Area,
    Choice,
    Question,
    QuizAttempt,
    QuizAttemptAnswer,
    Resource,
    ResourceQuizConfig,
    Subject,
    Topic,
    TopicEvaluationAttempt,
)
from apps.content.views.bank_analytics import _build_coverage_rows
from apps.content.views.question_review import _build_levels_data


User = get_user_model()


def coverage_counts():
    return {
        "1": {
            "practice": {"pool": 2, "shown": 1},
            "eval": {"pool": 1, "shown": 1},
        },
        "2": {
            "practice": {"pool": 0, "shown": 0},
            "eval": {"pool": 0, "shown": 0},
        },
        "3": {
            "practice": {"pool": 0, "shown": 0},
            "eval": {"pool": 0, "shown": 0},
        },
    }


class BankAnalyticsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password123",
        )
        self.staff = User.objects.create_user(
            username="staff",
            password="password123",
            is_staff=True,
        )
        self.student = User.objects.create_user(
            username="alumno",
            first_name="Ada",
            last_name="Lovelace",
            password="password123",
        )
        self.area = Area.objects.create(name="Matemática", order=1)
        self.subject = Subject.objects.create(name="Álgebra", area=self.area)
        self.topic = Topic.objects.create(name="Ecuaciones", subject=self.subject)
        self.resource = Resource.objects.create(
            title="Ecuaciones cuadráticas",
            subject=self.subject,
            topic=self.topic,
            video_url="https://www.youtube.com/watch?v=test",
            transcript="Contenido de la clase",
        )
        ResourceQuizConfig.objects.create(
            resource=self.resource,
            counts=coverage_counts(),
        )

    def _question(self, *, mode="preparacion", status="publicada", text="Pregunta"):
        question = Question.objects.create(
            resource=self.resource,
            level=1,
            mode=mode,
            status=status,
            text=text,
        )
        correct = Choice.objects.create(
            question=question,
            text="Correcta",
            is_correct=True,
            order=1,
        )
        distractor = Choice.objects.create(
            question=question,
            text="Distractor",
            is_correct=False,
            order=2,
        )
        return question, correct, distractor

    def test_analytics_pages_reject_staff_who_is_not_superuser(self):
        self.client.force_login(self.staff)
        for name in ("content:bank_coverage", "content:bank_results"):
            response = self.client.get(reverse(name))
            self.assertIn(response.status_code, (302, 403))

    def test_coverage_counts_legacy_both_mode_in_both_pools(self):
        self._question(mode="preparacion")
        self._question(mode="ambas")
        self._question(mode="evaluacion", status="borrador")

        self.client.force_login(self.admin)
        response = self.client.get(reverse("content:bank_coverage"))

        self.assertEqual(response.status_code, 200)
        row = response.context["rows"][0]
        self.assertEqual(row["published_total"], 2)
        self.assertEqual(row["draft_total"], 1)
        self.assertEqual(row["levels"][0]["practice"]["available"], 2)
        self.assertEqual(row["levels"][0]["eval"]["available"], 1)
        self.assertEqual(row["overall_state"], "complete")
        self.assertContains(response, "Ecuaciones cuadráticas")

    def test_coverage_query_count_does_not_grow_per_resource(self):
        second = Resource.objects.create(
            title="Funciones",
            subject=self.subject,
            topic=self.topic,
        )
        ResourceQuizConfig.objects.create(resource=second, counts=coverage_counts())

        with self.assertNumQueries(1):
            rows = _build_coverage_rows()
            self.assertEqual(len(rows), 2)

    def test_item_analysis_shows_accuracy_distribution_and_flags(self):
        question, correct, distractor = self._question(mode="evaluacion")
        for number, selected, is_correct in (
            (1, correct, True),
            (2, distractor, False),
            (3, distractor, False),
            (4, distractor, False),
        ):
            attempt = QuizAttempt.objects.create(
                user=self.student,
                resource=self.resource,
                level=1,
                mode="evaluacion",
                score=int(is_correct),
                total=1,
                passed=is_correct,
                attempt_number=number,
            )
            QuizAttemptAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_choice=selected,
                is_correct=is_correct,
            )

        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("content:question_review", args=[self.resource.slug])
        )

        self.assertContains(response, "25% de aciertos")
        self.assertContains(response, "Acierto muy bajo")
        self.assertContains(response, "distractor fue elegido más veces")
        self.assertContains(response, "3 · 75%")

    def test_item_analysis_uses_two_queries_independent_of_question_count(self):
        self._question(text="Primera")
        for index in range(5):
            self._question(text=f"Extra {index}")

        with self.assertNumQueries(2):
            levels = _build_levels_data(self.resource)
            self.assertEqual(levels[0]["count"], 6)

    def test_results_combines_quiz_and_topic_attempts(self):
        QuizAttempt.objects.create(
            user=self.student,
            resource=self.resource,
            level=1,
            mode="evaluacion",
            score=4,
            total=5,
            passed=True,
            attempt_number=1,
        )
        TopicEvaluationAttempt.objects.create(
            user=self.student,
            topic=self.topic,
            score=7,
            total=10,
            percentage=70,
            passed=False,
            attempt_number=1,
        )

        self.client.force_login(self.admin)
        response = self.client.get(reverse("content:bank_results"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["rows"]), 2)
        self.assertEqual(response.context["summary"][0]["attempts"], 2)
        self.assertEqual(response.context["summary"][0]["average"], 75.0)
        self.assertEqual(response.context["summary"][0]["pass_rate"], 50.0)
        self.assertContains(response, "Ada Lovelace")
        self.assertContains(response, "Evaluación")

    def test_results_filters_by_user_and_taxonomy(self):
        other_student = User.objects.create_user(
            username="otro",
            password="password123",
        )
        QuizAttempt.objects.create(
            user=self.student,
            resource=self.resource,
            level=1,
            mode="preparacion",
            score=5,
            total=5,
            passed=False,
            attempt_number=1,
        )
        QuizAttempt.objects.create(
            user=other_student,
            resource=self.resource,
            level=1,
            mode="preparacion",
            score=2,
            total=5,
            passed=False,
            attempt_number=1,
        )

        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("content:bank_results"),
            {
                "area": self.area.id,
                "subject": self.subject.id,
                "topic": self.topic.id,
                "user": self.student.id,
            },
        )

        self.assertEqual(len(response.context["rows"]), 1)
        self.assertEqual(response.context["rows"][0]["user"], self.student)
