from unittest.mock import MagicMock, patch
from django.contrib import messages
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from apps.content.admin import ResourceAdmin
from apps.content.models import Choice, Question, Resource, Subject, Topic
from apps.content.services.ai_generation_service import (
    _build_prompt,
    _loads_ai_json,
    generate_questions_for_resource,
)

User = get_user_model()


class LoadsAiJsonTests(TestCase):
    """El parser tolera el JSON con LaTeX (barras escapadas) y respuestas envueltas."""

    def test_parses_escaped_latex_to_literal_backslash(self):
        # En modo JSON la IA escapa las barras: "$\\frac{a}{b}$" -> "$\frac{a}{b}$".
        payload = r'[{"text": "Calcula $\\frac{a}{b}$ y $\\sqrt{x}$", "choices": []}]'
        data = _loads_ai_json(payload)
        self.assertEqual(data[0]["text"], r"Calcula $\frac{a}{b}$ y $\sqrt{x}$")

    def test_preserves_newline_separators_in_explanations(self):
        payload = r'[{"explanation": "1. Paso uno.\n2. Paso dos: $x^2$."}]'
        data = _loads_ai_json(payload)
        self.assertEqual(data[0]["explanation"], "1. Paso uno.\n2. Paso dos: $x^2$.")

    def test_strips_markdown_code_fences(self):
        payload = '```json\n[{"text": "$\\\\int_0^1 x\\\\,dx$"}]\n```'
        data = _loads_ai_json(payload)
        self.assertEqual(data[0]["text"], r"$\int_0^1 x\,dx$")

    def test_extracts_json_array_embedded_in_prose(self):
        payload = 'Aquí tienes las preguntas:\n[{"text": "$x^2$"}]\n¡Listo!'
        data = _loads_ai_json(payload)
        self.assertEqual(data[0]["text"], "$x^2$")

    def test_invalid_json_raises(self):
        from json import JSONDecodeError
        with self.assertRaises(JSONDecodeError):
            _loads_ai_json("esto no es json")


class AIGenerationTests(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(name="Matemáticas")
        self.topic = Topic.objects.create(name="Fracciones", subject=self.subject)
        self.resource = Resource.objects.create(
            title="Suma de fracciones",
            subject=self.subject,
            topic=self.topic,
            description="Aprende a sumar fracciones con el mismo y diferente denominador.",
            content="Para sumar fracciones con igual denominador se suman los numeradores...",
            is_published=True,
        )
        self.user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="password"
        )

    def test_mock_generation_math_level_1(self):
        """Verifica la generación simulada (mock) para matemáticas nivel 1."""
        questions = generate_questions_for_resource(
            resource=self.resource,
            level=1,
            mode="ambas",
            count=2,
            api_key=None,
        )

        self.assertEqual(len(questions), 2)
        for q in questions:
            self.assertEqual(q.resource, self.resource)
            self.assertEqual(q.level, 1)
            self.assertEqual(q.mode, "ambas")
            self.assertEqual(q.status, "publicada")
            self.assertTrue(q.text.startswith("[Simulado N1]"))
            self.assertTrue(len(q.explanation) > 0)

            choices = list(q.choices.all())
            self.assertEqual(len(choices), 4)
            correct_choices = [c for c in choices if c.is_correct]
            self.assertEqual(len(correct_choices), 1)

    def test_prompt_includes_latex_notation_directive(self):
        """El prompt instruye a la IA a escribir fórmulas en LaTeX (KaTeX)."""
        prompt = _build_prompt(self.resource, level=2, mode="ambas", count=3)

        self.assertIn("NOTACIÓN MATEMÁTICA", prompt)
        self.assertIn("KaTeX", prompt)
        self.assertIn("$...$", prompt)
        self.assertIn("$$...$$", prompt)
        # Ejemplo JSON con LaTeX correctamente escapado para JSON válido.
        self.assertIn(r"\\int", prompt)
        self.assertIn(r"\\frac", prompt)

    def test_prompt_includes_restructured_pedagogical_levels(self):
        """El prompt usa los tres niveles pedagógicos reestructurados."""
        prompt = _build_prompt(self.resource, level=1, mode="ambas", count=3)

        self.assertIn("Comprensión conceptual y funcional", prompt)
        self.assertIn("Dominio procedimental y resolución técnica", prompt)
        self.assertIn("Transferencia y aplicación en contextos reales", prompt)
        # Guía de distractores por nivel (rasgo de la nueva versión).
        self.assertIn("distractores", prompt)

    def test_mock_generation_science_level_3(self):
        """Verifica la generación simulada para ciencias/general nivel 3."""
        science_resource = Resource.objects.create(
            title="Fotosíntesis celular",
            subject=Subject.objects.create(name="Ciencias Naturales"),
            description="Proceso químico de conversión de luz solar en energía química.",
            content="La clorofila absorbe la luz...",
        )

        questions = generate_questions_for_resource(
            resource=science_resource,
            level=3,
            mode="evaluacion",
            count=1,
        )

        self.assertEqual(len(questions), 1)
        q = questions[0]
        self.assertEqual(q.level, 3)
        self.assertEqual(q.mode, "evaluacion")
        self.assertTrue(q.text.startswith("[Simulado N3]"))

        choices = list(q.choices.all())
        self.assertEqual(len(choices), 4)
        correct_choices = [c for c in choices if c.is_correct]
        self.assertEqual(len(correct_choices), 1)

    @patch("requests.post")
    @override_settings(GEMINI_API_KEY="fake-gemini-key")
    def test_api_generation_gemini_success(self, mock_post):
        """Verifica la generación exitosa llamando a la API de Gemini mockeada."""
        gemini_response_json = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": """
                                [
                                  {
                                    "text": "De acuerdo con el recurso, ¿cómo se suman fracciones con igual denominador?",
                                    "explanation": "Se suman los numeradores directamente y se mantiene el denominador.",
                                    "choices": [
                                      {"text": "Sumando los numeradores y manteniendo el denominador", "is_correct": true},
                                      {"text": "Sumando numeradores y denominadores", "is_correct": false},
                                      {"text": "Multiplicando cruzado", "is_correct": false},
                                      {"text": "Restando los numeradores", "is_correct": false}
                                    ]
                                  }
                                ]
                                """
                            }
                        ]
                    }
                }
            ]
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = gemini_response_json
        mock_post.return_value = mock_response

        questions = generate_questions_for_resource(
            resource=self.resource,
            level=1,
            mode="evaluacion",
            count=1,
        )

        self.assertEqual(len(questions), 1)
        q = questions[0]
        self.assertEqual(q.resource, self.resource)
        self.assertEqual(q.text, "De acuerdo con el recurso, ¿cómo se suman fracciones con igual denominador?")
        self.assertEqual(q.status, "publicada")

        choices = list(q.choices.all())
        self.assertEqual(len(choices), 4)
        correct = [c for c in choices if c.is_correct][0]
        self.assertEqual(correct.text, "Sumando los numeradores y manteniendo el denominador")

        # Verificar que el request a Gemini incluyó los parámetros esperados
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertTrue("gemini-2.5-flash" in args[0])
        self.assertIn("responseMimeType", kwargs["json"]["generationConfig"])

    @patch("requests.post")
    @override_settings(GEMINI_API_KEY="fake-gemini-key")
    def test_prompt_includes_existing_questions_to_avoid_repeats(self, mock_post):
        """El prompt enviado a la IA lista las preguntas ya existentes del recurso."""
        Question.objects.create(
            resource=self.resource,
            level=1,
            mode="preparacion",
            text="¿Cuánto es 1/2 + 1/2 expresado como entero?",
            status="publicada",
        )

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "[]"}]}}
            ]
        }
        mock_post.return_value = mock_response

        generate_questions_for_resource(
            resource=self.resource,
            level=1,
            mode="evaluacion",
            count=1,
        )

        args, kwargs = mock_post.call_args
        prompt = kwargs["json"]["contents"][0]["parts"][0]["text"]
        self.assertIn("PREGUNTAS YA EXISTENTES", prompt)
        self.assertIn("¿Cuánto es 1/2 + 1/2 expresado como entero?", prompt)

    @patch("requests.post")
    @override_settings(OPENAI_API_KEY="fake-openai-key")
    def test_api_generation_openai_success(self, mock_post):
        """Verifica la generación exitosa llamando a la API de OpenAI mockeada."""
        openai_response_json = {
            "choices": [
                {
                    "message": {
                        "content": """
                        {
                          "questions": [
                            {
                              "text": "Pregunta de prueba OpenAI",
                              "explanation": "Explicación OpenAI",
                              "choices": [
                                {"text": "A", "is_correct": true},
                                {"text": "B", "is_correct": false},
                                {"text": "C", "is_correct": false},
                                {"text": "D", "is_correct": false}
                              ]
                            }
                          ]
                        }
                        """
                    }
                }
            ]
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = openai_response_json
        mock_post.return_value = mock_response

        # Forzar que GEMINI_API_KEY no esté configurada para que use OpenAI
        with override_settings(GEMINI_API_KEY=""):
            questions = generate_questions_for_resource(
                resource=self.resource,
                level=2,
                mode="preparacion",
                count=1,
            )

        self.assertEqual(len(questions), 1)
        q = questions[0]
        self.assertEqual(q.text, "Pregunta de prueba OpenAI")
        self.assertEqual(q.explanation, "Explicación OpenAI")

        # Verificar que se llamó al endpoint de OpenAI
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://api.openai.com/v1/chat/completions")

    def test_management_command_success(self):
        """Verifica que el comando de management genere las preguntas correctamente."""
        initial_count = Question.objects.filter(resource=self.resource).count()

        call_command(
            "generate_ai_questions",
            resource=self.resource.slug,
            level=2,
            count=3,
            mode="preparacion",
        )

        final_count = Question.objects.filter(resource=self.resource).count()
        self.assertEqual(final_count, initial_count + 3)

        new_questions = Question.objects.filter(resource=self.resource, level=2, status="publicada")
        self.assertEqual(new_questions.count(), 3)

    def test_management_command_invalid_resource(self):
        """Verifica que el comando de management falle con un recurso inválido."""
        with self.assertRaises(CommandError):
            call_command(
                "generate_ai_questions",
                resource="no-existe-este-slug-123",
                level=1,
            )

    def test_admin_action_intermediate_page(self):
        """Prueba que la acción del admin devuelva la página de confirmación intermedia."""
        site = AdminSite()
        resource_admin = ResourceAdmin(Resource, site)

        # Simular request GET (sin confirmación del formulario intermedio)
        factory = RequestFactory()
        request = factory.get(reverse("admin:content_resource_changelist"))
        request.user = self.user

        # Queryset con nuestro recurso seleccionado
        queryset = Resource.objects.filter(pk=self.resource.pk)

        response = resource_admin.generar_preguntas_ia_action(request, queryset)

        # Debería retornar una TemplateResponse de confirmación
        self.assertIsNotNone(response)
        self.assertEqual(response.template_name, "admin/content/resource/generate_ai_questions_confirm.html")
        self.assertIn("queryset", response.context_data)
        self.assertEqual(list(response.context_data["queryset"]), [self.resource])

    def test_admin_action_execution_success(self):
        """Prueba la ejecución de la acción del admin cuando el formulario intermedio es enviado."""
        site = AdminSite()
        resource_admin = ResourceAdmin(Resource, site)

        # Simular request POST con el formulario confirmado ("apply": "yes")
        factory = RequestFactory()
        request = factory.post(
            reverse("admin:content_resource_changelist"),
            {
                "action": "generar_preguntas_ia_action",
                "apply": "yes",
                "levels": ["2"],
                "mode": "evaluacion",
                "count": "3",
            }
        )
        request.user = self.user

        # Añadir soporte de mensajes
        # Django admin usa la middleware de mensajes; necesitamos mockearla en el request
        setattr(request, "_messages", fallback_storage_mock())

        queryset = Resource.objects.filter(pk=self.resource.pk)

        initial_count = Question.objects.filter(resource=self.resource).count()

        response = resource_admin.generar_preguntas_ia_action(request, queryset)

        # Debería ejecutar la generación y retornar None (redirección por defecto de admin action)
        self.assertIsNone(response)

        final_count = Question.objects.filter(resource=self.resource).count()
        self.assertEqual(final_count, initial_count + 3)

        new_questions = Question.objects.filter(resource=self.resource, level=2, mode="evaluacion")
        self.assertEqual(new_questions.count(), 3)
        self.assertTrue(all(q.status == "publicada" for q in new_questions))


def fallback_storage_mock():
    """Genera un storage de mensajes mock para tests de admin."""
    from django.contrib.messages.storage.fallback import FallbackStorage
    from django.contrib.sessions.middleware import SessionMiddleware

    # Creamos un request de juguete para inicializar el storage
    factory = RequestFactory()
    request = factory.get("/")
    SessionMiddleware(lambda req: None).process_request(request)
    return FallbackStorage(request)
