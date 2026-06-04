from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.content.models import Area, Level, Module, ModuleResource, Resource, Subject, Topic


class ResourceDetailViewTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Matematica", is_active=True)
        self.topic = Topic.objects.create(
            name="Algebra",
            subject=self.subject,
            is_active=True,
        )
        self.level = Level.objects.create(name="Primaria", is_active=True)
        self.other_subject = Subject.objects.create(name="Lenguaje", is_active=True)
        self.other_level = Level.objects.create(name="Secundaria", is_active=True)
        self.related_public_resource = Resource.objects.create(
            title="Guia de geometria",
            subject=self.subject,
            topic=self.topic,
            is_published=True,
        )
        self.related_public_resource.levels.add(self.level)
        self.published_resource = Resource.objects.create(
            title="Guia de algebra",
            subject=self.subject,
            topic=self.topic,
            description="Ficha publica de algebra escolar.",
            content="Contenido completo privado de algebra.",
            file="resources/files/guia.pdf",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            is_published=True,
        )
        self.published_resource.levels.add(self.level)
        self.published_resource.levels.add(self.other_level)
        self.draft_resource = Resource.objects.create(
            title="Borrador de algebra",
            subject=self.subject,
            topic=self.topic,
            content="Contenido completo del borrador.",
            video_url="https://www.youtube.com/watch?v=9bZkp7q19f0",
            is_published=False,
        )
        self.draft_related_resource = Resource.objects.create(
            title="Borrador de lectura",
            subject=self.other_subject,
            is_published=False,
        )
        self.draft_related_resource.levels.add(self.level)
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="testpass123",
        )

    def test_anonymous_user_sees_public_resource_preview_only(self):
        response = self.client.get(
            reverse("content:resource_detail", args=[self.published_resource.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.published_resource.title)
        self.assertContains(response, self.published_resource.description)
        self.assertContains(response, "Para ver videos y el contenido completo")
        self.assertContains(response, reverse("content:subject_detail", args=[self.subject.slug]))
        self.assertContains(response, reverse("content:topic_detail", args=[self.topic.slug]))
        self.assertContains(response, reverse("content:level_detail", args=[self.level.slug]))
        self.assertContains(response, reverse("login"))
        self.assertContains(response, reverse("register"))
        self.assertNotContains(response, "youtube-nocookie.com")
        self.assertNotContains(response, "Descargar recurso")
        self.assertNotContains(response, self.published_resource.content)
        self.assertNotContains(response, "Siguiente Recurso")

    def test_authenticated_user_can_see_published_resource(self):
        user = User.objects.create_user(username="student2", password="testpass123")
        self.client.force_login(user)

        response = self.client.get(
            reverse("content:resource_detail", args=[self.published_resource.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.published_resource.title)
        self.assertContains(response, "BreadcrumbList")
        self.assertContains(response, "Article")
        self.assertContains(response, "youtube-nocookie.com")
        self.assertContains(response, "Descargar recurso")
        self.assertContains(response, self.published_resource.content)
        self.assertContains(response, "Siguiente Recurso")
        self.assertContains(
            response,
            reverse("content:subject_detail", args=[self.subject.slug]),
        )
        self.assertContains(
            response,
            reverse("content:level_detail", args=[self.level.slug]),
        )

    def test_authenticated_non_superuser_cannot_see_draft_resource(self):
        user = User.objects.create_user(username="student_draft", password="testpass123")
        self.client.force_login(user)
        response = self.client.get(
            reverse("content:resource_detail", args=[self.draft_resource.slug])
        )

        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_cannot_see_draft_resource(self):
        response = self.client.get(
            reverse("content:resource_detail", args=[self.draft_resource.slug])
        )

        self.assertEqual(response.status_code, 404)

    def test_superuser_can_see_draft_resource(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("content:resource_detail", args=[self.draft_resource.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.draft_resource.title)
        self.assertContains(response, self.draft_resource.content)
        self.assertContains(response, "youtube-nocookie.com")

    def test_login_from_resource_preview_returns_to_resource(self):
        resource_url = reverse("content:resource_detail", args=[self.published_resource.slug])
        user = User.objects.create_user(username="student_login", email="student@example.com", password="testpass123")
        from allauth.account.models import EmailAddress
        EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)

        response = self.client.post(
            f"{reverse('login')}?next={resource_url}",
            {
                "username": user.username,
                "password": "testpass123",
            },
        )

        self.assertRedirects(response, resource_url)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="none")
    def test_register_from_resource_preview_returns_to_resource(self):
        resource_url = reverse("content:resource_detail", args=[self.published_resource.slug])

        response = self.client.post(
            reverse("register"),
            {
                "username": "new_student",
                "first_name": "New",
                "last_name": "Student",
                "email": "new_student@example.com",
                "role": "alumno",
                "phone": "",
                "city": "",
                "institution": "",
                "education_level": "",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "next": resource_url,
            },
        )

        self.assertRedirects(response, resource_url)


class ModuleResourceEndpointTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Matematica")
        self.module = Module.objects.create(
            title="Ruta de algebra",
            subject=self.subject,
            is_published=True,
        )
        self.resource = Resource.objects.create(
            title="Ejercicios de ecuaciones",
            subject=self.subject,
            is_published=True,
        )
        ModuleResource.objects.create(
            module=self.module,
            resource=self.resource,
            order=1,
        )
        self.user = User.objects.create_user(
            username="student",
            password="testpass123",
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="testpass123",
        )

    def test_module_resource_list_requires_admin(self):
        response = self.client.get(
            reverse("content:module_resource_list", args=[self.module.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/cuentas/login/", response["Location"])

    def test_module_resource_list_rejects_non_admin_user(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("content:module_resource_list", args=[self.module.pk])
        )

        self.assertEqual(response.status_code, 302)

    def test_admin_can_list_module_resources(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("content:module_resource_list", args=[self.module.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["resources"][0]["title"], self.resource.title)

    def test_resource_options_requires_admin(self):
        response = self.client.get(reverse("content:resource_options"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/cuentas/login/", response["Location"])

    def test_admin_can_load_resource_options(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("content:resource_options"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["resources"][0]["title"], self.resource.title)


class ResourceListFilterTests(TestCase):
    def setUp(self):
        self.math = Subject.objects.create(name="Matematica", is_active=True)
        self.physics = Subject.objects.create(name="Fisica", is_active=True)
        self.math_topic = Topic.objects.create(
            subject=self.math,
            name="Ecuaciones lineales",
            is_active=True,
        )
        self.physics_topic = Topic.objects.create(
            subject=self.physics,
            name="Movimiento rectilineo",
            is_active=True,
        )
        self.math_resource = Resource.objects.create(
            title="Ejercicios de ecuaciones lineales",
            subject=self.math,
            topic=self.math_topic,
            is_published=True,
        )
        self.physics_resource = Resource.objects.create(
            title="Resumen de movimiento rectilineo",
            subject=self.physics,
            topic=self.physics_topic,
            is_published=True,
        )

    def test_clear_filters_link_is_visible_only_when_filters_are_active(self):
        response = self.client.get(reverse("content:resource_list"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Limpiar filtros")

        response = self.client.get(
            reverse("content:resource_list"),
            {
                "subject": self.math.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Limpiar filtros")
        self.assertContains(response, reverse("content:resource_list"))
        self.assertContains(response, "Asignatura: Matematica")
        self.assertTrue(response.context["has_active_filters"])
        self.assertEqual(response.context["filter_querystring"], f"subject={self.math.pk}")

    def test_invalid_topic_for_selected_subject_is_ignored(self):
        response = self.client.get(
            reverse("content:resource_list"),
            {
                "subject": self.math.pk,
                "topic": self.physics_topic.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.math_resource.title)
        self.assertNotContains(response, self.physics_resource.title)
        self.assertEqual(response.context["selected_subject"], str(self.math.pk))
        self.assertEqual(response.context["selected_topic"], "")

    def test_topic_select_excludes_topics_from_other_subjects(self):
        response = self.client.get(
            reverse("content:resource_list"),
            {
                "subject": self.math.pk,
                "topic": self.physics_topic.pk,
            },
        )

        self.assertContains(response, "Matematica - Ecuaciones lineales")
        self.assertNotContains(response, "Fisica - Movimiento rectilineo")

    def test_pagination_keeps_normalized_filters(self):
        for index in range(20):
            Resource.objects.create(
                title=f"Ejercicio extra {index + 1}",
                subject=self.math,
                topic=self.math_topic,
                is_published=True,
            )

        response = self.client.get(
            reverse("content:resource_list"),
            {
                "subject": self.math.pk,
                "topic": self.physics_topic.pk,
                "page": 2,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_topic"], "")
        self.assertEqual(response.context["filter_querystring"], f"subject={self.math.pk}")
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertContains(response, f"?page=1&subject={self.math.pk}")
        self.assertNotContains(response, f"topic={self.physics_topic.pk}")


class SpanishUrlTests(TestCase):
    def setUp(self):
        self.area = Area.objects.create(
            name="Matematica",
            is_active=True,
        )
        self.subject = Subject.objects.create(
            name="Matematica Escolar",
            area=self.area,
            is_active=True,
        )
        self.level = Level.objects.create(
            name="Primaria",
            is_active=True,
        )
        self.resource = Resource.objects.create(
            title="Guia de funciones",
            subject=self.subject,
            is_published=True,
        )
        self.resource.levels.add(self.level)

    def test_public_content_urls_reverse_to_spanish_paths(self):
        self.assertEqual(reverse("content:resource_list"), "/recursos/")
        self.assertEqual(reverse("content:area_list"), "/areas/")
        self.assertEqual(reverse("content:subject_list"), "/asignaturas/")
        self.assertEqual(reverse("content:topic_list"), "/temas/")
        self.assertEqual(reverse("content:level_list"), "/niveles/")
        self.assertEqual(reverse("content:module_list"), "/modulos/")
        self.assertEqual(
            reverse("content:area_detail", args=[self.area.slug]),
            f"/areas/{self.area.slug}/",
        )
        self.assertEqual(
            reverse("content:subject_detail", args=[self.subject.slug]),
            f"/asignaturas/{self.subject.slug}/",
        )
        self.assertEqual(
            reverse("content:level_detail", args=[self.level.slug]),
            f"/niveles/{self.level.slug}/",
        )

    def test_resource_detail_uses_slug_url(self):
        self.assertEqual(
            reverse("content:resource_detail", args=[self.resource.slug]),
            f"/recursos/{self.resource.slug}/",
        )

    def test_legacy_content_urls_still_work(self):
        response = self.client.get("/content/resources/")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/recursos/")

        response = self.client.get(f"/content/resources/{self.resource.pk}/")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], f"/recursos/{self.resource.slug}/")

        response = self.client.get(f"/content/subjects/{self.subject.pk}/")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], f"/asignaturas/{self.subject.slug}/")

        response = self.client.get(f"/content/levels/{self.level.pk}/")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], f"/niveles/{self.level.slug}/")

    def test_subject_and_level_detail_pages_render(self):
        area_response = self.client.get(
            reverse("content:area_detail", args=[self.area.slug])
        )
        subject_response = self.client.get(
            reverse("content:subject_detail", args=[self.subject.slug])
        )
        level_response = self.client.get(
            reverse("content:level_detail", args=[self.level.slug])
        )

        self.assertEqual(area_response.status_code, 200)
        self.assertEqual(subject_response.status_code, 200)
        self.assertEqual(level_response.status_code, 200)
        self.assertContains(area_response, self.subject.name)
        self.assertContains(area_response, self.resource.title)
        self.assertContains(subject_response, self.resource.title)
        self.assertContains(level_response, self.subject.name)


import os
from unittest.mock import patch
from django.core.exceptions import ValidationError

class YouTubeWebhookSecurityTests(TestCase):
    def setUp(self):
        cache.clear()
        self.url = reverse("content:api_create_resource_from_video")
        self.subject = Subject.objects.create(
            name="Fisica",
            slug="fisica",
            is_active=True,
        )
        self.topic = Topic.objects.create(
            name="Dinamica",
            slug="dinamica",
            subject=self.subject,
            is_active=True,
        )
        self.other_subject = Subject.objects.create(
            name="Quimica",
            slug="quimica",
            is_active=True,
        )
        self.other_topic = Topic.objects.create(
            name="Estequiometria",
            slug="estequiometria",
            subject=self.other_subject,
            is_active=True,
        )

    @patch.dict(os.environ, {}, clear=True)
    def test_webhook_fails_closed_if_secret_token_missing(self):
        response = self.client.post(
            self.url,
            data='{"title": "Test Video", "video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}',
            content_type="application/json",
            HTTP_X_API_TOKEN="some_token"
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["ok"], False)
        self.assertIn("Token de seguridad no configurado", response.json()["error"])

    @patch.dict(os.environ, {"API_SECRET_TOKEN": "default_secret_token_change_me"})
    def test_webhook_fails_closed_if_secret_token_is_default(self):
        response = self.client.post(
            self.url,
            data='{"title": "Test Video", "video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}',
            content_type="application/json",
            HTTP_X_API_TOKEN="default_secret_token_change_me"
        )
        self.assertEqual(response.status_code, 500)
        self.assertIn("Token de seguridad no configurado", response.json()["error"])

    @patch.dict(os.environ, {"API_SECRET_TOKEN": "my-secret-token"})
    def test_webhook_fails_if_token_in_body(self):
        # We only accept tokens in headers now
        response = self.client.post(
            self.url,
            data='{"title": "Test Video", "video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ", "token": "my-secret-token"}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

    @patch.dict(os.environ, {"API_SECRET_TOKEN": "my-secret-token"})
    def test_webhook_success_with_header_token_and_defaults_to_draft(self):
        response = self.client.post(
            self.url,
            data='{"title": "Test Webhook Video", "video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}',
            content_type="application/json",
            HTTP_X_API_TOKEN="my-secret-token"
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["ok"])
        self.assertTrue(response.json()["created"])

        # Verify the created resource is draft (is_published = False) by default
        resource = Resource.objects.get(pk=response.json()["resource_id"])
        self.assertEqual(resource.title, "Test Webhook Video")
        self.assertFalse(resource.is_published)

    @patch.dict(os.environ, {"API_SECRET_TOKEN": "my-secret-token"})
    def test_webhook_assigns_subject_topic_and_levels(self):
        level = Level.objects.create(
            name="Universitario",
            slug="universitario",
            is_active=True,
        )

        response = self.client.post(
            self.url,
            data=(
                '{"title": "Clase de dinamica", '
                '"video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ", '
                '"subject_slug": "fisica", '
                '"topic_slug": "dinamica", '
                '"level_slugs": ["universitario"], '
                '"is_published": true}'
            ),
            content_type="application/json",
            HTTP_X_API_TOKEN="my-secret-token",
        )

        self.assertEqual(response.status_code, 201)
        resource = Resource.objects.get(pk=response.json()["resource_id"])
        self.assertEqual(resource.subject, self.subject)
        self.assertEqual(resource.topic, self.topic)
        self.assertTrue(resource.is_published)
        self.assertEqual(list(resource.levels.all()), [level])

    @patch.dict(os.environ, {"API_SECRET_TOKEN": "my-secret-token"})
    def test_webhook_rejects_topic_from_another_subject(self):
        response = self.client.post(
            self.url,
            data=(
                '{"title": "Clase cruzada", '
                '"video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ", '
                '"subject_slug": "fisica", '
                '"topic_slug": "estequiometria"}'
            ),
            content_type="application/json",
            HTTP_X_API_TOKEN="my-secret-token",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["ok"])
        self.assertEqual(
            response.json()["error"],
            "El tema indicado no existe o no pertenece a la asignatura indicada",
        )

    @patch.dict(os.environ, {"API_SECRET_TOKEN": "my-secret-token"})
    def test_webhook_rejects_unknown_subject_slug(self):
        response = self.client.post(
            self.url,
            data=(
                '{"title": "Clase desconocida", '
                '"video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ", '
                '"subject_slug": "asignatura-inexistente"}'
            ),
            content_type="application/json",
            HTTP_X_API_TOKEN="my-secret-token",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["ok"])
        self.assertEqual(response.json()["error"], "La asignatura indicada no existe")

    @patch.dict(os.environ, {"API_SECRET_TOKEN": "my-secret-token"})
    def test_webhook_updates_existing_resource_topic(self):
        resource = Resource.objects.create(
            title="Titulo antiguo",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            subject=self.other_subject,
            topic=self.other_topic,
            is_published=False,
        )

        response = self.client.post(
            self.url,
            data=(
                '{"title": "Titulo nuevo", '
                '"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", '
                '"subject_slug": "fisica", '
                '"topic_slug": "dinamica", '
                '"is_published": true}'
            ),
            content_type="application/json",
            HTTP_X_API_TOKEN="my-secret-token",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["created"])
        resource.refresh_from_db()
        self.assertEqual(resource.title, "Titulo nuevo")
        self.assertEqual(resource.subject, self.subject)
        self.assertEqual(resource.topic, self.topic)
        self.assertTrue(resource.is_published)

    @patch.dict(os.environ, {"API_SECRET_TOKEN": "my-secret-token"})
    def test_webhook_dedupes_by_youtube_id_across_url_formats(self):
        resource = Resource.objects.create(
            title="Titulo original",
            video_url="https://youtu.be/dQw4w9WgXcQ",
            is_published=True,
        )

        response = self.client.post(
            self.url,
            data=(
                '{"title": "Titulo reprocesado", '
                '"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", '
                '"is_published": true}'
            ),
            content_type="application/json",
            HTTP_X_API_TOKEN="my-secret-token",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["created"])
        self.assertEqual(response.json()["resource_id"], resource.id)
        self.assertEqual(Resource.objects.count(), 1)
        resource.refresh_from_db()
        self.assertEqual(resource.title, "Titulo reprocesado")

    @patch.dict(os.environ, {"API_SECRET_TOKEN": "my-secret-token"})
    def test_webhook_preserves_published_state_when_flag_omitted(self):
        resource = Resource.objects.create(
            title="Titulo publicado",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            is_published=True,
        )

        response = self.client.post(
            self.url,
            data=(
                '{"title": "Titulo actualizado", '
                '"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
            ),
            content_type="application/json",
            HTTP_X_API_TOKEN="my-secret-token",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["created"])
        resource.refresh_from_db()
        self.assertEqual(resource.title, "Titulo actualizado")
        # No se envió is_published: debe conservar el estado publicado previo.
        self.assertTrue(resource.is_published)

    @patch.dict(os.environ, {"API_SECRET_TOKEN": "my-secret-token"})
    def test_webhook_fails_if_video_url_is_invalid(self):
        response = self.client.post(
            self.url,
            data='{"title": "Test Video", "video_url": "https://google.com/watch?v=dQw4w9WgXcQ"}',
            content_type="application/json",
            HTTP_X_API_TOKEN="my-secret-token"
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["ok"])
        self.assertEqual(response.json()["error"], "La URL del video debe ser un enlace valido de YouTube")

    @patch.dict(os.environ, {"API_SECRET_TOKEN": "my-secret-token"})
    def test_webhook_logs_failed_authentication_without_secret(self):
        with self.assertLogs("apps.content.views.api_video", level="WARNING") as logs:
            response = self.client.post(
                self.url,
                data='{"title": "Test Video", "video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}',
                content_type="application/json",
                HTTP_X_API_TOKEN="wrong-token",
            )

        self.assertEqual(response.status_code, 401)
        self.assertTrue(
            any("Rejected video webhook request" in message for message in logs.output)
        )
        self.assertFalse(any("my-secret-token" in message for message in logs.output))
        self.assertFalse(any("wrong-token" in message for message in logs.output))

    @override_settings(
        VIDEO_WEBHOOK_RATE_LIMIT_ATTEMPTS=2,
        VIDEO_WEBHOOK_RATE_LIMIT_WINDOW=60,
    )
    @patch.dict(os.environ, {"API_SECRET_TOKEN": "my-secret-token"})
    def test_webhook_rate_limits_repeated_failed_attempts(self):
        payload = '{"title": "Test Video", "video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}'

        for _index in range(2):
            response = self.client.post(
                self.url,
                data=payload,
                content_type="application/json",
                HTTP_X_API_TOKEN="wrong-token",
            )
            self.assertEqual(response.status_code, 401)

        response = self.client.post(
            self.url,
            data=payload,
            content_type="application/json",
            HTTP_X_API_TOKEN="wrong-token",
        )

        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.json()["error"], "Demasiados intentos")




class ResourceModelFileValidationTests(TestCase):
    def test_file_size_validation(self):
        from apps.content.models.resource import validate_file_size

        # 10MB limit is 10485760 bytes. Test with 11MB file.
        large_file = SimpleUploadedFile("test.pdf", b"x" * (11 * 1024 * 1024))
        with self.assertRaises(ValidationError):
            validate_file_size(large_file)

        # Test with 5MB file (should not raise error)
        small_file = SimpleUploadedFile("test.pdf", b"x" * (5 * 1024 * 1024))
        try:
            validate_file_size(small_file)
        except ValidationError:
            self.fail("validate_file_size raised ValidationError unexpectedly!")

    def test_file_mime_validation(self):
        from apps.content.models.resource import validate_file_mime

        # Valid PDF file (pdf mime type is application/pdf)
        valid_pdf = SimpleUploadedFile("test.pdf", b"x" * 100, content_type="application/pdf")
        try:
            validate_file_mime(valid_pdf)
        except ValidationError:
            self.fail("validate_file_mime raised ValidationError unexpectedly on valid PDF!")

        # Invalid executable file (non-allowed mime type)
        invalid_exe = SimpleUploadedFile("test.exe", b"x" * 100, content_type="application/octet-stream")
        with self.assertRaises(ValidationError):
            validate_file_mime(invalid_exe)


class TopicDetailViewTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Matematica", is_active=True)
        self.topic = Topic.objects.create(name="Algebra", subject=self.subject, is_active=True)
        self.inactive_topic = Topic.objects.create(name="Geometria", subject=self.subject, is_active=False)

        # Levels with different order values
        self.level_basic = Level.objects.create(name="Primaria", order=1, is_active=True)
        self.level_advanced = Level.objects.create(name="Preuniversitario", order=3, is_active=True)

        # Resources associated with the active topic
        # Basic resource (Primaria order=1)
        self.basic_resource = Resource.objects.create(
            title="Suma Basica",
            topic=self.topic,
            subject=self.subject,
            is_published=True,
        )
        self.basic_resource.levels.add(self.level_basic)

        # Advanced resource (Preuniversitario order=3)
        self.advanced_resource = Resource.objects.create(
            title="Ecuaciones Complejas",
            topic=self.topic,
            subject=self.subject,
            is_published=True,
        )
        self.advanced_resource.levels.add(self.level_advanced)

        # Resource with no level assigned (should be coalesced to order 9999 and come last)
        self.no_level_resource = Resource.objects.create(
            title="Teoria General",
            topic=self.topic,
            subject=self.subject,
            is_published=True,
        )

        # Draft resource (should not be visible to anonymous user)
        self.draft_resource = Resource.objects.create(
            title="Borrador de Algebra",
            topic=self.topic,
            subject=self.subject,
            is_published=False,
        )

    def test_anonymous_user_can_view_active_topic_detail_with_ordered_resources(self):
        response = self.client.get(
            reverse("content:topic_detail", args=[self.topic.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.topic.name)
        self.assertContains(response, "BreadcrumbList")

        # Verify resources are listed in order: basic_resource -> advanced_resource -> no_level_resource
        resources = list(response.context["resources"])
        self.assertEqual(len(resources), 3)
        self.assertEqual(resources[0], self.basic_resource)
        self.assertEqual(resources[1], self.advanced_resource)
        self.assertEqual(resources[2], self.no_level_resource)

        # Draft resource should not be in the context
        self.assertNotIn(self.draft_resource, resources)

    def test_anonymous_user_cannot_view_inactive_topic(self):
        response = self.client.get(
            reverse("content:topic_detail", args=[self.inactive_topic.slug])
        )
        self.assertEqual(response.status_code, 404)


class TopicSlugFallbackTemplateTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Matematica Escolar", is_active=True)
        self.level = Level.objects.create(name="Escolar", is_active=True)
        self.topic = Topic.objects.create(
            name="Numeros Enteros",
            subject=self.subject,
            is_active=True,
        )
        self.resource = Resource.objects.create(
            title="Clase de numeros enteros",
            subject=self.subject,
            topic=self.topic,
            is_published=True,
        )
        self.resource.levels.add(self.level)
        Topic.objects.filter(pk=self.topic.pk).update(slug=None)

    def test_topic_list_does_not_render_none_topic_links(self):
        response = self.client.get(reverse("content:topic_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.topic.name)
        self.assertNotContains(response, "/temas/None/")

    def test_subject_detail_does_not_render_none_topic_links(self):
        response = self.client.get(
            reverse("content:subject_detail", args=[self.subject.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.topic.name)
        self.assertNotContains(response, "/temas/None/")


class TopicListViewPaginationTests(TestCase):
    def setUp(self):
        from apps.content.models import Level, Resource
        self.level = Level.objects.create(name="Escolar", order=1, is_active=True)
        self.subject = Subject.objects.create(name="Matematica", is_active=True)
        # Create 25 topics to trigger pagination (since paginate_by = 20)
        self.topics = []
        for i in range(1, 26):
            t = Topic.objects.create(name=f"Tema {i:02d}", subject=self.subject, is_active=True)
            self.topics.append(t)
            # Create a mock resource for each to bind it to Level
            r = Resource.objects.create(
                title=f"Recurso {i}",
                subject=self.subject,
                topic=t,
                is_published=True
            )
            r.levels.set([self.level])

    def test_topic_list_pagination(self):
        response = self.client.get(reverse("content:topic_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["topics"]), 20) # Page 1 should contain 20 items

        # Page 2
        response_page2 = self.client.get(reverse("content:topic_list"), {"page": 2})
        self.assertEqual(response_page2.status_code, 200)
        self.assertEqual(len(response_page2.context["topics"]), 5) # Remaining 5 items
        self.assertContains(response_page2, "Página 2 de 2")


class TopicResourceOrderingAndNavigationTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Fisica", is_active=True)
        self.topic = Topic.objects.create(name="Termodinamica", subject=self.subject, is_active=True)
        self.user = User.objects.create_user(username="student_ordering", password="testpass123")
        self.client.force_login(self.user)

        self.r1 = Resource.objects.create(
            title="B: Ecuacion de estado",
            topic=self.topic,
            subject=self.subject,
            is_published=True,
            order=2,
        )
        self.r2 = Resource.objects.create(
            title="A: Calorimetria",
            topic=self.topic,
            subject=self.subject,
            is_published=True,
            order=1,
        )
        self.r3 = Resource.objects.create(
            title="C: Leyes termicas",
            topic=self.topic,
            subject=self.subject,
            is_published=True,
            order=3,
        )

    def test_default_ordering_level_fallback_alphabetical(self):
        # Default resource_ordering_method is level. No levels are assigned here.
        # Fallback should sort them by title: A: Calorimetria (r2) -> B: Ecuacion (r1) -> C: Leyes (r3)
        response = self.client.get(
            reverse("content:resource_detail", args=[self.r1.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["previous_resource"], self.r2)
        self.assertEqual(response.context["next_resource"], self.r3)

    def test_ordering_method_alphabetical(self):
        self.topic.resource_ordering_method = "alphabetical"
        self.topic.save()

        # Sorted by title: A: Calorimetria (r2) -> B: Ecuacion (r1) -> C: Leyes (r3)
        response = self.client.get(
            reverse("content:resource_detail", args=[self.r2.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["previous_resource"])
        self.assertEqual(response.context["next_resource"], self.r1)

    def test_ordering_method_manual(self):
        self.topic.resource_ordering_method = "manual"
        self.topic.save()

        # Ordered by order field: r2 (order 1) -> r1 (order 2) -> r3 (order 3)
        # Let's verify details on r1
        response = self.client.get(
            reverse("content:resource_detail", args=[self.r1.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["previous_resource"], self.r2)
        self.assertEqual(response.context["next_resource"], self.r3)

        # Change r3 order to 0 (should move to start: r3 -> r2 -> r1)
        self.r3.order = 0
        self.r3.save()

        response2 = self.client.get(
            reverse("content:resource_detail", args=[self.r1.slug])
        )
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.context["previous_resource"], self.r2)
        self.assertIsNone(response2.context["next_resource"])


class LevelDetailViewTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Matematica", is_active=True)
        self.level = Level.objects.create(name="Primaria", is_active=True)
        self.topic1 = Topic.objects.create(name="Algebra", subject=self.subject, is_active=True)
        self.topic2 = Topic.objects.create(name="Geometria", subject=self.subject, is_active=True)

        self.res1 = Resource.objects.create(title="Ficha 1", subject=self.subject, topic=self.topic1, is_published=True)
        self.res1.levels.add(self.level)

        self.res2 = Resource.objects.create(title="Ficha 2", subject=self.subject, topic=self.topic2, is_published=True)
        self.res2.levels.add(self.level)

    def test_level_detail_context_and_regrouping(self):
        url = reverse("content:level_detail", args=[self.level.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("topics", response.context)
        # Topics should be regrouped and shown
        self.assertContains(response, "Matematica")
        self.assertContains(response, "Algebra")
        self.assertContains(response, "Geometria")

    def test_level_detail_search_filter(self):
        url = reverse("content:level_detail", args=[self.level.slug])
        # Search matching Algebra
        response = self.client.get(url, {"q": "Alge"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Algebra")
        self.assertNotContains(response, "Geometria")

        # Search matching none
        response = self.client.get(url, {"q": "Inexistente"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Algebra")
        self.assertNotContains(response, "Geometria")
        self.assertContains(response, "No se encontraron temas que coincidan con")
