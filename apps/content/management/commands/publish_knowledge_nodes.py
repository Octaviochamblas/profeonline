"""Publica los nodos-recurso cuyo contenido ya está marcado como 'publicado'.

`KnowledgeNode.is_published` es un flag independiente de `NodeContent.estado`
(que solo controla indexación SEO). Los nodos estructurales (asignatura/eje/
bloque/tema) se publican directamente en `import_knowledge_tree`; los recursos
se publican aquí, una vez que su contenido está listo, para no exponer páginas
sin contenido.

  python manage.py publish_knowledge_nodes
  python manage.py publish_knowledge_nodes --dry-run
"""

from django.core.management.base import BaseCommand

from apps.content.models import KnowledgeNode, NodeContent


class Command(BaseCommand):
    help = "Publica nodos-recurso cuyo NodeContent.estado es 'publicado'."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Mostrar qué se publicaría sin hacer cambios.",
        )

    def handle(self, *args, **options):
        qs = KnowledgeNode.objects.filter(
            node_type=KnowledgeNode.NODE_RECURSO,
            content__estado=NodeContent.ESTADO_PUBLICADO,
            is_published=False,
        )

        count = qs.count()
        if count == 0:
            self.stdout.write("No hay recursos pendientes de publicar.")
            return

        self.stdout.write(f"Recursos con contenido publicado pero sin publicar: {count}")
        if options["dry_run"]:
            for node in qs[:20]:
                self.stdout.write(f"  {node.semantic_id}")
            if count > 20:
                self.stdout.write(f"  ... y {count - 20} más.")
            self.stdout.write("(dry-run: sin cambios)")
            return

        published = qs.update(is_published=True)
        self.stdout.write(self.style.SUCCESS(f"Publicados: {published} recursos."))
