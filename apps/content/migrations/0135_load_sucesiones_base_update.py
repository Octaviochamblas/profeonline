from django.db import migrations
from pathlib import Path
import yaml

SLUG_TO_FILE = {
    'definicion-de-sucesion-numerica-como-lista-ordenada-de-terminos': 'definicion-de-sucesion-numerica-como-lista-ordenada-de-terminos.yaml',
    'reconocimiento-del-orden-de-los-terminos-en-una-sucesion': 'reconocimiento-del-orden-de-los-terminos-en-una-sucesion.yaml',
    'uso-de-subindices-para-representar-terminos-de-una-sucesion': 'uso-de-subindices-para-representar-terminos-de-una-sucesion.yaml',
    'concepto-de-termino-general-de-una-sucesion': 'concepto-de-termino-general-de-una-sucesion.yaml',
    'calculo-de-terminos-de-una-sucesion-a-partir-del-termino-general': 'calculo-de-terminos-de-una-sucesion-a-partir-del-termino-general.yaml',
    'identificacion-de-regularidades-en-secuencias-numericas': 'identificacion-de-regularidades-en-secuencias-numericas.yaml',
    'identificacion-de-regularidades-en-secuencias-graficas': 'identificacion-de-regularidades-en-secuencias-graficas.yaml',
    'concepto-de-sucesion-definida-por-recurrencia-simple': 'concepto-de-sucesion-definida-por-recurrencia-simple.yaml',
    'diferencia-entre-sucesion-definida-por-termino-general-y-por-recurrencia': 'diferencia-entre-sucesion-definida-por-termino-general-y-por-recurrencia.yaml',
}

def update_sucesiones_base(apps, schema_editor):
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
        ('content', '0134_load_interes_compuesto_update'),
    ]

    operations = [
        migrations.RunPython(update_sucesiones_base, reverse_func),
    ]
