from django.test import TestCase

from apps.content.models import Area, KnowledgeNode, Resource, ResourceNodeSuggestion, Subject, Topic
from apps.content.services.node_matching_service import find_matching_block, generate_suggestion


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


class GenerateSuggestionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        cls.topic = Topic.objects.create(subject=subject, name="Fracciones")
        cls.tema = _node("MAT.FRAC.T1", "01.03.01", "Fracciones", KnowledgeNode.NODE_TEMA)

    def test_creates_sugerido_pointing_to_matched_tema(self):
        resource = Resource.objects.create(title="Qué es una fracción propia", topic=self.topic)
        suggestion = generate_suggestion(resource)
        self.assertEqual(suggestion.status, ResourceNodeSuggestion.STATUS_SUGERIDO)
        self.assertEqual(suggestion.node, self.tema)

    def test_creates_sin_bloque_when_no_topic_match(self):
        area = Area.objects.create(name="Otra")
        subject = Subject.objects.create(name="Otra materia", area=area)
        topic = Topic.objects.create(subject=subject, name="Zzz sin relación alguna")
        resource = Resource.objects.create(title="Video random", topic=topic)
        suggestion = generate_suggestion(resource)
        self.assertEqual(suggestion.status, ResourceNodeSuggestion.STATUS_SIN_BLOQUE)
        self.assertIsNone(suggestion.node)

    def test_idempotent_does_not_duplicate(self):
        resource = Resource.objects.create(title="Fracción propia", topic=self.topic)
        first = generate_suggestion(resource)
        second = generate_suggestion(resource)
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(ResourceNodeSuggestion.objects.filter(resource=resource).count(), 1)
