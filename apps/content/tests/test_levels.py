from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Level, Subject, Topic


class SubjectTopicLevelTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            "admin", "admin@example.com", "pass12345"
        )
        self.escolar = Level.objects.create(name="Escolar", order=1, is_active=True)
        self.universitario = Level.objects.create(
            name="Universitario", order=3, is_active=True
        )

    def test_admin_can_assign_levels_to_subject_via_form(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("content:subject_create"),
            {
                "name": "Mecánica",
                "description": "",
                "levels": [self.universitario.pk],
                "is_active": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        subject = Subject.objects.get(name="Mecánica")
        self.assertEqual(list(subject.levels.all()), [self.universitario])

    def test_subject_form_exposes_levels_field(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("content:subject_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Niveles")
        self.assertContains(response, "Universitario")

    def test_level_detail_lists_content_by_direct_level(self):
        escolar_subject = Subject.objects.create(
            name="Matemática Escolar", is_active=True
        )
        escolar_subject.levels.add(self.escolar)
        escolar_topic = Topic.objects.create(
            name="Fracciones", subject=escolar_subject, is_active=True
        )
        escolar_topic.levels.add(self.escolar)

        uni_subject = Subject.objects.create(name="Mecánica", is_active=True)
        uni_subject.levels.add(self.universitario)

        response = self.client.get(
            reverse("content:level_detail", kwargs={"slug": self.escolar.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Matemática Escolar")
        self.assertContains(response, "Fracciones")
        # Contenido de otro nivel no debe aparecer
        self.assertNotContains(response, "Mecánica")

    def test_subject_list_groups_by_direct_level(self):
        subject = Subject.objects.create(name="Matemática Escolar", is_active=True)
        subject.levels.add(self.escolar)

        response = self.client.get(reverse("content:subject_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Matemática Escolar")
        # Aparece bajo el grupo de su nivel, no en "Otras asignaturas"
        self.assertContains(response, "Escolar")
