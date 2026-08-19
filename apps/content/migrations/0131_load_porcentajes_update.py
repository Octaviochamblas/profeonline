from django.db import migrations
from pathlib import Path
import yaml

SLUG_TO_FILE = {
    'concepto-de-porcentaje-como-razon-de-denominador-100': 'concepto-de-porcentaje-como-razon-de-denominador-100.yaml',
    'representacion-grafica-de-porcentajes': 'representacion-grafica-de-porcentajes.yaml',
    'representacion-decimal-de-un-porcentaje': 'representacion-decimal-de-un-porcentaje.yaml',
    'representacion-fraccionaria-de-un-porcentaje': 'representacion-fraccionaria-de-un-porcentaje.yaml',
    'calculo-del-c-de-una-cantidad': 'calculo-del-c-de-una-cantidad.yaml',
    'calculo-del-porcentaje-que-representa-una-cantidad': 'calculo-del-porcentaje-que-representa-una-cantidad.yaml',
    'calculo-del-total-dado-un-porcentaje': 'calculo-del-total-dado-un-porcentaje.yaml',
    'calculo-de-porcentaje-de-un-porcentaje': 'calculo-de-porcentaje-de-un-porcentaje.yaml',
    'estrategia-de-calculo-mental-para-el-10': 'estrategia-de-calculo-mental-para-el-10.yaml',
    'estrategia-de-calculo-mental-para-el-1': 'estrategia-de-calculo-mental-para-el-1.yaml',
}

def update_porcentajes(apps, schema_editor):
    KnowledgeNode = apps.get_model('content', 'KnowledgeNode')
    NodeContent = apps.get_model('content', 'NodeContent')
    base_dir = Path(__file__).resolve().parents[3] / 'docs' / 'conocimiento' / 'contenido'

    for slug, filename in SLUG_TO_FILE.items():
        yaml_path = base_dir / filename
        if not yaml_path.exists():
            print(f"File not found: {yaml_path}")
            continue

        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        nodes = KnowledgeNode.objects.filter(slug=slug)
        if not nodes.exists():
            print(f"Node not found in DB: {slug}")
            continue

        node = nodes.first()
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
        print(f"Updated NodeContent: {slug} (Node ID: {node.id})")

def reverse_update(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('content', '0130_load_reparto_proporcional_escalas_update'),
    ]

    operations = [
        migrations.RunPython(update_porcentajes, reverse_update),
    ]
