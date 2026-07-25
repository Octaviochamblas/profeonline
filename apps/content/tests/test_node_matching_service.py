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


from unittest.mock import patch

from apps.content.models import ResourceNodeSuggestion
from apps.content.services.node_matching_service import (
    corroborate_with_ai,
    generate_suggestion,
)


class CorroborateWithAiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        topic = Topic.objects.create(subject=subject, name="Fracciones")
        cls.resource = Resource.objects.create(title="Fracción impropia explicada", topic=topic)
        cls.candidate = _node("MAT.A", "01.03.01.01", "Fracción propia", KnowledgeNode.NODE_RECURSO)
        cls.alt = _node("MAT.B", "01.03.01.02", "Fracción impropia", KnowledgeNode.NODE_RECURSO)

    @patch("apps.content.services.node_matching_service.call_ai_structured_json")
    def test_ai_confirms_candidate(self, mock_call):
        mock_call.return_value = {
            "chosen_id": self.candidate.id, "corrected": False, "rationale": "Coincide bien.",
        }
        result = corroborate_with_ai(self.resource, self.candidate, [self.alt])
        self.assertEqual(result["node"], self.candidate)
        self.assertFalse(result["ai_corrigio"])
        self.assertEqual(result["ai_rationale"], "Coincide bien.")

    @patch("apps.content.services.node_matching_service.call_ai_structured_json")
    def test_ai_corrects_to_alternative(self, mock_call):
        mock_call.return_value = {
            "chosen_id": self.alt.id, "corrected": True, "rationale": "El título dice impropia.",
        }
        result = corroborate_with_ai(self.resource, self.candidate, [self.alt])
        self.assertEqual(result["node"], self.alt)
        self.assertTrue(result["ai_corrigio"])

    @patch("apps.content.services.node_matching_service.call_ai_structured_json")
    def test_returns_none_when_ai_unavailable(self, mock_call):
        mock_call.side_effect = ValueError("sin llaves configuradas")
        result = corroborate_with_ai(self.resource, self.candidate, [self.alt])
        self.assertIsNone(result)


class GenerateSuggestionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        area = Area.objects.create(name="Ciencias")
        subject = Subject.objects.create(name="Matemática Escolar", area=area)
        cls.topic = Topic.objects.create(subject=subject, name="Fracciones")
        cls.bloque = _node("MAT.FRAC", "01.03", "Fracciones", KnowledgeNode.NODE_BLOQUE)
        cls.propia = _node("MAT.FRAC.PROPIA", "01.03.01.01", "Fracción propia", KnowledgeNode.NODE_RECURSO)

    @patch("apps.content.services.node_matching_service.call_ai_structured_json")
    def test_creates_sugerido_with_ai_confirmation(self, mock_call):
        mock_call.return_value = {
            "chosen_id": self.propia.id, "corrected": False, "rationale": "Calza.",
        }
        resource = Resource.objects.create(title="Qué es una fracción propia", topic=self.topic)
        suggestion = generate_suggestion(resource)
        self.assertEqual(suggestion.status, ResourceNodeSuggestion.STATUS_SUGERIDO)
        self.assertEqual(suggestion.node, self.propia)
        self.assertEqual(suggestion.origen, ResourceNodeSuggestion.ORIGEN_IA)

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
        with patch(
            "apps.content.services.node_matching_service.call_ai_structured_json",
            return_value={"chosen_id": self.propia.id, "corrected": False, "rationale": "x"},
        ):
            first = generate_suggestion(resource)
            second = generate_suggestion(resource)
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(ResourceNodeSuggestion.objects.filter(resource=resource).count(), 1)
