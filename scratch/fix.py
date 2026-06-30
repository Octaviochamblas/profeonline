import glob
import re

for f in glob.glob('docs/conocimiento/contenido/mat-alg-mult-*.yaml'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace double quotes around values containing backslashes with single quotes
    # The regex matches "..." where the content inside has a \
    # But YAML steps often start with - "..."
    # Actually, the simplest is to replace all "- \"" with "- '" and ending "\"" with "'"
    content = re.sub(r'- "(.*?)"', r"- '\1'", content)
    
    # Also for text: "..."
    content = re.sub(r'text: "(.*?)"', r"text: '\1'", content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
