from io import BytesIO
from random import Random
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from apps.content.models import Resource
from apps.content.services.editorial_asset_service import (
    BucketConfig,
    INFOGRAPHIC_WEBP_QUALITY,
    MAX_WEB_IMAGE_SIZE,
    _optimized_image_payload,
    upload_concept_image,
    upload_infographic,
)


def _image_file(
    *,
    name="source.png",
    size=(640, 480),
    mode="RGB",
    payload=None,
):
    image = Image.new(mode, size, (255, 255, 255, 0) if mode == "RGBA" else "white")
    if payload is not None:
        image = Image.frombytes(mode, size, payload)
    output = BytesIO()
    image.save(output, format="PNG")
    return SimpleUploadedFile(name, output.getvalue(), content_type="image/png")


class EditorialAssetOptimizationTests(TestCase):
    def test_png_is_compressed_to_webp(self):
        size = (640, 480)
        source = _image_file(
            size=size,
            payload=Random(42).randbytes(size[0] * size[1] * 3),
        )
        source_size = source.size

        payload, content_type, extension = _optimized_image_payload(
            source,
            quality=INFOGRAPHIC_WEBP_QUALITY,
        )

        self.assertEqual(content_type, "image/webp")
        self.assertEqual(extension, ".webp")
        self.assertTrue(payload.startswith(b"RIFF"))
        self.assertEqual(payload[8:12], b"WEBP")
        self.assertLess(len(payload), source_size)

    def test_large_image_is_resized_without_upscaling(self):
        source = _image_file(size=(2400, 1800))

        payload, _, _ = _optimized_image_payload(
            source,
            quality=INFOGRAPHIC_WEBP_QUALITY,
        )

        with Image.open(BytesIO(payload)) as optimized:
            self.assertLessEqual(optimized.width, MAX_WEB_IMAGE_SIZE[0])
            self.assertLessEqual(optimized.height, MAX_WEB_IMAGE_SIZE[1])
            self.assertEqual(optimized.size, (1920, 1440))

    def test_transparency_is_preserved(self):
        image = Image.new("RGBA", (240, 120), (255, 255, 255, 0))
        image.paste((20, 40, 180, 255), (40, 20, 200, 100))
        output = BytesIO()
        image.save(output, format="PNG")
        source = SimpleUploadedFile(
            "transparent.png",
            output.getvalue(),
            content_type="image/png",
        )

        payload, _, _ = _optimized_image_payload(
            source,
            quality=INFOGRAPHIC_WEBP_QUALITY,
        )

        with Image.open(BytesIO(payload)) as optimized:
            self.assertEqual(optimized.mode, "RGBA")
            self.assertEqual(optimized.getchannel("A").getextrema(), (0, 255))

    @mock.patch("apps.content.services.editorial_asset_service._s3_client")
    @mock.patch("apps.content.services.editorial_asset_service.get_bucket_config")
    def test_both_editorial_uploads_store_webp(self, get_config, s3_client):
        get_config.return_value = BucketConfig(
            endpoint="https://bucket.test",
            access_key_id="key",
            secret_access_key="secret",
            bucket_name="assets",
            region="auto",
        )
        resource = Resource.objects.create(title="Movimiento")

        infographic_key = upload_infographic(resource, _image_file(), "Resumen visual")
        concept_key = upload_concept_image(resource, _image_file(), "Explicacion visual")

        self.assertTrue(infographic_key.endswith(".webp"))
        self.assertTrue(concept_key.endswith(".webp"))
        self.assertEqual(s3_client.return_value.put_object.call_count, 2)
        for call in s3_client.return_value.put_object.call_args_list:
            self.assertEqual(call.kwargs["ContentType"], "image/webp")
            self.assertLessEqual(len(call.kwargs["Body"]), 8 * 1024 * 1024)
