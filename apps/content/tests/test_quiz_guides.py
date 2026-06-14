"""Tests de las guías de referencia (QuizGuide) y su uso en la generación."""

from django.test import TestCase

from apps.content.models import QuizGuide, Resource, Subject, Topic
from apps.content.services.ai_generation_service import _build_prompt
from apps.content.services import guide_service


class GuideServiceTests(TestCase):

    def test_normalize_text_compacta_y_recorta(self):
        raw = "Línea  1   con   espacios\r\n\n\n\nLínea 2\t\tcon   tabs   "
        out = guide_service.normalize_text(raw, max_chars=20)
        self.assertNotIn("   ", out)          # sin espacios triples
        self.assertNotIn("\n\n\n", out)       # sin 3+ saltos
        self.assertLessEqual(len(out), 20)    # respeta el tope

    def test_extract_guide_text_txt(self):
        data = "Ejercicio 1: resuelve 2x+3=7".encode("utf-8")
        self.assertEqual(
            guide_service.extract_guide_text(data, "guia.txt"),
            "Ejercicio 1: resuelve 2x+3=7",
        )

    def test_extract_guide_text_acepta_str(self):
        self.assertEqual(guide_service.extract_guide_text("texto directo"), "texto directo")


class GuideResolutionTests(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(name="Matemáticas")
        self.topic = Topic.objects.create(name="Álgebra", subject=self.subject)
        self.resource = Resource.objects.create(
            title="Ecuaciones lineales",
            subject=self.subject,
            topic=self.topic,
            description="Resolución de ecuaciones.",
            content="Una ecuación lineal...",
            is_published=True,
        )

    def _guide(self, title, text="Ejercicio tipo: despeja la incógnita."):
        return QuizGuide.objects.create(title=title, content_text=text)

    def test_resuelve_por_vinculo_directo(self):
        g = self._guide("Guía directa")
        g.resources.add(self.resource)
        ids = list(guide_service.guides_for_resource(self.resource).values_list("id", flat=True))
        self.assertEqual(ids, [g.id])

    def test_resuelve_por_tema_y_asignatura(self):
        g_topic = self._guide("Guía por tema")
        g_topic.topics.add(self.topic)
        g_subject = self._guide("Guía por asignatura")
        g_subject.subjects.add(self.subject)
        ids = set(guide_service.guides_for_resource(self.resource).values_list("id", flat=True))
        self.assertEqual(ids, {g_topic.id, g_subject.id})

    def test_ignora_guias_inactivas(self):
        g = self._guide("Inactiva")
        g.resources.add(self.resource)
        g.is_active = False
        g.save()
        self.assertEqual(guide_service.guides_for_resource(self.resource).count(), 0)

    def test_build_reference_block_combina_y_recorta(self):
        g1 = self._guide("G1", "AAAA " * 50)
        g1.resources.add(self.resource)
        g2 = self._guide("G2", "BBBB " * 50)
        g2.topics.add(self.topic)
        block = guide_service.build_reference_block(self.resource, max_chars=120)
        self.assertIn("[G1]", block)
        self.assertLessEqual(len(block), 200)  # cota holgada: 120 de texto + encabezados

    def test_build_reference_block_vacio_sin_guias(self):
        self.assertEqual(guide_service.build_reference_block(self.resource), "")

    def test_prompt_incluye_bloque_de_guia(self):
        """El prompt inyecta la guía con la instrucción de imitar el estilo."""
        prompt = _build_prompt(
            self.resource, level=1, mode="preparacion", count=3,
            reference_guides="Ejercicio modelo: factoriza x^2-1.",
        )
        self.assertIn("GUÍA(S) DE REFERENCIA", prompt)
        self.assertIn("factoriza x^2-1", prompt)


class ImportQuizGuideCommandTests(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(name="Física")

    def test_import_desde_texto_y_vincula_asignatura(self):
        from io import StringIO

        from django.core.management import call_command

        call_command(
            "import_quiz_guide",
            title="Guía PAES",
            text="Ejercicio tipo: calcula la velocidad media del móvil.",
            subjects=[self.subject.slug],
            stdout=StringIO(), stderr=StringIO(),
        )

        guide = QuizGuide.objects.get(title="Guía PAES")
        self.assertIn(self.subject, list(guide.subjects.all()))
        self.assertIn("velocidad", guide.content_text)
