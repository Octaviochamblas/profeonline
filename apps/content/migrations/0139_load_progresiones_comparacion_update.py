from django.db import migrations
from pathlib import Path
import yaml

SLUG_TO_FILE = {
    'distincion-entre-progresion-aritmetica-y-progresion-geometrica': 'distincion-entre-progresion-aritmetica-y-progresion-geometrica.yaml',
    'diferencia-entre-cambio-aditivo-y-cambio-multiplicativo-en-sucesiones': 'diferencia-entre-cambio-aditivo-y-cambio-multiplicativo-en-sucesiones.yaml',
    'eleccion-entre-modelo-aritmetico-y-geometrico-segun-el-contexto': 'eleccion-entre-modelo-aritmetico-y-geometrico-segun-el-contexto.yaml',
    'interpolacion-de-medios-aritmeticos-entre-dos-terminos': 'interpolacion-de-medios-aritmeticos-entre-dos-terminos.yaml',
    'interpolacion-de-medios-geometricos-entre-dos-terminos': 'interpolacion-de-medios-geometricos-entre-dos-terminos.yaml',
}

def update_progresiones_comparacion(apps, schema_editor):
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

def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('content', '0138_load_serie_geometrica_update'),
    ]

    operations = [
        migrations.RunPython(update_progresiones_comparacion, reverse_func),
    ]
