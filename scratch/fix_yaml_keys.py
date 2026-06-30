import glob
import re

def fix_yaml_keys():
    files = glob.glob('docs/conocimiento/contenido/*.yaml')
    count = 0
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '- title:' in content or '  title:' in content:
            # replace `- title:` with `- titulo:`
            content = re.sub(r'(\s+)-\s+title:\s+', r'\1- titulo: ', content)
            # replace `text:` with `enunciado:`
            content = re.sub(r'(\s+)text:\s+', r'\1enunciado: ', content)
            # replace `steps:` with `solucion_pasos:`
            content = re.sub(r'(\s+)steps:\s*', r'\1solucion_pasos:', content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {filepath}")
            count += 1
    print(f"Fixed {count} files.")

if __name__ == "__main__":
    fix_yaml_keys()
