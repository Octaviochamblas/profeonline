from __future__ import annotations

import os
import sys
from pathlib import Path

import django


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from apps.content.models import KnowledgeNode  # noqa: E402
from scratch import finalize_mat_num_b0203 as base  # noqa: E402


SPECS: dict[str, dict] = {}


def add(
    sid: str,
    label: str,
    definition: str,
    example: str,
    fact: str,
    hook: str,
    goal: str,
    steps: list[str],
    confusion: str,
) -> None:
    SPECS[sid] = {
        "label": label,
        "definition": definition,
        "example": example,
        "fact": fact,
        "hook": hook,
        "goal": goal,
        "steps": steps,
        "confusion": confusion,
    }


def add_classification(
    sid: str,
    label: str,
    definition: str,
    example: str,
    fact: str,
    hook: str,
    confusion: str,
) -> None:
    add(
        sid,
        label,
        definition,
        example,
        fact,
        hook,
        "clasificar un ángulo a partir de su medida.",
        [
            "Lee o estima la abertura del ángulo en grados.",
            "Compara la medida con los valores de referencia 0°, 90°, 180° y 360°.",
            "Asigna el nombre correcto y revisa que no contradiga el dibujo.",
        ],
        confusion,
    )


def add_transversal_identification(
    sid: str,
    label: str,
    relation_name: str,
    example: str,
    fact: str,
    confusion: str,
) -> None:
    add(
        sid,
        label,
        f"los ángulos {relation_name} se reconocen por su posición relativa respecto de dos paralelas y una transversal",
        example,
        fact,
        f"Cuando una calle cruza dos avenidas paralelas aparecen muchos ángulos con nombres distintos. El truco no es memorizar números, sino mirar dónde queda cada uno respecto de la transversal y de las paralelas.",
        f"identificar un par de ángulos {relation_name} en un esquema con paralelas.",
        [
            "Ubica primero cuáles son las rectas paralelas y cuál es la transversal.",
            "Decide si cada ángulo está en la zona interior o exterior y en qué lado de la transversal queda.",
            f"Concluye si el par corresponde a ángulos {relation_name} y descarta relaciones vecinas.",
        ],
        confusion,
    )


def add_transversal_property(
    sid: str,
    label: str,
    relation_name: str,
    property_text: str,
    example: str,
    confusion: str,
) -> None:
    add(
        sid,
        label,
        f"si dos rectas paralelas son cortadas por una transversal, los ángulos {relation_name} {property_text}",
        example,
        f"la propiedad solo puede aplicarse después de verificar que el par elegido realmente es {relation_name}",
        f"En geometría muchas igualdades parecen obvias porque el dibujo 'se ve bien'. Con paralelas y transversal conviene ir más lento: primero se nombra bien el par y recién después se transfiere la medida.",
        f"usar la propiedad de los ángulos {relation_name} para justificar una medida.",
        [
            f"Reconoce un par de ángulos {relation_name} en el esquema.",
            "Usa la propiedad correspondiente para relacionar la medida conocida con la incógnita.",
            "Comprueba que el resultado respete la posición del par y la condición de paralelismo.",
        ],
        confusion,
    )


def add_measure_conversion(
    sid: str,
    label: str,
    definition: str,
    example: str,
    fact: str,
    hook: str,
    confusion: str,
) -> None:
    add(
        sid,
        label,
        definition,
        example,
        fact,
        hook,
        "convertir medidas angulares usando la equivalencia adecuada.",
        [
            "Identifica en qué unidad está dada la medida y a qué unidad debe pasar.",
            "Escribe la equivalencia base del sistema involucrado antes de calcular.",
            "Resuelve la proporción o la operación y verifica que el resultado tenga la unidad pedida.",
        ],
        confusion,
    )


def yaml_filename(semantic_id: str) -> str:
    _, _, subtheme, concept = semantic_id.split(".", 3)
    return f"mat-geo-{subtheme.lower().replace('_', '-')}-{concept.lower().replace('_', '-')}.yaml"


def source_for(subtheme: str) -> str:
    if subtheme in {
        "ANGULOS_FUNDAMENTOS",
        "ANGULOS_CLASIFICACION",
        "ANGULOS_RELACIONES_METRICAS",
        "ANGULOS_RELACIONES_POSICION",
        "ANGULOS_RECTAS_TRANSVERSALES",
    }:
        return "Currículum Nacional MINEDUC — Geometría plana, ángulos, relaciones y paralelismo."
    if subtheme == "MEDICION_ANGULAR":
        return "Currículum Nacional MINEDUC — Medición angular, sistemas sexagesimal, radial y centesimal."
    return "Currículum Nacional MINEDUC — Aplicaciones de ángulos y lectura geométrica de situaciones cotidianas."


def errors_for(label: str, confusion: str, fact: str, steps: list[str]) -> list[str]:
    step1, step2, step3 = steps
    return [
        f"{label} significa {confusion}.",
        f"Para resolver {label.lower()}, basta con el paso “{step1}” y no hace falta revisar “{step2}”.",
        f"Si el dibujo parece claro, se puede ignorar que {fact}.",
        f"Dos configuraciones distintas representan {label.lower()} solo porque contienen la palabra 'ángulo'.",
        f"Se puede cerrar el ejercicio sin aplicar el control final “{step3}”.",
    ]


def build_examples(semantic_id: str, title: str, spec: dict) -> list[dict]:
    definition = base._without_trailing_period(spec["definition"])
    example = base._without_example_prefix(spec["example"])
    fact = base._without_trailing_period(spec["fact"])
    step1, step2, step3 = spec["steps"]
    label = spec["label"]

    open_title = base._variant(
        semantic_id,
        "geo-open-title",
        [
            f"Lectura del dibujo — {label}",
            f"Caso guiado — {label}",
            f"Situación geométrica — {label}",
            f"Aplicación directa — {label}",
        ],
    )
    review_title = base._variant(
        semantic_id,
        "geo-review-title",
        [
            f"Corrección de una respuesta — {label}",
            f"Chequeo del procedimiento — {label}",
            f"Revisión del razonamiento — {label}",
            f"Verificación de la solución — {label}",
        ],
    )
    yes_title = base._variant(
        semantic_id,
        "geo-yes-title",
        [
            f"¿El caso confirma que {fact.lower()}? — {label}",
            f"¿La interpretación del dibujo es válida? — {label}",
            f"¿Puede concluirse correctamente este hecho? — {label}",
            f"¿La situación respeta la idea clave del recurso? — {label}",
        ],
    )
    no_title = base._variant(
        semantic_id,
        "geo-no-title",
        [
            f"¿Basta con {step1[:-1].lower()}? — {label}",
            f"¿Se puede omitir el paso intermedio? — {label}",
            f"¿Alcanza con una lectura rápida del esquema? — {label}",
            f"¿Se puede cerrar sin el control final? — {label}",
        ],
    )

    review_prompt = base._variant(
        semantic_id,
        "geo-review-prompt",
        [
            f"Un estudiante usa la idea “{fact}” al analizar este caso: {example}. Explica qué debe revisar primero y cómo se justifica la conclusión.",
            f"En la situación “{example}”, un compañero llega a la respuesta correcta pero no explica el paso decisivo. Reconstruye la justificación completa.",
            f"Al resolver “{example}”, una alumna salta desde el dibujo a la conclusión. Indica qué control geométrico faltó y cómo cerrar la solución.",
            f"Revisa una solución del caso “{example}”: el resultado parece razonable, pero falta conectar el dibujo con la definición. Explica esa conexión.",
        ],
    )

    return [
        {
            "titulo": open_title,
            "enunciado": base._upper_initial(example).rstrip(".") + ".",
            "solucion_pasos": spec["steps"],
        },
        {
            "titulo": review_title,
            "enunciado": review_prompt,
            "solucion_pasos": [
                f"Parte de la definición: {definition}.",
                step2,
                step3,
            ],
        },
        {
            "titulo": yes_title,
            "respuesta": "Sí",
            "solucion_pasos": [
                f"Sí. La situación encaja con la definición del recurso: {definition}.",
                f"En el caso “{example}” se observa que {fact.lower()}.",
                step3,
            ],
        },
        {
            "titulo": no_title,
            "respuesta": "No",
            "solucion_pasos": [
                f"No. Un inicio útil no reemplaza la justificación completa de {title.lower()}.",
                f"Después del paso “{step1}” todavía hace falta revisar “{step2}”.",
                f"El cierre correcto exige “{step3}”.",
            ],
        },
    ]


def build_content(semantic_id: str, node_name: str) -> dict:
    spec = SPECS[semantic_id]
    definition = base._without_trailing_period(spec["definition"])
    example = base._without_example_prefix(spec["example"])
    fact = base._without_trailing_period(spec["fact"])
    step1, step2, step3 = spec["steps"]
    lower_title = node_name[:1].lower() + node_name[1:]

    intro = base._variant(
        semantic_id,
        "geo-intro",
        [
            spec["hook"],
            f"{spec['hook']} Este recurso se centra en {lower_title} y en cómo reconocerlo con un criterio geométrico claro.",
            f"{spec['hook']} Para resolver situaciones de {lower_title} conviene mirar el dibujo con método, no solo por intuición.",
            f"{spec['hook']} Aquí lo trabajaremos con ejemplos concretos y verificaciones cortas.",
        ],
    )

    explanation = base._variant(
        semantic_id,
        "geo-explanation",
        [
            f"{base._upper_initial(definition)}.\n\nEn el caso “{example}” esta idea se vuelve visible y permite comprobar que {fact.lower()}.",
            f"{base._upper_initial(definition)}.\n\nLa situación “{example}” muestra cómo pasar del dibujo a una conclusión válida: primero se identifica la relación correcta y luego se verifica que {fact.lower()}.",
            f"{base._upper_initial(definition)}.\n\nCuando se analiza “{example}” conviene evitar la memoria mecánica. El control decisivo es comprobar que {fact.lower()}.",
            f"{base._upper_initial(definition)}.\n\nEl ejemplo “{example}” no se resuelve por apariencia: se justifica usando la definición y revisando finalmente que {fact.lower()}.",
        ],
    )

    return {
        "semantic_id": semantic_id,
        "objetivo": f"{base._upper_initial(spec['goal']).rstrip('.')} y comprobar que {fact.lower()}.",
        "introduccion": intro,
        "resumen": f"{base._upper_initial(definition)}. Como idea de control, {fact.lower()}.",
        "explicacion": explanation,
        "procedimiento": [f"Paso 1: {step1}", f"Paso 2: {step2}", f"Paso 3: {step3}"],
        "ejemplos": build_examples(semantic_id, node_name, spec),
        "errores_frecuentes": errors_for(spec["label"], spec["confusion"], fact, spec["steps"]),
        "fuente": source_for(semantic_id.split(".")[2]),
        "estado": "publicado",
    }


# Fundamentos
add(
    "MAT.GEO.ANGULOS_FUNDAMENTOS.DEFINICION_RAYOS",
    "Definición de ángulo",
    "un ángulo es la figura formada por dos rayos que comparten un mismo origen",
    "los rayos \\(OA\\) y \\(OB\\) parten del punto \\(O\\) y abren una esquina visible",
    "sin origen común no hay ángulo, sino dos rayos distintos",
    "Cuando una puerta se abre, ambas posiciones salen de la misma bisagra. Esa idea de origen compartido es la que hace aparecer un ángulo.",
    "reconocer cuándo dos rayos sí forman un ángulo.",
    [
        "Identifica si los dos rayos parten exactamente del mismo punto.",
        "Observa la abertura determinada por esos rayos y no por segmentos ajenos al vértice.",
        "Concluye si la figura corresponde a un ángulo y justifica por qué.",
    ],
    "dos segmentos cualesquiera que aparezcan separados en el dibujo",
)
add(
    "MAT.GEO.ANGULOS_FUNDAMENTOS.ELEMENTO_VERTICE",
    "Vértice del ángulo",
    "el vértice es el punto común desde el cual nacen los dos rayos de un ángulo",
    "en \\(\\angle ABC\\), los rayos \\(BA\\) y \\(BC\\) salen del punto \\(B\\)",
    "en la notación de tres puntos, el vértice siempre queda escrito al centro",
    "En una esquina de la sala, el lugar importante no es cualquier punto del borde, sino justo el punto donde cambian de dirección las dos paredes.",
    "identificar el vértice de un ángulo a partir del dibujo o de su nombre.",
    [
        "Busca el punto desde donde parten ambos rayos.",
        "Si el ángulo está nombrado con tres letras, ubica la letra central.",
        "Verifica que el punto elegido sea común a los dos lados del ángulo.",
    ],
    "el primer punto que aparece escrito al nombrar el ángulo",
)
add(
    "MAT.GEO.ANGULOS_FUNDAMENTOS.ELEMENTO_LADOS",
    "Lados del ángulo",
    "los lados de un ángulo son los rayos que parten del vértice",
    "si el vértice es \\(O\\), los lados del ángulo pueden ser los rayos \\(OA\\) y \\(OB\\)",
    "cada lado conserva el vértice como punto inicial y se prolonga en una sola dirección",
    "Un ángulo no está hecho de bordes cerrados como una caja. Está formado por dos semirrectas que arrancan juntas y luego se abren.",
    "reconocer cuáles rayos actúan como lados de un ángulo.",
    [
        "Localiza primero el vértice común del ángulo.",
        "Determina qué dos rayos salen desde ese punto y delimitan la abertura.",
        "Comprueba que ambos lados compartan origen pero no dirección completa.",
    ],
    "dos rectas completas que se cruzan sin distinguir el origen común",
)
add(
    "MAT.GEO.ANGULOS_FUNDAMENTOS.NOTACION_LETRAS_GRIEGAS",
    "Notación con letras griegas",
    "un ángulo puede nombrarse con una letra griega cuando el contexto permite identificarlo sin ambigüedad",
    "en un esquema sencillo, un ángulo se puede marcar como \\(\\alpha\\) para referirse a su medida",
    "cambiar el nombre del ángulo no cambia su abertura ni sus lados",
    "En muchos diagramas sería incómodo escribir tres puntos sobre cada abertura. Una letra griega funciona como una etiqueta corta para hablar del mismo ángulo.",
    "interpretar la notación de un ángulo escrita con letras griegas.",
    [
        "Ubica en el dibujo qué abertura está asociada a la letra griega.",
        "Relaciona esa etiqueta con los lados y el vértice del ángulo marcado.",
        "Comprueba que la letra nombra el ángulo completo y no solo una de sus partes.",
    ],
    "una letra griega cualquiera dibujada cerca de la figura, aunque no señale una abertura concreta",
)
add(
    "MAT.GEO.ANGULOS_FUNDAMENTOS.NOTACION_TRES_PUNTOS",
    "Notación con tres puntos",
    "al escribir \\(\\angle ABC\\), el punto central \\(B\\) indica el vértice del ángulo",
    "la expresión \\(\\angle ABC\\) se lee mirando los rayos \\(BA\\) y \\(BC\\)",
    "cambiar el punto central modifica el ángulo nombrado, aunque se usen las mismas letras",
    "Nombrar un ángulo con tres puntos se parece a dar una dirección muy precisa: los extremos ayudan, pero el punto del centro es el que fija la esquina exacta.",
    "leer correctamente el orden de una notación angular con tres puntos.",
    [
        "Identifica la letra central del nombre del ángulo.",
        "Construye los dos rayos que salen desde ese punto hacia las letras de los extremos.",
        "Verifica que el nombre elegido coincide con la abertura que se quiere señalar.",
    ],
    "cualquier permutación de las tres letras, aunque cambie el punto central",
)
add(
    "MAT.GEO.ANGULOS_FUNDAMENTOS.SENTIDO_ANTIHORARIO",
    "Sentido antihorario",
    "por convenio, la medida positiva de un ángulo se lee desde el lado inicial hacia el lado final en sentido antihorario",
    "desde un rayo horizontal hacia la derecha hasta uno vertical hacia arriba se recorre una abertura de 90° en sentido antihorario",
    "el sentido de recorrido determina qué abertura se está midiendo",
    "Un reloj gira en sentido horario, pero en geometría la lectura positiva de los ángulos se hace al revés. Ese acuerdo evita ambigüedades al medir.",
    "interpretar el sentido antihorario al leer una medida angular.",
    [
        "Ubica cuál es el lado inicial y cuál es el lado final del ángulo.",
        "Recorre mentalmente la abertura en sentido contrario al movimiento del reloj.",
        "Verifica que la medida obtenida corresponda al recorrido elegido y no al complementario.",
    ],
    "medir siempre por el camino más corto, aunque el convenio indique otro sentido",
)

# Clasificación
add_classification(
    "MAT.GEO.ANGULOS_CLASIFICACION.NULO",
    "Ángulo nulo",
    "un ángulo nulo mide 0° porque sus dos rayos coinciden",
    "si ambos rayos quedan exactamente superpuestos, la abertura es 0°",
    "la coincidencia total de los lados impide que aparezca una apertura visible",
    "A veces un ángulo existe aunque no 'se vea abierto'. Si los dos rayos quedan uno sobre otro, sigue habiendo una posición geométrica que se puede nombrar.",
    "tener una abertura pequeña pero distinta de cero",
)
add_classification(
    "MAT.GEO.ANGULOS_CLASIFICACION.AGUDO",
    "Ángulo agudo",
    "un ángulo agudo mide más de 0° y menos de 90°",
    "una abertura de 35° cabe completamente antes de llegar a un ángulo recto",
    "compararlo con 90° permite distinguirlo de uno recto u obtuso",
    "Cuando una tijera apenas se abre, la abertura sigue siendo clara, pero todavía no alcanza un cuarto de vuelta.",
    "medir 90° o más",
)
add_classification(
    "MAT.GEO.ANGULOS_CLASIFICACION.RECTO",
    "Ángulo recto",
    "un ángulo recto mide exactamente 90°",
    "la esquina de una hoja o de una baldosa marca una abertura de 90°",
    "su medida exacta lo vuelve referencia para clasificar otros ángulos",
    "Muchas construcciones usan esquinas 'perfectas' para comprobar alineación. Esa abertura especial sirve como patrón de comparación.",
    "ser cualquier ángulo que parezca vertical u horizontal",
)
add_classification(
    "MAT.GEO.ANGULOS_CLASIFICACION.OBTUSO",
    "Ángulo obtuso",
    "un ángulo obtuso mide más de 90° y menos de 180°",
    "una abertura de 120° supera a un recto, pero todavía no forma una línea recta",
    "compararlo con 90° y 180° evita confundirlo con un recto o un extendido",
    "Si una puerta se abre más que una esquina cuadrada, pero aún no queda completamente alineada con el muro, su abertura es obtusa.",
    "medir menos de 90°",
)
add_classification(
    "MAT.GEO.ANGULOS_CLASIFICACION.EXTENDIDO",
    "Ángulo extendido",
    "un ángulo extendido mide exactamente 180°",
    "dos rayos opuestos forman una línea recta y determinan una abertura de 180°",
    "sus lados quedan alineados en direcciones opuestas sobre una misma recta",
    "Abrir completamente un compás hasta que sus brazos queden enfrentados sobre una misma línea produce una abertura muy especial: una media vuelta exacta.",
    "tener una medida cercana a 180° pero no exacta",
)
add(
    "MAT.GEO.ANGULOS_CLASIFICACION.LLANO",
    "Ángulo llano",
    "ángulo llano es otro nombre para un ángulo de 180°",
    "si dos rayos opuestos forman una recta, se puede decir que el ángulo es llano o extendido",
    "llano y extendido nombran la misma abertura geométrica",
    "En geometría a veces aparecen dos palabras para el mismo objeto. Aquí no hay dos ángulos distintos: hay dos formas de nombrar una media vuelta.",
    "reconocer que 'llano' y 'extendido' se usan como equivalentes.",
    [
        "Identifica si la abertura mide exactamente 180°.",
        "Relaciona esa medida con la imagen de una recta formada por rayos opuestos.",
        "Concluye que los términos 'llano' y 'extendido' describen el mismo ángulo.",
    ],
    "un ángulo diferente del extendido solo porque cambia la palabra usada",
)
add_classification(
    "MAT.GEO.ANGULOS_CLASIFICACION.CONCAVO",
    "Ángulo cóncavo",
    "un ángulo cóncavo mide más de 180° y menos de 360°",
    "si el recorrido elegido supera la media vuelta pero no completa un giro entero, el ángulo es cóncavo",
    "requiere mirar la abertura mayor y no la menor entre los mismos lados",
    "Entre dos rayos pueden existir dos recorridos posibles: uno corto y uno largo. El ángulo cóncavo aparece cuando estudiamos el recorrido grande.",
    "confundirlo con cualquier ángulo 'grande' aunque mida menos de 180°",
)
add_classification(
    "MAT.GEO.ANGULOS_CLASIFICACION.COMPLETO",
    "Ángulo completo",
    "un ángulo completo mide 360° y corresponde a un giro entero",
    "dar una vuelta completa y volver al mismo rayo inicial produce 360°",
    "volver a la dirección inicial no significa medir 0°, sino haber recorrido un giro total",
    "Cuando una rueda da una vuelta y apunta otra vez en la misma dirección, el movimiento no desaparece: completó un giro entero.",
    "ser idéntico a un ángulo nulo porque ambos terminan en la misma dirección",
)
add_classification(
    "MAT.GEO.ANGULOS_CLASIFICACION.CONVEXO",
    "Ángulo convexo",
    "un ángulo convexo mide más de 0° y menos de 180°",
    "una abertura de 150° sigue siendo convexa porque no sobrepasa la media vuelta",
    "todo agudo, recto u obtuso es convexo porque queda antes de 180°",
    "A veces conviene clasificar no por una sola medida puntual, sino por una familia entera de ángulos que comparten un mismo rango.",
    "ser cualquier ángulo menor que 360°",
)

# Relaciones métricas
add(
    "MAT.GEO.ANGULOS_RELACIONES_METRICAS.COMPLEMENTARIOS_DEFINICION",
    "Ángulos complementarios",
    "dos ángulos son complementarios cuando sus medidas suman 90°",
    "si un ángulo mide 30° y otro 60°, juntos completan 90°",
    "la relación depende de la suma de las medidas y no de la posición del dibujo",
    "Dos piezas pueden tener formas distintas y aun así completar exactamente una esquina recta cuando se juntan. Esa es la idea detrás del complemento.",
    "reconocer cuándo dos medidas forman un par de ángulos complementarios.",
    [
        "Lee las dos medidas angulares o represéntalas con una incógnita y una medida conocida.",
        "Suma ambas cantidades y compara el resultado con 90°.",
        "Concluye si el par es complementario explicando la comparación realizada.",
    ],
    "estar uno al lado del otro en el dibujo aunque su suma no sea 90°",
)
add(
    "MAT.GEO.ANGULOS_RELACIONES_METRICAS.COMPLEMENTO_CALCULO",
    "Cálculo del complemento",
    "el complemento de un ángulo se obtiene restando su medida a 90°",
    "el complemento de 27° es 63° porque \\(90°-27°=63°\\)",
    "solo existe complemento positivo para medidas menores o iguales que 90°",
    "Si ya tienes una parte de un ángulo recto, la otra parte se descubre mirando cuánto falta para completar 90°.",
    "calcular el complemento de un ángulo dado.",
    [
        "Comprueba que la medida dada no exceda 90°.",
        "Resta la medida del ángulo a 90° respetando la unidad en grados.",
        "Verifica que la suma entre el ángulo dado y el obtenido sea exactamente 90°.",
    ],
    "sumar 90° a la medida dada para hallar el complemento",
)
add(
    "MAT.GEO.ANGULOS_RELACIONES_METRICAS.SUPLEMENTARIOS_DEFINICION",
    "Ángulos suplementarios",
    "dos ángulos son suplementarios cuando sus medidas suman 180°",
    "si un ángulo mide 110° y otro 70°, juntos completan 180°",
    "la relación se comprueba por suma y no por la apariencia de estar sobre una recta",
    "Dos aberturas diferentes pueden completar una media vuelta exacta. Lo importante es el total de 180°, aunque el dibujo no las muestre pegadas.",
    "reconocer cuándo dos medidas forman un par de ángulos suplementarios.",
    [
        "Determina las dos medidas angulares que se comparan.",
        "Súmalas y contrasta el total con 180°.",
        "Decide si el par es suplementario justificando la igualdad o la diferencia encontrada.",
    ],
    "tener cualquier suma grande, aunque no llegue exactamente a 180°",
)
add(
    "MAT.GEO.ANGULOS_RELACIONES_METRICAS.SUPLEMENTO_CALCULO",
    "Cálculo del suplemento",
    "el suplemento de un ángulo se obtiene restando su medida a 180°",
    "el suplemento de 124° es 56° porque \\(180°-124°=56°\\)",
    "el resultado debe completar una media vuelta exacta con el ángulo original",
    "Cuando una abertura ya ocupa parte de una línea recta, el suplemento indica cuánto falta para completarla.",
    "calcular el suplemento de un ángulo dado.",
    [
        "Comprueba que la medida dada no exceda 180° si se busca un suplemento no negativo.",
        "Resta la medida del ángulo a 180°.",
        "Verifica que la suma del ángulo inicial y el suplemento obtenido sea 180°.",
    ],
    "restar la medida a 90° o tratar el suplemento como si fuera complemento",
)
add(
    "MAT.GEO.ANGULOS_RELACIONES_METRICAS.SUMA_RECTA",
    "Suma sobre una recta",
    "los ángulos que completan una recta suman 180°",
    "si dos ángulos adyacentes ocupan toda una línea, por ejemplo 48° y 132°, su suma es 180°",
    "la recta funciona como referencia para detectar pares lineales y suplementarios",
    "Una línea recta puede partirse en dos o más aberturas, pero la suma total sigue siendo una media vuelta.",
    "usar la recta como referencia para sumar ángulos.",
    [
        "Reconoce que los ángulos considerados cubren toda la recta sin superponerse.",
        "Suma las medidas conocidas o expresa con ecuaciones las incógnitas del esquema.",
        "Comprueba que el total obtenido sea 180° y úsalo para hallar la medida faltante.",
    ],
    "sumar 360° solo porque hay varios ángulos dibujados alrededor de un punto",
)
add(
    "MAT.GEO.ANGULOS_RELACIONES_METRICAS.SUMA_PUNTO",
    "Suma alrededor de un punto",
    "los ángulos que rodean completamente un punto suman 360°",
    "si cuatro sectores miden 80°, 95°, 110° y 75°, juntos completan 360° alrededor del punto",
    "dar una vuelta completa alrededor del vértice obliga a reunir 360°",
    "Cuando varias calles salen de una plaza central, recorrer todas sus aperturas alrededor del centro equivale a dar un giro completo.",
    "usar la suma de 360° alrededor de un punto para hallar una medida faltante.",
    [
        "Comprueba que los ángulos considerados rodean completamente el mismo vértice.",
        "Suma las medidas conocidas o representa las desconocidas con una expresión.",
        "Iguala el total a 360° y verifica que no falte ni sobre ninguna región.",
    ],
    "usar 180° aunque el recorrido complete toda la vuelta alrededor del vértice",
)

# Relaciones de posición
add(
    "MAT.GEO.ANGULOS_RELACIONES_POSICION.CONSECUTIVOS",
    "Ángulos consecutivos",
    "dos ángulos son consecutivos cuando comparten vértice y un lado",
    "si \\(\\angle AOB\\) y \\(\\angle BOC\\) tienen vértice \\(O\\) y el lado \\(OB\\) en común, son consecutivos",
    "compartir vértice no basta: también debe existir exactamente un lado común",
    "En un abanico abierto pueden aparecer varias aberturas que nacen del mismo punto. Para decidir si son consecutivas hay que mirar además si comparten un rayo.",
    "identificar un par de ángulos consecutivos en un dibujo.",
    [
        "Verifica que ambos ángulos tengan el mismo vértice.",
        "Busca si comparten uno de sus lados y distingue ese rayo común.",
        "Concluye si son consecutivos y descarta pares que solo compartan el vértice.",
    ],
    "tener solo el mismo vértice, aunque no compartan ningún lado",
)
add(
    "MAT.GEO.ANGULOS_RELACIONES_POSICION.ADYACENTES",
    "Ángulos adyacentes",
    "dos ángulos son adyacentes cuando son consecutivos y sus lados no comunes forman una recta",
    "si dos ángulos comparten un lado y los otros dos quedan como rayos opuestos, forman un par lineal",
    "todo par adyacente es consecutivo, pero no todo consecutivo es adyacente",
    "Dos ángulos pueden tocarse y aun así no completar una línea. La palabra 'adyacente' exige algo más preciso que estar uno junto al otro.",
    "distinguir un par de ángulos adyacentes de otros consecutivos.",
    [
        "Comprueba primero que los ángulos sean consecutivos.",
        "Observa si los lados no comunes quedan sobre una misma recta en sentidos opuestos.",
        "Concluye si se trata de un par adyacente o solo de un par consecutivo.",
    ],
    "compartir un lado, aunque los otros dos no formen una recta",
)
add(
    "MAT.GEO.ANGULOS_RELACIONES_POSICION.OPUESTOS_VERTICE_DEFINICION",
    "Opuestos por el vértice",
    "los ángulos opuestos por el vértice aparecen cuando dos rectas se cruzan y el par considerado queda enfrentado",
    "al cruzarse dos rectas, el ángulo de arriba y el de abajo forman un par opuesto por el vértice",
    "los ángulos opuestos por el vértice no comparten lado, pero sí el mismo vértice",
    "Cuando dos rectas se cruzan aparecen cuatro regiones. Las que se miran 'de frente' a través del cruce forman un par especial.",
    "identificar un par de ángulos opuestos por el vértice.",
    [
        "Ubica el punto donde se cortan las dos rectas.",
        "Mira qué regiones quedan enfrentadas a través del vértice y no comparten lado.",
        "Concluye si el par elegido es opuesto por el vértice y no adyacente.",
    ],
    "estar a lados distintos del dibujo aunque compartan un rayo",
)
add(
    "MAT.GEO.ANGULOS_RELACIONES_POSICION.OPUESTOS_VERTICE_IGUALDAD",
    "Igualdad de opuestos por el vértice",
    "cuando dos rectas se cruzan, los ángulos opuestos por el vértice tienen igual medida",
    "si un ángulo del cruce mide 47°, el opuesto por el vértice también mide 47°",
    "antes de copiar la medida hay que comprobar que el par sea realmente opuesto por el vértice",
    "En un cruce de rectas, algunas medidas se repiten. Esa repetición no es casual: depende de identificar bien qué regiones se enfrentan.",
    "usar la igualdad de los ángulos opuestos por el vértice.",
    [
        "Identifica un par de ángulos opuestos por el vértice en el cruce.",
        "Transfiere la medida conocida al ángulo enfrentado.",
        "Comprueba que el par elegido no comparte lado y que la igualdad aplicada corresponde al dibujo.",
    ],
    "sumar 180° para cualquier par enfrentado, aunque se trate de ángulos opuestos por el vértice",
)
add(
    "MAT.GEO.ANGULOS_RELACIONES_POSICION.BISECTRIZ_DEFINICION",
    "Bisectriz",
    "la bisectriz de un ángulo es el rayo que lo divide en dos ángulos de igual medida",
    "si un rayo interior parte el ángulo de 50° en dos aberturas de 25°, ese rayo es su bisectriz",
    "dividir en dos partes no basta: ambas medidas deben ser exactamente iguales",
    "Partir un sándwich 'a ojo' no asegura dos mitades iguales. Con los ángulos ocurre lo mismo: la bisectriz exige igualdad precisa.",
    "reconocer cuándo un rayo interior es bisectriz de un ángulo.",
    [
        "Ubica el rayo interior que sale desde el vértice del ángulo.",
        "Compara las dos medidas que genera ese rayo dentro del ángulo.",
        "Concluye que es bisectriz solo si ambas aberturas son iguales.",
    ],
    "cualquier rayo interior que salga del vértice, aunque no divida en partes iguales",
)
add(
    "MAT.GEO.ANGULOS_RELACIONES_POSICION.BISECTRIZ_CALCULO",
    "Cálculo con bisectriz",
    "si un ángulo es dividido por su bisectriz, las dos medidas resultantes son iguales y su suma reproduce el ángulo completo",
    "si una bisectriz parte un ángulo de 86°, cada mitad mide 43°",
    "también puede usarse al revés: dos partes iguales permiten reconstruir el ángulo total",
    "Cuando una abertura queda partida en dos mitades exactas, la mitad y el total se determinan uno a partir del otro con facilidad.",
    "calcular medidas angulares usando la propiedad de la bisectriz.",
    [
        "Comprueba que el rayo indicado sea efectivamente una bisectriz.",
        "Plantea la igualdad entre las dos partes o divide el total en dos mitades iguales.",
        "Verifica que la suma de las partes recupere el ángulo original.",
    ],
    "restar una mitad al total sin imponer que ambas partes sean iguales",
)
add(
    "MAT.GEO.ANGULOS_RELACIONES_POSICION.RECTAS_PERPENDICULARES_DEFINICION",
    "Rectas perpendiculares",
    "dos rectas son perpendiculares cuando se cortan formando un ángulo recto",
    "una recta vertical y una horizontal que se cruzan producen una abertura de 90°",
    "la perpendicularidad se decide por la medida del ángulo y no por la apariencia de estar inclinadas",
    "En una hoja cuadriculada muchas rectas parecen 'derechas', pero la perpendicularidad solo aparece cuando el cruce genera un ángulo recto.",
    "reconocer cuándo dos rectas son perpendiculares.",
    [
        "Ubica el punto de corte entre las dos rectas.",
        "Comprueba si una de las aberturas formadas mide 90°.",
        "Concluye que las rectas son perpendiculares y recuerda que entonces aparecen cuatro ángulos rectos.",
    ],
    "verse una hacia arriba y otra hacia el lado, aunque no formen 90° exactos",
)
add(
    "MAT.GEO.ANGULOS_RELACIONES_POSICION.RECTAS_PERPENDICULARES_ANGULOS_RECTOS",
    "Cuatro rectos en una perpendicular",
    "si dos rectas son perpendiculares, las cuatro regiones angulares del cruce miden 90°",
    "al saberse que un cruce es perpendicular, cada uno de los cuatro ángulos vale 90°",
    "basta reconocer un ángulo recto en el cruce para deducir los otros tres",
    "Cuando dos rectas se cruzan a escuadra, la regularidad del cruce hace que no aparezcan medidas distintas entre sus cuatro regiones.",
    "deducir las cuatro medidas rectas en un cruce perpendicular.",
    [
        "Identifica que el cruce corresponde a dos rectas perpendiculares.",
        "Usa la presencia de un ángulo recto para trasladar esa medida a las otras tres regiones.",
        "Verifica que las cuatro aberturas sumen 360° alrededor del punto.",
    ],
    "solo el ángulo marcado con un cuadrado mide 90°, mientras los demás pueden variar",
)

# Paralelas y transversal
add_transversal_identification(
    "MAT.GEO.ANGULOS_RECTAS_TRANSVERSALES.ALTERNOS_INTERNOS_IDENTIFICACION",
    "Alternos internos",
    "alternos internos",
    "entre dos paralelas, los ángulos 3 y 5 quedan dentro de las rectas y a lados opuestos de la transversal",
    "estar en la zona interior y en lados opuestos de la transversal es lo que define al par",
    "cualquier par interior, aunque quede del mismo lado de la transversal",
)
add_transversal_property(
    "MAT.GEO.ANGULOS_RECTAS_TRANSVERSALES.ALTERNOS_INTERNOS_IGUALDAD",
    "Igualdad de alternos internos",
    "alternos internos",
    "tienen igual medida",
    "si un alterno interno mide 68°, el otro alterno interno también mide 68°",
    "ser suplementarios por estar dentro de las paralelas",
)
add_transversal_identification(
    "MAT.GEO.ANGULOS_RECTAS_TRANSVERSALES.ALTERNOS_EXTERNOS_IDENTIFICACION",
    "Alternos externos",
    "alternos externos",
    "fuera de las paralelas, los ángulos 1 y 7 quedan a lados opuestos de la transversal",
    "la clave es estar en la zona exterior y cambiar de lado respecto de la transversal",
    "cualquier par externo, aunque ambos estén del mismo lado",
)
add_transversal_property(
    "MAT.GEO.ANGULOS_RECTAS_TRANSVERSALES.ALTERNOS_EXTERNOS_IGUALDAD",
    "Igualdad de alternos externos",
    "alternos externos",
    "tienen igual medida",
    "si un alterno externo vale 123°, su alterno externo correspondiente también vale 123°",
    "sumar 180° solo por estar en la parte exterior",
)
add_transversal_identification(
    "MAT.GEO.ANGULOS_RECTAS_TRANSVERSALES.CORRESPONDIENTES_IDENTIFICACION",
    "Correspondientes",
    "correspondientes",
    "en dos intersecciones análogas, los ángulos 2 y 6 ocupan la misma 'esquina' relativa",
    "la misma posición relativa en cada cruce identifica a los correspondientes",
    "estar uno frente al otro dentro del mismo cruce",
)
add_transversal_property(
    "MAT.GEO.ANGULOS_RECTAS_TRANSVERSALES.CORRESPONDIENTES_IGUALDAD",
    "Igualdad de correspondientes",
    "correspondientes",
    "tienen igual medida",
    "si un ángulo correspondiente mide 41°, el otro correspondiente también mide 41°",
    "ser suplementarios por parecer ubicados 'arriba' en el dibujo",
)
add_transversal_identification(
    "MAT.GEO.ANGULOS_RECTAS_TRANSVERSALES.COLATERALES_INTERNOS_IDENTIFICACION",
    "Colaterales internos",
    "colaterales internos",
    "entre las paralelas, dos ángulos quedan del mismo lado de la transversal",
    "compartir lado respecto de la transversal y estar dentro de las paralelas define este par",
    "estar en lados opuestos de la transversal aunque sigan siendo interiores",
)
add_transversal_property(
    "MAT.GEO.ANGULOS_RECTAS_TRANSVERSALES.COLATERALES_INTERNOS_SUPLEMENTARIOS",
    "Suplementarios colaterales internos",
    "colaterales internos",
    "suman 180°",
    "si un colateral interno mide 112°, el otro mide 68° para completar 180°",
    "tener siempre la misma medida por estar ambos en el interior",
)
add_transversal_identification(
    "MAT.GEO.ANGULOS_RECTAS_TRANSVERSALES.COLATERALES_EXTERNOS_IDENTIFICACION",
    "Colaterales externos",
    "colaterales externos",
    "fuera de las paralelas, dos ángulos quedan del mismo lado de la transversal",
    "la posición exterior y el mismo lado de la transversal son la clave del nombre",
    "quedar fuera de las paralelas y en lados opuestos de la transversal",
)
add_transversal_property(
    "MAT.GEO.ANGULOS_RECTAS_TRANSVERSALES.COLATERALES_EXTERNOS_SUPLEMENTARIOS",
    "Suplementarios colaterales externos",
    "colaterales externos",
    "suman 180°",
    "si un colateral externo vale 145°, el otro debe medir 35°",
    "ser iguales solo por estar ambos fuera de las paralelas",
)
add(
    "MAT.GEO.ANGULOS_RECTAS_TRANSVERSALES.RESOLUCION_MEDIDAS_INCOGNITAS",
    "Incógnitas con paralelas y transversal",
    "las incógnitas angulares en paralelas y transversal se resuelven identificando primero la relación geométrica correcta y luego usando igualdad o suplementariedad",
    "si \\(x\\) y 124° forman un par colateral interno, entonces \\(x+124=180\\)",
    "el paso decisivo es nombrar bien el par antes de escribir la ecuación",
    "En estos problemas la cuenta suele ser corta; lo difícil es descubrir qué relación geométrica gobierna el dibujo.",
    "resolver una incógnita angular usando paralelas y una transversal.",
    [
        "Identifica qué par de ángulos interviene y clasifícalo correctamente.",
        "Traduce esa relación a igualdad o a suma de 180° según corresponda.",
        "Resuelve la ecuación y comprueba que el valor obtenido coincide con la posición del dibujo.",
    ],
    "escribir una ecuación al azar sin clasificar antes el par de ángulos",
)

# Medición angular
add(
    "MAT.GEO.MEDICION_ANGULAR.SISTEMA_SEXAGESIMAL",
    "Sistema sexagesimal",
    "el sistema sexagesimal mide ángulos en grados y divide la vuelta completa en 360 partes iguales",
    "un cuarto de vuelta equivale a 90° dentro del sistema sexagesimal",
    "usar 360° para la vuelta completa permite comparar medias vueltas, cuartos y fracciones del giro",
    "Muchos ángulos escolares se expresan en grados porque esa unidad parte la vuelta completa en 360 trozos iguales y muy manejables.",
    "interpretar la medición angular en grados dentro del sistema sexagesimal.",
    [
        "Reconoce que la unidad usada es el grado.",
        "Relaciona la medida dada con fracciones de una vuelta completa de 360°.",
        "Comprueba si la interpretación coincide con media vuelta, cuarto de vuelta u otra referencia conocida.",
    ],
    "medir una vuelta completa con 100 unidades en vez de 360",
)
add(
    "MAT.GEO.MEDICION_ANGULAR.MINUTOS_SEGUNDOS",
    "Minutos y segundos angulares",
    "en el sistema sexagesimal, 1° se divide en 60 minutos y 1 minuto en 60 segundos",
    "la medida \\(25°\\,18'\\,36''\\) usa grados, minutos y segundos angulares",
    "minutos y segundos angulares no representan tiempo, sino subdivisiones del grado",
    "En un mapa o en astronomía se usan medidas muy finas. Para no abandonar los grados, se los subdivide en minutos y segundos angulares.",
    "leer y descomponer una medida angular en grados, minutos y segundos.",
    [
        "Ubica qué parte de la medida corresponde a grados, minutos y segundos.",
        "Recuerda las equivalencias \\(1°=60'\\) y \\(1'=60''\\).",
        "Comprueba que cada subunidad esté interpretada como parte del grado y no como tiempo.",
    ],
    "tratar los minutos y segundos angulares exactamente como minutos y segundos de un reloj",
)
add_measure_conversion(
    "MAT.GEO.MEDICION_ANGULAR.CONVERSION_GRADOS_MINUTOS_SEGUNDOS",
    "Conversión grados-minutos-segundos",
    "convertir entre grados, minutos y segundos exige usar que \\(1°=60'\\) y \\(1'=60''\\)",
    "para pasar \\(2.5°\\) a minutos, se calcula \\(2.5\\times 60=150'\\)",
    "cada cambio de unidad multiplica o divide por 60 según el sentido de la conversión",
    "Cambiar de grados a minutos o segundos se parece a cambiar de kilómetros a metros: la idea es la misma, pero la equivalencia correcta aquí es sexagesimal.",
    "sumar 60 en vez de multiplicar o dividir por 60",
)
add(
    "MAT.GEO.MEDICION_ANGULAR.RADIAN_DEFINICION",
    "Radián",
    "un radián es el ángulo central que subtiende un arco cuya longitud es igual al radio de la circunferencia",
    "si el arco y el radio miden lo mismo, el ángulo central correspondiente mide 1 radián",
    "el radián nace de una razón geométrica y no de una división arbitraria de la vuelta",
    "A diferencia del grado, el radián no aparece porque alguien partió la vuelta en muchas piezas. Surge directamente al comparar longitudes en una circunferencia.",
    "interpretar el radián como una unidad geométrica de medida angular.",
    [
        "Relaciona el ángulo con un arco y con el radio de la circunferencia.",
        "Comprueba si la longitud del arco coincide con la del radio o con un múltiplo de ella.",
        "Concluye la medida en radianes explicando la relación geométrica utilizada.",
    ],
    "ser simplemente otra palabra para 1°",
)
add_measure_conversion(
    "MAT.GEO.MEDICION_ANGULAR.EQUIVALENCIA_GRADOS_RADIANES",
    "Equivalencia grados-radianes",
    "una media vuelta equivale simultáneamente a 180° y a \\(\\pi\\) radianes",
    "el ángulo llano puede escribirse como 180° o como \\(\\pi\\) rad",
    "la equivalencia \\(180°=\\pi\\) rad es el puente básico entre ambos sistemas",
    "Para pasar de grados a radianes no hace falta memorizar muchas fórmulas: basta con recordar cómo se expresa la media vuelta en cada sistema.",
    "tratar \\(\\pi\\) como si fuera la medida de una vuelta completa",
)
add_measure_conversion(
    "MAT.GEO.MEDICION_ANGULAR.CONVERSION_GRADOS_RADIANES",
    "Conversión grados-radianes",
    "convertir entre grados y radianes exige usar la equivalencia \\(180°=\\pi\\) rad",
    "para pasar 60° a radianes se calcula \\(60\\cdot\\pi/180=\\pi/3\\)",
    "conviene dejar el resultado exacto en función de \\(\\pi\\) cuando no se pide aproximación decimal",
    "Una misma abertura puede leerse con grados o con radianes. La conversión no cambia el ángulo: solo cambia la unidad con que lo describimos.",
    "dividir por \\(\\pi\\) siempre, sin revisar en qué sentido va la conversión",
)
add(
    "MAT.GEO.MEDICION_ANGULAR.SISTEMA_CENTESIMAL",
    "Sistema centesimal",
    "el sistema centesimal divide la vuelta completa en 400 gradianes",
    "un ángulo recto equivale a 100 gradianes en el sistema centesimal",
    "en este sistema la media vuelta corresponde a 200 gradianes",
    "Así como el sistema sexagesimal reparte la vuelta en 360 partes, el centesimal la reparte en 400. Cambia la escala, no la abertura geométrica.",
    "interpretar medidas angulares en gradianes.",
    [
        "Reconoce que la unidad empleada es el gradian o gon.",
        "Relaciona la medida con la vuelta completa de 400 gradianes.",
        "Comprueba equivalencias simples como 100 gradianes para un recto y 200 para una media vuelta.",
    ],
    "usar 360 como vuelta completa también en el sistema centesimal",
)
add_measure_conversion(
    "MAT.GEO.MEDICION_ANGULAR.EQUIVALENCIA_CENTESIMAL",
    "Equivalencia sexagesimal-centesimal",
    "la vuelta completa puede escribirse como 360° o como 400 gradianes",
    "si una vuelta completa vale 400g, entonces un ángulo recto vale 100g",
    "la equivalencia 360° = 400g permite pasar de un sistema a otro por proporcionalidad",
    "Cambiar entre grados y gradianes es parecido a cambiar entre pesos y centavos: la magnitud no cambia, solo la escala numérica.",
    "pensar que 1° equivale exactamente a 1 gradian",
)

# Aplicaciones
add(
    "MAT.GEO.ANGULOS_APLICACIONES.ELEVACION_DEFINICION",
    "Ángulo de elevación",
    "el ángulo de elevación se mide desde la horizontal del observador hacia arriba, hasta la línea de visión",
    "si una persona mira la parte alta de un edificio, el ángulo entre la horizontal y su mirada es un ángulo de elevación",
    "la referencia siempre es la horizontal del observador y no la pared del objeto observado",
    "Cuando miras la cima de un cerro no partes desde el suelo del cerro, sino desde tu propia línea horizontal de mirada.",
    "reconocer un ángulo de elevación en un contexto real.",
    [
        "Ubica al observador y dibuja mentalmente su horizontal.",
        "Traza la línea de visión hacia el objeto que está por encima de esa horizontal.",
        "Identifica el ángulo formado entre ambas direcciones y verifica que se mida hacia arriba.",
    ],
    "medir el ángulo desde la vertical del edificio en vez de desde la horizontal del observador",
)
add(
    "MAT.GEO.ANGULOS_APLICACIONES.DEPRESION_DEFINICION",
    "Ángulo de depresión",
    "el ángulo de depresión se mide desde la horizontal del observador hacia abajo, hasta la línea de visión",
    "desde un balcón, el ángulo entre la horizontal de la vista y la mirada hacia un auto en la calle es un ángulo de depresión",
    "la horizontal sigue siendo la referencia, aunque el objeto observado quede más abajo",
    "Mirar hacia abajo desde un mirador parece lo opuesto del ángulo de elevación, pero la referencia geométrica sigue siendo exactamente la misma: la horizontal.",
    "reconocer un ángulo de depresión en un contexto real.",
    [
        "Ubica la horizontal del observador en el punto desde donde mira.",
        "Traza la línea de visión hacia el objeto situado más abajo.",
        "Comprueba que el ángulo se lee desde la horizontal descendiendo hacia la línea visual.",
    ],
    "medirlo desde el suelo del objeto observado y no desde el observador",
)
add(
    "MAT.GEO.ANGULOS_APLICACIONES.MANECILLA_MINUTERA_AVANCE",
    "Avance de la minutera",
    "la manecilla minutera recorre 360° en 60 minutos, por lo que avanza 6° por minuto",
    "en 10 minutos, la minutera gira \\(10\\cdot 6° = 60°\\)",
    "el cálculo se basa en una proporcionalidad directa entre tiempo transcurrido y giro",
    "Un reloj da una vuelta completa cada hora con la minutera. Repartir esa vuelta en 60 minutos permite saber cuánto gira en cualquier intervalo.",
    "calcular el giro de la manecilla minutera en un intervalo dado.",
    [
        "Recuerda que la vuelta completa de la minutera es 360° en 60 minutos.",
        "Obtén la tasa de giro de 6° por minuto.",
        "Multiplica esa tasa por el tiempo transcurrido y verifica que el resultado sea coherente con una hora completa.",
    ],
    "usar 0,5° por minuto, que corresponde a la manecilla horaria",
)
add(
    "MAT.GEO.ANGULOS_APLICACIONES.MANECILLA_HORARIA_AVANCE",
    "Avance de la horaria",
    "la manecilla horaria recorre 360° en 12 horas, por lo que avanza 30° por hora o 0,5° por minuto",
    "en 20 minutos, la horaria gira \\(20\\cdot 0.5° = 10°\\)",
    "aunque se mueva más lento que la minutera, su avance también es uniforme",
    "La manecilla de las horas parece casi quieta, pero en realidad gira todo el tiempo. Su lentitud obliga a medir con más atención.",
    "calcular el giro de la manecilla horaria en minutos u horas.",
    [
        "Recuerda que la horaria completa 360° en 12 horas.",
        "Convierte esa vuelta a una tasa de 30° por hora o 0,5° por minuto.",
        "Multiplica por el tiempo transcurrido y comprueba que el resultado sea menor que el de la minutera en el mismo intervalo.",
    ],
    "usar 6° por minuto, que corresponde a la manecilla minutera",
)
add(
    "MAT.GEO.ANGULOS_APLICACIONES.MANECILLAS_ANGULO_MENOR",
    "Ángulo menor entre manecillas",
    "el ángulo menor entre las manecillas del reloj se obtiene comparando sus posiciones y eligiendo la abertura más pequeña",
    "a las 3:00, la minutera está en 12 y la horaria en 3, de modo que el ángulo menor es 90°",
    "primero se calculan las posiciones de cada manecilla y solo al final se elige la abertura menor",
    "Entre dos manecillas siempre hay dos caminos posibles alrededor del centro. El problema pide el menor, así que no basta con restar sin interpretar el dibujo.",
    "calcular el ángulo menor entre las manecillas de un reloj.",
    [
        "Calcula o identifica la posición angular de cada manecilla respecto de las 12.",
        "Resta ambas posiciones para obtener una abertura posible.",
        "Compara esa abertura con 360° menos ella y elige la menor de las dos.",
    ],
    "restar las posiciones y aceptar siempre ese resultado, aunque exista una abertura menor",
)


def main() -> None:
    nodes = list(
        KnowledgeNode.objects.filter(
            node_type="recurso",
            parent__parent__semantic_id="MAT.GEO.B0401",
        ).order_by("parent__order", "order", "semantic_id")
    )
    ids = [node.semantic_id for node in nodes]
    missing = set(ids) - set(SPECS)
    extra = set(SPECS) - set(ids)
    if len(nodes) != 53 or missing or extra:
        raise RuntimeError(
            f"B0401 inconsistente: nodes={len(nodes)} missing={missing} extra={extra}"
        )

    for node in nodes:
        base.safe_write_yaml(
            base.CONTENT_DIR / yaml_filename(node.semantic_id),
            build_content(node.semantic_id, node.name),
        )

    all_meta = {
        sid: {
            "definition": SPECS[sid]["definition"],
            "example": SPECS[sid]["example"],
            "fact": SPECS[sid]["fact"],
        }
        for sid in ids
    }
    groups = [ids[i : i + 5] for i in range(0, len(ids), 5)]
    for index, group in enumerate(groups, start=1):
        rows = []
        for sid in group:
            node = next(n for n in nodes if n.semantic_id == sid)
            rows.extend(base.make_exercises(sid, node.name, node.competencia, all_meta))
        base.write_jsonl(
            base.EXERCISES_DIR / f"mat-geo-angulos-banco-gen-{index}.jsonl",
            rows,
        )

    print(f"B0401 generado: {len(nodes)} YAML y {len(groups)} JSONL.")


if __name__ == "__main__":
    main()
