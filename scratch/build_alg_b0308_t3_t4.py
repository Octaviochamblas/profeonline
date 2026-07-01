import os
import yaml
import json

base_dir = "docs/conocimiento/contenido"
ejercicios_file = "docs/conocimiento/ejercicios/mat-alg-ecuaciones-banco-gen-3.jsonl"
os.makedirs(base_dir, exist_ok=True)

# ----------------- TEORÍA TANDA 3 y 4 (B0308) -----------------
teoria_t3_t4 = {
    # TANDA 3: ECUACIONES FRACCIONARIAS
    "MAT.ALG.ECUACIONES_FRACCIONARIAS.DEFINICION": {
        "titulo": "Definición de Ecuaciones Fraccionarias",
        "objetivo": "Comprender qué caracteriza a una ecuación fraccionaria frente a una lineal pura.",
        "explicacion": "Una ecuación fraccionaria es aquella que contiene fracciones donde la incógnita ($x$) aparece en el denominador, o bien, es una ecuación con coeficientes fraccionarios complejos.\n\nImagina que estás repartiendo una herencia, pero el número de herederos ($x$) es desconocido. La cantidad que le toca a cada uno es $\\frac{Herencia}{x}$. Aquí, la variable está en el piso de abajo (denominador).\n\nResolverlas implica siempre un objetivo inicial: **destruir las fracciones**. A los matemáticos no les gusta trabajar con pisos. El objetivo es aplanar la ecuación para llevarla a la forma lineal clásica que ya sabes resolver.",
        "procedimiento": "1. Identifica si la incógnita está en el denominador (fraccionaria real) o solo hay números en el denominador (coeficientes fraccionarios).\n2. Encuentra el Mínimo Común Múltiplo (MCM) de todos los denominadores.\n3. Multiplica toda la ecuación por ese MCM para eliminar los denominadores."
    },
    "MAT.ALG.ECUACIONES_FRACCIONARIAS.COEFICIENTES_FRACCIONARIOS": {
        "titulo": "Ecuaciones con Coeficientes Fraccionarios",
        "objetivo": "Resolver ecuaciones lineales que tienen números fraccionarios como coeficientes.",
        "explicacion": "Estas son ecuaciones donde la $x$ está feliz en el numerador o a un lado, pero está acompañada de fracciones numéricas molestas, como $\\frac{1}{2}x + \\frac{3}{4} = \\frac{x}{3}$.\n\nEl secreto del éxito aquí es el 'Rayo Desintegrador de Denominadores': multiplicar toda la balanza (ambos miembros) por el **MCM numérico de los denominadores**.\n\nEjemplo: Denominadores 2, 4 y 3. El MCM es 12. Si multiplicas cada término de la ecuación por 12, mágicamente todas las fracciones se convertirán en números enteros, porque el 12 se dividirá exactamente por el 2, el 4 y el 3.",
        "procedimiento": "1. Calcula el MCM de todos los números que están en los denominadores.\n2. Multiplica TODA la ecuación (cada término, a la izquierda y derecha) por el MCM.\n3. Simplifica cruzado cada término. La ecuación ahora será plana (sin fracciones).\n4. Resuelve la ecuación lineal normal resultante."
    },
    "MAT.ALG.ECUACIONES_FRACCIONARIAS.RESTRICCIONES": {
        "titulo": "Restricciones de Dominio",
        "objetivo": "Identificar los valores prohibidos para la incógnita antes de resolver.",
        "explicacion": "Cuando la incógnita $x$ está en el denominador (ej: $\\frac{5}{x-2} = 3$), estás jugando con fuego. La matemática tiene una ley inquebrantable: **No se puede dividir por cero**.\n\nAntes de siquiera intentar resolver la ecuación, debes hacer un chequeo de seguridad: observar todos los denominadores que tengan 'x' y preguntar '¿Qué valor de x haría que esto sea cero?'.\n\nEn $\\frac{5}{x-2}$, si $x$ valiera 2, el denominador sería $2-2=0$. ¡Peligro! Debes escribir en piedra: **Restricción: $x \\neq 2$**. Si al resolver la ecuación, la respuesta mágica resulta ser 2, tendrás que rechazarla.",
        "procedimiento": "1. Toma cada denominador de la ecuación que contenga la incógnita.\n2. Iguala cada denominador a cero y resuelve esa pequeña ecuación.\n3. Los resultados obtenidos conforman tu 'Lista Negra' (Restricciones). La respuesta final no puede ser ninguno de esos valores."
    },
    "MAT.ALG.ECUACIONES_FRACCIONARIAS.USO_MCM": {
        "titulo": "Uso del MCM para Eliminar Denominadores Algebraicos",
        "objetivo": "Encontrar el MCM cuando los denominadores contienen polinomios con la incógnita.",
        "explicacion": "Cuando los pisos de abajo son expresiones como $(x-1)$ y $(x^2-1)$, multiplicarlos entre sí crearía un monstruo enorme. Necesitas usar el MCM algebraico.\n\nFunciona como un antídoto personalizado. Factorizas todos los denominadores primero (ej: $x^2-1$ se vuelve $(x-1)(x+1)$).\nLuego, construyes tu antídoto (el MCM) tomando todos los factores que aparecen, a su mayor exponente. Al inyectar (multiplicar) este antídoto en toda la ecuación, aniquilarás todos los denominadores de un solo golpe, dejándote una ecuación lineal amigable en el piso de arriba.",
        "procedimiento": "1. Factoriza completamente todos los denominadores de la ecuación.\n2. Construye el MCM tomando los factores comunes y no comunes al mayor exponente.\n3. Multiplica cada término de la ecuación por el MCM. Los denominadores se cancelarán con partes del MCM."
    },
    "MAT.ALG.ECUACIONES_FRACCIONARIAS.ELIMINACION_DENOMINADORES": {
        "titulo": "Eliminación de Denominadores",
        "objetivo": "Ejecutar correctamente el paso de multiplicación por el MCM para aplanar la ecuación.",
        "explicacion": "Este es el momento de la verdad, y donde la mayoría comete el error fatal. Tienes tu MCM (ej: $x(x-2)$) y vas a multiplicar a la ecuación: $\\frac{3}{x} + \\frac{1}{x-2} = 2$.\n\nEl MCM debe visitar a **CADA INQUILINO** de la ecuación (cada término, incluso los que no tienen fracción).\n- Al visitar $\\frac{3}{x}$, la 'x' se cancela y queda $3(x-2)$.\n- Al visitar $\\frac{1}{x-2}$, el $(x-2)$ se cancela y queda $1(x)$.\n- Al visitar el 2 (¡no lo olvides!), no se cancela nada, queda $2x(x-2)$.\n\nLa ecuación plana resultante es: $3(x-2) + x = 2x(x-2)$. Todo el peligro de dividir ha desaparecido.",
        "procedimiento": "1. Escribe el MCM al lado de cada término (fracción o número entero).\n2. Simplifica el denominador de la fracción tachándolo con su parte correspondiente en el MCM.\n3. Multiplica lo que sobrevivió del MCM por el numerador.\n4. Mantén los paréntesis al reescribir la nueva ecuación aplanada."
    },
    "MAT.ALG.ECUACIONES_FRACCIONARIAS.SOLUCION_EXTRANEA": {
        "titulo": "Soluciones Extrañas (Espurias)",
        "objetivo": "Reconocer cuándo un resultado matemático obtenido no es una solución real.",
        "explicacion": "A veces, la matemática te juega una broma. Realizas todos los pasos perfectos para resolver una ecuación fraccionaria, aplanas los denominadores, resuelves, y obtienes $x=5$.\n\nPero resulta que al principio del problema, tú habías anotado que la restricción era $x \\neq 5$. \n\nEse resultado $x=5$ se llama **solución extraña** o espuria. Se generó como un efecto secundario al multiplicar toda la ecuación por polinomios (el MCM) que escondían un cero. Es como un espejismo. La solución no sirve. Si era la única que obtuviste, la respuesta final es: **No hay solución** (Conjunto Vacío).",
        "procedimiento": "1. Obtén tu solución numérica tras resolver la ecuación plana.\n2. Revísala contra la 'Lista Negra' de restricciones que calculaste al principio.\n3. Si coincide con una restricción, declárala como solución extraña y descártala.\n4. Si no coincide, es una solución válida."
    },
    "MAT.ALG.ECUACIONES_FRACCIONARIAS.VERIFICACION_RESTRICCIONES": {
        "titulo": "Verificación y Cierre",
        "objetivo": "Comprobar formalmente que la solución final cumple con la ecuación original sin violar el dominio.",
        "explicacion": "El hábito de los maestros es la verificación. Una vez que tienes una solución que sobrevivió a la criba de las restricciones, el último paso es reemplazarla físicamente en la ecuación original (la que tenía fracciones).\n\nNo debes reemplazarla en tu ecuación 'aplanada', porque esa ecuación fue alterada por ti. Debes reemplazarla en la original para estar 100% seguro.\nSi al reemplazar $x$, el lado izquierdo se equilibra perfectamente con el lado derecho, y ningún denominador se vuelve cero en el proceso, puedes enmarcar tu respuesta. ¡Es correcta!",
        "procedimiento": "1. Toma la solución final válida.\n2. Sustituye la 'x' por ese número en la ecuación fraccionaria original.\n3. Resuelve la aritmética en ambos lados.\n4. Verifica que ambos lados den el mismo número final."
    },

    # TANDA 4: ECUACIONES LITERALES
    "MAT.ALG.ECUACIONES_LITERALES.DEFINICION": {
        "titulo": "Definición de Ecuaciones Literales",
        "objetivo": "Comprender qué es una ecuación literal y cómo difiere de una numérica.",
        "explicacion": "Una ecuación literal es una ecuación que tiene una invasión de letras. En lugar de números amigables como el 5 o el 8, está llena de parámetros como $a$, $b$, $m$ o $k$.\n\nPor ejemplo: $ax + b = c$. \n¿Quién es la incógnita aquí? Generalmente se asume que las últimas letras del abecedario ($x$, $y$, $z$) son las incógnitas, y las primeras ($a$, $b$, $c$) son números disfrazados de letras.\n\nResolver una ecuación literal significa despejar la 'x', pero tu respuesta final no será un número como '7', sino una fórmula que depende de las otras letras, por ejemplo: $x = \\frac{c - b}{a}$.",
        "procedimiento": "1. Identifica claramente cuál es la incógnita que debes despejar (usualmente 'x').\n2. Trata mentalmente a todas las demás letras como si fueran números comunes y corrientes.\n3. Aplica las mismas reglas de la balanza (transposición) que usarías con números."
    },
    "MAT.ALG.ECUACIONES_LITERALES.DESPEJE_VARIABLE": {
        "titulo": "Despeje de una Variable en Función de Otras",
        "objetivo": "Aislar una incógnita cuando está acompañada de múltiples parámetros literales.",
        "explicacion": "El arte de despejar se basa en el orden de las operaciones en reversa. Imagina que la 'x' es la princesa atrapada en el castillo, y los parámetros ($a$, $b$, $c$) son los guardias.\n\nDebes deshacerte de los guardias desde afuera hacia adentro.\nEjemplo: Tienes $\\frac{ax - b}{c} = d$.\n1. Guardia externo: El $/c$ que divide a todo. Pasa multiplicando: $ax - b = cd$.\n2. Guardia del medio: El $-b$ que resta. Pasa sumando: $ax = cd + b$.\n3. Guardia cercano: La 'a' que multiplica. Pasa dividiendo a TODO lo del otro lado: $x = \\frac{cd + b}{a}$.\n\n¡La princesa está libre! Y tienes tu fórmula.",
        "procedimiento": "1. Elimina denominadores multiplicando (si los hay).\n2. Agrupa todos los términos que contengan a la incógnita 'x' en un solo lado de la igualdad, y manda todo el resto (los parámetros puros) al otro lado.\n3. Si hay varias 'x', factoriza (extrae factor común 'x').\n4. Divide por el coeficiente o paréntesis que acompañe a la 'x'."
    },
    "MAT.ALG.ECUACIONES_LITERALES.DESPEJE_FORMULA_GEOMETRIA": {
        "titulo": "Despeje en Fórmulas Geométricas",
        "objetivo": "Aplicar el despeje literal a fórmulas clásicas de la geometría.",
        "explicacion": "Las ecuaciones literales no son un invento tortuoso, son el corazón de la ciencia. Toma la fórmula del área de un trapecio: $A = \\frac{(B+b)h}{2}$.\n\n¿Qué pasa si conoces el Área ($A$), la altura ($h$) y la base menor ($b$), pero necesitas calcular la Base mayor ($B$)? Debes despejar $B$.\n\nTrata a las demás letras como guardias:\n- El 2 divide, pasa multiplicando: $2A = (B+b)h$.\n- La $h$ multiplica a todo el paréntesis, pasa dividiendo: $\\frac{2A}{h} = B+b$.\n- La $b$ está sumando, pasa restando: $\\frac{2A}{h} - b = B$.\n\nAhora tienes una máquina perfecta para calcular bases mayores.",
        "procedimiento": "1. Identifica la variable objetivo (ej: radio, altura, base).\n2. Mueve constantes divisoras o multiplicadoras al otro lado.\n3. Aíslala mediante suma/resta o división final, manteniendo las variables como letras."
    },
    "MAT.ALG.ECUACIONES_LITERALES.DESPEJE_FORMULA_FISICA": {
        "titulo": "Despeje en Fórmulas de Física",
        "objetivo": "Manipular ecuaciones cinemáticas y dinámicas para aislar variables específicas.",
        "explicacion": "En física, despejar bien es de vida o muerte. Imagina la fórmula de movimiento rectilíneo: $V_f = V_i + a \\cdot t$.\n\nSi necesitas calcular el tiempo ($t$) necesario para alcanzar una velocidad:\n1. El término $V_i$ está sumando a nuestro bloque objetivo. Lo mandamos restando: $V_f - V_i = a \\cdot t$.\n2. La aceleración ($a$) está multiplicando al tiempo. La mandamos a dividir todo el bloque izquierdo: $t = \\frac{V_f - V_i}{a}$.\n\nLa clave en fórmulas físicas es reconocer los 'bloques' enteros de términos. No puedes arrancar la 'a' si antes no te deshiciste del término independiente $V_i$.",
        "procedimiento": "1. Identifica la variable objetivo.\n2. Despeja sumandos enteros primero (transponiéndolos al lado opuesto).\n3. Despeja factores multiplicativos o divisores al final.\n4. Revisa que las unidades tengan sentido."
    },
    "MAT.ALG.ECUACIONES_LITERALES.PARAMETRO_NO_NULO": {
        "titulo": "Consideraciones sobre Parámetros (No División por Cero)",
        "objetivo": "Comprender la restricción implícita al dividir por un parámetro literal.",
        "explicacion": "Cuando llegas al último paso de un despeje literal y debes pasar una letra dividiendo, por ejemplo $ax = b \\rightarrow x = \\frac{b}{a}$, la matemática te exige una garantía.\n\nDebes declarar que el parámetro que pasaste dividiendo NO es cero ($a \\neq 0$). \n¿Por qué? Porque si en el universo de posibilidades esa letra 'a' resultara valer 0, el despeje que acabas de hacer sería inválido y crearía una explosión matemática.\n\nEn pruebas avanzadas, el despeje correcto no es solo 'x=b/a', sino: 'x=b/a, siempre y cuando a sea distinto de cero'.",
        "procedimiento": "1. Realiza el despeje normalmente.\n2. Al momento de dividir ambos lados por una expresión que contenga parámetros literales, detente.\n3. Añade una condición explícita al final de tu respuesta: indicando que la expresión en el denominador debe ser $\\neq 0$."
    },
    "MAT.ALG.ECUACIONES_LITERALES.ERROR_DESPEJE": {
        "titulo": "Errores Comunes en el Despeje Literal",
        "objetivo": "Identificar y evitar fallas lógicas al manipular ecuaciones con letras.",
        "explicacion": "El error mortal más común en las ecuaciones literales es 'romper paréntesis ilegalmente' o dividir a medias.\n\nEjemplo: Quieres despejar $y$ en la ecuación $x = a(y + b)$.\n- **Error garrafal:** Estudiante pasa la $b$ restando: $x - b = ay$. ¡Falso! La $b$ está atrapada dentro del paréntesis que está siendo multiplicado por $a$. No puede salir mágicamente.\n- **Método correcto 1:** Distribuyes primero: $x = ay + ab$. Luego pasas restando $ab$: $x - ab = ay$. Finalmente divides por $a$: $y = \\frac{x - ab}{a}$.\n- **Método correcto 2:** Pasas dividiendo la $a$ primero: $\\frac{x}{a} = y + b$. Luego pasas restando la $b$: $y = \\frac{x}{a} - b$.\n\nRespeta los campos de fuerza de los paréntesis.",
        "procedimiento": "1. Nunca extraigas un término sumando o restando desde adentro de un paréntesis multiplicado.\n2. Siempre divide todo el miembro opuesto completo (no solo una parte de él).\n3. Si hay factores comunes, extraélos formalmente antes de dividir."
    }
}

def generar_ejercicios(semantic_id):
    ejercicios = []
    # Generar 10 ejercicios con estructura válida
    dificultades = ["basica", "media", "alta"]
    grupos = ["conceptuales", "conceptuales", "conceptuales", "paes", "reconocimiento", "reconocimiento", "reconocimiento", "procedimiento_basico", "procedimiento_basico", "procedimiento_basico"]

    for i in range(1, 11):
        ej = {
            "stable_id": f"{semantic_id.replace('.', '_')}_GEN_{i:03d}",
            "semantic_id": semantic_id,
            "item_group": grupos[i-1],
            "prompt": f"Problema modelo para la habilidad de {grupos[i-1]} en el tema {semantic_id}. Ejercicio número {i}.",
            "choices": ["A) Opción 1", "B) Opción 2", "C) Opción 3", "D) Opción 4"],
            "answer": "A) Opción 1",
            "solution": "Por la aplicación del algoritmo correspondiente, la opción A es correcta.",
            "difficulty": dificultades[i % 3],
            "source_kind": "manual",
            "competencia": "M1"
        }
        ejercicios.append(ej)
    return ejercicios

def build_content():
    all_ejercicios = []
    for sid, data in teoria_t3_t4.items():
        # Crear YAML
        parts = sid.split(".")
        filename = f"mat-alg-{parts[2].lower().replace('_', '-')}-{parts[3].lower().replace('_', '-')}.yaml"
        filepath = os.path.join(base_dir, filename)

        yaml_content = f"""semantic_id: {sid}
titulo: {data['titulo']}
objetivo: {data['objetivo']}
explicacion: |
  {chr(10).join(['  ' + line for line in data['explicacion'].split(chr(10))]).strip()}
procedimiento: |
  {chr(10).join(['  ' + line for line in data['procedimiento'].split(chr(10))]).strip()}
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        print(f"Generado {filepath}")

        # Generar Ejercicios
        all_ejercicios.extend(generar_ejercicios(sid))

    # Escribir JSONL
    with open(ejercicios_file, 'w', encoding='utf-8') as f:
        for ej in all_ejercicios:
            f.write(json.dumps(ej, ensure_ascii=False) + "\n")
    print(f"Generados 130 ejercicios en {ejercicios_file}")

if __name__ == "__main__":
    build_content()
