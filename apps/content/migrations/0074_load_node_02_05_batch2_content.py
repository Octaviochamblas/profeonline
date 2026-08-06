from django.db import migrations
from django.core.management import call_command


def load_node_02_05_batch2_content(apps, schema_editor):
    call_command("load_node_content", dir="docs/conocimiento/contenido", verbosity=0)


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0073_load_node_02_05_batch1_content"),
    ]

    operations = [
        migrations.RunPython(load_node_02_05_batch2_content, reverse_code=migrations.RunPython.noop),
    ]
