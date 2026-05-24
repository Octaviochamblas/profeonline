from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Module, ModuleResource, Resource, Subject


class ResourceDetailViewTests(TestCase):
    def setUp(self):
        self.published_resource = Resource.objects.create(
            title="Guia de algebra",
            is_published=True,
        )
        self.draft_resource = Resource.objects.create(
            title="Borrador de algebra",
            is_published=False,
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="testpass123",
        )

    def test_anonymous_user_can_see_published_resource(self):
        response = self.client.get(
            reverse("content:resource_detail", args=[self.published_resource.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.published_resource.title)

    def test_anonymous_user_cannot_see_draft_resource(self):
        response = self.client.get(
            reverse("content:resource_detail", args=[self.draft_resource.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_superuser_can_see_draft_resource(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("content:resource_detail", args=[self.draft_resource.pk])
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
