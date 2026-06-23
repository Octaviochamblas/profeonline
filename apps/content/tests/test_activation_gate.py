from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import (
    Choice,
    ExerciseItem,
    LearningGuide,
    Question,
    Resource,
    ResourceExerciseItem,
    Subject,
    Topic,
)
from apps.content.models.topic_bank_config import TopicBankConfig
from apps.content.services.activation_gate_service import evaluate_topic_gate

User = get_user_model()


class ActivationGateTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="f7-admin", email="a@b.cl", password="x"
        )
        self.subject = Subject.objects.create(name="F7 Matemática")
        # Tema en preparación (staging): editable por admin, oculto a alumnos.
        self.topic = Topic.objects.create(
            name="F7 Álgebra",
            subject=self.subject,
            structured_bank_enabled=False,
            structured_bank_staging=True,
        )
        self.config = TopicBankConfig.objects.create(
            topic=self.topic,
            level_eval_minutes=10,
            level_eval_attempts=1,
            final_minutes=5,
            final_attempts=1,
            # Distribución 100% N1: satisfacible con datos de un solo nivel.
            final_distribution={"conceptual": 100, "mecanico": 0, "aplicacion": 0},
            duration_tolerance_pct=100,
        )
        self.resource = Resource.objects.create(
            title="F7 Recurso",
            subject=self.subject,
            topic=self.topic,
            is_published=True,
        )
        self.item = ExerciseItem.objects.create(
            topic=self.topic,
            title="F7 Ítem",
            level=1,
            objective="Resolver",
            status="aprobado",
            detected_exercise_count=0,
        )
        self.link = ResourceExerciseItem.objects.create(
            exercise_item=self.item,
            resource=self.resource,
            practice_quota=1,
            evaluation_quota=1,
        )
        self.guide = LearningGuide.objects.create(
            topic=self.topic,
            title="F7 Guía",
            status="publicada",
            visibility="publica",
        )
        self._make_question(scope="banco_visible")
        self._make_question(scope="evaluacion_nivel")
        self._make_question(scope="prueba_final")
        self.client.force_login(self.admin)

    def _make_question(self, *, scope):
        question = Question.objects.create(
            resource=self.resource,
            exercise_item=self.item,
            learning_guide=self.guide,
            level=1,
            mode="evaluacion" if scope != "banco_visible" else "preparacion",
            text=f"Pregunta {scope}",
            explanation="Explicación",
            hint="Pista",
            difficulty="intermedia",
            question_type="alternativa",
            canonical_answer="Correcta",
            points=1,
            estimated_minutes=2,
            scope=scope,
            status="publicada",
        )
        Choice.objects.create(question=question, text="Correcta", is_correct=True, order=1)
        Choice.objects.create(question=question, text="Mala", is_correct=False, order=2)
        return question

    # --- Gate (servicio) -------------------------------------------------

    def test_gate_passes_when_topic_is_complete(self):
        gate = evaluate_topic_gate(self.topic, user=self.admin)
        self.assertTrue(gate["ok"], [c for c in gate["checks"] if not c.ok])

    def test_gate_blocks_when_item_not_approved(self):
        self.item.status = "propuesto"
        self.item.save(update_fields=["status"])
        gate = evaluate_topic_gate(self.topic, user=self.admin)
        self.assertFalse(gate["ok"])
        failed = {c.key for c in gate["checks"] if not c.ok}
        self.assertIn("items_aprobados", failed)

    def test_gate_blocks_without_public_guide(self):
        self.guide.delete()
        gate = evaluate_topic_gate(self.topic, user=self.admin)
        self.assertFalse(gate["ok"])
        self.assertIn(
            "guia_publica", {c.key for c in gate["checks"] if not c.ok}
        )

    def test_gate_blocks_when_visible_bank_incomplete(self):
        Question.objects.filter(scope="banco_visible").delete()
        gate = evaluate_topic_gate(self.topic, user=self.admin)
        self.assertFalse(gate["ok"])
        self.assertIn(
            "banco_visible_completo", {c.key for c in gate["checks"] if not c.ok}
        )

    def test_gate_blocks_when_evaluation_reserve_insufficient(self):
        # Pide 3 intentos de nivel pero solo hay 1 pregunta publicada.
        self.config.level_eval_attempts = 3
        self.config.save(update_fields=["level_eval_attempts"])
        gate = evaluate_topic_gate(self.topic, user=self.admin)
        self.assertFalse(gate["ok"])
        self.assertIn(
            "reserva_nivel", {c.key for c in gate["checks"] if not c.ok}
        )

    # --- Activación (vistas) --------------------------------------------

    def test_activate_flips_flag_when_gate_passes(self):
        response = self.client.post(
            reverse("content:activate_structured_bank"),
            {"topic_id": self.topic.id},
        )
        self.assertEqual(response.status_code, 200)
        self.topic.refresh_from_db()
        self.assertTrue(self.topic.structured_bank_enabled)
        self.assertFalse(self.topic.structured_bank_staging)

    def test_activate_refused_when_gate_fails(self):
        self.guide.delete()
        response = self.client.post(
            reverse("content:activate_structured_bank"),
            {"topic_id": self.topic.id},
        )
        self.assertEqual(response.status_code, 400)
        self.topic.refresh_from_db()
        self.assertFalse(self.topic.structured_bank_enabled)

    def test_deactivate_rolls_back_to_legacy(self):
        self.topic.structured_bank_enabled = True
        self.topic.structured_bank_staging = False
        self.topic.save(
            update_fields=["structured_bank_enabled", "structured_bank_staging"]
        )
        response = self.client.post(
            reverse("content:deactivate_structured_bank"),
            {"topic_id": self.topic.id},
        )
        self.assertEqual(response.status_code, 200)
        self.topic.refresh_from_db()
        self.assertFalse(self.topic.structured_bank_enabled)
        self.assertTrue(self.topic.structured_bank_staging)

    def test_staging_enables_admin_panel_but_hides_from_students(self):
        # Admin: el tema en staging aparece en el panel de ítems.
        admin_panel = self.client.get(reverse("content:item_extraction"))
        self.assertContains(admin_panel, "F7 Álgebra")
        # Alumno: la guía pública del tema en staging NO es accesible.
        student = User.objects.create_user(username="f7-student", password="x")
        self.client.force_login(student)
        detail = self.client.get(
            reverse("content:learning_guide_detail", args=[self.guide.slug])
        )
        self.assertEqual(detail.status_code, 404)
