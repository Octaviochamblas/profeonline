from django.db import models
from django.utils.text import slugify


class Topic(models.Model):
    subject = models.ForeignKey(
        "content.Subject",
        on_delete=models.CASCADE,
        related_name="topics",
        verbose_name="asignatura",
    )
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["subject__name", "name"]
        verbose_name = "tema"
        verbose_name_plural = "temas"
        constraints = [
            models.UniqueConstraint(
                fields=["subject", "name"],
                name="unique_topic_name_per_subject",
            )
        ]

    def __str__(self) -> str:
        return f"{self.subject.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Topic.objects.filter(subject=self.subject, slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)