import glob
import re

files = glob.glob('docs/conocimiento/contenido/mat-alg-funcion-tipos-inversa-*.yaml')
pattern = re.compile(r'\$f: ')
fixed = []
for fn in files:
    text = open(fn, encoding='utf-8').read()
    new_text = pattern.sub(r'$f\\colon ', text)
    if new_text != text:
        open(fn, 'w', encoding='utf-8').write(new_text)
        fixed.append(fn)
print('fixed', len(fixed))
for f in fixed:
    print(f)
