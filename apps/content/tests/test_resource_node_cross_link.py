from django.test import TestCase
from django.urls import reverse

from apps.content.models import (
    Area, KnowledgeNode, Resource, ResourceNodeSuggestion, Subject, Topic,
)


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
        topic = Topic.objects.create(subject=subject, name="Fracciones")
        self.resource = Resource.objects.create(
            title="Fracción propia", topic=topic, is_published=True,
        )
        self.node = _chain()

    def test_shows_cross_link_when_confirmed(self):
        ResourceNodeSuggestion.objects.create(
            resource=self.resource, node=self.node,
            status=ResourceNodeSuggestion.STATUS_CONFIRMADO,
        )
        response = self.client.get(reverse("content:resource_detail", args=[self.resource.slug]))
        self.assertContains(response, "Ver también")
        self.assertContains(response, "Fracción propia")

    def test_no_cross_link_without_confirmed_suggestion(self):
        ResourceNodeSuggestion.objects.create(
            resource=self.resource, node=self.node,
            status=ResourceNodeSuggestion.STATUS_SUGERIDO,
        )
        response = self.client.get(reverse("content:resource_detail", args=[self.resource.slug]))
        self.assertNotContains(response, "Ver también")
