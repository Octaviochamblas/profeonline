import glob
import os
import re

yaml_files = glob.glob('docs/conocimiento/contenido/MAT.ALG.*.yaml')

for file_path in yaml_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to replace all single backslashes with double backslashes
    # but not if they are already double backslashes.
    # A negative lookbehind for '\' and negative lookahead for '\'
    content = re.sub(r'(?<!\\)\\(?!\\)', r'\\\\', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done fixing all escapes.")
