from django.test import TestCase

from apps.content.models import Area, KnowledgeNode, Subject, Topic
from apps.content.services.node_matching_service import find_matching_block


def _node(sid, code, name, node_type):
    return KnowledgeNode.objects.create(
        semantic_id=sid, code=code, node_type=node_type, subject_abbr="MAT", name=name,
    )


class FindMatchingBlockTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        area = Area.objects.create(name="Ciencias")
        cls.subject = Subject.objects.create(name="Matemática Escolar", area=area)
        cls.bloque_fracciones = _node(
            "MAT.FRAC", "01.03", "Fracciones", KnowledgeNode.NODE_BLOQUE,
        )
        cls.bloque_conjuntos = _node(
            "MAT.CONJ", "01.02", "Conjuntos y relaciones", KnowledgeNode.NODE_BLOQUE,
        )

    def test_matches_block_by_name_similarity(self):
        topic = Topic.objects.create(subject=self.subject, name="Fracciones")
        match = find_matching_block(topic)
        self.assertEqual(match, self.bloque_fracciones)

    def test_returns_none_when_no_reasonable_match(self):
        topic = Topic.objects.create(subject=self.subject, name="Termodinámica avanzada")
        self.assertIsNone(find_matching_block(topic))
