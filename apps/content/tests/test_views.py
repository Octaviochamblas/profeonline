from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Level, Module, ModuleResource, Resource, Subject, Topic


class ResourceDetailViewTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Matematica", is_active=True)
        self.level = Level.objects.create(name="Primaria", is_active=True)
        self.other_subject = Subject.objects.create(name="Lenguaje", is_active=True)
        self.other_level = Level.objects.create(name="Secundaria", is_active=True)
        self.related_public_resource = Resource.objects.create(
            title="Guia de geometria",
            subject=self.subject,
            is_published=True,
        )
        self.related_public_resource.levels.add(self.level)
        self.published_resource = Resource.objects.create(
            title="Guia de algebra",
            subject=self.subject,
            is_published=True,
        )
        self.published_resource.levels.add(self.level)
        self.published_resource.levels.add(self.other_level)
        self.draft_resource = Resource.objects.create(
            title="Borrador de algebra",
            subject=self.subject,
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

    def test_anonymous_user_can_see_published_resource(self):
        response = self.client.get(
            reverse("content:resource_detail", args=[self.published_resource.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.published_resource.title)
        self.assertContains(response, "BreadcrumbList")
        self.assertContains(response, "Article")
        self.assertContains(response, self.related_public_resource.title)
        self.assertNotContains(response, self.draft_related_resource.title)
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
