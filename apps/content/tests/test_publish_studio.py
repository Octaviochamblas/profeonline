import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

from apps.content.models import Area, Level, Subject, Topic, Resource, Module
from apps.content.services.resource_copy import build_resource_copy, clean_video_title

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

        # Base structure (using get_or_create to avoid unique constraint conflicts with seeds/migrations)
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

    def test_copy_preview_omits_video_section_without_url(self):
        video_with_url = {"title": "Clase 1: Vectores y Fuerzas", "video_url": "https://youtube.com/watch?v=123"}
        video_without_url = {"title": "Clase 1: Vectores y Fuerzas", "video_url": ""}

        # Test build_resource_copy behavior
        desc_w, content_w = build_resource_copy(video_with_url, self.subject, self.topic)
        desc_wo, content_wo = build_resource_copy(video_without_url, self.subject, self.topic)

        self.assertIn("### Video", content_w)
        self.assertNotIn("### Video", content_wo)

        # Test AJAX endpoint
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_copy_preview")
        response = self.client.get(url, {
            "title": "Clase 1: Vectores y Fuerzas",
            "subject_id": self.subject.id,
            "topic_id": self.topic.id
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertNotIn("### Video", data["content_md"])

    def test_publish_duplicates_flags_same_topic_title(self):
        resource = Resource.objects.create(
            title="Leyes de Newton",
            subject=self.subject,
            topic=self.topic,
            video_url="https://youtube.com/watch?v=abc",
            is_published=True
        )

        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_duplicates")

        # Exact match
        response = self.client.get(url, {"title": "Leyes de Newton", "topic_id": self.topic.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Leyes de Newton")

        # Fuzzy match (iexact/icontains/slugify)
        response = self.client.get(url, {"title": "leyes de newton", "topic_id": self.topic.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

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
            "level_ids": [self.level.id],
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
        self.assertTrue(module.levels.filter(id=self.level.id).exists())

    def test_publish_post_rejects_incomplete_job(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        # Missing levels and topic
        payload = {
            "file_name": "video.mp4",
            "watch_folder": "default",
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": "", # empty!
            "privacy": "public",
            "skip_playlist": "on",
            "palette": "azul-profeonline",
            "main_text": "Texto principal",
            "title": "Título del video",
            "description": "Una descripción",
            "content_md": "Contenido"
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200) # Re-renders page with error info
        self.assertIn("errors", response.context)
        self.assertIn("topic_id", response.context["errors"])
        self.assertIn("level_ids", response.context["errors"])

    def test_publish_post_success_and_json_structure(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        payload = {
            "file_name": "video.mp4",
            "watch_folder": "default",
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": self.topic.id,
            "level_ids": [self.level.id],
            "privacy": "public",
            "skip_playlist": "on",
            "playlist_id": "",
            "playlist_title": "",
            "palette": "azul-profeonline",
            "main_text": "Texto miniatura",
            "class_label": "Clase 1",
            "ai_panel_instructions": "Panel ilustrativo",
            "title": "Suma de Vectores",
            "description": "Aprende a sumar vectores",
            "content_md": "### Contenido",
            "ai_instructions": "SEO de clases particulares",
            "is_published": "on"
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertIn("upload-job-suma-de-vectores.json", response["Content-Disposition"])

        # Decode output
        job = json.loads(response.content.decode("utf-8"))
        self.assertEqual(job["schema"], "profeonline.upload-job/v1")
        self.assertEqual(job["file"]["file_name"], "video.mp4")
        self.assertEqual(job["youtube"]["privacy"], "public")
        self.assertTrue(job["youtube"]["skip_playlist"])
        self.assertEqual(job["taxonomy"]["area_slug"], self.area.slug)
        self.assertEqual(job["taxonomy"]["subject_slug"], self.subject.slug)
        self.assertEqual(job["taxonomy"]["topic_slug"], self.topic.slug)
        self.assertEqual(job["taxonomy"]["level_slugs"], [self.level.slug])
        self.assertEqual(job["thumbnail"]["main_text"], "Texto miniatura")
        self.assertEqual(job["copy"]["title"], "Suma de Vectores")

    def test_publish_post_taxonomy_inconsistency_rejected(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        # Subject of another area, topic of another subject
        other_area = Area.objects.create(name="Matemática", is_active=True)
        other_subject = Subject.objects.create(name="Álgebra", area=other_area, is_active=True)
        other_topic = Topic.objects.create(name="Ecuaciones", subject=other_subject, is_active=True)

        base_payload = {
            "file_name": "video.mp4",
            "watch_folder": "default",
            "area_id": self.area.id,
            "level_ids": [self.level.id],
            "privacy": "public",
            "skip_playlist": "on",
            "palette": "azul-profeonline",
            "main_text": "Texto miniatura",
            "title": "Suma de Vectores",
            "description": "Aprende a sumar vectores",
            "content_md": "### Contenido",
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

        # Inactive Area, Subject, Topic, Level
        inactive_area = Area.objects.create(name="Área Inactiva", is_active=False)
        inactive_subject = Subject.objects.create(name="Sub Inactiva", area=self.area, is_active=False)
        inactive_topic = Topic.objects.create(name="Tema Inactivo", subject=self.subject, is_active=False)
        inactive_level = Level.objects.create(name="Nivel Inactivo", is_active=False)

        payload = {
            "file_name": "video.mp4",
            "area_id": inactive_area.id,
            "subject_id": inactive_subject.id,
            "topic_id": inactive_topic.id,
            "level_ids": [inactive_level.id],
            "privacy": "public",
            "skip_playlist": "on",
            "palette": "azul-profeonline",
            "main_text": "Texto miniatura",
            "title": "Suma de Vectores",
            "description": "Aprende a sumar vectores",
            "content_md": "### Contenido",
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("errors", response.context)
        self.assertIn("area_id", response.context["errors"])
        self.assertIn("subject_id", response.context["errors"])
        self.assertIn("topic_id", response.context["errors"])
        self.assertIn("level_ids", response.context["errors"])
        self.assertEqual(response.context["errors"]["area_id"], "El area seleccionada esta inactiva.")
        self.assertEqual(response.context["errors"]["subject_id"], "La asignatura seleccionada esta inactiva.")
        self.assertEqual(response.context["errors"]["topic_id"], "El tema seleccionado esta inactivo.")

    def test_publish_post_invalid_level_rejected(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_studio")

        payload = {
            "file_name": "video.mp4",
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": self.topic.id,
            "level_ids": [self.level.id, 99999],  # 99999 is invalid!
            "privacy": "public",
            "skip_playlist": "on",
            "palette": "azul-profeonline",
            "main_text": "Texto miniatura",
            "title": "Suma de Vectores",
            "description": "Aprende a sumar vectores",
            "content_md": "### Contenido",
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("errors", response.context)
        self.assertIn("level_ids", response.context["errors"])
        self.assertEqual(
            response.context["errors"]["level_ids"],
            "Uno o mas niveles seleccionados son invalidos o estan inactivos."
        )

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
            "file_name": "video.mp4",
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": self.topic.id,
            "level_ids": [self.level.id],
            "privacy": "public",
            "skip_playlist": "on",
            "palette": "azul-profeonline",
            "main_text": "Texto miniatura",
            "title": "Suma de Vectores",
            "description": "Aprende a sumar vectores",
            "content_md": "### Contenido",
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
            "file_name": "video.mp4",
            "area_id": self.area.id,
            "subject_id": self.subject.id,
            "topic_id": self.topic.id,
            "level_ids": [self.level.id],
            "privacy": "public",
            "skip_playlist": "off",  # skip is off, so we require a valid playlist!
            "palette": "azul-profeonline",
            "main_text": "Texto miniatura",
            "title": "Suma de Vectores",
            "description": "Aprende a sumar vectores",
            "content_md": "### Contenido",
        }

        # Case 1: Valid playlist URL with list param
        payload = base_payload.copy()
        payload["playlist_id"] = "https://www.youtube.com/playlist?list=PL12345XYZ"
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        job = json.loads(response.content.decode("utf-8"))
        self.assertEqual(job["youtube"]["playlist_id"], "PL12345XYZ")

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
        job = json.loads(response.content.decode("utf-8"))
        self.assertEqual(job["youtube"]["playlist_id"], "PL12345XYZ")

    def test_publish_copy_preview_inconsistency_rejected(self):
        self.client.login(username="admin", password="adminpassword")
        url = reverse("content:publish_copy_preview")

        other_area = Area.objects.create(name="Matemática II", is_active=True)
        other_subject = Subject.objects.create(name="Cálculo", area=other_area, is_active=True)
        other_topic = Topic.objects.create(name="Derivadas", subject=other_subject, is_active=True)

        inactive_subject = Subject.objects.create(name="Física Inactiva", area=self.area, is_active=False)
        inactive_topic = Topic.objects.create(name="Cinemática Inactiva", subject=self.subject, is_active=False)

        # Incompatible topic & subject
        response = self.client.get(url, {
            "title": "Prueba",
            "subject_id": self.subject.id,
            "topic_id": other_topic.id
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("El tema no pertenece a la asignatura especificada.", response.content.decode("utf-8"))

        # Inactive subject
        response = self.client.get(url, {
            "title": "Prueba",
            "subject_id": inactive_subject.id,
            "topic_id": self.topic.id
        })
        self.assertEqual(response.status_code, 400)

        # Inactive topic
        response = self.client.get(url, {
            "title": "Prueba",
            "subject_id": self.subject.id,
            "topic_id": inactive_topic.id
        })
        self.assertEqual(response.status_code, 400)
