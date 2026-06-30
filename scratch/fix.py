import glob
import re

for f in glob.glob('docs/conocimiento/contenido/mat-alg-*.yaml'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()

    # Convert "..." to '...' for all string values to avoid escape sequence issues
    def replacer(match):
        inner = match.group(1)
        # Escape single quotes inside the single quoted string
        inner = inner.replace("'", "''")
        return f"'{inner}'"

    content = re.sub(r'\"([^\"]*)\"', replacer, content)

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
