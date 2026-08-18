from django.db import migrations
from pathlib import Path
import yaml

SLUG_TO_FILE = {
    'concepto-de-multiplo-de-un-numero-natural': 'mat-num-divisibilidad-multiplo-concepto.yaml',
    'obtencion-de-multiplos-de-un-numero-natural': 'mat-num-divisibilidad-obtencion-multiplos.yaml',
    'concepto-de-divisor-de-un-numero-natural': 'mat-num-divisibilidad-divisor-concepto.yaml',
    'obtencion-de-divisores-de-un-numero-natural': 'mat-num-divisibilidad-obtencion-divisores.yaml',
    'divisibilidad-como-division-exacta': 'mat-num-divisibilidad-division-exacta.yaml',
    'criterio-de-divisibilidad-por-2': 'mat-num-divisibilidad-criterio-2.yaml',
    'criterio-de-divisibilidad-por-3': 'mat-num-divisibilidad-criterio-3.yaml',
    'criterio-de-divisibilidad-por-4': 'mat-num-divisibilidad-criterio-4.yaml',
    'criterio-de-divisibilidad-por-5': 'mat-num-divisibilidad-criterio-5.yaml',
    'criterio-de-divisibilidad-por-6': 'mat-num-divisibilidad-criterio-6.yaml',
    'criterio-de-divisibilidad-por-8': 'mat-num-divisibilidad-criterio-8.yaml',
    'criterio-de-divisibilidad-por-9': 'mat-num-divisibilidad-criterio-9.yaml',
    'criterio-de-divisibilidad-por-10': 'mat-num-divisibilidad-criterio-10.yaml',
    'criterio-de-divisibilidad-por-11': 'mat-num-divisibilidad-criterio-11.yaml',
    'criterio-de-divisibilidad-por-25': 'mat-num-divisibilidad-criterio-25.yaml'
}

def update_divisibilidad(apps, schema_editor):
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
            "estado": data.get("estado", "borrador"),
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
        ('content', '0093_load_operatoria_enteros_update'),
    ]

    operations = [
        migrations.RunPython(update_divisibilidad, reverse_update),
    ]
