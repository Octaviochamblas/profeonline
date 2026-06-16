"""El estudio en lote propaga el modo de generación (gen_source) por toda la cadena."""

import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Resource, Subject

User = get_user_model()


class StudioGenSourceTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "a@a.com", "pw")
        self.subject = Subject.objects.create(name="Matemáticas")
        self.resource = Resource.objects.create(
            title="R", subject=self.subject, description="d", content="c", is_published=True,
        )
        self.client.force_login(self.admin)

    def test_post_propaga_gen_source(self):
        data = {
            "resources": [self.resource.id],
            "max_attempts": 3, "pass_threshold": 100, "recovery_rule": "practice_5_5",
            "gen_source": "document",
        }
        for lvl in ("1", "2", "3"):
            data[f"practice_pool_{lvl}"] = 6
            data[f"practice_shown_{lvl}"] = 5
            data[f"eval_pool_{lvl}"] = 4
            data[f"eval_shown_{lvl}"] = 3
        resp = self.client.post(reverse("content:question_studio"), data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'name="gen_source" value="document"', resp.content)

    def test_tanda_reemite_gen_source(self):
        counts = {
            "1": {"practice": {"pool": 3, "shown": 2}, "eval": {"pool": 0, "shown": 0}},
            "2": {"practice": {"pool": 0, "shown": 0}, "eval": {"pool": 0, "shown": 0}},
            "3": {"practice": {"pool": 0, "shown": 0}, "eval": {"pool": 0, "shown": 0}},
        }
        resp = self.client.post(reverse("content:generate_questions_chunk"), {
            "resource_ids[]": [self.resource.id], "current_index": 0, "level": 1, "mode": "practice",
            "batch_offset": 0, "generated_total": 0, "autopublish": "false", "max_attempts": 3,
            "pass_threshold": "1.0", "recovery_rule": "practice_5_5", "allow_retake_passed": "false",
            "counts_data": json.dumps(counts), "gen_source": "document",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'name="gen_source" value="document"', resp.content)
