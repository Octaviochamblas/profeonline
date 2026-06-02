from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from apps.content.models import Area, Subject, Topic, Resource, Level

class Command(BaseCommand):
    help = "Crea y actualiza los recursos de Matemáticas con descripciones SEO ultra personalizadas para cada video."

    def add_arguments(self, parser):
        parser.add_argument(
            "--refrescar-seo",
            action="store_true",
            help="Actualiza la descripción y contenido de los recursos existentes para refrescar el SEO.",
        )

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

    custom_details = {
        "rFwyRipjDOY": {
            "intro": "Descubre qué son los números, su concepto abstracto de cantidad y cómo los seres humanos los crearon para contar y ordenar.",
            "p1": "El concepto fundamental de número y su rol indispensable como herramienta de conteo.",
            "p2": "La diferencia entre la cantidad abstracta y su representación gráfica (grafía).",
            "p3": "Ejemplos prácticos y cotidianos del uso de los números en mediciones básicas."
        },
        "yfUsZZrL7PA": {
            "intro": "Explora la estructura de los conjuntos numéricos y cómo clasificamos los números desde los más simples hasta los más complejos.",
            "p1": "La clasificación jerárquica de los conjuntos (Naturales, Enteros, Racionales e Irracionales).",
            "p2": "Las propiedades y características exclusivas de cada grupo numérico.",
            "p3": "El uso de diagramas visuales para identificar a qué conjunto pertenece cada número."
        },
        "khau52eLlCQ": {
            "intro": "Aprende a comparar números enteros positivos y negativos utilizando la recta numérica como guía visual de ordenamiento.",
            "p1": "El uso correcto de los operadores relacionales mayor que (>), menor que (<) e igual (=).",
            "p2": "La representación gráfica de los números enteros a la izquierda y derecha del cero.",
            "p3": "Por qué en los números negativos, el que tiene mayor valor absoluto es en realidad el menor."
        },
        "EkcPbQAz1I4": {
            "intro": "Domina el concepto de valor absoluto entendido como distancia y aprende a realizar comparaciones y relaciones de orden.",
            "p1": "La definición intuitiva de valor absoluto como la distancia de un número respecto al cero.",
            "p2": "El cálculo práctico del valor absoluto tanto para números positivos como negativos.",
            "p3": "Cómo resolver problemas y relaciones de orden aplicando las propiedades del valor absoluto."
        },
        "RVj8kW9QjSI": {
            "intro": "Aprende las reglas de signos fundamentales para realizar operaciones de adición y sustracción con números enteros sin cometer errores.",
            "p1": "La regla para sumar números con signos iguales y conservar el signo común.",
            "p2": "La regla para restar números con signos distintos manteniendo el signo del número mayor.",
            "p3": "Cómo evitar la confusión típica entre la regla de sumas y la regla de multiplicaciones."
        },
        "vHWVe72pVc0": {
            "intro": "Aplica las leyes de signos en la resolución de ejercicios prácticos combinados de sumas y restas de números enteros.",
            "p1": "El procedimiento paso a paso para agrupar y operar números positivos y negativos.",
            "p2": "La eliminación correcta de paréntesis cuando se presentan signos consecutivos (como -(-x)).",
            "p3": "Técnicas de cálculo mental para resolver operaciones combinadas de forma ágil."
        },
        "GGc-UZRUD90": {
            "intro": "Domina las leyes de los signos aplicadas a la multiplicación y división de números enteros mediante ejemplos sencillos.",
            "p1": "La regla general: signos iguales dan resultado positivo; signos distintos dan resultado negativo.",
            "p2": "Ejemplos prácticos multiplicando números enteros positivos y negativos.",
            "p3": "La aplicación idéntica de estas leyes para resolver cocientes y divisiones de enteros."
        },
        "j1EyI6Or4vQ": {
            "intro": "Comprende la jerarquía de las operaciones matemáticas al resolver expresiones combinadas que integran sumas, restas, productos y cocientes.",
            "p1": "El orden prioritario establecido por la regla PEMDAS (operar productos y cocientes antes de sumas y restas).",
            "p2": "La regla de evaluar de izquierda a derecha cuando las operaciones tienen el mismo nivel de prioridad.",
            "p3": "La resolución paso a paso de problemas combinados reales sin el uso de paréntesis."
        },
        "UzkH1lrlJ6w": {
            "intro": "Aprende a diferenciar los números primos de los compuestos y comprende los conceptos de múltiplos y divisores.",
            "p1": "La definición matemática de número primo (solo divisible por 1 y por sí mismo).",
            "p2": "Cómo calcular los múltiplos y divisores de cualquier número entero de forma metódica.",
            "p3": "La identificación de números compuestos y su descomposición básica."
        },
        "2Kk55AKkvyw": {
            "intro": "Domina los conceptos de Mínimo Común Múltiplo (MCM) y Máximo Común Divisor (MCD) y aprende a calcularlos.",
            "p1": "La definición y cálculo del Mínimo Común Múltiplo (MCM) para homogeneizar grupos de números.",
            "p2": "La definición y obtención del Máximo Común Divisor (MCD) para problemas de reparto.",
            "p3": "El método de descomposición simultánea en factores primos para calcular ambos valores."
        },
        "zb1m0mWyJCE": {
            "intro": "Resuelve ejercicios prácticos y problemas reales aplicando el concepto del Mínimo Común Múltiplo (MCM).",
            "p1": "La resolución paso a paso utilizando la tabla de factores primos.",
            "p2": "Cómo identificar en un enunciado que el problema requiere calcular el MCM.",
            "p3": "Estrategias para simplificar cálculos numéricos grandes durante la descomposición."
        },
        "rj4nGGjG6LI": {
            "intro": "Introduce el concepto de números racionales y aprende a clasificar fracciones propias, impropias y números mixtos.",
            "p1": "La diferencia conceptual entre fracciones propias (menores a 1) e impropias (mayores a 1).",
            "p2": "Qué es un número mixto y cómo representa una parte entera y una parte fraccionaria.",
            "p3": "El procedimiento matemático para convertir una fracción impropia a mixto y viceversa."
        },
        "q6yVrqXxksI": {
            "intro": "Aprende a transformar cualquier número decimal (finito, periódico o semiperiódico) en su correspondiente fracción.",
            "p1": "La conversión de decimales finitos dividiendo por potencias de 10.",
            "p2": "La regla de los nueves para convertir decimales periódicos puros.",
            "p3": "La conversión de decimales semiperiódicos restando el anteperíodo y combinando nueves y ceros."
        },
        "T-13XXsc6Yo": {
            "intro": "Práctica la conversión de decimales finitos e infinitos periódicos a fracción mediante la resolución de ejercicios.",
            "p1": "Ejercicios guiados para afianzar el uso de la regla de los nueves y ceros.",
            "p2": "La simplificación sistemática de la fracción resultante hasta su forma irreducible.",
            "p3": "Cómo evitar errores en la resta del numerador al transformar semiperiódicos."
        },
        "E-ODudw9TyI": {
            "intro": "Aprende el método correcto para sumar y restar números decimales alineando la coma decimal.",
            "p1": "La importancia de ordenar los números verticalmente alineando sus comas decimales.",
            "p2": "El relleno con ceros en las posiciones vacías para evitar confusiones en las restas.",
            "p3": "Cálculo con decimales positivos y negativos aplicando reglas de signos de enteros."
        },
        "Ud9_iYwVpXk": {
            "intro": "Resuelve ejercicios y problemas aplicados de adición y sustracción utilizando números decimales.",
            "p1": "Ejercicios prácticos de sumas y restas de decimales con distinto número de cifras.",
            "p2": "Resolución de problemas de la vida cotidiana que involucran dinero, medidas y decimales.",
            "p3": "Estrategias para operar decimales con signos combinados ágilmente."
        },
        "ZZLf3ENqI3Y": {
            "intro": "Aprende a multiplicar números decimales y descubre cómo posicionar correctamente la coma en el resultado final.",
            "p1": "El método de multiplicar los decimales omitiendo inicialmente la coma.",
            "p2": "Cómo contar las cifras decimales de los factores para ubicar la coma en el resultado.",
            "p3": "El truco para multiplicar decimales por potencias de 10 desplazando la coma a la derecha."
        },
        "8Bg-0hdKMF8": {
            "intro": "Resuelve ejercicios y practica la multiplicación de decimales incluyendo factores con signo negativo.",
            "p1": "Práctica con productos de números decimales de dos y tres dígitos.",
            "p2": "La aplicación de las leyes de signos en multiplicaciones decimales complejas.",
            "p3": "Consejos para estimar y verificar rápidamente la coherencia del resultado."
        },
        "g8xtA3qJ_rY": {
            "intro": "Aprende las reglas para dividir números decimales eliminando la coma decimal del divisor mediante amplificación.",
            "p1": "El paso fundamental: amplificar divisor y dividendo para obtener un divisor entero.",
            "p2": "Cómo operar la división y colocar la coma en el cociente al iniciar la parte decimal.",
            "p3": "Ejemplos prácticos de divisiones exactas e infinitas resueltas paso a paso."
        },
        "5GIVrWKXvnA": {
            "intro": "Práctica la división de decimales resolviendo diversos ejercicios con diferentes combinaciones de cifras.",
            "p1": "Resolución de divisiones donde el dividendo y el divisor tienen distinta cantidad de decimales.",
            "p2": "El paso a paso de la amplificación por 10, 100 o 1000 según corresponda.",
            "p3": "Cómo tratar restos y obtener aproximaciones decimales útiles en los resultados."
        },
        "pRoEh3n-m9A": {
            "intro": "Comprende la naturaleza de las fracciones como representación de partes de un todo y aprende a simplificarlas.",
            "p1": "La interpretación de los términos numerador (partes tomadas) y denominador (total de partes).",
            "p2": "El proceso de simplificación dividiendo ambos términos por divisores comunes.",
            "p3": "El concepto de fracción irreducible y cómo determinar cuándo se ha alcanzado."
        },
        "noyswbD3J5M": {
            "intro": "Resuelve operaciones matemáticas combinadas que integran tanto fracciones como números decimales y paréntesis.",
            "p1": "La toma de decisiones: cuándo conviene convertir todo a fracción o a decimal para facilitar el desarrollo.",
            "p2": "El respeto riguroso a la prioridad de operaciones (paréntesis, productos, sumas).",
            "p3": "Ejercicios combinados completos explicados paso a paso para evitar confusiones."
        },
        "U9FgyQbsYn0": {
            "intro": "Domina las operaciones de multiplicación y división en el conjunto de las fracciones de forma sencilla.",
            "p1": "La multiplicación lineal: multiplicar directamente numeradores con numeradores y denominadores con denominadores.",
            "p2": "La división mediante el producto por la fracción recíproca (multiplicar cruzado).",
            "p3": "La técnica esencial de simplificar factores antes de multiplicar para evitar trabajar con números grandes."
        },
        "w12XrOiqX3Q": {
            "intro": "Practica la multiplicación de fracciones aplicando técnicas avanzadas de simplificación cruzada antes de operar.",
            "p1": "Ejercicios resueltos de productos de dos y tres fracciones consecutivas.",
            "p2": "Cómo identificar y simplificar factores comunes de forma cruzada para agilizar el cálculo.",
            "p3": "Llegar a la fracción irreducible final de manera directa y sin multiplicaciones tediosas."
        },
        "McsEHWZprJM": {
            "intro": "Aprende los métodos para sumar y restar fracciones con igual y con distinto denominador utilizando el MCM.",
            "p1": "Operaciones con igual denominador sumando directamente los numeradores.",
            "p2": "Operaciones con distinto denominador obteniendo el denominador común mediante el MCM.",
            "p3": "El método cruzado (o de la mariposa) como alternativa rápida para operar dos fracciones."
        },
        "HeTkV_MZDMk": {
            "intro": "Práctica la adición y sustracción de múltiples fracciones de forma simultánea aplicando el Mínimo Común Múltiplo.",
            "p1": "Ejercicios prácticos con sumas y restas combinadas de tres o más fracciones.",
            "p2": "El cálculo del MCM de todos los denominadores y la amplificación ordenada de cada numerador.",
            "p3": "La simplificación del resultado y su conversión a números mixtos de ser necesario."
        },
        "DTLA0HU2MJw": {
            "intro": "Domina las reglas de prioridad de las operaciones en expresiones matemáticas que involucran números racionales.",
            "p1": "El orden correcto: resolver paréntesis primero, luego productos y divisiones, y finalmente sumas y restas.",
            "p2": "Resolución de ejercicios complejos con fracciones y decimales operados simultáneamente.",
            "p3": "Cómo mantener la dirección de izquierda a derecha al operar operaciones con la misma prioridad."
        }
    }

    @transaction.atomic
    def handle(self, *args, **options):
        refrescar_seo = options.get("refrescar_seo", False)
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

            # Fetch custom details
            det = self.custom_details.get(video_id, {
                "intro": f"Clase didáctica sobre {clean_title} dentro de la materia de {topic.name}.",
                "p1": "Explicación teórica y conceptual detallada.",
                "p2": "Resolución guiada de ejercicios prácticos.",
                "p3": "Consejos clave para evitar errores en pruebas matemáticas."
            })

            if is_exercise:
                seo_desc = f"Aprende a resolver ejercicios prácticos de {clean_title} paso a paso. Práctica interactiva para dominar {topic.name}."
                seo_content = f"""### 📝 Ejercicios Resueltos: {clean_title}
{det["intro"]} Ideal para reforzar el aprendizaje escolar y prepararse de forma óptima para exámenes y evaluaciones.

### 🎯 Lo que aprenderás en esta clase práctica:
- **{det["p1"]}**
- **{det["p2"]}**
- **{det["p3"]}**

### 📋 Detalles de la Clase:
* **Asignatura:** {subject.name}
* **Tema Principal:** {topic.name}
* **Nivel Recomendado:** Educación Escolar y Preparación de Exámenes.

### 🔗 Ver Recurso Completo:
* [Ver clase y resolución de ejercicios en YouTube]({url})"""
            else:
                seo_desc = f"Clase explicativa completa sobre {clean_title}. Domina los conceptos teóricos y fundamentos de {topic.name} para nivel escolar."
                seo_content = f"""### 🎥 Clase Teórica: {clean_title}
{det["intro"]} Diseñado para asegurar un entendimiento sólido antes de pasar a la resolución práctica de problemas.

### 🎯 Lo que aprenderás en este recurso:
- **{det["p1"]}**
- **{det["p2"]}**
- **{det["p3"]}**

### 📋 Detalles de la Clase:
* **Asignatura:** {subject.name}
* **Tema Principal:** {topic.name}
* **Nivel Recomendado:** Educación Escolar y Nivelación Académica.

### 🔗 Ver Recurso Completo:
* [Ver explicación de la clase en YouTube]({url})"""

            resource, created = Resource.objects.get_or_create(
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

            if created:
                resource.levels.set([level])
                created_count += 1
            else:
                if refrescar_seo:
                    resource.description = seo_desc
                    resource.content = seo_content
                    resource.save(update_fields=["description", "content"])
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Proceso completado: Se crearon {created_count} recursos y se actualizaron {updated_count} con descripciones SEO ultra personalizadas."
            )
        )
