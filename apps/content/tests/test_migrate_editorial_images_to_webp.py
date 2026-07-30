import tempfile
from io import BytesIO, StringIO
from pathlib import Path
from unittest import mock

from django.core.management import call_command
from django.test import TestCase
from PIL import Image

from apps.content.management.commands import migrate_editorial_images_to_webp as migrate_cmd
from apps.content.models import PublicationItem, QuizGuide, Resource
from apps.content.services.editorial_asset_service import BucketConfig

GUIDE_WITH_REQUIRED_HEADINGS = (
    "## Explicación formal\nContenido formal.\n\n"
    "## Definiciones clave\nDefinición clave.\n\n"
    "## Al terminar debes poder\nCerrar el tema correctamente y comprobar el resultado."
)
GUIDE_MISSING_CLOSING = "## Definiciones clave\nDefinición clave.\n"


def _png_bytes(size=(300, 200)):
    image = Image.new("RGB", size, "white")
    out = BytesIO()
    image.save(out, format="PNG")
    return out.getvalue()


class _FakeBody:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return self._payload


def _fake_get_object(payload, content_type="image/png"):
    def handler(**kwargs):
        return {"Body": _FakeBody(payload), "ContentType": content_type}

    return handler


@mock.patch("apps.content.services.editorial_asset_service.get_bucket_config")
@mock.patch("apps.content.services.editorial_asset_service._s3_client")
class MigrateEditorialImagesToWebpTests(TestCase):
    def setUp(self):
        self.png = _png_bytes()
        tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(tmp_dir.cleanup)
        patcher = mock.patch.object(migrate_cmd, "BACKUP_DIR", Path(tmp_dir.name))
        self.backup_dir = Path(tmp_dir.name)
        patcher.start()
        self.addCleanup(patcher.stop)

    def _configure_fake_bucket(self, s3_client, get_config):
        get_config.return_value = BucketConfig(
            endpoint="https://bucket.test",
            access_key_id="key",
            secret_access_key="secret",
            bucket_name="assets",
            region="auto",
        )
        client = mock.MagicMock()
        client.get_object.side_effect = _fake_get_object(self.png)
        s3_client.return_value = client
        return client

    def _resource(self, **overrides):
        defaults = dict(
            title="Recurso legado",
            slug=overrides.pop("slug", "recurso-legado"),
            is_published=True,
            content=GUIDE_WITH_REQUIRED_HEADINGS,
            infographic_key="editorial-infographics/1/old.png",
            concept_image_key="editorial-concept-images/1/old.png",
        )
        defaults.update(overrides)
        return Resource.objects.create(**defaults)

    def test_dry_run_reports_candidates_without_writing(self, s3_client, get_config):
        self._configure_fake_bucket(s3_client, get_config)
        resource = self._resource()

        out = StringIO()
        call_command("migrate_editorial_images_to_webp", "--dry-run", stdout=out)

        resource.refresh_from_db()
        self.assertTrue(resource.infographic_key.endswith(".png"))
        self.assertTrue(resource.concept_image_key.endswith(".png"))
        output = out.getvalue()
        self.assertIn(str(resource.id), output)
        self.assertIn("WEBP", output)
        self.assertIn("2 candidatos (dry-run)", output)

    def test_apply_migrates_direct_resource_and_syncs_content(self, s3_client, get_config):
        client = self._configure_fake_bucket(s3_client, get_config)
        resource = self._resource()

        out = StringIO()
        call_command("migrate_editorial_images_to_webp", "--apply", stdout=out)

        resource.refresh_from_db()
        self.assertTrue(resource.infographic_key.endswith(".webp"))
        self.assertTrue(resource.concept_image_key.endswith(".webp"))
        self.assertIn("?asset=infographic", resource.content)
        self.assertIn("?asset=concept", resource.content)
        self.assertEqual(client.put_object.call_count, 2)
        for call in client.put_object.call_args_list:
            self.assertEqual(call.kwargs["ContentType"], "image/webp")

    def test_apply_syncs_canonical_quiz_guide(self, s3_client, get_config):
        self._configure_fake_bucket(s3_client, get_config)
        resource = self._resource()
        guide = QuizGuide.objects.create(
            title="Guía canónica",
            content_text=resource.content,
            canonical_resource=resource,
        )
        PublicationItem.objects.create(
            batch_id="batch-1",
            source_filename="video.mp4",
            resource=resource,
            canonical_guide=guide,
            state=PublicationItem.STATE_PUBLISHED,
        )

        call_command("migrate_editorial_images_to_webp", "--apply", stdout=StringIO())

        resource.refresh_from_db()
        guide.refresh_from_db()
        self.assertIn("?asset=infographic", guide.content_text)
        self.assertIn("?asset=concept", guide.content_text)
        self.assertEqual(resource.content, guide.content_text)

    def test_idempotent_second_run_finds_zero_candidates(self, s3_client, get_config):
        self._configure_fake_bucket(s3_client, get_config)
        self._resource()
        call_command("migrate_editorial_images_to_webp", "--apply", stdout=StringIO())

        out = StringIO()
        call_command("migrate_editorial_images_to_webp", "--dry-run", stdout=out)

        self.assertIn("0 candidatos", out.getvalue())

    def test_webp_resources_are_skipped(self, s3_client, get_config):
        self._configure_fake_bucket(s3_client, get_config)
        self._resource(
            slug="ya-webp",
            infographic_key="editorial-infographics/2/already.webp",
            concept_image_key="editorial-concept-images/2/already.webp",
        )

        out = StringIO()
        call_command("migrate_editorial_images_to_webp", "--dry-run", stdout=out)

        self.assertIn("0 candidatos", out.getvalue())

    def test_resource_failure_rolls_back_and_continues(self, s3_client, get_config):
        client = self._configure_fake_bucket(s3_client, get_config)
        broken = self._resource(
            slug="recurso-roto",
            content=GUIDE_MISSING_CLOSING,
            concept_image_key="",
        )
        healthy = self._resource(slug="recurso-sano")

        out = StringIO()
        call_command("migrate_editorial_images_to_webp", "--apply", stdout=out)

        broken.refresh_from_db()
        healthy.refresh_from_db()
        self.assertTrue(broken.infographic_key.endswith(".png"))
        self.assertEqual(broken.content, GUIDE_MISSING_CLOSING)
        self.assertTrue(healthy.infographic_key.endswith(".webp"))
        self.assertTrue(healthy.concept_image_key.endswith(".webp"))
        self.assertIn("1 aplicados", out.getvalue())
        self.assertIn("1 fallidos", out.getvalue())

    def test_concurrent_migration_of_same_resource_does_not_recompress(self, s3_client, get_config):
        """Reproduce el incidente real: dos corridas procesan el mismo recurso.
        La segunda debe detectar bajo el lock que ya no es legado y omitirlo,
        en vez de recomprimir el WebP ya subido (pérdida generacional)."""
        client = self._configure_fake_bucket(s3_client, get_config)
        resource = self._resource()
        kinds = migrate_cmd._candidate_kinds(resource)

        first = migrate_cmd._apply_one_resource(resource, kinds)
        self.assertEqual(first["status"], "migrated")
        put_calls_after_first = client.put_object.call_count

        second = migrate_cmd._apply_one_resource(resource, kinds)

        self.assertEqual(second["status"], "omitted")
        self.assertEqual(client.put_object.call_count, put_calls_after_first)
