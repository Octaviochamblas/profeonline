from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from apps.content.models import Area, Subject, Topic, Resource, Level

class Command(BaseCommand):
    help = "Crea y actualiza los recursos de Matemáticas con descripciones SEO optimizadas mediante IA y asegura la existencia de sus modelos asociados."

    videos = [
        {"id": "rFwyRipjDOY", "title": "1.1 Qué son los Números"},
        {"id": "yfUsZZrL7PA", "title": "1.2 Conjuntos Numéricos"},
        {"id": "khau52eLlCQ", "title": "1.3 Números Enteros: Relaciones de Orden - Mayor, menor e igual"},
        {"id": "EkcPbQAz1I4", "title": "1.4 Valor Absoluto - Relaciones de orden"},
        {"id": "RVj8kW9QjSI", "title": "1.5 Regla de Signos para Sumas/Restas"},
        {"id": "vHWVe72pVc0", "title": "1.5a Ejercicios de Sumas y Restas - Aplicación de Regla de los Signos"},
        {"id": "GGc-UZRUD90", "title": "1.6 Regla de los signos en Multiplicación/División - Ejemplos"},
        {"id": "j1EyI6Or4vQ", "title": "1.7 Prioridad de Operaciones - Suma/Resta/Multiplicación/División Combinadas"},
        {"id": "UzkH1lrlJ6w", "title": "1.8 Números Primos - Múltiplos y divisores"},
        {"id": "2Kk55AKkvyw", "title": "1.9 Mínimo Común Múltiplo - Máximo Común Divisor"},
        {"id": "zb1m0mWyJCE", "title": "1.9a Ejercicios: Mínimo Común Múltiplo"},
        {"id": "rj4nGGjG6LI", "title": "2.0 Números Racionales, fraciones propias, impropias y  números mixtos"},
        {"id": "q6yVrqXxksI", "title": "2.01 Números Racionales - Conversión de decimales finitos, periodicos y semi-periodicos a Fracción"},
        {"id": "T-13XXsc6Yo", "title": "2.01a EJERCICIOS: Conversión de decimales finitos, periodicos y semi-periodicos a Fracción"},
        {"id": "E-ODudw9TyI", "title": "2.02 Números Racionales - Sumas y Restas de números decimales"},
        {"id": "Ud9_iYwVpXk", "title": "2.02A EJERCICIOS:  Números Racionales - Sumas y Restas de números decimales"},
        {"id": "ZZLf3ENqI3Y", "title": "2.03 Números Racionales: Multiplicacion de números decimales"},
        {"id": "8Bg-0hdKMF8", "title": "2.03a EJERCICIOS: Nodos Racionales: Multiplicación de Decimales"},
        {"id": "g8xtA3qJ_rY", "title": "2.04 Nodos Racionales: División de números Decimales"},
        {"id": "5GIVrWKXvnA", "title": "2.04a EJERCICIOS: Números Racionales - División de decimales"},
        {"id": "pRoEh3n-m9A", "title": "2.05 Números Racionales: Qué son las fracciones - Simplificación Fracciones"},
        {"id": "noyswbD3J5M", "title": "2.05A EJERCICIOS: Números Racionales - Operaciones Combinadas - ProfeOnline.cl"},
        {"id": "U9FgyQbsYn0", "title": "2.06 Números Racionales: Multiplicación y División de Fracciones"},
        {"id": "w12XrOiqX3Q", "title": "2.06a EJERCICIOS: Números Racionales: Multiplicación con simplificación - ProfeOnline.cl"},
        {"id": "McsEHWZprJM", "title": "2 07 Números Racionales Suma y Resta de Fracciones"},
        {"id": "HeTkV_MZDMk", "title": "2 07a EJERCICIOS: Suma y Resta de FRACCIONES | @ProfeOnline.cl"},
        {"id": "DTLA0HU2MJw", "title": "2.08 Números Racionales: Prioridad en las Operaciones"}
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        # 1. Ensure Area exists (Matemáticas)
        area, _ = Area.objects.get_or_create(
            name="Matemáticas",
            defaults={"description": "Conceptos, ejercicios y rutas de apoyo para el razonamiento numérico y resolución de problemas.", "is_active": True, "order": 1}
        )

        # 2. Rename 'Matemáticas Escolar' if it exists to 'Matemática Escolar' for consistency and user requests
        old_subject = Subject.objects.filter(name="Matemáticas Escolar").first()
        new_subject_exists = Subject.objects.filter(name="Matemática Escolar").exists()

        if old_subject:
            if new_subject_exists:
                new_subject = Subject.objects.get(name="Matemática Escolar")
                Topic.objects.filter(subject=old_subject).update(subject=new_subject)
                Resource.objects.filter(subject=old_subject).update(subject=new_subject)
                old_subject.delete()
                self.stdout.write(self.style.WARNING("Fusionada la asignatura 'Matemáticas Escolar' en 'Matemática Escolar'"))
            else:
                old_subject.name = "Matemática Escolar"
                old_subject.save()
                self.stdout.write(self.style.WARNING("Renombrada la asignatura 'Matemáticas Escolar' a 'Matemática Escolar'"))

        # Get or create Subject (Matemática Escolar)
        subject, _ = Subject.objects.get_or_create(
            name="Matemática Escolar",
            defaults={"area": area, "description": "Bases y operaciones fundamentales de matemáticas para nivel escolar básico.", "is_active": True}
        )

        # 3. Ensure Topics exist
        topic_enteros, _ = Topic.objects.get_or_create(
            name="Números Enteros",
            subject=subject,
            defaults={"description": "Clasificación, reglas de signos y operaciones básicas con números enteros.", "is_active": True, "resource_ordering_method": "manual"}
        )

        topic_racionales, _ = Topic.objects.get_or_create(
            name="Números Racionales",
            subject=subject,
            defaults={"description": "Concepto de fracciones, números decimales, conversión y operaciones combinadas.", "is_active": True, "resource_ordering_method": "manual"}
        )

        # Ensure level 'Escolar' exists
        level, _ = Level.objects.get_or_create(
            name="Escolar",
            defaults={"description": "Bases y material de apoyo para estudiantes de enseñanza básica.", "is_active": True, "order": 1}
        )

        created_count = 0
        updated_count = 0

        # 4. Populate resources
        for idx, video in enumerate(self.videos):
            video_id = video["id"]
            title = video["title"]

            # Select correct topic
            if title.startswith("1"):
                topic = topic_enteros
            elif title.startswith("2"):
                topic = topic_racionales
            else:
                continue

            url = f"https://www.youtube.com/watch?v={video_id}"
            slug = slugify(title)

            # Generate powerful SEO Description and Content
            is_exercise = "EJERCICIOS" in title.upper() or "EJERCICIO" in title.upper() or title.endswith("a") or title.endswith("A")

            clean_title = title.replace("ProfeOnline.cl", "").replace("@ProfeOnline.cl", "").strip()

            if is_exercise:
                seo_desc = f"Aprende a resolver ejercicios prácticos de {clean_title} paso a paso con esta videoclase interactiva. Domina el tema de {topic.name}."
                seo_content = f"""### 📝 Ejercicios Resueltos: {clean_title}
Aprende a aplicar las reglas matemáticas correctas con esta guía práctica enfocada en la resolución de ejercicios del tema **{topic.name}**. Ideal para reforzar el aprendizaje escolar y prepararse para exámenes.

### 🎯 Lo que aprenderás en esta clase práctica:
- **Análisis del problema:** Cómo estructurar y resolver cada ejercicio paso a paso de forma lógica.
- **Aplicación de reglas:** Uso de fórmulas, signos y simplificaciones necesarias para llegar a la respuesta correcta.
- **Consejos clave:** Cómo evitar los errores comunes que suelen cometer los estudiantes en evaluaciones.

### 🚀 Optimización SEO y Académica:
* **Asignatura:** {subject.name}
* **Tema Principal:** {topic.name}
* **Nivel Recomendado:** Educación Escolar y Preparación de Exámenes.
* **Palabras Clave:** resolución de ejercicios, {topic.name.lower()}, práctica de matemáticas, apoyo escolar.

### 🔗 Ver Recurso Completo:
* [Ver clase y resolución de ejercicios en YouTube]({url})"""
            else:
                seo_desc = f"Clase explicativa completa sobre {clean_title}. Domina los conceptos teóricos y fundamentos de {topic.name} para nivel escolar."
                seo_content = f"""### 🎥 Clase Teórica: {clean_title}
Explicación detallada y paso a paso para comprender los fundamentos teóricos del tema **{clean_title}** en la asignatura de **{subject.name}**. Diseñado para asegurar un entendimiento sólido antes de pasar a la práctica.

### 🎯 Lo que aprenderás en este recurso:
- **Bases Conceptuales:** Definición clara, intuitiva y rigurosa del concepto sin tecnicismos innecesarios.
- **Fundamentación:** Fórmulas principales, propiedades y reglas que rigen este contenido.
- **Conexión Temática:** Cómo se relaciona este tema con contenidos previos y futuros en tu plan de estudio.

### 🚀 Optimización SEO y Académica:
* **Asignatura:** {subject.name}
* **Tema Principal:** {topic.name}
* **Nivel Recomendado:** Educación Escolar y Nivelación Académica.
* **Palabras Clave:** clase teórica, {topic.name.lower()}, aprender matemáticas, conceptos de matemáticas.

### 🔗 Ver Recurso Completo:
* [Ver explicación de la clase en YouTube]({url})"""

            resource, created = Resource.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "subject": subject,
                    "topic": topic,
                    "video_url": url,
                    "description": seo_desc,
                    "content": seo_content,
                    "is_published": True,
                    "order": idx + 1
                }
            )
            resource.levels.set([level])

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Proceso completado: Se crearon {created_count} recursos y se actualizaron {updated_count} con descripciones SEO optimizadas."
            )
        )
