from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from apps.content.models import Area, Resource, Subject, Topic


class ResourceEducationLevelTests(TestCase):
    def setUp(self):
        self.area, _ = Area.objects.get_or_create(name="Física", defaults={"order": 1})
        self.subject = Subject.objects.create(name="Física Escolar (test)", area=self.area)
        self.topic = Topic.objects.create(name="Introducción", subject=self.subject)
        self.resource = Resource.objects.create(
            title="Qué es la física", subject=self.subject, topic=self.topic
        )

    def test_falls_back_to_subject_level_when_topic_has_none(self):
        self.subject.education_level = "media"
        self.subject.save(update_fields=["education_level"])
        self.assertEqual(self.resource.get_education_level(), "media")

    def test_topic_level_overrides_subject_level(self):
        self.subject.education_level = "media"
        self.subject.save(update_fields=["education_level"])
        self.topic.education_level = "universitaria"
        self.topic.save(update_fields=["education_level"])
        self.assertEqual(self.resource.get_education_level(), "universitaria")

    def test_empty_when_neither_has_level(self):
        self.assertEqual(self.resource.get_education_level(), "")

    def test_subject_level_via_topic_subject_when_resource_subject_missing(self):
        self.subject.education_level = "media"
        self.subject.save(update_fields=["education_level"])
        self.resource.subject = None
        self.resource.save(update_fields=["subject"])
        self.assertEqual(self.resource.get_education_level(), "media")


class SetSubjectLevelCommandTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Física Escolar")

    def _run(self, *args):
        out = StringIO()
        call_command("set_subject_level", *args, stdout=out, stderr=StringIO())
        return out.getvalue()

    def test_dry_run_does_not_write(self):
        self._run("--subject", "Física Escolar", "--level", "media")
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.education_level, "")

    def test_apply_sets_level(self):
        self._run("--subject", "Física Escolar", "--level", "media", "--apply")
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.education_level, "media")

    def test_partial_match_resolves_single_subject(self):
        self._run("--subject", "física esc", "--level", "media", "--apply")
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.education_level, "media")

    def test_unknown_subject_raises(self):
        with self.assertRaises(CommandError):
            self._run("--subject", "Inexistente", "--level", "media", "--apply")

    def test_ambiguous_match_raises(self):
        Subject.objects.create(name="Física I")
        with self.assertRaises(CommandError):
            self._run("--subject", "Física", "--level", "media", "--apply")
