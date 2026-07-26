from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Area, KnowledgeNode, Resource, Subject, Topic

User = get_user_model()


def _chain(subject_abbr="MAT"):
    asignatura = KnowledgeNode.objects.create(
        semantic_id="MAT", code="00", node_type=KnowledgeNode.NODE_ASIGNATURA,
        subject_abbr=subject_abbr, name="Matemáticas",
    )
    eje = KnowledgeNode.objects.create(
        semantic_id="MAT.FUND", code="01", node_type=KnowledgeNode.NODE_EJE,
        subject_abbr=subject_abbr, name="Fundamentos", parent=asignatura,
    )
    bloque = KnowledgeNode.objects.create(
        semantic_id="MAT.FUND.FRAC", code="01.03", node_type=KnowledgeNode.NODE_BLOQUE,
        subject_abbr=subject_abbr, name="Fracciones", parent=eje,
    )
    tema = KnowledgeNode.objects.create(
        semantic_id="MAT.FUND.FRAC.T1", code="01.03.01", node_type=KnowledgeNode.NODE_TEMA,
        subject_abbr=subject_abbr, name="Fracciones básicas", parent=bloque,
    )
    recurso = KnowledgeNode.objects.create(
        semantic_id="MAT.FUND.FRAC.T1.PROPIA", code="01.03.01.01", node_type=KnowledgeNode.NODE_RECURSO,
        subject_abbr=subject_abbr, name="Fracción propia", parent=tema, is_published=True,
    )
    return recurso


class ResourceDetailCrossLinkTests(TestCase):
    def setUp(self):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        self.topic = Topic.objects.create(subject=subject, name="Fracciones")
        self.resource = Resource.objects.create(
            title="Fracción propia", topic=self.topic, is_published=True,
        )
        self.node = _chain()

    def test_shows_cross_link_when_topic_linked(self):
        self.topic.related_node = self.node
        self.topic.save()
        response = self.client.get(reverse("content:resource_detail", args=[self.resource.slug]))
        self.assertContains(response, "Ver también")
        self.assertContains(response, "Fracción propia")

    def test_no_cross_link_when_topic_unlinked(self):
        response = self.client.get(reverse("content:resource_detail", args=[self.resource.slug]))
        self.assertNotContains(response, "Ver también")


class VincularBotonTests(TestCase):
    def setUp(self):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        self.topic = Topic.objects.create(subject=subject, name="Fracciones")
        self.resource = Resource.objects.create(
            title="Fracción propia", topic=self.topic, is_published=True,
        )
        self.node = _chain()
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password123",
        )

    def test_shows_link_button_when_unlinked(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("content:resource_detail", args=[self.resource.slug]))
        self.assertContains(response, "Vincular a nodo de conocimiento")

    def test_button_links_to_topic_anchor(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("content:resource_detail", args=[self.resource.slug]))
        self.assertContains(response, f"vinculos-tema/#topic-{self.topic.pk}")

    def test_no_link_button_when_topic_already_linked(self):
        self.topic.related_node = self.node
        self.topic.save()
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("content:resource_detail", args=[self.resource.slug]))
        self.assertNotContains(response, "Vincular a nodo de conocimiento")

    def test_no_link_button_for_non_staff(self):
        response = self.client.get(reverse("content:resource_detail", args=[self.resource.slug]))
        self.assertNotContains(response, "Vincular a nodo de conocimiento")
