from collections import defaultdict

from django.db import migrations


def backfill(apps, schema_editor):
    """Rellena Subject.levels y Topic.levels a partir de los niveles ya
    asignados a sus recursos, para no perder la organización por nivel que
    existía (derivada de Resource.levels). Idempotente."""
    Resource = apps.get_model("content", "Resource")
    Subject = apps.get_model("content", "Subject")
    Topic = apps.get_model("content", "Topic")

    subject_levels = defaultdict(set)
    topic_levels = defaultdict(set)

    for resource in Resource.objects.prefetch_related("levels"):
        level_ids = list(resource.levels.values_list("id", flat=True))
        if not level_ids:
            continue
        if resource.subject_id:
            subject_levels[resource.subject_id].update(level_ids)
        if resource.topic_id:
            topic_levels[resource.topic_id].update(level_ids)

    for subject_id, level_ids in subject_levels.items():
        Subject.objects.get(pk=subject_id).levels.add(*level_ids)

    for topic_id, level_ids in topic_levels.items():
        Topic.objects.get(pk=topic_id).levels.add(*level_ids)


def revertir(apps, schema_editor):
    """No-op: el rollback lo maneja la migración de esquema (0022) al eliminar
    los campos."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0022_subject_levels_topic_levels"),
    ]

    operations = [
        migrations.RunPython(backfill, revertir),
    ]
