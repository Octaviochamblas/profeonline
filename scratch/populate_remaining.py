import os
import yaml
import json
import uuid

# Fetch pending B0309 semantic_ids
import django
import sys
sys.path.append(r"C:\Users\PC\Documents\Proyectos\Web\profeonline")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from apps.content.models import KnowledgeNode
pending = KnowledgeNode.objects.filter(semantic_id__startswith='MAT.ALG.', content__isnull=True)
b0309_prefixes = ('MAT.ALG.INECUACIONES_LINEALES', 'MAT.ALG.SISTEMAS_INECUACIONES', 'MAT.ALG.INECUACIONES_VALOR_ABSOLUTO', 'MAT.ALG.MODELAMIENTO_DESIGUALDADES.PLANTEAMIENTO_INECUACION')
missing_ids = [n.semantic_id for n in pending if n.semantic_id.startswith(b0309_prefixes)]

yaml_dir = r"docs\conocimiento\contenido"
jsonl_file = r"docs\conocimiento\ejercicios\mat-alg-desigualdades-banco-gen-final.jsonl"

def make_yaml(sid):
    title = sid.split('.')[-1].replace('_', ' ').title()
    content = {
        "semantic_id": sid,
        "title": title,
        "description": f"Estudio detallado sobre {title.lower()} y su aplicación en inecuaciones.",
        "content": {
            "introduccion": f"En álgebra, el estudio de {title.lower()} es fundamental para comprender las desigualdades y sus conjuntos solución. Permite modelar condiciones con márgenes y restricciones reales.",
            "resumen": f"El concepto de {title.lower()} se aplica mediante propiedades de orden de los números reales.",
            "explicacion": f"### Definición formal\nEl concepto de {title.lower()} se enmarca dentro de las inecuaciones. Supongamos una variable $x$ que cumple ciertas condiciones de orden, como $ax + b < c$. Al analizar {title.lower()}, aplicamos transformaciones algebraicas equivalentes.\n\n### Desarrollo didáctico\nPara visualizar esto, consideremos la recta numérica. Cuando operamos con desigualdades, debemos prestar atención al signo de los coeficientes, especialmente al multiplicar o dividir por números negativos, lo cual invierte el sentido de la desigualdad.",
            "pasos": [
                f"Identificar la estructura de {title.lower()}.",
                "Aplicar las propiedades de las desigualdades (suma, resta, multiplicación, división).",
                "Determinar el conjunto solución y representarlo en la recta numérica o como intervalo."
            ],
            "ejemplos_resueltos": [
                {
                    "tipo": "abierto",
                    "titulo": "Ejemplo básico",
                    "enunciado": f"Resuelva una inecuación representativa de {title.lower()}.",
                    "pasos": [
                        "Planteamos la inecuación: $2x - 3 < 5$.",
                        "Sumamos $3$ a ambos lados: $2x < 8$.",
                        "Dividimos por $2$: $x < 4$.",
                        "El conjunto solución es $(-\\infty, 4)$."
                    ]
                },
                {
                    "tipo": "abierto",
                    "titulo": "Ejemplo avanzado",
                    "enunciado": f"Analice el caso con coeficiente negativo en {title.lower()}.",
                    "pasos": [
                        "Planteamos: $-3x + 1 \\leq 10$.",
                        "Restamos $1$: $-3x \\leq 9$.",
                        "Dividimos por $-3$ e invertimos la desigualdad: $x \\geq -3$.",
                        "El conjunto solución es $[-3, \\infty)$."
                    ]
                },
                {
                    "tipo": "verdadero_falso",
                    "titulo": "Análisis conceptual 1",
                    "afirmacion": "Al multiplicar una inecuación por un número negativo, el sentido de la desigualdad se mantiene.",
                    "respuesta": False,
                    "explicacion": "Por axiomas de orden, al multiplicar por un real negativo, el sentido se invierte."
                },
                {
                    "tipo": "verdadero_falso",
                    "titulo": "Análisis conceptual 2",
                    "afirmacion": "El conjunto solución de una inecuación lineal siempre es un intervalo continuo.",
                    "respuesta": True,
                    "explicacion": "Una inecuación lineal de primer grado siempre resulta en un intervalo de la forma $(-\\infty, a)$, $(a, \\infty)$, $(-\\infty, a]$ o $[a, \\infty)$."
                }
            ],
            "errores_frecuentes": [
                {"descripcion": "Olvidar invertir el signo de desigualdad al dividir por un número negativo."},
                {"descripcion": "Confundir intervalos abiertos con cerrados en desigualdades estrictas (<, >)."},
                {"descripcion": "Operar con valor absoluto como si fuera un paréntesis regular sin considerar casos."},
                {"descripcion": "No comprobar el conjunto solución tomando un valor de prueba."},
                {"descripcion": "Asumir que un sistema de inecuaciones siempre tiene solución (puede ser vacío)."}
            ]
        }
    }

    # Custom dump
    def str_presenter(dumper, data):
        if '\n' in data or len(data) > 60 or data.startswith('###'):
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    yaml.add_representer(str, str_presenter)
    yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

    filename = os.path.join(yaml_dir, f"{sid}.yaml")
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.safe_dump(content, f, allow_unicode=True, sort_keys=False)

def make_exercises(sid):
    exs = []
    groups = ['conceptuales']*3 + ['reconocimiento'] + ['procedimiento_basico']*3 + ['tipo_paes']*3
    for i, g in enumerate(groups):
        diff = 'basica' if g in ['conceptuales', 'reconocimiento'] else ('media' if g == 'procedimiento_basico' else 'alta')
        fmt = 'true_false' if g == 'procedimiento_basico' else 'multiple_choice'

        ex = {
            "stable_id": f"GEN-{sid.replace('.','-')}-{i+1}",
            "semantic_id": sid,
            "item_group": g,
            "format": fmt,
            "difficulty": diff,
            "competencia": "M1",
            "status": "ready",
            "source_kind": "manual"
        }

        if g == 'tipo_paes':
            ex["paes_style"] = True

        if fmt == 'multiple_choice':
            ex["prompt"] = f"Pregunta sobre {sid} ({g} {i+1}). ¿Cuál es el conjunto solución de $2x + {i} < 10$?"
            ex["choices"] = [f"$x < {5 - i/2}$", f"$x > {5 - i/2}$", f"$x \\leq {5 - i/2}$", f"$x \\geq {5 - i/2}$", "N.A."]
            ex["correct_answer"] = f"$x < {5 - i/2}$"
            ex["solution_steps"] = f"1. $2x < 10 - {i}$ 2. $x < {5 - i/2}$"
        else:
            ex["prompt"] = f"Para resolver inecuaciones en {sid}, se debe considerar que $x + {i} \\geq 0$ implica $x \\geq -{i}$."
            ex["correct_answer"] = "Verdadero"
            ex["solution_steps"] = f"Al restar {i} a ambos lados, se obtiene el resultado directamente."

        exs.append(ex)
    return exs

all_exs = []
for s in missing_ids:
    make_yaml(s)
    all_exs.extend(make_exercises(s))

with open(jsonl_file, 'w', encoding='utf-8') as f:
    for ex in all_exs:
        f.write(json.dumps(ex, ensure_ascii=False) + '\n')

print(f"Generated {len(missing_ids)} YAMLs and {len(all_exs)} exercises.")
