from django.db import models
from django.utils.text import slugify


class Module(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    subject = models.ForeignKey(
        "content.Subject",
        on_delete=models.CASCADE,
        related_name="modules",
        verbose_name="asignatura",
    )
    topic = models.ForeignKey(
        "content.Topic",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="modules",
        verbose_name="tema",
    )
    levels = models.ManyToManyField(
        "content.Level",
        blank=True,
        related_name="modules",
        verbose_name="niveles",
    )
    
    resources = models.ManyToManyField(
        "content.Resource",
        through="content.ModuleResource",
        related_name="modules",
        blank=True,
        verbose_name="recursos",
    )
    objective = models.TextField(blank=True, verbose_name="objetivo de aprendizaje")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["subject__name", "order", "title"]
        verbose_name = "módulo"
        verbose_name_plural = "módulos"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Module.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)