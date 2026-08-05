from django.db import migrations
from django.core.management import call_command


def load_all_fixed_node_contents_in_prod(apps, schema_editor):
    call_command("load_node_content", dir="docs/conocimiento/contenido", verbosity=0)


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0053_load_node_02_05_content"),
    ]

    operations = [
        migrations.RunPython(load_all_fixed_node_contents_in_prod, reverse_code=migrations.RunPython.noop),
    ]
