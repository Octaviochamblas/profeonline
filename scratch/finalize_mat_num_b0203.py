from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import django
import yaml


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from apps.content.models import KnowledgeNode  # noqa: E402


CONTENT_DIR = ROOT / "docs" / "conocimiento" / "contenido"
EXERCISES_DIR = ROOT / "docs" / "conocimiento" / "ejercicios"


class Dumper(yaml.SafeDumper):
    pass


def _str_presenter(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


Dumper.add_representer(str, _str_presenter)


RESOURCE_GROUPS = [
    [
        "MAT.NUM.RACIONALES_CONCEPTO.DEFINICION_Q",
        "MAT.NUM.RACIONALES_CONCEPTO.CONDICION_DENOMINADOR_NO_CERO",
        "MAT.NUM.RACIONALES_CONCEPTO.ENTEROS_COMO_RACIONALES",
        "MAT.NUM.RACIONALES_CONCEPTO.SIGNO_RACIONAL",
        "MAT.NUM.FRACCIONES_CONCEPTO.FRACCION_PARTE_TODO",
        "MAT.NUM.FRACCIONES_CONCEPTO.NUMERADOR_IDENTIFICACION",
        "MAT.NUM.FRACCIONES_CONCEPTO.DENOMINADOR_IDENTIFICACION",
        "MAT.NUM.FRACCIONES_CONCEPTO.UNIDAD_FRACCIONARIA",
    ],
    [
        "MAT.NUM.FRACCIONES_CLASIFICACION.FRACCION_PROPIA",
        "MAT.NUM.FRACCIONES_CLASIFICACION.FRACCION_IMPROPIA",
        "MAT.NUM.FRACCIONES_CLASIFICACION.FRACCION_APARENTE",
        "MAT.NUM.FRACCIONES_CLASIFICACION.NUMERO_MIXTO_CONCEPTO",
        "MAT.NUM.FRACCIONES_CLASIFICACION.FRACCION_NO_DEFINIDA",
    ],
    [
        "MAT.NUM.FRACCIONES_CLASIFICACION.FORMA_INDETERMINADA_CERO_SOBRE_CERO",
        "MAT.NUM.FRACCIONES_EQUIVALENCIA.FRACCIONES_EQUIVALENTES_CONCEPTO",
        "MAT.NUM.FRACCIONES_EQUIVALENCIA.AMPLIFICACION",
        "MAT.NUM.FRACCIONES_EQUIVALENCIA.SIMPLIFICACION",
        "MAT.NUM.FRACCIONES_EQUIVALENCIA.FRACCION_IRREDUCTIBLE",
    ],
    [
        "MAT.NUM.FRACCIONES_EQUIVALENCIA.PRODUCTOS_CRUZADOS",
        "MAT.NUM.FRACCIONES_EQUIVALENCIA.MIXTO_A_IMPROPIA",
        "MAT.NUM.FRACCIONES_EQUIVALENCIA.IMPROPIA_A_MIXTO",
        "MAT.NUM.FRACCIONES_COMPARACION.IGUAL_DENOMINADOR",
        "MAT.NUM.FRACCIONES_COMPARACION.IGUAL_NUMERADOR",
    ],
    [
        "MAT.NUM.FRACCIONES_COMPARACION.DISTINTO_DENOMINADOR",
        "MAT.NUM.FRACCIONES_COMPARACION.PRODUCTO_CRUZADO",
        "MAT.NUM.FRACCIONES_COMPARACION.UBICACION_RECTA",
        "MAT.NUM.FRACCIONES_COMPARACION.DENSIDAD_Q",
        "MAT.NUM.FRACCIONES_OPERATORIA.ADICION_IGUAL_DENOMINADOR",
    ],
    [
        "MAT.NUM.FRACCIONES_OPERATORIA.SUSTRACCION_IGUAL_DENOMINADOR",
        "MAT.NUM.FRACCIONES_OPERATORIA.ADICION_DISTINTO_DENOMINADOR",
        "MAT.NUM.FRACCIONES_OPERATORIA.SUSTRACCION_DISTINTO_DENOMINADOR",
        "MAT.NUM.FRACCIONES_OPERATORIA.MULTIPLICACION",
        "MAT.NUM.FRACCIONES_OPERATORIA.INVERSO_MULTIPLICATIVO",
    ],
    [
        "MAT.NUM.FRACCIONES_OPERATORIA.DIVISION",
        "MAT.NUM.FRACCIONES_OPERATORIA.OPERATORIA_CON_MIXTOS",
        "MAT.NUM.FRACCIONES_OPERATORIA.JERARQUIA_OPERACIONES",
        "MAT.NUM.FRACCIONES_OPERATORIA.FRACCION_DE_CANTIDAD",
        "MAT.NUM.RACIONALES_PROPIEDADES.CLAUSURA_ADICION",
    ],
    [
        "MAT.NUM.RACIONALES_PROPIEDADES.CLAUSURA_MULTIPLICACION",
        "MAT.NUM.RACIONALES_PROPIEDADES.CONMUTATIVA_ADICION",
        "MAT.NUM.RACIONALES_PROPIEDADES.CONMUTATIVA_MULTIPLICACION",
        "MAT.NUM.RACIONALES_PROPIEDADES.ASOCIATIVA_ADICION",
        "MAT.NUM.RACIONALES_PROPIEDADES.ASOCIATIVA_MULTIPLICACION",
    ],
    [
        "MAT.NUM.RACIONALES_PROPIEDADES.NEUTRO_ADITIVO",
        "MAT.NUM.RACIONALES_PROPIEDADES.NEUTRO_MULTIPLICATIVO",
        "MAT.NUM.RACIONALES_PROPIEDADES.INVERSO_ADITIVO",
        "MAT.NUM.RACIONALES_PROPIEDADES.INVERSO_MULTIPLICATIVO",
        "MAT.NUM.RACIONALES_PROPIEDADES.DISTRIBUTIVA_SUMA",
    ],
    [
        "MAT.NUM.RACIONALES_PROPIEDADES.DISTRIBUTIVA_RESTA",
        "MAT.NUM.DECIMALES_CLASIFICACION.DECIMAL_FINITO",
        "MAT.NUM.DECIMALES_CLASIFICACION.DECIMAL_PERIODICO",
        "MAT.NUM.DECIMALES_CLASIFICACION.DECIMAL_SEMIPERIODICO",
        "MAT.NUM.DECIMALES_CLASIFICACION.PERIODO_IDENTIFICACION",
    ],
    [
        "MAT.NUM.DECIMALES_CLASIFICACION.ANTEPERIODO_IDENTIFICACION",
        "MAT.NUM.DECIMALES_OPERATORIA.ADICION",
        "MAT.NUM.DECIMALES_OPERATORIA.SUSTRACCION",
        "MAT.NUM.DECIMALES_OPERATORIA.MULTIPLICACION",
        "MAT.NUM.DECIMALES_OPERATORIA.DIVISION_POR_NATURAL",
    ],
    [
        "MAT.NUM.DECIMALES_OPERATORIA.DIVISION_POR_DECIMAL",
        "MAT.NUM.FRACCION_DECIMAL.CONVERSION_DIVISION",
        "MAT.NUM.FRACCION_DECIMAL.DENOMINADOR_POTENCIA_DIEZ",
        "MAT.NUM.FRACCION_DECIMAL.DETECCION_DECIMAL_FINITO",
        "MAT.NUM.FRACCION_DECIMAL.DETECCION_DECIMAL_PERIODICO",
    ],
    [
        "MAT.NUM.DECIMAL_FRACCION.FINITO",
        "MAT.NUM.DECIMAL_FRACCION.PERIODICO",
        "MAT.NUM.DECIMAL_FRACCION.SEMIPERIODICO",
        "MAT.NUM.APROXIMACIONES.APROXIMACION_DEFECTO",
        "MAT.NUM.APROXIMACIONES.APROXIMACION_EXCESO",
    ],
    [
        "MAT.NUM.APROXIMACIONES.REDONDEO",
        "MAT.NUM.APROXIMACIONES.REGLA_DEL_CINCO",
        "MAT.NUM.APROXIMACIONES.TRUNCAMIENTO",
        "MAT.NUM.ERROR_NUMERICO.ERROR_ABSOLUTO",
        "MAT.NUM.ERROR_NUMERICO.ERROR_RELATIVO",
    ],
    [
        "MAT.NUM.ERROR_NUMERICO.ERROR_PORCENTUAL",
    ],
]


GENERIC_DEFINITIONS = [
    "una comparación que depende solo del orden en que aparecen los números",
    "una propiedad geométrica de figuras planas",
    "una operación que no usa fracciones ni decimales",
    "una regla aritmética válida solo para números enteros positivos",
]
GENERIC_EXAMPLES = [
    "Comparar dos ángulos sin usar fracciones.",
    "Resolver 8 + 3 sin interpretar partes de un todo.",
    "Medir el perímetro de un triángulo cualquiera.",
    "Contar objetos sin usar razones ni aproximaciones.",
]
GENERIC_FACTS = [
    "Siempre conviene revisar la definición antes de operar.",
    "La notación correcta evita errores de interpretación.",
    "El contexto indica qué representación es más útil.",
    "Un mismo número puede escribirse de distintas maneras equivalentes.",
]
GENERIC_TITLES = [
    "Una comparación geométrica",
    "Un cálculo entero",
    "Una propiedad de figuras",
    "Una suma sin contexto",
]


def safe_write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        yaml.dump(data, fh, Dumper=Dumper, allow_unicode=True, sort_keys=False)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def yaml_filename(semantic_id: str) -> str:
    _, _, subtema, concepto = semantic_id.split(".", 3)
    return f"mat-num-{subtema.lower().replace('_', '-')}-{concepto.lower().replace('_', '-')}.yaml"


def stable_prefix(semantic_id: str) -> str:
    return hashlib.sha1(semantic_id.encode("utf-8")).hexdigest()[:6].upper()


def siblings_for(all_meta: dict[str, dict], semantic_id: str, field: str) -> list[str]:
    subtheme = semantic_id.split(".")[2]
    values: list[str] = []
    for sid, meta in all_meta.items():
        if sid == semantic_id or sid.split(".")[2] != subtheme:
            continue
        if meta.get(field):
            values.append(meta[field])
    return values


def choose_distractors(correct: str, others: list[str], fallback: list[str]) -> list[str]:
    merged = [x for x in others if x and x != correct]
    for item in fallback:
        if item and item != correct and item not in merged:
            merged.append(item)
        if len(merged) >= 3:
            break
    return merged[:3]


def place_correct(correct: str, distractors: list[str], seed: str) -> tuple[list[str], str]:
    pos = int(hashlib.sha1(seed.encode("utf-8")).hexdigest(), 16) % 4
    choices = distractors[:]
    while len(choices) < 3:
        filler = f"Distractor {len(choices)+1}"
        if filler != correct and filler not in choices:
            choices.append(filler)
    choices.insert(pos, correct)
    return choices, correct


def meta_for(semantic_id: str, name: str) -> dict:
    subtheme = semantic_id.split(".")[2]
    concept = semantic_id.split(".")[3]

    if subtheme == "RACIONALES_CONCEPTO":
        if concept == "DEFINICION_Q":
            return {
                "definition": "un número racional es todo número que puede escribirse como \\(\\frac{a}{b}\\) con \\(a, b \\in \\mathbb{Z}\\) y \\(b \\neq 0\\)",
                "example": "Por ejemplo, \\(\\frac{3}{4}\\), \\(-\\frac{7}{2}\\) y \\(5=\\frac{5}{1}\\) son racionales.",
                "fact": "Todo número racional tiene una representación fraccionaria con denominador distinto de cero.",
            }
        if concept == "CONDICION_DENOMINADOR_NO_CERO":
            return {
                "definition": "en una fracción racional el denominador no puede ser cero, porque dividir por cero no está definido",
                "example": "La expresión \\(\\frac{5}{0}\\) no representa un número racional.",
                "fact": "La condición \\(b \\neq 0\\) es parte esencial de la definición de racional.",
            }
        if concept == "ENTEROS_COMO_RACIONALES":
            return {
                "definition": "todo número entero puede escribirse como un racional con denominador 1",
                "example": "El entero \\(-3\\) puede escribirse como \\(-\\frac{3}{1}\\).",
                "fact": "El conjunto de los enteros está contenido en el conjunto de los racionales.",
            }
        if concept == "SIGNO_RACIONAL":
            return {
                "definition": "el signo de un número racional depende del signo conjunto del numerador y del denominador",
                "example": "\\(-\\frac{2}{5}\\) y \\(\\frac{2}{-5}\\) son negativos, mientras que \\(-\\frac{2}{-5}\\) es positivo.",
                "fact": "Si numerador y denominador tienen igual signo, la fracción es positiva.",
            }

    if subtheme == "FRACCIONES_CONCEPTO":
        if concept == "FRACCION_PARTE_TODO":
            return {
                "definition": "una fracción puede interpretar una o varias partes iguales tomadas de un todo dividido en partes iguales",
                "example": "Si una pizza se divide en 8 partes y tomamos 3, representamos \\(\\frac{3}{8}\\).",
                "fact": "En la interpretación parte-todo, el entero debe estar dividido en partes del mismo tamaño.",
            }
        if concept == "NUMERADOR_IDENTIFICACION":
            return {
                "definition": "el numerador indica cuántas partes del todo se consideran",
                "example": "En \\(\\frac{5}{7}\\), el numerador es 5 y cuenta las partes tomadas.",
                "fact": "El numerador se escribe sobre la barra de fracción.",
            }
        if concept == "DENOMINADOR_IDENTIFICACION":
            return {
                "definition": "el denominador indica en cuántas partes iguales se dividió el todo",
                "example": "En \\(\\frac{5}{7}\\), el denominador es 7 y representa las partes iguales del entero.",
                "fact": "El denominador se escribe bajo la barra de fracción y no puede ser cero.",
            }
        if concept == "UNIDAD_FRACCIONARIA":
            return {
                "definition": "una unidad fraccionaria es una fracción con numerador 1 que representa una sola parte igual del entero",
                "example": "\\(\\frac{1}{6}\\) es una unidad fraccionaria del entero dividido en 6 partes iguales.",
                "fact": "Las unidades fraccionarias sirven como referencia para construir otras fracciones.",
            }

    if subtheme == "FRACCIONES_CLASIFICACION":
        if concept == "FRACCION_PROPIA":
            return {
                "definition": "una fracción propia tiene numerador menor que denominador y representa una cantidad menor que 1",
                "example": "\\(\\frac{3}{5}\\) es propia porque 3 es menor que 5.",
                "fact": "Toda fracción propia positiva se ubica entre 0 y 1 en la recta numérica.",
            }
        if concept == "FRACCION_IMPROPIA":
            return {
                "definition": "una fracción impropia tiene numerador mayor que denominador y representa una cantidad mayor que 1",
                "example": "\\(\\frac{9}{4}\\) es impropia porque 9 es mayor que 4.",
                "fact": "Una fracción impropia puede convertirse en número mixto.",
            }
        if concept == "FRACCION_APARENTE":
            return {
                "definition": "una fracción aparente es una fracción cuyo numerador es múltiplo del denominador y equivale a un número entero",
                "example": "\\(\\frac{12}{3}=4\\), por eso es una fracción aparente.",
                "fact": "Toda fracción aparente puede simplificarse hasta obtener un entero.",
            }
        if concept == "NUMERO_MIXTO_CONCEPTO":
            return {
                "definition": "un número mixto combina una parte entera y una fracción propia",
                "example": "\\(2\\frac{1}{3}\\) representa 2 enteros y un tercio adicional.",
                "fact": "Un número mixto es otra forma de escribir una fracción impropia positiva.",
            }
        if concept == "FRACCION_NO_DEFINIDA":
            return {
                "definition": "una fracción con denominador cero no está definida como número",
                "example": "\\(\\frac{7}{0}\\) no está definida.",
                "fact": "Dividir por cero no produce un número racional.",
            }
        if concept == "FORMA_INDETERMINADA_CERO_SOBRE_CERO":
            return {
                "definition": "la expresión \\(\\frac{0}{0}\\) es indeterminada porque no permite asignar un único valor numérico",
                "example": "\\(\\frac{0}{0}\\) no puede clasificarse como número racional.",
                "fact": "La forma \\(\\frac{0}{0}\\) es un caso especial distinto de una fracción no definida cualquiera.",
            }

    if subtheme == "FRACCIONES_EQUIVALENCIA":
        if concept == "FRACCIONES_EQUIVALENTES_CONCEPTO":
            return {
                "definition": "dos fracciones son equivalentes si representan la misma cantidad aunque tengan numerador y denominador distintos",
                "example": "\\(\\frac{1}{2}=\\frac{2}{4}=\\frac{3}{6}\\).",
                "fact": "Las fracciones equivalentes ocupan el mismo punto en la recta numérica.",
            }
        if concept == "AMPLIFICACION":
            return {
                "definition": "amplificar una fracción consiste en multiplicar numerador y denominador por el mismo número distinto de cero",
                "example": "Al amplificar \\(\\frac{2}{3}\\) por 4 se obtiene \\(\\frac{8}{12}\\).",
                "fact": "La amplificación conserva el valor de la fracción.",
            }
        if concept == "SIMPLIFICACION":
            return {
                "definition": "simplificar una fracción consiste en dividir numerador y denominador por un mismo divisor común distinto de cero",
                "example": "Al simplificar \\(\\frac{18}{24}\\) por 6 se obtiene \\(\\frac{3}{4}\\).",
                "fact": "La simplificación conserva el valor de la fracción y la escribe de forma más simple.",
            }
        if concept == "FRACCION_IRREDUCTIBLE":
            return {
                "definition": "una fracción irreductible es una fracción que ya no puede simplificarse porque su numerador y su denominador son coprimos",
                "example": "\\(\\frac{5}{8}\\) es irreductible porque 5 y 8 no tienen divisores comunes mayores que 1.",
                "fact": "Toda fracción racional puede escribirse en forma irreductible.",
            }
        if concept == "PRODUCTOS_CRUZADOS":
            return {
                "definition": "para verificar equivalencia entre \\(\\frac{a}{b}\\) y \\(\\frac{c}{d}\\), se comparan los productos cruzados \\(a\\cdot d\\) y \\(b\\cdot c\\)",
                "example": "\\(\\frac{2}{3}\\) y \\(\\frac{4}{6}\\) son equivalentes porque \\(2\\cdot 6 = 3\\cdot 4\\).",
                "fact": "Los productos cruzados iguales indican fracciones equivalentes, siempre que los denominadores no sean cero.",
            }
        if concept == "MIXTO_A_IMPROPIA":
            return {
                "definition": "para convertir un número mixto a fracción impropia se multiplica la parte entera por el denominador y luego se suma el numerador",
                "example": "\\(2\\frac{3}{5}=\\frac{2\\cdot 5 + 3}{5}=\\frac{13}{5}\\).",
                "fact": "En un número mixto el denominador se conserva al pasar a fracción impropia.",
            }
        if concept == "IMPROPIA_A_MIXTO":
            return {
                "definition": "para convertir una fracción impropia a número mixto se divide el numerador por el denominador y se usa el resto como numerador de la parte fraccionaria",
                "example": "\\(\\frac{17}{4}=4\\frac{1}{4}\\).",
                "fact": "La parte fraccionaria del número mixto debe quedar como fracción propia.",
            }

    if subtheme == "FRACCIONES_COMPARACION":
        if concept == "IGUAL_DENOMINADOR":
            return {
                "definition": "si dos fracciones tienen igual denominador, es mayor la que tiene mayor numerador",
                "example": "Entre \\(\\frac{5}{9}\\) y \\(\\frac{3}{9}\\), la mayor es \\(\\frac{5}{9}\\).",
                "fact": "Con denominadores iguales, las partes comparadas tienen el mismo tamaño.",
            }
        if concept == "IGUAL_NUMERADOR":
            return {
                "definition": "si dos fracciones positivas tienen igual numerador, es mayor la que tiene menor denominador",
                "example": "Entre \\(\\frac{3}{4}\\) y \\(\\frac{3}{7}\\), la mayor es \\(\\frac{3}{4}\\).",
                "fact": "Con el mismo número de partes tomadas, conviene mirar el tamaño de cada parte.",
            }
        if concept == "DISTINTO_DENOMINADOR":
            return {
                "definition": "para comparar fracciones con distinto denominador suele buscarse un denominador común o una representación equivalente",
                "example": "Para comparar \\(\\frac{2}{3}\\) y \\(\\frac{3}{5}\\), se puede llevar ambas a quinceavos.",
                "fact": "Usar fracciones equivalentes facilita comparar cantidades escritas de forma distinta.",
            }
        if concept == "PRODUCTO_CRUZADO":
            return {
                "definition": "el producto cruzado permite comparar dos fracciones sin calcular decimales, multiplicando cada numerador por el denominador opuesto",
                "example": "Para comparar \\(\\frac{4}{7}\\) y \\(\\frac{5}{9}\\), se comparan \\(4\\cdot 9\\) y \\(5\\cdot 7\\).",
                "fact": "Si \\(a\\cdot d > b\\cdot c\\), entonces \\(\\frac{a}{b} > \\frac{c}{d}\\) con denominadores positivos.",
            }
        if concept == "UBICACION_RECTA":
            return {
                "definition": "ubicar una fracción en la recta numérica consiste en localizar el punto que representa su valor",
                "example": "\\(\\frac{3}{4}\\) se ubica entre 0 y 1, más cerca de 1 que de 0.",
                "fact": "La recta numérica permite comparar fracciones visualmente por su posición.",
            }
        if concept == "DENSIDAD_Q":
            return {
                "definition": "la densidad de \\(\\mathbb{Q}\\) significa que entre dos números racionales distintos siempre existe otro número racional",
                "example": "Entre \\(\\frac{1}{2}\\) y \\(\\frac{3}{4}\\) está \\(\\frac{5}{8}\\).",
                "fact": "No existen racionales consecutivos en la recta numérica.",
            }

    if subtheme == "FRACCIONES_OPERATORIA":
        if concept == "ADICION_IGUAL_DENOMINADOR":
            return {
                "definition": "para sumar fracciones de igual denominador se suman los numeradores y se conserva el denominador",
                "example": "\\(\\frac{2}{7}+\\frac{3}{7}=\\frac{5}{7}\\).",
                "fact": "El denominador común indica el tamaño de las partes y no cambia en esta suma.",
            }
        if concept == "SUSTRACCION_IGUAL_DENOMINADOR":
            return {
                "definition": "para restar fracciones de igual denominador se restan los numeradores y se conserva el denominador",
                "example": "\\(\\frac{6}{9}-\\frac{2}{9}=\\frac{4}{9}\\).",
                "fact": "En una resta con igual denominador solo cambia la cantidad de partes tomadas.",
            }
        if concept == "ADICION_DISTINTO_DENOMINADOR":
            return {
                "definition": "para sumar fracciones de distinto denominador primero se buscan fracciones equivalentes con denominador común",
                "example": "\\(\\frac{1}{2}+\\frac{1}{3}=\\frac{3}{6}+\\frac{2}{6}=\\frac{5}{6}\\).",
                "fact": "No se pueden sumar directamente los denominadores.",
            }
        if concept == "SUSTRACCION_DISTINTO_DENOMINADOR":
            return {
                "definition": "para restar fracciones de distinto denominador primero se expresan con un denominador común",
                "example": "\\(\\frac{5}{6}-\\frac{1}{4}=\\frac{10}{12}-\\frac{3}{12}=\\frac{7}{12}\\).",
                "fact": "Buscar un m.c.m. suele hacer más eficiente la operación.",
            }
        if concept == "MULTIPLICACION":
            return {
                "definition": "para multiplicar fracciones se multiplican numeradores entre sí y denominadores entre sí",
                "example": "\\(\\frac{2}{3}\\cdot\\frac{5}{4}=\\frac{10}{12}=\\frac{5}{6}\\).",
                "fact": "Conviene simplificar antes o después de multiplicar para obtener una fracción más simple.",
            }
        if concept == "INVERSO_MULTIPLICATIVO":
            return {
                "definition": "el inverso multiplicativo de una fracción no nula se obtiene invirtiendo numerador y denominador",
                "example": "El inverso de \\(\\frac{3}{8}\\) es \\(\\frac{8}{3}\\).",
                "fact": "Al multiplicar una fracción no nula por su inverso multiplicativo se obtiene 1.",
            }
        if concept == "DIVISION":
            return {
                "definition": "dividir por una fracción equivale a multiplicar por su recíproco",
                "example": "\\(\\frac{2}{5}\\div\\frac{3}{4}=\\frac{2}{5}\\cdot\\frac{4}{3}=\\frac{8}{15}\\).",
                "fact": "El divisor debe ser distinto de cero para que la división exista.",
            }
        if concept == "OPERATORIA_CON_MIXTOS":
            return {
                "definition": "para operar con números mixtos suele convenir convertirlos primero a fracciones impropias",
                "example": "Para sumar \\(1\\frac{1}{2}+2\\frac{1}{3}\\) se convierten en \\(\\frac{3}{2}\\) y \\(\\frac{7}{3}\\).",
                "fact": "Trabajar con una sola representación reduce errores de cálculo.",
            }
        if concept == "JERARQUIA_OPERACIONES":
            return {
                "definition": "en expresiones con fracciones se respeta la jerarquía usual: paréntesis, multiplicaciones y divisiones, luego sumas y restas",
                "example": "En \\(\\frac{1}{2}+\\frac{3}{4}\\cdot\\frac{2}{3}\\), primero se calcula el producto.",
                "fact": "La jerarquía evita resultados distintos para una misma expresión.",
            }
        if concept == "FRACCION_DE_CANTIDAD":
            return {
                "definition": "calcular la fracción de una cantidad significa multiplicar la cantidad total por la fracción correspondiente",
                "example": "\\(\\frac{3}{5}\\) de 20 es \\(20\\cdot\\frac{3}{5}=12\\).",
                "fact": "Una fracción de cantidad representa una parte proporcional del total.",
            }

    if subtheme == "RACIONALES_PROPIEDADES":
        table = {
            "CLAUSURA_ADICION": (
                "la clausura de \\(\\mathbb{Q}\\) en la adición afirma que la suma de dos racionales siempre es racional",
                "Si \\(\\frac{1}{3}\\) y \\(\\frac{2}{5}\\) son racionales, entonces \\(\\frac{1}{3}+\\frac{2}{5}=\\frac{11}{15}\\) también es racional.",
                "La operación no saca el resultado fuera del conjunto de los racionales.",
            ),
            "CLAUSURA_MULTIPLICACION": (
                "la clausura de \\(\\mathbb{Q}\\) en la multiplicación afirma que el producto de dos racionales siempre es racional",
                "Si \\(\\frac{3}{4}\\) y \\(-\\frac{2}{7}\\) son racionales, entonces su producto también lo es.",
                "La multiplicación conserva pertenencia al conjunto de los racionales.",
            ),
            "CONMUTATIVA_ADICION": (
                "la propiedad conmutativa de la adición establece que cambiar el orden de los sumandos no altera la suma",
                "\\(\\frac{1}{2}+\\frac{3}{7}=\\frac{3}{7}+\\frac{1}{2}\\).",
                "En una suma de racionales el orden no cambia el resultado.",
            ),
            "CONMUTATIVA_MULTIPLICACION": (
                "la propiedad conmutativa de la multiplicación establece que cambiar el orden de los factores no altera el producto",
                "\\(\\frac{2}{3}\\cdot\\frac{5}{4}=\\frac{5}{4}\\cdot\\frac{2}{3}\\).",
                "En una multiplicación de racionales el orden no cambia el resultado.",
            ),
            "ASOCIATIVA_ADICION": (
                "la propiedad asociativa de la adición permite agrupar sumandos de distintas maneras sin cambiar la suma",
                "\\((\\frac{1}{2}+\\frac{1}{3})+\\frac{1}{6}=\\frac{1}{2}+(\\frac{1}{3}+\\frac{1}{6})\\).",
                "Al sumar racionales, cambiar la agrupación no cambia el resultado.",
            ),
            "ASOCIATIVA_MULTIPLICACION": (
                "la propiedad asociativa de la multiplicación permite agrupar factores de distintas maneras sin cambiar el producto",
                "\\((\\frac{2}{3}\\cdot\\frac{3}{5})\\cdot\\frac{5}{2}=\\frac{2}{3}\\cdot(\\frac{3}{5}\\cdot\\frac{5}{2})\\).",
                "Al multiplicar racionales, cambiar la agrupación no cambia el resultado.",
            ),
            "NEUTRO_ADITIVO": (
                "el neutro aditivo en \\(\\mathbb{Q}\\) es 0 porque sumar 0 no cambia el número",
                "\\(\\frac{5}{8}+0=\\frac{5}{8}\\).",
                "El cero conserva cualquier racional al sumarse con él.",
            ),
            "NEUTRO_MULTIPLICATIVO": (
                "el neutro multiplicativo en \\(\\mathbb{Q}\\) es 1 porque multiplicar por 1 no cambia el número",
                "\\(-\\frac{4}{9}\\cdot 1=-\\frac{4}{9}\\).",
                "El uno conserva cualquier racional al multiplicarse con él.",
            ),
            "INVERSO_ADITIVO": (
                "el inverso aditivo de un racional es el número que sumado con él produce 0",
                "El inverso aditivo de \\(\\frac{3}{5}\\) es \\(-\\frac{3}{5}\\).",
                "Todo racional tiene inverso aditivo y ambos suman cero.",
            ),
            "INVERSO_MULTIPLICATIVO": (
                "el inverso multiplicativo de un racional no nulo es el número que multiplicado por él produce 1",
                "El inverso multiplicativo de \\(-\\frac{7}{3}\\) es \\(-\\frac{3}{7}\\).",
                "Solo el cero no tiene inverso multiplicativo.",
            ),
            "DISTRIBUTIVA_SUMA": (
                "la distributiva respecto de la suma permite multiplicar un factor común por cada sumando",
                "\\(\\frac{2}{3}(\\frac{1}{4}+\\frac{5}{4})=\\frac{2}{3}\\cdot\\frac{1}{4}+\\frac{2}{3}\\cdot\\frac{5}{4}\\).",
                "Multiplicar una suma puede hacerse repartiendo el factor común.",
            ),
            "DISTRIBUTIVA_RESTA": (
                "la distributiva respecto de la resta permite multiplicar un factor común por el minuendo y por el sustraendo",
                "\\(\\frac{3}{5}(\\frac{7}{2}-\\frac{1}{2})=\\frac{3}{5}\\cdot\\frac{7}{2}-\\frac{3}{5}\\cdot\\frac{1}{2}\\).",
                "La distributiva también funciona cuando dentro del paréntesis hay una resta.",
            ),
        }
        definition, example, fact = table[concept]
        return {"definition": definition, "example": example, "fact": fact}

    if subtheme == "DECIMALES_CLASIFICACION":
        table = {
            "DECIMAL_FINITO": (
                "un decimal finito tiene una cantidad limitada de cifras decimales",
                "\\(0.75\\) es decimal finito porque sus cifras después de la coma terminan.",
                "Todo decimal finito puede escribirse como fracción con denominador potencia de 10.",
            ),
            "DECIMAL_PERIODICO": (
                "un decimal periódico infinito repite un bloque de cifras llamado período desde la primera cifra decimal o después de un anteperíodo",
                "\\(0.\\overline{3}\\) es un decimal periódico.",
                "El período es el bloque que se repite indefinidamente.",
            ),
            "DECIMAL_SEMIPERIODICO": (
                "un decimal semiperiódico tiene primero cifras no repetidas y luego un período que se repite indefinidamente",
                "\\(1.2\\overline{7}\\) es semiperiódico porque antes del período aparece un anteperíodo.",
                "En un decimal semiperiódico conviven anteperíodo y período.",
            ),
            "PERIODO_IDENTIFICACION": (
                "el período es el bloque mínimo de cifras que se repite indefinidamente en un decimal periódico",
                "En \\(0.\\overline{27}\\), el período es 27.",
                "Para identificar el período hay que ubicar la parte que se repite una y otra vez.",
            ),
            "ANTEPERIODO_IDENTIFICACION": (
                "el anteperíodo es el conjunto de cifras decimales que aparece antes de que empiece la repetición",
                "En \\(0.16\\overline{4}\\), el anteperíodo es 16.",
                "Solo los decimales semiperiódicos tienen anteperíodo.",
            ),
        }
        definition, example, fact = table[concept]
        return {"definition": definition, "example": example, "fact": fact}

    if subtheme == "DECIMALES_OPERATORIA":
        table = {
            "ADICION": (
                "para sumar decimales se alinean las comas y se suman cifras del mismo valor posicional",
                "\\(3.45 + 0.8 = 3.45 + 0.80 = 4.25\\).",
                "Alinear la coma mantiene unidades, décimas y centésimas en su lugar correcto.",
            ),
            "SUSTRACCION": (
                "para restar decimales se alinean las comas y se restan cifras del mismo valor posicional",
                "\\(5.20 - 1.37 = 3.83\\).",
                "Completar con ceros puede ayudar a ordenar la sustracción.",
            ),
            "MULTIPLICACION": (
                "para multiplicar decimales se multiplican como enteros y luego se ubica la coma según el total de cifras decimales",
                "\\(1.2\\cdot 0.4 = 0.48\\).",
                "La cantidad de cifras decimales del producto es la suma de las cifras decimales de los factores.",
            ),
            "DIVISION_POR_NATURAL": (
                "al dividir un decimal por un número natural se conserva la coma y se continúa la división cifra a cifra",
                "\\(4.8 \\div 3 = 1.6\\).",
                "La división por natural mantiene el valor posicional si se baja la coma en el momento adecuado.",
            ),
            "DIVISION_POR_DECIMAL": (
                "para dividir por un decimal se amplifican dividendo y divisor por una potencia de 10 hasta que el divisor sea natural",
                "\\(3.6 \\div 0.4 = 36 \\div 4 = 9\\).",
                "Multiplicar ambos términos por la misma potencia de 10 no cambia el cociente.",
            ),
        }
        definition, example, fact = table[concept]
        return {"definition": definition, "example": example, "fact": fact}

    if subtheme == "FRACCION_DECIMAL":
        table = {
            "CONVERSION_DIVISION": (
                "una fracción puede convertirse a decimal efectuando la división del numerador entre el denominador",
                "\\(\\frac{3}{8}=3\\div 8 = 0.375\\).",
                "La escritura decimal de una fracción se obtiene con la división asociada.",
            ),
            "DENOMINADOR_POTENCIA_DIEZ": (
                "si una fracción tiene denominador potencia de 10, su forma decimal se lee directamente por valor posicional",
                "\\(\\frac{47}{100}=0.47\\).",
                "Los denominadores 10, 100 y 1000 facilitan la lectura decimal.",
            ),
            "DETECCION_DECIMAL_FINITO": (
                "una fracción irreductible produce decimal finito cuando su denominador solo tiene factores primos 2 y/o 5",
                "\\(\\frac{3}{20}\\) da decimal finito porque \\(20=2^2\\cdot 5\\).",
                "Los factores 2 y 5 son los que aparecen en las potencias de 10.",
            ),
            "DETECCION_DECIMAL_PERIODICO": (
                "una fracción irreductible produce decimal periódico cuando su denominador tiene factores primos distintos de 2 y 5",
                "\\(\\frac{1}{3}\\) da decimal periódico porque 3 no divide ninguna potencia de 10.",
                "La presencia de otros factores primos impide obtener un decimal finito.",
            ),
        }
        definition, example, fact = table[concept]
        return {"definition": definition, "example": example, "fact": fact}

    if subtheme == "DECIMAL_FRACCION":
        table = {
            "FINITO": (
                "un decimal finito se convierte a fracción escribiéndolo sobre una potencia de 10 y simplificando si es posible",
                "\\(0.125 = \\frac{125}{1000} = \\frac{1}{8}\\).",
                "La cantidad de cifras decimales indica qué potencia de 10 usar en el denominador.",
            ),
            "PERIODICO": (
                "un decimal periódico puro puede convertirse a fracción usando una igualdad algebraica y restando el período",
                "Si \\(x=0.\\overline{3}\\), entonces \\(10x-x=3\\) y \\(x=\\frac{1}{3}\\).",
                "La repetición del período permite eliminar la parte decimal mediante una resta.",
            ),
            "SEMIPERIODICO": (
                "un decimal semiperiódico se convierte a fracción aislando el anteperíodo y el período con potencias de 10 adecuadas",
                "Si \\(x=0.1\\overline{6}\\), se usan \\(10x\\) y \\(100x\\) para cancelar la repetición y hallar la fracción.",
                "En un semiperiódico hay que considerar por separado anteperíodo y período.",
            ),
        }
        definition, example, fact = table[concept]
        return {"definition": definition, "example": example, "fact": fact}

    if subtheme == "APROXIMACIONES":
        table = {
            "APROXIMACION_DEFECTO": (
                "una aproximación por defecto es un valor menor o igual que el número original",
                "Aproximar por defecto \\(5.78\\) a la décima da \\(5.7\\).",
                "La aproximación por defecto nunca supera el valor original.",
            ),
            "APROXIMACION_EXCESO": (
                "una aproximación por exceso es un valor mayor o igual que el número original",
                "Aproximar por exceso \\(5.72\\) a la décima da \\(5.8\\).",
                "La aproximación por exceso nunca queda por debajo del valor original.",
            ),
            "REDONDEO": (
                "redondear consiste en reemplazar un número por otro cercano según una cifra de referencia",
                "Redondear \\(12.46\\) a la décima da \\(12.5\\).",
                "El redondeo busca un valor cercano y fácil de usar conservando una precisión dada.",
            ),
            "REGLA_DEL_CINCO": (
                "la regla del cinco indica que si la cifra siguiente es 5 o mayor se aumenta en una unidad la cifra que se conserva",
                "Al redondear \\(8.267\\) a la centésima, como la milésima es 7, resulta \\(8.27\\).",
                "Si la cifra siguiente es menor que 5, la cifra conservada se mantiene.",
            ),
            "TRUNCAMIENTO": (
                "truncar un número significa cortar las cifras a partir de cierto orden sin redondear",
                "Truncar \\(4.987\\) a la décima produce \\(4.9\\).",
                "El truncamiento no mira la cifra siguiente; simplemente elimina las restantes.",
            ),
        }
        definition, example, fact = table[concept]
        return {"definition": definition, "example": example, "fact": fact}

    if subtheme == "ERROR_NUMERICO":
        table = {
            "ERROR_ABSOLUTO": (
                "el error absoluto es la diferencia en valor absoluto entre el valor exacto y el valor aproximado",
                "Si el valor exacto es 10 y el aproximado es 9.7, el error absoluto es \\(|10-9.7|=0.3\\).",
                "El error absoluto mide cuánto se aleja la aproximación del valor real.",
            ),
            "ERROR_RELATIVO": (
                "el error relativo compara el error absoluto con el tamaño del valor exacto",
                "Si el error absoluto es 0.3 y el valor exacto es 10, el error relativo es \\(0.3/10=0.03\\).",
                "El error relativo permite evaluar la magnitud del error en proporción al valor exacto.",
            ),
            "ERROR_PORCENTUAL": (
                "el error porcentual es el error relativo expresado en porcentaje",
                "Si el error relativo es 0.03, el error porcentual es \\(3\\%\\).",
                "Multiplicar el error relativo por 100 permite interpretarlo como porcentaje.",
            ),
        }
        definition, example, fact = table[concept]
        return {"definition": definition, "example": example, "fact": fact}

    raise KeyError(f"Sin meta para {semantic_id} ({name})")


def source_for(subtheme: str) -> str:
    if subtheme in {
        "RACIONALES_CONCEPTO",
        "FRACCIONES_CONCEPTO",
        "FRACCIONES_CLASIFICACION",
        "FRACCIONES_EQUIVALENCIA",
        "FRACCIONES_COMPARACION",
        "FRACCIONES_OPERATORIA",
        "RACIONALES_PROPIEDADES",
    }:
        return "Texto escolar MINEDUC — Matemática 7° Básico, unidad de fracciones y números racionales."
    if subtheme in {
        "DECIMALES_CLASIFICACION",
        "DECIMALES_OPERATORIA",
        "FRACCION_DECIMAL",
        "DECIMAL_FRACCION",
        "APROXIMACIONES",
        "ERROR_NUMERICO",
    }:
        return "Texto escolar MINEDUC — Matemática 7°-8° Básico, decimales, aproximaciones y error."
    return "Apunte escolar de números racionales."


def procedure_for(subtheme: str, title: str) -> list[str]:
    if subtheme in {"RACIONALES_CONCEPTO", "FRACCIONES_CONCEPTO"}:
        return [
            "Paso 1: Identificar qué representa el número o la fracción en la situación.",
            "Paso 2: Revisar la definición formal del concepto y sus condiciones.",
            f"Paso 3: Concluir si el ejemplo sí corresponde a {title.lower()} y justificarlo.",
        ]
    if subtheme == "FRACCIONES_CLASIFICACION":
        return [
            "Paso 1: Observar numerador y denominador, y verificar si el denominador es distinto de cero.",
            "Paso 2: Comparar numerador y denominador o transformar la fracción si hace falta.",
            f"Paso 3: Clasificar la expresión según la definición de {title.lower()}.",
        ]
    if subtheme in {"FRACCIONES_EQUIVALENCIA", "FRACCIONES_COMPARACION"}:
        return [
            "Paso 1: Elegir una estrategia conveniente: simplificar, amplificar, usar productos cruzados o un denominador común.",
            "Paso 2: Ejecutar la comparación o transformación paso a paso, cuidando el valor de la fracción.",
            "Paso 3: Interpretar el resultado y expresarlo con lenguaje matemático claro.",
        ]
    if subtheme in {"FRACCIONES_OPERATORIA", "DECIMALES_OPERATORIA"}:
        return [
            "Paso 1: Identificar la operación y preparar una representación adecuada de los datos.",
            "Paso 2: Aplicar la regla específica de la operación respetando valor posicional o denominadores.",
            "Paso 3: Simplificar o verificar el resultado final según corresponda.",
        ]
    if subtheme == "RACIONALES_PROPIEDADES":
        return [
            "Paso 1: Escribir ambos lados de la propiedad con números racionales simples.",
            "Paso 2: Calcular cada lado por separado respetando el orden de las operaciones.",
            "Paso 3: Comparar los resultados y concluir si la propiedad se cumple.",
        ]
    if subtheme == "DECIMALES_CLASIFICACION":
        return [
            "Paso 1: Observar si la escritura decimal termina o continúa indefinidamente.",
            "Paso 2: Si continúa, identificar si existe un período y si aparece un anteperíodo.",
            "Paso 3: Clasificar el decimal usando la definición correspondiente.",
        ]
    if subtheme == "FRACCION_DECIMAL":
        return [
            "Paso 1: Simplificar la fracción si es necesario para analizarla mejor.",
            "Paso 2: Convertir mediante división o estudiar el denominador en forma irreductible.",
            "Paso 3: Decidir si la expresión decimal es finita o periódica y justificarlo.",
        ]
    if subtheme == "DECIMAL_FRACCION":
        return [
            "Paso 1: Identificar si el decimal es finito, periódico o semiperiódico.",
            "Paso 2: Aplicar el método de conversión adecuado según el tipo de decimal.",
            "Paso 3: Simplificar la fracción obtenida y verificar que represente el mismo valor.",
        ]
    if subtheme == "APROXIMACIONES":
        return [
            "Paso 1: Identificar el orden al que se quiere aproximar el número.",
            "Paso 2: Mirar la cifra relevante y aplicar defecto, exceso, redondeo o truncamiento según corresponda.",
            "Paso 3: Escribir la aproximación y comprobar si cumple la condición pedida.",
        ]
    if subtheme == "ERROR_NUMERICO":
        return [
            "Paso 1: Distinguir el valor exacto del valor aproximado.",
            "Paso 2: Calcular primero el error absoluto y luego, si se requiere, el relativo o porcentual.",
            "Paso 3: Interpretar el resultado indicando cuán precisa es la aproximación.",
        ]
    return [
        "Paso 1: Identificar los datos relevantes.",
        "Paso 2: Aplicar la definición o regla correspondiente.",
        "Paso 3: Verificar el resultado.",
    ]


def _without_trailing_period(text: str) -> str:
    return text.strip().rstrip(".")


def _without_example_prefix(text: str) -> str:
    clean = _without_trailing_period(text)
    for prefix in ("Por ejemplo, ", "Por ejemplo: "):
        if clean.startswith(prefix):
            return clean[len(prefix) :]
    return clean


def _upper_initial(text: str) -> str:
    return text[:1].upper() + text[1:]


def _variant(semantic_id: str, salt: str, options: list[str]) -> str:
    digest = hashlib.sha1(f"{semantic_id}:{salt}".encode("utf-8")).hexdigest()
    return options[int(digest, 16) % len(options)]


def _objective_for(semantic_id: str, title: str, goal: str, fact: str) -> str:
    return _upper_initial(goal).rstrip(".") + "."


def _examples_for(
    semantic_id: str,
    title: str,
    definition: str,
    example: str,
    fact: str,
    prepare: str,
    execute: str,
    verify: str,
) -> list[dict]:
    lower_title = title[:1].lower() + title[1:]
    prepare_text = prepare.rstrip(".")
    verify_text = verify.rstrip(".")
    return [
        {
            "titulo": f"Aplicación razonada — {title}",
            "enunciado": _upper_initial(example).rstrip(".") + ".",
            "solucion_pasos": [prepare, execute, verify],
        },
        {
            "titulo": f"Revisión de una solución — {title}",
            "enunciado": f"Una solución aplica “{execute}”, pero termina sin comprobar que {fact[0].lower() + fact[1:]}. Determina qué falta justificar.",
            "solucion_pasos": [
                f"Vuelve a la condición que define {lower_title}: {definition}.",
                prepare,
                f"Completa la revisión con este control: {verify}",
            ],
        },
        {
            "titulo": f"¿Se cumple que {fact[0].lower() + fact[1:]}? — {title}",
            "respuesta": "Sí",
            "solucion_pasos": [
                f"Sí. La definición pertinente establece que {definition}.",
                f"El caso “{example}” satisface esa condición.",
                verify,
            ],
        },
        {
            "titulo": f"¿Es válido omitir el paso “{prepare_text}”? — {title}",
            "respuesta": "No",
            "solucion_pasos": [
                f"No. Ese paso comprueba una condición necesaria de {lower_title}.",
                f"Omitirlo puede volver inválida la acción siguiente: {execute}",
                f"La solución debe terminar de este modo: {verify_text}.",
            ],
        },
    ]


def _resource_plan(semantic_id: str) -> tuple[str, str, str, str]:
    concept = semantic_id.split(".")[3]
    plans = {
        "DEFINICION_Q": ("decidir si un número pertenece a \(\mathbb{Q}\)", "Escribe el número como un cociente \(a/b\) de enteros.", "Comprueba que el denominador elegido sea distinto de cero.", "Concluye si la representación cumple completa la definición de racional."),
        "CONDICION_DENOMINADOR_NO_CERO": ("detectar cuándo una expresión fraccionaria no está definida", "Localiza el denominador antes de efectuar cualquier cálculo.", "Si el denominador vale cero, detén la operación: la división no existe.", "Distingue una expresión no definida de un número racional válido."),
        "ENTEROS_COMO_RACIONALES": ("representar cualquier entero como número racional", "Toma el entero que quieres expresar como fracción.", "Colócalo como numerador y usa \(1\) como denominador.", "Divide para comprobar que \(n/1=n\) y que el valor no cambió."),
        "SIGNO_RACIONAL": ("determinar el signo de una fracción", "Identifica por separado el signo del numerador y el del denominador.", "Combina los signos: iguales producen positivo y distintos producen negativo.", "Normaliza la escritura dejando, de preferencia, el signo menos en el numerador."),
        "FRACCION_PARTE_TODO": ("interpretar una fracción como partes iguales de una unidad", "Verifica que el entero esté dividido en partes del mismo tamaño.", "Cuenta cuántas partes iguales hay en total y cuántas se consideran.", "Escribe consideradas/total y explica a qué unidad se refiere la fracción."),
        "NUMERADOR_IDENTIFICACION": ("identificar e interpretar el numerador", "Ubica el número escrito sobre la barra de fracción.", "Relaciona ese número con las partes tomadas o consideradas.", "Comprueba que tu interpretación use como referencia el total indicado por el denominador."),
        "DENOMINADOR_IDENTIFICACION": ("identificar e interpretar el denominador", "Ubica el número escrito bajo la barra y verifica que no sea cero.", "Interprétalo como la cantidad de partes iguales en que se divide la unidad.", "Comprueba que el tamaño de cada parte sea \(1/b\) de la unidad."),
        "UNIDAD_FRACCIONARIA": ("reconocer la unidad fraccionaria asociada a una partición", "Determina en cuántas partes iguales se dividió el entero.", "Escribe una sola de esas partes como \(1/b\).", "Verifica que reunir \(b\) unidades fraccionarias reconstruya el entero."),
        "FRACCION_PROPIA": ("reconocer una fracción propia", "Comprueba que numerador y denominador sean naturales y que el denominador no sea cero.", "Compara ambos términos y verifica que el numerador sea menor.", "Confirma que el valor obtenido quede entre \(0\) y \(1\)."),
        "FRACCION_IMPROPIA": ("reconocer una fracción impropia", "Verifica primero que la expresión esté definida.", "Compara numerador y denominador y comprueba que el numerador sea mayor.", "Divide para confirmar que el valor de la fracción sea mayor que \(1\)."),
        "FRACCION_APARENTE": ("reconocer una fracción aparente", "Revisa que el denominador sea distinto de cero.", "Comprueba si el numerador es múltiplo del denominador.", "Efectúa la división exacta para obtener el entero representado."),
        "NUMERO_MIXTO_CONCEPTO": ("interpretar un número mixto", "Separa la parte entera de la parte fraccionaria propia.", "Interpreta el número como la suma de ambas partes.", "Convierte a impropia cuando necesites verificar o efectuar operaciones."),
        "FRACCION_NO_DEFINIDA": ("reconocer una fracción no definida", "Inspecciona el denominador de la expresión.", "Si es cero y el numerador no lo es, reconoce que no existe cociente posible.", "No asignes infinito ni ningún valor numérico a la expresión."),
        "FORMA_INDETERMINADA_CERO_SOBRE_CERO": ("distinguir la forma indeterminada \(0/0\)", "Comprueba que numerador y denominador sean simultáneamente cero.", "Reconoce que cualquier número multiplicado por cero produce cero, por lo que no hay cociente único.", "Clasifica \(0/0\) como indeterminada y no como una fracción de valor cero."),
        "FRACCIONES_EQUIVALENTES_CONCEPTO": ("decidir si dos fracciones son equivalentes", "Simplifica ambas fracciones o busca una transformación común.", "Compara sus productos cruzados sin alterar los signos.", "Declara equivalencia solo si representan exactamente el mismo valor."),
        "AMPLIFICACION": ("amplificar una fracción conservando su valor", "Elige un entero no nulo como factor de amplificación.", "Multiplica por ese mismo factor el numerador y el denominador.", "Simplifica de vuelta o divide para comprobar que el valor inicial se conserva."),
        "SIMPLIFICACION": ("simplificar una fracción conservando su valor", "Busca un divisor común mayor que uno para numerador y denominador.", "Divide ambos términos por exactamente el mismo divisor no nulo.", "Verifica que la nueva fracción sea equivalente a la original."),
        "FRACCION_IRREDUCTIBLE": ("determinar si una fracción es irreductible", "Calcula o identifica el máximo común divisor del numerador y el denominador.", "Si el MCD es mayor que uno, divide ambos términos por él.", "Confirma que el MCD final sea \(1\) y que ya no exista simplificación entera."),
        "PRODUCTOS_CRUZADOS": ("verificar equivalencia mediante productos cruzados", "Escribe las fracciones como \(a/b\) y \(c/d\), con denominadores no nulos.", "Calcula \(a\cdot d\) y \(b\cdot c\).", "Concluye que son equivalentes únicamente cuando ambos productos coinciden."),
        "MIXTO_A_IMPROPIA": ("convertir un número mixto en fracción impropia", "Multiplica la parte entera por el denominador de la fracción.", "Suma el numerador y conserva el denominador original.", "Divide la impropia obtenida para comprobar que reproduce el número mixto."),
        "IMPROPIA_A_MIXTO": ("convertir una fracción impropia en número mixto", "Divide el numerador por el denominador.", "Usa el cociente como parte entera y el resto como nuevo numerador.", "Conserva el denominador y verifica que parte entera más fracción recupere la impropia."),
        "IGUAL_DENOMINADOR": ("comparar fracciones con igual denominador", "Comprueba que ambas fracciones tengan el mismo denominador positivo.", "Compara directamente sus numeradores.", "Escribe el orden de las fracciones con el símbolo correspondiente."),
        "IGUAL_NUMERADOR": ("comparar fracciones positivas con igual numerador", "Verifica que los numeradores coincidan y que las fracciones sean positivas.", "Compara los denominadores: más partes implican partes más pequeñas.", "Ordena de forma inversa a los denominadores y comprueba con un dibujo o decimal."),
        "DISTINTO_DENOMINADOR": ("comparar fracciones con denominadores distintos", "Busca un denominador común positivo o el mínimo común múltiplo.", "Amplifica cada fracción hasta obtener denominadores iguales.", "Compara los nuevos numeradores y traslada el orden a las fracciones originales."),
        "PRODUCTO_CRUZADO": ("comparar dos fracciones mediante producto cruzado", "Comprueba que los denominadores sean positivos; si no, normaliza los signos.", "Calcula los productos cruzados \(a\cdot d\) y \(c\cdot b\).", "Compara esos productos para establecer el orden entre \(a/b\) y \(c/d\)."),
        "UBICACION_RECTA": ("ubicar una fracción en la recta numérica", "Identifica los enteros consecutivos entre los que está la fracción.", "Divide la unidad del intervalo en tantas partes iguales como indique el denominador.", "Cuenta las partes desde cero y marca la posición indicada por el numerador."),
        "DENSIDAD_Q": ("encontrar un racional entre otros dos", "Ordena los dos racionales y verifica que sean distintos.", "Calcula su promedio \((a+b)/2\), que queda estrictamente entre ambos.", "Comprueba las dos desigualdades y reconoce que el proceso puede repetirse indefinidamente."),
        "ADICION_IGUAL_DENOMINADOR": ("sumar fracciones con igual denominador", "Comprueba que los denominadores sean iguales y distintos de cero.", "Suma los numeradores y conserva el denominador común.", "Simplifica la fracción resultante y estima si su tamaño es razonable."),
        "SUSTRACCION_IGUAL_DENOMINADOR": ("restar fracciones con igual denominador", "Verifica que ambas fracciones compartan un denominador no nulo.", "Resta los numeradores en el orden dado y conserva el denominador.", "Simplifica y revisa especialmente el signo del resultado."),
        "ADICION_DISTINTO_DENOMINADOR": ("sumar fracciones con denominadores distintos", "Calcula un denominador común, preferentemente el mínimo común múltiplo.", "Amplifica cada fracción y suma los numeradores equivalentes.", "Simplifica el resultado y comprueba la suma mediante una estimación."),
        "SUSTRACCION_DISTINTO_DENOMINADOR": ("restar fracciones con denominadores distintos", "Obtén un denominador común para ambas fracciones.", "Reescribe fracciones equivalentes y resta los numeradores respetando el orden.", "Simplifica y compara con una estimación para controlar el signo y la magnitud."),
        "MULTIPLICACION": ("multiplicar fracciones", "Revisa los signos y simplifica factores cruzados cuando sea posible.", "Multiplica numerador por numerador y denominador por denominador.", "Reduce la fracción final y verifica el signo del producto."),
        "INVERSO_MULTIPLICATIVO": ("obtener el inverso multiplicativo de un racional no nulo", "Comprueba que el racional sea distinto de cero.", "Intercambia numerador y denominador, conservando el signo.", "Multiplica el número por su recíproco y verifica que el producto sea \(1\)."),
        "DIVISION": ("dividir fracciones mediante el recíproco", "Comprueba que la fracción divisora sea distinta de cero.", "Conserva el dividendo, invierte el divisor y cambia división por multiplicación.", "Multiplica, simplifica y verifica el resultado con la operación inversa."),
        "OPERATORIA_CON_MIXTOS": ("operar números mixtos", "Convierte cada número mixto en fracción impropia antes de operar.", "Aplica la regla correspondiente de suma, resta, multiplicación o división.", "Simplifica y, si conviene, vuelve a número mixto para interpretar el resultado."),
        "JERARQUIA_OPERACIONES": ("resolver operaciones combinadas con fracciones", "Separa la expresión según paréntesis, multiplicaciones/divisiones y sumas/restas.", "Resuelve cada nivel de izquierda a derecha usando fracciones equivalentes cuando corresponda.", "Sustituye los resultados parciales y verifica que no hayas alterado el orden."),
        "FRACCION_DE_CANTIDAD": ("calcular una fracción de una cantidad", "Interpreta “\(a/b\) de \(N\)” como una multiplicación.", "Divide la cantidad en \(b\) partes y toma \(a\), o calcula \(N\cdot a/b\).", "Comprueba que la respuesta tenga la unidad del problema y una magnitud coherente."),
        "CLAUSURA_ADICION": ("verificar la clausura de \(\mathbb{Q}\) bajo la suma", "Elige dos racionales y escríbelos con denominador común.", "Súmalos para obtener una nueva fracción con denominador no nulo.", "Concluye que el resultado sigue perteneciendo a \(\mathbb{Q}\)."),
        "CLAUSURA_MULTIPLICACION": ("verificar la clausura de \(\mathbb{Q}\) bajo el producto", "Representa los dos racionales como fracciones de denominador no nulo.", "Multiplica numeradores y denominadores.", "Comprueba que el denominador del producto no sea cero y concluye que sigue siendo racional."),
        "CONMUTATIVA_ADICION": ("aplicar la conmutatividad de la suma racional", "Escribe una suma de dos racionales en el orden original.", "Intercambia únicamente el orden de los sumandos y calcula ambas expresiones.", "Verifica que los resultados coincidan: \(a+b=b+a\)."),
        "CONMUTATIVA_MULTIPLICACION": ("aplicar la conmutatividad del producto racional", "Escribe un producto de dos racionales.", "Cambia el orden de los factores sin modificar sus signos.", "Comprueba que ambos productos sean iguales: \(ab=ba\)."),
        "ASOCIATIVA_ADICION": ("reagrupar una suma de racionales", "Mantén el orden de tres sumandos y calcula primero los dos iniciales.", "Calcula luego agrupando los dos últimos.", "Compara \((a+b)+c\) con \(a+(b+c)\) y verifica la igualdad."),
        "ASOCIATIVA_MULTIPLICACION": ("reagrupar un producto de racionales", "Conserva el orden de tres factores y multiplica primero los dos iniciales.", "Repite agrupando los dos factores finales.", "Verifica que \((ab)c=a(bc)\) sin confundir reagrupar con reordenar."),
        "NEUTRO_ADITIVO": ("reconocer y usar el neutro aditivo", "Toma un racional cualquiera y súmale cero.", "Efectúa la suma escribiendo \(0\) con un denominador conveniente.", "Comprueba que el resultado sea el racional original."),
        "NEUTRO_MULTIPLICATIVO": ("reconocer y usar el neutro multiplicativo", "Toma un racional y multiplícalo por \(1\).", "Representa \(1\) como una fracción equivalente si facilita el cálculo.", "Comprueba que el producto conserve exactamente el racional inicial."),
        "INVERSO_ADITIVO": ("encontrar el inverso aditivo de un racional", "Copia el racional y cambia únicamente su signo.", "Suma ambos números usando un denominador común.", "Verifica que el resultado sea \(0\), el neutro aditivo."),
        "INVERSO_MULTIPLICATIVO": ("encontrar el inverso multiplicativo de un racional no nulo", "Comprueba que el racional no sea cero.", "Intercambia numerador y denominador conservando el signo global.", "Multiplica ambos números y verifica que el resultado sea \(1\)."),
        "DISTRIBUTIVA_SUMA": ("distribuir un factor sobre una suma", "Identifica el factor exterior y los dos sumandos interiores.", "Multiplica el factor por cada sumando y conserva el signo más.", "Compara \(a(b+c)\) con \(ab+ac\) mediante el cálculo de ambos lados."),
        "DISTRIBUTIVA_RESTA": ("distribuir un factor sobre una resta", "Identifica el factor exterior, el minuendo y el sustraendo.", "Multiplica el factor por ambos términos y conserva el signo menos entre productos.", "Verifica que \(a(b-c)=ab-ac\), cuidando especialmente los signos negativos."),
        "DECIMAL_FINITO": ("reconocer un decimal finito", "Observa si la escritura decimal termina después de una cantidad limitada de cifras.", "Cuenta las posiciones decimales y escríbelo sobre la potencia de diez correspondiente.", "Simplifica la fracción para confirmar que representa el mismo valor."),
        "DECIMAL_PERIODICO": ("reconocer un decimal periódico", "Observa la expansión después de la coma y busca un bloque que se repita desde el comienzo.", "Marca el bloque mínimo repetitivo como período.", "Comprueba que no haya cifras no repetitivas antes del período."),
        "DECIMAL_SEMIPERIODICO": ("reconocer un decimal semiperiódico", "Busca primero las cifras decimales que no se repiten.", "Identifica a continuación el bloque que se repite indefinidamente.", "Separa anteperíodo y período para justificar la clasificación."),
        "PERIODO_IDENTIFICACION": ("identificar el período de un decimal", "Descarta la parte entera y cualquier anteperíodo.", "Localiza el bloque mínimo de cifras que se repite sin fin.", "Comprueba que repetir solo ese bloque reconstruya la cola decimal."),
        "ANTEPERIODO_IDENTIFICACION": ("identificar el anteperíodo de un decimal", "Ubica las cifras posteriores a la coma que aparecen antes de la repetición.", "Detén el anteperíodo justo donde comienza el bloque periódico.", "Comprueba que esas cifras iniciales no vuelvan a repetirse como parte del período."),
        "ADICION": ("sumar números decimales", "Alinea los sumandos haciendo coincidir sus comas decimales.", "Completa con ceros si ayuda y suma columna por columna.", "Coloca la coma en la misma columna y estima para controlar el resultado."),
        "SUSTRACCION": ("restar números decimales", "Alinea minuendo y sustraendo por la coma y completa posiciones con ceros.", "Resta por columnas respetando los préstamos.", "Mantén la coma alineada y usa una estimación para revisar signo y magnitud."),
        "MULTIPLICACION": ("multiplicar números decimales", "Cuenta el total de cifras decimales de ambos factores.", "Multiplica temporalmente como si fueran enteros.", "Separa en el producto tantas cifras decimales como contaste y verifica con una estimación."),
        "DIVISION_POR_NATURAL": ("dividir un decimal por un número natural", "Plantea la división y avanza por las cifras del dividendo.", "Al cruzar la coma del dividendo, coloca la coma en el cociente.", "Multiplica cociente por divisor para comprobar que recuperas el dividendo."),
        "DIVISION_POR_DECIMAL": ("dividir por un número decimal", "Desplaza la coma del divisor hasta convertirlo en entero.", "Desplaza la coma del dividendo exactamente la misma cantidad de lugares.", "Divide la expresión equivalente y verifica multiplicando por el divisor original."),
        "CONVERSION_DIVISION": ("convertir una fracción en decimal mediante división", "Comprueba que el denominador sea distinto de cero.", "Divide el numerador por el denominador agregando ceros cuando sea necesario.", "Observa si el residuo llega a cero o comienza a repetirse."),
        "DENOMINADOR_POTENCIA_DIEZ": ("transformar una fracción a denominador potencia de diez", "Simplifica la fracción y factoriza su denominador.", "Busca el factor que completa \(10\), \(100\), \(1000\) u otra potencia de diez.", "Amplifica numerador y denominador por el mismo factor y lee el decimal resultante."),
        "DETECCION_DECIMAL_FINITO": ("predecir si una fracción produce decimal finito", "Reduce la fracción a su forma irreductible.", "Factoriza el denominador y comprueba que solo contenga factores \(2\) y/o \(5\).", "Concluye que la expansión termina y confirma mediante la división."),
        "DETECCION_DECIMAL_PERIODICO": ("predecir si una fracción produce decimal periódico", "Simplifica la fracción hasta hacerla irreductible.", "Factoriza el denominador y busca algún primo distinto de \(2\) y \(5\).", "Concluye que la expansión será periódica y comprueba el patrón por división."),
        "FINITO": ("convertir un decimal finito en fracción", "Elimina temporalmente la coma y usa las cifras como numerador.", "Pon como denominador una potencia de diez con tantos ceros como cifras decimales.", "Simplifica y divide para comprobar que recuperas el decimal original."),
        "PERIODICO": ("convertir un decimal periódico puro en fracción", "Llama \(x\) al decimal e identifica la longitud de su período.", "Multiplica por la potencia de diez que desplaza un período y resta la ecuación original.", "Despeja \(x\), simplifica la fracción y verifica su expansión decimal."),
        "SEMIPERIODICO": ("convertir un decimal semiperiódico en fracción", "Llama \(x\) al decimal y cuenta cifras de anteperíodo y período.", "Forma dos ecuaciones con potencias de diez que alineen la parte repetitiva y réstalas.", "Despeja, simplifica y comprueba que la fracción reproduce anteperíodo y período."),
        "APROXIMACION_DEFECTO": ("aproximar por defecto", "Elige el orden decimal solicitado y conserva las cifras anteriores.", "Descarta las cifras posteriores sin aumentar la última conservada.", "Comprueba que la aproximación sea menor o igual que el valor original."),
        "APROXIMACION_EXCESO": ("aproximar por exceso", "Ubica el orden al que debes aproximar.", "Si hay cifras posteriores no nulas, aumenta en una unidad la última cifra conservada.", "Comprueba que el resultado sea mayor o igual que el número original."),
        "REDONDEO": ("redondear un número al orden indicado", "Marca la cifra que quieres conservar y observa inmediatamente la siguiente.", "Conserva si la siguiente es menor que \(5\); aumenta una unidad si es \(5\) o mayor.", "Elimina las cifras restantes y compara la distancia al valor original."),
        "REGLA_DEL_CINCO": ("aplicar correctamente la regla del cinco", "Identifica la primera cifra que será eliminada.", "Si esa cifra es \(5\) o mayor, incrementa la última cifra conservada; si es menor, mantenla.", "Revisa posibles llevadas, como al redondear \(1.99\) a décimas."),
        "TRUNCAMIENTO": ("truncar un número al orden indicado", "Ubica la última posición decimal que se conservará.", "Elimina todas las cifras posteriores sin modificar la última conservada.", "Distingue el truncamiento del redondeo comparando ambos resultados."),
        "ERROR_ABSOLUTO": ("calcular el error absoluto de una aproximación", "Identifica cuál es el valor exacto y cuál el aproximado.", "Resta ambos valores y toma el valor absoluto de la diferencia.", "Expresa el error en la misma unidad de la magnitud medida."),
        "ERROR_RELATIVO": ("calcular e interpretar el error relativo", "Calcula primero el error absoluto.", "Divide ese error por el valor absoluto del dato exacto, que debe ser distinto de cero.", "Interpreta el cociente como error por unidad y compáralo entre mediciones."),
        "ERROR_PORCENTUAL": ("expresar el error relativo como porcentaje", "Obtén el error relativo a partir del valor exacto y el aproximado.", "Multiplica el error relativo por \(100\).", "Añade el símbolo \(\%\) e interpreta el porcentaje respecto del valor exacto."),
    }
    if semantic_id == "MAT.NUM.FRACCIONES_OPERATORIA.MULTIPLICACION":
        return (
            "multiplicar fracciones",
            "Revisa los signos y simplifica factores cruzados cuando sea posible.",
            "Multiplica numerador por numerador y denominador por denominador.",
            "Reduce la fracción final y verifica el signo del producto.",
        )
    if semantic_id == "MAT.NUM.FRACCIONES_OPERATORIA.INVERSO_MULTIPLICATIVO":
        return (
            "construir el recíproco de una fracción para usarlo en una división",
            "Verifica que numerador y denominador sean distintos de cero antes de invertir.",
            "Intercambia ambos términos y conserva el signo global de la fracción.",
            "Comprueba el recíproco calculando que el producto con la fracción original sea \(1\).",
        )
    try:
        return plans[concept]
    except KeyError as exc:
        raise KeyError(f"Sin plan pedagógico específico para {semantic_id}") from exc


def build_content(semantic_id: str, node_name: str) -> dict:
    meta = meta_for(semantic_id, node_name)
    subtheme = semantic_id.split(".")[2]
    title = node_name
    lower_title = title[:1].lower() + title[1:]
    definition = _without_trailing_period(meta["definition"])
    example = _without_example_prefix(meta["example"])
    fact = _without_trailing_period(meta["fact"])
    goal, prepare, execute, verify = _resource_plan(semantic_id)

    introduction = _variant(
        semantic_id,
        "intro",
        [
            f"Observa este caso: {example}. Para explicar por qué funciona estudiaremos {lower_title}. Al finalizar podrás {goal}.",
            f"El caso “{example}” plantea una situación propia de {lower_title}. Resolverla exige usar esta condición con precisión: {definition}.",
            f"La afirmación “{fact}” se puede comprobar en {example}. Este recurso desarrolla el razonamiento de {lower_title} que conecta ambas ideas.",
            f"En el caso “{example}” aparece {lower_title}. Lo analizaremos paso a paso para {goal}, sin depender de una regla memorizada.",
            f"Para estudiar {lower_title} partiremos de una situación concreta: {example}. La definición que guiará cada decisión es: {definition}.",
            f"Una tarea matemática frecuente es {goal}. El caso “{example}” muestra cómo abordarla desde {lower_title}.",
            f"{_upper_initial(example)}. Este resultado se explica mediante {lower_title}; el criterio que permite controlarlo es: {fact}.",
            f"La idea “{fact}” cobra sentido al analizar el caso “{example}”. Ese vínculo es el foco de {lower_title}.",
        ],
    )

    explanation_middle = _variant(
        semantic_id,
        "explanation",
        [
            f"En el caso “{example}” esta definición se aplica de forma directa. El control final consiste en comprobar que {fact[0].lower() + fact[1:]}",
            f"El ejemplo “{example}” lleva la definición a una situación concreta y permite verificar esta consecuencia: {fact}",
            f"Para analizar “{example}” se identifican los datos, se aplica la definición y se controla el resultado mediante la idea “{fact}”",
            f"La relación entre la definición y el caso “{example}” conduce a una conclusión útil: {fact}",
            f"En “{example}” cada decisión debe justificarse desde la definición, no desde la memoria. La comprobación decisiva es que {fact[0].lower() + fact[1:]}",
            f"Esta formulación se hace concreta en “{example}”. Allí puede reconocerse que {fact[0].lower() + fact[1:]}",
        ],
    )

    procedure = [f"Paso 1: {prepare}", f"Paso 2: {execute}", f"Paso 3: {verify}"]

    return {
        "semantic_id": semantic_id,
        "objetivo": _objective_for(semantic_id, title, goal, fact),
        "introduccion": introduction,
        "resumen": f"{_upper_initial(definition)}. Como criterio de control, {fact[0].lower() + fact[1:]}",
        "explicacion": f"{_upper_initial(definition)}.\n\n{explanation_middle}.",
        "procedimiento": procedure,
        "ejemplos": _examples_for(
            semantic_id,
            title,
            definition,
            example,
            fact,
            prepare,
            execute,
            verify,
        ),
        "errores_frecuentes": [
            f"Empezar {lower_title} sin realizar este control inicial: {prepare}",
            f"Memorizar “{example}” como respuesta aislada, sin reconstruir la definición que lo justifica.",
            f"Convertir en receta el paso “{execute}” y usarlo aunque cambien las condiciones del problema.",
            f"Dar por válida una conclusión sobre {lower_title} que contradice el criterio “{fact}”.",
            f"Cerrar el ejercicio sin esta comprobación específica: {verify}",
        ],
        "fuente": source_for(subtheme),
        "estado": "publicado",
    }


def make_exercises(semantic_id: str, node_name: str, competencia: str, all_meta: dict[str, dict]) -> list[dict]:
    meta = all_meta[semantic_id]
    prefix = stable_prefix(semantic_id)
    title = node_name
    lower_title = title[:1].lower() + title[1:]
    definition = _without_trailing_period(meta["definition"])
    example = _without_example_prefix(meta["example"])
    fact = _without_trailing_period(meta["fact"])

    def_choices, def_answer = place_correct(
        definition,
        choose_distractors(
            definition,
            siblings_for(all_meta, semantic_id, "definition"),
            GENERIC_DEFINITIONS,
        ),
        prefix + "-DEF",
    )
    ex_choices, ex_answer = place_correct(
        example,
        choose_distractors(
            example,
            siblings_for(all_meta, semantic_id, "example"),
            GENERIC_EXAMPLES,
        ),
        prefix + "-EX",
    )
    fact_choices, fact_answer = place_correct(
        fact,
        choose_distractors(
            fact,
            siblings_for(all_meta, semantic_id, "fact"),
            GENERIC_FACTS,
        ),
        prefix + "-FACT",
    )
    title_choices, title_answer = place_correct(
        title,
        choose_distractors(
            title,
            [KnowledgeNode.objects.get(semantic_id=sid).name for sid in all_meta if sid != semantic_id and sid.split(".")[2] == semantic_id.split(".")[2]][:3],
            GENERIC_TITLES,
        ),
        prefix + "-TITLE",
    )
    false_reference = (
        siblings_for(all_meta, semantic_id, "definition")
        + siblings_for(all_meta, semantic_id, "fact")
        + ["es una regla que puede usarse sin revisar sus condiciones"]
    )[0]

    def_prompt = _variant(
        semantic_id,
        "exercise-definition",
        [
            f"¿Cuál formulación define con precisión {lower_title}?",
            f"Para estudiar {lower_title}, ¿qué definición debe utilizarse?",
            f"Selecciona la descripción matemática completa de {lower_title}.",
            f"¿Qué alternativa expresa el significado de {lower_title} sin omitir condiciones?",
            f"Una estudiante necesita recordar qué es {lower_title}. ¿Qué opción debería anotar?",
        ],
    )
    example_prompt = _variant(
        semantic_id,
        "exercise-example",
        [
            f"¿Qué caso muestra de manera directa {lower_title}?",
            f"Selecciona el ejemplo que permite reconocer {lower_title}.",
            f"¿En cuál situación aparece correctamente {lower_title}?",
            f"Entre los siguientes casos, ¿cuál representa {lower_title}?",
            f"¿Qué ejemplo usarías para explicar {lower_title} a otra persona?",
        ],
    )
    fact_prompt = _variant(
        semantic_id,
        "exercise-fact",
        [
            f"¿Qué conclusión es propia de {lower_title}?",
            f"Después de aplicar {lower_title}, ¿qué idea sirve como control?",
            f"¿Cuál afirmación completa correctamente el estudio de {lower_title}?",
            f"¿Qué consecuencia conviene comprobar al trabajar {lower_title}?",
            f"Selecciona la propiedad clave asociada con {lower_title}.",
        ],
    )

    return [
        {
            "stable_id": f"{prefix}-GEN-CONC-1",
            "semantic_id": semantic_id,
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": competencia or "M1",
            "prompt": def_prompt,
            "choices": def_choices,
            "correct_answer": def_answer,
            "solution_steps": f"Para {lower_title}, la formulación completa es “{definition}”. Las demás alternativas describen conceptos distintos o incompletos.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-CONC-2",
            "semantic_id": semantic_id,
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": competencia or "M1",
            "prompt": example_prompt,
            "choices": ex_choices,
            "correct_answer": ex_answer,
            "solution_steps": f"El caso “{_without_example_prefix(example)}” cumple la definición de {lower_title}: {definition}.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-CONC-3",
            "semantic_id": semantic_id,
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": competencia or "M1",
            "prompt": fact_prompt,
            "choices": fact_choices,
            "correct_answer": fact_answer,
            "solution_steps": f"La conclusión específica para {lower_title} es “{fact}”; funciona como control del razonamiento.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-REC-1",
            "semantic_id": semantic_id,
            "item_group": "reconocimiento",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": competencia or "M1",
            "prompt": f"El caso “{_without_example_prefix(example)}” corresponde principalmente a uno de estos recursos. ¿A cuál?",
            "choices": title_choices,
            "correct_answer": title_answer,
            "solution_steps": f"Los datos del caso satisfacen “{definition}”; por eso corresponden a {title}.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-PROC-1",
            "semantic_id": semantic_id,
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "competencia": competencia or "M1",
            "prompt": f"Respecto de {lower_title}, evalúa la afirmación: “{_upper_initial(definition)}”.",
            "correct_answer": "Verdadero",
            "solution_steps": f"Verdadero. La afirmación incluye la condición que caracteriza {lower_title}.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-PROC-2",
            "semantic_id": semantic_id,
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "competencia": competencia or "M1",
            "prompt": f"Para {lower_title}, se propone el caso “{_without_example_prefix(example)}”. ¿Cumple la idea “{fact}”?",
            "correct_answer": "Verdadero",
            "solution_steps": f"Verdadero. Al aplicar la definición de {lower_title} al caso, se verifica que {fact[0].lower() + fact[1:]}.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-PROC-3",
            "semantic_id": semantic_id,
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "competencia": competencia or "M1",
            "prompt": f"La frase “{false_reference}” pertenece a un concepto cercano. ¿Basta por sí sola para definir completamente {lower_title}?",
            "correct_answer": "Falso",
            "solution_steps": f"Falso. Esa frase no reúne las condiciones completas de {lower_title}; la definición pertinente es “{definition}”.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-PAES-1",
            "semantic_id": semantic_id,
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": competencia or "M1",
            "prompt": f"En el caso “{_without_example_prefix(example)}”, ¿qué definición justifica de forma completa el procedimiento o la clasificación realizada?",
            "choices": def_choices,
            "correct_answer": def_answer,
            "solution_steps": f"La justificación debe nombrar la condición de {lower_title}: {definition}.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-PAES-2",
            "semantic_id": semantic_id,
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": competencia or "M1",
            "prompt": f"Un estudiante concluye que “{fact}”. ¿Qué recurso matemático está usando principalmente?",
            "choices": title_choices,
            "correct_answer": title_answer,
            "solution_steps": f"Esa conclusión se obtiene al estudiar {title}, cuya definición es “{definition}”.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-PAES-3",
            "semantic_id": semantic_id,
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": competencia or "M1",
            "prompt": f"Tras analizar “{_without_example_prefix(example)}”, ¿qué afirmación permite comprobar que la interpretación de {lower_title} es correcta?",
            "choices": fact_choices,
            "correct_answer": fact_answer,
            "solution_steps": f"El control pertinente para {lower_title} es “{fact}”; las otras opciones se refieren a recursos vecinos.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual",
        },
    ]


def main() -> None:
    nodes = {
        node.semantic_id: node
        for node in KnowledgeNode.objects.filter(
            node_type="recurso",
            parent__parent__semantic_id="MAT.NUM.B0203",
        )
    }
    ordered_semantic_ids = [sid for group in RESOURCE_GROUPS for sid in group]
    if len(ordered_semantic_ids) != 74:
        raise RuntimeError(f"RESOURCE_GROUPS suma {len(ordered_semantic_ids)} y debería sumar 74")
    missing = set(ordered_semantic_ids) - set(nodes)
    extra = set(nodes) - set(ordered_semantic_ids)
    if missing or extra:
        raise RuntimeError(f"Diferencia entre DB y RESOURCE_GROUPS. missing={missing} extra={extra}")

    all_meta = {sid: meta_for(sid, nodes[sid].name) for sid in ordered_semantic_ids}

    for sid in ordered_semantic_ids:
        safe_write_yaml(CONTENT_DIR / yaml_filename(sid), build_content(sid, nodes[sid].name))

    for i, group in enumerate(RESOURCE_GROUPS, start=1):
        rows: list[dict] = []
        for sid in group:
            node = nodes[sid]
            rows.extend(make_exercises(sid, node.name, node.competencia, all_meta))
        write_jsonl(EXERCISES_DIR / f"mat-num-racionales-banco-gen-{i}.jsonl", rows)

    print(f"B0203 generado: {len(ordered_semantic_ids)} YAML y {len(RESOURCE_GROUPS)} JSONL.")


if __name__ == "__main__":
    main()
