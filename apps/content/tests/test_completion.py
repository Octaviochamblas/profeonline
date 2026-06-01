from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Resource, ResourceCompletion, Subject, Topic


class ResourceCompletionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("estudiante", "e@example.com", "pass12345")
        self.subject = Subject.objects.create(name="Matematica", is_active=True)
        self.topic = Topic.objects.create(
            name="Algebra", subject=self.subject, is_active=True
        )
        self.resource = Resource.objects.create(
            title="Guia 1",
            subject=self.subject,
            topic=self.topic,
            is_published=True,
        )

    def _toggle_url(self):
        return reverse(
            "content:resource_toggle_completion", kwargs={"slug": self.resource.slug}
        )

    def test_toggle_requires_login(self):
        response = self.client.post(self._toggle_url())
        self.assertEqual(response.status_code, 302)
        self.assertIn("/cuentas/login/", response.url)
        self.assertEqual(ResourceCompletion.objects.count(), 0)

    def test_toggle_creates_then_removes_completion(self):
        self.client.force_login(self.user)

        self.client.post(self._toggle_url())
        self.assertTrue(
            ResourceCompletion.objects.filter(
                user=self.user, resource=self.resource
            ).exists()
        )

        self.client.post(self._toggle_url())
        self.assertFalse(
            ResourceCompletion.objects.filter(
                user=self.user, resource=self.resource
            ).exists()
        )

    def test_htmx_toggle_returns_button_partial(self):
        self.client.force_login(self.user)
        response = self.client.post(self._toggle_url(), HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "includes/completion_button.html")
        self.assertContains(response, "Comprendido")

    def test_topic_detail_reports_progress(self):
        self.client.force_login(self.user)
        ResourceCompletion.objects.create(user=self.user, resource=self.resource)

        response = self.client.get(
            reverse("content:topic_detail", kwargs={"slug": self.topic.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["completed_count"], 1)
        self.assertEqual(response.context["total_count"], 1)
        self.assertEqual(response.context["completed_percent"], 100)
        self.assertContains(response, "1/1 comprendidos")
