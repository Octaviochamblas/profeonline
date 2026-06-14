from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.content.models import Area, Subject, Topic, Level, Resource, ResourceQuizConfig
from apps.content.services.evaluation_service import (
    get_quiz_config,
    get_questions_for_quiz,
    get_attempts_info,
    submit_quiz,
    _can_recover,
)
from apps.content.models import Question, Choice, QuizAttempt

User = get_user_model()


class ResourceQuizConfigTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="teststudent", password="password123")
        self.area = Area.objects.create(name="Matemática", order=1)
        self.subject = Subject.objects.create(name="Álgebra", area=self.area)
        self.topic = Topic.objects.create(name="Ecuaciones", subject=self.subject)
        self.resource = Resource.objects.create(
            title="Ecuaciones Cuadráticas",
            subject=self.subject,
            topic=self.topic,
        )

    def test_get_quiz_config_fallback(self):
        # El recurso no tiene configuración explícita
        config = get_quiz_config(self.resource)
        self.assertEqual(config.pass_threshold, 1.0)
        self.assertEqual(config.max_attempts, 3)
        self.assertEqual(config.recovery_rule, "practice_5_5")
        self.assertFalse(config.allow_retake_passed)
        self.assertFalse(config.autopublish)
        self.assertEqual(config.counts["1"]["practice"]["shown"], 5)
        self.assertEqual(config.counts["1"]["eval"]["shown"], 5)

    def test_get_quiz_config_override(self):
        # Crear una configuración explícita
        counts = {
            "1": {"practice": {"pool": 10, "shown": 6}, "eval": {"pool": 8, "shown": 4}},
            "2": {"practice": {"pool": 10, "shown": 6}, "eval": {"pool": 8, "shown": 4}},
            "3": {"practice": {"pool": 10, "shown": 6}, "eval": {"pool": 8, "shown": 4}}
        }
        ResourceQuizConfig.objects.create(
            resource=self.resource,
            counts=counts,
            pass_threshold=0.8,
            max_attempts=5,
            recovery_rule="none",
            allow_retake_passed=False,
            autopublish=True,
        )

        # Volver a cargar el recurso para asegurar la relación one-to-one
        self.resource.refresh_from_db()
        config = get_quiz_config(self.resource)
        self.assertEqual(config.pass_threshold, 0.8)
        self.assertEqual(config.max_attempts, 5)
        self.assertEqual(config.recovery_rule, "none")
        self.assertFalse(config.allow_retake_passed)
        self.assertTrue(config.autopublish)
        self.assertEqual(config.counts["1"]["practice"]["shown"], 6)
        self.assertEqual(config.counts["1"]["eval"]["shown"], 4)

    def test_config_validation_invalid_counts_structure(self):
        # Falta nivel 3
        invalid_counts = {
            "1": {"practice": {"pool": 10, "shown": 5}, "eval": {"pool": 8, "shown": 3}},
            "2": {"practice": {"pool": 10, "shown": 5}, "eval": {"pool": 8, "shown": 3}}
        }
        config = ResourceQuizConfig(resource=self.resource, counts=invalid_counts)
        with self.assertRaises(ValidationError):
            config.clean()

    def test_config_validation_shown_exceeds_pool(self):
        # shown > pool
        invalid_counts = {
            "1": {"practice": {"pool": 5, "shown": 6}, "eval": {"pool": 8, "shown": 3}},
            "2": {"practice": {"pool": 10, "shown": 5}, "eval": {"pool": 8, "shown": 3}},
            "3": {"practice": {"pool": 10, "shown": 5}, "eval": {"pool": 8, "shown": 3}}
        }
        config = ResourceQuizConfig(resource=self.resource, counts=invalid_counts)
        with self.assertRaises(ValidationError):
            config.clean()

    def test_config_validation_negative_counts(self):
        invalid_counts = {
            "1": {"practice": {"pool": -1, "shown": 5}, "eval": {"pool": 8, "shown": 3}},
            "2": {"practice": {"pool": 10, "shown": 5}, "eval": {"pool": 8, "shown": 3}},
            "3": {"practice": {"pool": 10, "shown": 5}, "eval": {"pool": 8, "shown": 3}}
        }
        config = ResourceQuizConfig(resource=self.resource, counts=invalid_counts)
        with self.assertRaises(ValidationError):
            config.clean()

    def test_runtime_questions_count(self):
        # Crear preguntas suficientes
        for i in range(10):
            q = Question.objects.create(
                resource=self.resource,
                level=1,
                mode="evaluacion",
                text=f"Pregunta {i}",
                status="publicada",
                order=i,
            )
            Choice.objects.create(question=q, text="Opción correcta", is_correct=True)

        # Sin configuración, por defecto se muestran 5 en evaluación (Nivel 1)
        questions = get_questions_for_quiz(self.resource, level=1, mode="evaluacion")
        self.assertEqual(len(questions), 5)

        # Con configuración custom que dice 6
        counts = {
            "1": {"practice": {"pool": 10, "shown": 5}, "eval": {"pool": 10, "shown": 6}},
            "2": {"practice": {"pool": 10, "shown": 5}, "eval": {"pool": 10, "shown": 3}},
            "3": {"practice": {"pool": 10, "shown": 5}, "eval": {"pool": 10, "shown": 3}}
        }
        ResourceQuizConfig.objects.create(resource=self.resource, counts=counts)
        self.resource.refresh_from_db()

        questions = get_questions_for_quiz(self.resource, level=1, mode="evaluacion")
        self.assertEqual(len(questions), 6)

    def test_attempts_limit_and_retake(self):
        # Configurar 2 intentos máximos y no permitir repetir
        counts = {
            "1": {"practice": {"pool": 5, "shown": 2}, "eval": {"pool": 5, "shown": 2}},
            "2": {"practice": {"pool": 5, "shown": 2}, "eval": {"pool": 5, "shown": 2}},
            "3": {"practice": {"pool": 5, "shown": 2}, "eval": {"pool": 5, "shown": 2}}
        }
        ResourceQuizConfig.objects.create(
            resource=self.resource,
            counts=counts,
            max_attempts=2,
            allow_retake_passed=False,
            pass_threshold=1.0,
        )
        self.resource.refresh_from_db()

        # Crear 2 preguntas
        q1 = Question.objects.create(resource=self.resource, level=1, mode="evaluacion", text="Q1", status="publicada")
        c1 = Choice.objects.create(question=q1, text="C1", is_correct=True)
        q2 = Question.objects.create(resource=self.resource, level=1, mode="evaluacion", text="Q2", status="publicada")
        c2 = Choice.objects.create(question=q2, text="C2", is_correct=True)

        # Intento 1: fallado
        attempt1 = submit_quiz(self.user, self.resource, level=1, mode="evaluacion", answers_dict={q1.id: None, q2.id: None})
        self.assertFalse(attempt1.passed)

        info = get_attempts_info(self.user, self.resource, level=1)
        self.assertEqual(info["used"], 1)
        self.assertEqual(info["remaining"], 1)
        self.assertFalse(info["max_reached"])

        # Intento 2: aprobado
        attempt2 = submit_quiz(self.user, self.resource, level=1, mode="evaluacion", answers_dict={q1.id: c1.id, q2.id: c2.id})
        self.assertTrue(attempt2.passed)

        info = get_attempts_info(self.user, self.resource, level=1)
        self.assertEqual(info["used"], 2)
        self.assertEqual(info["remaining"], 0)
        self.assertTrue(info["max_reached"])
        self.assertTrue(info["passed"])

        # Intentar rendir de nuevo: debería lanzar error de que ya aprobó
        with self.assertRaises(ValueError) as ctx:
            submit_quiz(self.user, self.resource, level=1, mode="evaluacion", answers_dict={q1.id: c1.id, q2.id: c2.id})
        self.assertEqual(str(ctx.exception), "Ya aprobaste este nivel.")

    def test_recovery_rule_perfect_practice(self):
        # Configurar recuperación con práctica perfecta (practice_5_5) y 1 intento max
        counts = {
            "1": {"practice": {"pool": 5, "shown": 2}, "eval": {"pool": 5, "shown": 2}},
            "2": {"practice": {"pool": 5, "shown": 2}, "eval": {"pool": 5, "shown": 2}},
            "3": {"practice": {"pool": 5, "shown": 2}, "eval": {"pool": 5, "shown": 2}}
        }
        ResourceQuizConfig.objects.create(
            resource=self.resource,
            counts=counts,
            max_attempts=1,
            recovery_rule="practice_5_5",
        )
        self.resource.refresh_from_db()

        # Crear preguntas
        q1 = Question.objects.create(resource=self.resource, level=1, mode="ambas", text="Q1", status="publicada")
        c1 = Choice.objects.create(question=q1, text="C1", is_correct=True)
        q2 = Question.objects.create(resource=self.resource, level=1, mode="ambas", text="Q2", status="publicada")
        c2 = Choice.objects.create(question=q2, text="C2", is_correct=True)

        # Intento 1 de evaluación fallido
        submit_quiz(self.user, self.resource, level=1, mode="evaluacion", answers_dict={q1.id: None, q2.id: None})

        info = get_attempts_info(self.user, self.resource, level=1)
        self.assertTrue(info["max_reached"])
        self.assertFalse(info["can_recover"])

        # Práctica imperfecta (1/2 correctas = 50%) -> no debería poder recuperar bajo practice_5_5
        submit_quiz(self.user, self.resource, level=1, mode="preparacion", answers_dict={q1.id: c1.id, q2.id: None})
        self.assertFalse(_can_recover(self.user, self.resource, level=1))

        # Práctica perfecta (2/2 correctas = 100%) -> debería poder recuperar
        submit_quiz(self.user, self.resource, level=1, mode="preparacion", answers_dict={q1.id: c1.id, q2.id: c2.id})
        self.assertTrue(_can_recover(self.user, self.resource, level=1))

        info = get_attempts_info(self.user, self.resource, level=1)
        self.assertTrue(info["can_recover"])

        # Al rendir de nuevo con can_recover = True, submit_quiz debe auto-recuperar (borrar el fallido anterior)
        attempt = submit_quiz(self.user, self.resource, level=1, mode="evaluacion", answers_dict={q1.id: c1.id, q2.id: c2.id})
        self.assertTrue(attempt.passed)


class QuestionStudioViewsTests(TestCase):
    """Smoke + permisos de las páginas solo-admin del banco de preguntas."""

    def setUp(self):
        from django.urls import reverse

        self.reverse = reverse
        self.admin = User.objects.create_superuser(
            username="admin", password="password123", email="admin@test.cl"
        )
        self.student = User.objects.create_user(
            username="alumno", password="password123"
        )
        self.area = Area.objects.create(name="Matemática", order=1)
        self.subject = Subject.objects.create(name="Álgebra", area=self.area)
        self.topic = Topic.objects.create(name="Ecuaciones", subject=self.subject)
        self.resource = Resource.objects.create(
            title="Ecuaciones Cuadráticas",
            subject=self.subject,
            topic=self.topic,
        )

    def test_studio_rejects_non_admin(self):
        self.client.force_login(self.student)
        resp = self.client.get(self.reverse("content:question_studio"))
        self.assertIn(resp.status_code, (302, 403))

    def test_studio_renders_for_admin(self):
        self.client.force_login(self.admin)
        resp = self.client.get(self.reverse("content:question_studio"))
        self.assertEqual(resp.status_code, 200)

    def test_review_rejects_non_admin(self):
        self.client.force_login(self.student)
        resp = self.client.get(
            self.reverse("content:question_review", args=[self.resource.slug])
        )
        self.assertIn(resp.status_code, (302, 403))

    def test_review_renders_for_admin(self):
        self.client.force_login(self.admin)
        resp = self.client.get(
            self.reverse("content:question_review", args=[self.resource.slug])
        )
        self.assertEqual(resp.status_code, 200)

    def test_review_renders_accordion(self):
        """La página de gestión muestra el acordeón Nivel → Modo."""
        self.client.force_login(self.admin)
        resp = self.client.get(
            self.reverse("content:question_review", args=[self.resource.slug])
        )
        self.assertContains(resp, "acc-level")
        self.assertContains(resp, "Práctica")
        self.assertContains(resp, "Evaluación")

    def test_add_question_targets_level_and_mode(self):
        """Añadir pregunta respeta el nivel y modo de la sección."""
        from apps.content.models import Question

        self.client.force_login(self.admin)
        resp = self.client.post(
            self.reverse("content:add_question_inline", args=[self.resource.id]),
            {"level": "2", "mode": "evaluacion"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(resp.status_code, 200)
        q = Question.objects.filter(resource=self.resource).latest("id")
        self.assertEqual(q.level, 2)
        self.assertEqual(q.mode, "evaluacion")
        self.assertEqual(q.status, "borrador")
        # Nace con 4 alternativas y devuelve el ítem plegable abierto.
        self.assertEqual(q.choices.count(), 4)
        self.assertContains(resp, "acc-q")

    def test_save_config_persists(self):
        self.client.force_login(self.admin)
        data = {
            "max_attempts": 3,
            "pass_threshold": 100,
            "recovery_rule": "practice_5_5",
        }
        for lvl in ("1", "2", "3"):
            data[f"practice_pool_{lvl}"] = 15
            data[f"practice_shown_{lvl}"] = 5
            data[f"eval_pool_{lvl}"] = 10
            data[f"eval_shown_{lvl}"] = 3
        resp = self.client.post(
            self.reverse("content:save_resource_quiz_config", args=[self.resource.id]),
            data,
        )
        self.assertIn(resp.status_code, (200, 302))
        config = ResourceQuizConfig.objects.get(resource=self.resource)
        self.assertEqual(config.counts["3"]["eval"]["shown"], 3)
        self.assertEqual(config.pass_threshold, 1.0)

    def test_chunk_generates_in_small_batches(self):
        """Cada tanda crea ≤5 preguntas y avanza de celda al completar el pool."""
        import json as _json

        self.client.force_login(self.admin)
        counts = {
            "1": {"practice": {"pool": 12, "shown": 5}, "eval": {"pool": 0, "shown": 0}},
            "2": {"practice": {"pool": 0, "shown": 0}, "eval": {"pool": 0, "shown": 0}},
            "3": {"practice": {"pool": 0, "shown": 0}, "eval": {"pool": 0, "shown": 0}},
        }
        base = {
            "resource_ids[]": [self.resource.id],
            "current_index": 0,
            "level": 1,
            "mode": "practice",
            "generated_total": 0,
            "autopublish": "false",
            "max_attempts": 3,
            "pass_threshold": 1.0,
            "recovery_rule": "practice_5_5",
            "allow_retake_passed": "false",
            "counts_data": _json.dumps(counts),
        }
        url = self.reverse("content:generate_questions_chunk")

        # Primer lote: offset 0 → crea 5 y se queda en la misma celda (offset 5).
        r1 = self.client.post(url, {**base, "batch_offset": 0})
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(
            Question.objects.filter(
                resource=self.resource, level=1, mode="preparacion"
            ).count(),
            5,
        )
        self.assertIn(b'name="batch_offset" value="5"', r1.content)
        self.assertIn(b'name="mode" value="practice"', r1.content)

        # Último lote de la celda: offset 10, pool 12 → crea 2 y avanza a (N1, eval).
        r2 = self.client.post(url, {**base, "batch_offset": 10, "generated_total": 10})
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(
            Question.objects.filter(
                resource=self.resource, level=1, mode="preparacion"
            ).count(),
            7,
        )
        self.assertIn(b'name="batch_offset" value="0"', r2.content)
        self.assertIn(b'name="mode" value="eval"', r2.content)

    def test_studio_post_requires_resources(self):
        self.client.force_login(self.admin)
        resp = self.client.post(self.reverse("content:question_studio"), {})
        self.assertEqual(resp.status_code, 400)

    def test_studio_post_renders_progress(self):
        """El punto de entrada de generación (usado por el botón de la página de
        gestión) devuelve el contenedor de progreso que encadena las tandas."""
        self.client.force_login(self.admin)
        data = {
            "resources": [self.resource.id],
            "max_attempts": 3,
            "pass_threshold": 100,
            "recovery_rule": "practice_5_5",
        }
        for lvl in ("1", "2", "3"):
            data[f"practice_pool_{lvl}"] = 6
            data[f"practice_shown_{lvl}"] = 5
            data[f"eval_pool_{lvl}"] = 4
            data[f"eval_shown_{lvl}"] = 3
        resp = self.client.post(self.reverse("content:question_studio"), data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'chunk-form', resp.content)
        self.assertIn(b'batch_offset', resp.content)
        # El umbral debe renderizarse en formato máquina (punto), no con coma de locale.
        self.assertIn(b'name="pass_threshold" value="1.0"', resp.content)

    def test_chunk_handles_comma_decimal_threshold(self):
        """Regresión: el umbral puede llegar con coma decimal (locale es-*) sin romper."""
        import json as _json

        self.client.force_login(self.admin)
        counts = {
            "1": {"practice": {"pool": 3, "shown": 2}, "eval": {"pool": 0, "shown": 0}},
            "2": {"practice": {"pool": 0, "shown": 0}, "eval": {"pool": 0, "shown": 0}},
            "3": {"practice": {"pool": 0, "shown": 0}, "eval": {"pool": 0, "shown": 0}},
        }
        resp = self.client.post(self.reverse("content:generate_questions_chunk"), {
            "resource_ids[]": [self.resource.id],
            "current_index": 0,
            "level": 1,
            "mode": "practice",
            "batch_offset": 0,
            "generated_total": 0,
            "autopublish": "false",
            "max_attempts": 3,
            "pass_threshold": "1,0",  # coma decimal, como lo manda el navegador en es-*
            "recovery_rule": "practice_5_5",
            "allow_retake_passed": "false",
            "counts_data": _json.dumps(counts),
        })
        self.assertEqual(resp.status_code, 200)
