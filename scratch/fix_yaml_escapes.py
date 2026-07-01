import glob
import os
import re

yaml_files = glob.glob('docs/conocimiento/contenido/MAT.ALG.*.yaml')

for file_path in yaml_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to escape backslashes that are part of LaTeX commands inside double-quoted strings.
    # It's safer to just replace all backslashes that precede characters commonly used in our LaTeX.
    # Actually, the python yaml parser throws error for \l, \g, \i, \n (if not intended as newline), etc.
    # Since these are math strings, let's just replace all single backslashes with double backslashes
    # inside the lines that start with `- "` or are inside `"` in general.
    # An easier way is to just do specific replacements for common math symbols used in this module.

    replacements = [
        (r'\leq', r'\\leq'),
        (r'\geq', r'\\geq'),
        (r'\in', r'\\in'),
        (r'\notin', r'\\notin'),
        (r'\infty', r'\\infty'),
        (r'\to', r'\\to'),
        (r'\cup', r'\\cup'),
        (r'\cap', r'\\cap'),
        (r'\mathbb', r'\\mathbb'),
        (r'\left', r'\\left'),
        (r'\right', r'\\right'),
        (r'\frac', r'\\frac'),
        (r'\cdot', r'\\cdot'),
        (r'\neq', r'\\neq'),
        (r'\sqrt', r'\\sqrt'),
        (r'\{', r'\\{'),
        (r'\}', r'\\}')
    ]

    original = content
    for old, new in replacements:
        # We only want to replace if it is preceded by a single backslash, not a double backslash.
        # It's simpler to replace all occurrences of `\leq` with `\\leq` if it is not already `\\leq`.
        # using negative lookbehind
        pattern = r'(?<!\\)' + old.replace('\\', '\\\\')
        content = re.sub(pattern, new, content)

    if original != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed escapes in {file_path}")

print("Done fixing escapes.")
