from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
import json
import os

from apps.content.models import Area, Level, Module, ModuleResource, Resource, Subject, Topic


class Command(BaseCommand):
    help = "Crea contenido semilla para ProfeOnline con videos reales de YouTube y descripciones SEO estructuradas editorialmente."

    def add_arguments(self, parser):
        parser.add_argument(
            "--refrescar-seo",
            action="store_true",
            help="Actualiza la descripción y contenido de los recursos existentes para refrescar el SEO.",
        )

    areas = [
        {
            "name": "Matemática",
            "description": "Conceptos, ejercicios y rutas de apoyo para el razonamiento numérico y resolución de problemas.",
            "order": 1,
        },
        {
            "name": "Física",
            "description": "Material de apoyo para interpretar fenómenos físicos, fórmulas y ejercicios resueltos.",
            "order": 2,
        },
        {
            "name": "Química",
            "description": "Guías y ejercicios para comprender estructura de la materia, enlaces y termodinámica.",
            "order": 3,
        },
    ]

    levels = [
        {
            "name": "Escolar",
            "description": "Bases y material de apoyo para estudiantes de enseñanza básica.",
            "order": 1,
        },
        {
            "name": "Media/Preuniversitario",
            "description": "Contenidos clave para enseñanza media y preparación de exámenes de admisión.",
            "order": 2,
        },
        {
            "name": "Universitario",
            "description": "Apoyo académico y materias avanzadas para educación superior.",
            "order": 3,
        },
    ]

    subjects = [
        # Matemática
        {
            "name": "Matemática Escolar",
            "area": "Matemática",
            "description": "Bases y operaciones fundamentales de matemáticas para nivel escolar básico.",
            "topics": [
                {
                    "name": "Números y operaciones básicas",
                    "description": "Conceptos iniciales, fracciones, decimales y operaciones fundamentales.",
                },
                {
                    "name": "Proporcionalidad directa e inversa",
                    "description": "Conceptos y ejercicios prácticos de proporcionalidad.",
                },
            ],
        },
        {
            "name": "Matemática Media",
            "area": "Matemática",
            "description": "Contenidos de matemáticas para enseñanza media y preparación para el ingreso universitario.",
            "topics": [
                {
                    "name": "Lenguaje y expresiones algebraicas",
                    "description": "Polinomios, factorización y operaciones algebraicas.",
                },
                {
                    "name": "Preparación PAES",
                    "description": "Repaso de contenidos y resolución de ejercicios tipo PAES.",
                },
            ],
        },
        {
            "name": "Cálculo I",
            "area": "Matemática",
            "description": "Cálculo diferencial universitario.",
            "topics": [
                {
                    "name": "Límites y Continuidad",
                    "description": "Cálculo de límites algebraicos y análisis de continuidad.",
                },
                {
                    "name": "Derivadas y Optimización",
                    "description": "Reglas de derivación, rectas tangentes y problemas de optimización.",
                },
            ],
        },
        {
            "name": "Cálculo II",
            "area": "Matemática",
            "description": "Cálculo integral universitario.",
            "topics": [
                {
                    "name": "Integrales y técnicas de integración",
                    "description": "Integrales definidas, indefinidas, sustitución e integración por partes.",
                },
            ],
        },
        {
            "name": "Cálculo III",
            "area": "Matemática",
            "description": "Cálculo multivariable y funciones vectoriales.",
            "topics": [
                {
                    "name": "Funciones de varias variables y optimización",
                    "description": "Derivadas parciales, gradiente y multiplicadores de Lagrange.",
                },
                {
                    "name": "Integrales Múltiples",
                    "description": "Integrales dobles e iteradas, cálculo de áreas y volúmenes.",
                },
            ],
        },
        {
            "name": "Álgebra",
            "area": "Matemática",
            "description": "Álgebra universitaria y lógica matemática.",
            "topics": [
                {
                    "name": "Lógica matemática y proposicional",
                    "description": "Tablas de verdad, conectivos lógicos y razonamiento proposicional.",
                },
                {
                    "name": "Fundamentos de álgebra universitaria",
                    "description": "Ecuaciones, polinomios complejos y estructuras básicas.",
                },
            ],
        },
        {
            "name": "Álgebra Lineal",
            "area": "Matemática",
            "description": "Matrices, determinantes y espacios vectoriales.",
            "topics": [
                {
                    "name": "Matrices, vectores y sistemas lineales",
                    "description": "Operaciones con matrices, cálculo de determinantes y sistemas lineales.",
                },
            ],
        },
        {
            "name": "EDO",
            "area": "Matemática",
            "description": "Ecuaciones Diferenciales Ordinarias.",
            "topics": [
                {
                    "name": "Ecuaciones Diferenciales Ordinarias",
                    "description": "Métodos de resolución de EDOs de primer y segundo orden.",
                },
            ],
        },
        {
            "name": "Estadística",
            "area": "Matemática",
            "description": "Teoría de probabilidades y estadística descriptiva.",
            "topics": [
                {
                    "name": "Probabilidad y Estadística descriptiva",
                    "description": "Cálculo de probabilidades, variables aleatorias y gráficos estadísticos.",
                },
            ],
        },
        # Física
        {
            "name": "Física Escolar",
            "area": "Física",
            "description": "Conceptos introductorios y física básica para nivel escolar.",
            "topics": [
                {
                    "name": "Introducción a la física escolar",
                    "description": "Unidades de medida, vectores y conceptos básicos.",
                },
            ],
        },
        {
            "name": "Física I",
            "area": "Física",
            "description": "Física mecánica universitaria - Cinemática.",
            "topics": [
                {
                    "name": "Cinemática y análisis del movimiento",
                    "description": "Movimiento rectilíneo, aceleración y gráficos de movimiento.",
                },
            ],
        },
        {
            "name": "Física II",
            "area": "Física",
            "description": "Física de fluidos y ondas.",
            "topics": [
                {
                    "name": "Mecánica de Fluidos y continuidad",
                    "description": "Principio de Bernoulli, hidrostática y dinámica de fluidos.",
                },
            ],
        },
        {
            "name": "Electromagnetismo",
            "area": "Física",
            "description": "Teoría electromagnética, campos y potencial.",
            "topics": [
                {
                    "name": "Campo eléctrico y potencial",
                    "description": "Ley de Coulomb, campo eléctrico y potencial eléctrico.",
                },
            ],
        },
        {
            "name": "Mecánica",
            "area": "Física",
            "description": "Dinámica clásica de sistemas de partículas.",
            "topics": [
                {
                    "name": "Dinámica de partículas y energía",
                    "description": "Leyes de Newton, trabajo, energía y colisiones.",
                },
            ],
        },
        {
            "name": "Estática",
            "area": "Física",
            "description": "Estudio del equilibrio de cuerpos rígidos.",
            "topics": [
                {
                    "name": "Equilibrio de cuerpos rígidos y fuerzas",
                    "description": "Torque, centro de gravedad y condiciones de equilibrio.",
                },
            ],
        },
        # Química
        {
            "name": "Química Universitaria",
            "area": "Química",
            "description": "Fundamentos y conceptos introductorios de química.",
            "topics": [
                {
                    "name": "Estructura de la materia y enlaces",
                    "description": "Modelos atómicos, tabla periódica y enlaces químicos.",
                },
            ],
        },
        {
            "name": "Termodinámica",
            "area": "Química",
            "description": "Principios termodinámicos, estados y ciclos.",
            "topics": [
                {
                    "name": "Ciclos, líquidos y vapores",
                    "description": "Leyes de la termodinámica, trabajo térmico y ciclos.",
                },
            ],
        },
        {
            "name": "Química I",
            "area": "Química",
            "description": "Química general I universitaria.",
            "topics": [
                {
                    "name": "Estequiometría y soluciones",
                    "description": "Cálculos estequiométricos, reacciones y disoluciones químicas.",
                },
            ],
        },
        {
            "name": "Química II",
            "area": "Química",
            "description": "Química física y termoquímica universitaria.",
            "topics": [
                {
                    "name": "Físico-Química, entalpía y equilibrio",
                    "description": "Entalpía, entropía, energía libre de Gibbs y constante de equilibrio.",
                },
            ],
        },
        {
            "name": "Química Analítica",
            "area": "Química",
            "description": "Métodos químicos de análisis cuantitativo.",
            "topics": [
                {
                    "name": "Métodos de análisis y equilibrio químico",
                    "description": "Equilibrio ácido-base, volumetría y gravimetría.",
                },
            ],
        },
    ]

    modules = [
        {
            "title": "Ruta de fracciones y decimales",
            "subject": "Matemática Escolar",
            "topic": "Números y operaciones básicas",
            "levels": ["Escolar", "Media/Preuniversitario"],
            "objective": "Fortalecer el cálculo básico y la equivalencia entre fracciones y decimales.",
            "description": "Ruta de apoyo con recursos graduales para reforzar cálculo y práctica.",
            "order": 1,
            "resource": "Guía de fracciones y decimales",
        },
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        refrescar_seo = options.get("refrescar_seo", False)
        area_by_name = {}
        for item in self.areas:
            area, _ = Area.objects.get_or_create(
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
            level, _ = Level.objects.get_or_create(
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
            subject, _ = Subject.objects.get_or_create(
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
                topic, _ = Topic.objects.get_or_create(
                    subject=subject,
                    name=topic_item["name"],
                    defaults={
                        "description": topic_item["description"],
                        "is_active": True,
                    },
                )
                topic_by_subject[subject.name][topic.name] = topic

        # Load resources from JSON file to prevent python escape string character corruption
        current_dir = os.path.dirname(__file__)
        json_path = os.path.join(current_dir, "seed_resources.json")
        with open(json_path, "r", encoding="utf-8") as f:
            resources = json.load(f)

        resource_by_title = {}
        for item in resources:
            resource_slug = slugify(item["title"])
            resource, created = Resource.objects.get_or_create(
                slug=resource_slug,
                defaults={
                    "title": item["title"],
                    "subject": subject_by_name[item["subject"]],
                    "topic": topic_by_subject[item["subject"]][item["topic"]],
                    "description": item["description"],
                    "content": item["content"],
                    "video_url": item.get("video_url"),
                    "is_published": True,
                },
            )
            if created:
                resource.levels.set([level_by_name[name] for name in item["levels"]])
            else:
                if refrescar_seo:
                    resource.description = item["description"]
                    resource.content = item["content"]
                    resource.save(update_fields=["description", "content"])
            resource_by_title[resource.title] = resource

        for item in self.modules:
            module_slug = slugify(item["title"])
            # Ensure referenced resource exists before creating module
            ref_resource = resource_by_title.get(item["resource"])
            if not ref_resource:
                fallback_resources = Resource.objects.filter(topic=topic_by_subject[item["subject"]][item["topic"]])
                if fallback_resources.exists():
                    ref_resource = fallback_resources.first()
                else:
                    continue

            module, created = Module.objects.get_or_create(
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
            if created:
                module.levels.set([level_by_name[name] for name in item["levels"]])

            ModuleResource.objects.get_or_create(
                module=module,
                resource=ref_resource,
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
                f"{len(self.levels)} niveles, {len(resources)} recursos y {len(self.modules)} modulos."
            )
        )
