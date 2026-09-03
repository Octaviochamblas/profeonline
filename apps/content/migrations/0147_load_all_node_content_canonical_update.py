from django.db import migrations
from django.core.management import call_command


def load_all_canonical_node_contents(apps, schema_editor):
    call_command("load_node_content", dir="docs/conocimiento/contenido", verbosity=1)


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0146_sync_all_node_content_yamls_update"),
    ]

    operations = [
        migrations.RunPython(load_all_canonical_node_contents, reverse_code=migrations.RunPython.noop),
    ]
