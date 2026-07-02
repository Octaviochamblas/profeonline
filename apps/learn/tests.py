"""Tests de F2 — vistas de apps/learn/."""

import json
import re

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from apps.content.models import (
    ItemGroup,
    KnowledgeNode,
    NodeContent,
    NodeExercise,
    NodePrerequisite,
)

User = get_user_model()


def _build_tree(published=True):
    """Crea asignatura → eje → bloque → tema → recurso (hoja)."""
    asig = KnowledgeNode.objects.create(
        semantic_id="MAT", code="MAT", node_type=KnowledgeNode.NODE_ASIGNATURA,
        subject_abbr="MAT", name="Matemáticas", is_published=True,
    )
    eje = KnowledgeNode.objects.create(
        semantic_id="MAT.NUM", code="02", node_type=KnowledgeNode.NODE_EJE,
        subject_abbr="MAT", axis_abbr="NUM", name="Números", parent=asig,
        is_published=True,
    )
    bloque = KnowledgeNode.objects.create(
        semantic_id="MAT.NUM.B0201", code="02.01", node_type=KnowledgeNode.NODE_BLOQUE,
        subject_abbr="MAT", axis_abbr="NUM", name="Enteros", parent=eje,
        is_published=True,
    )
    tema = KnowledgeNode.objects.create(
        semantic_id="MAT.NUM.ENTEROS_CONJUNTO", code="02.01.01",
        node_type=KnowledgeNode.NODE_TEMA, subject_abbr="MAT", axis_abbr="NUM",
        name="Conjunto y orden", parent=bloque, is_published=True,
    )
    recurso = KnowledgeNode.objects.create(
        semantic_id="MAT.NUM.ENTEROS_CONJUNTO.NATURALES", code="02.01.01.01",
        node_type=KnowledgeNode.NODE_RECURSO, subject_abbr="MAT", axis_abbr="NUM",
        name="Números naturales", parent=tema, is_published=published,
    )
    return asig, eje, bloque, tema, recurso


class LearnHomeViewTests(TestCase):
    def test_home_200(self):
        KnowledgeNode.objects.create(
            semantic_id="MAT", code="MAT", node_type=KnowledgeNode.NODE_ASIGNATURA,
            subject_abbr="MAT", name="Matemáticas", is_published=True,
        )
        response = self.client.get("/aprender/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Matemáticas")

    def test_home_hides_unpublished(self):
        KnowledgeNode.objects.create(
            semantic_id="MAT", code="MAT", node_type=KnowledgeNode.NODE_ASIGNATURA,
            subject_abbr="MAT", name="Matemáticas", is_published=False,
        )
        response = self.client.get("/aprender/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Matemáticas")


class NodeListViewTests(TestCase):
    def setUp(self):
        self.asig, self.eje, self.bloque, self.tema, self.recurso = _build_tree()

    def test_asignatura_page_200(self):
        response = self.client.get(f"/aprender/{self.asig.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.eje.name)

    def test_eje_page_200(self):
        response = self.client.get(f"/aprender/{self.asig.slug}/{self.eje.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.bloque.name)

    def test_bloque_page_200(self):
        url = f"/aprender/{self.asig.slug}/{self.eje.slug}/{self.bloque.slug}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tema.name)

    def test_tema_page_200(self):
        url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recurso.name)

    def test_unknown_slug_returns_404(self):
        response = self.client.get("/aprender/no-existe/")
        self.assertEqual(response.status_code, 404)


class NodeDetailViewTests(TestCase):
    def setUp(self):
        self.asig, self.eje, self.bloque, self.tema, self.recurso = _build_tree()
        self.url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/{self.recurso.slug}/"
        )

    def test_recurso_without_content_shows_placeholder(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "siendo preparado")

    def test_recurso_with_content_shows_sections(self):
        NodeContent.objects.create(
            node=self.recurso,
            objetivo="Identificar números naturales.",
            explicacion="Los naturales son $\\mathbb{N}$.",
            estado=NodeContent.ESTADO_PUBLICADO,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Identificar números naturales.")

    def test_resumen_renders_markdown_and_math(self):
        NodeContent.objects.create(
            node=self.recurso,
            resumen="Un **resumen** con $0$ y una lista:\n\n- punto clave",
            estado=NodeContent.ESTADO_PUBLICADO,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<strong>resumen</strong>", html=False)
        self.assertContains(response, "<li>punto clave</li>", html=False)
        self.assertContains(response, "$0$", html=False)
        self.assertNotContains(response, "**resumen**", html=False)

    def test_draft_content_sets_noindex(self):
        NodeContent.objects.create(
            node=self.recurso,
            estado=NodeContent.ESTADO_BORRADOR,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "noindex")

    def test_published_content_no_noindex(self):
        NodeContent.objects.create(
            node=self.recurso,
            estado=NodeContent.ESTADO_PUBLICADO,
        )
        response = self.client.get(self.url)
        self.assertNotContains(response, "noindex")

    def test_unpublished_node_returns_404_for_anonymous(self):
        _, _, _, _, recurso_priv = _build_tree.__func__() if False else (None,) * 4 + (None,)
        recurso_priv = KnowledgeNode.objects.create(
            semantic_id="MAT.NUM.ENTEROS_CONJUNTO.ENTEROS",
            code="02.01.01.02",
            node_type=KnowledgeNode.NODE_RECURSO,
            subject_abbr="MAT",
            name="Enteros (privado)",
            parent=self.tema,
            is_published=False,
        )
        url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/{recurso_priv.slug}/"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_unpublished_node_visible_for_staff(self):
        staff = User.objects.create_user("prof", password="pass", is_staff=True)
        self.client.force_login(staff)
        recurso_priv = KnowledgeNode.objects.create(
            semantic_id="MAT.NUM.ENTEROS_CONJUNTO.ENTEROS2",
            code="02.01.01.03",
            node_type=KnowledgeNode.NODE_RECURSO,
            subject_abbr="MAT",
            name="Enteros (privado staff)",
            parent=self.tema,
            is_published=False,
        )
        url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/{recurso_priv.slug}/"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_breadcrumb_contains_ancestors(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Matemáticas")
        self.assertContains(response, "Números")
        self.assertContains(response, "Enteros")

    def test_anonymous_does_not_see_manual_content_editor(self):
        NodeContent.objects.create(node=self.recurso)

        response = self.client.get(self.url)

        self.assertNotContains(response, "Editar contenido")

    def test_authorized_staff_can_edit_existing_content(self):
        content = NodeContent.objects.create(node=self.recurso)
        admin = User.objects.create_superuser(
            "admin-editor", "admin@example.com", "pass"
        )
        self.client.force_login(admin)

        response = self.client.get(self.url)

        self.assertContains(response, "Editar contenido")
        self.assertContains(response, "data-content-editor-dialog")
        self.assertContains(response, 'name="updated_at"')
        self.assertContains(response, reverse("learn:edit_node_content", args=[self.recurso.pk]))

    def test_authorized_staff_can_create_missing_content_for_node(self):
        admin = User.objects.create_superuser(
            "admin-creator", "creator@example.com", "pass"
        )
        self.client.force_login(admin)

        response = self.client.get(self.url)

        self.assertContains(response, "Crear contenido")
        self.assertContains(response, "data-content-editor-dialog")
        self.assertContains(response, reverse("learn:edit_node_content", args=[self.recurso.pk]))

    def test_staff_without_model_permission_does_not_see_editor(self):
        NodeContent.objects.create(node=self.recurso)
        staff = User.objects.create_user(
            "staff-no-editor", password="pass", is_staff=True
        )
        self.client.force_login(staff)

        response = self.client.get(self.url)

        self.assertNotContains(response, "Editar contenido")


class ResourceNavigationTests(TestCase):
    def setUp(self):
        self.asig, self.eje, self.bloque, self.tema, self.recurso = _build_tree()
        self.recurso.order = 2
        self.recurso.save(update_fields=["order"])
        self.url = self._url(self.recurso)

    def _resource(self, name, code, order, published=True):
        return KnowledgeNode.objects.create(
            semantic_id=f"MAT.NUM.ENTEROS_CONJUNTO.{name.upper().replace(' ', '_')}",
            code=code,
            node_type=KnowledgeNode.NODE_RECURSO,
            subject_abbr="MAT",
            axis_abbr="NUM",
            name=name,
            parent=self.tema,
            order=order,
            is_published=published,
        )

    def _url(self, resource):
        return (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/{resource.slug}/"
        )

    def test_middle_resource_links_to_previous_and_next(self):
        previous = self._resource("Anterior ordenado", "02.01.01.00", 1)
        next_resource = self._resource("Siguiente ordenado", "02.01.01.02", 3)

        response = self.client.get(self.url)

        self.assertContains(response, "Recurso anterior")
        self.assertContains(response, previous.name)
        self.assertContains(response, self._url(previous))
        self.assertContains(response, "Recurso siguiente")
        self.assertContains(response, next_resource.name)
        self.assertContains(response, self._url(next_resource))

    def test_same_order_uses_code_as_tiebreaker(self):
        previous = self._resource("Anterior por código", "02.01.01.00", 2)
        next_resource = self._resource("Siguiente por código", "02.01.01.02", 2)

        response = self.client.get(self.url)

        self.assertContains(response, previous.name)
        self.assertContains(response, next_resource.name)

    def test_first_resource_only_shows_next_link(self):
        self.recurso.order = 0
        self.recurso.save(update_fields=["order"])
        next_resource = self._resource("Solo siguiente", "02.01.01.02", 1)

        response = self.client.get(self.url)

        self.assertNotContains(response, "Recurso anterior")
        self.assertContains(response, "Recurso siguiente")
        self.assertContains(response, next_resource.name)

    def test_anonymous_skips_unpublished_neighbor(self):
        visible = self._resource("Anterior visible", "02.01.01.00", 0)
        hidden = self._resource("Anterior privado", "02.01.01.02", 1, published=False)

        response = self.client.get(self.url)

        self.assertContains(response, visible.name)
        self.assertNotContains(response, hidden.name)

    def test_staff_can_navigate_to_unpublished_neighbor(self):
        hidden = self._resource("Anterior privado", "02.01.01.00", 1, published=False)
        staff = User.objects.create_user("nav-staff", password="pass", is_staff=True)
        self.client.force_login(staff)

        response = self.client.get(self.url)

        self.assertContains(response, hidden.name)
        self.assertContains(response, self._url(hidden))


class NodeContentEditorViewTests(TestCase):
    def setUp(self):
        self.asig, self.eje, self.bloque, self.tema, self.recurso = _build_tree()
        self.url = reverse("learn:edit_node_content", args=[self.recurso.pk])
        self.page_url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/{self.recurso.slug}/"
        )
        self.admin = User.objects.create_superuser(
            "inline-editor", "inline@example.com", "pass"
        )

    def _payload(self, content=None, **overrides):
        payload = {
            "objetivo": "Objetivo **editado**",
            "introduccion": "Introducción con $x$",
            "resumen": "Resumen",
            "explicacion": "Explicación",
            "procedimiento": ["Paso 2", "Paso 1"],
            "ejemplos": [
                {
                    "titulo": "Ejemplo visual",
                    "enunciado": "Resuelve $x+1=2$",
                    "respuesta": "Sí",
                    "solucion_pasos": ["Restar 1", "$x=1$"],
                }
            ],
            "errores_frecuentes": ["Error B", "Error A"],
            "fuente": "Fuente manual",
            "estado": NodeContent.ESTADO_PUBLICADO,
            "updated_at": content.updated_at.isoformat() if content else "",
        }
        payload.update(overrides)
        return payload

    def _post(self, payload):
        return self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_get_is_not_allowed(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_anonymous_post_redirects_to_login(self):
        response = self._post(self._payload())
        self.assertEqual(response.status_code, 302)

    def test_post_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.admin)
        response = csrf_client.post(
            self.url,
            data=json.dumps(self._payload()),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_without_permission_gets_403(self):
        user = User.objects.create_user("no-editor", password="pass")
        self.client.force_login(user)
        response = self._post(self._payload())
        self.assertEqual(response.status_code, 403)

    def test_non_resource_node_returns_404(self):
        self.client.force_login(self.admin)
        self.url = reverse("learn:edit_node_content", args=[self.tema.pk])
        response = self._post(self._payload())
        self.assertEqual(response.status_code, 404)

    def test_invalid_json_returns_400_without_write(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            self.url, data="{", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(NodeContent.objects.filter(node=self.recurso).exists())

    def test_invalid_example_returns_400_without_partial_update(self):
        content = NodeContent.objects.create(node=self.recurso, objetivo="Original")
        self.client.force_login(self.admin)
        payload = self._payload(
            content,
            ejemplos=[{"titulo": "", "enunciado": "", "respuesta": "Tal vez"}],
        )
        response = self._post(payload)
        self.assertEqual(response.status_code, 400)
        content.refresh_from_db()
        self.assertEqual(content.objetivo, "Original")

    def test_creates_content_and_marks_manual_override(self):
        self.client.force_login(self.admin)
        response = self._post(self._payload())
        self.assertEqual(response.status_code, 200)
        content = NodeContent.objects.get(node=self.recurso)
        self.assertTrue(content.manual_override)
        self.assertEqual(content.manual_edited_by, self.admin)
        self.assertIsNotNone(content.manual_edited_at)
        self.assertEqual(content.estado, NodeContent.ESTADO_PUBLICADO)

    def test_updates_all_fields_preserving_list_order(self):
        content = NodeContent.objects.create(node=self.recurso, objetivo="Original")
        self.client.force_login(self.admin)
        response = self._post(self._payload(content))
        self.assertEqual(response.status_code, 200)
        content.refresh_from_db()
        self.assertEqual(content.objetivo, "Objetivo **editado**")
        self.assertEqual(content.procedimiento, ["Paso 2", "Paso 1"])
        self.assertEqual(content.errores_frecuentes, ["Error B", "Error A"])
        self.assertEqual(content.ejemplos[0]["solucion_pasos"], ["Restar 1", "$x=1$"])
        self.assertEqual(content.fuente, "Fuente manual")

    def test_rendered_version_token_is_accepted(self):
        content = NodeContent.objects.create(node=self.recurso, objetivo="Original")
        self.client.force_login(self.admin)
        page = self.client.get(self.page_url)
        match = re.search(
            rb'name="updated_at" value="([^"]+)"', page.content
        )
        self.assertIsNotNone(match)
        rendered_token = match.group(1).decode()

        response = self._post(self._payload(content, updated_at=rendered_token))

        self.assertEqual(response.status_code, 200)

    def test_stale_updated_at_returns_409(self):
        content = NodeContent.objects.create(node=self.recurso, objetivo="Original")
        content.objetivo = "Cambio paralelo"
        content.save()
        self.client.force_login(self.admin)
        response = self._post(
            self._payload(
                content,
                updated_at="2000-01-01T00:00:00+00:00",
                objetivo="Sobrescribir",
            )
        )
        self.assertEqual(response.status_code, 409)
        content.refresh_from_db()
        self.assertEqual(content.objetivo, "Cambio paralelo")


class NodePracticeBankViewTests(TestCase):
    def setUp(self):
        self.asig, self.eje, self.bloque, self.tema, self.recurso = _build_tree()
        self.url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/{self.recurso.slug}/"
        )
        self.group = ItemGroup.objects.create(
            node=self.recurso,
            code="conceptuales",
            title="Preguntas conceptuales",
            level=ItemGroup.LEVEL_COMPRENDER,
            order=1,
            is_published=True,
        )

    def test_published_exercise_shows_in_bank(self):
        NodeExercise.objects.create(
            node=self.recurso,
            item_group=self.group,
            prompt="¿Qué es un número natural?",
            correct_answer="Un entero positivo",
            status=NodeExercise.STATUS_PUBLISHED,
        )
        response = self.client.get(self.url)
        self.assertContains(response, "Practica")
        self.assertContains(response, "¿Qué es un número natural?")

    def test_unpublished_exercise_hidden_from_bank(self):
        NodeExercise.objects.create(
            node=self.recurso,
            item_group=self.group,
            prompt="Ejercicio en revisión",
            status=NodeExercise.STATUS_REVIEW_REQUIRED,
        )
        response = self.client.get(self.url)
        self.assertNotContains(response, "Practica")
        self.assertNotContains(response, "Ejercicio en revisión")

    def test_no_exercises_no_bank_section(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "Practica")


class NodePrerequisiteDisplayTests(TestCase):
    def setUp(self):
        self.asig, self.eje, self.bloque, self.tema, self.recurso = _build_tree()
        self.url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/{self.recurso.slug}/"
        )
        self.target = KnowledgeNode.objects.create(
            semantic_id="MAT.NUM.ENTEROS_CONJUNTO.PRE",
            code="02.01.01.09",
            node_type=KnowledgeNode.NODE_RECURSO,
            subject_abbr="MAT",
            axis_abbr="NUM",
            name="Recurso previo",
            parent=self.tema,
            is_published=True,
        )

    def test_shows_published_prerequisite(self):
        NodePrerequisite.objects.create(
            node=self.recurso,
            requires=self.target,
            kind=NodePrerequisite.KIND_REQUERIDO,
        )
        response = self.client.get(self.url)
        self.assertContains(response, "Antes de empezar")
        self.assertContains(response, "Recurso previo")

    def test_hides_unpublished_prerequisite_target(self):
        self.target.is_published = False
        self.target.save()
        NodePrerequisite.objects.create(
            node=self.recurso,
            requires=self.target,
            kind=NodePrerequisite.KIND_REQUERIDO,
        )
        response = self.client.get(self.url)
        self.assertNotContains(response, "Antes de empezar")

    def test_no_prerequisites_no_section(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "Antes de empezar")
