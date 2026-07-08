"""Tests de F2 — vistas de apps/learn/."""

from django.contrib.auth import get_user_model
from django.test import TestCase
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
        subject = KnowledgeNode.objects.create(
            semantic_id="MAT", code="MAT", node_type=KnowledgeNode.NODE_ASIGNATURA,
            subject_abbr="MAT", name="Matemáticas", is_published=True,
        )
        response = self.client.get("/aprender/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Matemáticas")
        self.assertContains(response, "learn-card-grid")
        self.assertContains(response, "learn-card")
        self.assertContains(response, f'/aprender/{subject.slug}/')
        self.assertContains(response, "/static/css/learn-catalog.css?v=7")

    def test_home_hides_unpublished(self):
        KnowledgeNode.objects.create(
            semantic_id="MAT", code="MAT", node_type=KnowledgeNode.NODE_ASIGNATURA,
            subject_abbr="MAT", name="Matemáticas", is_published=False,
        )
        response = self.client.get("/aprender/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Matemáticas")

    def test_home_empty_state_is_presented_as_panel(self):
        response = self.client.get("/aprender/")

        self.assertContains(response, "learn-card-grid__empty")
        self.assertContains(response, "Estamos preparando nuevas asignaturas")


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

    def test_list_uses_clickable_cards_and_compact_breadcrumbs(self):
        url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/"
        )

        response = self.client.get(url)

        self.assertContains(response, 'class="learn-breadcrumbs"')
        self.assertContains(response, 'class="learn-breadcrumbs__current"')
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, 'class="learn-card"')
        self.assertContains(response, self.recurso.code)
        self.assertContains(response, f'{url}{self.recurso.slug}/')
        self.assertContains(response, "Selecciona un contenido para continuar")
        self.assertContains(response, "/static/css/learn-catalog.css?v=7")

    def test_list_hides_unpublished_children_for_anonymous(self):
        hidden = KnowledgeNode.objects.create(
            semantic_id="MAT.NUM.ENTEROS_CONJUNTO.OCULTO",
            code="02.01.01.02",
            node_type=KnowledgeNode.NODE_RECURSO,
            subject_abbr="MAT",
            axis_abbr="NUM",
            name="Recurso oculto",
            parent=self.tema,
            is_published=False,
        )
        url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/"
        )

        response = self.client.get(url)

        self.assertNotContains(response, hidden.name)

    def test_list_renders_long_title_inside_card(self):
        self.recurso.name = (
            "Identificación del desplazamiento vertical de una función "
            "trigonométrica periódica"
        )
        self.recurso.save(update_fields=["name"])
        url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/"
        )

        response = self.client.get(url)

        self.assertContains(response, self.recurso.name)
        self.assertContains(response, 'class="learn-card__name"')

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
        self.assertContains(response, 'class="learn-breadcrumbs"')
        self.assertContains(response, 'class="learn-breadcrumbs__current"')
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, "/static/css/learn-catalog.css?v=7")
        self.assertNotContains(response, 'class="breadcrumb-wrap"')


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
