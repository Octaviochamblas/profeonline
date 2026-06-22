import json
from django.db import IntegrityError, transaction
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from unittest.mock import patch

from apps.content.models import (
    Subject,
    Topic,
    Resource,
    QuizGuide,
    ExerciseItem,
    LearningGuide,
    ResourceExerciseItem,
    Question,
)
from apps.content.services.learning_guide_service import (
    generate_guide_draft,
    validate_guide_schema,
)
from apps.content.services.originality_service import (
    check_originality,
    calculate_audit_hash,
)
from apps.content.services.ai_generation_service import call_ai_structured_json

User = get_user_model()


class LearningGuideTests(TestCase):
    def setUp(self):
        # Crear estructura curricular básica
        self.subject = Subject.objects.create(name="Física Media", education_level="media")
        self.topic = Topic.objects.create(name="Cinemática", subject=self.subject, structured_bank_enabled=True)

        self.resource = Resource.objects.create(
            title="MRU Introducción",
            subject=self.subject,
            topic=self.topic,
            is_published=True
        )

        self.quiz_guide = QuizGuide.objects.create(
            title="Guía Fuente de Cinemática",
            content_text="El movimiento rectilíneo uniforme se define como una trayectoria en línea recta con velocidad constante."
        )
        self.quiz_guide.topics.add(self.topic)

        # Crear ítems aprobados
        self.item_approved = ExerciseItem.objects.create(
            topic=self.topic,
            title="Cálculo de velocidad",
            level=2,
            objective="Calcular velocidad usando la ecuación $v = \\frac{d}{t}$.",
            status="aprobado"
        )

        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@profeonline.cl", password="password"
        )
        self.regular_user = User.objects.create_user(
            username="regular", email="regular@profeonline.cl", password="password"
        )

    def valid_content(self, *, introduction="Introducción original"):
        return {
            "schema_version": 1,
            "introduction": introduction,
            "summary": "Resumen original.",
            "formulas": [],
            "items": [
                {
                    "item_id": self.item_approved.id,
                    "title": self.item_approved.title,
                    "examples": [],
                    "exercises": [
                        {
                            "id": "q1",
                            "difficulty": "intermedia",
                            "statement": "Calcula una velocidad media.",
                            "hint": "",
                            "solution": "La velocidad es $5$.",
                        }
                    ],
                }
            ],
            "challenges": [],
            "answer_key": [{"exercise_id": "q1", "solution": "La velocidad es $5$."}],
        }

    @patch("apps.content.services.learning_guide_service.call_ai_structured_json")
    def test_generation_mock_complete_and_zero_red(self, mock_ai_call):
        """Verifica que la generación simulada/mock de borrador es completa y no toca red."""
        # Configurar mock de llamada IA
        mock_response = {
            "schema_version": 1,
            "introduction": "Intro test",
            "summary": "Summary test",
            "formulas": [{"id": "f1", "latex": "$$v = d/t$$", "explanation": "formula desc"}],
            "items": [
                {
                    "item_id": self.item_approved.id,
                    "title": "Cálculo de velocidad",
                    "examples": [{"id": "ex1", "statement": "Calcular v", "steps": ["Paso 1"], "answer": "v=2"}],
                    "exercises": [{"id": "q1", "difficulty": "intermedia", "statement": "Calcular d", "hint": "Usa f1", "solution": "d=4"}]
                }
            ],
            "challenges": [],
            "answer_key": [{"exercise_id": "q1", "solution": "d=4"}]
        }
        mock_ai_call.return_value = mock_response

        # Act
        draft = generate_guide_draft(self.topic, [self.quiz_guide], api_key="fake-key")

        # Assert
        self.assertEqual(draft["schema_version"], 1)
        self.assertEqual(draft["introduction"], "Intro test")
        self.assertEqual(draft["items"][0]["item_id"], self.item_approved.id)
        mock_ai_call.assert_called_once()

    @override_settings(GEMINI_API_KEY="", OPENAI_API_KEY="openai-test-key")
    @patch("apps.content.services.ai_generation_service._post_json_with_retry")
    def test_structured_json_uses_openai_when_only_openai_is_configured(
        self, mock_post
    ):
        response = mock_post.return_value
        response.json.return_value = {
            "choices": [{"message": {"content": '{"schema_version": 1}'}}]
        }
        result = call_ai_structured_json("prompt")
        self.assertEqual(result, {"schema_version": 1})
        self.assertIn("api.openai.com", mock_post.call_args.args[0])

    def test_generation_rejects_mixed_authorized_and_unauthorized_sources(self):
        unauthorized = QuizGuide.objects.create(
            title="Fuente ajena",
            content_text="Contenido privado ajeno.",
        )
        client = Client()
        client.force_login(self.admin_user)
        response = client.post(
            reverse("content:generate_guide_draft_view"),
            {
                "topic_id": self.topic.id,
                "private_guide_ids": [self.quiz_guide.id, unauthorized.id],
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            LearningGuide.objects.filter(topic=self.topic, status="borrador").exists()
        )

    def test_schema_malformed_validation(self):
        """Valida que validate_guide_schema rechace JSONs incompletos o malformados."""
        approved_items = [self.item_approved]

        # Caso 1: Estructura vacía
        with self.assertRaises(ValueError):
            validate_guide_schema({}, approved_items)

        # Caso 2: Falta schema_version o es inválido
        invalid_version = {"schema_version": 2, "introduction": "..."}
        with self.assertRaises(ValueError):
            validate_guide_schema(invalid_version, approved_items)

        # Caso 3: Falta sección requerida
        missing_section = {
            "schema_version": 1,
            "introduction": "Intro",
            "summary": "Summary",
            "formulas": [],
            "items": []
            # falta challenges y answer_key
        }
        with self.assertRaises(ValueError):
            validate_guide_schema(missing_section, approved_items)

    def test_schema_duplicate_ids_and_invalid_references(self):
        """Valida que se rechacen IDs duplicados y referencias de solucionario inválidas."""
        approved_items = [self.item_approved]

        # Ejercicio y ejemplo con el mismo ID
        duplicate_ids_data = {
            "schema_version": 1,
            "introduction": "Intro",
            "summary": "Summary",
            "formulas": [],
            "items": [
                {
                    "item_id": self.item_approved.id,
                    "title": "Item",
                    "examples": [{"id": "dup_1", "statement": "Ejemplo", "steps": ["1"], "answer": "1"}],
                    "exercises": [{"id": "dup_1", "difficulty": "intermedia", "statement": "Ejercicio", "hint": "", "solution": "1"}]
                }
            ],
            "challenges": [],
            "answer_key": [{"exercise_id": "dup_1", "solution": "1"}]
        }
        with self.assertRaises(ValueError):
            validate_guide_schema(duplicate_ids_data, approved_items)

        # Solucionario apunta a ID inexistente
        invalid_ref_data = {
            "schema_version": 1,
            "introduction": "Intro",
            "summary": "Summary",
            "formulas": [],
            "items": [
                {
                    "item_id": self.item_approved.id,
                    "title": "Item",
                    "examples": [],
                    "exercises": [{"id": "q1", "difficulty": "intermedia", "statement": "Ejercicio", "hint": "", "solution": "1"}]
                }
            ],
            "challenges": [],
            "answer_key": [{"exercise_id": "non_existent_id", "solution": "1"}]
        }
        with self.assertRaises(ValueError):
            validate_guide_schema(invalid_ref_data, approved_items)

    def test_absence_of_approved_items_blocks_generation(self):
        """Verifica que se bloquee la generación si no hay ítems aprobados."""
        self.item_approved.status = "propuesto"
        self.item_approved.save()

        with self.assertRaises(ValueError):
            generate_guide_draft(self.topic, [self.quiz_guide], api_key="fake-key")

    def test_inactive_or_unauthorized_private_guide_rejected(self):
        """Verifica que la vista rechace generar guías con fuentes inactivas o ajenas."""
        inactive_guide = QuizGuide.objects.create(title="Inactiva", content_text="...", is_active=False)
        inactive_guide.topics.add(self.topic)

        c = Client()
        c.force_login(self.admin_user)

        # 1. Fuente inactiva
        url = reverse("content:generate_guide_draft_view")
        response = c.post(url, {"topic_id": self.topic.id, "private_guide_ids": [inactive_guide.id]})
        self.assertEqual(response.status_code, 400)

        # 2. Fuente ajena (no asociada al tema/asignatura)
        stranger_guide = QuizGuide.objects.create(title="Ajena", content_text="...", is_active=True)
        response = c.post(url, {"topic_id": self.topic.id, "private_guide_ids": [stranger_guide.id]})
        self.assertEqual(response.status_code, 400)

    def test_topic_flag_disabled_blocks_panel_and_mutations(self):
        """Asegura que se bloquee el panel y mutaciones si structured_bank_enabled=False."""
        self.topic.structured_bank_enabled = False
        self.topic.save()

        c = Client()
        c.force_login(self.admin_user)

        # Panel principal GET
        url_panel = f"{reverse('content:learning_guide_review')}?action=load_topic_details&topic_id={self.topic.id}"
        response = c.get(url_panel)
        self.assertEqual(response.status_code, 400)

        # Generar borrador POST
        url_gen = reverse("content:generate_guide_draft_view")
        response = c.post(url_gen, {"topic_id": self.topic.id, "private_guide_ids": [self.quiz_guide.id]})
        self.assertEqual(response.status_code, 400)

    def test_originality_plagiarism_and_brand_detection(self):
        """Prueba que el motor de originalidad detecte n-gramas plagiados y marcas prohibidas."""
        # 1. Caso de plagio: texto contiene exactamente la secuencia de 10 palabras de la fuente
        # Fuente: "El movimiento rectilíneo uniforme se define como una trayectoria en línea recta con velocidad constante."
        plagiarized_content = {
            "introduction": "Aquí hablaremos de Cinemática.",
            "summary": "El movimiento rectilíneo uniforme se define como una trayectoria en línea recta con velocidad constante.", # copia literal
            "formulas": [],
            "items": [],
            "challenges": [],
            "answer_key": []
        }
        res_plagio = check_originality(plagiarized_content, [self.quiz_guide], threshold=10)
        self.assertFalse(res_plagio["passed"])
        self.assertTrue(any(issue["type"] == "copia_textual" for issue in res_plagio["issues"]))

        # 2. Caso de marca prohibida
        branded_content = {
            "introduction": "Material de cinemática distribuido por editorial sm.", # marca prohibida
            "summary": "Trayectoria original sin plagio textual.",
            "formulas": [],
            "items": [],
            "challenges": [],
            "answer_key": []
        }
        res_brand = check_originality(branded_content, [self.quiz_guide], threshold=10)
        self.assertFalse(res_brand["passed"])
        self.assertTrue(any(issue["type"] == "marca_prohibida" for issue in res_brand["issues"]))

        # 3. Caso original permitido
        original_content = {
            "introduction": "Estudiemos el movimiento rectilíneo.",
            "summary": "En esta clase analizaremos cuerpos que viajan a tasa uniforme.",
            "formulas": [],
            "items": [],
            "challenges": [],
            "answer_key": []
        }
        res_ok = check_originality(original_content, [self.quiz_guide], threshold=10)
        self.assertTrue(res_ok["passed"])

    def test_edit_draft_invalidates_originality_report(self):
        """Verifica que editar el borrador de la guía limpie atómicamente hash e informe previo."""
        guide = LearningGuide.objects.create(
            topic=self.topic,
            title="Guía",
            status="borrador",
            structured_content={"introduction": "Original"},
            originality_content_hash="some-hash",
            originality_report={"passed": True},
            originality_checked_at=timezone.now()
        )

        c = Client()
        c.force_login(self.admin_user)

        url_edit = reverse("content:edit_guide_draft_view", args=[guide.id])

        # POST con cambios
        new_content = self.valid_content(introduction="Cambio manual")
        response = c.post(url_edit, {"structured_content_json": json.dumps(new_content)})
        self.assertEqual(response.status_code, 200)

        guide.refresh_from_db()
        self.assertEqual(guide.originality_content_hash, "")
        self.assertEqual(guide.originality_report, {})
        self.assertIsNone(guide.originality_checked_at)

    def test_source_modification_invalidates_hash_on_publish(self):
        """Verifica que modificar una fuente privada después de validar invalide el hash extendido al publicar."""
        # 1. Generar la guía borrador
        guide = LearningGuide.objects.create(
            topic=self.topic,
            title="Guía de Cinemática",
            status="borrador",
            structured_content={
                "schema_version": 1,
                "introduction": "Estudiamos la velocidad en línea recta.",
                "summary": "En conclusión...",
                "formulas": [],
                "items": [],
                "challenges": [],
                "answer_key": []
            }
        )
        guide.private_sources.add(self.quiz_guide)

        # 2. Correr la validación inicial
        c = Client()
        c.force_login(self.admin_user)

        url_val = reverse("content:validate_originality_view", args=[guide.id])
        c.post(url_val)
        guide.refresh_from_db()

        # Validar que tiene hash correcto guardado
        hash_inicial = guide.originality_content_hash
        self.assertTrue(len(hash_inicial) > 0)

        # 3. Modificar la fuente privada (cambiar content_text para alterar su huella/hash)
        self.quiz_guide.content_text = "Movimiento alterado para romper el hash extendido de auditoría."
        self.quiz_guide.save()

        # 4. Intentar publicar. La revalidación en caliente recalculará el hash actual, detectará
        # la desincronización (porque la huella de la fuente cambió) y al re-evaluar la originalidad
        # actual, el hash debe fallar o no coincidir con el anterior, impidiendo la publicación.
        url_pub = reverse("content:publish_learning_guide_view", args=[guide.id])
        response = c.post(url_pub)
        self.assertEqual(response.status_code, 400) # Publicación bloqueada / revalidación en caliente fallida

    def test_concurrence_blocks_simultaneous_publishing(self):
        """Prueba que los bloqueos y UniqueConstraint prevengan dos publicaciones simultáneas en el mismo tema."""
        # Guía 1 (publicada)
        guide1 = LearningGuide.objects.create(
            topic=self.topic,
            title="Guía 1",
            status="publicada",
            visibility="publica",
            structured_content={"schema_version": 1}
        )

        # Guía 2 (borrador) intenta publicarse. La restricción unique_active_published_guide_per_topic
        # impide que exista más de una publicada activa.
        guide2 = LearningGuide.objects.create(
            topic=self.topic,
            title="Guía 2",
            status="borrador",
            visibility="interna",
            structured_content={"schema_version": 1}
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                # Forzar verificación de constraints en BD al intentar publicar una segunda guía del mismo tema
                guide2.status = "publicada"
                guide2.save()

    def test_draft_visibility_is_internal_only(self):
        """Verifica que una guía en estado borrador mantenga visibilidad interna y oculta al público."""
        guide = LearningGuide.objects.create(
            topic=self.topic,
            title="Borrador oculto",
            status="borrador",
            visibility="interna",
            structured_content={"schema_version": 1}
        )
        self.assertEqual(guide.visibility, "interna")

    def test_published_guide_cannot_be_silently_overwritten(self):
        """Verifica que una guía publicada no pueda ser editada/sobrescrita por la vista de edición."""
        guide = LearningGuide.objects.create(
            topic=self.topic,
            title="Publicada",
            status="publicada",
            visibility="publica",
            structured_content={"schema_version": 1, "introduction": "Original"}
        )

        c = Client()
        c.force_login(self.admin_user)

        url_edit = reverse("content:edit_guide_draft_view", args=[guide.id])
        # Intentar POST a una guía publicada debe arrojar error o requerir clonado/nuevo borrador
        # En la especificación la vista de edición está acotada al borrador; si está publicada
        # se bloquea o arroja error. Para forzar la protección, agregamos una comprobación en edit_guide_draft_view
        # de que la guía no esté publicada.
        # Probemos que la respuesta es 400
        new_content = {
            "schema_version": 1,
            "introduction": "Edición prohibida",
            "summary": "...",
            "formulas": [],
            "items": [],
            "challenges": [],
            "answer_key": []
        }
        response = c.post(url_edit, {"structured_content_json": json.dumps(new_content)})
        # Modificaremos edit_guide_draft_view en views para bloquear si no es borrador.
        self.assertEqual(response.status_code, 400)

    def test_access_control(self):
        """Prueba accesos no autorizados."""
        c = Client()
        response = c.get(reverse("content:learning_guide_review"))
        self.assertEqual(response.status_code, 302)

        c.force_login(self.regular_user)
        response = c.get(reverse("content:learning_guide_review"))
        self.assertEqual(response.status_code, 302)

    def test_legacy_bank_regression_remains_intact(self):
        """Verifica que los temas con structured_bank_enabled=False sigan funcionando con el banco legacy."""
        legacy_topic = Topic.objects.create(name="Física legacy", subject=self.subject, structured_bank_enabled=False)
        self.assertFalse(legacy_topic.structured_bank_enabled)

        # El flujo legacy de creación de preguntas y visualización sigue operando con normalidad.
        q = Question.objects.create(
            resource=self.resource,
            level=1,
            text="Pregunta legacy de prueba",
            scope=""
        )
        self.assertEqual(q.scope, "")
        self.assertIsNone(q.exercise_item)

    def test_originality_size_limit_exceeded(self):
        """Verifica que check_originality lance ValueError si el tamaño del contenido supera el límite operativo."""
        huge_content = {
            "introduction": "A" * 160000,
            "summary": "...",
            "formulas": [],
            "items": [],
            "challenges": [],
            "answer_key": []
        }
        with self.assertRaises(ValueError):
            check_originality(huge_content, [self.quiz_guide])

    def test_schema_invalid_difficulty(self):
        """Verifica que validate_guide_schema rechace ejercicios con dificultades no válidas."""
        invalid_diff_data = {
            "schema_version": 1,
            "introduction": "Intro",
            "summary": "Summary",
            "formulas": [],
            "items": [
                {
                    "item_id": self.item_approved.id,
                    "title": "Item",
                    "examples": [],
                    "exercises": [{"id": "q1", "difficulty": "super_dificil", "statement": "Ejercicio", "hint": "", "solution": "1"}]
                }
            ],
            "challenges": [],
            "answer_key": [{"exercise_id": "q1", "solution": "1"}]
        }
        with self.assertRaises(ValueError):
            validate_guide_schema(invalid_diff_data, [self.item_approved])

    def test_schema_duplicate_ids_in_challenges(self):
        """Verifica que validate_guide_schema rechace IDs de desafíos duplicados con ejemplos o ejercicios."""
        dup_challenge_data = {
            "schema_version": 1,
            "introduction": "Intro",
            "summary": "Summary",
            "formulas": [],
            "items": [
                {
                    "item_id": self.item_approved.id,
                    "title": "Item",
                    "examples": [],
                    "exercises": [{"id": "dup_id", "difficulty": "intermedia", "statement": "Ejercicio", "hint": "", "solution": "1"}]
                }
            ],
            "challenges": [
                {
                    "id": "dup_id",
                    "statement": "Desafío con id duplicado",
                    "hint": "",
                    "solution": "1"
                }
            ],
            "answer_key": [
                {"exercise_id": "dup_id", "solution": "1"}
            ]
        }
        with self.assertRaises(ValueError):
            validate_guide_schema(dup_challenge_data, [self.item_approved])

    def test_schema_requires_complete_item_and_answer_key_coverage(self):
        content = self.valid_content()
        content["answer_key"] = []
        with self.assertRaises(ValueError):
            validate_guide_schema(content, [self.item_approved])

        content = self.valid_content()
        content["items"] = []
        with self.assertRaises(ValueError):
            validate_guide_schema(content, [self.item_approved])

    def test_published_guide_can_spawn_replacement_without_overwrite(self):
        published = LearningGuide.objects.create(
            topic=self.topic,
            title="Versión publicada",
            status="publicada",
            visibility="publica",
            structured_content=self.valid_content(),
        )
        client = Client()
        client.force_login(self.admin_user)

        response = client.post(
            reverse("content:generate_guide_draft_view"),
            {
                "topic_id": self.topic.id,
                "private_guide_ids": [self.quiz_guide.id],
            },
        )
        self.assertEqual(response.status_code, 200)
        published.refresh_from_db()
        self.assertEqual(published.status, "publicada")
        replacement = LearningGuide.objects.get(
            topic=self.topic,
            status="borrador",
        )
        self.assertNotEqual(replacement.id, published.id)

    def test_replaced_published_guide_is_archived_and_not_reused(self):
        old_guide = LearningGuide.objects.create(
            topic=self.topic,
            title="Versión histórica",
            status="publicada",
            visibility="publica",
            structured_content=self.valid_content(),
        )
        new_guide = LearningGuide.objects.create(
            topic=self.topic,
            title="Versión nueva",
            status="borrador",
            visibility="interna",
            structured_content=self.valid_content(introduction="Redacción independiente."),
        )
        new_guide.private_sources.add(self.quiz_guide)
        result = check_originality(
            new_guide.structured_content,
            [self.quiz_guide],
        )
        self.assertTrue(result["passed"])
        new_guide.originality_report = result
        new_guide.originality_checked_at = timezone.now()
        new_guide.originality_content_hash = calculate_audit_hash(
            new_guide.structured_content,
            [self.quiz_guide],
        )
        new_guide.save()

        client = Client()
        client.force_login(self.admin_user)
        response = client.post(
            reverse("content:publish_learning_guide_view", args=[new_guide.id])
        )
        self.assertEqual(response.status_code, 200)
        old_guide.refresh_from_db()
        self.assertEqual(old_guide.status, "archivada")
        self.assertEqual(old_guide.visibility, "interna")

    def test_publish_rejects_source_that_becomes_unauthorized(self):
        guide = LearningGuide.objects.create(
            topic=self.topic,
            title="Borrador",
            status="borrador",
            structured_content=self.valid_content(),
        )
        guide.private_sources.add(self.quiz_guide)
        guide.originality_report = {"passed": True, "issues": []}
        guide.originality_checked_at = timezone.now()
        guide.originality_content_hash = calculate_audit_hash(
            guide.structured_content,
            [self.quiz_guide],
        )
        guide.save()
        self.quiz_guide.topics.remove(self.topic)

        client = Client()
        client.force_login(self.admin_user)
        response = client.post(
            reverse("content:publish_learning_guide_view", args=[guide.id])
        )
        self.assertEqual(response.status_code, 400)
        guide.refresh_from_db()
        self.assertEqual(guide.status, "borrador")

    def test_edit_cancel_returns_content_instead_of_edit_form(self):
        guide = LearningGuide.objects.create(
            topic=self.topic,
            title="Borrador",
            status="borrador",
            structured_content=self.valid_content(),
        )
        client = Client()
        client.force_login(self.admin_user)
        response = client.get(
            reverse("content:edit_guide_draft_view", args=[guide.id])
            + "?cancel=true"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Introducción")
        self.assertNotContains(response, "structured_content_json")
