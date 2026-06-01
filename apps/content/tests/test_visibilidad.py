from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
import django.db

from apps.content.models import (
    Choice,
    Question,
    Resource,
    ResourceCompletion,
    Subject,
    Topic,
    XPEvent,
)


class TopicProgressCardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("estudiante", "e@example.com", "pass123")
        self.subject = Subject.objects.create(name="Matemáticas", is_active=True)
        from apps.content.models import Level
        self.level = Level.objects.create(name="Escolar", order=1, is_active=True)

        # Topic 1: 2 resources
        self.topic1 = Topic.objects.create(name="Álgebra", subject=self.subject, is_active=True)
        self.r1 = Resource.objects.create(title="Ecuaciones", subject=self.subject, topic=self.topic1, is_published=True)
        self.r1.levels.set([self.level])
        self.r2 = Resource.objects.create(title="Inecuaciones", subject=self.subject, topic=self.topic1, is_published=True)
        self.r2.levels.set([self.level])

        # Topic 2: 0 resources
        self.topic2 = Topic.objects.create(name="Geometría", subject=self.subject, is_active=True)

    def test_anonymous_user_no_crash(self):
        # Anonymous users shouldn't see progress but page should render fine
        url = reverse("content:topic_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "de 2 comprendidos")
        self.assertNotContains(response, "de 0 comprendidos")

    def test_authenticated_user_progress_in_cards(self):
        self.client.force_login(self.user)
        # Mark 1 resource as completed (comprehended)
        ResourceCompletion.objects.create(user=self.user, resource=self.r1)

        url = reverse("content:topic_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Check topic 1 progress (1 of 2 completed = 50%)
        self.assertContains(response, "1 de 2 comprendidos")
        # Check topic 2 progress (0 of 0 completed = 0%)
        self.assertContains(response, "0 de 0 comprendidos")

    def test_no_n_plus_1_queries_for_topic_list(self):
        self.client.force_login(self.user)
        ResourceCompletion.objects.create(user=self.user, resource=self.r1)

        # Warm up
        self.client.get(reverse("content:topic_list"))

        django.db.reset_queries()
        self.client.get(reverse("content:topic_list"))
        base_queries = len(django.db.connection.queries)

        # Add 5 more topics with resources
        for i in range(5):
            t = Topic.objects.create(name=f"Tema {i}", subject=self.subject, is_active=True)
            r = Resource.objects.create(title=f"Recurso {i}", subject=self.subject, topic=t, is_published=True)
            r.levels.set([self.level])

        django.db.reset_queries()
        self.client.get(reverse("content:topic_list"))
        new_queries = len(django.db.connection.queries)

        # The number of queries should remain unchanged (O(1) respect to number of topics)
        self.assertEqual(base_queries, new_queries)


class TopicDetailProgressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("estudiante", "e@example.com", "pass123")
        self.subject = Subject.objects.create(name="Matemáticas", is_active=True)
        self.topic = Topic.objects.create(name="Álgebra", subject=self.subject, is_active=True)
        self.r1 = Resource.objects.create(title="Ecuaciones", subject=self.subject, topic=self.topic, is_published=True)
        self.r2 = Resource.objects.create(title="Inecuaciones", subject=self.subject, topic=self.topic, is_published=True)

    def test_topic_detail_division_by_zero_protected(self):
        self.client.force_login(self.user)
        # Topic with 0 resources
        empty_topic = Topic.objects.create(name="Vacío", subject=self.subject, is_active=True)
        url = reverse("content:topic_detail", kwargs={"slug": empty_topic.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["stars_total"], 0)
        self.assertEqual(response.context["stars_percent"], 0)

    def test_stars_total_calculation_with_fewer_published_levels(self):
        # We publish questions for level 1 on r1, and level 1 and 2 on r2
        # r1 has level 1 published (1 level)
        q1 = Question.objects.create(resource=self.r1, level=1, text="Q1", status="publicada")
        Choice.objects.create(question=q1, text="C1", is_correct=True)

        # r2 has level 1 and 2 published (2 levels)
        q2 = Question.objects.create(resource=self.r2, level=1, text="Q2", status="publicada")
        Choice.objects.create(question=q2, text="C2", is_correct=True)
        q3 = Question.objects.create(resource=self.r2, level=2, text="Q3", status="publicada")
        Choice.objects.create(question=q3, text="C3", is_correct=True)

        # total published levels across all resources in this topic is 1 (for r1) + 2 (for r2) = 3
        # So stars_total should be 3
        self.client.force_login(self.user)
        url = reverse("content:topic_detail", kwargs={"slug": self.topic.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["stars_total"], 3)

    def test_comprehension_does_not_award_xp(self):
        self.client.force_login(self.user)
        xp_before = XPEvent.objects.filter(user=self.user).count()

        # Mark resource as completed
        toggle_url = reverse("content:resource_toggle_completion", kwargs={"slug": self.r1.slug})
        self.client.post(toggle_url)

        xp_after = XPEvent.objects.filter(user=self.user).count()
        self.assertEqual(xp_before, xp_after)

    def test_draft_questions_not_visible(self):
        # Create a draft question
        q = Question.objects.create(resource=self.r1, level=1, text="Draft Question Text", status="borrador")
        Choice.objects.create(question=q, text="C", is_correct=True)

        self.client.force_login(self.user)
        url = reverse("content:resource_detail", kwargs={"slug": self.r1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # It shouldn't render draft question text
        self.assertNotContains(response, "Draft Question Text")
        # It should render quiz section and the empty state message
        self.assertContains(response, "quiz-section")
        self.assertContains(response, "Aún no hay ejercicios publicados para este nivel")

    def test_draft_questions_hint_visible_to_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)

        # Create a draft question and a published question so that quiz section is available
        q_pub = Question.objects.create(resource=self.r1, level=1, text="Published Question", status="publicada")
        Choice.objects.create(question=q_pub, text="C", is_correct=True)

        q_draft = Question.objects.create(resource=self.r1, level=1, text="Draft Question", status="borrador")
        Choice.objects.create(question=q_draft, text="C", is_correct=True)

        url = reverse("content:resource_detail", kwargs={"slug": self.r1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hay 1 pregunta en borrador")
