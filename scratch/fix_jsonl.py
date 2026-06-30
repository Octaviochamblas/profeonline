import json

# Map 'kind' to 'item_group'
kind_map = {
    "conceptual": "conceptuales",
    "reconocimiento": "reconocimiento",
    "procedimiento_basico": "procedimiento_basico",
    "tipo_paes": "tipo_paes"
}

exercises = []
with open('docs/conocimiento/ejercicios/mat-alg-multiplicacion-banco-gen-4.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if not line.strip(): continue
        ex = json.loads(line)

        node_id = ex.get('node_id')
        kind = ex.get('kind')

        # Build stable_id
        prefix = "GEN4"
        if node_id == "MAT.ALG.MULT_MON_POL.MONOMIO_NEGATIVO": prefix = "MN"
        elif node_id == "MAT.ALG.MULT_POLINOMIOS.COEFICIENTES_FRACCIONARIOS": prefix = "CF"
        elif node_id == "MAT.ALG.MULT_MONOMIOS.GRADO_PRODUCTO": prefix = "GP"
        elif node_id == "MAT.ALG.MULT_MON_POL.DISTRIBUCION_PARCIAL_ERROR": prefix = "DPE"

        stable_id = f"{prefix}-{kind_map[kind].upper()}-{i}"

        # Build choices
        options = ex.get('options', [])
        letters = ['A) ', 'B) ', 'C) ', 'D) ']
        choices = []
        correct_ans = ""
        for j, opt in enumerate(options):
            txt = letters[j] + opt['text']
            choices.append(txt)
            if opt.get('is_correct'):
                correct_ans = txt

        new_ex = {
            "stable_id": stable_id,
            "semantic_id": node_id,
            "item_group": kind_map[kind],
            "format": "multiple_choice",
            "difficulty": ex.get('difficulty'),
            "competencia": "M1",
            "prompt": ex.get('text'),
            "choices": choices,
            "correct_answer": correct_ans,
            "solution_steps": ex.get('explanation'),
            "paes_style": (kind == "tipo_paes")
        }
        exercises.append(new_ex)

with open('docs/conocimiento/ejercicios/mat-alg-multiplicacion-banco-gen-4.jsonl', 'w', encoding='utf-8') as f:
    for ex in exercises:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")
