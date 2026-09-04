"""Audita el desfase entre los `semantic_id` de los YAML de contenido y el árbol.

`load_node_content` hace `KnowledgeNode.objects.get(semantic_id=...)` con match
EXACTO. Si un archivo de `docs/conocimiento/contenido/*.yaml` trae un `semantic_id`
que no existe en el árbol (construido por `import_knowledge_tree` desde los
skeletons atómicos), su contenido de 12 secciones NUNCA llega a la BD y la página
de `/aprender/` queda con el fallback genérico.

Uso:
    .venv/Scripts/python.exe manage.py shell -c "import scripts.audit_content_semantic_ids as a; a.run()"
o directo:
    .venv/Scripts/python.exe scripts/audit_content_semantic_ids.py

Salida: 3 baldes —
  rename_directo : el leaf existe igualito bajo otro bloque de la MISMA rama → cambio mecánico.
  revisar        : el leaf existe en varios bloques → elegir a mano.
  sin_destino    : el leaf no existe en la rama → mapear a un nodo con otro nombre
                   o crear el nodo en el skeleton atómico.
"""
from __future__ import annotations

import os
import pathlib
import sys

import yaml

CONTENIDO = pathlib.Path("docs/conocimiento/contenido")


def _bootstrap_django() -> None:
    sys.path.insert(0, os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    import django

    django.setup()


def run() -> dict[str, list[tuple[str, str]]]:
    from apps.content.models import KnowledgeNode

    live: set[str] = set(KnowledgeNode.objects.values_list("semantic_id", flat=True))
    by_leaf: dict[str, list[str]] = {}
    for sid in live:
        by_leaf.setdefault(sid.rsplit(".", 1)[-1], []).append(sid)

    buckets: dict[str, list[tuple[str, str]]] = {
        "rename_directo": [],
        "revisar": [],
        "sin_destino": [],
    }
    for path in sorted(CONTENIDO.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        sid = data.get("semantic_id")
        if not sid or sid in live:
            continue
        branch = ".".join(sid.split(".")[:2])  # MAT.NUM / MAT.ALG / ...
        leaf = sid.rsplit(".", 1)[-1]
        same_branch = sorted(c for c in by_leaf.get(leaf, []) if c.startswith(branch))
        if len(same_branch) == 1:
            buckets["rename_directo"].append((sid, same_branch[0]))
        elif same_branch:
            buckets["revisar"].append((sid, " | ".join(same_branch)))
        else:
            buckets["sin_destino"].append((sid, path.name))

    total = sum(len(v) for v in buckets.values())
    print(f"orphans: {total}\n")
    for name, rows in buckets.items():
        print(f"########## {name} ({len(rows)}) ##########")
        for a, b in rows:
            print(f"  {a:54s} -> {b}")
        print()
    return buckets


if __name__ == "__main__":
    _bootstrap_django()
    run()
