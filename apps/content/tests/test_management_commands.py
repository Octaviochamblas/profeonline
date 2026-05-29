from io import StringIO

from django.core.management import call_command
from django.test import TestCase

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
