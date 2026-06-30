import os
import sys
import json
import time
import requests
import subprocess
import yaml
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
try:
    import django
    django.setup()
    from apps.content.models import KnowledgeNode
except Exception as e:
    print(f"Advertencia: No se pudo inicializar Django: {e}")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY no encontrada.")
    sys.exit(1)

CONTENT_DIR = Path("docs/conocimiento/contenido")
EJERCICIOS_DIR = Path("docs/conocimiento/ejercicios")

# Configurar formateador YAML para usar bloques literales '|' en strings multilinea
class Dumper(yaml.SafeDumper):
    pass

def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

Dumper.add_representer(str, str_presenter)

PROMPT_TEMPLATE = """
Eres un profesor de matemáticas experto y redactor de material pedagógico para ProfeOnline.
Debes generar contenido didáctico y 10 preguntas de evaluación para el siguiente recurso matemático:

ID Semántico: {semantic_id}
Nombre: {name}
Descripción: {description}
Abreviatura: {abbr}

Deberás responder ÚNICAMENTE con un objeto JSON válido (sin delimitadores markdown ```json) que se ajuste exactamente al siguiente esquema JSON:

{{
  "content": {{
    "semantic_id": "{semantic_id}",
    "objetivo": "Verbo en infinitivo más el logro (ej: Calcular el MCM de dos números...).",
    "introduccion": "Explicación muy didáctica (para niño de 10 años) usando analogías del mundo real. Sin LaTeX en las primeras líneas. Entre 2 y 3 párrafos.",
    "resumen": "Resumen técnico de 2 o 3 oraciones de qué es y cómo se usa. Puede tener LaTeX ($...$).",
    "explicacion": "Explicación formal en Markdown. Usa negrita para conceptos clave. Fórmulas en LaTeX ($...$ para inline, $$...$$ para bloques independientes).",
    "procedimiento": [
      "Paso 1: ...",
      "Paso 2: ...",
      "Paso 3: ..."
    ],
    "ejemplos": [
      {{
        "titulo": "Ejemplo 1",
        "enunciado": "Determina o calcula...",
        "solucion_pasos": [
          "Paso a: ...",
          "Paso b: ..."
        ]
      }},
      {{
        "titulo": "Ejemplo 2",
        "enunciado": "Calcula...",
        "solucion_pasos": [
          "Paso a: ...",
          "Paso b: ..."
        ]
      }},
      {{
        "titulo": "¿Es el número X divisible por Y?",
        "respuesta": "Sí",
        "solucion_pasos": [
          "Justificación..."
        ]
      }},
      {{
        "titulo": "¿Es el número W divisible por Z?",
        "respuesta": "No",
        "solucion_pasos": [
          "Justificación..."
        ]
      }}
    ],
    "errores_frecuentes": [
      "Afirmación FALSA 1 (sin LaTeX o mínimo)",
      "Afirmación FALSA 2",
      "Afirmación FALSA 3",
      "Afirmación FALSA 4",
      "Afirmación FALSA 5"
    ],
    "fuente": "Matemática 7° Básico Tomo 1 — {fuente}"
  }},
  "exercises": [
    {{
      "stable_id": "{abbr}-GEN-CONC-1",
      "semantic_id": "{semantic_id}",
      "item_group": "conceptuales",
      "format": "multiple_choice",
      "difficulty": "basica",
      "competencia": "M1",
      "prompt": "Pregunta conceptual. Soporta LaTeX (una barra \\, ej: $2 \\cdot 3$).",
      "choices": ["A) Opción correcta", "B) Opción incorrecta", "C) Opción incorrecta", "D) Opción incorrecta"],
      "correct_answer": "A) Opción correcta",
      "solution_steps": "Solución paso a paso.",
      "paes_style": false
    }},
    {{
      "stable_id": "{abbr}-GEN-CONC-2",
      "semantic_id": "{semantic_id}",
      "item_group": "conceptuales",
      "format": "multiple_choice",
      "difficulty": "basica",
      "competencia": "M1",
      "prompt": "Pregunta conceptual 2.",
      "choices": ["A) Opción correcta", "B) Opción incorrecta", "C) Opción incorrecta", "D) Opción incorrecta"],
      "correct_answer": "A) Opción correcta",
      "solution_steps": "Explicación.",
      "paes_style": false
    }},
    {{
      "stable_id": "{abbr}-GEN-CONC-3",
      "semantic_id": "{semantic_id}",
      "item_group": "conceptuales",
      "format": "multiple_choice",
      "difficulty": "basica",
      "competencia": "M1",
      "prompt": "Pregunta conceptual 3.",
      "choices": ["A) Opción correcta", "B) Opción incorrecta", "C) Opción incorrecta", "D) Opción incorrecta"],
      "correct_answer": "A) Opción correcta",
      "solution_steps": "Explicación.",
      "paes_style": false
    }},
    {{
      "stable_id": "{abbr}-GEN-REC-1",
      "semantic_id": "{semantic_id}",
      "item_group": "reconocimiento",
      "format": "multiple_choice",
      "difficulty": "basica",
      "competencia": "M1",
      "prompt": "Pregunta de reconocimiento de datos o conceptos.",
      "choices": ["A) Opción correcta", "B) Opción incorrecta", "C) Opción incorrecta", "D) Opción incorrecta"],
      "correct_answer": "A) Opción correcta",
      "solution_steps": "Explicación.",
      "paes_style": false
    }},
    {{
      "stable_id": "{abbr}-GEN-PROC-1",
      "semantic_id": "{semantic_id}",
      "item_group": "procedimiento_basico",
      "format": "true_false",
      "difficulty": "basica",
      "competencia": "M1",
      "prompt": "¿Es verdadero que ...?",
      "choices": [],
      "correct_answer": "Verdadero",
      "solution_steps": "Explicación de por qué es verdadero.",
      "paes_style": false
    }},
    {{
      "stable_id": "{abbr}-GEN-PROC-2",
      "semantic_id": "{semantic_id}",
      "item_group": "procedimiento_basico",
      "format": "true_false",
      "difficulty": "basica",
      "competencia": "M1",
      "prompt": "¿Es verdadero que ...?",
      "choices": [],
      "correct_answer": "Falso",
      "solution_steps": "Explicación de por qué es falso.",
      "paes_style": false
    }},
    {{
      "stable_id": "{abbr}-GEN-PROC-3",
      "semantic_id": "{semantic_id}",
      "item_group": "procedimiento_basico",
      "format": "true_false",
      "difficulty": "basica",
      "competencia": "M1",
      "prompt": "¿Es verdadero que ...?",
      "choices": [],
      "correct_answer": "Verdadero",
      "solution_steps": "Explicación.",
      "paes_style": false
    }},
    {{
      "stable_id": "{abbr}-GEN-PAES-1",
      "semantic_id": "{semantic_id}",
      "item_group": "tipo_paes",
      "format": "multiple_choice",
      "difficulty": "media",
      "competencia": "M1",
      "prompt": "Pregunta de aplicación en contexto (tipo PAES).",
      "choices": ["A) Opción correcta", "B) Opción incorrecta", "C) Opción incorrecta", "D) Opción incorrecta"],
      "correct_answer": "A) Opción correcta",
      "solution_steps": "Solución.",
      "paes_style": true
    }},
    {{
      "stable_id": "{abbr}-GEN-PAES-2",
      "semantic_id": "{semantic_id}",
      "item_group": "tipo_paes",
      "format": "multiple_choice",
      "difficulty": "media",
      "competencia": "M1",
      "prompt": "Pregunta tipo PAES 2.",
      "choices": ["A) Opción correcta", "B) Opción incorrecta", "C) Opción incorrecta", "D) Opción incorrecta"],
      "correct_answer": "A) Opción correcta",
      "solution_steps": "Solución.",
      "paes_style": true
    }},
    {{
      "stable_id": "{abbr}-GEN-PAES-3",
      "semantic_id": "{semantic_id}",
      "item_group": "tipo_paes",
      "format": "multiple_choice",
      "difficulty": "media",
      "competencia": "M1",
      "prompt": "Pregunta tipo PAES 3.",
      "choices": ["A) Opción correcta", "B) Opción incorrecta", "C) Opción incorrecta", "D) Opción incorrecta"],
      "correct_answer": "A) Opción correcta",
      "solution_steps": "Solución.",
      "paes_style": true
    }}
  ]
}}

Reglas críticas de LaTeX:
- En las preguntas, explicaciones y alternativas, usa siempre LaTeX encerrado en $ o $$.
- Como la salida debe ser JSON válido, todos los backslashes de LaTeX deben escribirse escapados (ej: escribir \\mathbb{{Z}} o \\div en lugar de una sola barra).
- No uses comillas dentro del texto del JSON sin escaparlas como \\\" si es estrictamente necesario, o prefiere usar comillas simples.
"""

TANDAS = [
    {
        "name": "Tanda 3",
        "jsonl": "mat-num-teoria-numeros-banco-gen-3.jsonl",
        "resources": [
            ("MAT.NUM.DIVISIBILIDAD.CRITERIO_6", "CRIT6", "El número es divisible por 2 y por 3 simultáneamente", "mat-num-divisibilidad-criterio-6", "Teoría de Números"),
            ("MAT.NUM.DIVISIBILIDAD.CRITERIO_8", "CRIT8", "Las tres últimas cifras forman un número divisible por 8", "mat-num-divisibilidad-criterio-8", "Teoría de Números"),
            ("MAT.NUM.DIVISIBILIDAD.CRITERIO_9", "CRIT9", "La suma de las cifras es múltiplo de 9", "mat-num-divisibilidad-criterio-9", "Teoría de Números"),
            ("MAT.NUM.DIVISIBILIDAD.CRITERIO_10", "CRIT10", "Termina en 0", "mat-num-divisibilidad-criterio-10", "Teoría de Números"),
            ("MAT.NUM.DIVISIBILIDAD.CRITERIO_11", "CRIT11", "La diferencia entre la suma de cifras en posición impar y par es múltiplo de 11", "mat-num-divisibilidad-criterio-11", "Teoría de Números"),
            ("MAT.NUM.DIVISIBILIDAD.CRITERIO_25", "CRIT25", "Las dos últimas cifras son 00, 25, 50 o 75", "mat-num-divisibilidad-criterio-25", "Teoría de Números"),
        ]
    },
    {
        "name": "Tanda 4",
        "jsonl": "mat-num-teoria-numeros-banco-gen-4.jsonl",
        "resources": [
            ("MAT.NUM.NUMEROS_PRIMOS.PRIMO_DEFINICION", "PDEF", "Definición de número primo: tiene exactamente 2 divisores (1 y sí mismo)", "mat-num-numeros-primos-definicion", "Teoría de Números"),
            ("MAT.NUM.NUMEROS_PRIMOS.PRIMO_IDENTIFICACION", "PIDC", "Identificar números primos aplicando la criba de Eratóstenes", "mat-num-numeros-primos-identificacion", "Teoría de Números"),
            ("MAT.NUM.NUMEROS_PRIMOS.COMPUESTO_DEFINICION", "CDEF", "Definición de número compuesto: tiene más de 2 divisores", "mat-num-numeros-compuestos-definicion", "Teoría de Números"),
            ("MAT.NUM.NUMEROS_PRIMOS.COMPUESTO_IDENTIFICACION", "CIDC", "Identificar números compuestos y listar sus divisores", "mat-num-numeros-compuestos-identificacion", "Teoría de Números"),
            ("MAT.NUM.NUMEROS_PRIMOS.UNO_NO_PRIMO_NO_COMPUESTO", "UNPNC", "El número 1 como caso especial: no es primo ni compuesto", "mat-num-numeros-primos-caso-uno", "Teoría de Números"),
        ]
    },
    {
        "name": "Tanda 5",
        "jsonl": "mat-num-teoria-numeros-banco-gen-5.jsonl",
        "resources": [
            ("MAT.NUM.FACTORIZACION_PRIMA.FACTOR_PRIMO_CONCEPTO", "FCONC", "Concepto de factor primo", "mat-num-factorizacion-prima-factor-concepto", "Teoría de Números"),
            ("MAT.NUM.FACTORIZACION_PRIMA.DESCOMPOSICION_PRIMA_CONCEPTO", "DPCONC", "Concepto de descomposición en factores primos", "mat-num-factorizacion-prima-descomposicion-concepto", "Teoría de Números"),
            ("MAT.NUM.FACTORIZACION_PRIMA.DESCOMPOSICION_UNICA", "DUNI", "Teorema fundamental de la aritmética: la descomposición es única", "mat-num-factorizacion-prima-descomposicion-unica", "Teoría de Números"),
            ("MAT.NUM.FACTORIZACION_PRIMA.METODO_TABLA", "MTBL", "Método de tabla de divisiones sucesivas para descomponer", "mat-num-factorizacion-prima-metodo-tabla", "Teoría de Números"),
            ("MAT.NUM.FACTORIZACION_PRIMA.METODO_ARBOL", "MARBOL", "Método del árbol de factores para descomponer", "mat-num-factorizacion-prima-metodo-arbol", "Teoría de Números"),
        ]
    },
    {
        "name": "Tanda 6",
        "jsonl": "mat-num-teoria-numeros-banco-gen-6.jsonl",
        "resources": [
            ("MAT.NUM.FACTORIZACION_PRIMA.CANTIDAD_DIVISORES", "CDIV", "Cálculo de la cantidad de divisores a partir de la descomposición prima", "mat-num-factorizacion-cantidad-divisores", "Teoría de Números"),
            ("MAT.NUM.MINIMO_COMUN_MULTIPLO.CONCEPTO", "MCMC", "Definición y concepto del mínimo común múltiplo (MCM)", "mat-num-mcm-concepto", "Teoría de Números"),
            ("MAT.NUM.MINIMO_COMUN_MULTIPLO.IDENTIFICACION_LISTA", "MCMI", "Identificar el MCM listando múltiplos de los números", "mat-num-mcm-identificacion-lista", "Teoría de Números"),
            ("MAT.NUM.MINIMO_COMUN_MULTIPLO.METODO_TABLA_SIMULTANEA", "MCMT", "Método de tabla de divisiones simultáneas para calcular el MCM", "mat-num-mcm-metodo-tabla-simultanea", "Teoría de Números"),
            ("MAT.NUM.MINIMO_COMUN_MULTIPLO.METODO_POTENCIAS_PRIMAS", "MCMP", "Calcular el MCM multiplicando factores primos comunes y no comunes con su mayor exponente", "mat-num-mcm-metodo-potencias-primas", "Teoría de Números"),
        ]
    },
    {
        "name": "Tanda 7",
        "jsonl": "mat-num-teoria-numeros-banco-gen-7.jsonl",
        "resources": [
            ("MAT.NUM.MAXIMO_COMUN_DIVISOR.CONCEPTO", "MCDC", "Definición y concepto del máximo común divisor (MCD)", "mat-num-mcd-concepto", "Teoría de Números"),
            ("MAT.NUM.MAXIMO_COMUN_DIVISOR.IDENTIFICACION_LISTA", "MCDI", "Identificar el MCD listando divisores de los números", "mat-num-mcd-identificacion-lista", "Teoría de Números"),
            ("MAT.NUM.MAXIMO_COMUN_DIVISOR.METODO_TABLA_FACTORES_COMUNES", "MCDTFC", "Método de tabla para calcular el MCD dividiendo solo por factores comunes", "mat-num-mcd-metodo-tabla-factores-comunes", "Teoría de Números"),
            ("MAT.NUM.MAXIMO_COMUN_DIVISOR.METODO_POTENCIAS_PRIMAS", "MCDP", "Calcular el MCD multiplicando factores primos comunes con su menor exponente", "mat-num-mcd-metodo-potencias-primas", "Teoría de Números"),
            ("MAT.NUM.MAXIMO_COMUN_DIVISOR.ALGORITMO_EUCLIDES", "MCDE", "Calcular el MCD aplicando el algoritmo de divisiones sucesivas de Euclides", "mat-num-mcd-algoritmo-euclides", "Teoría de Números"),
        ]
    },
    {
        "name": "Tanda 8",
        "jsonl": "mat-num-teoria-numeros-banco-gen-8.jsonl",
        "resources": [
            ("MAT.NUM.MAXIMO_COMUN_DIVISOR.COPRIMOS_CONCEPTO", "MCOP", "Concepto de números coprimos (primos entre sí): su MCD es 1", "mat-num-mcd-coprimos", "Teoría de Números"),
            ("MAT.NUM.APLICACIONES_MCM_MCD.RELACION_PRODUCTO", "APREL", "Propiedad: el producto del MCM y del MCD de dos números es igual al producto de los números", "mat-num-aplicaciones-relacion-producto", "Teoría de Números"),
            ("MAT.NUM.APLICACIONES_MCM_MCD.PROBLEMA_MCM_COINCIDENCIA", "APMCM", "Problemas verbales que requieren calcular el MCM para determinar coincidencia o periodicidad", "mat-num-aplicaciones-problema-mcm-coincidencia", "Teoría de Números"),
            ("MAT.NUM.APLICACIONES_MCM_MCD.PROBLEMA_MCD_REPARTO", "APMCD", "Problemas verbales que requieren calcular el MCD para reparto equitativo máximo", "mat-num-aplicaciones-problema-mcd-reparto", "Teoría de Números"),
            ("MAT.NUM.APLICACIONES_MCM_MCD.SELECCION_MCM_O_MCD", "APSEL", "Analizar enunciados verbales para seleccionar si resolver con MCM o MCD", "mat-num-aplicaciones-seleccion-mcm-o-mcd", "Teoría de Números"),
        ]
    },
    {
        "name": "Tanda B01-1",
        "jsonl": "mat-num-enteros-operatoria-banco-gen-1.jsonl",
        "resources": [
            ("MAT.NUM.ENTEROS_OPERATORIA.ADICION_IGUAL_SIGNO", "ADIS", "Adición de enteros con el mismo signo", "mat-num-enteros-operatoria-adicion-igual-signo", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.ADICION_DISTINTO_SIGNO", "ADIDS", "Adición de enteros con diferente signo", "mat-num-enteros-operatoria-adicion-distinto-signo", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.CONMUTATIVA_ADICION", "COMA", "Propiedad conmutativa de la adición en Z", "mat-num-enteros-operatoria-conmutativa-adicion", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.ASOCIATIVA_ADICION", "ASOA", "Propiedad asociativa de la adición en Z", "mat-num-enteros-operatoria-asociativa-adicion", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.NEUTRO_ADITIVO", "NADIT", "Elemento neutro de la adición en Z (el cero)", "mat-num-enteros-operatoria-neutro-aditivo", "Enteros"),
        ]
    },
    {
        "name": "Tanda B01-2",
        "jsonl": "mat-num-enteros-operatoria-banco-gen-2.jsonl",
        "resources": [
            ("MAT.NUM.ENTEROS_OPERATORIA.INVERSO_ADITIVO", "INVA", "Concepto de inverso aditivo u opuesto de un número entero", "mat-num-enteros-operatoria-inverso-aditivo", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.SUSTRACCION_REGLA", "SUSR", "Sustracción de enteros como la adición del opuesto", "mat-num-enteros-operatoria-sustraccion-regla", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.MULT_SIGNOS_IGUALES", "MULTIG", "Multiplicación de enteros con igual signo", "mat-num-enteros-operatoria-mult-signos-iguales", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.MULT_SIGNOS_DISTINTOS", "MULTDI", "Multiplicación de enteros con distinto signo", "mat-num-enteros-operatoria-mult-signos-distintos", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.CONMUTATIVA_MULT", "COMM", "Propiedad conmutativa de la multiplicación en Z", "mat-num-enteros-operatoria-conmutativa-mult", "Enteros"),
        ]
    },
    {
        "name": "Tanda B01-3",
        "jsonl": "mat-num-enteros-operatoria-banco-gen-3.jsonl",
        "resources": [
            ("MAT.NUM.ENTEROS_OPERATORIA.ASOCIATIVA_MULT", "ASOM", "Propiedad asociativa de la multiplicación en Z", "mat-num-enteros-operatoria-asociativa-mult", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.NEUTRO_MULT", "NMULT", "Elemento neutro de la multiplicación en Z (el uno)", "mat-num-enteros-operatoria-neutro-mult", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.ABSORBENTE_CERO", "ABSC", "Elemento absorbente de la multiplicación (el cero)", "mat-num-enteros-operatoria-absorbente-cero", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.DISTRIBUTIVA_MULT_ADICION", "DIST", "Propiedad distributiva de la multiplicación respecto a la adición", "mat-num-enteros-operatoria-distributiva-mult-adicion", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.DIV_SIGNOS_IGUALES", "DIVIG", "División de enteros con el mismo signo", "mat-num-enteros-operatoria-div-signos-iguales", "Enteros"),
        ]
    },
    {
        "name": "Tanda B01-4",
        "jsonl": "mat-num-enteros-operatoria-banco-gen-4.jsonl",
        "resources": [
            ("MAT.NUM.ENTEROS_OPERATORIA.DIV_SIGNOS_DISTINTOS", "DIVDI", "División de enteros con diferente signo", "mat-num-enteros-operatoria-div-signos-distintos", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.DIVISION_POR_CERO", "DIVC", "La indeterminación/indefinición de la división por cero", "mat-num-enteros-operatoria-division-por-cero", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.PAPOMUDAS_ORDEN", "PAPO", "Prioridad de operaciones matemáticas (PAPOMUDAS)", "mat-num-enteros-operatoria-papomudas-orden", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.PARENTESIS_MAS", "PMAS", "Uso de paréntesis precedidos por el signo más", "mat-num-enteros-operatoria-parentesis-mas", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.PARENTESIS_MENOS", "PMEN", "Uso de paréntesis precedidos por el signo menos", "mat-num-enteros-operatoria-parentesis-menos", "Enteros"),
            ("MAT.NUM.ENTEROS_OPERATORIA.PARENTESIS_ANIDADOS", "PANI", "Operaciones con paréntesis anidados (corchetes y llaves)", "mat-num-enteros-operatoria-parentesis-anidados", "Enteros"),
        ]
    }
]

def call_gemini(prompt: str) -> dict:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 8000,
            "responseMimeType": "application/json",
            "thinkingConfig": {"thinkingBudget": 0},
        },
    }

    for attempt in range(4):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=90)
            if resp.status_code == 429:
                sleep_time = 45 * (attempt + 1)
                print(f"Rate limit alcanzado (429). Durmiendo por {sleep_time} segundos...")
                time.sleep(sleep_time)
                continue

            resp.raise_for_status()
            data = resp.json()
            parts = data["candidates"][0]["content"]["parts"]
            text = "".join(p.get("text", "") for p in parts if not p.get("thought"))

            return json.loads(text.strip())
        except Exception as e:
            print(f"Intento {attempt + 1} falló: {e}")
            if attempt == 3:
                raise e
            time.sleep(5 * (attempt + 1))

    raise RuntimeError("No se pudo obtener respuesta de Gemini tras varios intentos.")

def run_command(cmd, shell=False):
    print(f"Ejecutando comando: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    res = subprocess.run(cmd, capture_output=True, text=True, shell=shell)
    if res.returncode != 0:
        print(f"Comando falló con código {res.returncode}")
        print(f"STDOUT: {res.stdout}")
        print(f"STDERR: {res.stderr}")
        return False
    return True

def process_resource(semantic_id, abbr, desc, filename, fuente):
    yaml_path = CONTENT_DIR / f"{filename}.yaml"

    # Comprobar si el archivo YAML ya existe
    if yaml_path.exists():
        print(f"  [Skip] {semantic_id} ya tiene YAML.")
        return None

    print(f"  [Gen] Generando contenido para {semantic_id}...")
    prompt = PROMPT_TEMPLATE.format(
        semantic_id=semantic_id,
        name=semantic_id.split('.')[-1].replace('_', ' ').capitalize(),
        description=desc,
        abbr=abbr,
        fuente=fuente
    )

    # Llamar a la API
    result = call_gemini(prompt)

    content_dict = result["content"]
    content_dict["estado"] = "publicado"

    # Guardar YAML usando el SafeDumper customizado
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(content_dict, f, Dumper=Dumper, allow_unicode=True, sort_keys=False)
    print(f"    -> Guardado {yaml_path.name}")

    # Serializar ejercicios a una cadena en formato JSONL
    exercises_lines = []
    for ex in result["exercises"]:
        ex["status"] = "ready"
        ex["source_kind"] = "manual"
        # json.dumps con ensure_ascii=False para mantener tildes y caracteres en español
        exercises_lines.append(json.dumps(ex, ensure_ascii=False))

    return "\n".join(exercises_lines)

def cleanup_failed_files():
    print("Limpiando archivos de ejecuciones fallidas...")
    for tanda in TANDAS:
        for sem_id, abbr, desc, filename, fuente in tanda["resources"]:
            yaml_path = CONTENT_DIR / f"{filename}.yaml"
            if yaml_path.exists():
                try:
                    os.remove(yaml_path)
                    print(f"  Eliminado: {yaml_path.name}")
                except Exception as e:
                    print(f"  No se pudo eliminar {yaml_path.name}: {e}")
        jsonl_path = EJERCICIOS_DIR / tanda["jsonl"]
        if jsonl_path.exists():
            try:
                os.remove(jsonl_path)
                print(f"  Eliminado: {jsonl_path.name}")
            except Exception as e:
                print(f"  No se pudo eliminar {jsonl_path.name}: {e}")

def main():
    print("=== INICIANDO POBLACIÓN AUTOMÁTICA DE CONTENIDO ===")

    cleanup_failed_files()

    for idx, tanda in enumerate(TANDAS, start=3):
        tanda_name = tanda["name"]
        tanda_jsonl_file = EJERCICIOS_DIR / tanda["jsonl"]
        print(f"\n--- Procesando {tanda_name} ---")

        exercises_collected = []
        resources_processed = 0

        # Leer ejercicios ya existentes en este archivo de tanda
        existing_stable_ids = set()
        if tanda_jsonl_file.exists():
            with open(tanda_jsonl_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            ex = json.loads(line)
                            if "stable_id" in ex:
                                existing_stable_ids.add(ex["stable_id"])
                        except:
                            pass

        for sem_id, abbr, desc, filename, fuente in tanda["resources"]:
            try:
                has_exercises = any(abbr in sid for sid in existing_stable_ids)
                yaml_path = CONTENT_DIR / f"{filename}.yaml"

                if yaml_path.exists() and has_exercises:
                    print(f"  [Skip] {sem_id} ya existe por completo.")
                    continue

                jsonl_text = process_resource(sem_id, abbr, desc, filename, fuente)

                if jsonl_text:
                    for line in jsonl_text.split("\n"):
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            ex = json.loads(line)
                            if ex.get("stable_id") in existing_stable_ids:
                                continue
                            exercises_collected.append(line)
                            resources_processed += 1
                        except Exception as je:
                            print(f"    Error validando línea JSONL: {je}. Línea: {line}")

                time.sleep(6)
            except Exception as ex:
                print(f"  [Error] Falló la generación del recurso {sem_id}: {ex}")
                print("Continuando con el siguiente recurso de la tanda...")

        # Escribir ejercicios recopilados en esta tanda
        if exercises_collected:
            mode = "a" if tanda_jsonl_file.exists() else "w"
            with open(tanda_jsonl_file, mode, encoding="utf-8") as f:
                for ex_line in exercises_collected:
                    f.write(ex_line + "\n")
            print(f"  -> Guardados {len(exercises_collected)} ejercicios nuevos en {tanda_jsonl_file.name}")

        yaml_files_in_tanda = [CONTENT_DIR / f"{r[3]}.yaml" for r in tanda["resources"]]
        any_new_yamls = any(y.exists() for y in yaml_files_in_tanda)

        if any_new_yamls:
            print(f"  -> Cargando contenido en BD...")
            load_content_ok = run_command([".venv\\Scripts\\python.exe", "manage.py", "load_node_content"])

            if load_content_ok and tanda_jsonl_file.exists():
                print(f"  -> Cargando banco de ejercicios en BD...")
                run_command([".venv\\Scripts\\python.exe", "manage.py", "load_exercise_bank", "--file", str(tanda_jsonl_file)])

            # Git add & commit
            print(f"  -> Registrando cambios en git...")
            for y_file in yaml_files_in_tanda:
                if y_file.exists():
                    run_command(["git", "add", str(y_file)])
            if tanda_jsonl_file.exists():
                run_command(["git", "add", str(tanda_jsonl_file)])

            commit_msg = f"content(mat-num): tanda {idx} — {tanda_name} cargada ({len(tanda['resources'])} recursos)"
            run_command(["git", "commit", "-m", commit_msg])

    print("\n=== VERIFICACIÓN FINAL DE COBERTURA EN BD ===")
    check_query = """from apps.content.models import KnowledgeNode, NodeContent, NodeExercise
for bloque_id in ['MAT.NUM.B0201', 'MAT.NUM.B0202']:
    recursos = KnowledgeNode.objects.filter(node_type='recurso', parent__parent__semantic_id=bloque_id)
    con_contenido = recursos.filter(content__isnull=False).count()
    total = recursos.count()
    print(f'{bloque_id}: {con_contenido}/{total} recursos con contenido')
    sin_contenido = recursos.filter(content__isnull=True)
    for r in sin_contenido:
        print(f'  FALTA: {r.semantic_id}')
"""
    run_command([".venv\\Scripts\\python.exe", "manage.py", "shell", "-c", check_query])

    print("\n=== PROCESO COMPLETADO EXCELENTEMENTE ===")

if __name__ == "__main__":
    main()
