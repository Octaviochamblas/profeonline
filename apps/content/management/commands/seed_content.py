from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from apps.content.models import Area, Level, Module, ModuleResource, Resource, Subject, Topic


class Command(BaseCommand):
    help = "Crea contenido semilla para ProfeOnline."

    areas = [
        {
            "name": "Matemáticas",
            "description": "Conceptos, ejercicios y rutas de apoyo para el razonamiento numérico.",
            "order": 1,
        },
        {
            "name": "Ciencias",
            "description": "Material de apoyo para física y química con foco en comprensión y práctica.",
            "order": 2,
        },
    ]

    levels = [
        {
            "name": "Primaria",
            "description": "Bases de lectura, cálculo y hábitos de estudio para estudiantes de primaria.",
            "order": 1,
        },
        {
            "name": "Secundaria",
            "description": "Contenidos y ejercicios para fortalecer el avance en secundaria.",
            "order": 2,
        },
        {
            "name": "Preuniversitario",
            "description": "Apoyo para preparar evaluaciones de ingreso y reforzar contenidos clave.",
            "order": 3,
        },
    ]

    subjects = [
        {
            "name": "Matemática",
            "area": "Matemáticas",
            "description": "Clases particulares y recursos para operaciones, álgebra y resolución de problemas.",
            "topics": [
                {
                    "name": "Fracciones y decimales",
                    "description": "Repaso de equivalencias, operaciones y problemas aplicados.",
                },
                {
                    "name": "Ecuaciones lineales",
                    "description": "Procedimientos paso a paso para resolver ecuaciones de primer grado.",
                },
            ],
        },
        {
            "name": "Física",
            "area": "Ciencias",
            "description": "Material de apoyo para interpretar fenómenos, fórmulas y ejercicios de física.",
            "topics": [
                {
                    "name": "Movimiento rectilíneo",
                    "description": "Velocidad, desplazamiento y lectura de gráficos básicos.",
                },
                {
                    "name": "Fuerza y energía",
                    "description": "Conceptos introductorios para comprender interacción, trabajo y energía.",
                },
            ],
        },
        {
            "name": "Química",
            "area": "Ciencias",
            "description": "Guías y ejercicios para comprender estructura de la materia y enlaces.",
            "topics": [
                {
                    "name": "Tabla periódica",
                    "description": "Organización de elementos y lectura de tendencias periódicas.",
                },
                {
                    "name": "Enlaces químicos",
                    "description": "Unión entre átomos, tipos de enlace y ejemplos de aplicación.",
                },
            ],
        },
    ]

    resources = [
        {
            "title": "Guía de fracciones y decimales",
            "subject": "Matemática",
            "topic": "Fracciones y decimales",
            "levels": ["Primaria", "Secundaria"],
            "description": "Repaso guiado para convertir, comparar y operar con fracciones y decimales.",
            "content": (
                "Este recurso resume procedimientos básicos para trabajar con fracciones y decimales.\n\n"
                "Incluye ejemplos de suma, resta y conversión para reforzar el aprendizaje con práctica breve."
            ),
        },
        {
            "title": "Ejercicios de ecuaciones lineales",
            "subject": "Matemática",
            "topic": "Ecuaciones lineales",
            "levels": ["Secundaria", "Preuniversitario"],
            "description": "Serie de ejercicios para practicar despeje y resolución paso a paso.",
            "content": (
                "Material de práctica centrado en ecuaciones de primer grado.\n\n"
                "El objetivo es ordenar el procedimiento y reconocer errores comunes al despejar incógnitas."
            ),
        },
        {
            "title": "Resumen de movimiento rectilíneo",
            "subject": "Física",
            "topic": "Movimiento rectilíneo",
            "levels": ["Secundaria"],
            "description": "Resumen visual para interpretar velocidad, posición y desplazamiento.",
            "content": (
                "Este resumen explica los conceptos esenciales del movimiento rectilíneo.\n\n"
                "Sirve para repasar definiciones, fórmulas y lectura de gráficos antes de una evaluación."
            ),
        },
        {
            "title": "Tabla periódica y enlaces químicos",
            "subject": "Química",
            "topic": "Tabla periódica",
            "levels": ["Secundaria", "Preuniversitario"],
            "description": "Guía de apoyo para reconocer elementos, grupos y enlaces básicos.",
            "content": (
                "La guía ordena los conceptos clave de química general.\n\n"
                "Presenta la estructura de la tabla periódica y la relación con los enlaces químicos más comunes."
            ),
        },
    ]

    modules = [
        {
            "title": "Ruta de fracciones y decimales",
            "subject": "Matemática",
            "topic": "Fracciones y decimales",
            "levels": ["Primaria", "Secundaria"],
            "objective": "Fortalecer el cálculo básico y la equivalencia entre fracciones y decimales.",
            "description": "Ruta de apoyo con recursos graduales para reforzar cálculo y práctica.",
            "order": 1,
            "resource": "Guía de fracciones y decimales",
        },
        {
            "title": "Ruta de ecuaciones",
            "subject": "Matemática",
            "topic": "Ecuaciones lineales",
            "levels": ["Secundaria", "Preuniversitario"],
            "objective": "Practicar despeje de incógnitas y resolución ordenada de ecuaciones.",
            "description": "Secuencia de estudio para ganar soltura con ecuaciones lineales.",
            "order": 2,
            "resource": "Ejercicios de ecuaciones lineales",
        },
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        area_by_name = {}
        for item in self.areas:
            area, _ = Area.objects.update_or_create(
                name=item["name"],
                defaults={
                    "description": item["description"],
                    "is_active": True,
                    "order": item["order"],
                },
            )
            area_by_name[area.name] = area

        level_by_name = {}
        for item in self.levels:
            level, _ = Level.objects.update_or_create(
                name=item["name"],
                defaults={
                    "description": item["description"],
                    "is_active": True,
                    "order": item["order"],
                },
            )
            level_by_name[level.name] = level

        subject_by_name = {}
        topic_by_subject = {}
        for item in self.subjects:
            subject, _ = Subject.objects.update_or_create(
                name=item["name"],
                defaults={
                    "area": area_by_name[item["area"]],
                    "description": item["description"],
                    "is_active": True,
                },
            )
            subject_by_name[subject.name] = subject
            topic_by_subject[subject.name] = {}

            for topic_item in item["topics"]:
                topic, _ = Topic.objects.update_or_create(
                    subject=subject,
                    name=topic_item["name"],
                    defaults={
                        "description": topic_item["description"],
                        "is_active": True,
                    },
                )
                topic_by_subject[subject.name][topic.name] = topic

        resource_by_title = {}
        for item in self.resources:
            resource_slug = slugify(item["title"])
            resource, _ = Resource.objects.update_or_create(
                slug=resource_slug,
                defaults={
                    "title": item["title"],
                    "subject": subject_by_name[item["subject"]],
                    "topic": topic_by_subject[item["subject"]][item["topic"]],
                    "description": item["description"],
                    "content": item["content"],
                    "is_published": True,
                },
            )
            resource.levels.set([level_by_name[name] for name in item["levels"]])
            resource_by_title[resource.title] = resource

        for item in self.modules:
            module_slug = slugify(item["title"])
            module, _ = Module.objects.update_or_create(
                slug=module_slug,
                defaults={
                    "title": item["title"],
                    "subject": subject_by_name[item["subject"]],
                    "topic": topic_by_subject[item["subject"]][item["topic"]],
                    "objective": item["objective"],
                    "description": item["description"],
                    "order": item["order"],
                    "is_published": True,
                },
            )
            module.levels.set([level_by_name[name] for name in item["levels"]])
            ModuleResource.objects.update_or_create(
                module=module,
                resource=resource_by_title[item["resource"]],
                defaults={
                    "order": 1,
                    "is_required": True,
                    "note": "Recurso base para esta ruta de aprendizaje.",
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Contenido semilla listo: "
                f"{len(self.areas)} areas, {len(self.subjects)} asignaturas, "
                f"{len(self.levels)} niveles, {len(self.resources)} recursos y {len(self.modules)} modulos."
            )
        )
