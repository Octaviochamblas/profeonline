"""Tests de F2 — NodeContent, NodeMedia, load_node_content."""

import tempfile
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

from apps.content.models import KnowledgeNode, NodeContent, NodeMedia


def _make_node(semantic_id="MAT.NUM.ENTEROS_CONJUNTO.NATURALES", is_published=True):
    parent = KnowledgeNode.objects.create(
        semantic_id="MAT",
        code="MAT",
        node_type=KnowledgeNode.NODE_ASIGNATURA,
        subject_abbr="MAT",
        name="Matemáticas",
        is_published=True,
    )
    node = KnowledgeNode.objects.create(
        semantic_id=semantic_id,
        code="02.01.01.01",
        node_type=KnowledgeNode.NODE_RECURSO,
        subject_abbr="MAT",
        name="Números naturales",
        parent=parent,
        is_published=is_published,
    )
    return node


SAMPLE_YAML = """\
semantic_id: MAT.NUM.ENTEROS_CONJUNTO.NATURALES
objetivo: "Identificar los números naturales."
explicacion: |
  Los naturales son $\\mathbb{N} = \\{1, 2, 3, \\ldots\\}$.
procedimiento:
  - "Paso 1: verifica que sea positivo."
  - "Paso 2: verifica que sea entero."
ejemplos:
  - titulo: "Ejemplo 1"
    enunciado: "¿Es 7 natural?"
    solucion_pasos:
      - "7 > 0 y es entero: sí."
errores_frecuentes:
  - "Incluir el cero."
fuente: "Moraleja p.21"
estado: publicado
media:
  - kind: video_youtube
    video_kind: explicacion
    url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    order: 0
"""


class NodeContentModelTests(TestCase):
    def test_node_content_creates_and_is_draft_by_default(self):
        node = _make_node()
        content = NodeContent.objects.create(node=node, objetivo="Objetivo de prueba")
        self.assertTrue(content.is_draft)
        self.assertEqual(content.estado, NodeContent.ESTADO_BORRADOR)

    def test_node_content_published(self):
        node = _make_node()
        content = NodeContent.objects.create(
            node=node, estado=NodeContent.ESTADO_PUBLICADO
        )
        self.assertFalse(content.is_draft)

    def test_node_content_o2o_unique(self):
        from django.db import IntegrityError

        node = _make_node()
        NodeContent.objects.create(node=node)
        with self.assertRaises(IntegrityError):
            NodeContent.objects.create(node=node)

    def test_node_media_ordering(self):
        node = _make_node()
        NodeMedia.objects.create(
            node=node, kind=NodeMedia.KIND_VIDEO_YOUTUBE, order=2
        )
        NodeMedia.objects.create(
            node=node, kind=NodeMedia.KIND_VIDEO_YOUTUBE, order=1
        )
        orders = list(node.media.values_list("order", flat=True))
        self.assertEqual(orders, [1, 2])


class LoadNodeContentCommandTests(TestCase):
    def _write(self, dirpath, name, content):
        path = Path(dirpath) / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_creates_content_and_media(self):
        _make_node()
        with tempfile.TemporaryDirectory() as d:
            self._write(d, "naturales.yaml", SAMPLE_YAML)
            call_command("load_node_content", dir=d, verbosity=0)

        self.assertEqual(NodeContent.objects.count(), 1)
        content = NodeContent.objects.first()
        self.assertEqual(content.objetivo, "Identificar los números naturales.")
        self.assertEqual(content.estado, NodeContent.ESTADO_PUBLICADO)
        self.assertEqual(len(content.procedimiento), 2)
        self.assertEqual(len(content.ejemplos), 1)
        self.assertEqual(NodeMedia.objects.count(), 1)
        media = NodeMedia.objects.first()
        self.assertEqual(media.video_kind, NodeMedia.VIDEO_KIND_EXPLICACION)

    def test_idempotent(self):
        _make_node()
        with tempfile.TemporaryDirectory() as d:
            self._write(d, "naturales.yaml", SAMPLE_YAML)
            call_command("load_node_content", dir=d, verbosity=0)
            call_command("load_node_content", dir=d, verbosity=0)

        self.assertEqual(NodeContent.objects.count(), 1)
        self.assertEqual(NodeMedia.objects.count(), 1)

    def test_warns_on_unknown_semantic_id(self):
        yaml_unknown = "semantic_id: MAT.INEXISTENTE.NODO\nobjetivo: test\n"
        with tempfile.TemporaryDirectory() as d:
            self._write(d, "unknown.yaml", yaml_unknown)
            import io
            from contextlib import redirect_stderr

            buf = io.StringIO()
            call_command("load_node_content", dir=d, verbosity=0, stderr=buf)

        self.assertEqual(NodeContent.objects.count(), 0)

    def test_single_file_option(self):
        _make_node()
        with tempfile.TemporaryDirectory() as d:
            path = self._write(d, "naturales.yaml", SAMPLE_YAML)
            call_command("load_node_content", file=str(path), verbosity=0)

        self.assertEqual(NodeContent.objects.count(), 1)
