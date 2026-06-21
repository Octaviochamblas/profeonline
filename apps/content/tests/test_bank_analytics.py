from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import (
    Area,
    Choice,
    Level,
    Question,
    QuizAttempt,
    QuizAttemptAnswer,
    Resource,
    ResourceQuizConfig,
    Subject,
    Topic,
    TopicEvaluationAttempt,
)
from apps.content.views.bank_analytics import (
    _build_coverage_rows,
    _build_effectiveness_context,
)
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
        self.education_level = Level.objects.create(
            name="Escolar",
            order=1,
        )
        self.subject = Subject.objects.create(name="Álgebra", area=self.area)
        self.topic = Topic.objects.create(name="Ecuaciones", subject=self.subject)
        self.resource = Resource.objects.create(
            title="Ecuaciones cuadráticas",
            subject=self.subject,
            topic=self.topic,
            video_url="https://www.youtube.com/watch?v=test",
            transcript="Contenido de la clase",
            editorial_audit={
                "audited_at": "2026-06-20T00:00:00+00:00",
                "transcript": {"available": True, "audited": True},
                "web": {
                    "title_audited": True,
                    "description_audited": True,
                },
                "youtube": {
                    "title_audited": True,
                    "description_audited": True,
                },
            },
        )
        self.resource.levels.add(self.education_level)
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
        for name in (
            "content:bank_coverage",
            "content:bank_results",
            "content:bank_effectiveness",
        ):
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
        self.assertTrue(row["editorial_complete"])
        self.assertTrue(row["editorial_checks"]["transcript"])
        self.assertEqual(response.context["totals"]["editorial_complete"], 1)
        self.assertContains(response, "Ecuaciones cuadráticas")
        self.assertContains(response, "Título web")
        self.assertContains(response, "Descripción YouTube")

    def test_coverage_marks_pending_editorial_components(self):
        self.resource.editorial_audit = {
            "transcript": {"available": True, "audited": True},
            "web": {
                "title_audited": True,
                "description_audited": False,
            },
            "youtube": {
                "title_audited": False,
                "description_audited": False,
            },
        }
        self.resource.save(
            update_fields=["editorial_audit"],
            _preserve_editorial_audit=True,
        )

        self.client.force_login(self.admin)
        response = self.client.get(reverse("content:bank_coverage"))

        row = response.context["rows"][0]
        self.assertFalse(row["editorial_complete"])
        self.assertEqual(row["editorial_pending"], 3)
        self.assertEqual(response.context["totals"]["editorial_pending"], 1)
        # La hoja del recurso muestra ✓/✗ por categoría editorial.
        self.assertContains(response, "res-audit is-missing")
        self.assertContains(response, "res-audit is-done")

    def test_coverage_tree_aggregates_audit_fractions_per_node(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("content:bank_coverage"))

        tree = response.context["tree"]
        self.assertEqual(len(tree), 1)
        area = tree[0]
        self.assertEqual(area["area"], self.area)
        self.assertEqual(area["resource_count"], 1)
        # El recurso tiene las 5 categorías auditadas → 1/1 en cada una.
        fractions = {item["label"]: (item["done"], item["total"]) for item in area["audit"]}
        self.assertEqual(fractions["Transcripción"], (1, 1))
        self.assertEqual(fractions["Descripción YouTube"], (1, 1))
        level = area["levels"][0]
        self.assertEqual(level["level"], self.education_level)
        subject = level["subjects"][0]
        self.assertEqual(subject["subject"], self.subject)
        topic = subject["topics"][0]
        self.assertEqual(topic["topic"], self.topic)
        self.assertEqual(topic["rows"][0]["resource"], self.resource)

    def test_coverage_status_critical_when_below_twenty_percent(self):
        # pool requerido = 2 (prep N1) + 1 (eval N1) = 3; 0 publicadas → 0% → rojo.
        self.client.force_login(self.admin)
        response = self.client.get(reverse("content:bank_coverage"))

        row = response.context["rows"][0]
        self.assertEqual(row["coverage_status"], "critical")
        self.assertContains(response, "res-row--critical")

    def test_editing_description_invalidates_only_web_description_audit(self):
        self.resource.description = "Descripción modificada después de auditar"
        self.resource.save(update_fields=["description"])
        self.resource.refresh_from_db()

        audit = self.resource.editorial_audit
        self.assertTrue(audit["web"]["title_audited"])
        self.assertFalse(audit["web"]["description_audited"])
        self.assertTrue(audit["youtube"]["title_audited"])
        self.assertTrue(audit["youtube"]["description_audited"])
        self.assertTrue(audit["requires_reaudit"])

    def test_coverage_query_count_does_not_grow_per_resource(self):
        second = Resource.objects.create(
            title="Funciones",
            subject=self.subject,
            topic=self.topic,
        )
        ResourceQuizConfig.objects.create(resource=second, counts=coverage_counts())

        with self.assertNumQueries(2):
            rows = _build_coverage_rows()
            self.assertEqual(len(rows), 2)

    def test_coverage_tree_places_multilevel_resource_in_each_level(self):
        university = Level.objects.create(name="Universitario", order=3)
        self.resource.levels.add(university)

        self.client.force_login(self.admin)
        response = self.client.get(reverse("content:bank_coverage"))

        area = response.context["tree"][0]
        self.assertEqual(area["resource_count"], 1)
        self.assertEqual(
            [node["level"] for node in area["levels"]],
            [self.education_level, university],
        )
        for level in area["levels"]:
            resource = level["subjects"][0]["topics"][0]["rows"][0]["resource"]
            self.assertEqual(resource, self.resource)

    def test_coverage_tree_uses_pedagogical_level_order(self):
        middle = Level.objects.create(
            name="Medio/Preuniversitario",
            order=99,
        )
        university = Level.objects.create(name="Universitario", order=0)
        self.resource.levels.add(middle, university)

        self.client.force_login(self.admin)
        response = self.client.get(reverse("content:bank_coverage"))

        levels = response.context["tree"][0]["levels"]
        self.assertEqual(
            [node["level"].slug for node in levels],
            ["escolar", "mediopreuniversitario", "universitario"],
        )

    def test_coverage_tree_groups_resources_without_level(self):
        self.resource.levels.clear()

        self.client.force_login(self.admin)
        response = self.client.get(reverse("content:bank_coverage"))

        level = response.context["tree"][0]["levels"][0]
        self.assertIsNone(level["level"])
        self.assertContains(response, "Sin nivel")

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

    def _seed_effectiveness_answers(self):
        other_student = User.objects.create_user(
            username="grace",
            first_name="Grace",
            last_name="Hopper",
            password="password123",
        )
        first, first_correct, first_wrong = self._question(
            mode="evaluacion",
            text="Pregunta uno",
        )
        second, second_correct, second_wrong = self._question(
            mode="evaluacion",
            text="Pregunta dos",
        )
        for student, attempt_number, answers in (
            (
                self.student,
                1,
                ((first, first_correct, True), (second, second_wrong, False)),
            ),
            (
                other_student,
                1,
                ((first, first_wrong, False), (second, second_wrong, False)),
            ),
        ):
            attempt = QuizAttempt.objects.create(
                user=student,
                resource=self.resource,
                level=1,
                mode="evaluacion",
                score=sum(is_correct for _q, _choice, is_correct in answers),
                total=2,
                passed=False,
                attempt_number=attempt_number,
            )
            for question, choice, is_correct in answers:
                QuizAttemptAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_choice=choice,
                    is_correct=is_correct,
                )
        return other_student

    def test_effectiveness_filters_single_student_and_compares_global(self):
        self._seed_effectiveness_answers()
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("content:bank_effectiveness"),
            {"users": self.student.id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["totals"]["answers"], 2)
        self.assertEqual(response.context["totals"]["correct"], 1)
        self.assertEqual(response.context["totals"]["students"], 1)
        self.assertEqual(response.context["totals"]["accuracy"], 50.0)
        self.assertEqual(response.context["totals"]["global_accuracy"], 25.0)
        self.assertEqual(response.context["totals"]["delta"], 25.0)
        self.assertEqual(response.context["topic_stats"][0]["accuracy"], 50.0)
        self.assertEqual(response.context["resource_stats"][0]["accuracy"], 50.0)
        self.assertEqual(len(response.context["question_stats"]), 2)
        self.assertContains(response, "Ada Lovelace")
        self.assertContains(response, "+25,0 pp")

    def test_effectiveness_supports_ad_hoc_group_selection(self):
        other_student = self._seed_effectiveness_answers()
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("content:bank_effectiveness"),
            {"users": [self.student.id, other_student.id]},
        )

        self.assertEqual(response.context["totals"]["answers"], 4)
        self.assertEqual(response.context["totals"]["correct"], 1)
        self.assertEqual(response.context["totals"]["students"], 2)
        self.assertEqual(response.context["totals"]["accuracy"], 25.0)
        self.assertEqual(
            response.context["selected_user_ids"],
            [self.student.id, other_student.id],
        )

    def test_effectiveness_aggregations_use_constant_queries(self):
        self._seed_effectiveness_answers()
        filters = {"area": "", "subject": "", "topic": "", "resource": ""}

        with self.assertNumQueries(4):
            context = _build_effectiveness_context(filters, [self.student.id])
            self.assertEqual(context["totals"]["answers"], 2)
            self.assertEqual(len(context["topic_stats"]), 1)
            self.assertEqual(len(context["resource_stats"]), 1)
            self.assertEqual(len(context["question_stats"]), 2)

    def test_results_ignores_invalid_get_filters(self):
        """Parámetros GET no numéricos no deben reventar (500); se ignoran."""
        QuizAttempt.objects.create(
            user=self.student,
            resource=self.resource,
            level=1,
            mode="evaluacion",
            score=3,
            total=5,
            passed=False,
            attempt_number=1,
        )
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("content:bank_results"),
            {"area": "abc", "subject": "x", "topic": "y", "user": "z", "group_by": "raro"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["rows"]), 1)
        self.assertEqual(response.context["group_by"], "student")  # inválido → default

    def test_effectiveness_ignores_invalid_get_filters(self):
        """Filtros/usuarios GET inválidos no rompen; sin selección válida → global."""
        self._seed_effectiveness_answers()
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("content:bank_effectiveness"),
            {"area": "abc", "subject": "x", "topic": "y", "resource": "z", "users": "bad"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["totals"]["answers"], 4)
        self.assertEqual(response.context["selected_user_ids"], [])

    def test_effectiveness_excludes_topic_final_eval(self):
        """La evaluación final de tema no guarda respuestas por pregunta: queda fuera."""
        TopicEvaluationAttempt.objects.create(
            user=self.student,
            topic=self.topic,
            score=8,
            total=10,
            percentage=80,
            passed=True,
            attempt_number=1,
        )
        self.client.force_login(self.admin)
        response = self.client.get(reverse("content:bank_effectiveness"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["totals"]["answers"], 0)
        self.assertEqual(response.context["question_stats"], [])
        self.assertEqual(response.context["topic_stats"], [])
