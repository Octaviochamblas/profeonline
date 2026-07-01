import glob
import json
import os

jsonl_files = glob.glob('docs/conocimiento/ejercicios/mat-alg-desigualdades-banco-gen-*.jsonl')

def fix_record(rec):
    new_rec = {}
    new_rec['stable_id'] = rec.get('stable_id')
    new_rec['semantic_id'] = rec.get('semantic_id')

    # map group
    group = rec.get('item_group') or rec.get('tipo') or rec.get('subnivel') or rec.get('tipo_ejercicio')
    if group == 'conceptual': group = 'conceptuales'
    if group == 'reconocimiento': group = 'reconocimiento'
    if group == 'procedimiento_basico': group = 'procedimiento_basico'
    if group == 'tipo_paes': group = 'tipo_paes'
    new_rec['item_group'] = group

    # format
    fmt = rec.get('format') or rec.get('formato') or rec.get('tipo_ejercicio')
    new_rec['format'] = fmt

    new_rec['difficulty'] = rec.get('difficulty', 'media')
    if new_rec['item_group'] == 'conceptuales' or new_rec['item_group'] == 'reconocimiento':
        new_rec['difficulty'] = 'basica'
    elif new_rec['item_group'] == 'tipo_paes':
        new_rec['difficulty'] = 'alta'

    new_rec['competencia'] = rec.get('competencia', 'M1')

    # prompt
    new_rec['prompt'] = rec.get('prompt') or rec.get('enunciado')

    if new_rec['format'] == 'multiple_choice':
        new_rec['choices'] = rec.get('choices') or rec.get('opciones')

    new_rec['correct_answer'] = rec.get('correct_answer') or rec.get('respuesta_correcta')

    sol = rec.get('solution_steps') or rec.get('solucion_pasos') or rec.get('solucion')
    if isinstance(sol, list):
        sol = " ".join(sol)
    new_rec['solution_steps'] = sol

    new_rec['status'] = 'ready'
    new_rec['source_kind'] = 'manual'
    if rec.get('paes_style') or rec.get('tipo_paes'):
        new_rec['paes_style'] = True

    # Extra check for boolean string answers in true_false
    if new_rec['format'] == 'true_false':
        if str(new_rec['correct_answer']).lower() == 'true' or str(new_rec['correct_answer']) == 'Verdadero':
            new_rec['correct_answer'] = 'Verdadero'
        else:
            new_rec['correct_answer'] = 'Falso'

    return new_rec

for file_path in jsonl_files:
    fixed_records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace literal \n with actual newline, except in some json contexts, but since the whole file is just json objects concatenated with literal \n
    content = content.replace('}\\n{', '}\n{')

    lines = content.split('\n')
    for line in lines:
        if not line.strip(): continue
        try:
            rec = json.loads(line)
            fixed_records.append(fix_record(rec))
        except Exception as e:
            print(f"Error parsing line in {file_path}: {e}")

    with open(file_path, 'w', encoding='utf-8') as f:
        for rec in fixed_records:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')

    print(f"Fixed {file_path}")
