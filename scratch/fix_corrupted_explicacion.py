import ast
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENIDO = ROOT / "docs" / "conocimiento" / "contenido"

FILES = [
    "mat-alg-sistemas_inecuaciones-interseccion_soluciones.yaml",
    "mat-alg-inecuaciones_valor_absoluto-mayor_que_positivo.yaml",
]

def clean(t: str) -> str:
    t = t.replace("\\n", "\n")
    t = re.sub(r"\\{2,}", r"\\", t)
    return t.strip()


for fname in FILES:
    path = CONTENIDO / fname
    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    exp = data["explicacion"]
    parsed = ast.literal_eval(exp)
    formal = clean(parsed[0])
    didactic = clean(parsed[1])
    new_value = formal + "\n\n" + didactic

    lines = raw.splitlines(keepends=True)
    start_idx = None
    for i, line in enumerate(lines):
        if line.startswith("explicacion:"):
            start_idx = i
            break
    assert start_idx is not None, f"no explicacion key in {fname}"
    end_idx = start_idx + 1
    while end_idx < len(lines) and not re.match(r"^[A-Za-z_][\w]*:", lines[end_idx]):
        end_idx += 1

    block_lines = ["explicacion: |-\n"]
    for line in new_value.split("\n"):
        block_lines.append(("  " + line).rstrip() + "\n" if line else "\n")

    new_lines = lines[:start_idx] + block_lines + lines[end_idx:]
    new_raw = "".join(new_lines)

    new_data = yaml.safe_load(new_raw)
    assert new_data["explicacion"] == new_value, f"round-trip mismatch in {fname}"
    assert new_data.get("procedimiento") == data.get("procedimiento")
    assert new_data.get("ejemplos") == data.get("ejemplos")

    path.write_text(new_raw, encoding="utf-8")
    print(f"Fixed {fname}: explicacion now {len(new_value)} chars, block lines {start_idx}-{end_idx-1} -> {len(block_lines)} lines")
