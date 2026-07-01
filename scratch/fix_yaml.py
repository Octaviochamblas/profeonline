import glob

def fix_yaml_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_solucion_pasos = False

    for line in lines:
        if line.strip() == "solucion_pasos:":
            in_solucion_pasos = True
            new_lines.append(line)
            continue

        if in_solucion_pasos:
            if line.startswith("  - '"):
                # Increase indentation by 2 spaces
                line = "  " + line
            else:
                in_solucion_pasos = False

        new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

for filepath in glob.glob("docs/conocimiento/contenido/mat-alg-*.yaml"):
    fix_yaml_file(filepath)

print("Fixed YAML indentation!")
