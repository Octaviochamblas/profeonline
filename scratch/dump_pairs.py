import os
import yaml
import json
import sys
import importlib.util

sys.path.append(r"C:\Users\PC\Documents\Proyectos\Web\profeonline\scratch")

all_topics = {}

for p in range(1, 14):
    module_name = f"build_alg_b0309_pair_{p}"
    file_path = f"C:\\Users\\PC\\Documents\\Proyectos\\Web\\profeonline\\scratch\\b0309_pair_{p}.py"
    if os.path.exists(file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "topics"):
            for sid, payload in module.topics.items():
                if "yaml" in payload and "jsonl" in payload:
                    all_topics[sid] = {"yaml": payload["yaml"], "jsonl": payload["jsonl"]}
                elif "yaml" in payload:
                    all_topics[sid] = {"yaml": payload["yaml"], "jsonl": payload.get("ejercicios", [])}
                else:
                    all_topics[sid] = {"yaml": payload, "jsonl": payload.get("ejercicios", [])}
        else:
            print(f"Warning: {file_path} does not have 'topics'")

yaml_dir = r"C:\Users\PC\Documents\Proyectos\Web\profeonline\docs\conocimiento\contenido"
jsonl_file = r"C:\Users\PC\Documents\Proyectos\Web\profeonline\docs\conocimiento\ejercicios\mat-alg-desigualdades-banco-gen-final-real-pairs.jsonl"

def str_presenter(dumper, data):
    if '\n' in data or len(data) > 60 or data.startswith('###'):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

all_exs = []

for sid, combined_data in all_topics.items():
    data = combined_data["yaml"]
    jsonl_data = combined_data["jsonl"]

    content_dict = {
        "semantic_id": data.get("semantic_id", sid),
        "title": data.get("titulo", ""),
        "description": data.get("objetivo", data.get("description", "")),
        "content": {
            "introduccion": data.get("introduccion", ""),
            "resumen": data.get("resumen", ""),
            "explicacion": data.get("explicacion", ""),
            "pasos": data.get("procedimiento", data.get("pasos", [])),
            "ejemplos_resueltos": [],
            "errores_frecuentes": [{"descripcion": e} if isinstance(e, str) else e for e in data.get("errores_frecuentes", [])]
        }
    }

    for ej in data.get("ejemplos", data.get("ejemplos_resueltos", [])):
        if "respuesta" in ej or ej.get("tipo") == "verdadero_falso":
            resp = ej.get("respuesta", True)
            if isinstance(resp, str):
                resp = (resp.lower() in ["sí", "si", "true"])

            content_dict["content"]["ejemplos_resueltos"].append({
                "tipo": "verdadero_falso",
                "titulo": ej.get("titulo", ""),
                "afirmacion": ej.get("enunciado", ej.get("afirmacion", ej.get("titulo", ""))),
                "respuesta": resp,
                "explicacion": "\n".join(ej.get("solucion_pasos", [])) if isinstance(ej.get("solucion_pasos", ej.get("explicacion", [])), list) else ej.get("solucion_pasos", ej.get("explicacion", ""))
            })
        else:
            content_dict["content"]["ejemplos_resueltos"].append({
                "tipo": "abierto",
                "titulo": ej.get("titulo", ""),
                "enunciado": ej.get("enunciado", ""),
                "pasos": ej.get("solucion_pasos", ej.get("pasos", [])) if isinstance(ej.get("solucion_pasos", ej.get("pasos", [])), list) else [ej.get("solucion_pasos", "")]
            })

    filename = os.path.join(yaml_dir, f"{sid.lower().replace('.', '-')}.yaml")
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.safe_dump(content_dict, f, allow_unicode=True, sort_keys=False)

    for ej in jsonl_data:
        subtipo = ej.get("subtipo", ej.get("tipo", ej.get("item_group", "")))
        if "conceptual" in subtipo.lower(): ig = "conceptuales"
        elif "reconocimiento" in subtipo.lower(): ig = "reconocimiento"
        elif "procedimiento" in subtipo.lower(): ig = "procedimiento_basico"
        elif "paes" in subtipo.lower(): ig = "tipo_paes"
        else: ig = subtipo

        ex = {
            "stable_id": ej.get("stable_id", f"{sid}-EX"),
            "semantic_id": ej.get("semantic_id", sid),
            "item_group": ig,
            "format": ej.get("formato", ej.get("tipo_ejercicio", ej.get("format", "multiple_choice"))),
            "difficulty": "basica" if ej.get("nivel") == 1 else ("media" if ej.get("nivel") == 2 else ej.get("difficulty", "alta")),
            "competencia": "M1",
            "status": "ready",
            "source_kind": "manual",
            "prompt": ej.get("pregunta", ej.get("enunciado", ej.get("prompt", ""))),
            "correct_answer": ej.get("respuesta_correcta", ej.get("correct_answer", "")),
            "solution_steps": ej.get("explicacion", ej.get("solucion", ej.get("solution_steps", "")))
        }
        if "opciones" in ej:
            ex["choices"] = ej["opciones"]
        elif "choices" in ej:
            ex["choices"] = ej["choices"]

        if ig == "tipo_paes" or ej.get("paes_style") or ej.get("paes_style", False) == True:
            ex["paes_style"] = True

        all_exs.append(ex)

with open(jsonl_file, 'w', encoding='utf-8') as f:
    for ex in all_exs:
        f.write(json.dumps(ex, ensure_ascii=False) + '\n')

print(f"Successfully dumped {len(all_topics)} topics and {len(all_exs)} exercises.")
