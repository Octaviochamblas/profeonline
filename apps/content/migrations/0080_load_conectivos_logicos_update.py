from django.db import migrations
from django.core.management import call_command


def load_conectivos_logicos_update(apps, schema_editor):
    call_command("load_node_content", dir="docs/conocimiento/contenido", verbosity=0)


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0079_load_interactive_ejemplos"),
    ]

    operations = [
        migrations.RunPython(load_conectivos_logicos_update, reverse_code=migrations.RunPython.noop),
    ]
