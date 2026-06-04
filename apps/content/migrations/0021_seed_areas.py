from django.db import migrations
from django.utils.text import slugify


# El área de Matemáticas ya la garantiza el comando `seed_math_resources`
# (que corre en cada deploy de producción) como "Matemáticas". Aquí solo
# aseguramos Física y Química, que es lo que faltaba.
AREAS = [
    ("Física", 2),
    ("Química", 3),
]


def crear_areas(apps, schema_editor):
    """Asegura que existan las áreas Física y Química. Idempotente: si un área
    ya existe (por nombre), no se modifica."""
    Area = apps.get_model("content", "Area")
    for name, order in AREAS:
        # El modelo histórico no ejecuta el save() personalizado que genera el
        # slug, así que lo fijamos explícitamente.
        Area.objects.get_or_create(
            name=name,
            defaults={"order": order, "slug": slugify(name)},
        )


def revertir(apps, schema_editor):
    """No-op: no eliminamos áreas al revertir para no arrastrar el borrado de
    asignaturas/temas asociados."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0020_alter_subject_area"),
    ]

    operations = [
        migrations.RunPython(crear_areas, revertir),
    ]
