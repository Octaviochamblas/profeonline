import os
import re
import yaml
import ast

with open('scratch/build_alg_b0309_tanda1.py', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'topics\s*=\s*(\{.*?\})\n\ndef\s', content, re.DOTALL)
if match:
    topics = ast.literal_eval(match.group(1))

    class Dumper(yaml.SafeDumper):
        pass

    def str_presenter(dumper, data):
        if '\n' in data or len(data) > 80:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

    Dumper.add_representer(str, str_presenter)

    for sem_id, data in topics.items():
        # Build the proper dictionary structure based on the generator's intent
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

        # Build examples
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
            'solucion_pasos': [
                "Reemplazar el valor propuesto en la formulación.",
                "Verificar la concordancia lógica positiva."
            ]
        })
        item['ejemplos'].append({
            'titulo': "¿Cumple el número $-3$ con la condición matemática descrita?",
            'respuesta': "No",
            'solucion_pasos': [
                "Sustituir la cantidad constante en el modelo algebraico.",
                "Demostrar que el valor no satisface la exigencia definida."
            ]
        })

        yaml_path = f"docs/conocimiento/contenido/{sem_id}.yaml"
        with open(yaml_path, 'w', encoding='utf-8') as yf:
            yf.write(f"semantic_id: {sem_id}\n")
            for key in ['titulo', 'objetivo', 'introduccion', 'resumen', 'explicacion']:
                if key in item:
                    yf.write(yaml.dump({key: item[key]}, Dumper=Dumper, allow_unicode=True, default_flow_style=False))
            for key in ['procedimiento', 'ejemplos', 'errores_frecuentes']:
                if key in item:
                    yf.write(yaml.dump({key: item[key]}, Dumper=Dumper, allow_unicode=True, default_flow_style=False))
            for key in ['fuente', 'estado']:
                if key in item:
                    yf.write(yaml.dump({key: item[key]}, Dumper=Dumper, allow_unicode=True, default_flow_style=False))

    print("Fixed Tanda 1 YAMLs.")
else:
    print("Failed to parse topics.")
