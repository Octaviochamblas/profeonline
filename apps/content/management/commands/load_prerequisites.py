"""Carga el DAG de prerrequisitos (`NodePrerequisite`) desde YAML.

Formato (docs/conocimiento/dag/*.yaml):

    prerequisitos:
      - node: MAT.NUM.ENTEROS_OPERATORIA      # el que tiene prerrequisitos
        requires: MAT.NUM.ENTEROS_CONJUNTO    # el que se necesita antes
        kind: requerido                       # requerido | recomendado
        min_mastery: 0.75

Valida **aciclicidad** sobre el grafo final (existentes + nuevas) con `graphlib`
antes de escribir; si hay ciclo, aborta sin tocar la DB. Idempotente por
`(node, requires)`. Las aristas con `semantic_id` inexistente se omiten (aviso),
no son error fatal; un autoprerrequisito sí es error.
"""

from collections import defaultdict
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

import yaml
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.content.models import KnowledgeNode, NodePrerequisite

_VALID_KINDS = {NodePrerequisite.KIND_REQUERIDO, NodePrerequisite.KIND_RECOMENDADO}


class Command(BaseCommand):
    help = "Carga NodePrerequisite (DAG) desde YAML, validando aciclicidad."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",
            default="docs/conocimiento/dag",
            help="Directorio con los YAML del DAG (default: docs/conocimiento/dag)",
        )
        parser.add_argument("--file", default=None, help="Cargar un único YAML")

    def handle(self, *args, **options):
        if options["file"]:
            files = [Path(options["file"])]
        else:
            d = Path(options["dir"])
            files = sorted(d.glob("*.yaml")) + sorted(d.glob("*.yml"))

        raw_edges = []
        for path in files:
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if not data:
                continue
            items = data.get("prerequisitos") or data.get("prerrequisitos") or []
            for item in items:
                raw_edges.append((item, path.name))

        # Resolver semantic_ids (una sola consulta).
        sids = set()
        for item, _ in raw_edges:
            sids.add(item.get("node"))
            sids.add(item.get("requires"))
        sids.discard(None)
        nodes = {
            n.semantic_id: n
            for n in KnowledgeNode.objects.filter(semantic_id__in=sids)
        }

        skipped = 0
        edges = []  # (node, requires, kind, min_mastery)
        for item, fname in raw_edges:
            node_sid = item.get("node")
            req_sid = item.get("requires")
            if not node_sid or not req_sid:
                self.stderr.write(f"{fname}: arista incompleta {item} — omitida")
                skipped += 1
                continue
            if node_sid == req_sid:
                raise CommandError(f"Autoprerrequisito inválido: {node_sid} ({fname})")
            if node_sid not in nodes or req_sid not in nodes:
                self.stderr.write(
                    f"{fname}: semantic_id inexistente ({node_sid} ← {req_sid}) — omitida"
                )
                skipped += 1
                continue
            kind = item.get("kind", NodePrerequisite.KIND_REQUERIDO)
            if kind not in _VALID_KINDS:
                kind = NodePrerequisite.KIND_REQUERIDO
            edges.append((nodes[node_sid], nodes[req_sid], kind, item.get("min_mastery", 0.75)))

        # Validar aciclicidad sobre el grafo final (existentes + nuevas).
        graph = defaultdict(set)
        for pr in NodePrerequisite.objects.select_related("node", "requires"):
            graph[pr.node.semantic_id].add(pr.requires.semantic_id)
        for node, req, _, _ in edges:
            graph[node.semantic_id].add(req.semantic_id)
        try:
            TopologicalSorter(graph).prepare()
        except CycleError as exc:
            cycle = " → ".join(exc.args[1]) if len(exc.args) > 1 else str(exc)
            raise CommandError(f"Ciclo detectado en el DAG: {cycle}")

        created = updated = 0
        with transaction.atomic():
            for node, req, kind, min_mastery in edges:
                _, is_new = NodePrerequisite.objects.update_or_create(
                    node=node,
                    requires=req,
                    defaults={"kind": kind, "min_mastery": min_mastery},
                )
                if is_new:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Creados: {created}, Actualizados: {updated}, Omitidos: {skipped}"
            )
        )
