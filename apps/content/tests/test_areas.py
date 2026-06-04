from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Area, Subject


class AreaSeedTests(TestCase):
    def test_seed_areas_exist(self):
        # La migración de datos 0021_seed_areas crea Física y Química
        # (Matemáticas la garantiza seed_math_resources en producción).
        for name in ["Física", "Química"]:
            self.assertTrue(
                Area.objects.filter(name=name).exists(),
                f"Falta el área '{name}' creada por la migración",
            )


class AreaCrudTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            "admin", "admin@example.com", "pass12345"
        )
        self.user = User.objects.create_user(
            "user", "user@example.com", "pass12345"
        )

    def test_admin_can_create_area_and_it_is_visible(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("content:area_create"),
            {
                "name": "Biología",
                "description": "Ciencias de la vida",
                "order": 4,
                "is_active": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Area.objects.filter(name="Biología").exists())

        list_response = self.client.get(reverse("content:area_list"))
        self.assertContains(list_response, "Biología")

    def test_non_admin_cannot_create_area(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("content:area_create"))
        self.assertEqual(response.status_code, 403)

    def test_deleting_area_keeps_its_subjects(self):
        # on_delete=SET_NULL: borrar un área NO debe borrar sus asignaturas.
        area = Area.objects.create(name="Provisional", order=9)
        subject = Subject.objects.create(
            name="Asignatura de prueba", area=area, is_active=True
        )

        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("content:area_delete", kwargs={"pk": area.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Area.objects.filter(pk=area.pk).exists())
        subject.refresh_from_db()
        self.assertIsNone(subject.area)
        self.assertTrue(Subject.objects.filter(pk=subject.pk).exists())
