from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Area, KnowledgeNode, Subject, Topic

User = get_user_model()


def _node(sid, code, name, node_type):
    return KnowledgeNode.objects.create(
        semantic_id=sid, code=code, node_type=node_type, subject_abbr="MAT", name=name,
    )


class TopicNodeLinksViewsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password123",
        )
        self.student = User.objects.create_user(username="alumno", password="password123")

        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        self.topic = Topic.objects.create(subject=subject, name="Fracciones")
        self.node = _node("MAT.A", "01.03", "Fracciones", KnowledgeNode.NODE_BLOQUE)
        self.other_node = _node("MAT.B", "01.02", "Conjuntos", KnowledgeNode.NODE_BLOQUE)

    def test_review_requires_staff(self):
        self.client.login(username="alumno", password="password123")
        response = self.client.get(reverse("content:topic_node_links_review"))
        self.assertEqual(response.status_code, 302)

    def test_review_lists_topics_with_suggestion(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("content:topic_node_links_review"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fracciones")
        self.assertContains(response, "Sugerencia automática")

    def test_set_topic_node_link(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(
            reverse("content:set_topic_node_link", args=[self.topic.pk]),
            {"node_id": self.node.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.related_node, self.node)

    def test_set_topic_node_link_accepts_tema(self):
        tema = _node("MAT.TEMA", "01.03.01", "Fracciones básicas", KnowledgeNode.NODE_TEMA)
        self.client.login(username="admin", password="password123")
        response = self.client.post(
            reverse("content:set_topic_node_link", args=[self.topic.pk]),
            {"node_id": tema.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.related_node, tema)

    def test_clear_topic_node_link(self):
        self.topic.related_node = self.node
        self.topic.save()
        self.client.login(username="admin", password="password123")
        response = self.client.post(
            reverse("content:clear_topic_node_link", args=[self.topic.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.topic.refresh_from_db()
        self.assertIsNone(self.topic.related_node)

    def test_node_options_filters_by_query(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("content:node_options"), {"q": "conjuntos"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["nodes"]), 1)
        self.assertIn("Conjuntos", data["nodes"][0]["label"])

    def test_node_options_empty_query_returns_empty(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("content:node_options"))
        self.assertEqual(response.json()["nodes"], [])
