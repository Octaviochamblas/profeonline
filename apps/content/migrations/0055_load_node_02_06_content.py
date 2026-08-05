from django.db import migrations
from django.core.management import call_command


def load_node_02_06_content_in_prod(apps, schema_editor):
    call_command("load_node_content", dir="docs/conocimiento/contenido", verbosity=0)


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0054_load_all_fixed_node_contents"),
    ]

    operations = [
        migrations.RunPython(load_node_02_06_content_in_prod, reverse_code=migrations.RunPython.noop),
    ]
