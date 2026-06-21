"""Asocia un nivel educativo a una ASIGNATURA (Subject.education_level).

Los temas/recursos sin nivel propio heredan el de la asignatura
(`Resource.get_education_level`). Por defecto es dry-run: sin `--apply` solo
muestra lo que haría, sin escribir.

Ejemplos:
    python manage.py set_subject_level --subject "Física Escolar" --level media
    python manage.py set_subject_level --subject "Física Escolar" --level media --apply
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.content.models import Subject


class Command(BaseCommand):
    help = "Asigna el nivel educativo (education_level) a una asignatura."

    def add_arguments(self, parser):
        parser.add_argument(
            "--subject",
            required=True,
            help="Nombre de la asignatura (exacto; si no, coincidencia parcial única).",
        )
        parser.add_argument(
            "--level",
            required=True,
            choices=[value for value, _ in Subject.EDUCATION_LEVEL_CHOICES],
            help="Nivel educativo a asignar.",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Escribe el cambio. Sin esta bandera solo se simula (dry-run).",
        )

    def _resolve_subject(self, name):
        exact = Subject.objects.filter(name__iexact=name)
        if exact.count() == 1:
            return exact.first()
        partial = Subject.objects.filter(name__icontains=name)
        count = partial.count()
        if count == 1:
            return partial.first()
        if count == 0:
            raise CommandError(f"No existe ninguna asignatura que coincida con «{name}».")
        nombres = ", ".join(partial.values_list("name", flat=True))
        raise CommandError(
            f"«{name}» coincide con {count} asignaturas ({nombres}). "
            "Especifica el nombre exacto."
        )

    def handle(self, *args, **options):
        subject = self._resolve_subject(options["subject"])
        level = options["level"]
        apply = options["apply"]

        label = dict(Subject.EDUCATION_LEVEL_CHOICES)[level]
        current = subject.education_level or "(sin nivel)"

        self.stdout.write(
            f"Asignatura: «{subject.name}» (id {subject.id}) · "
            f"nivel actual: {current} -> objetivo: {level} ({label})"
        )

        if subject.education_level == level:
            self.stdout.write(self.style.SUCCESS("Ya estaba en ese nivel; no hay cambios."))
            return

        if not apply:
            self.stdout.write(
                self.style.WARNING("DRY-RUN: no se escribió nada. Re-ejecuta con --apply para aplicar.")
            )
            return

        with transaction.atomic():
            subject.education_level = level
            subject.save(update_fields=["education_level"])

        topics_propios = subject.topics.exclude(education_level="").count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Aplicado: «{subject.name}» -> {level}. "
                f"Los temas/recursos sin nivel propio lo heredan "
                f"({topics_propios} tema(s) conservan su nivel propio)."
            )
        )
