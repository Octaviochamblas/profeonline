import os
import sys

# Añadir la raíz del proyecto al path de búsqueda de módulos de Python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Asegurar codificación UTF-8 en consola para evitar UnicodeEncodeError en Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()


from django.core.management import call_command

slugs = [
    '11-que-son-los-numeros',
    '12-conjuntos-numericos',
    '13-numeros-enteros-relaciones-de-orden-mayor-menor-e-igual',
    '14-valor-absoluto-relaciones-de-orden',
    '15-regla-de-signos-para-sumasrestas',
    '15a-ejercicios-de-sumas-y-restas-aplicacion-de-regla-de-los-signos',
    '16-regla-de-los-signos-en-multiplicaciondivision-ejemplos',
    '17-prioridad-de-operaciones-sumarestamultiplicaciondivision-combinadas',
    '18-numeros-primos-multiplos-y-divisores',
    '19-minimo-comun-multiplo-maximo-comun-divisor',
    '19a-ejercicios-minimo-comun-multiplo'
]

print("Iniciando poblado masivo de recursos de 'Números enteros' para nivel 'escolar'...")
for idx, slug in enumerate(slugs, 1):
    print(f"\n[{idx}/{len(slugs)}] Procesando recurso: {slug}...")
    try:
        call_command(
            'generate_pending_questions',
            resource=slug,
            education_level='escolar',
            allow_without_transcript=True,
            publish=True
        )
    except Exception as e:
        print(f"Error procesando {slug}: {e}")

print("\n¡Proceso de población en lote finalizado!")
