from unittest.mock import patch

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.content.models import (
    Subject,
    Topic,
    Resource,
    QuizGuide,
    ExerciseItem,
    ResourceExerciseItem,
    Question,
)
from apps.content.services.item_extraction_service import (
    propose_items_from_guide,
    get_topic_education_level,
    _build_item_prompt,
)
from apps.content.services.ai_generation_service import generate_questions_for_resource

User = get_user_model()


class ItemExtractionTests(TestCase):
    def setUp(self):
        # Configurar la BD básica para las pruebas
        self.subject = Subject.objects.create(name="Física y Álgebra", education_level="media")
        self.topic = Topic.objects.create(
            name="Álgebra interactiva", subject=self.subject, structured_bank_enabled=True
        )

        self.resource1 = Resource.objects.create(
            title="Introducción al Álgebra",
            subject=self.subject,
            topic=self.topic,
            is_published=True
        )
        self.resource2 = Resource.objects.create(
            title="Reducción de expresiones",
            subject=self.subject,
            topic=self.topic,
            is_published=True
        )

        self.quiz_guide = QuizGuide.objects.create(
            title="Guía Estilo PAES de Álgebra",
            content_text="Resolver $3x + 5 = 14$ paso a paso. Problema de aplicación de optimización lineal."
        )
        self.quiz_guide.topics.add(self.topic)

        # Crear usuarios para las pruebas de permisos
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@profeonline.cl", password="password"
        )
        self.regular_user = User.objects.create_user(
            username="regular", email="regular@profeonline.cl", password="password"
        )

    def test_education_level_fallback(self):
        """Verifica que get_topic_education_level sigue las reglas de fallback correctas."""
        # Caso 1: Los recursos del tema no tienen nivel propio pero la asignatura es 'media'
        self.assertEqual(get_topic_education_level(self.topic), "media")

        # Caso 2: El tema tiene nivel propio configurado
        self.topic.education_level = "escolar"
        self.topic.save()
        self.assertEqual(get_topic_education_level(self.topic), "escolar")

        # Caso 3: El tema tiene recursos asociados que devuelven un nivel (heredado o explícito)
        # Vamos a quitar el nivel educativo del tema y agregar un nivel educativo a la asignatura.
        # Por herencia de get_education_level de Resource, si la asignatura tiene 'universitaria',
        # los recursos devuelven 'universitaria'.
        self.topic.education_level = ""
        self.topic.save()
        self.subject.education_level = "universitaria"
        self.subject.save()

        self.assertEqual(self.resource1.get_education_level(), "universitaria")
        self.assertEqual(get_topic_education_level(self.topic), "universitaria")

    def test_build_prompt_includes_education_level(self):
        """Verifica que el prompt generado para la IA incluye el nivel educativo."""
        prompt = _build_item_prompt(self.quiz_guide, self.topic, "escolar")
        self.assertIn("escolar", prompt.lower())
        self.assertIn("basica o intermedia", prompt.lower())

        prompt_uni = _build_item_prompt(self.quiz_guide, self.topic, "universitaria")
        self.assertIn("universitaria", prompt_uni.lower())
        self.assertIn("avanzada o desafio", prompt_uni.lower())

    def test_service_mock_items(self):
        """Verifica que el modo mock determinista funciona y calibra dificultades."""
        # Para el nivel escolar
        self.topic.education_level = "escolar"
        self.topic.save()
        items_escolar = propose_items_from_guide(self.quiz_guide, self.topic)
        self.assertEqual(len(items_escolar), 3)
        # Escolar debe retornar basica e intermedia (claves canónicas, sin acento)
        difficulties_escolar = {itm["difficulty"] for itm in items_escolar}
        self.assertTrue(difficulties_escolar.issubset({"basica", "intermedia"}))

        # Para el nivel universitario
        self.topic.education_level = "universitaria"
        self.topic.save()
        items_uni = propose_items_from_guide(self.quiz_guide, self.topic)
        difficulties_uni = {itm["difficulty"] for itm in items_uni}
        # Universitaria debe retornar avanzada y desafio (claves canónicas, sin acento)
        self.assertTrue(difficulties_uni.issubset({"avanzada", "desafio"}))

    def test_access_control_item_extraction_views(self):
        """Verifica que solo los administradores puedan acceder al panel de ítems."""
        c = Client()
        urls = [
            reverse("content:item_extraction"),
            reverse("content:propose_items"),
            reverse("content:edit_item_inline", args=[1]),
            reverse("content:set_item_status", args=[1]),
            reverse("content:merge_items"),
            reverse("content:link_item_resource", args=[1]),
            reverse("content:unlink_item_resource", args=[1]),
        ]

        for url in urls:
            # 1. Anónimo -> Redirige al login o devuelve 403/redirect
            response = c.get(url)
            self.assertEqual(response.status_code, 302)

            # 2. Regular -> Redirige/403
            c.force_login(self.regular_user)
            if url == reverse("content:item_extraction"):
                response = c.get(url)
            else:
                response = c.post(url)
            self.assertEqual(response.status_code, 302)
            c.logout()

            # 3. Admin -> Debe funcionar (devolver 200, 400 o 404, no redireccionar a login)
            c.force_login(self.admin_user)
            if url == reverse("content:item_extraction"):
                response = c.get(url)
                self.assertEqual(response.status_code, 200)
            elif url == reverse("content:edit_item_inline", args=[999]): # ID inexistente para causar 404
                response = c.get(url)
                self.assertEqual(response.status_code, 404)
            c.logout()

    def test_propose_items_view(self):
        """Prueba que propose_items guarda los ítems y recursos asociados con validaciones."""
        c = Client()
        c.force_login(self.admin_user)

        # 1. Ejecutar POST para proponer ítems (usará el mock determinista en testing)
        url = reverse("content:propose_items")
        response = c.post(url, {"topic_id": self.topic.id, "guide_id": self.quiz_guide.id})
        self.assertEqual(response.status_code, 200)

        # Verificar que se crearon los ítems en base de datos
        items = ExerciseItem.objects.filter(topic=self.topic)
        self.assertEqual(items.count(), 3)
        for item in items:
            self.assertEqual(item.status, "propuesto")
            # Los recursos sugeridos en el mock (los del tema) deben estar vinculados en ResourceExerciseItem
            self.assertTrue(item.resource_links.exists())
            for link in item.resource_links.all():
                self.assertEqual(link.practice_quota, 0)
                self.assertEqual(link.evaluation_quota, 0)

    def test_edit_item_inline_view(self):
        """Prueba la edición en línea y la cancelación."""
        item = ExerciseItem.objects.create(
            topic=self.topic,
            title="Item original",
            level=1,
            difficulty="basica",
            objective="Original",
        )

        c = Client()
        c.force_login(self.admin_user)

        # 1. GET: Formulario de edición
        url = reverse("content:edit_item_inline", args=[item.id])
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Item original")

        # 2. GET con cancel=true -> debe volver a la fila normal (modo lectura)
        response = c.get(f"{url}?cancel=true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "✏️ Editar")

        # 3. POST: Guardar cambios
        response = c.post(url, {
            "title": "Item editado",
            "objective": "Objetivo editado",
            "level": 2,
            "difficulty": "avanzada",
            "recommendation": "Rec",
            "common_errors": "Err",
        })
        self.assertEqual(response.status_code, 200)

        item.refresh_from_db()
        self.assertEqual(item.title, "Item editado")
        self.assertEqual(item.objective, "Objetivo editado")
        self.assertEqual(item.level, 2)
        self.assertEqual(item.difficulty, "avanzada")

    def test_set_item_status_view(self):
        """Prueba la aprobación y archivado de ítems."""
        item = ExerciseItem.objects.create(
            topic=self.topic,
            title="Item de estado",
            level=1,
            objective="Test",
            status="propuesto",
        )

        c = Client()
        c.force_login(self.admin_user)

        # 1. Aprobar
        url = reverse("content:set_item_status", args=[item.id])
        response = c.post(url, {"status": "aprobado"})
        self.assertEqual(response.status_code, 200)
        item.refresh_from_db()
        self.assertEqual(item.status, "aprobado")

        # 2. Archivar -> Debe responder vacío (o eliminar la fila del DOM)
        response = c.post(url, {"status": "archivado"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")
        item.refresh_from_db()
        self.assertEqual(item.status, "archivado")

    def test_merge_items_view(self):
        """Prueba la fusión de ítems combinando campos y previniendo duplicados de recursos."""
        item1 = ExerciseItem.objects.create(
            topic=self.topic, title="Tema 1", level=1, difficulty="basica", objective="Obj1", common_errors="Err1"
        )
        item2 = ExerciseItem.objects.create(
            topic=self.topic, title="Tema 2", level=2, difficulty="intermedia", objective="Obj2", common_errors="Err2"
        )

        # Asociar recursos a ambos (algunos compartidos para probar unicidad)
        ResourceExerciseItem.objects.create(exercise_item=item1, resource=self.resource1)
        ResourceExerciseItem.objects.create(exercise_item=item2, resource=self.resource1) # recurso compartido
        ResourceExerciseItem.objects.create(exercise_item=item2, resource=self.resource2) # recurso único de item2

        c = Client()
        c.force_login(self.admin_user)

        url = reverse("content:merge_items")
        response = c.post(url, {
            "item_ids": [item1.id, item2.id],
            "topic_id": self.topic.id
        })
        self.assertEqual(response.status_code, 200)

        # Verificar que los antiguos se archivaron
        item1.refresh_from_db()
        item2.refresh_from_db()
        self.assertEqual(item1.status, "archivado")
        self.assertEqual(item2.status, "archivado")

        # Verificar que se creó el nuevo ítem consolidado
        merged_item = ExerciseItem.objects.exclude(status="archivado").get(topic=self.topic)
        self.assertIn("Fusión", merged_item.title)
        self.assertEqual(merged_item.level, 2) # max de 1 y 2
        self.assertIn("Obj1", merged_item.objective)
        self.assertIn("Obj2", merged_item.objective)
        self.assertIn("Err1", merged_item.common_errors)
        self.assertIn("Err2", merged_item.common_errors)

        # Verificar que se asignaron los recursos sin duplicados
        self.assertEqual(merged_item.resource_links.count(), 2)
        linked_res_ids = set(merged_item.resource_links.values_list("resource_id", flat=True))
        self.assertEqual(linked_res_ids, {self.resource1.id, self.resource2.id})

    def test_link_and_unlink_resource_views(self):
        """Prueba la vinculación y desvinculación de recursos."""
        item = ExerciseItem.objects.create(
            topic=self.topic, title="Item", level=1, objective="Obj"
        )

        c = Client()
        c.force_login(self.admin_user)

        # 1. Vincular resource1
        url_link = reverse("content:link_item_resource", args=[item.id])
        response = c.post(url_link, {"resource_id": self.resource1.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ResourceExerciseItem.objects.filter(exercise_item=item, resource=self.resource1).exists())

        # 2. Desvincular resource1
        url_unlink = reverse("content:unlink_item_resource", args=[item.id])
        response = c.post(url_unlink, {"resource_id": self.resource1.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ResourceExerciseItem.objects.filter(exercise_item=item, resource=self.resource1).exists())

    def test_flag_disabled_blocks_panel_and_mutations(self):
        """Un tema con structured_bank_enabled=False queda fuera del sistema nuevo."""
        off_topic = Topic.objects.create(
            name="Tema legacy", subject=self.subject, structured_bank_enabled=False
        )
        off_guide = QuizGuide.objects.create(title="G", content_text="x")
        off_guide.topics.add(off_topic)
        off_item = ExerciseItem.objects.create(
            topic=off_topic, title="X", level=1, objective="Y"
        )

        c = Client()
        c.force_login(self.admin_user)

        # No aparece en el selector inicial de temas.
        resp = c.get(reverse("content:item_extraction"))
        self.assertNotContains(resp, "Tema legacy")

        # load_guides / list_items sobre un tema apagado → 404.
        url = reverse("content:item_extraction")
        self.assertEqual(c.get(f"{url}?action=load_guides&topic_id={off_topic.id}").status_code, 404)
        self.assertEqual(c.get(f"{url}?action=list_items&topic_id={off_topic.id}").status_code, 404)

        # No se pueden proponer ni mutar ítems de un tema apagado.
        self.assertEqual(
            c.post(reverse("content:propose_items"),
                   {"topic_id": off_topic.id, "guide_id": off_guide.id}).status_code,
            404,
        )
        self.assertEqual(
            c.post(reverse("content:set_item_status", args=[off_item.id]),
                   {"status": "aprobado"}).status_code,
            404,
        )
        off_item.refresh_from_db()
        self.assertEqual(off_item.status, "propuesto")  # intacto

    def test_foreign_or_inactive_guide_rejected(self):
        """propose_items rechaza guías ajenas al tema o inactivas (no las manda a la IA)."""
        c = Client()
        c.force_login(self.admin_user)
        url = reverse("content:propose_items")

        # Guía sin vínculo al tema ni a su asignatura.
        foreign = QuizGuide.objects.create(title="Ajena", content_text="x")
        resp = c.post(url, {"topic_id": self.topic.id, "guide_id": foreign.id})
        self.assertEqual(resp.status_code, 404)

        # Guía vinculada pero inactiva.
        self.quiz_guide.is_active = False
        self.quiz_guide.save()
        resp = c.post(url, {"topic_id": self.topic.id, "guide_id": self.quiz_guide.id})
        self.assertEqual(resp.status_code, 404)
        self.assertFalse(ExerciseItem.objects.filter(topic=self.topic).exists())

    def test_merge_cross_topic_rejected(self):
        """No se pueden fusionar ítems de temas distintos."""
        other_topic = Topic.objects.create(
            name="Otro tema", subject=self.subject, structured_bank_enabled=True
        )
        item_a = ExerciseItem.objects.create(topic=self.topic, title="A", level=1, objective="oa")
        item_b = ExerciseItem.objects.create(topic=other_topic, title="B", level=1, objective="ob")

        c = Client()
        c.force_login(self.admin_user)
        resp = c.post(reverse("content:merge_items"), {"item_ids": [item_a.id, item_b.id]})
        self.assertEqual(resp.status_code, 400)
        item_a.refresh_from_db()
        item_b.refresh_from_db()
        self.assertEqual(item_a.status, "propuesto")
        self.assertEqual(item_b.status, "propuesto")

    def test_template_has_no_inline_script_or_onclick(self):
        """La página del panel no debe traer JS inline ni handlers onclick (CSP con nonce)."""
        c = Client()
        c.force_login(self.admin_user)
        html = c.get(reverse("content:item_extraction")).content.decode()
        self.assertNotIn("onclick", html)
        # El único <script> debe cargar el archivo externo con nonce.
        self.assertIn("js/item-extraction.js", html)
        self.assertNotIn("<script>", html)  # sin scripts inline sin atributos

    def test_service_does_not_call_network_in_tests(self):
        """Sin llaves y en modo test, el servicio usa el mock y nunca llama a la red."""
        with patch("apps.content.services.item_extraction_service._call_gemini_api") as gem, \
             patch("apps.content.services.item_extraction_service._call_openai_api") as oai:
            items = propose_items_from_guide(self.quiz_guide, self.topic)
        self.assertTrue(items)
        gem.assert_not_called()
        oai.assert_not_called()

    def test_propose_items_dedupes_resources_and_stores_count(self):
        """IDs de recurso duplicados de la IA no abortan la transacción; se guarda el conteo."""
        crafted = [{
            "title": "Ítem con duplicados",
            "level": 2,
            "difficulty": "avanzada",
            "objective": "Obj",
            "recommendation": "",
            "common_errors": "",
            "suggested_resource_ids": [self.resource1.id, self.resource1.id, 999999],
            "detected_exercise_count": 7,
        }]
        c = Client()
        c.force_login(self.admin_user)
        with patch("apps.content.views.item_review.propose_items_from_guide", return_value=crafted):
            resp = c.post(reverse("content:propose_items"),
                          {"topic_id": self.topic.id, "guide_id": self.quiz_guide.id})
        self.assertEqual(resp.status_code, 200)
        item = ExerciseItem.objects.get(topic=self.topic, title="Ítem con duplicados")
        # Solo un vínculo (deduplicado); el ID inexistente se ignora.
        self.assertEqual(item.resource_links.count(), 1)
        self.assertEqual(item.detected_exercise_count, 7)

    def test_edit_rejects_invalid_choices(self):
        """La edición valida level/difficulty contra los choices (400 si inválidos)."""
        item = ExerciseItem.objects.create(
            topic=self.topic, title="Item", level=1, difficulty="basica", objective="Obj"
        )
        c = Client()
        c.force_login(self.admin_user)
        resp = c.post(reverse("content:edit_item_inline", args=[item.id]), {
            "title": "T", "objective": "O", "level": 99, "difficulty": "imposible",
        })
        self.assertEqual(resp.status_code, 400)
        item.refresh_from_db()
        self.assertEqual(item.level, 1)  # sin cambios
        self.assertEqual(item.difficulty, "basica")

    def test_normalize_difficulty_maps_accented_variants(self):
        """normalize_difficulty mapea variantes acentuadas/mayúsculas a la clave del modelo."""
        self.assertEqual(Question.normalize_difficulty("Básica"), "basica")
        self.assertEqual(Question.normalize_difficulty("DESAFÍO"), "desafio")
        self.assertEqual(Question.normalize_difficulty(" intermedia "), "intermedia")
        self.assertEqual(Question.normalize_difficulty("avanzada"), "avanzada")
        self.assertEqual(Question.normalize_difficulty("inexistente"), "")
        self.assertEqual(Question.normalize_difficulty(""), "")
        self.assertEqual(Question.normalize_difficulty(None), "")

    def test_propose_items_normalizes_accented_difficulty(self):
        """La IA puede devolver 'Básica' (acentuada); debe persistirse como clave canónica."""
        crafted = [{
            "title": "Ítem acentuado", "level": 2, "difficulty": "Avanzada",
            "objective": "Obj", "recommendation": "", "common_errors": "",
            "suggested_resource_ids": [], "detected_exercise_count": 0,
        }]
        c = Client()
        c.force_login(self.admin_user)
        with patch("apps.content.views.item_review.propose_items_from_guide", return_value=crafted):
            resp = c.post(reverse("content:propose_items"),
                          {"topic_id": self.topic.id, "guide_id": self.quiz_guide.id})
        self.assertEqual(resp.status_code, 200)
        item = ExerciseItem.objects.get(topic=self.topic, title="Ítem acentuado")
        self.assertEqual(item.difficulty, "avanzada")  # normalizada, no perdida

    def test_legacy_generation_regression(self):
        """Prueba de regresión: verifica que los flujos legacy de generación siguen funcionando."""
        # Se genera mock_questions normalmente usando la suite legacy de generación
        self.resource1.content = "Ecuación afín de la forma $y = mx + n$."
        self.resource1.save()

        # Debe generar 2 preguntas en modo mock (sin llaves configuradas)
        questions = generate_questions_for_resource(self.resource1, level=1, count=2)
        self.assertEqual(len(questions), 2)
        for q in questions:
            self.assertEqual(q.resource, self.resource1)
            self.assertEqual(q.level, 1)
            self.assertEqual(q.scope, "")  # scope vacío indica pregunta legacy sin clasificar
