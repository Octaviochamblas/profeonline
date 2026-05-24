from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Level, Module, ModuleResource, Resource, Subject


class ResourceDetailViewTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Matematica", is_active=True)
        self.level = Level.objects.create(name="Primaria", is_active=True)
        self.published_resource = Resource.objects.create(
            title="Guia de algebra",
            subject=self.subject,
            is_published=True,
        )
        self.published_resource.levels.add(self.level)
        self.draft_resource = Resource.objects.create(
            title="Borrador de algebra",
            subject=self.subject,
            is_published=False,
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="testpass123",
        )

    def test_anonymous_user_can_see_published_resource(self):
        response = self.client.get(
            reverse("content:resource_detail", args=[self.published_resource.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.published_resource.title)
        self.assertContains(response, "BreadcrumbList")
        self.assertContains(response, "Article")
        self.assertContains(
            response,
            reverse("content:subject_detail", args=[self.subject.slug]),
        )
        self.assertContains(
            response,
            reverse("content:level_detail", args=[self.level.slug]),
        )

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


class SpanishUrlTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(
            name="Matematica",
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

        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"/content/resources/{self.resource.pk}/")

        self.assertEqual(response.status_code, 200)

    def test_subject_and_level_detail_pages_render(self):
        subject_response = self.client.get(
            reverse("content:subject_detail", args=[self.subject.slug])
        )
        level_response = self.client.get(
            reverse("content:level_detail", args=[self.level.slug])
        )

        self.assertEqual(subject_response.status_code, 200)
        self.assertEqual(level_response.status_code, 200)
        self.assertContains(subject_response, self.resource.title)
        self.assertContains(level_response, self.resource.title)
