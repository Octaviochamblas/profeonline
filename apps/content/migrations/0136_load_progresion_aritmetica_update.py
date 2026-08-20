from django.db import migrations
from pathlib import Path
import yaml

SLUG_TO_FILE = {
    'definicion-de-progresion-aritmetica-mediante-diferencia-constante': 'definicion-de-progresion-aritmetica-mediante-diferencia-constante.yaml',
    'determinacion-de-la-diferencia-comun-en-una-progresion-aritmetica': 'determinacion-de-la-diferencia-comun-en-una-progresion-aritmetica.yaml',
    'reconocimiento-de-una-progresion-aritmetica-a-partir-de-sus-terminos': 'reconocimiento-de-una-progresion-aritmetica-a-partir-de-sus-terminos.yaml',
    'aplicacion-de-la-formula-del-termino-general-en-una-progresion-aritmetica': 'aplicacion-de-la-formula-del-termino-general-en-una-progresion-aritmetica.yaml',
    'determinacion-del-primer-termino-a-partir-de-un-termino-conocido-y-la-diferencia-comun': 'determinacion-del-primer-termino-a-partir-de-un-termino-conocido-y-la-diferencia-comun.yaml',
    'determinacion-de-la-posicion-de-un-termino-en-una-progresion-aritmetica': 'determinacion-de-la-posicion-de-un-termino-en-una-progresion-aritmetica.yaml',
    'calculo-de-la-suma-de-los-n-primeros-terminos-de-una-progresion-aritmetica': 'calculo-de-la-suma-de-los-n-primeros-terminos-de-una-progresion-aritmetica.yaml',
    'modelamiento-de-situaciones-de-cambio-lineal-mediante-progresiones-aritmeticas': 'modelamiento-de-situaciones-de-cambio-lineal-mediante-progresiones-aritmeticas.yaml',
    'interpretacion-contextual-de-la-diferencia-comun-en-una-progresion-aritmetica': 'interpretacion-contextual-de-la-diferencia-comun-en-una-progresion-aritmetica.yaml',
}

def update_progresion_aritmetica(apps, schema_editor):
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
        ('content', '0135_load_sucesiones_base_update'),
    ]

    operations = [
        migrations.RunPython(update_progresion_aritmetica, reverse_func),
    ]
