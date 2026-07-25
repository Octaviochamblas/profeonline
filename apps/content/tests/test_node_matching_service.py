from django.test import TestCase

from apps.content.models import Area, KnowledgeNode, Resource, Subject, Topic
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
        resource = Resource.objects.create(title="Suma de fracciones", topic=topic)
        match = find_matching_block(resource)
        self.assertEqual(match, self.bloque_fracciones)

    def test_returns_none_when_no_topic(self):
        resource = Resource.objects.create(title="Video suelto", topic=None)
        self.assertIsNone(find_matching_block(resource))

    def test_returns_none_when_no_reasonable_match(self):
        topic = Topic.objects.create(subject=self.subject, name="Termodinámica avanzada")
        resource = Resource.objects.create(title="Entropía y calor", topic=topic)
        self.assertIsNone(find_matching_block(resource))


from apps.content.services.node_matching_service import find_candidate_leaf_nodes


class FindCandidateLeafNodesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        cls.topic = Topic.objects.create(subject=subject, name="Fracciones")
        cls.bloque = _node("MAT.FRAC", "01.03", "Fracciones", KnowledgeNode.NODE_BLOQUE)
        cls.tema = _node("MAT.FRAC.T1", "01.03.01", "Fracciones básicas", KnowledgeNode.NODE_TEMA)
        cls.tema.parent = cls.bloque
        cls.tema.save()
        cls.propia = _node("MAT.FRAC.PROPIA", "01.03.01.01", "Fracción propia", KnowledgeNode.NODE_RECURSO)
        cls.propia.parent = cls.tema
        cls.propia.save()
        cls.impropia = _node("MAT.FRAC.IMPROPIA", "01.03.01.02", "Fracción impropia", KnowledgeNode.NODE_RECURSO)
        cls.impropia.parent = cls.tema
        cls.impropia.save()

    def test_finds_best_leaf_by_title_similarity(self):
        resource = Resource.objects.create(title="Qué es una fracción propia", topic=self.topic)
        results = find_candidate_leaf_nodes(self.bloque, resource)
        self.assertGreater(len(results), 0)
        top_node, top_score = results[0]
        self.assertEqual(top_node, self.propia)
        self.assertGreater(top_score, 0)

    def test_returns_at_most_three_candidates(self):
        resource = Resource.objects.create(title="Fracciones en general", topic=self.topic)
        results = find_candidate_leaf_nodes(self.bloque, resource)
        self.assertLessEqual(len(results), 3)

    def test_empty_when_no_leaf_descendants(self):
        bloque_vacio = _node("MAT.VACIO", "01.09", "Bloque vacío", KnowledgeNode.NODE_BLOQUE)
        resource = Resource.objects.create(title="Video huérfano", topic=self.topic)
        self.assertEqual(find_candidate_leaf_nodes(bloque_vacio, resource), [])
