from django.db import migrations
from pathlib import Path
import yaml

SLUG_TO_FILE = {
    'adicion-de-enteros-con-el-mismo-signo': 'mat-num-enteros-operatoria-adicion-igual-signo.yaml',
    'adicion-de-enteros-con-distinto-signo': 'mat-num-enteros-operatoria-adicion-distinto-signo.yaml',
    'propiedad-conmutativa-de-la-adicion': 'mat-num-enteros-operatoria-conmutativa-adicion.yaml',
    'propiedad-asociativa-de-la-adicion': 'mat-num-enteros-operatoria-asociativa-adicion.yaml',
    'propiedad-del-elemento-neutro-aditivo-el-cero': 'mat-num-enteros-operatoria-neutro-aditivo.yaml',
    'identificacion-del-inverso-aditivo-opuesto': 'mat-num-enteros-operatoria-inverso-aditivo.yaml',
    'transformacion-de-sustraccion-a-suma-por-el-inverso': 'mat-num-enteros-operatoria-sustraccion-regla.yaml',
    'multiplicacion-de-enteros-regla-de-signos-iguales': 'mat-num-enteros-operatoria-mult-signos-iguales.yaml',
    'multiplicacion-de-enteros-regla-de-signos-distintos': 'mat-num-enteros-operatoria-mult-signos-distintos.yaml',
    'propiedad-conmutativa-de-la-multiplicacion': 'mat-num-enteros-operatoria-conmutativa-mult.yaml',
    'propiedad-asociativa-de-la-multiplicacion': 'mat-num-enteros-operatoria-asociativa-mult.yaml',
    'elemento-neutro-multiplicativo-el-uno': 'mat-num-enteros-operatoria-neutro-mult.yaml',
    'elemento-absorbente-de-la-multiplicacion-el-cero': 'mat-num-enteros-operatoria-absorbente-cero.yaml',
    'propiedad-distributiva-de-la-multiplicacion-sobre-la-adicion': 'mat-num-enteros-operatoria-distributiva-mult-adicion.yaml',
    'division-de-enteros-regla-de-signos-iguales': 'mat-num-enteros-operatoria-div-signos-iguales.yaml',
    'division-de-enteros-regla-de-signos-distintos': 'mat-num-enteros-operatoria-div-signos-distintos.yaml',
    'indefinicion-de-la-division-por-cero': 'mat-num-enteros-operatoria-division-por-cero.yaml',
    'prioridad-de-operaciones-el-orden-papomudas': 'mat-num-enteros-operatoria-papomudas-orden.yaml',
    'eliminacion-de-parentesis-precedidos-por-signo': 'mat-num-enteros-operatoria-parentesis-mas.yaml',
    'eliminacion-de-parentesis-precedidos-por-signo-1': 'mat-num-enteros-operatoria-parentesis-menos.yaml',
    'resolucion-de-parentesis-de-adentro-hacia-afuera': 'mat-num-enteros-operatoria-parentesis-anidados.yaml'
}

def update_operatoria_enteros(apps, schema_editor):
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
        ('content', '0092_load_enteros_orden_update'),
    ]

    operations = [
        migrations.RunPython(update_operatoria_enteros, reverse_update),
    ]
