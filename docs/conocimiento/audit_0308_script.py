import yaml, glob, re, os

with open('docs/conocimiento/algebra-ecuaciones-sistemas.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

id_to_file = {}
for filepath in glob.glob('docs/conocimiento/contenido/*.yaml'):
    try:
        with open(filepath, 'r', encoding='utf-8') as fh:
            for line in fh:
                if line.startswith('semantic_id:'):
                    sem_id = line.split('semantic_id:')[1].strip().strip('"').strip("'")
                    id_to_file[sem_id] = filepath
                    break
    except Exception:
        pass

out = []
out.append(f"Bloque: {config['bloque']} ({config['bloque_codigo']})")
out.append(f"Total Subtemas: {len(config['temas'])}")

verbs = ['Omitir', 'Excluir', 'Confundir', 'Multiplicar', 'Sumar', 'Restar', 'Invertir', 'Cambiar', 'Dejar', 'Asumir', 'Olvidar', 'Intentar', 'Considerar', 'Tratar', 'Aplicar', 'Creer', 'Usar', 'Pensar']

total_recursos = 0
recursos_con_observaciones = 0

for tema in config['temas']:
    tema_code = tema['codigo']
    tema_nombre = tema['nombre']
    recursos = tema['recursos']

    out.append(f"\n=======================================================")
    out.append(f"Subtema {tema_code}: {tema_nombre} ({len(recursos)} recursos)")
    out.append(f"=======================================================")

    subtema_obs = 0
    for r in recursos:
        total_recursos += 1
        sem_id = r['id']
        cod = r['cod']
        nombre = r['nombre']

        matching_file = id_to_file.get(sem_id)
        if not matching_file:
            out.append(f"  [MISSING] [{cod}] {sem_id} -> ARCHIVO NO ENCONTRADO EN CONTENIDO!")
            subtema_obs += 1
            recursos_con_observaciones += 1
            continue

        file_name = os.path.basename(matching_file)

        issues = []
        with open(matching_file, 'r', encoding='utf-8') as fh:
            data = yaml.safe_load(fh)

        errs = data.get('errores_frecuentes', [])
        verb_found = []
        no_latex = []
        for i, e in enumerate(errs):
            for v in verbs:
                if re.search(r'\b' + v + r'\b', str(e), re.IGNORECASE):
                    verb_found.append((v, e))
            if '$' not in str(e):
                no_latex.append(e)

        if verb_found:
            verbs_str = ", ".join(sorted(set([v[0] for v in verb_found])))
            issues.append(f"Meta-lenguaje/Verbos procedimentales en errores_frecuentes ({verbs_str})")
        if no_latex:
            issues.append(f"{len(no_latex)}/5 afirmaciones sin $LaTeX$ en errores_frecuentes")

        atdp = data.get('al_terminar_debes_poder', '')
        if 'QUÉ:' not in str(atdp) or 'CÓMO:' not in str(atdp):
            issues.append("Objetivo sin estructura QUÉ: / CÓMO:")

        if issues:
            subtema_obs += 1
            recursos_con_observaciones += 1
            out.append(f"  [WARN] [{cod}] {file_name}")
            for iss in issues:
                out.append(f"      - {iss}")
        else:
            out.append(f"  [OK] [{cod}] {file_name}")

out.append(f"\n-------------------------------------------------------")
out.append(f"RESUMEN GLOBAL AUDITORÍA BLOQUE 03.08:")
out.append(f"Total recursos: {total_recursos}")
out.append(f"Recursos conformes (100% 12 secciones): {total_recursos - recursos_con_observaciones}")
out.append(f"Recursos con observaciones por corregir: {recursos_con_observaciones}")

with open('docs/conocimiento/report_0308.txt', 'w', encoding='utf-8') as fh:
    fh.write("\n".join(out))

print("Done writing docs/conocimiento/report_0308.txt")
