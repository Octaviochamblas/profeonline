from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import (
    Area, KnowledgeNode, Resource, ResourceNodeSuggestion, Subject, Topic,
)

User = get_user_model()


def _node(sid, code, name, node_type):
    return KnowledgeNode.objects.create(
        semantic_id=sid, code=code, node_type=node_type, subject_abbr="MAT", name=name,
    )


class NodeSuggestionsViewsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password123",
        )
        self.student = User.objects.create_user(username="alumno", password="password123")

        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        topic = Topic.objects.create(subject=subject, name="Fracciones")
        self.resource = Resource.objects.create(title="Fracción propia", topic=topic, is_published=True)
        self.node = _node("MAT.A", "01.03.01.01", "Fracción propia", KnowledgeNode.NODE_RECURSO)
        self.other_node = _node("MAT.B", "01.03.01.02", "Fracción impropia", KnowledgeNode.NODE_RECURSO)
        self.suggestion = ResourceNodeSuggestion.objects.create(
            resource=self.resource, node=self.node, status=ResourceNodeSuggestion.STATUS_SUGERIDO,
        )

    def test_review_requires_staff(self):
        self.client.login(username="alumno", password="password123")
        response = self.client.get(reverse("content:node_suggestions_review"))
        self.assertEqual(response.status_code, 302)

    def test_review_lists_pending_suggestions(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("content:node_suggestions_review"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fracción propia")

    def test_confirm_automatic_suggestion(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(
            reverse("content:confirm_node_suggestion", args=[self.suggestion.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.suggestion.refresh_from_db()
        self.assertEqual(self.suggestion.status, ResourceNodeSuggestion.STATUS_CONFIRMADO)
        self.assertEqual(self.suggestion.origen, ResourceNodeSuggestion.ORIGEN_IA)
        self.assertIsNotNone(self.suggestion.confirmed_at)

    def test_confirm_manual_override(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(
            reverse("content:confirm_node_suggestion", args=[self.suggestion.pk]),
            {"node_id": self.other_node.pk},
        )
        self.assertEqual(response.status_code, 200)
        self.suggestion.refresh_from_db()
        self.assertEqual(self.suggestion.node, self.other_node)
        self.assertEqual(self.suggestion.origen, ResourceNodeSuggestion.ORIGEN_MANUAL)

    def test_discard_suggestion(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(
            reverse("content:discard_node_suggestion", args=[self.suggestion.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.suggestion.refresh_from_db()
        self.assertEqual(self.suggestion.status, ResourceNodeSuggestion.STATUS_DESCARTADO)

    def test_node_options_filters_by_query(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("content:node_options"), {"q": "impropia"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["nodes"]), 1)
        self.assertIn("Fracción impropia", data["nodes"][0]["label"])

    def test_node_options_empty_query_returns_empty(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("content:node_options"))
        self.assertEqual(response.json()["nodes"], [])
