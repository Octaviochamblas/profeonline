from django.db import migrations


SUBJECT_NAME = "Mec\u00e1nica de Fluidos"
SUBJECT_SLUG = "mecanica-de-fluidos"
AREA_SLUG = "fisica"
LEVEL_SLUG = "universitario"


def crear_asignatura(apps, schema_editor):
    Area = apps.get_model("content", "Area")
    Level = apps.get_model("content", "Level")
    Subject = apps.get_model("content", "Subject")

    area = Area.objects.filter(slug=AREA_SLUG).first()
    level = Level.objects.filter(slug=LEVEL_SLUG).first()

    subject, _ = Subject.objects.get_or_create(
        slug=SUBJECT_SLUG,
        defaults={
            "name": SUBJECT_NAME,
            "area": area,
            "is_active": True,
        },
    )

    changed = False
    if subject.name != SUBJECT_NAME:
        subject.name = SUBJECT_NAME
        changed = True
    if area and subject.area_id != area.id:
        subject.area = area
        changed = True
    if not subject.is_active:
        subject.is_active = True
        changed = True

    if changed:
        subject.save()

    if level:
        subject.levels.add(level)


def revertir(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0023_backfill_levels_from_resources"),
    ]

    operations = [
        migrations.RunPython(crear_asignatura, revertir),
    ]
