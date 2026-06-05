import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

from apps.content.models import Area, Level, Subject, Topic, Module

User = get_user_model()

class PublishStudioTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@profeonline.cl",
            password="adminpassword"
        )
        self.regular_user = User.objects.create_user(
            username="user",
            email="user@profeonline.cl",
            password="userpassword"
        )

        # Base structure
        self.area, _ = Area.objects.get_or_create(name="Física Test Studio", defaults={"is_active": True})
        self.subject, _ = Subject.objects.get_or_create(name="Física Escolar Test Studio", defaults={"area": self.area, "is_active": True})
        self.topic, _ = Topic.objects.get_or_create(name="Ondas y Sonido Test Studio", defaults={"subject": self.subject, "is_active": True})
        self.level, _ = Level.objects.get_or_create(name="Escolar Test Studio", defaults={"is_active": True})

    def test_publish_studio_requires_staff(self):
        url = reverse("content:publish_studio")

        # Anonymous user gets redirected (302)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        # Regular user gets redirected (302)
        self.client.login(username="user", password="userpassword")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

        # Superuser gets 200
        self.client.login(username="admin", password="adminpassword")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_subject_options_filters_by_area(self):
        # Create another Area and Subject
        area2 = Area.objects.create(name="Matemática", is_active=True)
        sub2 = Subject.objects.create(name="Álgebra", area=area2, is_active=True)

        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:subject_options")

        # Request for area 1
        response = self.client.get(url, {"area_id": self.area.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data["subjects"]), 1)
        self.assertEqual(data["subjects"][0]["id"], self.subject.id)

        # Request for area 2
        response = self.client.get(url, {"area_id": area2.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data["subjects"]), 1)
        self.assertEqual(data["subjects"][0]["id"], sub2.id)

    def test_module_options_filters_by_subject(self):
        # Create a module
        module = Module.objects.create(title="Ondas Electromagnéticas", subject=self.subject, is_published=True)

        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:module_options")

        # Request for subject 1
        response = self.client.get(url, {"subject_id": self.subject.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data["modules"]), 1)
        self.assertEqual(data["modules"][0]["id"], module.id)

    def test_inline_create_subject_returns_json_and_slug(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_inline_create", args=["subject"])

        # Valid create
        response = self.client.post(url, {
            "area_id": self.area.id,
            "name": "Termodinámica",
            "description": "Estudio del calor"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["ok"])
        self.assertEqual(data["name"], "Termodinámica")
        self.assertEqual(data["slug"], "termodinamica")

        # Verify db persistence
        self.assertTrue(Subject.objects.filter(name="Termodinámica").exists())

        # Invalid create (empty name)
        response = self.client.post(url, {
            "area_id": self.area.id,
            "name": "",
            "description": ""
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data["ok"])
        self.assertIn("name", data["errors"])

    def test_inline_create_module_returns_json_with_title_mapped_to_name(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_inline_create", args=["module"])

        # Valid create
        response = self.client.post(url, {
            "subject_id": self.subject.id,
            "topic_id": self.topic.id,
            "title": "Módulo 1: Ondas Sonoras",
            "description": "Conceptos de sonido"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["ok"])
        self.assertEqual(data["name"], "Módulo 1: Ondas Sonoras")
        self.assertEqual(data["slug"], "modulo-1-ondas-sonoras")

        # Verify db persistence and relationships
        module = Module.objects.get(title="Módulo 1: Ondas Sonoras")
        self.assertEqual(module.subject, self.subject)
        self.assertEqual(module.topic, self.topic)

    def test_publish_batch_requires_files_and_taxonomy(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        # Missing files and topic
        payload = {
            "file_names": "[]",  # empty
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": "", # empty!
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200) # Re-renders page with error info
        self.assertIn("errors", response.context)
        self.assertIn("file_names", response.context["errors"])
        self.assertIn("topic_id", response.context["errors"])

    def test_publish_batch_json_has_files_and_slugs(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        payload = {
            "file_names": '["video1.mp4", "video2.mp4"]',
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": self.topic.id,
            "playlist_id": "",
            "playlist_title": "",
            "instructions": "Instrucciones de prueba"
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertIn("upload-batch-ondas-y-sonido-test-studio.json", response["Content-Disposition"])

        # Decode output
        batch = json.loads(response.content.decode("utf-8"))
        self.assertEqual(batch["schema"], "profeonline.upload-batch/v1")
        removed_folder_field = "watch" + "_folder"
        self.assertNotIn(removed_folder_field, batch)
        self.assertEqual(batch["files"], ["video1.mp4", "video2.mp4"])
        self.assertEqual(batch["taxonomy"]["area_slug"], self.area.slug)
        self.assertEqual(batch["taxonomy"]["subject_slug"], self.subject.slug)
        self.assertEqual(batch["taxonomy"]["topic_slug"], self.topic.slug)
        self.assertEqual(batch["taxonomy"]["module_slug"], None)
        self.assertEqual(batch["youtube"]["playlist_id"], "")
        self.assertEqual(batch["youtube"]["playlist_title"], "")
        self.assertFalse(batch["youtube"]["create_playlist"])
        self.assertIsNone(batch["youtube"]["new_playlist"])
        self.assertEqual(batch["instructions"], "Instrucciones de prueba")

    def test_publish_post_taxonomy_inconsistency_rejected(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        # Subject of another area, topic of another subject
        other_area = Area.objects.create(name="Matemática", is_active=True)
        other_subject = Subject.objects.create(name="Álgebra", area=other_area, is_active=True)
        other_topic = Topic.objects.create(name="Ecuaciones", subject=other_subject, is_active=True)

        base_payload = {
            "file_names": '["video.mp4"]',
            "area_id": self.area.id,
        }

        # Case 1: Subject does not belong to Area
        payload = base_payload.copy()
        payload["subject_id"] = other_subject.id
        payload["topic_id"] = self.topic.id
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("errors", response.context)
        self.assertIn("subject_id", response.context["errors"])
        self.assertEqual(
            response.context["errors"]["subject_id"],
            "La asignatura no pertenece al area seleccionada."
        )

        # Case 2: Topic does not belong to Subject
        payload = base_payload.copy()
        payload["subject_id"] = self.subject.id
        payload["topic_id"] = other_topic.id
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("errors", response.context)
        self.assertIn("topic_id", response.context["errors"])
        self.assertEqual(
            response.context["errors"]["topic_id"],
            "El tema no pertenece a la asignatura seleccionada."
        )

    def test_publish_post_inactive_entities_rejected(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        # Inactive Area, Subject, Topic
        inactive_area = Area.objects.create(name="Área Inactiva", is_active=False)
        inactive_subject = Subject.objects.create(name="Sub Inactiva", area=self.area, is_active=False)
        inactive_topic = Topic.objects.create(name="Tema Inactivo", subject=self.subject, is_active=False)

        payload = {
            "file_names": '["video.mp4"]',
            "area_id": inactive_area.id,
            "subject_id": inactive_subject.id,
            "topic_id": inactive_topic.id,
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("errors", response.context)
        self.assertIn("area_id", response.context["errors"])
        self.assertIn("subject_id", response.context["errors"])
        self.assertIn("topic_id", response.context["errors"])
        self.assertEqual(response.context["errors"]["area_id"], "El area seleccionada esta inactiva.")
        self.assertEqual(response.context["errors"]["subject_id"], "La asignatura seleccionada esta inactiva.")
        self.assertEqual(response.context["errors"]["topic_id"], "El tema seleccionado esta inactivo.")

    def test_publish_post_module_inconsistency_rejected(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        # Module of another subject, or not published
        other_subject = Subject.objects.create(name="Física Universitaria", area=self.area, is_active=True)
        other_topic = Topic.objects.create(name="Termodinámica", subject=self.subject, is_active=True)

        module_wrong_subject = Module.objects.create(title="Módulo A", subject=other_subject, is_published=True)
        module_wrong_topic = Module.objects.create(title="Módulo B", subject=self.subject, topic=other_topic, is_published=True)
        module_unpublished = Module.objects.create(title="Módulo C", subject=self.subject, topic=self.topic, is_published=False)

        base_payload = {
            "file_names": '["video.mp4"]',
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": self.topic.id,
        }

        # Case 1: Wrong subject
        payload = base_payload.copy()
        payload["module_id"] = module_wrong_subject.id
        response = self.client.post(url, payload)
        self.assertIn("errors", response.context)
        self.assertIn("module_id", response.context["errors"])
        self.assertEqual(response.context["errors"]["module_id"], "El modulo no pertenece a la asignatura seleccionada.")

        # Case 2: Wrong topic
        payload = base_payload.copy()
        payload["module_id"] = module_wrong_topic.id
        response = self.client.post(url, payload)
        self.assertIn("errors", response.context)
        self.assertIn("module_id", response.context["errors"])
        self.assertEqual(response.context["errors"]["module_id"], "El modulo no pertenece al tema seleccionado.")

        # Case 3: Unpublished module
        payload = base_payload.copy()
        payload["module_id"] = module_unpublished.id
        response = self.client.post(url, payload)
        self.assertIn("errors", response.context)
        self.assertIn("module_id", response.context["errors"])
        self.assertEqual(response.context["errors"]["module_id"], "El modulo seleccionado no esta publicado.")

    def test_publish_post_playlist_normalization_and_validation(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        base_payload = {
            "file_names": '["video.mp4"]',
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": self.topic.id,
            "playlist_id": "",
            "playlist_title": ""
        }

        # Case 1: Valid playlist URL with list param
        payload = base_payload.copy()
        payload["playlist_id"] = "https://www.youtube.com/playlist?list=PL12345XYZ"
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        batch = json.loads(response.content.decode("utf-8"))
        self.assertEqual(batch["youtube"]["playlist_id"], "PL12345XYZ")
        self.assertFalse(batch["youtube"]["create_playlist"])
        self.assertIsNone(batch["youtube"]["new_playlist"])

        # Case 2: Invalid playlist URL (no list parameter)
        payload = base_payload.copy()
        payload["playlist_id"] = "https://www.youtube.com/watch?v=123"
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("errors", response.context)
        self.assertIn("playlist_id", response.context["errors"])

        # Case 3: Plain playlist ID (accepted)
        payload = base_payload.copy()
        payload["playlist_id"] = "PL12345XYZ"
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        batch = json.loads(response.content.decode("utf-8"))
        self.assertEqual(batch["youtube"]["playlist_id"], "PL12345XYZ")
        self.assertFalse(batch["youtube"]["create_playlist"])
        self.assertIsNone(batch["youtube"]["new_playlist"])

        # Case 4: Empty playlist ID (accepted as optional)
        payload = base_payload.copy()
        payload["playlist_id"] = ""
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        batch = json.loads(response.content.decode("utf-8"))
        self.assertEqual(batch["youtube"]["playlist_id"], "")
        self.assertFalse(batch["youtube"]["create_playlist"])
        self.assertIsNone(batch["youtube"]["new_playlist"])

    def test_publish_post_create_playlist_metadata(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        payload = {
            "file_names": '["video.mp4"]',
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": self.topic.id,
            "playlist_id": "https://www.youtube.com/watch?v=123",
            "playlist_title": "Playlist existente ignorada",
            "create_playlist": "true",
            "new_playlist_title": "Fisica Escolar - Sonido",
            "new_playlist_description": "Clases de sonido para reforzamiento escolar."
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        batch = json.loads(response.content.decode("utf-8"))

        self.assertEqual(batch["youtube"]["playlist_id"], "")
        self.assertEqual(batch["youtube"]["playlist_title"], "")
        self.assertTrue(batch["youtube"]["create_playlist"])
        self.assertEqual(batch["youtube"]["new_playlist"]["title"], "Fisica Escolar - Sonido")
        self.assertEqual(
            batch["youtube"]["new_playlist"]["description"],
            "Clases de sonido para reforzamiento escolar."
        )

    def test_publish_post_create_playlist_requires_title(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        payload = {
            "file_names": '["video.mp4"]',
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": self.topic.id,
            "create_playlist": "true",
            "new_playlist_title": "",
            "new_playlist_description": "Descripcion sin titulo."
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("errors", response.context)
        self.assertIn("new_playlist_title", response.context["errors"])

    def test_publish_post_malformed_filenames_rejected(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        payload = {
            "file_names": "{malformed json",
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": self.topic.id,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("formato JSON invalido", response.content.decode("utf-8"))

    def test_publish_post_non_list_filenames_rejected(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        # Not a list
        payload = {
            "file_names": '"just a string"',
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": self.topic.id,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("debe ser una lista de nombres de archivos", response.content.decode("utf-8"))

        # List of integers, not strings
        payload = {
            "file_names": '[1, 2, 3]',
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": self.topic.id,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("debe ser una lista de nombres de archivos", response.content.decode("utf-8"))
