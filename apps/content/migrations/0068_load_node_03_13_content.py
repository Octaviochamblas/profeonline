from django.db import migrations
from django.core.management import call_command


def load_node_03_13_content_in_prod(apps, schema_editor):
    call_command("load_node_content", dir="docs/conocimiento/contenido", verbosity=0)


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0067_load_node_03_12_content"),
    ]

    operations = [
        migrations.RunPython(load_node_03_13_content_in_prod, reverse_code=migrations.RunPython.noop),
    ]
