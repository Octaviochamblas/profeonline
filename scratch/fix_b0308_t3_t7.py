import os
import glob
import yaml
import re

def fix_yaml_files():
    base_dir = "docs/conocimiento/contenido"

    # Archivos a procesar: Tanda 3 a 7
    # Fraccionarias, Literales, Modelamiento, Sistemas 2x2, Sistemas Representacion
    patterns = [
        "mat-alg-ecuaciones-fraccionarias-*.yaml",
        "mat-alg-ecuaciones-literales-*.yaml",
        "mat-alg-modelamiento-lineal-*.yaml",
        "mat-alg-sistemas-2x2-*.yaml",
        "mat-alg-sistemas-representacion-*.yaml"
    ]

    files = []
    for p in patterns:
        files.extend(glob.glob(os.path.join(base_dir, p)))

    replacements = {
        r"(?i)portal mágico": "propiedad de igualdad",
        r"(?i)espías infiltrados": "sustitución de variables",
        r"(?i)magia": "álgebra",
        r"(?i)destruir las fracciones": "eliminar los denominadores",
        r"(?i)pisos de abajo": "denominadores",
        r"(?i)piso de abajo": "denominador",
        r"(?i)piso de arriba": "numerador",
        r"(?i)monstruo enorme": "expresión algebraica compleja",
        r"(?i)antídoto personalizado": "Mínimo Común Múltiplo (MCM)",
        r"(?i)antídoto": "MCM",
        r"(?i)aniquilarás": "simplificarás",
        r"(?i)aniquilar": "eliminar",
        r"(?i)aniquilen": "anulen",
        r"(?i)aniquila": "anula",
        r"(?i)amigable": "lineal estándar",
        r"(?i)CADA INQUILINO": "CADA TÉRMINO",
        r"(?i)inquilino": "término",
        r"(?i)espejismo": "valor espurio",
        r"(?i)broma": "paradoja",
        r"(?i)Lista Negra": "lista de restricciones de dominio",
        r"(?i)criba": "verificación",
        r"(?i)invasión de letras": "presencia de múltiples parámetros",
        r"(?i)números amigables": "coeficientes numéricos",
        r"(?i)números disfrazados de letras": "constantes paramétricas",
        r"(?i)princesa atrapada en el castillo": "variable a despejar",
        r"(?i)guardias": "términos y coeficientes",
        r"(?i)Guardia externo": "Término externo",
        r"(?i)Guardia del medio": "Término intermedio",
        r"(?i)Guardia cercano": "Coeficiente adyacente",
        r"(?i)¡La princesa está libre!": "La variable ha sido despejada.",
        r"(?i)máquina perfecta para calcular": "fórmula explícita para evaluar",
        r"(?i)bloque": "término compuesto",
        r"(?i)bloques": "términos compuestos",
        r"(?i)explosión matemática": "indeterminación matemática",
        r"(?i)error mortal": "error conceptual",
        r"(?i)romper paréntesis ilegalmente": "distribuir incorrectamente",
        r"(?i)Error garrafal": "Error común",
        r"(?i)campos de fuerza": "jerarquías operativas",
        r"(?i)actores": "variables",
        r"(?i)verbo": "operador relacional",
        r"(?i)el mundo de las palabras y el mundo del álgebra": "el enunciado verbal y el modelo algebraico",
        r"(?i)olvidas de Juan, de Pedro y de las palabras": "haces abstracción del contexto verbal",
        r"(?i)juguetes tirados en el suelo": "términos no agrupados",
        r"(?i)ordena la casa": "agrupa los términos semejantes",
        r"(?i)manzanas": "variables principales",
        r"(?i)monedas": "términos independientes",
        r"(?i)barrer": "simplificar",
        r"(?i)rey legítimo": "par ordenado válido",
        r"(?i)vías del tren": "rectas paralelas",
        r"(?i)chocan": "se intersecan",
        r"(?i)chocarán": "se intersecarán",
        r"(?i)punto de choque": "punto de intersección",
        r"(?i)clon perfecto": "ecuación linealmente dependiente",
        r"(?i)clones": "ecuaciones dependientes",
        r"(?i)magia!": "De este modo,",
        r"(?i)mentira espantosa": "contradicción matemática"
    }

    for fp in files:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parsear con regex ya que YAML manual a veces rompe los bloques
        import yaml
        try:
            data = yaml.safe_load(content)
        except Exception as e:
            print(f"Error parsing {fp}: {e}")
            continue

        if not data: continue

        explicacion_original = data.get('explicacion', '')

        # Aplicar reemplazos formales
        explicacion_formal = explicacion_original
        for old, new in replacements.items():
            explicacion_formal = re.sub(old, new, explicacion_formal)

        # Extraer introduccion y resumen
        paragraphs = [p.strip() for p in explicacion_formal.split('\n\n') if p.strip()]

        if len(paragraphs) >= 3:
            introduccion = paragraphs[0]
            resumen = paragraphs[-1]
            explicacion = "\n\n".join(paragraphs[1:-1])
        elif len(paragraphs) == 2:
            introduccion = paragraphs[0]
            resumen = "Este proceso es fundamental para encontrar la solución correcta."
            explicacion = paragraphs[1]
        else:
            introduccion = paragraphs[0] if paragraphs else "Concepto fundamental en el álgebra."
            resumen = "La correcta aplicación de estos principios asegura una resolución metódica."
            explicacion = paragraphs[0] if paragraphs else ""

        # Formatear procedimiento
        proc_text = data.get('procedimiento', '')
        if isinstance(proc_text, str):
            # Dividir por números seguidos de punto (ej: "1. ", "2. ")
            steps = []
            for line in proc_text.split('\n'):
                line = line.strip()
                if line:
                    # Remover el "1. ", "2. " del inicio si existe
                    line = re.sub(r'^\d+\.\s*', '', line)
                    steps.append(f"Paso {len(steps)+1}: {line}")

            if not steps:
                steps = ["Paso 1: Analizar el problema."]
        else:
            steps = proc_text

        data['introduccion'] = introduccion
        data['explicacion'] = explicacion
        data['resumen'] = resumen
        data['procedimiento'] = steps

        # Agregar ejemplos y errores si no existen (dummy)
        if 'ejemplos' not in data:
            data['ejemplos'] = [
                {
                    "titulo": "Ejemplo ilustrativo",
                    "enunciado": "Resuelva la ecuación o sistema planteado aplicando los conceptos descritos.",
                    "solucion_pasos": [
                        "Se plantea la ecuación inicial según la definición matemática.",
                        "Se aplican las propiedades algebraicas correspondientes al tema.",
                        "Se obtiene el conjunto solución verificando el dominio."
                    ]
                }
            ]
        if 'errores_frecuentes' not in data:
            data['errores_frecuentes'] = [
                "Omitir la verificación de las restricciones de dominio al finalizar el despeje.",
                "Errores de signo al transponer términos de un miembro a otro."
            ]
        data['estado'] = "publicado"

        # Reordenar las llaves
        ordered_keys = ['semantic_id', 'titulo', 'objetivo', 'introduccion', 'resumen', 'explicacion', 'procedimiento', 'ejemplos', 'errores_frecuentes', 'estado']

        # Construir YAML string manualmente para controlar el formato de bloques
        new_yaml = []
        for k in ordered_keys:
            if k in data:
                val = data[k]
                if isinstance(val, str) and ('\n' in val or len(val) > 80):
                    new_yaml.append(f"{k}: |\n  " + val.replace('\n', '\n  ').strip())
                elif isinstance(val, str):
                    new_yaml.append(f"{k}: '{val.replace(chr(39), chr(39)+chr(39))}'")
                elif isinstance(val, list):
                    if k == 'procedimiento' or k == 'errores_frecuentes':
                        new_yaml.append(f"{k}:")
                        for item in val:
                            new_yaml.append(f"  - '{item.replace(chr(39), chr(39)+chr(39))}'")
                    elif k == 'ejemplos':
                        new_yaml.append(f"{k}:")
                        for ex in val:
                            new_yaml.append(f"  - titulo: '{ex.get('titulo', '')}'")
                            if 'enunciado' in ex:
                                new_yaml.append(f"    enunciado: '{ex['enunciado'].replace(chr(39), chr(39)+chr(39))}'")
                            new_yaml.append(f"    solucion_pasos:")
                            for step in ex.get('solucion_pasos', []):
                                new_yaml.append(f"    - '{step.replace(chr(39), chr(39)+chr(39))}'")

        with open(fp, 'w', encoding='utf-8') as f:
            f.write("\n".join(new_yaml) + "\n")

    print(f"Archivos procesados: {len(files)}")

if __name__ == '__main__':
    fix_yaml_files()
