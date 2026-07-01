import re
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENIDO = ROOT / "docs" / "conocimiento" / "contenido"

with open(ROOT / "scratch" / "dup_procedimiento_files.txt", encoding="utf-8") as f:
    filenames = [line.strip() for line in f if line.strip()]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


ITEM_START_RE = re.compile(r"^(\s*)-\s")

fixed = []
skipped = []

for fname in filenames:
    path = CONTENIDO / fname
    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    procedimiento = data.get("procedimiento") or []
    if len(procedimiento) < 2:
        skipped.append((fname, "procedimiento tiene <2 items, no se toca"))
        continue

    last_item_value = procedimiento[-1]
    last_norm = norm(last_item_value)

    lines = raw.splitlines(keepends=True)
    # Find the "procedimiento:" key line (top-level, column 0)
    proc_key_idx = None
    for i, line in enumerate(lines):
        if re.match(r"^procedimiento:\s*$", line):
            proc_key_idx = i
            break
    if proc_key_idx is None:
        skipped.append((fname, "no se encontro 'procedimiento:' como bloque de lista"))
        continue

    # Collect item blocks: each starts with '- ' at some indentation, continues
    # until the next line at the same indentation starting with '- ', or a
    # top-level key (column 0, matches ^\w+:), or end of file.
    item_starts = []
    base_indent = None
    j = proc_key_idx + 1
    while j < len(lines):
        line = lines[j]
        if re.match(r"^\S", line) and not ITEM_START_RE.match(line):
            break
        m = ITEM_START_RE.match(line)
        if m:
            indent = len(m.group(1))
            if base_indent is None:
                base_indent = indent
            if indent == base_indent:
                item_starts.append(j)
        j += 1
    block_end = j  # exclusive

    if len(item_starts) != len(procedimiento):
        skipped.append((fname, f"conteo de items no coincide (yaml={len(procedimiento)}, texto={len(item_starts)})"))
        continue

    last_block_start = item_starts[-1]
    last_block_lines = lines[last_block_start:block_end]
    last_block_text = "".join(last_block_lines)

    # Sanity check: parse just this one item back via yaml to compare with expected value
    try:
        parsed_last = yaml.safe_load(last_block_text)
        parsed_value = parsed_last[0] if isinstance(parsed_last, list) else None
    except Exception:
        parsed_value = None

    if parsed_value is None or norm(parsed_value) != last_norm:
        skipped.append((fname, "no se pudo verificar el bloque de texto del ultimo item"))
        continue

    if re.match(r"^['\"]?Paso\s*\d+\s*:", parsed_value.strip()):
        skipped.append((fname, "el ultimo item SI tiene prefijo 'Paso N:', no se toca"))
        continue

    new_lines = lines[:last_block_start] + lines[block_end:]
    new_raw = "".join(new_lines)

    # Verify the resulting file still parses and procedimiento shrank by exactly 1
    new_data = yaml.safe_load(new_raw)
    new_procedimiento = new_data.get("procedimiento") or []
    if len(new_procedimiento) != len(procedimiento) - 1:
        skipped.append((fname, "verificacion post-edicion fallo (conteo)"))
        continue
    if new_procedimiento != procedimiento[:-1]:
        skipped.append((fname, "verificacion post-edicion fallo (contenido distinto)"))
        continue

    path.write_text(new_raw, encoding="utf-8")
    fixed.append(fname)

print(f"fixed={len(fixed)} skipped={len(skipped)}")
out = ROOT / "scratch" / "fix_procedimiento_dup_report.txt"
with open(out, "w", encoding="utf-8") as f:
    f.write(f"FIXED ({len(fixed)}):\n")
    for x in fixed:
        f.write(x + "\n")
    f.write(f"\nSKIPPED ({len(skipped)}):\n")
    for x in skipped:
        f.write(str(x) + "\n")
print(f"Report: {out}")
