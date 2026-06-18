"""Tests de la importación de guías desde Google Drive.

La red de Drive se mockea (igual que en `test_ai_generation`): se prueban el
parseo de IDs, los permisos, el listado, la importación y la degradación cuando
Drive no está configurado, sin hacer peticiones reales.
"""

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.content.models import Area, QuizGuide, Subject
from apps.content.services import drive_service

User = get_user_model()

_DUMMY_CREDS = '{"type": "service_account", "client_email": "x@y.iam.gserviceaccount.com"}'


class ParseFolderIdTests(TestCase):
    def test_extracts_id_from_folder_url(self):
        url = "https://drive.google.com/drive/folders/1A2b3C4d_eF?usp=sharing"
        self.assertEqual(drive_service.parse_folder_id(url), "1A2b3C4d_eF")

    def test_extracts_id_from_u_path(self):
        url = "https://drive.google.com/drive/u/0/folders/ZZZ123_abc"
        self.assertEqual(drive_service.parse_folder_id(url), "ZZZ123_abc")

    def test_extracts_id_param(self):
        self.assertEqual(
            drive_service.parse_folder_id("https://drive.google.com/open?id=PARAM999"),
            "PARAM999",
        )

    def test_bare_id_passthrough(self):
        self.assertEqual(drive_service.parse_folder_id("  BareId_123  "), "BareId_123")

    def test_unrecognized_returns_empty(self):
        self.assertEqual(drive_service.parse_folder_id("carpeta con espacios"), "")
        self.assertEqual(drive_service.parse_folder_id(""), "")


class DriveGuidesViewTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", password="pw", email="a@test.cl"
        )
        self.student = User.objects.create_user(username="alumno", password="pw")
        self.area = Area.objects.create(name="Matemática", order=1)
        self.subject = Subject.objects.create(name="Álgebra", area=self.area)

    # ----------------------------------------------------------- permisos
    def test_import_rejects_non_admin(self):
        self.client.force_login(self.student)
        resp = self.client.post(
            reverse("content:import_drive_guides"), {"drive_files": ["x"]}
        )
        self.assertIn(resp.status_code, (302, 403))
        self.assertEqual(QuizGuide.objects.count(), 0)

    def test_import_anonymous_redirects(self):
        resp = self.client.post(
            reverse("content:import_drive_guides"), {"drive_files": ["x"]}
        )
        self.assertIn(resp.status_code, (302, 403))

    # ----------------------------------------------------------- listado
    @override_settings(GOOGLE_SERVICE_ACCOUNT_JSON=_DUMMY_CREDS)
    @patch("apps.content.services.drive_service.list_folder")
    def test_listing_shows_files_and_subfolders(self, mock_list):
        mock_list.return_value = {
            "folder_id": "FOLDER1",
            "name": "Material Académico",
            "folders": [{"id": "sub1", "name": "Matemáticas"}],
            "files": [{"id": "f1", "name": "Guía Álgebra.pdf", "mime": "application/pdf"}],
        }
        self.client.force_login(self.admin)
        resp = self.client.get(
            reverse("content:quiz_guides"), {"drive_folder": "FOLDER1"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Guía Álgebra.pdf")
        self.assertContains(resp, "Matemáticas")          # subcarpeta listada
        self.assertContains(resp, "?drive_folder=sub1")    # link de drill-down
        mock_list.assert_called_once()

    @override_settings(GOOGLE_SERVICE_ACCOUNT_JSON="")
    @patch("apps.content.services.drive_service.list_folder")
    def test_not_configured_does_not_call_api(self, mock_list):
        self.client.force_login(self.admin)
        resp = self.client.get(
            reverse("content:quiz_guides"), {"drive_folder": "FOLDER1"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Drive no está configurado")
        mock_list.assert_not_called()

    @override_settings(GOOGLE_SERVICE_ACCOUNT_JSON=_DUMMY_CREDS)
    @patch("apps.content.services.drive_service.list_folder")
    def test_listing_shows_error_gracefully(self, mock_list):
        mock_list.side_effect = RuntimeError("Drive denegó el acceso (403).")
        self.client.force_login(self.admin)
        resp = self.client.get(
            reverse("content:quiz_guides"), {"drive_folder": "FOLDER1"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "403")

    # ----------------------------------------------------------- importación
    @patch("apps.content.services.drive_service.fetch_file")
    def test_import_creates_guide_with_links(self, mock_fetch):
        mock_fetch.return_value = {
            "id": "f1",
            "name": "Estilo PAES.pdf",
            "mime": "application/pdf",
            "text": "  Ejercicio 1:   resolver  2x=4 \n\n\n más texto ",
        }
        self.client.force_login(self.admin)
        resp = self.client.post(
            reverse("content:import_drive_guides"),
            {"drive_files": ["f1"], "subjects": [str(self.subject.id)]},
        )
        self.assertEqual(resp.status_code, 302)
        guide = QuizGuide.objects.get(source_filename="Estilo PAES.pdf")
        self.assertEqual(guide.title, "Estilo PAES.pdf")
        self.assertIn("Ejercicio 1", guide.content_text)
        self.assertNotIn("   ", guide.content_text)  # normalize_text colapsó espacios
        self.assertIn(self.subject, list(guide.subjects.all()))
        mock_fetch.assert_called_once_with("f1")

    def test_import_without_selection_shows_error(self):
        self.client.force_login(self.admin)
        resp = self.client.post(reverse("content:import_drive_guides"), {})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(QuizGuide.objects.count(), 0)

    @patch("apps.content.services.drive_service.fetch_file")
    def test_import_skips_file_without_text(self, mock_fetch):
        mock_fetch.return_value = {
            "id": "f1", "name": "vacio.pdf", "mime": "application/pdf", "text": "   ",
        }
        self.client.force_login(self.admin)
        resp = self.client.post(
            reverse("content:import_drive_guides"), {"drive_files": ["f1"]}
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(QuizGuide.objects.count(), 0)
