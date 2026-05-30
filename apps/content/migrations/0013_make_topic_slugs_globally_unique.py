from django.db import migrations, models
from django.utils.text import slugify


def backfill_unique_topic_slugs(apps, schema_editor):
    Topic = apps.get_model("content", "Topic")
    used_slugs = set()

    for topic in Topic.objects.order_by("pk"):
        base_slug = topic.slug or slugify(topic.name) or f"tema-{topic.pk}"
        slug = base_slug
        counter = 1

        while slug in used_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1

        if topic.slug != slug:
            topic.slug = slug
            topic.save(update_fields=["slug"])

        used_slugs.add(slug)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0012_backfill_public_slugs"),
    ]

    operations = [
        migrations.RunPython(backfill_unique_topic_slugs, noop_reverse),
        migrations.AlterField(
            model_name="topic",
            name="slug",
            field=models.SlugField(blank=True, max_length=140, null=True, unique=True),
        ),
    ]
