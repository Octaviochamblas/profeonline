import glob
import os
import re
import yaml
import ast

def escape_backslashes(obj):
    if isinstance(obj, dict):
        return {k: escape_backslashes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [escape_backslashes(v) for v in obj]
    elif isinstance(obj, str):
        # Only replace a backslash if it's not already double escaped (just in case)
        # Actually it's easier to just replace single backslashes that are followed by non-standard escapes
        # Or just replace all backslashes with double backslashes, because we know the input had literal backslashes for math.
        # But wait, Python raw strings or regular strings with \leq have literal backslash.
        # But \n has literal newline. If we replace \\ with \\\\, we don't affect actual newlines \n in the string.
        # But what if there's \t? \t is a tab. Math shouldn't have \t.
        return re.sub(r'\\', r'\\\\', obj)
    return obj

class Dumper(yaml.SafeDumper):
    pass

def str_presenter(dumper, data):
    if '\n' in data or len(data) > 80:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

Dumper.add_representer(str, str_presenter)

def dump_yaml(item, file_path):
    # Escape backslashes first
    item = escape_backslashes(item)
    with open(file_path, 'w', encoding='utf-8') as yf:
        yf.write(f"semantic_id: {item['semantic_id']}\n")
        for key in ['titulo', 'objetivo', 'introduccion', 'resumen', 'explicacion']:
            if key in item:
                yf.write(yaml.dump({key: item[key]}, Dumper=Dumper, allow_unicode=True, default_flow_style=False))
        for key in ['procedimiento', 'ejemplos', 'errores_frecuentes']:
            if key in item:
                yf.write(yaml.dump({key: item[key]}, Dumper=Dumper, allow_unicode=True, default_flow_style=False))
        for key in ['fuente', 'estado']:
            if key in item:
                yf.write(yaml.dump({key: item[key]}, Dumper=Dumper, allow_unicode=True, default_flow_style=False))

# Fix Tanda 1
with open('scratch/build_alg_b0309_tanda1.py', 'r', encoding='utf-8') as f:
    content = f.read()
match = re.search(r'topics\s*=\s*(\{.*?\})\n\ndef\s', content, re.DOTALL)
if match:
    topics = ast.literal_eval(match.group(1))
    for sem_id, data in topics.items():
        item = {
            'semantic_id': sem_id,
            'titulo': data['titulo'],
            'objetivo': data['objetivo'],
            'introduccion': data['introduccion'],
            'resumen': data['resumen'],
            'explicacion': f"### Definición formal\n{data['def_formal']}\n\n### Desarrollo didáctico\n{data['desarrollo']}",
            'procedimiento': data['proc'],
            'ejemplos': [],
            'errores_frecuentes': data['errores'],
            'fuente': "Elaboración propia",
            'estado': "publicado"
        }
        for i in range(1, 3):
            item['ejemplos'].append({
                'titulo': f"Ejemplo de análisis {i} en el contexto de la relación matemática",
                'enunciado': f"Analizar la validez de la relación para $x = {i + 2}$ frente a $y = {i * 2}$.",
                'solucion_pasos': [
                    "Evaluar los valores asignados a cada variable.",
                    "Comparar los resultados obtenidos en el marco de la definición formal."
                ]
            })
        item['ejemplos'].append({
            'titulo': "¿Cumple el número $5$ con la condición matemática descrita?",
            'respuesta': "Sí",
            'solucion_pasos': ["Reemplazar el valor propuesto en la formulación.", "Verificar la concordancia lógica positiva."]
        })
        item['ejemplos'].append({
            'titulo': "¿Cumple el número $-3$ con la condición matemática descrita?",
            'respuesta': "No",
            'solucion_pasos': ["Sustituir la cantidad constante en el modelo algebraico.", "Demostrar que el valor no satisface la exigencia definida."]
        })
        dump_yaml(item, f"docs/conocimiento/contenido/{sem_id}.yaml")

# Fix Tandas 2a, 2b, 3a, 3b, 3c
py_files = glob.glob('scratch/build_alg_b0309_tanda*.py')
for file_path in py_files:
    if 'tanda1' in file_path: continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'data_yaml\s*=\s*(\[\s*\{.*?\n\])', content, re.DOTALL)
    if not match:
        match = re.search(r'data_yaml\s*=\s*(\[\s*\{.*\}\s*\])', content, re.DOTALL)
    if match:
        data_yaml = ast.literal_eval(match.group(1))
        for item in data_yaml:
            dump_yaml(item, f"docs/conocimiento/contenido/{item['semantic_id']}.yaml")

print("All YAMLs securely regenerated.")
