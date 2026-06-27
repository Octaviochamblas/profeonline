import shutil
import tempfile
from io import StringIO
from pathlib import Path

import yaml
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from apps.content.models import KnowledgeNode, NodePrerequisite


def _node(sid, code, name="N"):
    return KnowledgeNode.objects.create(
        semantic_id=sid,
        code=code,
        node_type=KnowledgeNode.NODE_RECURSO,
        subject_abbr="MAT",
        name=name,
    )


class LoadPrerequisitesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.a = _node("MAT.A", "01.01.01.01", "A")
        cls.b = _node("MAT.B", "01.01.01.02", "B")
        cls.c = _node("MAT.C", "01.01.01.03", "C")

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _run(self, edges):
        path = Path(self.tmpdir) / "dag.yaml"
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump({"prerequisitos": edges}, f)
        call_command(
            "load_prerequisites", file=str(path), stdout=StringIO(), stderr=StringIO()
        )

    def test_happy_path(self):
        self._run([{"node": "MAT.A", "requires": "MAT.B", "kind": "requerido"}])
        pr = NodePrerequisite.objects.get()
        self.assertEqual(pr.node, self.a)
        self.assertEqual(pr.requires, self.b)
        self.assertEqual(pr.kind, NodePrerequisite.KIND_REQUERIDO)

    def test_default_kind_and_min_mastery(self):
        self._run([{"node": "MAT.A", "requires": "MAT.B"}])
        pr = NodePrerequisite.objects.get()
        self.assertEqual(pr.kind, NodePrerequisite.KIND_REQUERIDO)
        self.assertEqual(pr.min_mastery, 0.75)

    def test_idempotent(self):
        edges = [{"node": "MAT.A", "requires": "MAT.B"}]
        self._run(edges)
        self._run(edges)
        self.assertEqual(NodePrerequisite.objects.count(), 1)

    def test_cycle_aborts_without_saving(self):
        with self.assertRaises(CommandError):
            self._run(
                [
                    {"node": "MAT.A", "requires": "MAT.B"},
                    {"node": "MAT.B", "requires": "MAT.A"},
                ]
            )
        self.assertEqual(NodePrerequisite.objects.count(), 0)

    def test_longer_cycle_aborts(self):
        with self.assertRaises(CommandError):
            self._run(
                [
                    {"node": "MAT.A", "requires": "MAT.B"},
                    {"node": "MAT.B", "requires": "MAT.C"},
                    {"node": "MAT.C", "requires": "MAT.A"},
                ]
            )
        self.assertEqual(NodePrerequisite.objects.count(), 0)

    def test_self_reference_aborts(self):
        with self.assertRaises(CommandError):
            self._run([{"node": "MAT.A", "requires": "MAT.A"}])
        self.assertEqual(NodePrerequisite.objects.count(), 0)

    def test_missing_semantic_id_skipped_not_fatal(self):
        self._run([{"node": "MAT.A", "requires": "MAT.NOEXISTE"}])
        self.assertEqual(NodePrerequisite.objects.count(), 0)
