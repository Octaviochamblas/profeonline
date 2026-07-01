import os
import glob
import json

mapping = {
    "MAT.ALG.FACTOR_CUADRADOS.DIFERENCIA_CUADRADOS": "MAT.ALG.FACTOR_CUADRADOS.RECONOCIMIENTO_DIFERENCIA_CUADRADOS",
    "MAT.ALG.FACTOR_CUADRADOS.CASOS_ESPECIALES_DIFERENCIA": "MAT.ALG.FACTOR_CUADRADOS.FACTORIZACION_DIFERENCIA_CUADRADOS",
    "MAT.ALG.FACTOR_CUADRADOS.SUMA_CUADRADOS": "MAT.ALG.FACTOR_CUADRADOS.RECONOCIMIENTO_TRINOMIO_CUADRADO",
    "MAT.ALG.FACTOR_CUADRADOS.TRINOMIO_CUADRADO_PERFECTO": "MAT.ALG.FACTOR_CUADRADOS.FACTORIZACION_TRINOMIO_CUADRADO",
    "MAT.ALG.FACTOR_CUADRADOS.EVALUACION_TCP": "MAT.ALG.FACTOR_CUADRADOS.SIGNO_TERMINO_CENTRAL",
    "MAT.ALG.FACTOR_CUADRADOS.COMBINACION_CUADRADOS": "MAT.ALG.FACTOR_CUADRADOS.COMPLETACION_CUADRADO"
}

# 1. Update YAML files
for old_id, new_id in mapping.items():
    old_filename = f"docs/conocimiento/contenido/{old_id.lower().replace('.', '-').replace('_', '-')}.yaml"
    new_filename = f"docs/conocimiento/contenido/{new_id.lower().replace('.', '-').replace('_', '-')}.yaml"

    if os.path.exists(old_filename):
        with open(old_filename, 'r', encoding='utf-8') as f:
            content = f.read()

        content = content.replace(f"semantic_id: '{old_id}'", f"semantic_id: '{new_id}'")

        with open(new_filename, 'w', encoding='utf-8') as f:
            f.write(content)

        os.remove(old_filename)
        print(f"Renamed {old_filename} to {new_filename}")

# 2. Update JSONL file
jsonl_file = "docs/conocimiento/ejercicios/mat-alg-factorizacion-banco-gen-3.jsonl"
if os.path.exists(jsonl_file):
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for line in lines:
            if not line.strip(): continue
            doc = json.loads(line)
            if doc['semantic_id'] in mapping:
                doc['semantic_id'] = mapping[doc['semantic_id']]
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    print(f"Updated {jsonl_file}")
