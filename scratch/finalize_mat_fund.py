from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "docs" / "conocimiento" / "contenido"
EXERCISES_DIR = ROOT / "docs" / "conocimiento" / "ejercicios"


class Dumper(yaml.SafeDumper):
    pass


def _str_presenter(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


Dumper.add_representer(str, _str_presenter)


VALID_JSON_ESCAPE_NEXT = set('"\\/bfnrtu')


def repair_json_line(raw: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(raw):
        ch = raw[i]
        if ch != "\\":
            out.append(ch)
            i += 1
            continue

        j = i
        while j < len(raw) and raw[j] == "\\":
            j += 1
        run_len = j - i
        next_char = raw[j] if j < len(raw) else ""

        if run_len % 2 == 0:
            out.append("\\" * run_len)
            i = j
            continue

        if next_char in VALID_JSON_ESCAPE_NEXT:
            out.append("\\" * run_len)
            i = j + 1
            continue

        out.append("\\" * (run_len + 1))
        i = j
    return "".join(out)


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    if not path.exists():
        return rows
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                rows.append(json.loads(repair_json_line(line)))
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_yaml(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        yaml.dump(data, fh, Dumper=Dumper, allow_unicode=True, sort_keys=False)


def subtheme_of(semantic_id: str) -> str:
    return semantic_id.split(".")[2]


def concept_of(semantic_id: str) -> str:
    return semantic_id.split(".")[3]


def yaml_filename(semantic_id: str) -> str:
    subtema = subtheme_of(semantic_id).lower().replace("_", "-")
    concepto = concept_of(semantic_id).lower().replace("_", "-")
    return f"mat-fund-{subtema}-{concepto}.yaml"


def stable_prefix(semantic_id: str) -> str:
    return hashlib.sha1(semantic_id.encode("utf-8")).hexdigest()[:6].upper()


def place_correct(correct: str, distractors: list[str], seed: str) -> tuple[list[str], str]:
    uniq: list[str] = []
    seen = {correct}
    for item in distractors:
        if item and item not in seen:
            uniq.append(item)
            seen.add(item)
        if len(uniq) == 3:
            break
    while len(uniq) < 3:
        filler = f"Distractor {len(uniq) + 1}"
        if filler not in seen:
            uniq.append(filler)
            seen.add(filler)
    pos = int(hashlib.sha1(seed.encode("utf-8")).hexdigest(), 16) % 4
    choices = uniq.copy()
    choices.insert(pos, correct)
    return choices, correct


GENERIC_DEFINITIONS = [
    "una operación aritmética entre números enteros",
    "una regla que depende solo del orden en que se escriben los datos",
    "una propiedad exclusiva de figuras geométricas",
    "un procedimiento de cálculo sin relación con lógica ni conjuntos",
]

GENERIC_EXAMPLES = [
    "Resolver 8 + 5 sumando dos números naturales.",
    "Ordenar una lista de mayor a menor sin usar criterios de pertenencia.",
    "Medir el perímetro de un triángulo cualquiera.",
    "Calcular un porcentaje sin usar símbolos lógicos ni conjuntos.",
]

GENERIC_FACTS = [
    "No depende del gusto personal, sino de una definición precisa.",
    "Conviene distinguir la idea principal de otras nociones cercanas.",
    "Una notación correcta evita confundir la representación con el significado.",
    "El contexto determina cómo se interpreta el concepto.",
]

GENERIC_TITLES = [
    "Una operación aritmética",
    "Una regla de orden",
    "Una propiedad geométrica",
    "Un cálculo numérico",
]


META = {
    # Conjuntos básicos
    "MAT.FUND.CONJUNTOS_BASICOS.DEFINICION_CONJUNTO": {
        "title": "Definición de conjunto",
        "definition": "un conjunto es una colección bien definida de elementos",
        "example": "Las vocales {a, e, i, o, u} forman un conjunto bien definido.",
        "fact": "La pertenencia a un conjunto debe poder decidirse sin ambigüedad.",
    },
    "MAT.FUND.CONJUNTOS_BASICOS.NOTACION_LLAVES": {
        "title": "Notación con llaves",
        "definition": "la notación con llaves escribe un conjunto entre { } para agrupar sus elementos",
        "example": "El conjunto de números pares menores que 8 puede escribirse como {2, 4, 6}.",
        "fact": "Las llaves indican que estamos nombrando un conjunto y no una expresión cualquiera.",
    },
    "MAT.FUND.CONJUNTOS_BASICOS.ELEMENTO": {
        "title": "Elemento de un conjunto",
        "definition": "un elemento es un objeto que pertenece a un conjunto",
        "example": "Si A = {2, 4, 6}, entonces 4 es un elemento de A.",
        "fact": "Los elementos son los objetos individuales que forman el conjunto.",
    },
    "MAT.FUND.CONJUNTOS_BASICOS.PERTENENCIA": {
        "title": "Pertenencia",
        "definition": "la pertenencia indica que un objeto está dentro de un conjunto",
        "example": "La expresión 3 ∈ {1, 2, 3} muestra una pertenencia correcta.",
        "fact": "El símbolo ∈ se usa para afirmar que un elemento pertenece a un conjunto.",
    },
    "MAT.FUND.CONJUNTOS_BASICOS.NO_PERTENENCIA": {
        "title": "No pertenencia",
        "definition": "la no pertenencia indica que un objeto no está dentro de un conjunto",
        "example": "La expresión 5 ∉ {2, 4, 6} muestra una no pertenencia correcta.",
        "fact": "El símbolo ∉ se usa para afirmar que un elemento no pertenece a un conjunto.",
    },
    "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_EXTENSION": {
        "title": "Conjunto por extensión",
        "definition": "un conjunto por extensión se describe listando uno a uno sus elementos",
        "example": "A = {1, 2, 3, 4} es una descripción por extensión.",
        "fact": "La forma por extensión muestra directamente qué elementos integran el conjunto.",
    },
    "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_COMPRENSION": {
        "title": "Conjunto por comprensión",
        "definition": "un conjunto por comprensión se describe mediante una propiedad común",
        "example": "A = {x ∈ ℕ : x es par y x < 10} es una descripción por comprensión.",
        "fact": "La forma por comprensión usa una condición que deben cumplir los elementos.",
    },
    "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_VACIO": {
        "title": "Conjunto vacío",
        "definition": "el conjunto vacío es el conjunto que no tiene elementos",
        "example": "El conjunto {x ∈ ℕ : x < 0} es vacío y se representa por ∅.",
        "fact": "El conjunto vacío puede denotarse por ∅ o por {}.",
    },
    "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_UNITARIO": {
        "title": "Conjunto unitario",
        "definition": "un conjunto unitario es un conjunto que tiene exactamente un elemento",
        "example": "El conjunto {7} es unitario porque contiene un solo elemento.",
        "fact": "La cardinalidad de un conjunto unitario es 1.",
    },
    "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_UNIVERSAL": {
        "title": "Conjunto universal",
        "definition": "el conjunto universal es el conjunto de referencia que contiene todos los elementos del contexto",
        "example": "Si el contexto son los naturales menores que 10, entonces U = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}.",
        "fact": "El conjunto universal depende del problema y suele denotarse por U.",
    },
    "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_POTENCIA": {
        "title": "Conjunto potencia",
        "definition": "el conjunto potencia de A es el conjunto formado por todos los subconjuntos de A",
        "example": "Si A = {1, 2}, entonces P(A) = {∅, {1}, {2}, {1, 2}}.",
        "fact": "El conjunto potencia siempre incluye al conjunto vacío y al conjunto original.",
    },
    "MAT.FUND.CONJUNTOS_BASICOS.CARDINALIDAD_CONJUNTO_POTENCIA": {
        "title": "Cardinalidad del conjunto potencia",
        "definition": "la cardinalidad del conjunto potencia cuenta cuántos subconjuntos tiene un conjunto",
        "example": "Si |A| = 3, entonces |P(A)| = 2³ = 8.",
        "fact": "Si un conjunto tiene n elementos, su conjunto potencia tiene 2ⁿ subconjuntos.",
    },
    # Cuantificadores
    "MAT.FUND.CUANTIFICADORES.CUANTIFICADOR_UNIVERSAL": {
        "title": "Cuantificador universal",
        "definition": "el cuantificador universal afirma que todos los elementos del dominio cumplen una propiedad",
        "example": "∀x ∈ ℕ, x + 0 = x es un ejemplo de cuantificador universal.",
        "fact": "El símbolo ∀ se lee “para todo”.",
    },
    "MAT.FUND.CUANTIFICADORES.CUANTIFICADOR_EXISTENCIAL": {
        "title": "Cuantificador existencial",
        "definition": "el cuantificador existencial afirma que al menos un elemento del dominio cumple una propiedad",
        "example": "∃x ∈ ℕ tal que x es par es un ejemplo de cuantificador existencial.",
        "fact": "El símbolo ∃ se lee “existe al menos uno”.",
    },
    "MAT.FUND.CUANTIFICADORES.DOMINIO_DE_DISCURSO": {
        "title": "Dominio de discurso",
        "definition": "el dominio de discurso es el conjunto sobre el que se interpreta un enunciado cuantificado",
        "example": "En ∀x ∈ ℝ, x² ≥ 0, el dominio de discurso es ℝ.",
        "fact": "Cambiar el dominio puede cambiar el valor de verdad de una proposición.",
    },
    "MAT.FUND.CUANTIFICADORES.NEGACION_UNIVERSAL": {
        "title": "Negación del cuantificador universal",
        "definition": "negar un cuantificador universal equivale a afirmar que existe un contraejemplo",
        "example": "¬(∀x P(x)) equivale a ∃x ¬P(x).",
        "fact": "Al negar ∀, el cuantificador cambia a ∃ y la propiedad se niega.",
    },
    "MAT.FUND.CUANTIFICADORES.NEGACION_EXISTENCIAL": {
        "title": "Negación del cuantificador existencial",
        "definition": "negar un cuantificador existencial equivale a afirmar que ningún elemento cumple la propiedad",
        "example": "¬(∃x P(x)) equivale a ∀x ¬P(x).",
        "fact": "Al negar ∃, el cuantificador cambia a ∀ y la propiedad se niega.",
    },
    "MAT.FUND.CUANTIFICADORES.CONTRAEJEMPLO": {
        "title": "Contraejemplo",
        "definition": "un contraejemplo es un caso concreto que muestra que un enunciado universal es falso",
        "example": "En “todos los números primos son impares”, el número 2 funciona como contraejemplo.",
        "fact": "Basta un solo contraejemplo para refutar una afirmación universal.",
    },
    # Diagramas de Venn
    "MAT.FUND.DIAGRAMAS_VENN.DIAGRAMA_UN_CONJUNTO": {
        "title": "Diagrama de un conjunto",
        "definition": "un diagrama de un conjunto representa visualmente un conjunto dentro del universo",
        "example": "Se dibuja un rectángulo para U y un círculo para A dentro de él.",
        "fact": "El diagrama permite ubicar elementos dentro o fuera del conjunto.",
    },
    "MAT.FUND.DIAGRAMAS_VENN.DIAGRAMA_DOS_CONJUNTOS_DISJUNTOS": {
        "title": "Diagrama de dos conjuntos disjuntos",
        "definition": "representa dos conjuntos que no comparten elementos",
        "example": "En el diagrama, A y B aparecen como dos regiones separadas sin superposición.",
        "fact": "Si dos conjuntos son disjuntos, entonces A ∩ B = ∅.",
    },
    "MAT.FUND.DIAGRAMAS_VENN.DIAGRAMA_DOS_CONJUNTOS_INTERSECTADOS": {
        "title": "Diagrama de dos conjuntos intersectados",
        "definition": "representa dos conjuntos con una región común",
        "example": "La zona central compartida por A y B representa A ∩ B.",
        "fact": "Los elementos comunes a ambos conjuntos se ubican en la intersección.",
    },
    "MAT.FUND.DIAGRAMAS_VENN.DIAGRAMA_TRES_CONJUNTOS": {
        "title": "Diagrama de tres conjuntos",
        "definition": "representa tres conjuntos y sus posibles superposiciones",
        "example": "Tres círculos permiten ver intersecciones dobles y la intersección triple.",
        "fact": "La región central del diagrama representa A ∩ B ∩ C.",
    },
    "MAT.FUND.DIAGRAMAS_VENN.REGIONES_DOS_CONJUNTOS": {
        "title": "Regiones en dos conjuntos",
        "definition": "las regiones de un diagrama de dos conjuntos separan solo A, solo B, A ∩ B y el exterior",
        "example": "En dos conjuntos hay una zona exclusiva de A, otra de B, una intersección y una zona fuera de ambos.",
        "fact": "Estas regiones ayudan a interpretar unión, intersección y complemento.",
    },
    "MAT.FUND.DIAGRAMAS_VENN.REGIONES_TRES_CONJUNTOS": {
        "title": "Regiones en tres conjuntos",
        "definition": "las regiones de un diagrama de tres conjuntos distinguen zonas exclusivas, dobles, triple y exterior",
        "example": "En tres conjuntos pueden distinguirse zonas solo de A, solo de B, solo de C, intersecciones dobles y triple.",
        "fact": "En un diagrama de tres conjuntos se suelen analizar ocho regiones básicas.",
    },
    # Razonamiento lógico
    "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_CONTRARRECIPROCO": {
        "title": "Condicional contrarrecíproco",
        "definition": "el contrarrecíproco de p → q es ¬q → ¬p",
        "example": "Si de “si estudias, apruebas” formamos “si no apruebas, no estudias”, obtenemos el contrarrecíproco.",
        "fact": "El contrarrecíproco es lógicamente equivalente al condicional original.",
    },
    "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_INVERSO": {
        "title": "Condicional inverso",
        "definition": "el inverso de p → q es ¬p → ¬q",
        "example": "De “si estudias, apruebas” se obtiene “si no estudias, no apruebas” al formar el inverso.",
        "fact": "El inverso no es equivalente en general al condicional original.",
    },
    "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_PONENS": {
        "title": "Modus ponens",
        "definition": "modus ponens permite concluir q a partir de p → q y p",
        "example": "Si estudias, apruebas. Estudias. Luego, apruebas.",
        "fact": "Su esquema es: p → q, p, por lo tanto q.",
    },
    "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_TOLLENS": {
        "title": "Modus tollens",
        "definition": "modus tollens permite concluir ¬p a partir de p → q y ¬q",
        "example": "Si estudias, apruebas. No apruebas. Luego, no estudias.",
        "fact": "Su esquema es: p → q, ¬q, por lo tanto ¬p.",
    },
    # Tablas de verdad
    "MAT.FUND.TABLAS_VERDAD.TABLA_NEGACION": {
        "title": "Tabla de verdad de la negación",
        "definition": "la tabla de negación muestra que ¬p invierte el valor de verdad de p",
        "example": "Si p = V, entonces ¬p = F; si p = F, entonces ¬p = V.",
        "fact": "La negación trabaja con una sola variable proposicional.",
    },
    "MAT.FUND.TABLAS_VERDAD.TABLA_CONJUNCION": {
        "title": "Tabla de verdad de la conjunción",
        "definition": "la tabla de conjunción muestra que p ∧ q solo es verdadera cuando ambas proposiciones son verdaderas",
        "example": "V ∧ F = F es una fila típica de la tabla de conjunción.",
        "fact": "La conjunción exige dos valores verdaderos para resultar verdadera.",
    },
    "MAT.FUND.TABLAS_VERDAD.TABLA_DISYUNCION_INCLUSIVA": {
        "title": "Tabla de verdad de la disyunción inclusiva",
        "definition": "la disyunción inclusiva p ∨ q es verdadera cuando al menos una proposición es verdadera",
        "example": "V ∨ F = V es una fila típica de la disyunción inclusiva.",
        "fact": "La disyunción inclusiva solo es falsa cuando ambas proposiciones son falsas.",
    },
    "MAT.FUND.TABLAS_VERDAD.TABLA_DISYUNCION_EXCLUSIVA": {
        "title": "Tabla de verdad de la disyunción exclusiva",
        "definition": "la disyunción exclusiva es verdadera cuando exactamente una proposición es verdadera",
        "example": "V ⊕ F = V, pero V ⊕ V = F.",
        "fact": "La disyunción exclusiva es falsa cuando ambas proposiciones tienen el mismo valor.",
    },
    "MAT.FUND.TABLAS_VERDAD.TABLA_CONDICIONAL": {
        "title": "Tabla de verdad del condicional",
        "definition": "el condicional p → q solo es falso cuando p es verdadera y q es falsa",
        "example": "La fila V → F = F es la única fila falsa del condicional.",
        "fact": "El condicional es equivalente a ¬p ∨ q.",
    },
    "MAT.FUND.TABLAS_VERDAD.TABLA_BICONDICIONAL": {
        "title": "Tabla de verdad del bicondicional",
        "definition": "el bicondicional p ↔ q es verdadero cuando p y q tienen el mismo valor de verdad",
        "example": "V ↔ V = V y F ↔ F = V.",
        "fact": "El bicondicional es falso cuando las proposiciones difieren.",
    },
    "MAT.FUND.TABLAS_VERDAD.FILAS_DOS_VARIABLES": {
        "title": "Filas con dos variables",
        "definition": "una tabla de verdad con dos variables tiene 4 filas de combinaciones",
        "example": "Con p y q se enumeran las combinaciones VV, VF, FV y FF.",
        "fact": "La cantidad de filas se calcula con 2² cuando hay dos variables.",
    },
    "MAT.FUND.TABLAS_VERDAD.FILAS_TRES_VARIABLES": {
        "title": "Filas con tres variables",
        "definition": "una tabla de verdad con tres variables tiene 8 filas de combinaciones",
        "example": "Con p, q y r se necesitan 8 combinaciones distintas.",
        "fact": "La cantidad de filas se calcula con 2³ cuando hay tres variables.",
    },
    "MAT.FUND.TABLAS_VERDAD.CONSTRUCCION_DOS_VARIABLES": {
        "title": "Construcción de tabla con dos variables",
        "definition": "construir una tabla con dos variables implica listar 4 combinaciones y evaluar la expresión paso a paso",
        "example": "Primero se escriben las columnas de p y q, luego las subexpresiones y finalmente la proposición completa.",
        "fact": "La tabla se completa columna por columna para evitar errores.",
    },
    "MAT.FUND.TABLAS_VERDAD.CONSTRUCCION_TRES_VARIABLES": {
        "title": "Construcción de tabla con tres variables",
        "definition": "construir una tabla con tres variables implica listar 8 combinaciones y evaluar la expresión ordenadamente",
        "example": "Primero se escriben las 8 filas de p, q y r antes de calcular la proposición compuesta.",
        "fact": "Al agregar una variable, el número de filas se duplica.",
    },
    "MAT.FUND.TABLAS_VERDAD.TAUTOLOGIA": {
        "title": "Tautología",
        "definition": "una tautología es una proposición compuesta que resulta verdadera en todas las filas",
        "example": "p ∨ ¬p es una tautología.",
        "fact": "La columna final de una tautología contiene solo V.",
    },
    "MAT.FUND.TABLAS_VERDAD.CONTRADICCION": {
        "title": "Contradicción",
        "definition": "una contradicción es una proposición compuesta que resulta falsa en todas las filas",
        "example": "p ∧ ¬p es una contradicción.",
        "fact": "La columna final de una contradicción contiene solo F.",
    },
    "MAT.FUND.TABLAS_VERDAD.CONTINGENCIA": {
        "title": "Contingencia",
        "definition": "una contingencia es una proposición compuesta que es verdadera en algunas filas y falsa en otras",
        "example": "p ∧ q es una contingencia porque no es siempre verdadera ni siempre falsa.",
        "fact": "Una contingencia no es ni tautología ni contradicción.",
    },
    # Cardinalidad / producto cartesiano
    "MAT.FUND.CARDINALIDAD_CONJUNTOS.REGION_EXACTAMENTE_DOS_CONJUNTOS": {
        "title": "Región exactamente en dos conjuntos",
        "definition": "en tres conjuntos, la región exactamente en dos conjuntos reúne los elementos que pertenecen a dos conjuntos pero no al tercero",
        "example": "Las zonas A ∩ B sin C, A ∩ C sin B y B ∩ C sin A forman la región exactamente en dos conjuntos.",
        "fact": "La región exactamente en dos conjuntos excluye la intersección triple.",
    },
    "MAT.FUND.CARDINALIDAD_CONJUNTOS.REGION_TRES_CONJUNTOS": {
        "title": "Región de tres conjuntos",
        "definition": "la región de tres conjuntos corresponde a los elementos comunes a A, B y C al mismo tiempo",
        "example": "La zona central de un diagrama de tres conjuntos representa A ∩ B ∩ C.",
        "fact": "La región triple se obtiene intersectando los tres conjuntos.",
    },
    "MAT.FUND.PRODUCTO_CARTESIANO.PRODUCTO_CARTESIANO_DEFINICION": {
        "title": "Definición de producto cartesiano",
        "definition": "el producto cartesiano A × B es el conjunto de todos los pares ordenados (a, b) con a ∈ A y b ∈ B",
        "example": "Si A = {1, 2} y B = {a, b}, entonces A × B = {(1, a), (1, b), (2, a), (2, b)}.",
        "fact": "En A × B importa el orden: primero va un elemento de A y luego uno de B.",
    },
    "MAT.FUND.PRODUCTO_CARTESIANO.ELEMENTOS_PRODUCTO_CARTESIANO": {
        "title": "Elementos del producto cartesiano",
        "definition": "los elementos de un producto cartesiano son pares ordenados",
        "example": "En A × B, un elemento puede ser (2, b), pero no simplemente 2 ni b por separado.",
        "fact": "Cada par ordenado toma un elemento del primer conjunto y otro del segundo.",
    },
    "MAT.FUND.PRODUCTO_CARTESIANO.CARDINALIDAD_PRODUCTO_CARTESIANO": {
        "title": "Cardinalidad del producto cartesiano",
        "definition": "la cardinalidad de A × B se calcula multiplicando la cantidad de elementos de A por la de B",
        "example": "Si |A| = 2 y |B| = 3, entonces |A × B| = 6.",
        "fact": "La regla general es |A × B| = |A| · |B|.",
    },
    "MAT.FUND.PRODUCTO_CARTESIANO.REPRESENTACION_PLANO_CARTESIANO": {
        "title": "Representación en el plano cartesiano",
        "definition": "un par ordenado puede representarse como un punto (x, y) en el plano cartesiano",
        "example": "El par (2, 3) se ubica avanzando 2 en el eje x y 3 en el eje y.",
        "fact": "Cada par ordenado del producto cartesiano puede interpretarse como una ubicación en el plano.",
    },
}


MISSING_YAMLS = [
    "MAT.FUND.CARDINALIDAD_CONJUNTOS.REGION_EXACTAMENTE_DOS_CONJUNTOS",
    "MAT.FUND.CARDINALIDAD_CONJUNTOS.REGION_TRES_CONJUNTOS",
    "MAT.FUND.CONJUNTOS_BASICOS.CARDINALIDAD_CONJUNTO_POTENCIA",
    "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_COMPRENSION",
    "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_EXTENSION",
    "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_POTENCIA",
    "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_UNITARIO",
    "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_UNIVERSAL",
    "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_VACIO",
    "MAT.FUND.PRODUCTO_CARTESIANO.REPRESENTACION_PLANO_CARTESIANO",
]


GENERATED_BANKS = {
    "mat-fund-conjuntos-basicos-banco-gen-1.jsonl": [
        "MAT.FUND.CONJUNTOS_BASICOS.DEFINICION_CONJUNTO",
        "MAT.FUND.CONJUNTOS_BASICOS.NOTACION_LLAVES",
        "MAT.FUND.CONJUNTOS_BASICOS.ELEMENTO",
        "MAT.FUND.CONJUNTOS_BASICOS.PERTENENCIA",
        "MAT.FUND.CONJUNTOS_BASICOS.NO_PERTENENCIA",
        "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_EXTENSION",
        "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_COMPRENSION",
    ],
    "mat-fund-conjuntos-basicos-banco-gen-2.jsonl": [
        "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_VACIO",
        "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_UNITARIO",
        "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_UNIVERSAL",
        "MAT.FUND.CONJUNTOS_BASICOS.CONJUNTO_POTENCIA",
        "MAT.FUND.CONJUNTOS_BASICOS.CARDINALIDAD_CONJUNTO_POTENCIA",
    ],
    "mat-fund-cuantificadores-banco-gen-1.jsonl": [
        "MAT.FUND.CUANTIFICADORES.CUANTIFICADOR_UNIVERSAL",
        "MAT.FUND.CUANTIFICADORES.CUANTIFICADOR_EXISTENCIAL",
        "MAT.FUND.CUANTIFICADORES.DOMINIO_DE_DISCURSO",
        "MAT.FUND.CUANTIFICADORES.NEGACION_UNIVERSAL",
        "MAT.FUND.CUANTIFICADORES.NEGACION_EXISTENCIAL",
        "MAT.FUND.CUANTIFICADORES.CONTRAEJEMPLO",
    ],
    "mat-fund-razonamiento-banco-gen-2.jsonl": [
        "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_CONTRARRECIPROCO",
        "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_INVERSO",
        "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_PONENS",
        "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_TOLLENS",
    ],
    "mat-fund-tablas-verdad-banco-gen-1.jsonl": [
        "MAT.FUND.TABLAS_VERDAD.TABLA_NEGACION",
        "MAT.FUND.TABLAS_VERDAD.TABLA_CONJUNCION",
        "MAT.FUND.TABLAS_VERDAD.TABLA_DISYUNCION_INCLUSIVA",
        "MAT.FUND.TABLAS_VERDAD.TABLA_DISYUNCION_EXCLUSIVA",
        "MAT.FUND.TABLAS_VERDAD.TABLA_CONDICIONAL",
        "MAT.FUND.TABLAS_VERDAD.TABLA_BICONDICIONAL",
    ],
    "mat-fund-tablas-verdad-banco-gen-2.jsonl": [
        "MAT.FUND.TABLAS_VERDAD.FILAS_DOS_VARIABLES",
        "MAT.FUND.TABLAS_VERDAD.FILAS_TRES_VARIABLES",
        "MAT.FUND.TABLAS_VERDAD.CONSTRUCCION_DOS_VARIABLES",
        "MAT.FUND.TABLAS_VERDAD.CONSTRUCCION_TRES_VARIABLES",
        "MAT.FUND.TABLAS_VERDAD.TAUTOLOGIA",
        "MAT.FUND.TABLAS_VERDAD.CONTRADICCION",
        "MAT.FUND.TABLAS_VERDAD.CONTINGENCIA",
    ],
    "mat-fund-diagramas-venn-banco-gen-1.jsonl": [
        "MAT.FUND.DIAGRAMAS_VENN.DIAGRAMA_UN_CONJUNTO",
        "MAT.FUND.DIAGRAMAS_VENN.DIAGRAMA_DOS_CONJUNTOS_DISJUNTOS",
        "MAT.FUND.DIAGRAMAS_VENN.DIAGRAMA_DOS_CONJUNTOS_INTERSECTADOS",
        "MAT.FUND.DIAGRAMAS_VENN.DIAGRAMA_TRES_CONJUNTOS",
        "MAT.FUND.DIAGRAMAS_VENN.REGIONES_DOS_CONJUNTOS",
        "MAT.FUND.DIAGRAMAS_VENN.REGIONES_TRES_CONJUNTOS",
    ],
    "mat-fund-producto-cartesiano-banco-gen-2.jsonl": [
        "MAT.FUND.CARDINALIDAD_CONJUNTOS.REGION_EXACTAMENTE_DOS_CONJUNTOS",
        "MAT.FUND.CARDINALIDAD_CONJUNTOS.REGION_TRES_CONJUNTOS",
        "MAT.FUND.PRODUCTO_CARTESIANO.PRODUCTO_CARTESIANO_DEFINICION",
        "MAT.FUND.PRODUCTO_CARTESIANO.ELEMENTOS_PRODUCTO_CARTESIANO",
        "MAT.FUND.PRODUCTO_CARTESIANO.CARDINALIDAD_PRODUCTO_CARTESIANO",
        "MAT.FUND.PRODUCTO_CARTESIANO.REPRESENTACION_PLANO_CARTESIANO",
    ],
}


NORMALIZE_ONLY = [
    "mat-fund-cardinalidad-banco-gen-1.jsonl",
    "mat-fund-cardinalidad-producto-banco-gen-1.jsonl",
    "mat-fund-conectivos-logicos-banco-gen-1.jsonl",
    "mat-fund-conjuntos-relaciones-banco-gen-1.jsonl",
    "mat-fund-conjuntos-relaciones-banco-gen-2.jsonl",
    "mat-fund-logica-basica-banco-gen-1.jsonl",
    "mat-fund-operaciones-conjuntos-banco-gen-1.jsonl",
    "mat-fund-propiedades-conjuntos-banco-gen-1.jsonl",
    "mat-fund-propiedades-conjuntos-banco-gen-2.jsonl",
    "mat-fund-razonamiento-banco-gen-1.jsonl",
]


def siblings_for(semantic_id: str, field: str) -> list[str]:
    group = subtheme_of(semantic_id)
    values: list[str] = []
    for sid, meta in META.items():
        if sid == semantic_id:
            continue
        if subtheme_of(sid) == group and meta.get(field):
            values.append(meta[field])
    return values


def distractors_for(semantic_id: str, field: str, fallback: list[str]) -> list[str]:
    values = siblings_for(semantic_id, field)
    if len(values) >= 3:
        return values[:3]
    merged = values + [x for x in fallback if x not in values]
    return merged[:3]


def false_reference_for(semantic_id: str) -> str:
    candidates = siblings_for(semantic_id, "fact") + siblings_for(semantic_id, "definition")
    if candidates:
        return candidates[0]
    return "depende solo del orden en que se escriben los datos"


def normalize_legacy_row(row: dict) -> dict:
    if row.get("semantic_id") and row.get("item_group") and row.get("prompt"):
        return row

    stable_id = row.get("stable_id", "")
    try:
        index = int(stable_id.rsplit("-", 1)[-1])
    except Exception:
        index = 0

    if 1 <= index <= 3:
        item_group = "conceptuales"
    elif index == 4:
        item_group = "reconocimiento"
    elif 5 <= index <= 7:
        item_group = "procedimiento_basico"
    else:
        item_group = "tipo_paes"

    return {
        "stable_id": stable_id,
        "semantic_id": row.get("semantic_id", ""),
        "item_group": item_group,
        "format": row.get("tipo") or row.get("format") or "multiple_choice",
        "difficulty": row.get("dificultad") or row.get("difficulty") or "basica",
        "competencia": row.get("competencia") or "U",
        "prompt": row.get("enunciado") or row.get("prompt") or "",
        "choices": row.get("opciones") or row.get("choices") or [],
        "correct_answer": row.get("respuesta_correcta") or row.get("correct_answer") or "",
        "solution_steps": row.get("explicacion") or row.get("solution_steps") or "",
        "paes_style": item_group == "tipo_paes",
        "status": row.get("status") or "ready",
        "source_kind": row.get("source_kind") or "manual",
    }


def make_exercises(semantic_id: str) -> list[dict]:
    meta = META[semantic_id]
    title = meta["title"]
    definition = meta["definition"].rstrip(".")
    example = meta["example"].rstrip(".")
    fact = meta["fact"].rstrip(".")
    prefix = stable_prefix(semantic_id)
    lower_title = title.lower()

    def_choices, def_answer = place_correct(
        meta["definition"],
        distractors_for(semantic_id, "definition", GENERIC_DEFINITIONS),
        prefix + "-DEF",
    )
    ex_choices, ex_answer = place_correct(
        meta["example"],
        distractors_for(semantic_id, "example", GENERIC_EXAMPLES),
        prefix + "-EX",
    )
    fact_choices, fact_answer = place_correct(
        meta["fact"],
        distractors_for(semantic_id, "fact", GENERIC_FACTS),
        prefix + "-FACT",
    )
    title_choices, title_answer = place_correct(
        title,
        distractors_for(semantic_id, "title", GENERIC_TITLES),
        prefix + "-TITLE",
    )
    wrong_reference = false_reference_for(semantic_id)

    rows = [
        {
            "stable_id": f"{prefix}-GEN-CONC-1",
            "semantic_id": semantic_id,
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": f"¿Qué describe mejor {lower_title}?",
            "choices": def_choices,
            "correct_answer": def_answer,
            "solution_steps": f"La definición correcta es: {meta['definition']}. Esa es la idea central de {lower_title}.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-CONC-2",
            "semantic_id": semantic_id,
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": f"¿Cuál de los siguientes casos ejemplifica mejor {lower_title}?",
            "choices": ex_choices,
            "correct_answer": ex_answer,
            "solution_steps": f"El ejemplo correcto es: {meta['example']}. Ese caso representa adecuadamente {lower_title}.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-CONC-3",
            "semantic_id": semantic_id,
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": f"¿Qué afirmación clave conviene recordar sobre {lower_title}?",
            "choices": fact_choices,
            "correct_answer": fact_answer,
            "solution_steps": f"La afirmación correcta es: {meta['fact']}. Esa observación ayuda a usar bien el concepto.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-REC-1",
            "semantic_id": semantic_id,
            "item_group": "reconocimiento",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": f"Identifica la opción que corresponde a {lower_title}.",
            "choices": ex_choices,
            "correct_answer": ex_answer,
            "solution_steps": f"Se reconoce {lower_title} en el ejemplo: {meta['example']}.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-PROC-1",
            "semantic_id": semantic_id,
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": f"¿Es correcto afirmar que {definition}?",
            "correct_answer": "Verdadero",
            "solution_steps": f"Verdadero. Esa es justamente la definición de {lower_title}.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-PROC-2",
            "semantic_id": semantic_id,
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": f"¿El caso “{example}” corresponde a {lower_title}?",
            "correct_answer": "Verdadero",
            "solution_steps": f"Verdadero. El ejemplo dado es una aplicación directa de {lower_title}.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-PROC-3",
            "semantic_id": semantic_id,
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": f"¿La afirmación “{wrong_reference}” describe {lower_title}?",
            "correct_answer": "Falso",
            "solution_steps": f"Falso. {lower_title.capitalize()} se describe mejor así: {meta['definition']}. La afirmación propuesta corresponde a otra idea.",
            "status": "ready",
            "source_kind": "manual",
        },
        {
            "stable_id": f"{prefix}-GEN-PAES-1",
            "semantic_id": semantic_id,
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": f"En una guía PAES, una estudiante debe reconocer {lower_title}. ¿Qué alternativa aplica correctamente esta idea?",
            "choices": ex_choices,
            "correct_answer": ex_answer,
            "solution_steps": f"La alternativa correcta es: {meta['example']}. Ese caso representa {lower_title} sin ambigüedad.",
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
            "competencia": "U",
            "prompt": f"Un profesor escribe la afirmación “{fact}”. ¿A qué recurso se refiere principalmente?",
            "choices": title_choices,
            "correct_answer": title_answer,
            "solution_steps": f"La afirmación remite a {title}, porque su idea clave es: {meta['fact']}.",
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
            "competencia": "U",
            "prompt": f"En un control se pide identificar la definición correcta de {lower_title}. ¿Qué alternativa debe marcarse?",
            "choices": def_choices,
            "correct_answer": def_answer,
            "solution_steps": f"La opción correcta es la definición: {meta['definition']}.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual",
        },
    ]
    return rows


def build_content(semantic_id: str) -> dict:
    meta = META[semantic_id]
    title = meta["title"]
    definition = meta["definition"]
    example = meta["example"]
    fact = meta["fact"]
    subtheme = subtheme_of(semantic_id)

    if subtheme == "CONJUNTOS_BASICOS":
        procedimiento = (
            "1. Identifica qué objetos o expresiones intervienen en la situación.\n"
            "2. Determina qué idea de teoría de conjuntos se está usando.\n"
            "3. Verifica la notación o la propiedad relevante del concepto.\n"
            "4. Concluye usando una representación correcta del conjunto."
        )
        fuente = "Lipschutz, S. (2011). Teoría de conjuntos. McGraw-Hill."
    elif subtheme == "CARDINALIDAD_CONJUNTOS":
        procedimiento = (
            "1. Dibuja o interpreta el diagrama de Venn correspondiente.\n"
            "2. Ubica la región pedida con cuidado, distinguiendo intersecciones y exclusiones.\n"
            "3. Considera si deben incluirse o excluirse zonas compartidas.\n"
            "4. Expresa la región con lenguaje de conjuntos y, si corresponde, cuenta sus elementos."
        )
        fuente = "Baldor, A. (2004). Álgebra. Publicaciones Cultural."
    else:
        procedimiento = (
            "1. Identifica los conjuntos o pares ordenados involucrados.\n"
            "2. Determina qué relación o representación pide el problema.\n"
            "3. Aplica la definición del concepto paso a paso.\n"
            "4. Verifica que la conclusión respete el orden, la notación y el contexto."
        )
        fuente = "Swokowski, E. (2011). Álgebra y trigonometría con geometría analítica. Cengage."

    return {
        "semantic_id": semantic_id,
        "nombre": title,
        "objetivo": f"Comprender {title.lower()} y aplicarlo correctamente en situaciones básicas.",
        "introduccion": (
            f"El estudio de {title.lower()} ayuda a organizar ideas y evitar errores frecuentes de interpretación.\n\n"
            f"Cuando comprendemos este recurso, podemos leer mejor enunciados, representar conjuntos con precisión y justificar conclusiones matemáticas con lenguaje claro."
        ),
        "resumen": f"{definition.capitalize()}. Además, {fact[0].lower() + fact[1:]}",
        "explicacion": (
            f"{definition.capitalize()}. Esta idea aparece de manera natural cuando trabajamos con lenguaje de conjuntos o con representaciones formales.\n\n"
            f"Una forma útil de reconocerla es recordar que {fact[0].lower() + fact[1:]}\n\n"
            f"Por ejemplo: {example}"
        ),
        "procedimiento": procedimiento,
        "ejemplos": [
            {
                "tipo": "A",
                "titulo": "Identificar el concepto en contexto",
                "enunciado": f"Explica por qué el caso “{example}” corresponde a {title.lower()}.",
                "solucion_pasos": (
                    f"1. Observa qué objetos o expresiones aparecen.\n"
                    f"2. Compáralos con la definición: {definition}.\n"
                    f"3. Concluye que el caso sí corresponde a {title.lower()}."
                ),
            },
            {
                "tipo": "A",
                "titulo": "Recordar la idea clave",
                "enunciado": f"Justifica la afirmación: “{fact}”.",
                "solucion_pasos": (
                    f"1. Parte de la definición del concepto.\n"
                    f"2. Relaciona esa definición con la propiedad indicada.\n"
                    f"3. Explica por qué la afirmación es correcta en este recurso."
                ),
            },
            {
                "tipo": "B",
                "titulo": "Verificar una afirmación",
                "respuesta": "Sí",
                "solucion_pasos": f"Sí. El ejemplo “{example}” es una aplicación válida de {title.lower()}.",
            },
            {
                "tipo": "B",
                "titulo": "Descartar una confusión",
                "respuesta": "No",
                "solucion_pasos": (
                    f"No. {title} no debe confundirse con otra noción distinta; su definición correcta es: {definition}."
                ),
            },
        ],
        "fuente": fuente,
        "errores_frecuentes": [
            f"Confundir {title.lower()} con otro concepto cercano del mismo subtema.",
            "Usar la notación de manera informal y sacar conclusiones sin revisar la definición.",
            "Mirar solo un ejemplo particular y olvidar la idea general del recurso.",
            "Interpretar el contexto sin fijarse en qué conjunto, dominio o representación se está usando.",
            "Responder de memoria sin comprobar la propiedad clave que caracteriza al concepto.",
        ],
        "estado": "publicado",
    }


def generate_yaml_files() -> None:
    for semantic_id in MISSING_YAMLS:
        path = CONTENT_DIR / yaml_filename(semantic_id)
        write_yaml(path, build_content(semantic_id))


def normalize_existing_files() -> None:
    for name in NORMALIZE_ONLY:
        path = EXERCISES_DIR / name
        rows = [normalize_legacy_row(row) for row in read_jsonl(path)]
        if name == "mat-fund-cardinalidad-banco-gen-1.jsonl":
            for row in rows:
                if row.get("stable_id") == "PIE2-GEN-CONC-2":
                    row["semantic_id"] = "MAT.FUND.CARDINALIDAD_CONJUNTOS.INCLUSION_EXCLUSION_DOS_CONJUNTOS"
        write_jsonl(path, rows)


def generate_banks() -> None:
    for name, semantic_ids in GENERATED_BANKS.items():
        rows: list[dict] = []
        for semantic_id in semantic_ids:
            rows.extend(make_exercises(semantic_id))
        write_jsonl(EXERCISES_DIR / name, rows)


def verify_generated_banks() -> None:
    for name, semantic_ids in GENERATED_BANKS.items():
        rows = read_jsonl(EXERCISES_DIR / name)
        counts: dict[str, int] = {}
        for row in rows:
            counts[row["semantic_id"]] = counts.get(row["semantic_id"], 0) + 1
        for semantic_id in semantic_ids:
            count = counts.get(semantic_id, 0)
            if count != 10:
                raise RuntimeError(f"{name}: {semantic_id} quedó con {count} ejercicios")


def main() -> None:
    generate_yaml_files()
    normalize_existing_files()
    generate_banks()
    verify_generated_banks()
    print("MAT.FUND finalizado: YAML faltantes generados y bancos JSONL corregidos.")


if __name__ == "__main__":
    main()
