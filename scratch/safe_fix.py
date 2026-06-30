import glob

# Fix YAMLs
for f in glob.glob('docs/conocimiento/contenido/mat-alg-mult-*.yaml'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('node_id:', 'semantic_id:')
    content = content.replace('objective:', 'objetivo:')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

# Fix JSONL
for f in glob.glob('docs/conocimiento/ejercicios/mat-alg-multiplicacion-banco-gen-4.jsonl'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('\\n', '\n')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
