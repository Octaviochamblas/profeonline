from django.db import migrations
from django.core.management import call_command


def load_definicion_conjunto_update(apps, schema_editor):
    call_command("load_node_content", dir="docs/conocimiento/contenido", verbosity=0)


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0083_load_cuantificadores_update"),
    ]

    operations = [
        migrations.RunPython(load_definicion_conjunto_update, reverse_code=migrations.RunPython.noop),
    ]
