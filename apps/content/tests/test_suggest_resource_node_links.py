from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from apps.content.models import (
    Area, KnowledgeNode, Resource, ResourceNodeSuggestion, Subject, Topic,
)


def _node(sid, code, name, node_type):
    return KnowledgeNode.objects.create(
        semantic_id=sid, code=code, node_type=node_type, subject_abbr="MAT", name=name,
    )


class SuggestResourceNodeLinksCommandTests(TestCase):
    def setUp(self):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        self.topic = Topic.objects.create(subject=subject, name="Fracciones")
        _node("MAT.FRAC", "01.03", "Fracciones", KnowledgeNode.NODE_BLOQUE)
        _node("MAT.FRAC.PROPIA", "01.03.01", "Fracción propia", KnowledgeNode.NODE_RECURSO)

    def test_processes_unpublished_resources_only(self):
        Resource.objects.create(title="Borrador", topic=self.topic, is_published=False)
        call_command("suggest_resource_node_links", stdout=StringIO())
        self.assertEqual(ResourceNodeSuggestion.objects.count(), 0)

    def test_skips_resources_with_existing_suggestion(self):
        resource = Resource.objects.create(title="Fracción propia", topic=self.topic, is_published=True)
        ResourceNodeSuggestion.objects.create(resource=resource, node=None, status="sin_bloque")
        call_command("suggest_resource_node_links", stdout=StringIO())
        self.assertEqual(ResourceNodeSuggestion.objects.filter(resource=resource).count(), 1)

    @patch("apps.content.services.node_matching_service.call_ai_structured_json")
    def test_generates_suggestion_for_new_published_resource(self, mock_call):
        mock_call.side_effect = ValueError("sin llaves en test")
        resource = Resource.objects.create(title="Fracción propia", topic=self.topic, is_published=True)
        out = StringIO()
        call_command("suggest_resource_node_links", stdout=out)
        self.assertEqual(ResourceNodeSuggestion.objects.filter(resource=resource).count(), 1)
        self.assertIn("Sugerencias generadas: 1", out.getvalue())

    def test_continues_after_error_in_one_resource(self):
        ok_resource = Resource.objects.create(title="Fracción propia", topic=self.topic, is_published=True)
        broken_resource = Resource.objects.create(title="Otra", topic=self.topic, is_published=True)

        import apps.content.services.node_matching_service as svc
        original = svc.generate_suggestion

        def flaky(resource):
            if resource.pk == broken_resource.pk:
                raise RuntimeError("fallo simulado")
            return original(resource)

        with patch("apps.content.management.commands.suggest_resource_node_links.generate_suggestion", side_effect=flaky):
            err = StringIO()
            call_command("suggest_resource_node_links", stdout=StringIO(), stderr=err)

        self.assertEqual(ResourceNodeSuggestion.objects.filter(resource=ok_resource).count(), 1)
        self.assertEqual(ResourceNodeSuggestion.objects.filter(resource=broken_resource).count(), 0)
        self.assertIn("fallo simulado", err.getvalue())
