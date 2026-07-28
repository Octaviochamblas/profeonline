import os
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Resource


class _BucketBody:
    def iter_chunks(self):
        yield b"image-bytes"


class ResourceInfographicTests(TestCase):
    def setUp(self):
        self.resource = Resource.objects.create(
            title="Orden de enteros",
            slug="orden-de-enteros",
            is_published=True,
            infographic_key="editorial-infographics/1/example.png",
        )

    @mock.patch("apps.content.views.resource_detail.get_infographic_object")
    def test_detail_route_serves_infographic_asset(self, get_object):
        get_object.return_value = {
            "Body": _BucketBody(),
            "ContentType": "image/png",
            "ContentLength": 11,
            "CacheControl": "public, max-age=31536000, immutable",
        }

        url = reverse("content:resource_detail", kwargs={"slug": self.resource.slug})
        response = self.client.get(url, {"asset": "infographic"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")
        self.assertEqual(b"".join(response.streaming_content), b"image-bytes")

    @mock.patch.dict(os.environ, {"API_SECRET_TOKEN": "test-token"})
    @mock.patch("apps.content.views.api_video._store_infographic_for_resource")
    def test_upload_api_can_resolve_direct_resource_by_slug(self, store):
        url = reverse(
            "content:api_resource_infographic_upload_by_slug",
            kwargs={"slug": self.resource.slug},
        )
        response = self.client.post(
            url,
            data={
                "image": SimpleUploadedFile(
                    "infografia.png",
                    b"\x89PNG\r\n\x1a\ncontenido",
                    content_type="image/png",
                ),
                "alt_text": "Resumen visual",
            },
            HTTP_X_API_TOKEN="test-token",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["resource_id"], self.resource.id)
        store.assert_called_once()
