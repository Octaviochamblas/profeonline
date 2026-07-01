import os
import yaml
import json
import sys

# We'll import the dictionaries from the scripts
sys.path.append(r"C:\Users\PC\Documents\Proyectos\Web\profeonline\scratch")

try:
    from build_alg_b0309_tanda4 import topics as t4
    from build_alg_b0309_tanda5 import topics as t5
    from build_alg_b0309_tanda6 import topics as t6
    from build_alg_b0309_tanda7 import topics as t7
except ImportError as e:
    print(f"Error importing topics: {e}")
    sys.exit(1)

all_topics = {}
all_topics.update(t4)
all_topics.update(t5)
all_topics.update(t6)
all_topics.update(t7)

yaml_dir = r"C:\Users\PC\Documents\Proyectos\Web\profeonline\docs\conocimiento\contenido"
jsonl_file = r"C:\Users\PC\Documents\Proyectos\Web\profeonline\docs\conocimiento\ejercicios\mat-alg-desigualdades-banco-gen-final-real.jsonl"

def str_presenter(dumper, data):
    if '\n' in data or len(data) > 60 or data.startswith('###'):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

all_exs = []

for sid, data in all_topics.items():
    # 1. Create YAML
    content_dict = {
        "semantic_id": sid,
        "title": data.get("titulo", ""),
        "description": data.get("objetivo", ""),
        "content": {
            "introduccion": data.get("introduccion", ""),
            "resumen": data.get("resumen", ""),
            "explicacion": data.get("explicacion", ""),
            "pasos": data.get("procedimiento", []),
            "ejemplos_resueltos": [],
            "errores_frecuentes": [{"descripcion": e} for e in data.get("errores_frecuentes", [])]
        }
    }

    for ej in data.get("ejemplos", []):
        if "respuesta" in ej:
            content_dict["content"]["ejemplos_resueltos"].append({
                "tipo": "verdadero_falso",
                "titulo": ej.get("titulo", ""),
                "afirmacion": ej.get("enunciado", ""), # sometimes affirmative is in 'enunciado', sometimes in 'titulo'
                "respuesta": ej.get("respuesta") == "Sí" or ej.get("respuesta") == True,
                "explicacion": "\n".join(ej.get("solucion_pasos", []))
            })
            # Fix if afirmacion is missing
            if not content_dict["content"]["ejemplos_resueltos"][-1]["afirmacion"]:
                content_dict["content"]["ejemplos_resueltos"][-1]["afirmacion"] = ej.get("titulo", "")
        else:
            content_dict["content"]["ejemplos_resueltos"].append({
                "tipo": "abierto",
                "titulo": ej.get("titulo", ""),
                "enunciado": ej.get("enunciado", ""),
                "pasos": ej.get("solucion_pasos", [])
            })

    filename = os.path.join(yaml_dir, f"{sid.lower().replace('.', '-')}.yaml")
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.safe_dump(content_dict, f, allow_unicode=True, sort_keys=False)

    # 2. Extract exercises
    for ej in data.get("ejercicios", []):
        subtipo = ej.get("subtipo", "")
        if subtipo == "conceptual":
            ig = "conceptuales"
        elif subtipo == "reconocimiento":
            ig = "reconocimiento"
        elif subtipo == "procedimiento_basico":
            ig = "procedimiento_basico"
        elif subtipo == "tipo_paes":
            ig = "tipo_paes"
        else:
            ig = subtipo

        ex = {
            "stable_id": ej.get("stable_id", ""),
            "semantic_id": sid,
            "item_group": ig,
            "format": ej.get("tipo_ejercicio", ""),
            "difficulty": "basica" if ej.get("nivel") == 1 else ("media" if ej.get("nivel") == 2 else "alta"),
            "competencia": "M1",
            "status": "ready",
            "source_kind": "manual",
            "prompt": ej.get("enunciado", ""),
            "correct_answer": ej.get("respuesta_correcta", ""),
            "solution_steps": ej.get("explicacion", "")
        }
        if "opciones" in ej:
            ex["choices"] = ej["opciones"]
        if ig == "tipo_paes":
            ex["paes_style"] = True

        all_exs.append(ex)

with open(jsonl_file, 'w', encoding='utf-8') as f:
    for ex in all_exs:
        f.write(json.dumps(ex, ensure_ascii=False) + '\n')

print(f"Successfully dumped {len(all_topics)} topics and {len(all_exs)} exercises.")
