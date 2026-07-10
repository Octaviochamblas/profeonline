"""Genera y publica las preguntas de evaluación faltantes para todos los nodos.

Arma el entorno (variables del servicio `web` en Railway + `DATABASE_URL`
pública del servicio Postgres, porque el host interno `postgres.railway.internal`
no es alcanzable desde esta máquina) y corre
`generate_node_assessment_questions --all --publish` en bucle hasta que el
déficit llegue a cero o se agoten los reintentos (el comando es idempotente:
cada corrida solo genera lo que falta, así que reintentar tras un fallo
puntual de Gemini es seguro).

Requiere: `railway link` ya hecho en este repo, y la CLI de Railway logueada.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PYTHON = BASE_DIR / "venv" / "Scripts" / "python.exe"
FULLY_POPULATED_MARKER = "Se generarían 0 preguntas"
RAILWAY = shutil.which("railway")
if not RAILWAY:
    sys.exit("No se encontró el ejecutable 'railway' en el PATH.")


def _parse_kv_value(kv_output, key):
    """Extrae el valor de `key=valor` de la salida de `railway variables --kv`."""
    for line in kv_output.splitlines():
        if line.startswith(f"{key}="):
            return line[len(key) + 1:]
    raise ValueError(f"No se encontró {key!r} en la salida de railway variables")


def build_env():
    web_vars = json.loads(
        subprocess.run(
            ["railway", "variables", "--service", "web", "--json"],
            cwd=BASE_DIR, capture_output=True, text=True, check=True,
        ).stdout
    )
    pg_kv = subprocess.run(
        ["railway", "variables", "--service", "Postgres", "--kv"],
        cwd=BASE_DIR, capture_output=True, text=True, check=True,
    ).stdout
    env = dict(web_vars)
    env["DATABASE_URL"] = _parse_kv_value(pg_kv, "DATABASE_PUBLIC_URL")
    return env


def run_manage(env, *args):
    result = subprocess.run(
        [str(PYTHON), "manage.py", "generate_node_assessment_questions", *args],
        cwd=BASE_DIR, env=env, capture_output=True, text=True,
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.stdout


def _is_fully_populated(dry_run_output):
    return FULLY_POPULATED_MARKER in dry_run_output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node", help="Procesar un solo nodo (semantic_id) en vez de --all.")
    parser.add_argument("--max-retries", type=int, default=3, help="Reintentos de --publish si queda déficit (def. 3).")
    parser.add_argument("--dry-run-only", action="store_true", help="Solo mostrar el déficit, no generar nada.")
    args = parser.parse_args()

    target = ["--node", args.node] if args.node else ["--all"]
    env = build_env()

    print("== Déficit inicial ==")
    run_manage(env, *target, "--dry-run")
    if args.dry_run_only:
        return

    for attempt in range(1, args.max_retries + 1):
        print(f"== Generando y publicando (intento {attempt}/{args.max_retries}) ==")
        run_manage(env, *target, "--publish")

        print("== Verificando déficit restante ==")
        remaining = run_manage(env, *target, "--dry-run")
        if _is_fully_populated(remaining):
            print("Listo: no queda déficit.")
            return

    print(f"Quedó déficit tras {args.max_retries} intentos. Revisa el output de arriba.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        assert _parse_kv_value("A=1\nB=2\n", "B") == "2"
        assert _is_fully_populated("Se generarían 0 preguntas de evaluación.")
        assert not _is_fully_populated("Se generarían 21 preguntas de evaluación.")
        print("selftest OK")
        sys.exit(0)
    main()
