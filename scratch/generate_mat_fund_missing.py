from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Iterable

import django
import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()


CONTENT_DIR = ROOT / "docs" / "conocimiento" / "contenido"
EJERCICIOS_DIR = ROOT / "docs" / "conocimiento" / "ejercicios"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

if not GEMINI_API_KEY:
    raise SystemExit("Falta GEMINI_API_KEY")


class Dumper(yaml.SafeDumper):
    pass


def _str_presenter(dumper, data):
    if isinstance(data, str) and "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


Dumper.add_representer(str, _str_presenter)


VALID_JSON_ESCAPE_NEXT = set('\"\\/bfnrtu')


def repair_json_line(raw: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(raw):
        ch = raw[i]
        if ch != "\\":
            out.append(ch)
            i += 1
            continue

        j = i
        while j < len(raw) and raw[j] == "\\":
            j += 1
        run_len = j - i
        next_char = raw[j] if j < len(raw) else ""

        if run_len % 2 == 0:
            out.append("\\" * run_len)
            i = j
            continue

        if next_char in VALID_JSON_ESCAPE_NEXT:
            out.append("\\" * run_len)
            i = j + 1
            continue

        out.append("\\" * (run_len + 1))
        i = j

    return "".join(out)


def call_gemini(prompt: str) -> dict:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 8000,
            "responseMimeType": "application/json",
            "thinkingConfig": {"thinkingBudget": 0},
        },
    }

    for attempt in range(4):
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        if response.status_code == 429:
            wait = 20 * (attempt + 1)
            print(f"    [Gemini 429] reintento en {wait}s")
            time.sleep(wait)
            continue
        response.raise_for_status()
        data = response.json()
        parts = data["candidates"][0]["content"]["parts"]
        text = "".join(part.get("text", "") for part in parts if not part.get("thought")).strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return json.loads(repair_json_line(text))

    raise RuntimeError("Gemini sigue devolviendo 429")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                rows.append(json.loads(repair_json_line(line)))
    return rows


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        yaml.dump(data, fh, Dumper=Dumper, allow_unicode=True, sort_keys=False)


def semantic_name(semantic_id: str) -> str:
    return semantic_id.split(".")[-1].replace("_", " ").title()


def short_abbr(semantic_id: str) -> str:
    return hashlib.sha1(semantic_id.encode("utf-8")).hexdigest()[:6].upper()


def yaml_filename(semantic_id: str) -> str:
    _, _, rest = semantic_id.split(".", 2)
    subtema, concepto = rest.split(".", 1)
    subtema_slug = subtema.lower().replace("_", "-")
    concepto_slug = concepto.lower().replace("_", "-")
    return f"mat-fund-{subtema_slug}-{concepto_slug}.yaml"


PROMPT_TEMPLATE = """
Eres un profesor de matemáticas experto y redactor de material pedagógico para ProfeOnline.
Debes generar contenido didáctico y 10 preguntas de evaluación para el siguiente recurso.

ID semántico: {semantic_id}
Nombre breve: {name}
Descripción breve: {description}

Responde ÚNICAMENTE con un objeto JSON válido con esta forma:
{{
  "content": {{
    "nombre": "Nombre didáctico del recurso",
    "objetivo": "Verbo en infinitivo más el logro.",
    "introduccion": "Texto amable y pedagógico de 2 o 3 párrafos.",
    "resumen": "Resumen técnico breve con notación matemática cuando convenga.",
    "explicacion": "Explicación formal en Markdown.",
    "procedimiento": ["Paso 1: ...", "Paso 2: ...", "Paso 3: ..."],
    "ejemplos": [
      {{"tipo": "A", "titulo": "...", "enunciado": "...", "solucion_pasos": "..." }},
      {{"tipo": "A", "titulo": "...", "enunciado": "...", "solucion_pasos": "..." }},
      {{"tipo": "B", "titulo": "...", "respuesta": "Sí o No o texto corto", "solucion_pasos": "..." }},
      {{"tipo": "B", "titulo": "...", "respuesta": "Sí o No o texto corto", "solucion_pasos": "..." }}
    ],
    "errores_frecuentes": ["...", "...", "...", "...", "..."],
    "fuente": "Una fuente breve y creíble"
  }},
  "exercises": [
    {{
      "item_group": "conceptuales",
      "format": "multiple_choice",
      "difficulty": "basica",
      "competencia": "U",
      "prompt": "...",
      "choices": ["...", "...", "...", "..."],
      "correct_answer": "...",
      "solution_steps": "..."
    }},
    {{
      "item_group": "conceptuales",
      "format": "multiple_choice",
      "difficulty": "basica",
      "competencia": "U",
      "prompt": "...",
      "choices": ["...", "...", "...", "..."],
      "correct_answer": "...",
      "solution_steps": "..."
    }},
    {{
      "item_group": "conceptuales",
      "format": "multiple_choice",
      "difficulty": "basica",
      "competencia": "U",
      "prompt": "...",
      "choices": ["...", "...", "...", "..."],
      "correct_answer": "...",
      "solution_steps": "..."
    }},
    {{
      "item_group": "reconocimiento",
      "format": "multiple_choice",
      "difficulty": "basica",
      "competencia": "U",
      "prompt": "...",
      "choices": ["...", "...", "...", "..."],
      "correct_answer": "...",
      "solution_steps": "..."
    }},
    {{
      "item_group": "procedimiento_basico",
      "format": "true_false",
      "difficulty": "basica",
      "competencia": "U",
      "prompt": "...",
      "correct_answer": "Verdadero o Falso",
      "solution_steps": "..."
    }},
    {{
      "item_group": "procedimiento_basico",
      "format": "true_false",
      "difficulty": "basica",
      "competencia": "U",
      "prompt": "...",
      "correct_answer": "Verdadero o Falso",
      "solution_steps": "..."
    }},
    {{
      "item_group": "procedimiento_basico",
      "format": "true_false",
      "difficulty": "basica",
      "competencia": "U",
      "prompt": "...",
      "correct_answer": "Verdadero o Falso",
      "solution_steps": "..."
    }},
    {{
      "item_group": "tipo_paes",
      "format": "multiple_choice",
      "difficulty": "media",
      "competencia": "U",
      "paes_style": true,
      "prompt": "...",
      "choices": ["...", "...", "...", "..."],
      "correct_answer": "...",
      "solution_steps": "..."
    }},
    {{
      "item_group": "tipo_paes",
      "format": "multiple_choice",
      "difficulty": "media",
      "competencia": "U",
      "paes_style": true,
      "prompt": "...",
      "choices": ["...", "...", "...", "..."],
      "correct_answer": "...",
      "solution_steps": "..."
    }},
    {{
      "item_group": "tipo_paes",
      "format": "multiple_choice",
      "difficulty": "media",
      "competencia": "U",
      "paes_style": true,
      "prompt": "...",
      "choices": ["...", "...", "...", "..."],
      "correct_answer": "...",
      "solution_steps": "..."
    }}
  ]
}}

Reglas:
- Usa lenguaje pedagógico claro, apropiado para 1°-2° Medio.
  - No uses LaTeX ni barras invertidas. Si necesitas notación matemática, usa símbolos Unicode
    como ∈, ⊆, ∪, ∩, ∅, →, ↔, ∀, ∃ y ×.
- Mantén exactamente 10 ejercicios y la distribución 3+1+3+3.
- No añadas texto fuera del JSON.
""".strip()


RESOURCE_BATCHES = [
    (
        "mat-fund-conjuntos-basicos-banco-gen-1.jsonl",
        [
            "MAT.FUND.CONJUNTOS_BASICOS.DEFINICION_CONJUNTO",
            "MAT.FUND.CONJUNTOS_BASICOS.NOTACION_LLAVES",
            "MAT.FUND.CONJUNTOS_BASICOS.ELEMENTO",
            "MAT.FUND.CONJUNTOS_BASICOS.PERTENENCIA",
            "MAT.FUND.CONJUNTOS_BASICOS.NO_PERTENENCIA",
            "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_EXTENSION",
            "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_COMPRENSION",
        ],
    ),
    (
        "mat-fund-conjuntos-basicos-banco-gen-2.jsonl",
        [
            "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_VACIO",
            "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_UNITARIO",
            "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_UNIVERSAL",
            "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_POTENCIA",
            "MAT.FUND.CONJUNTOS_BASICOS.CARDINALIDAD_CONJUNTO_POTENCIA",
        ],
    ),
    (
        "mat-fund-tablas-verdad-banco-gen-1.jsonl",
        [
            "MAT.FUND.TABLAS_VERDAD.TABLA_NEGACION",
            "MAT.FUND.TABLAS_VERDAD.TABLA_CONJUNCION",
            "MAT.FUND.TABLAS_VERDAD.TABLA_DISYUNCION_INCLUSIVA",
            "MAT.FUND.TABLAS_VERDAD.TABLA_DISYUNCION_EXCLUSIVA",
            "MAT.FUND.TABLAS_VERDAD.TABLA_CONDICIONAL",
            "MAT.FUND.TABLAS_VERDAD.TABLA_BICONDICIONAL",
            "MAT.FUND.TABLAS_VERDAD.FILAS_DOS_VARIABLES",
        ],
    ),
    (
        "mat-fund-tablas-verdad-banco-gen-2.jsonl",
        [
            "MAT.FUND.TABLAS_VERDAD.FILAS_TRES_VARIABLES",
            "MAT.FUND.TABLAS_VERDAD.CONSTRUCCION_DOS_VARIABLES",
            "MAT.FUND.TABLAS_VERDAD.CONSTRUCCION_TRES_VARIABLES",
            "MAT.FUND.TABLAS_VERDAD.TAUTOLOGIA",
            "MAT.FUND.TABLAS_VERDAD.CONTRADICCION",
            "MAT.FUND.TABLAS_VERDAD.CONTINGENCIA",
        ],
    ),
    (
        "mat-fund-cuantificadores-banco-gen-1.jsonl",
        [
            "MAT.FUND.CUANTIFICADORES.CUANTIFICADOR_UNIVERSAL",
            "MAT.FUND.CUANTIFICADORES.CUANTIFICADOR_EXISTENCIAL",
            "MAT.FUND.CUANTIFICADORES.DOMINIO_DE_DISCURSO",
            "MAT.FUND.CUANTIFICADORES.NEGACION_UNIVERSAL",
            "MAT.FUND.CUANTIFICADORES.NEGACION_EXISTENCIAL",
            "MAT.FUND.CUANTIFICADORES.CONTRAEJEMPLO",
        ],
    ),
    (
        "mat-fund-razonamiento-banco-gen-2.jsonl",
        [
            "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_INVERSO",
            "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_CONTRARRECIPROCO",
            "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_PONENS",
            "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_TOLLENS",
        ],
    ),
    (
        "mat-fund-diagramas-venn-banco-gen-1.jsonl",
        [
            "MAT.FUND.DIAGRAMAS_VENN.DIAGRAMA_UN_CONJUNTO",
            "MAT.FUND.DIAGRAMAS_VENN.DIAGRAMA_DOS_CONJUNTOS_DISJUNTOS",
            "MAT.FUND.DIAGRAMAS_VENN.DIAGRAMA_DOS_CONJUNTOS_INTERSECTADOS",
            "MAT.FUND.DIAGRAMAS_VENN.DIAGRAMA_TRES_CONJUNTOS",
            "MAT.FUND.DIAGRAMAS_VENN.REGIONES_DOS_CONJUNTOS",
            "MAT.FUND.DIAGRAMAS_VENN.REGIONES_TRES_CONJUNTOS",
        ],
    ),
    (
        "mat-fund-producto-cartesiano-banco-gen-2.jsonl",
        [
            "MAT.FUND.PRODUCTO_CARTESIANO.PRODUCTO_CARTESIANO_DEFINICION",
            "MAT.FUND.PRODUCTO_CARTESIANO.ELEMENTOS_PRODUCTO_CARTESIANO",
            "MAT.FUND.PRODUCTO_CARTESIANO.CARDINALIDAD_PRODUCTO_CARTESIANO",
            "MAT.FUND.PRODUCTO_CARTESIANO.REPRESENTACION_PLANO_CARTESIANO",
        ],
    ),
]


def make_prompt(semantic_id: str, batch_name: str) -> str:
    name = semantic_name(semantic_id)
    return PROMPT_TEMPLATE.format(
        semantic_id=semantic_id,
        name=name,
        description=name,
        batch=batch_name,
    )


def generate_resource(semantic_id: str, batch_name: str) -> tuple[dict, list[dict]]:
    prompt = make_prompt(semantic_id, batch_name)
    data = call_gemini(prompt)
    if not isinstance(data, dict) or "content" not in data or "exercises" not in data:
        raise ValueError(f"Respuesta inesperada para {semantic_id}: {type(data)!r}")
    content = data["content"]
    exercises = data["exercises"]
    if not isinstance(content, dict) or not isinstance(exercises, list):
        raise ValueError(f"Formato inválido para {semantic_id}")
    return content, exercises


def normalize_exercise(exercise: dict, semantic_id: str, abbr: str, index: int) -> dict:
    ex = dict(exercise)
    ex["semantic_id"] = semantic_id
    ex["stable_id"] = f"{abbr}-GEN-{ex.get('item_group', 'UNK').upper()[:4]}-{index}"
    ex.setdefault("competencia", "U")
    ex.setdefault("status", "ready")
    ex.setdefault("source_kind", "manual")
    if ex.get("item_group") == "tipo_paes":
        ex["paes_style"] = True
    return ex


def main() -> None:
    print("=== Generando MAT.FUND faltante ===")
    for batch_name, semantic_ids in RESOURCE_BATCHES:
        batch_path = EJERCICIOS_DIR / batch_name
        existing = read_jsonl(batch_path)
        existing_ids = {row.get("semantic_id") for row in existing if row.get("semantic_id")}
        rows = list(existing)
        print(f"\n--- {batch_name} ---")
        print(f"existentes: {len(existing_ids)} recursos")
        for semantic_id in semantic_ids:
            yaml_path = CONTENT_DIR / yaml_filename(semantic_id)
            abbr = short_abbr(semantic_id)
            if semantic_id in existing_ids and yaml_path.exists():
                print(f"  [skip] {semantic_id}")
                continue

            print(f"  [gen] {semantic_id}")
            content, exercises = generate_resource(semantic_id, batch_name)

            content = dict(content)
            content["semantic_id"] = semantic_id
            content["estado"] = "publicado"
            content.setdefault("nombre", semantic_name(semantic_id))
            content.setdefault("fuente", "ProfeOnline")

            if not yaml_path.exists():
                write_yaml(yaml_path, content)

            group_counts = {"conceptuales": 0, "reconocimiento": 0, "procedimiento_basico": 0, "tipo_paes": 0}
            for exercise in exercises:
                group = exercise.get("item_group", "conceptuales")
                group_counts[group] = group_counts.get(group, 0) + 1
                rows.append(normalize_exercise(exercise, semantic_id, abbr, group_counts[group]))

            time.sleep(30)

        rows_sorted = []
        seen = set()
        for row in rows:
            sid = row.get("semantic_id")
            if not sid or sid in seen:
                continue
            rows_sorted.append(row)
            seen.add(sid)
        # Preserve all rows including same semantic_id repeated across items.
        # Rebuild from the original rows while only de-duplicating exact stable IDs.
        cleaned_rows = []
        seen_stable_ids = set()
        for row in rows:
            stable_id = row.get("stable_id")
            if stable_id and stable_id in seen_stable_ids:
                continue
            if stable_id:
                seen_stable_ids.add(stable_id)
            cleaned_rows.append(row)
        write_jsonl(batch_path, cleaned_rows)
        print(f"  -> {len(cleaned_rows)} ejercicios escritos")

    print("\n=== Normalizando JSONL existentes ===")
    for path in sorted(EJERCICIOS_DIR.glob("mat-fund-*.jsonl")):
        rows = read_jsonl(path)
        write_jsonl(path, rows)
        print(f"  {path.name}: {len(rows)} líneas")


if __name__ == "__main__":
    main()
