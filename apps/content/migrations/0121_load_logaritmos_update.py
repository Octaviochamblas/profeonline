from django.db import migrations
from pathlib import Path
import yaml

SLUG_TO_FILE = {
    'definicion-de-logaritmo': 'definicion-de-logaritmo.yaml',
    'relacion-entre-logaritmo-y-potencia': 'relacion-entre-logaritmo-y-potencia.yaml',
    'conversion-de-forma-logaritmica-a-forma-exponencial': 'conversion-de-forma-logaritmica-a-forma-exponencial.yaml',
    'conversion-de-forma-exponencial-a-forma-logaritmica': 'conversion-de-forma-exponencial-a-forma-logaritmica.yaml',
    'restriccion-de-base-positiva-en-un-logaritmo': 'restriccion-de-base-positiva-en-un-logaritmo.yaml',
    'restriccion-de-base-distinta-de-uno-en-un-logaritmo': 'restriccion-de-base-distinta-de-uno-en-un-logaritmo.yaml',
    'restriccion-de-argumento-positivo-en-un-logaritmo': 'restriccion-de-argumento-positivo-en-un-logaritmo.yaml',
    'logaritmo-de-uno': 'logaritmo-de-uno.yaml',
    'logaritmo-de-la-base': 'logaritmo-de-la-base.yaml',
    'concepto-de-logaritmo-decimal': 'concepto-de-logaritmo-decimal.yaml',
    'concepto-de-logaritmo-natural': 'concepto-de-logaritmo-natural.yaml',
}

def update_logaritmos(apps, schema_editor):
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
        ('content', '0120_load_racionalizacion_update'),
    ]

    operations = [
        migrations.RunPython(update_logaritmos, reverse_update),
    ]
