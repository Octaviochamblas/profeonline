import glob
import re

files = glob.glob('docs/conocimiento/contenido/mat-alg-*.yaml')

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find "procedimiento: |" and all indented lines after it until the next unindented key
    match = re.search(r'^procedimiento:\s*\|(.*?)^\w+:', content, re.MULTILINE | re.DOTALL)
    if not match:
        continue

    proc_block = match.group(1)
    lines = proc_block.strip().split('\n')
    
    new_lines = []
    step_num = 1
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Remove numbers like "1. " or "Paso 1: " or just text if it's an intro
        line = re.sub(r'^\d+\.\s*', '', line)
        line = re.sub(r'^Paso\s*\d+:\s*', '', line)
        line = line.replace("'", "''") # escape single quotes for YAML
        
        # If it's an intro line like "Para entender la regla:" we can make it step 1 or ignore it?
        # Actually it's better to just include it as a step.
        new_lines.append(f"  - 'Paso {step_num}: {line}'")
        step_num += 1

    new_proc = "procedimiento:\n" + "\n".join(new_lines) + "\n"
    
    # Replace the old block
    new_content = content[:match.start()] + new_proc + content[match.end()-len(match.group(0).split('\n')[-1]):]

    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)

print(f"Processed {len(files)} files.")
