from django.test import TestCase

from apps.content.models import KnowledgeNode, NodeContent


class NodeContentNewFieldsTests(TestCase):
    def setUp(self):
        self.node = KnowledgeNode.objects.create(
            semantic_id="MAT.TEST.NODO",
            code="99.99.99.99",
            node_type=KnowledgeNode.NODE_RECURSO,
            subject_abbr="MAT",
            name="Nodo de prueba",
            is_published=True,
        )

    def test_new_fields_default_to_empty(self):
        content = NodeContent.objects.create(node=self.node)

        self.assertEqual(content.resumen_inicial, "")
        self.assertEqual(content.explicacion_simple, "")
        self.assertEqual(content.explicacion_formal, "")
        self.assertEqual(content.definiciones_clave, "")
        self.assertEqual(content.propiedades_relaciones, "")
        self.assertEqual(content.ejemplo_guiado, {})
        self.assertEqual(content.errores_correccion, "")
        self.assertEqual(content.al_terminar_debes_poder, "")
        self.assertEqual(content.checkpoints, [])

    def test_new_fields_persist_after_save(self):
        content = NodeContent.objects.create(
            node=self.node,
            resumen_inicial="Resumen de apertura.",
            explicacion_simple="En palabras simples.",
            explicacion_formal="Definición formal.",
            definiciones_clave="Término: definición.",
            propiedades_relaciones="Propiedad: enunciado.",
            ejemplo_guiado={"enunciado": "Calcula X.", "pasos": ["Paso 1", "Paso 2"]},
            errores_correccion="Error común: por qué está mal y cómo corregirlo.",
            al_terminar_debes_poder="Resolver el procedimiento completo.",
            checkpoints=[
                {
                    "placement": "after_explicacion_formal",
                    "question": "¿Pregunta?",
                    "choices": [
                        {"text": "A", "is_correct": True},
                        {"text": "B", "is_correct": False},
                        {"text": "C", "is_correct": False},
                        {"text": "D", "is_correct": False},
                    ],
                    "explanation": "La correcta es A porque...",
                    "reinforcement_section": "Explicación formal",
                },
            ],
        )
        content.refresh_from_db()

        self.assertEqual(content.resumen_inicial, "Resumen de apertura.")
        self.assertEqual(content.ejemplo_guiado["pasos"], ["Paso 1", "Paso 2"])
        self.assertEqual(len(content.checkpoints), 1)
        self.assertEqual(content.checkpoints[0]["placement"], "after_explicacion_formal")
