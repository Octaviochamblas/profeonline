from django.db import migrations
from pathlib import Path
import yaml

SLUGS = [
    'cardinalidad-de-la-union-de-conjuntos-disjuntos',
    'principio-de-inclusion-exclusion-para-dos-conjuntos',
    'principio-de-inclusion-exclusion-para-tres-conjuntos',
    'problema-de-conteo-con-diagrama-de-venn-de-dos-conjuntos',
    'problema-de-conteo-con-diagrama-de-venn-de-tres-conjuntos',
    'calculo-de-regiones-exclusivas-en-dos-conjuntos',
    'calculo-de-la-region-ninguno-en-problemas-de-conjuntos',
    'calculo-de-regiones-exclusivas-en-tres-conjuntos',
    'calculo-de-regiones-pertenecientes-exactamente-a-dos-conjuntos',
    'calculo-de-la-region-comun-a-tres-conjuntos'
]

def update_cardinalidad_conteo(apps, schema_editor):
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
        ('content', '0089_load_propiedades_conjuntos_update'),
    ]

    operations = [
        migrations.RunPython(update_cardinalidad_conteo, reverse_update),
    ]
