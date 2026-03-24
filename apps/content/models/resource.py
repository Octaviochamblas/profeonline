from django.db import models
from django.utils.text import slugify


class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ("text", "Texto"),
        ("video", "Video"),
        ("document", "Documento"),
        ("link", "Enlace"),
    ]

    

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
    description = models.TextField(blank=True)
    content_body = models.TextField(blank=True)
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPE_CHOICES,
        default="text",
    )
    external_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

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