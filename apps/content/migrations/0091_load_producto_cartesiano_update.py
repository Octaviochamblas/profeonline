from django.db import migrations
from pathlib import Path
import yaml

SLUGS = [
    'par-ordenado',
    'igualdad-de-pares-ordenados',
    'definicion-de-producto-cartesiano',
    'enumeracion-de-elementos-de-un-producto-cartesiano',
    'cardinalidad-del-producto-cartesiano',
    'representacion-de-pares-ordenados-en-el-plano-cartesiano'
]

def update_producto_cartesiano(apps, schema_editor):
    KnowledgeNode = apps.get_model('content', 'KnowledgeNode')
    base_dir = Path(__file__).resolve().parents[3] / 'docs' / 'conocimiento' / 'contenido'

    for slug in SLUGS:
        matches = list(base_dir.glob(f"*{slug}*.yaml"))
        if not matches:
            print(f"YAML not found for {slug}")
            continue

        yaml_path = matches[0]
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        nodes = KnowledgeNode.objects.filter(slug=slug)
        if not nodes.exists():
            print(f"Node not found in DB for slug: {slug}")
            continue

        node = nodes.first()
        node.data = data
        node.save()
        print(f"Updated node: {slug} (ID: {node.id})")

def reverse_update(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('content', '0090_load_cardinalidad_conteo_update'),
    ]

    operations = [
        migrations.RunPython(update_producto_cartesiano, reverse_update),
    ]
