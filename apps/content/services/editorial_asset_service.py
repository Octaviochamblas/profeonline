"""Persistent editorial image storage backed by a Railway Bucket."""

from __future__ import annotations

import hashlib
import mimetypes
import os
import warnings
from dataclasses import dataclass
from io import BytesIO

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from PIL import Image, ImageOps, UnidentifiedImageError


MAX_INFOGRAPHIC_BYTES = 8 * 1024 * 1024
MAX_WEB_IMAGE_SIZE = (1920, 2400)
INFOGRAPHIC_WEBP_QUALITY = 95
CONCEPT_WEBP_QUALITY = 88
ALLOWED_IMAGES = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
}


@dataclass(frozen=True)
class BucketConfig:
    endpoint: str
    access_key_id: str
    secret_access_key: str
    bucket_name: str
    region: str


def get_bucket_config() -> BucketConfig:
    values = {
        "endpoint": getattr(settings, "AWS_ENDPOINT_URL", "")
        or os.environ.get("AWS_ENDPOINT_URL", ""),
        "access_key_id": getattr(settings, "AWS_ACCESS_KEY_ID", "")
        or os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "secret_access_key": getattr(settings, "AWS_SECRET_ACCESS_KEY", "")
        or os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        "bucket_name": getattr(settings, "AWS_S3_BUCKET_NAME", "")
        or os.environ.get("AWS_S3_BUCKET_NAME", ""),
        "region": getattr(settings, "AWS_DEFAULT_REGION", "")
        or os.environ.get("AWS_DEFAULT_REGION", "auto"),
    }
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise ImproperlyConfigured(
            "Railway Storage Bucket no está configurado "
            "(faltan variables de almacenamiento)."
        )
    return BucketConfig(**values)


def _s3_client():
    try:
        import boto3
    except ImportError as exc:  # pragma: no cover - only occurs in a misconfigured deploy.
        raise ImproperlyConfigured(
            "Falta boto3 para usar Railway Storage Bucket."
        ) from exc
    config = get_bucket_config()
    return boto3.client(
        "s3",
        endpoint_url=config.endpoint,
        region_name=config.region,
        aws_access_key_id=config.access_key_id,
        aws_secret_access_key=config.secret_access_key,
    )


def _source_image_payload(uploaded_file) -> tuple[bytes, str]:
    if uploaded_file.size > MAX_INFOGRAPHIC_BYTES:
        raise ValidationError("La imagen no puede superar 8 MB.")
    payload = uploaded_file.read()
    if not payload:
        raise ValidationError("La imagen está vacía.")
    content_type = (uploaded_file.content_type or "").lower()
    if content_type not in ALLOWED_IMAGES:
        content_type = mimetypes.guess_type(uploaded_file.name)[0] or ""
    if content_type not in ALLOWED_IMAGES:
        raise ValidationError("La imagen debe ser PNG, JPEG o WebP.")
    signatures = {
        "image/png": payload.startswith(b"\x89PNG\r\n\x1a\n"),
        "image/jpeg": payload.startswith(b"\xff\xd8\xff"),
        "image/webp": payload[:4] == b"RIFF" and payload[8:12] == b"WEBP",
    }
    if not signatures[content_type]:
        raise ValidationError("El archivo no coincide con el tipo de imagen declarado.")
    return payload, content_type


def _optimized_image_payload(
    uploaded_file,
    *,
    quality: int,
) -> tuple[bytes, str, str]:
    source, content_type = _source_image_payload(uploaded_file)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(source)) as opened:
                image = ImageOps.exif_transpose(opened)
                image.load()
    except (
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
        UnidentifiedImageError,
        OSError,
    ) as exc:
        raise ValidationError("No se pudo procesar la imagen de forma segura.") from exc

    has_alpha = "A" in image.getbands() or "transparency" in image.info
    target_mode = "RGBA" if has_alpha else "RGB"
    if image.mode != target_mode:
        image = image.convert(target_mode)

    original_size = image.size
    image.thumbnail(MAX_WEB_IMAGE_SIZE, Image.Resampling.LANCZOS)
    output = BytesIO()
    image.save(output, format="WEBP", quality=quality, method=6, exact=has_alpha)
    optimized = output.getvalue()

    if (
        content_type == "image/webp"
        and image.size == original_size
        and len(source) <= len(optimized)
    ):
        return source, "image/webp", ".webp"
    return optimized, "image/webp", ".webp"


def upload_infographic(resource, uploaded_file, alt_text: str = "") -> str:
    """Optimizes and stores an immutable infographic for web delivery."""
    payload, content_type, extension = _optimized_image_payload(
        uploaded_file,
        quality=INFOGRAPHIC_WEBP_QUALITY,
    )
    digest = hashlib.sha256(payload).hexdigest()
    config = get_bucket_config()
    key = f"editorial-infographics/{resource.id}/{digest[:24]}{extension}"
    _s3_client().put_object(
        Bucket=config.bucket_name,
        Key=key,
        Body=payload,
        ContentType=content_type,
        CacheControl="public, max-age=31536000, immutable",
    )
    resource.infographic_key = key
    resource.infographic_alt_text = (
        alt_text or f"Infografía de repaso: {resource.title}"
    ).strip()[:240]
    resource.save(update_fields=["infographic_key", "infographic_alt_text"])
    return key


def upload_concept_image(resource, uploaded_file, alt_text: str = "") -> str:
    """Optimizes and stores a conceptual image without replacing the infographic."""
    payload, content_type, extension = _optimized_image_payload(
        uploaded_file,
        quality=CONCEPT_WEBP_QUALITY,
    )
    digest = hashlib.sha256(payload).hexdigest()
    config = get_bucket_config()
    key = f"editorial-concept-images/{resource.id}/{digest[:24]}{extension}"
    _s3_client().put_object(
        Bucket=config.bucket_name,
        Key=key,
        Body=payload,
        ContentType=content_type,
        CacheControl="public, max-age=31536000, immutable",
    )
    resource.concept_image_key = key
    resource.concept_image_alt_text = (
        alt_text or f"Explicación visual integrada: {resource.title}"
    ).strip()[:240]
    resource.save(update_fields=["concept_image_key", "concept_image_alt_text"])
    return key


def get_infographic_object(resource):
    if not resource.infographic_key:
        return None
    config = get_bucket_config()
    return _s3_client().get_object(
        Bucket=config.bucket_name,
        Key=resource.infographic_key,
    )


def get_concept_image_object(resource):
    if not resource.concept_image_key:
        return None
    config = get_bucket_config()
    return _s3_client().get_object(
        Bucket=config.bucket_name,
        Key=resource.concept_image_key,
    )
