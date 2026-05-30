from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Area, Level, Module, ModuleResource, Resource, Subject, Topic


class SeedContentCommandTests(TestCase):
    def test_seed_content_command_is_idempotent(self):
        stdout = StringIO()

        call_command("seed_content", stdout=stdout)
        call_command("seed_content", stdout=stdout)

        self.assertEqual(Area.objects.count(), 3)
        self.assertEqual(Level.objects.count(), 3)
        self.assertEqual(Subject.objects.count(), 20)
        self.assertEqual(Topic.objects.count(), 25)
        self.assertEqual(Resource.objects.filter(is_published=True).count(), 168)
        self.assertEqual(Module.objects.filter(is_published=True).count(), 1)
        self.assertGreater(ModuleResource.objects.count(), 0)
        self.assertIn("Contenido semilla listo", stdout.getvalue())


class ImportYouTubeResourcesCommandTests(TestCase):
    @patch(
        "apps.content.management.commands.import_youtube_resources.fetch_playlist_videos",
        return_value=[
            {
                "id": "abcdefghijk",
                "title": "1.1 Que son los numeros enteros",
                "description": "Video de prueba",
                "position": 0,
                "video_url": "https://www.youtube.com/watch?v=abcdefghijk",
            },
            {
                "id": "lmnopqrstuv",
                "title": "1.2 EJERCICIOS: Suma y resta de enteros - ProfeOnline.cl",
                "description": "Video de ejercicios",
                "position": 1,
                "video_url": "https://www.youtube.com/watch?v=lmnopqrstuv",
            },
        ],
    )
    def test_import_youtube_resources_creates_public_hierarchy(self, fetch_mock):
        stdout = StringIO()

        call_command(
            "import_youtube_resources",
            playlist_url="https://www.youtube.com/playlist?list=PL123",
            area="Matematica",
            subject="Matematica Escolar",
            topic="Numeros Enteros",
            youtube_api_key="fake-key",
            stdout=stdout,
        )

        area = Area.objects.get(name="Matematica")
        subject = Subject.objects.get(name="Matematica Escolar")
        topic = Topic.objects.get(name="Numeros Enteros")

        self.assertEqual(subject.area, area)
        self.assertEqual(topic.subject, subject)
        self.assertEqual(topic.resource_ordering_method, "manual")
        self.assertEqual(Resource.objects.filter(topic=topic, is_published=True).count(), 2)
        self.assertTrue(area.slug)
        self.assertTrue(subject.slug)
        self.assertTrue(topic.slug)
        self.assertIn(reverse("content:area_detail", args=[area.slug]), stdout.getvalue())
        self.assertIn(reverse("content:subject_detail", args=[subject.slug]), stdout.getvalue())
        self.assertIn(reverse("content:topic_detail", args=[topic.slug]), stdout.getvalue())

        resource = Resource.objects.get(video_url__contains="abcdefghijk")
        self.assertEqual(resource.subject, subject)
        self.assertEqual(resource.topic, topic)
        self.assertNotIn("1.1", resource.description)
        self.assertIn("Numeros Enteros", resource.description)

        area_response = self.client.get(reverse("content:area_detail", args=[area.slug]))
        subject_response = self.client.get(reverse("content:subject_detail", args=[subject.slug]))
        topic_response = self.client.get(reverse("content:topic_detail", args=[topic.slug]))

        self.assertEqual(area_response.status_code, 200)
        self.assertEqual(subject_response.status_code, 200)
        self.assertEqual(topic_response.status_code, 200)
        self.assertContains(area_response, subject.name)
        self.assertContains(subject_response, topic.name)
        self.assertContains(topic_response, resource.title)
        fetch_mock.assert_called_once()
