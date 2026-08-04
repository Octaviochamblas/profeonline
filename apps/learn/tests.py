"""Tests de F2 — vistas de apps/learn/."""

from urllib.parse import parse_qs, urlparse

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import (
    Area,
    ItemGroup,
    KnowledgeNode,
    NodeContent,
    NodeExercise,
    NodePrerequisite,
    Resource,
    Subject,
    Topic,
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


class NodeDetailNextNodeTests(TestCase):
    def setUp(self):
        self.asig, self.eje, self.bloque, self.tema, self.recurso = _build_tree()
        self.url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/{self.recurso.slug}/"
        )

    def test_shows_next_node_button_when_sibling_exists(self):
        siguiente = KnowledgeNode.objects.create(
            semantic_id="MAT.NUM.ENTEROS_CONJUNTO.CARDINALES",
            code="02.01.01.02",
            node_type=KnowledgeNode.NODE_RECURSO,
            subject_abbr="MAT",
            name="Números cardinales",
            parent=self.tema,
            is_published=True,
        )
        response = self.client.get(self.url)
        self.assertContains(response, "resource-navigation__link--next")
        self.assertContains(response, "Números cardinales")
        self.assertContains(response, siguiente.get_absolute_url())

    def test_no_next_node_button_when_last_in_tema(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "resource-navigation__link--next")

    def test_next_node_skips_unpublished_for_anonymous(self):
        KnowledgeNode.objects.create(
            semantic_id="MAT.NUM.ENTEROS_CONJUNTO.CARDINALES",
            code="02.01.01.02",
            node_type=KnowledgeNode.NODE_RECURSO,
            subject_abbr="MAT",
            name="Números cardinales (borrador)",
            parent=self.tema,
            is_published=False,
        )
        response = self.client.get(self.url)
        self.assertNotContains(response, "resource-navigation__link--next")

    def test_shows_previous_node_button_when_sibling_exists(self):
        anterior = KnowledgeNode.objects.create(
            semantic_id="MAT.NUM.ENTEROS_CONJUNTO.PREVIO",
            code="02.01.01.00",
            node_type=KnowledgeNode.NODE_RECURSO,
            subject_abbr="MAT",
            name="Conteo básico",
            parent=self.tema,
            is_published=True,
        )
        response = self.client.get(self.url)
        self.assertContains(response, "resource-navigation__link--prev")
        self.assertContains(response, "Conteo básico")
        self.assertContains(response, anterior.get_absolute_url())

    def test_no_previous_node_button_when_first_in_tema(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "resource-navigation__link--prev")


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


class NodeAssessmentAuthTests(TestCase):
    """Login en el flujo de evaluación de nodo (bug del overlay HTMX)."""

    def setUp(self):
        self.asig, self.eje, self.bloque, self.tema, self.recurso = _build_tree()
        self.page_url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/{self.recurso.slug}/"
        )
        self.eval_url = self.page_url + "evaluar/1/"

    def test_anonymous_htmx_gets_hx_redirect_to_login(self):
        """Anónimo + HTMX: en vez de un 302 que HTMX inyecta en el overlay,
        debe devolver header HX-Redirect para forzar navegación real al login,
        con next = la página del recurso (desde HX-Current-URL)."""
        response = self.client.get(
            self.eval_url,
            HTTP_HX_REQUEST="true",
            HTTP_HX_CURRENT_URL="http://testserver" + self.page_url,
        )
        self.assertIn("HX-Redirect", response)
        location = response["HX-Redirect"]
        self.assertIn("/cuentas/login/", location)
        next_val = parse_qs(urlparse(location).query).get("next", [""])[0]
        self.assertEqual(next_val, self.page_url)

    def test_anonymous_full_page_still_redirects_to_login(self):
        """Petición normal (no HTMX) conserva el redirect 302 clásico."""
        response = self.client.get(self.eval_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/cuentas/login/", response["Location"])


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


class NodeDetailCrossLinkTests(TestCase):
    """Un Topic legacy se vincula una sola vez a un nodo; todos sus videos
    (y la página del nodo) heredan ese enlace."""

    def setUp(self):
        *_, self.node = _build_tree()
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        self.topic = Topic.objects.create(subject=subject, name="Fracciones")
        self.resource = Resource.objects.create(
            title="Video de fracción propia", topic=self.topic, is_published=True, slug="video-fraccion-propia",
        )

    def test_shows_cross_link_when_topic_linked(self):
        self.topic.related_node = self.node
        self.topic.save()
        response = self.client.get(f"/aprender/{self.node.slug}/")
        self.assertContains(response, "Ver material Audiovisual")
        self.assertContains(response, "Fracciones")

    def test_no_cross_link_when_topic_unlinked(self):
        response = self.client.get(f"/aprender/{self.node.slug}/")
        self.assertNotContains(response, "Ver material Audiovisual")


class NodeListCrossLinkTests(TestCase):
    """Un Tema del árbol nuevo puede recibir el link de varios Topics legacy."""

    def setUp(self):
        *_, self.tema, _recurso = _build_tree()
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        self.topic_a = Topic.objects.create(subject=subject, name="Enteros")
        self.topic_b = Topic.objects.create(subject=subject, name="Orden de enteros")

    def test_lists_all_topics_linked_to_the_tema(self):
        self.topic_a.related_node = self.tema
        self.topic_a.save()
        self.topic_b.related_node = self.tema
        self.topic_b.save()
        response = self.client.get(self.tema.get_absolute_url())
        self.assertContains(response, "Ver material Audiovisual")
        self.assertContains(response, "Enteros")
        self.assertContains(response, "Orden de enteros")

    def test_no_cross_link_when_no_topic_linked(self):
        response = self.client.get(self.tema.get_absolute_url())
        self.assertNotContains(response, "Ver material Audiovisual")

    def test_lists_directly_linked_resource_alongside_topics(self):
        self.topic_a.related_node = self.tema
        self.topic_a.save()
        resource = Resource.objects.create(
            title="Video puntual sobre enteros",
            topic=self.topic_b,
            is_published=True,
            related_node=self.tema,
        )
        response = self.client.get(self.tema.get_absolute_url())
        self.assertContains(response, "Ver material Audiovisual")
        self.assertContains(response, "Enteros")
        self.assertContains(response, "Video puntual sobre enteros")


class NodeEjemploMultipleChoiceRenderTests(TestCase):
    def setUp(self):
        self.asig, self.eje, self.bloque, self.tema, self.recurso = _build_tree()
        self.url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/{self.recurso.slug}/"
        )

    def test_ejemplo_with_alternativas_renders_as_multiple_choice(self):
        NodeContent.objects.create(
            node=self.recurso,
            estado=NodeContent.ESTADO_PUBLICADO,
            ejemplos=[
                {
                    "titulo": "Ejemplo 1",
                    "enunciado": "¿Cuál es el sucesor de 4?",
                    "alternativas": ["5", "3", "4"],
                    "respuesta": "5",
                    "solucion_pasos": ["4 + 1 = 5."],
                }
            ],
        )
        response = self.client.get(self.url)
        self.assertContains(response, 'data-format="multiple_choice"')
        self.assertContains(response, 'data-answer="5"')
        self.assertContains(response, "¿Cuál es el sucesor de 4?")
        self.assertNotContains(response, 'class="ex-submit">Ver solución')

    def test_ejemplo_without_alternativas_keeps_open_answer(self):
        NodeContent.objects.create(
            node=self.recurso,
            estado=NodeContent.ESTADO_PUBLICADO,
            ejemplos=[
                {
                    "titulo": "Ejemplo 1",
                    "enunciado": "Demuestra que 4 es par.",
                    "solucion_pasos": ["4 / 2 = 2, resto 0."],
                }
            ],
        )
        response = self.client.get(self.url)
        self.assertContains(response, 'data-format="open_answer"')
        self.assertContains(response, "Ver solución")


class NodeCheckpointRenderTests(TestCase):
    def setUp(self):
        self.asig, self.eje, self.bloque, self.tema, self.recurso = _build_tree()
        self.url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/{self.recurso.slug}/"
        )

    def test_no_checkpoints_no_section(self):
        NodeContent.objects.create(node=self.recurso, estado=NodeContent.ESTADO_PUBLICADO)
        response = self.client.get(self.url)
        self.assertNotContains(response, "Comprueba tu avance")

    def test_checkpoint_after_formal_explanation_renders_with_choices(self):
        NodeContent.objects.create(
            node=self.recurso,
            estado=NodeContent.ESTADO_PUBLICADO,
            checkpoints=[
                {
                    "placement": "after_explicacion_formal",
                    "question": "¿Cuál es el opuesto de -5?",
                    "choices": [
                        {"text": "5", "is_correct": True},
                        {"text": "-5", "is_correct": False},
                        {"text": "0", "is_correct": False},
                        {"text": "10", "is_correct": False},
                    ],
                    "explanation": "La correcta es 5.",
                    "reinforcement_section": "Explicación formal",
                },
            ],
        )
        response = self.client.get(self.url)
        self.assertContains(response, "Comprueba tu avance")
        self.assertContains(response, "¿Cuál es el opuesto de -5?")
        self.assertContains(response, 'data-answer="5"')
