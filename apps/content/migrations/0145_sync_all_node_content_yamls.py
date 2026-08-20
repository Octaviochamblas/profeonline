from django.db import migrations
from pathlib import Path
import yaml


def sync_all_node_content(apps, schema_editor):
    KnowledgeNode = apps.get_model('content', 'KnowledgeNode')
    NodeContent = apps.get_model('content', 'NodeContent')
    base_dir = Path(__file__).resolve().parents[3] / 'docs' / 'conocimiento' / 'contenido'

    if not base_dir.exists():
        print(f"Directory not found: {base_dir}")
        return

    updated_count = 0
    for yaml_path in base_dir.glob('*.yaml'):
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading {yaml_path}: {e}")
            continue

        if not isinstance(data, dict):
            continue

        slug = yaml_path.stem
        semantic_id = data.get('semantic_id')
        node = None
        if semantic_id:
            node = KnowledgeNode.objects.filter(semantic_id=semantic_id).first()
        if not node:
            node = KnowledgeNode.objects.filter(slug=slug).first()

        if not node:
            continue

        defaults = {
            "objetivo": data.get("objetivo", ""),
            "introduccion": data.get("introduccion", ""),
            "resumen": data.get("resumen", ""),
            "explicacion": data.get("explicacion", ""),
            "procedimiento": data.get("procedimiento") or [],
            "ejemplos": data.get("ejemplos") or [],
            "errores_frecuentes": data.get("errores_frecuentes") or [],
            "afirmaciones_verdaderas": data.get("afirmaciones_verdaderas") or [],
            "estado": data.get("estado", "publicado"),
            "fuente": data.get("fuente", ""),
            "resumen_inicial": data.get("resumen_inicial", ""),
            "explicacion_simple": data.get("explicacion_simple", ""),
            "explicacion_formal": data.get("explicacion_formal", ""),
            "definiciones_clave": data.get("definiciones_clave", ""),
            "propiedades_relaciones": data.get("propiedades_relaciones", ""),
            "ejemplo_guiado": data.get("ejemplo_guiado") or {},
            "errores_correccion": data.get("errores_correccion", ""),
            "al_terminar_debes_poder": data.get("al_terminar_debes_poder", ""),
            "checkpoints": data.get("checkpoints") or [],
        }

        NodeContent.objects.update_or_create(node=node, defaults=defaults)
        updated_count += 1

    print(f"Synced {updated_count} NodeContent objects from YAMLs.")


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0144_load_clasificacion_tecnica_update'),
    ]

    operations = [
        migrations.RunPython(sync_all_node_content, reverse_func),
    ]
