from django.db import migrations
from pathlib import Path
import yaml

SLUGS = [
    'propiedad-conmutativa-de-la-union',
    'propiedad-conmutativa-de-la-interseccion',
    'propiedad-asociativa-de-la-union',
    'propiedad-asociativa-de-la-interseccion',
    'propiedad-distributiva-de-la-union-sobre-la-interseccion',
    'propiedad-distributiva-de-la-interseccion-sobre-la-union',
    'propiedad-idempotente-de-la-union',
    'propiedad-idempotente-de-la-interseccion',
    'elemento-neutro-de-la-union',
    'elemento-neutro-de-la-interseccion',
    'propiedad-de-absorcion-de-la-union',
    'propiedad-de-absorcion-de-la-interseccion',
    'ley-de-de-morgan-para-el-complemento-de-una-union',
    'ley-de-de-morgan-para-el-complemento-de-una-interseccion'
]

def update_propiedades_conjuntos(apps, schema_editor):
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
        ('content', '0088_load_operaciones_conjuntos_update'),
    ]

    operations = [
        migrations.RunPython(update_propiedades_conjuntos, reverse_update),
    ]
