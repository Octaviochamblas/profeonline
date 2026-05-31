from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Resource, ResourceCompletion, ResourceView, Subject, Topic


class ResumeWhereLeftOffTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("estudiante", "e@example.com", "pass12345")
        self.subject = Subject.objects.create(name="Matematica", is_active=True)
        self.topic = Topic.objects.create(
            name="Algebra", subject=self.subject, is_active=True
        )
        self.resource = Resource.objects.create(
            title="Guia 1", subject=self.subject, topic=self.topic, is_published=True
        )

    def test_viewing_resource_records_a_view(self):
        self.client.force_login(self.user)
        self.client.get(
            reverse("content:resource_detail", kwargs={"slug": self.resource.slug})
        )
        self.assertTrue(
            ResourceView.objects.filter(
                user=self.user, resource=self.resource
            ).exists()
        )

    def test_anonymous_view_does_not_record(self):
        self.client.get(
            reverse("content:resource_detail", kwargs={"slug": self.resource.slug})
        )
        self.assertEqual(ResourceView.objects.count(), 0)

    def test_profile_shows_resume_card_for_last_viewed(self):
        self.client.force_login(self.user)
        ResourceView.objects.create(user=self.user, resource=self.resource)

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["last_resource"], self.resource)
        self.assertContains(response, "Continuar donde quedaste")
        self.assertContains(response, self.resource.title)

    def test_profile_without_views_has_no_resume_card(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("profile"))

        self.assertIsNone(response.context["last_resource"])
        self.assertNotContains(response, "Continuar donde quedaste")

    def test_home_shows_resume_card_for_logged_in_user(self):
        self.client.force_login(self.user)
        ResourceView.objects.create(user=self.user, resource=self.resource)

        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["last_resource"], self.resource)
        self.assertContains(response, "Continuar donde quedaste")

    def test_home_has_no_resume_card_for_anonymous(self):
        response = self.client.get(reverse("core:home"))
        self.assertNotContains(response, "Continuar donde quedaste")

    def test_resume_card_marks_completed(self):
        self.client.force_login(self.user)
        ResourceView.objects.create(user=self.user, resource=self.resource)
        ResourceCompletion.objects.create(user=self.user, resource=self.resource)

        response = self.client.get(reverse("profile"))

        self.assertTrue(response.context["last_resource_completed"])
