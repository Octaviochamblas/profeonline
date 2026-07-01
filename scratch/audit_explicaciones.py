import re
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENIDO = ROOT / "docs" / "conocimiento" / "contenido"

with open(ROOT / "scratch" / "loop_semantic_ids.txt", encoding="utf-8") as f:
    semantic_ids = [line.strip() for line in f if line.strip()]


def candidate_filenames(sid: str) -> list[str]:
    # Two conventions coexist in the repo:
    #  - fully dashed: MAT.ALG.POLINOMIOS.IGUALDAD_COEFICIENTES -> mat-alg-polinomios-igualdad-coeficientes.yaml
    #  - underscore-preserving (B0309): MAT.ALG.INECUACIONES_LINEALES.DEFINICION -> mat-alg-inecuaciones_lineales-definicion.yaml
    parts = sid.split(".")
    fully_dashed = "-".join(p.lower().replace("_", "-") for p in parts) + ".yaml"
    underscore_preserving = "-".join(p.lower() for p in parts) + ".yaml"
    legacy_upper_dotted = sid + ".yaml"
    return [fully_dashed, underscore_preserving, legacy_upper_dotted]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


missing_file = []
missing_formal = []
missing_didactic = []
short_formal = []
dup_with_procedimiento = []
dup_with_resumen = []
dup_with_errores = []

for sid in semantic_ids:
    candidates = candidate_filenames(sid)
    path = None
    fname = candidates[0]
    for c in candidates:
        p = CONTENIDO / c
        if p.exists():
            path = p
            fname = c
            break
    if path is None:
        missing_file.append((sid, " | ".join(candidates)))
        continue
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        missing_file.append((sid, f"YAML ERROR: {e}"))
        continue
    if not data:
        missing_file.append((sid, "EMPTY"))
        continue

    explicacion = data.get("explicacion", "") or ""
    m_formal = re.search(r"###\s*Definici[oó]n formal\s*\n+(.*?)(?:\n+###|\Z)", explicacion, re.S)
    m_didactic = re.search(r"###\s*Desarrollo\s+did[aá]ctico\s*\n+(.*)", explicacion, re.S)

    if not m_formal:
        missing_formal.append((sid, fname))
        continue
    if not m_didactic:
        missing_didactic.append((sid, fname))

    formal_text = m_formal.group(1).strip()
    formal_norm = norm(formal_text)

    if len(formal_text) < 30:
        short_formal.append((sid, fname, formal_text))

    procedimiento = data.get("procedimiento", []) or []
    if procedimiento and formal_norm and norm(procedimiento[-1]) == formal_norm:
        dup_with_procedimiento.append((sid, fname, formal_text[:80]))

    errores = data.get("errores_frecuentes", []) or []
    for e in errores:
        if norm(e) == formal_norm and formal_norm:
            dup_with_errores.append((sid, fname, formal_text[:80]))
            break

    resumen = data.get("resumen", "") or ""
    if formal_norm and formal_norm == norm(resumen):
        dup_with_resumen.append((sid, fname, formal_text[:80]))

out_path = ROOT / "scratch" / "audit_explicaciones_report.txt"
with open(out_path, "w", encoding="utf-8") as out:
    def w(line=""):
        out.write(str(line) + "\n")

    w(f"=== MISSING FILE / EMPTY / YAML ERROR === {len(missing_file)}")
    for x in missing_file:
        w(x)

    w(f"\n=== MISSING '### Definicion formal' HEADING === {len(missing_formal)}")
    for x in missing_formal:
        w(x)

    w(f"\n=== MISSING '### Desarrollo didactico' HEADING === {len(missing_didactic)}")
    for x in missing_didactic:
        w(x)

    w(f"\n=== SUSPICIOUSLY SHORT FORMAL (<30 chars) === {len(short_formal)}")
    for x in short_formal:
        w(x)

    w(f"\n=== FORMAL DUPLICATES LAST STEP OF PROCEDIMIENTO (bug pattern) === {len(dup_with_procedimiento)}")
    for x in dup_with_procedimiento:
        w(x)

    w(f"\n=== FORMAL DUPLICATES AN ERROR_FRECUENTE === {len(dup_with_errores)}")
    for x in dup_with_errores:
        w(x)

    w(f"\n=== FORMAL IDENTICAL TO RESUMEN VERBATIM === {len(dup_with_resumen)}")
    for x in dup_with_resumen:
        w(x)

with open(ROOT / "scratch" / "dup_procedimiento_files.txt", "w", encoding="utf-8") as f:
    for sid, fname, _ in dup_with_procedimiento:
        f.write(fname + "\n")

with open(ROOT / "scratch" / "missing_formal_files.txt", "w", encoding="utf-8") as f:
    for sid, fname in missing_formal:
        f.write(fname + "\n")

print(f"Report written to {out_path}")
print(f"missing_file={len(missing_file)} missing_formal={len(missing_formal)} missing_didactic={len(missing_didactic)} short_formal={len(short_formal)} dup_procedimiento={len(dup_with_procedimiento)} dup_errores={len(dup_with_errores)} dup_resumen={len(dup_with_resumen)}")
