from django.db import migrations
from pathlib import Path
import yaml

SLUG_TO_FILE = {
    # Variaciones Porcentuales (9 nodos)
    'concepto-de-aumento-porcentual': 'concepto-de-aumento-porcentual.yaml',
    'concepto-de-disminucion-porcentual': 'concepto-de-disminucion-porcentual.yaml',
    'concepto-de-descuento-porcentual': 'concepto-de-descuento-porcentual.yaml',
    'calculo-del-cambio-absoluto': 'calculo-del-cambio-absoluto.yaml',
    'calculo-del-cambio-relativo': 'calculo-del-cambio-relativo.yaml',
    'calculo-del-valor-final-con-aumento-porcentual': 'calculo-del-valor-final-con-aumento-porcentual.yaml',
    'calculo-del-valor-final-con-descuento-porcentual': 'calculo-del-valor-final-con-descuento-porcentual.yaml',
    'calculo-del-valor-final-por-porcentajes-sucesivos': 'calculo-del-valor-final-por-porcentajes-sucesivos.yaml',
    'aplicacion-del-impuesto-al-valor-agregado': 'aplicacion-del-impuesto-al-valor-agregado.yaml',
    # Finanzas Personales (10 nodos)
    'clasificacion-de-tipos-de-gasto-fijo-variable-imprevisto': 'clasificacion-de-tipos-de-gasto-fijo-variable-imprevisto.yaml',
    'clasificacion-de-tipos-de-ingreso-salario-comision-dividendo-interes': 'clasificacion-de-tipos-de-ingreso-salario-comision-dividendo-interes.yaml',
    'clasificacion-de-tipos-de-deuda-personal-estudiantil-tarjeta': 'clasificacion-de-tipos-de-deuda-personal-estudiantil-tarjeta.yaml',
    'construccion-de-presupuesto-personal': 'construccion-de-presupuesto-personal.yaml',
    'calculo-de-balance-financiero-personal': 'calculo-de-balance-financiero-personal.yaml',
    'definicion-del-indice-de-precios-al-consumidor': 'definicion-del-indice-de-precios-al-consumidor.yaml',
    'concepto-de-rentabilidad-financiera': 'concepto-de-rentabilidad-financiera.yaml',
    'calculo-de-tasa-de-interes-real': 'calculo-de-tasa-de-interes-real.yaml',
    'calculo-de-cotizacion-previsional-sobre-sueldo-imponible': 'calculo-de-cotizacion-previsional-sobre-sueldo-imponible.yaml',
    'proyeccion-de-ahorro-previsional-con-aporte-constante': 'proyeccion-de-ahorro-previsional-con-aporte-constante.yaml',
}

def update_variaciones_finanzas(apps, schema_editor):
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
        ('content', '0131_load_porcentajes_update'),
    ]

    operations = [
        migrations.RunPython(update_variaciones_finanzas, reverse_update),
    ]
