from django.db import migrations
from django.db.models import Q
from django.utils.text import slugify


def unique_slug(instance, queryset, scope=None):
    base_slug = slugify(instance.name if hasattr(instance, "name") else instance.title)
    if not base_slug:
        base_slug = f"{instance._meta.model_name}-{instance.pk}"

    slug = base_slug
    counter = 1
    existing = queryset
    if scope:
        existing = existing.filter(**scope)

    while existing.filter(slug=slug).exclude(pk=instance.pk).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


def backfill_public_slugs(apps, schema_editor):
    Area = apps.get_model("content", "Area")
    Subject = apps.get_model("content", "Subject")
    Topic = apps.get_model("content", "Topic")
    Level = apps.get_model("content", "Level")
    Resource = apps.get_model("content", "Resource")

    for model in (Area, Subject, Level, Resource):
        missing_slug_items = model.objects.filter(Q(slug__isnull=True) | Q(slug=""))
        for item in missing_slug_items.order_by("pk"):
            item.slug = unique_slug(item, model.objects.all())
            item.save(update_fields=["slug"])

    missing_topic_slugs = Topic.objects.filter(Q(slug__isnull=True) | Q(slug=""))
    for topic in missing_topic_slugs.order_by("subject_id", "pk"):
        topic.slug = unique_slug(
            topic,
            Topic.objects.all(),
            scope={"subject_id": topic.subject_id},
        )
        topic.save(update_fields=["slug"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0011_populate_math_resources"),
    ]

    operations = [
        migrations.RunPython(backfill_public_slugs, noop_reverse),
    ]
