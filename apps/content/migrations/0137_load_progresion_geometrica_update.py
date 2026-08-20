from django.db import migrations
from pathlib import Path
import yaml

SLUG_TO_FILE = {
    'definicion-de-progresion-geometrica-mediante-razon-constante': 'definicion-de-progresion-geometrica-mediante-razon-constante.yaml',
    'identificacion-de-la-razon-geometrica-en-una-sucesion': 'identificacion-de-la-razon-geometrica-en-una-sucesion.yaml',
    'reconocimiento-de-una-progresion-geometrica-a-partir-de-sus-terminos': 'reconocimiento-de-una-progresion-geometrica-a-partir-de-sus-terminos.yaml',
    'aplicacion-de-la-formula-del-termino-general-de-una-progresion-geometrica': 'aplicacion-de-la-formula-del-termino-general-de-una-progresion-geometrica.yaml',
    'determinacion-del-primer-termino-a-partir-de-un-termino-conocido-y-la-razon-geometrica': 'determinacion-del-primer-termino-a-partir-de-un-termino-conocido-y-la-razon-geometrica.yaml',
    'determinacion-de-la-posicion-de-un-termino-en-una-progresion-geometrica': 'determinacion-de-la-posicion-de-un-termino-en-una-progresion-geometrica.yaml',
    'calculo-de-la-suma-finita-de-los-n-primeros-terminos-de-una-progresion-geometrica': 'calculo-de-la-suma-finita-de-los-n-primeros-terminos-de-una-progresion-geometrica.yaml',
    'modelamiento-de-crecimiento-porcentual-mediante-progresiones-geometricas': 'modelamiento-de-crecimiento-porcentual-mediante-progresiones-geometricas.yaml',
    'interpretacion-contextual-de-la-razon-geometrica-en-modelos-multiplicativos': 'interpretacion-contextual-de-la-razon-geometrica-en-modelos-multiplicativos.yaml',
}

def update_progresion_geometrica(apps, schema_editor):
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
        ('content', '0136_load_progresion_aritmetica_update'),
    ]

    operations = [
        migrations.RunPython(update_progresion_geometrica, reverse_func),
    ]
