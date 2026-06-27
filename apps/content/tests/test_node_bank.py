import json
import shutil
import tempfile
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.content.models import ItemGroup, KnowledgeNode, NodeExercise
from apps.content.models.node_bank import (
    STANDARD_ITEM_GROUPS,
    ensure_standard_item_groups,
)


def _make_node(semantic_id, code, name="Recurso"):
    return KnowledgeNode.objects.create(
        semantic_id=semantic_id,
        code=code,
        node_type=KnowledgeNode.NODE_RECURSO,
        subject_abbr="MAT",
        name=name,
    )


class ItemGroupModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.node = _make_node("MAT.NUM.TEST.UNO", "01.01.01.01")

    def test_unique_code_per_node(self):
        ItemGroup.objects.create(
            node=self.node,
            code="conceptuales",
            title="Conceptuales",
            level=ItemGroup.LEVEL_COMPRENDER,
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ItemGroup.objects.create(
                    node=self.node,
                    code="conceptuales",
                    title="Otra",
                    level=ItemGroup.LEVEL_COMPRENDER,
                )

    def test_same_code_different_nodes_ok(self):
        other = _make_node("MAT.NUM.TEST.DOS", "01.01.01.02", name="Dos")
        ItemGroup.objects.create(
            node=self.node, code="conceptuales", title="A", level=ItemGroup.LEVEL_COMPRENDER
        )
        ItemGroup.objects.create(
            node=other, code="conceptuales", title="B", level=ItemGroup.LEVEL_COMPRENDER
        )
        self.assertEqual(ItemGroup.objects.filter(code="conceptuales").count(), 2)


class StandardItemGroupsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.node = _make_node("MAT.NUM.TEST.TPL", "01.01.02.01", name="Plantilla")

    def test_creates_seven_groups(self):
        groups = ensure_standard_item_groups(self.node)
        self.assertEqual(len(groups), len(STANDARD_ITEM_GROUPS))
        self.assertEqual(self.node.item_groups.count(), 7)

    def test_idempotent(self):
        ensure_standard_item_groups(self.node)
        ensure_standard_item_groups(self.node)
        self.assertEqual(self.node.item_groups.count(), 7)

    def test_order_follows_progression(self):
        ensure_standard_item_groups(self.node)
        codes = list(
            self.node.item_groups.order_by("order").values_list("code", flat=True)
        )
        self.assertEqual(codes[0], "conceptuales")
        self.assertEqual(codes[-1], "mixto")


class NodeExerciseModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.node = _make_node("MAT.NUM.TEST.EX", "01.01.03.01", name="Ejercicios")
        cls.group = ItemGroup.objects.create(
            node=cls.node,
            code="procedimiento_basico",
            title="Básicos",
            level=ItemGroup.LEVEL_RESOLVER,
        )

    def test_defaults(self):
        ex = NodeExercise.objects.create(
            node=self.node, item_group=self.group, prompt="¿Cuánto es 2+2?"
        )
        self.assertEqual(ex.status, NodeExercise.STATUS_DRAFT)
        self.assertEqual(ex.kind, NodeExercise.KIND_ITEM)
        self.assertEqual(ex.source_kind, NodeExercise.SOURCE_MANUAL)
        self.assertFalse(ex.is_published)

    def test_is_published_property(self):
        ex = NodeExercise.objects.create(
            node=self.node,
            item_group=self.group,
            prompt="x",
            status=NodeExercise.STATUS_PUBLISHED,
        )
        self.assertTrue(ex.is_published)

    def test_stable_id_unique_when_set(self):
        NodeExercise.objects.create(
            node=self.node, item_group=self.group, prompt="a", stable_id="EX-1"
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                NodeExercise.objects.create(
                    node=self.node, item_group=self.group, prompt="b", stable_id="EX-1"
                )

    def test_blank_stable_id_allows_many(self):
        NodeExercise.objects.create(node=self.node, item_group=self.group, prompt="a")
        NodeExercise.objects.create(node=self.node, item_group=self.group, prompt="b")
        self.assertEqual(NodeExercise.objects.filter(stable_id="").count(), 2)


class LoadExerciseBankTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.node = _make_node("MAT.NUM.FRAC.SUMA", "02.08.04.03", name="Suma fracciones")

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_jsonl(self, rows):
        path = Path(self.tmpdir) / "bank.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row) + "\n")
        return str(path)

    def _run(self, rows):
        path = self._write_jsonl(rows)
        call_command(
            "load_exercise_bank", file=path, stdout=StringIO(), stderr=StringIO()
        )

    def test_happy_path_creates_exercise_and_group_from_template(self):
        self._run(
            [
                {
                    "semantic_id": "MAT.NUM.FRAC.SUMA",
                    "item_group": "conceptuales",
                    "format": "multiple_choice",
                    "difficulty": "basica",
                    "prompt": "¿Qué hacer primero?",
                    "choices": ["A", "B"],
                    "correct_answer": "B",
                    "status": "ready",
                }
            ]
        )
        self.assertEqual(NodeExercise.objects.count(), 1)
        ex = NodeExercise.objects.get()
        self.assertEqual(ex.status, NodeExercise.STATUS_PUBLISHED)
        # ItemGroup creado desde plantilla estándar.
        self.assertEqual(ex.item_group.title, "Preguntas conceptuales")
        self.assertEqual(ex.item_group.level, ItemGroup.LEVEL_COMPRENDER)

    def test_idempotent_by_stable_id(self):
        row = {
            "semantic_id": "MAT.NUM.FRAC.SUMA",
            "item_group": "conceptuales",
            "prompt": "P",
            "correct_answer": "X",
            "status": "ready",
            "stable_id": "EX-1",
        }
        self._run([row])
        self._run([row])
        self.assertEqual(NodeExercise.objects.filter(stable_id="EX-1").count(), 1)

    def test_semantic_id_not_found_skips(self):
        self._run(
            [
                {
                    "semantic_id": "MAT.NO.EXISTE",
                    "item_group": "conceptuales",
                    "prompt": "P",
                    "correct_answer": "X",
                }
            ]
        )
        self.assertEqual(NodeExercise.objects.count(), 0)

    def test_legal_review_publishes_and_sets_flag(self):
        self._run(
            [
                {
                    "semantic_id": "MAT.NUM.FRAC.SUMA",
                    "item_group": "tipo_paes",
                    "prompt": "P",
                    "correct_answer": "X",
                    "status": "published",
                    "legal_review": True,
                }
            ]
        )
        ex = NodeExercise.objects.get()
        self.assertEqual(ex.status, NodeExercise.STATUS_PUBLISHED)
        self.assertTrue(ex.legal_review)

    def test_missing_answer_still_publishes(self):
        self._run(
            [
                {
                    "semantic_id": "MAT.NUM.FRAC.SUMA",
                    "item_group": "mixto",
                    "prompt": "P",
                    "status": "ready",
                }
            ]
        )
        self.assertEqual(
            NodeExercise.objects.get().status, NodeExercise.STATUS_PUBLISHED
        )

    def test_published_status_in_jsonl_publishes_immediately(self):
        self._run(
            [
                {
                    "semantic_id": "MAT.NUM.FRAC.SUMA",
                    "item_group": "mixto",
                    "prompt": "P",
                    "correct_answer": "X",
                    "status": "published",
                }
            ]
        )
        self.assertEqual(NodeExercise.objects.get().status, NodeExercise.STATUS_PUBLISHED)

    def test_reimport_does_not_unpublish(self):
        row = {
            "semantic_id": "MAT.NUM.FRAC.SUMA",
            "item_group": "conceptuales",
            "prompt": "P",
            "correct_answer": "X",
            "status": "ready",
            "stable_id": "EX-PUB",
        }
        self._run([row])
        NodeExercise.objects.filter(stable_id="EX-PUB").update(
            status=NodeExercise.STATUS_PUBLISHED
        )
        self._run([row])  # mismo JSONL, sigue 'ready'
        self.assertEqual(
            NodeExercise.objects.get(stable_id="EX-PUB").status,
            NodeExercise.STATUS_PUBLISHED,
        )

    def test_missing_prompt_skipped(self):
        self._run(
            [
                {
                    "semantic_id": "MAT.NUM.FRAC.SUMA",
                    "item_group": "mixto",
                    "correct_answer": "X",
                }
            ]
        )
        self.assertEqual(NodeExercise.objects.count(), 0)
