from django.db import migrations
from django.core.management import call_command


def load_interactive_ejemplos(apps, schema_editor):
    call_command("load_node_content", dir="docs/conocimiento/contenido", verbosity=0)


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0078_load_logica_basica_svg_trilogy"),
    ]

    operations = [
        migrations.RunPython(load_interactive_ejemplos, reverse_code=migrations.RunPython.noop),
    ]
