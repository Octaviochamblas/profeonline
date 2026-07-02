"""Importa el árbol de conocimiento (KnowledgeNode) desde los YAML atómicos.

Lee los archivos de `docs/conocimiento/*.yaml` que cumplen el estándar atómico
EE.BB.TT.RR (con `codigo`, `bloque_codigo` y `temas[].id`) y los vuelca a la tabla
`KnowledgeNode` como un árbol Asignatura > Eje > Bloque > Tema > Recurso.

Es idempotente: el upsert es por `semantic_id`, así que correrlo dos veces no duplica.
Los archivos legacy de resumen (sin `codigo`/`bloque_codigo`) se omiten con aviso.
"""

from pathlib import Path

import yaml
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.content.models import KnowledgeNode

SUBJECT_NAMES = {
    "MAT": "Matemáticas",
    "FIS": "Física",
    "QUI": "Química",
}


class Command(BaseCommand):
    help = (
        "Importa el árbol de conocimiento desde los YAML atómicos "
        "(docs/conocimiento/*.yaml con formato EE.BB.TT.RR). Idempotente por semantic_id."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",
            dest="dir",
            default=None,
            help="Directorio con los YAML (default: docs/conocimiento).",
        )
        parser.add_argument(
            "--file",
            dest="file",
            default=None,
            help="Importar un único archivo YAML en vez de todo el directorio.",
        )

    def handle(self, *args, **options):
        self.verbosity = options.get("verbosity", 1)
        self.created = 0
        self.existing = 0
        self.skipped = []
        self._cache = {}

        files = self._resolve_files(options)

        with transaction.atomic():
            for yaml_file in files:
                self._import_file(yaml_file)

        total = KnowledgeNode.objects.count()
        if self.verbosity:
            if self.skipped:
                self.stdout.write(
                    self.style.WARNING(
                        f"Omitidos {len(self.skipped)} archivo(s) no atómicos: "
                        + ", ".join(self.skipped)
                    )
                )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Import OK. Creados: {self.created}, Existentes: {self.existing}. "
                    f"Total nodos en DB: {total}"
                )
            )

    # ------------------------------------------------------------------ helpers

    def _resolve_files(self, options):
        if options["file"]:
            path = Path(options["file"])
            if not path.is_file():
                raise CommandError(f"No existe el archivo: {path}")
            return [path]

        base = options["dir"]
        conocimiento_dir = (
            Path(base) if base else Path(settings.BASE_DIR) / "docs" / "conocimiento"
        )
        if not conocimiento_dir.is_dir():
            raise CommandError(f"No existe el directorio: {conocimiento_dir}")

        files = sorted(
            f for f in conocimiento_dir.glob("*.yaml") if not f.name.startswith("_")
        )
        if not files:
            raise CommandError(f"No se encontraron YAML en {conocimiento_dir}")
        return files

    def _import_file(self, yaml_file):
        try:
            with open(yaml_file, encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
        except (OSError, yaml.YAMLError) as exc:
            raise CommandError(f"Error leyendo {yaml_file.name}: {exc}") from exc

        # Solo formato atómico: requiere codigo (eje) + bloque_codigo + temas.
        if (
            not isinstance(data, dict)
            or not data.get("codigo")
            or not data.get("bloque_codigo")
            or not data.get("temas")
        ):
            self.skipped.append(yaml_file.name)
            return

        abreviatura = data.get("abreviatura") or ""
        eje_codigo = str(data["codigo"])
        rama = data.get("rama") or abreviatura
        bloque_nombre = data.get("bloque") or ""
        bloque_codigo = str(data["bloque_codigo"])
        temas = data["temas"]

        subject_abbr = self._derive_subject(temas)
        if not subject_abbr:
            self.skipped.append(yaml_file.name)
            return

        asignatura = self._upsert(
            subject_abbr,
            dict(
                code=subject_abbr,
                node_type=KnowledgeNode.NODE_ASIGNATURA,
                parent=None,
                subject_abbr=subject_abbr,
                axis_abbr="",
                name=SUBJECT_NAMES.get(subject_abbr, subject_abbr),
                order=0,
                is_published=True,
            ),
        )

        eje = self._upsert(
            f"{subject_abbr}.{abreviatura}",
            dict(
                code=eje_codigo,
                node_type=KnowledgeNode.NODE_EJE,
                parent=asignatura,
                subject_abbr=subject_abbr,
                axis_abbr=abreviatura,
                name=rama,
                order=self._int(eje_codigo),
                is_published=True,
            ),
        )

        bloque = self._upsert(
            f"{subject_abbr}.{abreviatura}.B{bloque_codigo.replace('.', '')}",
            dict(
                code=bloque_codigo,
                node_type=KnowledgeNode.NODE_BLOQUE,
                parent=eje,
                subject_abbr=subject_abbr,
                axis_abbr=abreviatura,
                name=bloque_nombre,
                order=self._last_segment(bloque_codigo),
                is_published=True,
            ),
        )

        for t_index, tema in enumerate(temas, start=1):
            if not isinstance(tema, dict) or not tema.get("id"):
                continue
            tema_comp = tema.get("competencia", "") or ""
            tema_node = self._upsert(
                tema["id"],
                dict(
                    code=str(tema.get("codigo", "")),
                    node_type=KnowledgeNode.NODE_TEMA,
                    parent=bloque,
                    subject_abbr=subject_abbr,
                    axis_abbr=abreviatura,
                    name=tema.get("nombre", tema["id"]),
                    competencia=tema_comp,
                    order=t_index,
                    is_published=True,
                ),
            )
            for r_index, rec in enumerate(tema.get("recursos") or [], start=1):
                if not isinstance(rec, dict) or not rec.get("id"):
                    continue
                self._upsert(
                    rec["id"],
                    dict(
                        code=str(rec.get("cod", "")),
                        node_type=KnowledgeNode.NODE_RECURSO,
                        parent=tema_node,
                        subject_abbr=subject_abbr,
                        axis_abbr=abreviatura,
                        name=rec.get("nombre", rec["id"]),
                        competencia=rec.get("competencia", tema_comp) or "",
                        dificultad=rec.get("dificultad", "") or "",
                        cursos=rec.get("cursos") or [],
                        order=r_index,
                    ),
                )

    def _derive_subject(self, temas):
        """La asignatura es el primer segmento del id de un tema/recurso (MAT.…)."""
        for tema in temas:
            if not isinstance(tema, dict):
                continue
            tid = tema.get("id", "") or ""
            if "." in tid:
                return tid.split(".", 1)[0]
            for rec in tema.get("recursos") or []:
                rid = (rec or {}).get("id", "") or ""
                if "." in rid:
                    return rid.split(".", 1)[0]
        return None

    def _int(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def _last_segment(self, code):
        return self._int(str(code).split(".")[-1])

    def _upsert(self, semantic_id, defaults):
        if semantic_id in self._cache:
            return self._cache[semantic_id]
        obj, created = KnowledgeNode.objects.update_or_create(
            semantic_id=semantic_id, defaults=defaults
        )
        if created:
            self.created += 1
        else:
            self.existing += 1
        self._cache[semantic_id] = obj
        return obj
