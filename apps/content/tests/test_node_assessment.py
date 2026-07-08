from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command

from apps.content.models import (
    KnowledgeNode,
    NodeContent,
    NodeAssessmentQuestion,
    NodeAssessmentChoice,
    NodeAssessmentAttempt,
)
from apps.content.services.node_assessment_service import (
    get_questions_for_assessment,
    submit_assessment,
    get_node_mastery,
    get_attempts_info,
)


class NodeAssessmentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alumno@profeonline.cl", email="alumno@profeonline.cl", password="password")

        # Jerarquía para urls: Asignatura > Eje > Bloque > Tema > Recurso
        self.asignatura = KnowledgeNode.objects.create(
            name="Matemática", slug="matematica", node_type=KnowledgeNode.NODE_ASIGNATURA, semantic_id="MAT", subject_abbr="MAT", code="01"
        )
        self.eje = KnowledgeNode.objects.create(
            name="Números", slug="numeros", node_type=KnowledgeNode.NODE_EJE, parent=self.asignatura, semantic_id="MAT.NUM", subject_abbr="MAT", axis_abbr="NUM", code="01.01"
        )
        self.bloque = KnowledgeNode.objects.create(
            name="Enteros", slug="enteros", node_type=KnowledgeNode.NODE_BLOQUE, parent=self.eje, semantic_id="MAT.NUM.ENTEROS", subject_abbr="MAT", axis_abbr="NUM", code="01.01.01"
        )
        self.tema = KnowledgeNode.objects.create(
            name="Conjunto", slug="conjunto", node_type=KnowledgeNode.NODE_TEMA, parent=self.bloque, semantic_id="MAT.NUM.ENTEROS_CONJUNTO", subject_abbr="MAT", axis_abbr="NUM", code="01.01.01.01"
        )
        self.node = KnowledgeNode.objects.create(
            name="Naturales", slug="naturales", node_type=KnowledgeNode.NODE_RECURSO, parent=self.tema, semantic_id="MAT.NUM.ENTEROS_CONJUNTO.NATURALES", subject_abbr="MAT", axis_abbr="NUM", is_published=True, code="01.01.01.01.01"
        )

        self.content = NodeContent.objects.create(
            node=self.node,
            objetivo="Comprender los números naturales.",
            estado=NodeContent.ESTADO_PUBLICADO
        )

    def _create_question(self, level=1, status="publicada", text="Pregunta de prueba"):
        q = NodeAssessmentQuestion.objects.create(
            node=self.node,
            level=level,
            text=text,
            status=status
        )
        c1 = NodeAssessmentChoice.objects.create(question=q, text="A", is_correct=True)
        c2 = NodeAssessmentChoice.objects.create(question=q, text="B", is_correct=False)
        return q, c1, c2

    def test_get_questions_for_assessment(self):
        # Crear 10 preguntas
        for i in range(10):
            self._create_question(level=1, text=f"Pregunta {i}")

        questions = get_questions_for_assessment(self.node, 1)
        self.assertEqual(len(questions), 7)  # Debe traer max 7

    def test_submit_assessment_passing(self):
        questions_dict = {}
        for i in range(7):
            q, c1, c2 = self._create_question(level=1, text=f"P {i}")
            # 6 correctas (85.7% >= 80% aprueba)
            if i < 6:
                questions_dict[q.pk] = c1.pk
            else:
                questions_dict[q.pk] = c2.pk

        attempt = submit_assessment(self.user, self.node, 1, questions_dict)
        self.assertTrue(attempt.passed)
        self.assertEqual(attempt.score, 6)
        self.assertEqual(attempt.total, 7)
        self.assertEqual(attempt.attempt_number, 1)

    def test_submit_assessment_failing(self):
        questions_dict = {}
        for i in range(7):
            q, c1, c2 = self._create_question(level=1, text=f"P {i}")
            # 3 correctas (42.8% reprobado)
            if i < 3:
                questions_dict[q.pk] = c1.pk
            else:
                questions_dict[q.pk] = c2.pk

        attempt = submit_assessment(self.user, self.node, 1, questions_dict)
        self.assertFalse(attempt.passed)

    def test_max_attempts_blocked(self):
        # Generar 3 intentos fallidos
        q, c1, c2 = self._create_question(level=1)
        for i in range(3):
            submit_assessment(self.user, self.node, 1, {q.pk: c2.pk})

        info = get_attempts_info(self.user, self.node, 1)
        self.assertTrue(info["max_reached"])
        self.assertEqual(info["remaining"], 0)

        # Intentar un cuarto intento debe lanzar ValueError
        with self.assertRaises(ValueError):
            submit_assessment(self.user, self.node, 1, {q.pk: c1.pk})

    def test_mastery_stars(self):
        q, c1, c2 = self._create_question(level=1)
        # Nivel 1 aprobado
        submit_assessment(self.user, self.node, 1, {q.pk: c1.pk})

        q2, c1_2, c2_2 = self._create_question(level=2)
        # Nivel 2 aprobado
        submit_assessment(self.user, self.node, 2, {q2.pk: c1_2.pk})

        # Nivel 3 no intentado
        mastery = get_node_mastery(self.user, self.node)
        self.assertEqual(mastery["stars"], 2)

    def test_generate_command_dry_run(self):
        # Probar el comando de Django en dry-run
        call_command("generate_node_assessment_questions", node=self.node.semantic_id, dry_run=True)
        # No debe haber creado ninguna pregunta física
        self.assertEqual(NodeAssessmentQuestion.objects.filter(node=self.node).count(), 0)

    def test_generate_command_execution(self):
        # Ejecutar generación real (mock)
        call_command("generate_node_assessment_questions", node=self.node.semantic_id)
        # Debe haber creado 7 preguntas por cada nivel (21 total)
        self.assertEqual(NodeAssessmentQuestion.objects.filter(node=self.node).count(), 21)

        # Idempotencia: volver a ejecutar no debe duplicar preguntas
        call_command("generate_node_assessment_questions", node=self.node.semantic_id)
        self.assertEqual(NodeAssessmentQuestion.objects.filter(node=self.node).count(), 21)

    def test_views_flow(self):
        self.client.force_login(self.user)

        # Generar las preguntas con el comando
        call_command("generate_node_assessment_questions", node=self.node.semantic_id, publish=True)

        url_params = [
            self.asignatura.slug,
            self.eje.slug,
            self.bloque.slug,
            self.tema.slug,
            self.node.slug,
        ]

        # 1. GET Start Form
        start_url = reverse("learn:assessment_start", args=url_params + [1])
        response = self.client.get(start_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Evaluación · Nivel 1")

        # 2. POST Submit answers
        submit_url = reverse("learn:assessment_submit", args=url_params + [1])
        # Construir post payload en base al formulario (pasamos respuestas simuladas vacías)
        payload = {}
        session_key = f"node_assessment_{self.node.pk}_1"
        session = self.client.session
        # Simular que renderizó las preguntas guardadas en la sesión
        questions = NodeAssessmentQuestion.objects.filter(node=self.node, level=1)
        session[session_key] = [q.pk for q in questions]
        session.save()

        # Enviar el submit
        response = self.client.post(submit_url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Intento No Aprobado")  # Al estar vacías, reprueba

        # 3. GET Status panel
        status_url = reverse("learn:assessment_status", args=url_params)
        response = self.client.get(status_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Estrellas de dominio")
