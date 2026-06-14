"""Crea una guía de referencia (QuizGuide) desde un archivo o texto y la vincula.

La guía es reutilizable: se vincula a recursos, temas o asignaturas (por slug), y al
generar preguntas la IA mimetiza su estilo de ejercicios y usa su contenido.

Ejemplos:
    # Desde un PDF, aplicada a toda una asignatura:
    python manage.py import_quiz_guide --file "C:/guias/paes.pdf" \
        --title "Estilo PAES" --subject matematica-escolar

    # Desde texto pegado, aplicada a un tema y un recurso puntual:
    python manage.py import_quiz_guide --text "Ejercicio tipo: ..." \
        --title "Guía integrales" --topic integrales-multiples --resource mi-slug
"""

import os

from django.core.management.base import BaseCommand, CommandError

from apps.content.models import QuizGuide, Resource, Subject, Topic
from apps.content.services.guide_service import extract_guide_text, normalize_text


class Command(BaseCommand):
    help = "Crea una QuizGuide desde un archivo (PDF/Word/texto) o --text y la vincula por slug."

    def add_arguments(self, parser):
        parser.add_argument("--file", default=None, help="Ruta al material (PDF, .docx, .txt, .md).")
        parser.add_argument("--text", default=None, help="Texto de la guía, como alternativa a --file.")
        parser.add_argument("--title", required=True, help="Título de la guía.")
        parser.add_argument("--description", default="", help="Descripción opcional.")
        parser.add_argument("--subject", action="append", default=[], dest="subjects",
                            help="Slug de asignatura a vincular (repetible).")
        parser.add_argument("--topic", action="append", default=[], dest="topics",
                            help="Slug de tema a vincular (repetible).")
        parser.add_argument("--resource", action="append", default=[], dest="resources",
                            help="Slug de recurso a vincular (repetible).")
        parser.add_argument("--preview-chars", type=int, default=400,
                            help="Cuántos caracteres del texto normalizado mostrar (def. 400).")

    def handle(self, *args, **opts):
        if not opts["file"] and not opts["text"]:
            raise CommandError('Indica el material con --file RUTA o con --text "...".')

        # 1) Obtener el texto crudo.
        if opts["file"]:
            path = opts["file"]
            if not os.path.exists(path):
                raise CommandError(f"No existe el archivo: {path}")
            with open(path, "rb") as fh:
                data = fh.read()
            raw = extract_guide_text(data, filename=os.path.basename(path))
            source = os.path.basename(path)
        else:
            raw = opts["text"]
            source = ""

        # 2) Normalizar (compacto, barato en tokens).
        text = normalize_text(raw)
        if not text:
            raise CommandError(
                "No se pudo extraer texto del material. Si es un PDF escaneado (imagen), "
                "no tiene texto seleccionable: pásalo por OCR o usa --text con el contenido."
            )

        # 3) Crear la guía.
        guide = QuizGuide.objects.create(
            title=opts["title"],
            description=opts["description"],
            source_filename=source,
            content_text=text,
        )

        # 4) Vincular por slug (avisa si algún slug no existe).
        linked = []
        for slug in opts["subjects"]:
            obj = Subject.objects.filter(slug=slug).first()
            if obj:
                guide.subjects.add(obj)
                linked.append(f"asignatura:{slug}")
            else:
                self.stdout.write(self.style.WARNING(f"  Asignatura '{slug}' no encontrada; omitida."))
        for slug in opts["topics"]:
            obj = Topic.objects.filter(slug=slug).first()
            if obj:
                guide.topics.add(obj)
                linked.append(f"tema:{slug}")
            else:
                self.stdout.write(self.style.WARNING(f"  Tema '{slug}' no encontrado; omitido."))
        for slug in opts["resources"]:
            obj = Resource.objects.filter(slug=slug).first()
            if obj:
                guide.resources.add(obj)
                linked.append(f"recurso:{slug}")
            else:
                self.stdout.write(self.style.WARNING(f"  Recurso '{slug}' no encontrado; omitido."))

        # 5) Resumen.
        self.stdout.write(self.style.SUCCESS(
            f"Guia '{guide.title}' creada (id={guide.id}, {len(text)} caracteres)."
        ))
        if linked:
            self.stdout.write("  Vinculada a: " + ", ".join(linked))
        else:
            self.stdout.write(self.style.WARNING(
                "  Sin vinculos: no aplicara a ningun recurso hasta que la vincules "
                "(--subject/--topic/--resource)."
            ))

        preview = text[: opts["preview_chars"]]
        self.stdout.write("\n--- Vista previa del texto normalizado ---")
        self.stdout.write(preview)
