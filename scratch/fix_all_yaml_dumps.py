import glob
import os
import re

py_files = glob.glob('scratch/build_alg_b0309_*.py')

for file_path in py_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to use json.dumps for all string values written to YAML to ensure perfect escaping.
    # But it's easier to just use yaml.dump instead of custom string formatting.
    # The subagents used hardcoded f.write lines.
    # Let's replace the f.write block with a proper yaml.dump loop.

    # However, rewriting their python AST is complex.
    # Instead, let's just use Python to load the 'data_yaml' list from the python script's source directly!

    # Extract the data_yaml variable
    match = re.search(r'data_yaml\s*=\s*(\[\s*\{.*\}\s*\])', content, re.DOTALL)
    if not match:
        continue

    import ast
    try:
        data_yaml = ast.literal_eval(match.group(1))
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        continue

    # Now write them using pyyaml properly
    import yaml

    class Dumper(yaml.SafeDumper):
        pass

    def str_presenter(dumper, data):
        if '\n' in data or len(data) > 80:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

    Dumper.add_representer(str, str_presenter)

    for item in data_yaml:
        yaml_path = f"docs/conocimiento/contenido/{item['semantic_id']}.yaml"
        # We need to preserve the specific order
        # semantic_id, titulo, objetivo, introduccion, resumen, explicacion, procedimiento, ejemplos, errores_frecuentes, fuente, estado
        with open(yaml_path, 'w', encoding='utf-8') as yf:
            yf.write(f"semantic_id: {item['semantic_id']}\n")
            for key in ['titulo', 'objetivo', 'introduccion', 'resumen', 'explicacion']:
                if key in item:
                    yf.write(yaml.dump({key: item[key]}, Dumper=Dumper, allow_unicode=True, default_flow_style=False))
            for key in ['procedimiento', 'ejemplos', 'errores_frecuentes']:
                if key in item:
                    yf.write(yaml.dump({key: item[key]}, Dumper=Dumper, allow_unicode=True, default_flow_style=False))
            for key in ['fuente', 'estado']:
                if key in item:
                    yf.write(yaml.dump({key: item[key]}, Dumper=Dumper, allow_unicode=True, default_flow_style=False))

    print(f"Rewrote YAMLs for {file_path} using proper PyYAML dump.")
