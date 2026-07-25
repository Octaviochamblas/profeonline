from django.test import TestCase

from apps.content.models import (
    Area,
    KnowledgeNode,
    Resource,
    ResourceNodeSuggestion,
    Subject,
    Topic,
)


def _node(sid, code, name="N", node_type=KnowledgeNode.NODE_RECURSO):
    return KnowledgeNode.objects.create(
        semantic_id=sid, code=code, node_type=node_type, subject_abbr="MAT", name=name,
    )


class ResourceNodeSuggestionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        topic = Topic.objects.create(subject=subject, name="Fracciones")
        cls.resource = Resource.objects.create(title="Video de fracciones", topic=topic)
        cls.node = _node("MAT.A", "01.01.01.01", "Fracción propia")

    def test_creates_confirmed_suggestion(self):
        suggestion = ResourceNodeSuggestion.objects.create(
            resource=self.resource,
            node=self.node,
            status=ResourceNodeSuggestion.STATUS_CONFIRMADO,
            origen=ResourceNodeSuggestion.ORIGEN_IA,
            ai_rationale="Coincide en tema y título.",
        )
        self.assertEqual(self.resource.node_suggestion, suggestion)
        self.assertEqual(self.node.resource_suggestions.first(), suggestion)
        self.assertIn("Video de fracciones", str(suggestion))

    def test_node_can_be_null_for_sin_bloque(self):
        suggestion = ResourceNodeSuggestion.objects.create(
            resource=self.resource, node=None, status=ResourceNodeSuggestion.STATUS_SIN_BLOQUE,
        )
        self.assertIsNone(suggestion.node)
        self.assertIn("sin bloque", str(suggestion))

    def test_one_suggestion_per_resource(self):
        ResourceNodeSuggestion.objects.create(resource=self.resource, node=self.node)
        with self.assertRaises(Exception):
            ResourceNodeSuggestion.objects.create(resource=self.resource, node=self.node)
