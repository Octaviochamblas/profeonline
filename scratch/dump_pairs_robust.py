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
        try:
            spec.loader.exec_module(module)
            if hasattr(module, "topics"):
                for sid, payload in module.topics.items():
                    yaml_obj = None
                    jsonl_obj = None

                    if "yaml" in payload:
                        yaml_obj = payload["yaml"]
                    elif "yaml_data" in payload:
                        yaml_obj = payload["yaml_data"]
                    else:
                        yaml_obj = payload

                    if "jsonl" in payload:
                        jsonl_obj = payload["jsonl"]
                    elif "exercises" in payload:
                        jsonl_obj = payload["exercises"]
                    elif "jsonl_data" in payload:
                        jsonl_obj = payload["jsonl_data"]
                    else:
                        jsonl_obj = payload.get("ejercicios", [])

                    # Parse if string
                    if isinstance(yaml_obj, str):
                        try:
                            # Replace backslashes
                            clean_yaml = yaml_obj.replace('\\', '\\\\')
                            # Fix YAML colon issues
                            clean_yaml = clean_yaml.replace(": $", " - $")
                            clean_yaml = clean_yaml.replace(": x", " - x")
                            yaml_obj = yaml.safe_load(clean_yaml)
                        except Exception as e:
                            print(f"Error parsing yaml string for {sid}: {e}")

                    if isinstance(jsonl_obj, str):
                        try:
                            clean_jsonl = jsonl_obj.replace('\\', '\\\\')
                            jsonl_obj = json.loads(clean_jsonl)
                        except:
                            pass

                    if isinstance(jsonl_obj, str):
                        try:
                            lines = []
                            for l in jsonl_obj.strip().split('\n'):
                                if l.strip():
                                    try:
                                        lines.append(json.loads(l.replace('\\', '\\\\')))
                                    except Exception as ex:
                                        # Fix common json errors
                                        fixed = l.replace('\\"', '"').replace("'", '"')
                                        try:
                                            lines.append(json.loads(fixed))
                                        except:
                                            pass
                            jsonl_obj = lines
                        except Exception as e:
                            print(f"Error parsing JSONL lines for {sid}: {e}")

                    all_topics[sid] = {"yaml": yaml_obj, "jsonl": jsonl_obj}
            else:
                print(f"Warning: {file_path} does not have 'topics'")
        except Exception as e:
            print(f"Error executing {file_path}: {e}")
    else:
        print(f"Missing {file_path}")

yaml_dir = r"C:\Users\PC\Documents\Proyectos\Web\profeonline\docs\conocimiento\contenido"
jsonl_file = r"C:\Users\PC\Documents\Proyectos\Web\profeonline\docs\conocimiento\ejercicios\mat-alg-desigualdades-banco-gen-final-real-pairs.jsonl"

def str_presenter(dumper, data):
    if '\n' in data or len(data) > 60 or data.startswith('###'):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

all_exs = []

def parse_solucion_pasos(sp):
    if isinstance(sp, list):
        return "\n".join([s if isinstance(s, str) else json.dumps(s, ensure_ascii=False) for s in sp])
    elif isinstance(sp, str):
        return sp
    return str(sp)

def parse_pasos_list(sp):
    if isinstance(sp, list):
        return [s if isinstance(s, str) else json.dumps(s, ensure_ascii=False) for s in sp]
    elif isinstance(sp, str):
        return [sp]
    return [str(sp)]

for sid, combined_data in all_topics.items():
    data = combined_data["yaml"]
    jsonl_data = combined_data["jsonl"]

    if not isinstance(data, dict):
        print(f"Skipping {sid} because yaml data is not a dict: {type(data)}")
        continue

    if "content" in data and "explicacion" in data["content"]:
        content_dict = data
        if "semantic_id" not in content_dict:
            content_dict["semantic_id"] = sid
    else:
        content_dict = {
            "semantic_id": data.get("semantic_id", sid),
            "title": data.get("titulo", data.get("title", "")),
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
                    "explicacion": parse_solucion_pasos(ej.get("solucion_pasos", ej.get("explicacion", [])))
                })
            else:
                content_dict["content"]["ejemplos_resueltos"].append({
                    "tipo": "abierto",
                    "titulo": ej.get("titulo", ""),
                    "enunciado": ej.get("enunciado", ""),
                    "pasos": parse_pasos_list(ej.get("solucion_pasos", ej.get("pasos", [])))
                })

    filename = os.path.join(yaml_dir, f"{sid.lower().replace('.', '-')}.yaml")
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.safe_dump(content_dict, f, allow_unicode=True, sort_keys=False)

    if not isinstance(jsonl_data, list):
        print(f"Skipping exercises for {sid} as it is not a list")
        continue

    for ej in jsonl_data:
        if not isinstance(ej, dict):
            continue

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
            "solution_steps": parse_solucion_pasos(ej.get("explicacion", ej.get("solucion", ej.get("solution_steps", ""))))
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
