from django.test import TestCase

from apps.content.forms import LevelForm, ResourceForm, SubjectForm, TopicForm
from apps.content.models import Level, Subject, Topic


class ContentFormTests(TestCase):
    def setUp(self):
        self.active_subject = Subject.objects.create(name="Matemática", is_active=True)
        self.inactive_subject = Subject.objects.create(name="Historia", is_active=False)
        self.other_subject = Subject.objects.create(name="Lenguaje", is_active=True)
        self.active_topic = Topic.objects.create(
            subject=self.active_subject,
            name="Ecuaciones lineales",
            is_active=True,
        )
        self.other_topic = Topic.objects.create(
            subject=self.other_subject,
            name="Comprensión lectora",
            is_active=True,
        )
        self.level = Level.objects.create(name="Primaria", is_active=True)
        self.other_level = Level.objects.create(name="Secundaria", is_active=True)

    def test_subject_form_uses_shared_classes(self):
        form = SubjectForm()

        self.assertIn("form-control", form.fields["name"].widget.attrs["class"])
        self.assertIn("form-control", form.fields["description"].widget.attrs["class"])

    def test_level_form_uses_shared_classes(self):
        form = LevelForm()

        self.assertIn("form-control", form.fields["name"].widget.attrs["class"])
        self.assertIn("form-control", form.fields["order"].widget.attrs["class"])

    def test_topic_form_limits_subject_queryset_to_active_subjects(self):
        form = TopicForm()

        subject_names = list(form.fields["subject"].queryset.values_list("name", flat=True))

        self.assertEqual(subject_names, ["Lenguaje", "Matemática"])

    def test_resource_form_filters_topics_by_subject_and_active_levels(self):
        form = ResourceForm(data={"subject": self.active_subject.pk})

        topic_names = list(form.fields["topic"].queryset.values_list("name", flat=True))
        level_names = list(form.fields["levels"].queryset.values_list("name", flat=True))

        self.assertEqual(topic_names, ["Ecuaciones lineales"])
        self.assertEqual(level_names, ["Primaria", "Secundaria"])
        self.assertIn("checkbox-list", form.fields["levels"].widget.attrs["class"])

    def test_resource_form_validates_youtube_video_url(self):
        # Valid youtube URL
        form = ResourceForm(data={
            "title": "Un Recurso",
            "subject": self.active_subject.pk,
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        })
        self.assertTrue(form.is_valid())

        # Invalid youtube URL
        form_invalid = ResourceForm(data={
            "title": "Un Recurso",
            "subject": self.active_subject.pk,
            "video_url": "https://www.google.com/watch?v=dQw4w9WgXcQ"
        })
        self.assertFalse(form_invalid.is_valid())
        self.assertIn("video_url", form_invalid.errors)
        self.assertEqual(
            form_invalid.errors["video_url"][0],
            "La URL debe ser un enlace válido de YouTube (ej: https://www.youtube.com/watch?v=...) o youtu.be."
        )

