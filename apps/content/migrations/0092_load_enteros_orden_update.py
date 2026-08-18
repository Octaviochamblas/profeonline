from django.db import migrations
from pathlib import Path
import yaml

SLUG_TO_FILE = {
    'identificacion-de-los-numeros-naturales-n': 'mat-num-enteros-conjunto-naturales.yaml',
    'identificacion-de-los-numeros-cardinales-n0': 'mat-num-enteros-conjunto-cardinales.yaml',
    'definicion-de-los-numeros-enteros-z-como-extension-de-n': 'mat-num-enteros-conjunto-definicion.yaml',
    'identificacion-de-enteros-positivos-y-negativos': 'mat-num-enteros-conjunto-positivos-negativos.yaml',
    'ubicacion-de-enteros-en-la-recta-numerica': 'mat-num-enteros-conjunto-recta-ubicacion.yaml',
    'convencion-de-sentido-en-la-recta-derecha-vs-izquierda': 'mat-num-enteros-conjunto-recta-convencion.yaml',
    'determinacion-de-orden-en-la-recta-numerica-mayor-a-la-derecha': 'mat-num-enteros-conjunto-orden-logica.yaml',
    'ley-de-tricotomia-para-el-orden-de-enteros': 'mat-num-enteros-conjunto-tricotomia.yaml',
    'concepto-de-valor-absoluto-como-distancia-al-origen': 'mat-num-enteros-conjunto-valor-absoluto-def.yaml',
    'notacion-y-signo-del-valor-absoluto-x': 'mat-num-enteros-conjunto-valor-absoluto-notacion.yaml',
    'propiedad-valor-absoluto-de-numeros-opuestos': 'mat-num-enteros-conjunto-valor-absoluto-opuestos.yaml',
    'definicion-de-numeros-pares': 'mat-num-enteros-conjunto-pares.yaml',
    'definicion-de-numeros-impares': 'mat-num-enteros-conjunto-impares.yaml',
    'concepto-de-sucesor-de-un-numero-n-1': 'mat-num-enteros-conjunto-sucesor.yaml',
    'concepto-de-antecesor-de-un-numero-n-1': 'mat-num-enteros-conjunto-antecesor.yaml'
}

def update_enteros_orden(apps, schema_editor):
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
        ('content', '0091_load_producto_cartesiano_update'),
    ]

    operations = [
        migrations.RunPython(update_enteros_orden, reverse_update),
    ]
