import mimetypes
from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


def validate_file_mime(value):
    mime_type, _ = mimetypes.guess_type(value.name)
    allowed_mimes = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "image/png",
        "image/jpeg",
        "application/zip",
        "application/x-zip-compressed",
    ]
    if not mime_type or mime_type not in allowed_mimes:
        raise ValidationError("El tipo de archivo (MIME) no está permitido o no es válido.")


def validate_file_size(value):
    # Límite de 10MB
    limit_mb = 10
    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(f"El archivo no puede pesar más de {limit_mb}MB.")


class Resource(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(
        "content.Subject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resources",
        verbose_name="asignatura",
    )

    topic = models.ForeignKey(
        "content.Topic",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resources",
        verbose_name="tema",
    )

    levels = models.ManyToManyField(
        "content.Level",
        blank=True,
        related_name="resources",
        verbose_name="niveles",
    )

    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    description = models.TextField("Descripción breve", blank=True)
    content = models.TextField("Contenido", blank=True)
    file = models.FileField(
        upload_to="resources/files/",
        blank=True,
        null=True,
        verbose_name="archivo descargable",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "png", "jpg", "jpeg", "zip"]),
            validate_file_size,
            validate_file_mime,
        ]
    )
    video_url = models.URLField(
        "URL del video de YouTube",
        blank=True,
        null=True,
    )

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0, blank=True, verbose_name="orden manual")

    class Meta:
        ordering = ["title"]
        verbose_name = "recurso"
        verbose_name_plural = "recursos"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Resource.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
