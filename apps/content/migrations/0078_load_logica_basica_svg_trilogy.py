from django.db import migrations
from django.core.management import call_command


def load_logica_basica_svg_trilogy(apps, schema_editor):
    call_command("load_node_content", dir="docs/conocimiento/contenido", verbosity=0)


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0077_load_logica_basica_and_master_nodes"),
    ]

    operations = [
        migrations.RunPython(load_logica_basica_svg_trilogy, reverse_code=migrations.RunPython.noop),
    ]
