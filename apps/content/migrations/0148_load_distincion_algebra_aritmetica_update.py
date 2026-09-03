from django.db import migrations
from django.core.management import call_command


def load_node_update(apps, schema_editor):
    call_command("load_node_content", file="docs/conocimiento/contenido/distincion-entre-algebra-frente-a-aritmetica.yaml", verbosity=1)


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0147_load_all_node_content_canonical_update"),
    ]

    operations = [
        migrations.RunPython(load_node_update, reverse_code=migrations.RunPython.noop),
    ]
