import random
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from apps.content.models import (
    Subject,
    Topic,
    Resource,
    ExerciseItem,
    ResourceExerciseItem,
    Question,
    Choice,
    LearningGuide,
    QuizAttempt,
)
from apps.content.selectors.evaluation_selectors import get_question_availability_map
from apps.content.services.evaluation_service import (
    get_questions_for_quiz,
    _topic_exam_question_qs,
)
from apps.content.services.visible_bank_service import (
    generate_visible_bank_questions,
    select_visible_practice_questions,
)
from apps.content.services.progress_service import get_resource_progress

User = get_user_model()


class VisibleBankTests(TestCase):
    def setUp(self):
        # 1. Crear estructura curricular
        self.subject = Subject.objects.create(name="Matemática Media", education_level="media")
        self.topic = Topic.objects.create(name="Álgebra", subject=self.subject, structured_bank_enabled=True)

        self.resource = Resource.objects.create(
            title="Video Ecuaciones",
            subject=self.subject,
            topic=self.topic,
            is_published=True
        )

        # 2. Ítem de aprendizaje aprobado y vínculo
        self.item = ExerciseItem.objects.create(
            topic=self.topic,
            title="Resolución de Ecuaciones",
            level=1,
            objective="Resolver ecuaciones lineales sencillas.",
            status="aprobado",
            detected_exercise_count=5
        )
        self.link = ResourceExerciseItem.objects.create(
            exercise_item=self.item,
            resource=self.resource,
            practice_quota=6
        )

        # 3. Guía ProfeOnline publicada y pública
        self.guide = LearningGuide.objects.create(
            topic=self.topic,
            title="Guía Oficial de Álgebra",
            structured_content={
                "introduction": "Intro a las ecuaciones.",
                "summary": "Teoría resumida.",
                "formulas": ["x + a = b => x = b - a"],
                "solved_examples": [{"question": "x + 2 = 5", "explanation": "x = 3"}],
            },
            status="publicada",
            visibility="publica"
        )

        # 4. Usuarios
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@profeonline.cl", password="password"
        )
        self.student = User.objects.create_user(
            username="student", email="student@profeonline.cl", password="password"
        )

        self.client = Client()

    def test_generate_visible_bank_questions_success(self):
        """Verifica que generate_visible_bank_questions genera preguntas borrador con los campos correctos."""
        questions = generate_visible_bank_questions(
            exercise_item=self.item,
            resource=self.resource,
            learning_guide=self.guide,
            count=2
        )
        self.assertEqual(len(questions), 2)

        for q in questions:
            self.assertEqual(q.status, "borrador")
            self.assertEqual(q.scope, "banco_visible")
            self.assertEqual(q.question_type, "alternativa")
            self.assertEqual(q.level, self.item.level)
            self.assertEqual(q.exercise_item, self.item)
            self.assertEqual(q.learning_guide, self.guide)
            self.assertTrue(q.hint)
            self.assertTrue(q.canonical_answer)
            self.assertEqual(q.choices.count(), 4)
            # Debe haber una única alternativa marcada como correcta
            self.assertEqual(q.choices.filter(is_correct=True).count(), 1)

        # Sincronización guide.resources
        self.assertIn(self.resource, self.guide.resources.all())

    @patch(
        "apps.content.services.ai_generation_service.generate_question_candidates"
    )
    def test_generation_never_uses_network_during_tests(self, generate_candidates):
        questions = generate_visible_bank_questions(
            exercise_item=self.item,
            resource=self.resource,
            learning_guide=self.guide,
            count=1,
            api_key="test-key-that-must-not-be-used",
        )
        self.assertEqual(len(questions), 1)
        generate_candidates.assert_not_called()

    def test_generate_visible_bank_questions_preconditions(self):
        """Verifica el rechazo defensivo ante precondiciones insatisfechas."""
        # 1. Tema inactivo
        self.topic.is_active = False
        self.topic.save()
        with self.assertRaises(ValueError):
            generate_visible_bank_questions(exercise_item=self.item, resource=self.resource, learning_guide=self.guide)
        self.topic.is_active = True
        self.topic.save()

        # 2. Banco estructurado desactivado por tema
        self.topic.structured_bank_enabled = False
        self.topic.save()
        with self.assertRaises(ValueError):
            generate_visible_bank_questions(exercise_item=self.item, resource=self.resource, learning_guide=self.guide)
        self.topic.structured_bank_enabled = True
        self.topic.save()

        # 3. Ítem no aprobado
        self.item.status = "propuesto"
        self.item.save()
        with self.assertRaises(ValueError):
            generate_visible_bank_questions(exercise_item=self.item, resource=self.resource, learning_guide=self.guide)
        self.item.status = "aprobado"
        self.item.save()

        # 4. Guía no pública/publicada
        self.guide.status = "borrador"
        self.guide.save()
        with self.assertRaises(ValueError):
            generate_visible_bank_questions(exercise_item=self.item, resource=self.resource, learning_guide=self.guide)

    def test_deficit_quota_calculation(self):
        """Verifica que el generador calcula correctamente el déficit contra borrador + publicadas (no archivadas)."""
        # Crear 1 borrador, 1 publicada, 1 archivada
        # Borrador
        q1 = Question.objects.create(
            resource=self.resource, level=self.item.level, status="borrador",
            exercise_item=self.item, scope="banco_visible", learning_guide=self.guide
        )
        # Publicada
        q2 = Question.objects.create(
            resource=self.resource, level=self.item.level, status="publicada",
            exercise_item=self.item, scope="banco_visible", learning_guide=self.guide
        )
        # Archivada
        q3 = Question.objects.create(
            resource=self.resource, level=self.item.level, status="archivada",
            exercise_item=self.item, scope="banco_visible", learning_guide=self.guide
        )

        # Cuota de práctica: 6 (link.practice_quota)
        # Activas (borrador + publicada): 2
        # Déficit esperado: 6 - 2 = 4
        questions = generate_visible_bank_questions(
            exercise_item=self.item,
            resource=self.resource,
            learning_guide=self.guide,
            count=None # Fuerza cálculo de déficit
        )
        self.assertEqual(len(questions), 4)

    def test_legacy_isolation(self):
        """Verifica que las preguntas del banco visible están aisladas del sistema legacy."""
        # Crear pregunta estructurada
        q_visible = Question.objects.create(
            resource=self.resource, level=1, status="publicada", mode="preparacion",
            exercise_item=self.item, scope="banco_visible", learning_guide=self.guide
        )
        Choice.objects.create(question=q_visible, text="Correcta", is_correct=True, order=1)

        # Crear pregunta legacy
        q_legacy = Question.objects.create(
            resource=self.resource, level=1, status="publicada", mode="ambas",
            scope=""
        )
        Choice.objects.create(question=q_legacy, text="Correcta", is_correct=True, order=1)

        # 1. Availability map solo ve legacy (scope="")
        avail = get_question_availability_map([self.resource.id])
        # Solo debe haber disponibilidad para la pregunta legacy, no la visible
        self.assertTrue(avail[self.resource.id][1]["practice"])

        # 2. Quiz generator solo retorna la legacy (scope="")
        quiz_qs = get_questions_for_quiz(self.resource, level=1, mode="preparacion")
        self.assertEqual(len(quiz_qs), 1)
        self.assertEqual(quiz_qs[0].id, q_legacy.id)

        # 3. Final exam del tema solo retorna la legacy
        exam_qs = _topic_exam_question_qs(self.topic)
        self.assertEqual(exam_qs.count(), 1)
        self.assertEqual(exam_qs[0].id, q_legacy.id)

    def test_select_visible_practice_questions_mixed(self):
        """Verifica la selección round-robin mixta y equilibrada."""
        # Crear un segundo ítem
        item2 = ExerciseItem.objects.create(
            topic=self.topic, title="Ítem 2", level=2, status="aprobado"
        )

        # Generar preguntas para ambos ítems
        # Ítem 1 (Resolución de Ecuaciones)
        for i in range(3):
            q = Question.objects.create(
                resource=self.resource, level=1, status="publicada", scope="banco_visible",
                exercise_item=self.item, learning_guide=self.guide, difficulty="basica", order=i
            )
            Choice.objects.create(question=q, text="A", is_correct=True)

        # Ítem 2
        for i in range(3):
            q = Question.objects.create(
                resource=self.resource, level=2, status="publicada", scope="banco_visible",
                exercise_item=item2, learning_guide=self.guide, difficulty="intermedia", order=i
            )
            Choice.objects.create(question=q, text="A", is_correct=True)

        # Seleccionar práctica mixta equilibrada
        selected = select_visible_practice_questions(topic=self.topic, count=4)
        self.assertEqual(len(selected), 4)

        # Al equilibrar con round-robin, deberíamos tener 2 de cada ítem/dificultad
        item_counts = {self.item.id: 0, item2.id: 0}
        for q in selected:
            item_counts[q.exercise_item_id] += 1

        self.assertEqual(item_counts[self.item.id], 2)
        self.assertEqual(item_counts[item2.id], 2)

    def test_learning_guide_detail_view_permissions(self):
        """Verifica que el detalle de la guía requiere autenticación y retorna 404 si no es pública."""
        url = reverse("content:learning_guide_detail", args=[self.guide.slug])

        # Anónimo -> Redirección a login
        response = self.client.get(url)
        self.assertRedirects(response, f"/cuentas/login/?next={url}")

        # Autenticado -> OK
        self.client.login(username="student", password="password")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/learning_guide_detail.html")

        # Guía en borrador -> 404
        self.guide.status = "borrador"
        self.guide.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_and_resource_detail_view_guide_context(self):
        """Verifica la carga del contexto de la guía en vistas del alumno."""
        self.client.login(username="student", password="password")

        # 1. Tema con estructurado habilitado -> contiene la guía
        topic_url = reverse("content:topic_detail", args=[self.topic.slug])
        response = self.client.get(topic_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["learning_guide"], self.guide)

        # 2. Recurso vinculado -> contiene la guía
        self.guide.resources.add(self.resource)
        resource_url = reverse("content:resource_detail", args=[self.resource.slug])
        response = self.client.get(resource_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["learning_guide"], self.guide)

        # 3. Recurso desvinculado -> guía es None
        self.guide.resources.remove(self.resource)
        response = self.client.get(resource_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context.get("learning_guide"))

    def test_practice_session_lifecycle_and_validation(self):
        """Verifica el flujo completo de inicio y envío de práctica con validación estricta de IDs."""
        # Generar preguntas publicadas
        q1 = Question.objects.create(
            resource=self.resource, level=1, status="publicada", scope="banco_visible",
            exercise_item=self.item, learning_guide=self.guide, difficulty="basica"
        )
        c1 = Choice.objects.create(question=q1, text="Correcta", is_correct=True)
        Choice.objects.create(question=q1, text="Incorrecta A", is_correct=False)

        q2 = Question.objects.create(
            resource=self.resource, level=1, status="publicada", scope="banco_visible",
            exercise_item=self.item, learning_guide=self.guide, difficulty="intermedia"
        )
        Choice.objects.create(question=q2, text="Correcta B", is_correct=True)
        c2_inc = Choice.objects.create(question=q2, text="Incorrecta B", is_correct=False)

        self.client.login(username="student", password="password")

        # 1. Iniciar Práctica (POST htmx)
        progress_before = get_resource_progress(self.student, self.resource)
        start_url = reverse("content:start_visible_practice", args=[self.topic.id])
        response = self.client.post(start_url, {"count": 2})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "partials/_practice_quiz_player.html")

        # Verificar guardado en sesión
        session_key = f"visible_practice_{self.student.id}_{self.topic.id}"
        self.assertIn(session_key, self.client.session)
        session_data = self.client.session[session_key]
        self.assertEqual(len(session_data["question_ids"]), 2)

        # 2. Envío de práctica válido
        submit_url = reverse("content:submit_visible_practice", args=[self.topic.id])
        post_data = {
            f"question_{q1.id}": c1.id,
            f"question_{q2.id}": c2_inc.id,
        }
        response = self.client.post(submit_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "partials/_practice_quiz_player.html")

        # Validar resultados en contexto
        self.assertEqual(response.context["score"], 1)
        self.assertEqual(response.context["total"], 2)
        self.assertEqual(response.context["percentage"], 50)

        # Verificar que la sesión fue eliminada al terminar
        self.assertNotIn(session_key, self.client.session)

        # Verificar que no se creó ningún QuizAttempt
        self.assertEqual(QuizAttempt.objects.count(), 0)
        self.assertEqual(
            get_resource_progress(self.student, self.resource),
            progress_before,
        )

    def test_practice_session_manipulation_rejection(self):
        """Verifica que el envío de alternativas o IDs manipulados es rechazado con HTTP 400."""
        q1 = Question.objects.create(
            resource=self.resource, level=1, status="publicada", scope="banco_visible",
            exercise_item=self.item, learning_guide=self.guide, difficulty="basica"
        )
        c1 = Choice.objects.create(question=q1, text="Correcta", is_correct=True)

        # Pregunta ajena (no está en la sesión)
        q_other = Question.objects.create(
            resource=self.resource, level=1, status="publicada", scope="banco_visible",
            exercise_item=self.item, learning_guide=self.guide, difficulty="basica"
        )
        c_other = Choice.objects.create(question=q_other, text="Ajena Correcta", is_correct=True)

        self.client.login(username="student", password="password")

        # Iniciar sesión
        start_url = reverse("content:start_visible_practice", args=[self.topic.id])
        self.client.post(start_url, {"count": 1})

        # Envío con pregunta ajena manipulada -> HTTP 400
        submit_url = reverse("content:submit_visible_practice", args=[self.topic.id])
        bad_post_data = {
            f"question_{q1.id}": c1.id,
            f"question_{q_other.id}": c_other.id, # No está en la sesión de práctica
        }
        response = self.client.post(submit_url, bad_post_data)
        self.assertEqual(response.status_code, 400)

        # Alternativa de otra pregunta
        bad_post_data_2 = {
            f"question_{q1.id}": c_other.id, # c_other pertenece a q_other, no a q1
        }
        response = self.client.post(submit_url, bad_post_data_2)
        self.assertEqual(response.status_code, 400)

    def test_admin_bulk_actions_validation(self):
        """Verifica que las acciones masivas de administración validan estrictamente pertenencia y devuelven 400 en discrepancias."""
        # Generar preguntas
        q1 = Question.objects.create(
            resource=self.resource, level=1, status="borrador", scope="banco_visible",
            exercise_item=self.item, learning_guide=self.guide,
            text="¿Cuánto vale x en x + 1 = 2?",
            explanation="Se resta 1 a ambos lados.",
            difficulty="basica",
            hint="Aísla x.",
            canonical_answer="1",
        )
        Choice.objects.create(question=q1, text="1", is_correct=True, order=1)
        Choice.objects.create(question=q1, text="2", is_correct=False, order=2)
        Choice.objects.create(question=q1, text="3", is_correct=False, order=3)
        Choice.objects.create(question=q1, text="4", is_correct=False, order=4)

        topic_other = Topic.objects.create(name="Física", subject=self.subject, structured_bank_enabled=True)
        item_other = ExerciseItem.objects.create(topic=topic_other, title="Cinemática", level=1, status="aprobado")
        q_other = Question.objects.create(
            resource=self.resource, level=1, status="borrador", scope="banco_visible",
            exercise_item=item_other, learning_guide=self.guide
        )

        self.client.login(username="admin", password="password")

        bulk_url = reverse("content:bulk_action_questions", args=[self.resource.id])

        # Intento de acción masiva incluyendo la pregunta ajena -> Debe fallar con HTTP 400
        bad_post = {
            "action": "publicar",
            "scope": "banco_visible",
            "exercise_item_id": self.item.id,
            "learning_guide_id": self.guide.id,
            "selected_questions": [q1.id, q_other.id],
        }
        response = self.client.post(bulk_url, bad_post)
        self.assertEqual(response.status_code, 400)
        self.assertIn("no pertenecen al recurso, guía, ítem o scope esperados", response.content.decode("utf-8"))

        # Intento de acción masiva con IDs correctos -> Debe funcionar (HTTP 200)
        good_post = {
            "action": "publicar",
            "scope": "banco_visible",
            "exercise_item_id": self.item.id,
            "learning_guide_id": self.guide.id,
            "selected_questions": [q1.id],
        }
        response = self.client.post(bulk_url, good_post, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        q1.refresh_from_db()
        self.assertEqual(q1.status, "publicada")

    def test_visible_question_cannot_publish_incomplete_and_delete_archives(self):
        question = Question.objects.create(
            resource=self.resource,
            level=1,
            status="borrador",
            scope="banco_visible",
            exercise_item=self.item,
            learning_guide=self.guide,
            text="Pregunta incompleta",
        )
        self.client.force_login(self.admin_user)
        bulk_url = reverse("content:bulk_action_questions", args=[self.resource.id])
        response = self.client.post(
            bulk_url,
            {
                "action": "publicar",
                "scope": "banco_visible",
                "exercise_item_id": self.item.id,
                "learning_guide_id": self.guide.id,
                "selected_questions": [question.id],
            },
        )
        self.assertEqual(response.status_code, 400)
        question.refresh_from_db()
        self.assertEqual(question.status, "borrador")

        response = self.client.post(
            reverse("content:delete_question", args=[question.id])
        )
        self.assertEqual(response.status_code, 200)
        question.refresh_from_db()
        self.assertEqual(question.status, "archivada")

    def test_submit_revalidates_question_visibility(self):
        question = Question.objects.create(
            resource=self.resource,
            level=1,
            status="publicada",
            scope="banco_visible",
            exercise_item=self.item,
            learning_guide=self.guide,
            difficulty="basica",
        )
        choice = Choice.objects.create(
            question=question, text="Correcta", is_correct=True
        )
        self.client.force_login(self.student)
        self.client.post(
            reverse("content:start_visible_practice", args=[self.topic.id]),
            {"count": 1},
        )
        question.status = "archivada"
        question.save(update_fields=["status"])
        response = self.client.post(
            reverse("content:submit_visible_practice", args=[self.topic.id]),
            {f"question_{question.id}": choice.id},
        )
        self.assertEqual(response.status_code, 400)
