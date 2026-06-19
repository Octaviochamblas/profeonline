import json
import os
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.content.models import (
    Choice,
    PublicationItem,
    Question,
    QuizAttempt,
    QuizAttemptAnswer,
    Resource,
    Subject,
    Topic,
)
from apps.content.services.publication_pipeline_service import (
    PipelineError,
    finalize_publication,
    process_publication_item,
)

TOKEN = "pipeline-test-token"
VIDEO_ID = "pipe1234XYZ"


def _counts_one_question():
    return {
        "1": {
            "practice": {"pool": 1, "shown": 1},
            "eval": {"pool": 0, "shown": 0},
        },
        "2": {
            "practice": {"pool": 0, "shown": 0},
            "eval": {"pool": 0, "shown": 0},
        },
        "3": {
            "practice": {"pool": 0, "shown": 0},
            "eval": {"pool": 0, "shown": 0},
        },
    }


def _canonical(_item):
    return {
        "resource_title": "Suma de enteros con signos",
        "youtube_title": "Cómo sumar números enteros con signos",
        "resource_description": "Aprende a sumar enteros positivos y negativos.",
        "youtube_description": "Clase sobre suma de enteros basada en ejemplos resueltos.",
        "introduction": "Introducción a la suma de enteros con signos.",
        "guide_title": "Guía canónica: suma de enteros",
        "pedagogical_document": (
            "Objetivo: sumar enteros. Conceptos: signo positivo y negativo. "
            "Procedimiento: comparar signos, operar valores y conservar el signo. "
            "Ejemplo presente: sumar una ganancia y una deuda. Error advertido: "
            "sumar los signos sin comparar valores. Límite: no incluye multiplicación."
        ),
    }


def _candidate_generator(**_kwargs):
    return [{
        "text": "¿Cuál es el resultado de sumar -3 y 5?",
        "explanation": "Se comparan los valores absolutos y se conserva el signo de 5: 2.",
        "cognitive_type": "aplicacion",
        "choices": [
            {"text": "2", "is_correct": True},
            {"text": "-2", "is_correct": False},
            {"text": "8", "is_correct": False},
            {"text": "-8", "is_correct": False},
        ],
    }]


def _auditor(_item, _level, _mode, candidates):
    return candidates, {
        0: {
            "accepted": True,
            "cognitive_type": "aplicacion",
            "audited_by": "test",
        }
    }


class PublicationPipelineServiceTests(TestCase):
    def setUp(self):
        subject = Subject.objects.create(name="Matemática pipeline")
        topic = Topic.objects.create(name="Enteros pipeline", subject=subject)
        transcript = " ".join(
            ["En esta clase sumamos números enteros positivos y negativos con ejemplos."] * 12
        )
        self.resource = Resource.objects.create(
            title="Temporal",
            subject=subject,
            topic=topic,
            transcript=transcript,
            video_url=f"https://youtu.be/{VIDEO_ID}",
            is_published=False,
        )
        self.item = PublicationItem.objects.create(
            batch_id="batch-test",
            source_filename="clase.mp4",
            youtube_video_id=VIDEO_ID,
            youtube_url=self.resource.video_url,
            resource=self.resource,
            target_counts=_counts_one_question(),
            taxonomy={"education_level": "media"},
        )

    def test_pipeline_creates_canonical_guide_and_audited_drafts_idempotently(self):
        process_publication_item(
            self.item,
            metadata_generator=_canonical,
            candidate_generator=_candidate_generator,
            auditor=_auditor,
        )
        self.item.refresh_from_db()
        self.resource.refresh_from_db()
        self.assertEqual(self.item.state, PublicationItem.STATE_QUESTIONS_READY)
        self.assertFalse(self.resource.is_published)
        self.assertEqual(self.resource.title, "Temporal")
        self.assertEqual(self.resource.canonical_quiz_guide, self.item.canonical_guide)
        question = Question.objects.get(publication_item=self.item)
        self.assertEqual(question.status, "borrador")
        self.assertTrue(question.audit_data["accepted"])
        self.assertEqual(question.choices.filter(is_correct=True).count(), 1)

        process_publication_item(
            self.item,
            metadata_generator=_canonical,
            candidate_generator=_candidate_generator,
            auditor=_auditor,
        )
        self.assertEqual(Question.objects.filter(publication_item=self.item).count(), 1)

    def test_insufficient_transcript_stops_without_calling_ai(self):
        self.resource.transcript = "demasiado corto"
        self.resource.save(update_fields=["transcript"])
        generator = mock.Mock()
        process_publication_item(self.item, metadata_generator=generator)
        self.item.refresh_from_db()
        self.assertEqual(self.item.state, PublicationItem.STATE_TRANSCRIPT_PENDING)
        self.assertFalse(Question.objects.filter(publication_item=self.item).exists())
        generator.assert_not_called()

    def test_finalize_requires_public_youtube_and_publishes_atomically(self):
        process_publication_item(
            self.item,
            metadata_generator=_canonical,
            candidate_generator=_candidate_generator,
            auditor=_auditor,
        )
        with self.assertRaises(PipelineError):
            finalize_publication(self.item)
        self.item.youtube_privacy = "public"
        self.item.save(update_fields=["youtube_privacy"])
        finalize_publication(self.item)
        self.item.refresh_from_db()
        self.resource.refresh_from_db()
        self.assertEqual(self.item.state, PublicationItem.STATE_PUBLISHED)
        self.assertTrue(self.resource.is_published)
        self.assertEqual(self.resource.title, "Suma de enteros con signos")
        self.assertEqual(
            Question.objects.get(publication_item=self.item).status,
            "publicada",
        )

    def test_pipeline_never_touches_historical_questions(self):
        old = Question.objects.create(
            resource=self.resource,
            level=2,
            mode="evaluacion",
            text="Pregunta histórica",
            explanation="Explicación histórica",
            status="publicada",
        )
        Choice.objects.create(question=old, text="Correcta", is_correct=True)
        process_publication_item(
            self.item,
            metadata_generator=_canonical,
            candidate_generator=_candidate_generator,
            auditor=_auditor,
        )
        self.assertTrue(Question.objects.filter(pk=old.pk, status="publicada").exists())

    def test_rejected_candidates_are_regenerated_until_covered(self):
        calls = {"n": 0}

        def flaky_auditor(_item, _level, _mode, candidates):
            calls["n"] += 1
            if calls["n"] == 1:
                return [], {}
            return candidates, {
                0: {"accepted": True, "cognitive_type": "aplicacion", "audited_by": "test"}
            }

        process_publication_item(
            self.item,
            metadata_generator=_canonical,
            candidate_generator=_candidate_generator,
            auditor=flaky_auditor,
        )
        self.item.refresh_from_db()
        self.assertEqual(self.item.state, PublicationItem.STATE_QUESTIONS_READY)
        self.assertEqual(Question.objects.filter(publication_item=self.item).count(), 1)
        self.assertGreaterEqual(calls["n"], 2)

    def test_regeneration_exhaustion_raises_without_partial_questions(self):
        def reject_all(_item, _level, _mode, _candidates):
            return [], {}

        with self.assertRaises(PipelineError):
            process_publication_item(
                self.item,
                metadata_generator=_canonical,
                candidate_generator=_candidate_generator,
                auditor=reject_all,
            )
        self.assertFalse(Question.objects.filter(publication_item=self.item).exists())
        self.item.refresh_from_db()
        self.assertEqual(self.item.state, PublicationItem.STATE_METADATA_READY)


class PublicationPipelineApiTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Física pipeline")
        self.topic = Topic.objects.create(name="Ondas pipeline", subject=self.subject)
        self.create_url = reverse("content:api_create_resource_from_video")

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": TOKEN})
    def test_webhook_upserts_pipeline_item_and_forces_draft(self):
        payload = {
            "batch_id": "batch-api",
            "source_filename": "ondas.mp4",
            "title": "Temporal",
            "video_url": f"https://youtu.be/{VIDEO_ID}",
            "transcript": " ".join(["Transcripción real sobre ondas y frecuencia."] * 20),
            "subject_slug": self.subject.slug,
            "topic_slug": self.topic.slug,
            "is_published": True,
        }
        first = self.client.post(
            self.create_url,
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_X_API_TOKEN=TOKEN,
        )
        second = self.client.post(
            self.create_url,
            data=json.dumps({**payload, "video_url": f"https://youtube.com/watch?v={VIDEO_ID}"}),
            content_type="application/json",
            HTTP_X_API_TOKEN=TOKEN,
        )
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(Resource.objects.filter(video_url__icontains=VIDEO_ID).count(), 1)
        self.assertEqual(PublicationItem.objects.count(), 1)
        self.assertFalse(Resource.objects.get().is_published)

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": TOKEN})
    def test_existing_published_resource_keeps_live_version_until_finalize(self):
        resource = Resource.objects.create(
            title="Versión vigente",
            video_url=f"https://youtu.be/{VIDEO_ID}",
            is_published=True,
        )
        response = self.client.post(
            self.create_url,
            data=json.dumps({
                "batch_id": "batch-existing",
                "source_filename": "existing.mp4",
                "title": "Título temporal",
                "video_url": f"https://youtube.com/watch?v={VIDEO_ID}",
                "transcript": " ".join(["Transcript actualizado y verificable."] * 20),
                "is_published": False,
            }),
            content_type="application/json",
            HTTP_X_API_TOKEN=TOKEN,
        )
        self.assertEqual(response.status_code, 200)
        resource.refresh_from_db()
        self.assertTrue(resource.is_published)
        self.assertEqual(resource.title, "Versión vigente")

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": TOKEN})
    def test_status_does_not_expose_metadata_before_ready(self):
        resource = Resource.objects.create(title="R", is_published=False)
        item = PublicationItem.objects.create(
            batch_id="b",
            source_filename="f.mp4",
            resource=resource,
            metadata={"youtube_title": "privado"},
        )
        response = self.client.get(
            reverse("content:api_publication_item_status", args=[item.id]),
            HTTP_X_API_TOKEN=TOKEN,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["metadata"], {})

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": TOKEN})
    def test_failed_confirmation_does_not_persist_public_privacy(self):
        resource = Resource.objects.create(title="R2", is_published=False)
        item = PublicationItem.objects.create(
            batch_id="b2",
            source_filename="f2.mp4",
            resource=resource,
            state=PublicationItem.STATE_METADATA_READY,
        )
        response = self.client.post(
            reverse("content:api_confirm_publication_item", args=[item.id]),
            data=json.dumps({"youtube_privacy": "public"}),
            content_type="application/json",
            HTTP_X_API_TOKEN=TOKEN,
        )
        self.assertEqual(response.status_code, 409)
        item.refresh_from_db()
        self.assertEqual(item.youtube_privacy, "unlisted")

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": TOKEN})
    def test_status_and_confirm_endpoints_require_token(self):
        resource = Resource.objects.create(title="RX", is_published=False)
        item = PublicationItem.objects.create(
            batch_id="bx", source_filename="fx.mp4", resource=resource
        )
        status_resp = self.client.get(
            reverse("content:api_publication_item_status", args=[item.id])
        )
        confirm_resp = self.client.post(
            reverse("content:api_confirm_publication_item", args=[item.id]),
            data=json.dumps({"youtube_privacy": "public"}),
            content_type="application/json",
        )
        self.assertEqual(status_resp.status_code, 401)
        self.assertEqual(confirm_resp.status_code, 401)


class HistoricalAnswerProtectionTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="pipeline-admin",
            email="pipeline@example.com",
            password="secret",
        )
        self.client.force_login(self.admin)
        self.resource = Resource.objects.create(title="Histórico", is_published=True)
        self.question = Question.objects.create(
            resource=self.resource,
            level=1,
            mode="evaluacion",
            text="Pregunta respondida",
            explanation="Explicación",
            status="publicada",
        )
        self.choice = Choice.objects.create(
            question=self.question,
            text="Respuesta",
            is_correct=True,
        )
        attempt = QuizAttempt.objects.create(
            user=self.admin,
            resource=self.resource,
            level=1,
            mode="evaluacion",
            score=1,
            total=1,
            passed=True,
            attempt_number=1,
        )
        QuizAttemptAnswer.objects.create(
            attempt=attempt,
            question=self.question,
            selected_choice=self.choice,
            is_correct=True,
        )

    def test_question_with_answers_is_archived_not_deleted(self):
        response = self.client.post(
            reverse("content:delete_question", args=[self.question.id])
        )
        self.assertEqual(response.status_code, 409)
        self.question.refresh_from_db()
        self.assertEqual(self.question.status, "archivada")
        self.assertTrue(QuizAttemptAnswer.objects.filter(question=self.question).exists())

    def test_choice_with_answers_cannot_be_deleted(self):
        response = self.client.post(
            reverse("content:delete_choice", args=[self.choice.id])
        )
        self.assertEqual(response.status_code, 409)
        self.assertTrue(Choice.objects.filter(id=self.choice.id).exists())
