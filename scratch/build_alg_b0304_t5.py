import json
import os

YAMLS = {
    "mat-alg-mult-polinomios-multiples-polinomios.yaml": """semantic_id: "MAT.ALG.MULT_POLINOMIOS.MULTIPLES_POLINOMIOS"
titulo: "Multiplicación de tres o más polinomios"
objetivo: "Multiplicar tres o más polinomios, realizando las operaciones en pares sucesivos y reduciendo términos semejantes en cada paso."
introduccion: "Cuando tienes que multiplicar tres o más polinomios, el secreto está en ir paso a paso. Multiplica los dos primeros, reduce el resultado y luego multiplica ese nuevo polinomio por el tercero."
resumen: |
  Para multiplicar más de dos polinomios:
  
  1. Selecciona dos polinomios cualesquiera y multiplícalos usando la propiedad distributiva.
  2. Reduce los términos semejantes del producto obtenido.
  3. Multiplica el resultado simplificado por el tercer polinomio.
  4. Repite el proceso hasta haber multiplicado todos los factores.
explicacion: |
  La multiplicación de polinomios es asociativa, lo que significa que el orden en que agrupes los factores no altera el producto final. Si debes calcular $A \\cdot B \\cdot C$:
  
  Puedes hacer $(A \\cdot B) \\cdot C$ o $A \\cdot (B \\cdot C)$. 
  Generalmente, conviene operar de izquierda a derecha o buscar productos notables (como suma por su diferencia) que simplifiquen los pasos intermedios.
  
  Es crucial **reducir términos semejantes** después de cada multiplicación parcial; si no lo haces, la siguiente multiplicación tendrá demasiados términos y aumentará la probabilidad de error.
procedimiento: |
  1. Elige los dos primeros factores a multiplicar (pueden ser los más sencillos o los que formen un producto notable).
  2. Aplica la distributividad multiplicando cada término del primer polinomio por cada término del segundo.
  3. Reduce términos semejantes en el polinomio resultante.
  4. Coloca el nuevo polinomio entre paréntesis y multiplícalo por el siguiente factor.
  5. Repite hasta agotar los factores.
ejemplos:
  - title: "Producto de tres binomios"
    text: "Resuelve: $(x + 1)(x - 2)(x + 3)$"
    steps:
      - "Paso 1: Multiplica los dos primeros: $(x + 1)(x - 2) = x^2 - 2x + x - 2 = (x^2 - x - 2)$."
      - "Paso 2: Multiplica el resultado por el tercero: $(x^2 - x - 2)(x + 3)$."
      - "Distribuye $x^2$: $x^3 + 3x^2$."
      - "Distribuye $-x$: $-x^2 - 3x$."
      - "Distribuye $-2$: $-2x - 6$."
      - "Paso 3: Suma todo y reduce: $x^3 + (3-1)x^2 + (-3-2)x - 6 = x^3 + 2x^2 - 5x - 6$."
  - title: "Aprovechando productos notables"
    text: "Calcula $(x - 5)(x + 5)(x + 1)$"
    steps:
      - "Los dos primeros forman una suma por su diferencia: $(x - 5)(x + 5) = (x^2 - 25)$."
      - "Multiplicamos el resultado por el tercer factor: $(x^2 - 25)(x + 1)$."
      - "Distribuyendo: $x^3 + x^2 - 25x - 25$."
  - title: "Monomio por dos binomios"
    text: "Desarrolla $2x(x + 2)(x - 1)$"
    steps:
      - "Podemos multiplicar los binomios primero: $(x + 2)(x - 1) = x^2 + x - 2$."
      - "Luego distribuimos el monomio: $2x(x^2 + x - 2) = 2x^3 + 2x^2 - 4x$."
      - "(También se pudo distribuir $2x$ en $(x+2)$ primero, dando el mismo resultado)."
errores_frecuentes:
  - "Olvidar reducir términos semejantes después de la primera multiplicación."
  - "Distribuir el primer factor (ej. un monomio) a TODOS los paréntesis a la vez, violando la asociatividad."
  - "Perder el signo negativo de un factor intermedio."
""",
    "mat-alg-leyes-multiplicacion-propiedad-asociativa.yaml": """semantic_id: "MAT.ALG.LEYES_MULTIPLICACION.PROPIEDAD_ASOCIATIVA"
titulo: "Propiedad asociativa de la multiplicación"
objetivo: "Aplicar la propiedad asociativa en multiplicaciones algebraicas para agrupar factores de la manera más conveniente y simplificar los cálculos."
introduccion: "Cuando tienes tres factores que multiplicar, tienes la libertad de elegir cuáles dos multiplicar primero. ¡El resultado final será siempre el mismo!"
resumen: |
  La propiedad asociativa establece que la forma en que se agrupan los factores no altera el producto.
  
  Matemáticamente: $(a \\cdot b) \\cdot c = a \\cdot (b \\cdot c)$
  
  En álgebra, esta propiedad nos permite buscar agrupaciones estratégicas que generen cálculos más simples, como agrupar números con números, variables iguales o productos notables.
explicacion: |
  La asociatividad es una herramienta de optimización. No cambia *qué* estamos multiplicando, sino el *orden de los pasos intermedios*.
  
  Por ejemplo, en $5 \\cdot (2x) \\cdot 3y$:
  Si agrupamos como $(5 \\cdot 2x) \\cdot 3y$, obtenemos $10x \\cdot 3y = 30xy$.
  Si agrupamos como $5 \\cdot (2x \\cdot 3y)$, obtenemos $5 \\cdot (6xy) = 30xy$.
  El resultado es idéntico, pero a veces una ruta es mentalmente más rápida.
  
  Esto también aplica a binomios. Si tienes $x(x-2)(x+2)$, es mucho más rápido asociar los binomios primero: $x[(x-2)(x+2)] = x[x^2-4] = x^3 - 4x$, en lugar de distribuir la $x$ primero.
procedimiento: |
  Para aprovechar la propiedad asociativa:
  1. Observa todos los factores de la multiplicación.
  2. Identifica si hay dos factores que al multiplicarse produzcan un resultado sencillo (por ejemplo, coeficientes que den números redondos, o productos notables).
  3. Agrupa y multiplica esos dos factores primero.
  4. Multiplica el resultado obtenido por el factor o factores restantes.
ejemplos:
  - title: "Agrupación estratégica numérica"
    text: "Calcula $4 \\cdot (7a^2) \\cdot 25$"
    steps:
      - "Asociando $4$ y $25$: $(4 \\cdot 25) \\cdot 7a^2$."
      - "$100 \\cdot 7a^2$."
      - "$700a^2$."
      - "(Asociar $4 \\cdot 7a^2$ primero hubiera dado $28a^2$, luego multiplicar por $25$ es más difícil)."
  - title: "Agrupación con polinomios"
    text: "Desarrolla $-3(a - b)(a + b)$"
    steps:
      - "Asociamos los binomios, que forman una suma por su diferencia: $-3[(a - b)(a + b)]$."
      - "Resolvemos los binomios: $-3[a^2 - b^2]$."
      - "Distribuimos el $-3$: $-3a^2 + 3b^2$."
  - title: "Verdadero o Falso: Distribución múltiple"
    text: "Es correcto afirmar que $2(x+1)(x+3) = (2x+2)(2x+6)$."
    steps:
      - "En $(a \\cdot b \\cdot c)$, si asocias el primero con el segundo, tienes $(ab)c$."
      - "El $2$ solo debe multiplicar a UNO de los paréntesis. Al multiplicar a ambos, estás haciendo $2(x+1) \\cdot 2(x+3) = 4(x+1)(x+3)$, lo cual es el doble de lo pedido."
      - "La afirmación es Falsa."
errores_frecuentes:
  - "Multiplicar el primer coeficiente (monomio) por TODOS los paréntesis siguientes a la vez."
  - "Creer que el orden de los factores cambia el signo del resultado final."
""",
    "mat-alg-mult-polinomios-signos-agrupacion.yaml": """semantic_id: "MAT.ALG.MULT_POLINOMIOS.SIGNOS_AGRUPACION"
titulo: "Multiplicación con signos de agrupación anidados"
objetivo: "Resolver multiplicaciones algebraicas que incluyen paréntesis, corchetes y llaves, respetando la jerarquía desde adentro hacia afuera."
introduccion: "A veces los polinomios vienen envueltos en múltiples 'capas' protectoras: paréntesis, corchetes y llaves. La clave está en desarmarlos pacientemente desde la capa más interna hacia la más externa."
resumen: |
  Cuando una expresión contiene signos de agrupación anidados (uno dentro de otro), se deben eliminar desde adentro hacia afuera.
  
  La secuencia habitual es:
  1. Paréntesis circulares $( \\quad )$
  2. Corchetes $[ \\quad ]$
  3. Llaves $\\{ \\quad \\}$
  
  En cada nivel, se aplican las operaciones indicadas (multiplicación o distribución de signos) y se reducen términos semejantes antes de pasar al nivel superior.
explicacion: |
  Los signos de agrupación indican el orden estricto de las operaciones. Trabajar de adentro hacia afuera asegura que no alteremos la lógica del problema original.
  
  Si tenemos $2x[3 - (x + 1)]$:
  No podemos distribuir el $2x$ al $3$ y al paréntesis sin cuidado. Debemos resolver el interior del corchete primero.
  Dentro del corchete, el signo menos afecta al paréntesis: $3 - x - 1$, lo que se reduce a $2 - x$.
  Ahora el corchete es simplemente $[2 - x]$.
  Finalmente, multiplicamos: $2x(2 - x) = 4x - 2x^2$.
procedimiento: |
  1. Localiza el signo de agrupación más interno (generalmente un paréntesis circular).
  2. Efectúa las operaciones (multiplicación, ley de signos) para eliminar ese signo interno.
  3. Reduce términos semejantes dentro del nuevo nivel (el corchete o llave que quedó).
  4. Repite el proceso para el siguiente nivel de agrupación.
  5. Continúa hasta que no queden signos de agrupación.
ejemplos:
  - title: "Paréntesis y corchetes"
    text: "Desarrolla: $a[2a - 3(a - 2)]$"
    steps:
      - "Identificamos el paréntesis interno: $(a - 2)$."
      - "Distribuimos el $-3$: $a[2a - 3a + 6]$."
      - "Reducimos dentro del corchete ($2a - 3a = -a$): $a[-a + 6]$."
      - "Multiplicamos el exterior por el corchete: $-a^2 + 6a$."
  - title: "Tres niveles de anidación"
    text: "Calcula: $2\\{x - [y + 2(x - y)]\\}$"
    steps:
      - "Paréntesis interno: $2(x - y) = 2x - 2y$."
      - "La expresión queda: $2\\{x - [y + 2x - 2y]\\}$."
      - "Reducimos el corchete ($y - 2y = -y$): $2\\{x - [2x - y]\\}$."
      - "El signo menos frente al corchete invierte signos: $2\\{x - 2x + y\\}$."
      - "Reducimos dentro de la llave: $2\\{-x + y\\}$."
      - "Multiplicamos finalmente: $-2x + 2y$."
  - title: "Verdadero o Falso: Orden de resolución"
    text: "En la expresión $3[x(x+1)]$, es incorrecto distribuir primero el $3$ hacia la $x$."
    steps:
      - "Por jerarquía, se podría resolver el corchete primero: $3[x^2+x] = 3x^2+3x$."
      - "Sin embargo, por asociatividad, $(3 \\cdot x)(x+1) = 3x(x+1) = 3x^2+3x$."
      - "Ambos caminos son válidos matemáticamente si solo hay multiplicación, pero el algoritmo estándar pide resolver desde adentro."
      - "Técnicamente, no es 'incorrecto' por la asociatividad, pero la afirmación pedida evalúa la rigidez."
      - "Respuesta: Falso, porque la asociatividad permite $(3x)(x+1)$."
errores_frecuentes:
  - "Intentar eliminar los corchetes o llaves exteriores antes que los paréntesis internos."
  - "Olvidar cambiar los signos de todos los términos cuando un paréntesis interno está precedido por un signo menos."
  - "Multiplicar términos que solo se están sumando o restando dentro de un corchete."
""",
    "mat-alg-leyes-multiplicacion-propiedad-distributiva.yaml": """semantic_id: "MAT.ALG.LEYES_MULTIPLICACION.PROPIEDAD_DISTRIBUTIVA"
titulo: "Propiedad distributiva generalizada"
objetivo: "Aplicar la propiedad distributiva de forma exhaustiva para multiplicar polinomios de cualquier cantidad de términos."
introduccion: "La propiedad distributiva es el corazón de la multiplicación algebraica. Es como un sistema de correos donde cada término del primer bloque debe enviar una carta a cada término del segundo bloque, ¡sin excepciones!"
resumen: |
  La propiedad distributiva de la multiplicación con respecto a la suma establece que un factor se reparte multiplicando a cada sumando:
  $a(b + c) = ab + ac$
  
  Generalizada a polinomios, significa que **cada término del primer polinomio debe multiplicarse por cada término del segundo polinomio**.
  
  Si un polinomio tiene $m$ términos y el otro tiene $n$ términos, antes de reducir semejantes se generarán exactamente $m \\times n$ términos parciales.
explicacion: |
  La distributividad garantiza que estemos considerando todas las combinaciones posibles entre los factores.
  
  Si tenemos el binomio $(a + b)$ multiplicando al trinomio $(x + y + z)$, la propiedad exige que:
  1. El término $a$ multiplique a $x$, $y$, y $z$.
  2. El término $b$ multiplique a $x$, $y$, y $z$.
  
  El resultado crudo será: $ax + ay + az + bx + by + bz$.
  Este proceso es riguroso: un polinomio de 3 términos por uno de 4 términos generará inicialmente $12$ multiplicaciones individuales. Saltarse una sola de estas arruinará el resultado final.
procedimiento: |
  Para realizar una distribución completa sin omitir términos:
  1. Toma el primer término del primer polinomio.
  2. Multiplícalo ordenadamente por cada uno de los términos del segundo polinomio.
  3. Pasa al segundo término del primer polinomio y repite el proceso.
  4. Continúa hasta haber utilizado todos los términos del primer polinomio.
  5. Escribe todos los productos parciales obtenidos en una sola línea.
  6. Agrupa y suma (reduce) los términos semejantes.
ejemplos:
  - title: "Binomio por trinomio"
    text: "Desarrolla $(2x - 1)(x^2 + 3x - 5)$"
    steps:
      - "Distribuye el $2x$: $(2x)(x^2) + (2x)(3x) + (2x)(-5) = 2x^3 + 6x^2 - 10x$."
      - "Distribuye el $-1$: $(-1)(x^2) + (-1)(3x) + (-1)(-5) = -x^2 - 3x + 5$."
      - "Junta todo: $2x^3 + 6x^2 - 10x - x^2 - 3x + 5$."
      - "Reduce semejantes: $2x^3 + 5x^2 - 13x + 5$."
  - title: "Conteo de términos (Verificación)"
    text: "Si multiplicas $(a+b+c)(x+y+z)$, ¿cuántos términos obtienes antes de reducir?"
    steps:
      - "El primer polinomio tiene 3 términos."
      - "El segundo polinomio tiene 3 términos."
      - "El número de productos es $3 \\times 3 = 9$ términos."
  - title: "Polinomio por binomio"
    text: "Calcula $(x^3 - x + 2)(x + 4)$"
    steps:
      - "También puedes distribuir el binomio sobre el trinomio: $(x^3)(x) + (x^3)(4) + (-x)(x) + (-x)(4) + (2)(x) + (2)(4)$."
      - "$x^4 + 4x^3 - x^2 - 4x + 2x + 8$."
      - "Resultado final: $x^4 + 4x^3 - x^2 - 2x + 8$."
errores_frecuentes:
  - "Olvidar multiplicar un término del primer polinomio por alguno del segundo."
  - "Multiplicar el primero con el primero y el segundo con el segundo, ignorando los cruzados (ej. $(a+b)(x+y) = ax + by$)."
  - "Arrastrar incorrectamente los signos negativos durante las multiplicaciones parciales."
""",
    "mat-alg-mult-polinomios-exponentes-literales.yaml": """semantic_id: "MAT.ALG.MULT_POLINOMIOS.EXPONENTES_LITERALES"
titulo: "Multiplicación de polinomios con exponentes literales"
objetivo: "Multiplicar polinomios cuyos exponentes contienen variables (letras), aplicando las propiedades de las potencias para sumar dichas expresiones algebraicas."
introduccion: "A veces, los exponentes no son simples números como el 2 o el 3, sino que tienen letras (como $x+1$). ¡No te asustes! Las reglas son las mismas: para multiplicar potencias de igual base, se copian las bases y se suman algebraicamente los exponentes."
resumen: |
  Cuando los exponentes de los polinomios contienen letras, la operación sigue la misma regla fundamental de los exponentes:
  $a^m \\cdot a^n = a^{m+n}$
  
  En este caso, la suma $m+n$ será una suma de expresiones algebraicas. Se deben reducir los términos semejantes en el exponente resultante.
explicacion: |
  Si multiplicamos monomios como $x^{a}$ y $x^{a+2}$, la base $x$ se mantiene y sumamos los exponentes: $a + (a+2) = 2a + 2$. El resultado es $x^{2a+2}$.
  
  Cuando trabajamos con polinomios enteros que tienen exponentes literales, aplicamos la propiedad distributiva igual que siempre, pero en cada producto parcial realizaremos una suma algebraica en los exponentes.
  
  Es muy importante alinear y ordenar los resultados según sus exponentes literales para poder reducir correctamente los términos semejantes al final del ejercicio.
procedimiento: |
  1. Multiplica coeficiente con coeficiente aplicando regla de signos.
  2. Mantiene la variable base.
  3. Suma algebraicamente los exponentes literales correspondientes a esa variable.
  4. Escribe el nuevo exponente simplificado.
  5. Repite para cada producto parcial de la distribución.
  6. Agrupa y reduce los términos cuyos exponentes literales y partes literales completas sean exactamente iguales.
ejemplos:
  - title: "Suma simple de exponentes"
    text: "Multiplica $3x^a$ por $2x^{a+1}$"
    steps:
      - "Multiplica coeficientes: $3 \\cdot 2 = 6$."
      - "Suma exponentes: $a + (a + 1) = 2a + 1$."
      - "Resultado: $6x^{2a+1}$."
  - title: "Monomio por binomio"
    text: "Desarrolla: $-2y^{n-1}(y^{n+2} - y^{n-3})$"
    steps:
      - "Primer término: $(-2)(1)y^{(n-1)+(n+2)} = -2y^{2n+1}$."
      - "Segundo término: $(-2)(-1)y^{(n-1)+(n-3)} = +2y^{2n-4}$."
      - "Resultado: $-2y^{2n+1} + 2y^{2n-4}$."
  - title: "Verdadero o Falso: Multiplicación de exponentes literales"
    text: "Al multiplicar $x^{2n}$ por $x^{3n}$, el resultado es $x^{6n^2}$."
    steps:
      - "La regla es sumar exponentes, no multiplicarlos."
      - "El exponente resultante debe ser $2n + 3n = 5n$."
      - "Por tanto, el resultado es $x^{5n}$ y la afirmación es Falsa."
errores_frecuentes:
  - "Multiplicar los exponentes literales en lugar de sumarlos."
  - "No sumar los términos independientes dentro de los exponentes (ej. $x^{a+2} \\cdot x^{a+3} = x^{2a+5}$, no $x^{2a+6}$)."
  - "Confundir términos que no son semejantes porque sus exponentes literales difieren (ej. sumar $x^{n+1}$ con $x^{n-1}$)."
""",
    "mat-alg-mult-polinomios-coeficientes-separados.yaml": """semantic_id: "MAT.ALG.MULT_POLINOMIOS.COEFICIENTES_SEPARADOS"
titulo: "Multiplicación por coeficientes separados (Opcional avanzado)"
objetivo: "Aplicar el método de coeficientes separados para multiplicar polinomios ordenados y completos de una variable, abstrayendo las letras para optimizar el cálculo."
introduccion: "Cuando manejamos polinomios con una sola letra, ordenados y sin saltos en sus exponentes, podemos usar un truco: multiplicar usando solo sus coeficientes numéricos. ¡Es como hacer una multiplicación aritmética tradicional!"
resumen: |
  El método de coeficientes separados simplifica la multiplicación de polinomios de una sola variable.
  
  Condiciones:
  1. Ambos polinomios deben tener una sola variable.
  2. Ambos deben estar ordenados en forma descendente respecto a esa variable.
  3. Si falta algún exponente intermedio, se debe rellenar con un coeficiente de cero.
  
  El método consiste en extraer solo los números, multiplicarlos como si fueran números enteros (pero sin llevar decenas) y luego reasignar las variables al resultado.
explicacion: |
  Este método abstrae la variable (por ejemplo, $x$) y se enfoca en los coeficientes. Si tenemos $2x^2 + 3x - 1$ y $x + 4$, los coeficientes son $(2, 3, -1)$ y $(1, 4)$.
  
  Multiplicamos como en la escuela:
        2   3  -1
      x     1   4
      -----------
        8  12  -4  (multiplicando por 4)
    2   3  -1      (multiplicando por 1 y corriendo un espacio)
    ---------------
    2  11  11  -4
    
  Para colocar las variables de nuevo, determinamos el grado máximo sumando los grados de los factores originales: grado $2 +$ grado $1 = $ grado $3$.
  El resultado es: $2x^3 + 11x^2 + 11x - 4$.
procedimiento: |
  1. Verifica que los polinomios estén en orden descendente y completa con ceros los grados faltantes.
  2. Escribe solo los coeficientes de ambos polinomios, uno debajo del otro.
  3. Multiplica el primer coeficiente del factor inferior por todos los superiores y anota la fila.
  4. Multiplica el segundo coeficiente del factor inferior, anotando los resultados en la fila siguiente desplazados una columna a la derecha.
  5. Repite hasta agotar el factor inferior.
  6. Suma las columnas verticalmente.
  7. Reasigna las variables en orden descendente, partiendo desde la suma de los grados mayores de los factores originales.
ejemplos:
  - title: "Polinomios completos"
    text: "Multiplica $(3x^2 - x + 2)(2x - 1)$ usando coeficientes separados."
    steps:
      - "Coeficientes P1: $3, -1, 2$."
      - "Coeficientes P2: $2, -1$."
      - "Multiplicando por $-1$:  $-3,   1, -2$."
      - "Multiplicando por $2$:    $6, -2,  4$."
      - "Alineamos y sumamos:"
      - "      $3   -1    2$"
      - "    x      $2   -1$"
      - "    --------------"
      - "     $-3    1   -2$"
      - " $6   -2    4$"
      - " -----------------"
      - " $6   -5    5   -2$"
      - "El grado máximo es $2+1=3$. Resultado: $6x^3 - 5x^2 + 5x - 2$."
  - title: "Polinomio incompleto (requiere cero)"
    text: "Multiplica $(x^3 - 2)(x + 3)$."
    steps:
      - "El primer polinomio no tiene grado 2 ni 1. Coeficientes: $1, 0, 0, -2$."
      - "Segundo polinomio: $1, 3$."
      - "Multiplicando por $3$:  $3, 0, 0, -6$."
      - "Multiplicando por $1$:  $1, 0, 0, -2$."
      - "Suma:"
      - "       $1   0   0  -2$"
      - "     x         $1   3$"
      - "     ----------------"
      - "       $3   0   0  -6$"
      - "   $1   0   0  -2$"
      - "   ------------------"
      - "   $1   3   0  -2  -6$"
      - "Grado máximo $3+1=4$. Resultado: $1x^4 + 3x^3 + 0x^2 - 2x - 6 = x^4 + 3x^3 - 2x - 6$."
errores_frecuentes:
  - "Olvidar colocar un coeficiente de $0$ en los términos faltantes."
  - "No desplazar las filas hacia la izquierda al cambiar de multiplicador, perdiendo la alineación de grados."
  - "Llevar la reserva (decenas) a la columna siguiente como en la suma aritmética, lo cual es inválido en álgebra."
""",
    "mat-alg-mult-polinomios-modelo-area-binomios.yaml": """semantic_id: "MAT.ALG.MULT_POLINOMIOS.MODELO_AREA_BINOMIOS"
titulo: "Modelo de área para multiplicación de binomios"
objetivo: "Utilizar el modelo geométrico de área (cuadro de Punnett algebraico) para visualizar y calcular la multiplicación de binomios."
introduccion: "A veces el álgebra se ve mejor en un dibujo. Si piensas en la multiplicación como el área de un rectángulo, calcular $(x+3)(x+2)$ es simplemente encontrar el área de un terreno dividido en cuatro parcelas. ¡Visual y sin errores!"
resumen: |
  El modelo de área representa la multiplicación de dos binomios como el cálculo del área de un rectángulo dividido en cuatro cuadrantes (una cuadrícula de $2 \\times 2$).
  
  - La longitud de la base es el primer binomio, separada en sus dos términos.
  - La altura es el segundo binomio, separada en sus dos términos.
  - El área de cada uno de los cuatro cuadrantes interiores se calcula multiplicando su base por su altura correspondiente.
  - El área total es la suma de las cuatro áreas interiores, reduciendo los términos semejantes (generalmente en la diagonal).
explicacion: |
  Para $(a + b)(c + d)$:
  Dibujas un rectángulo grande dividido en 4.
  Arriba escribes $a$ sobre la primera columna y $b$ sobre la segunda.
  A la izquierda escribes $c$ junto a la primera fila y $d$ junto a la segunda.
  
  Las cuatro áreas internas serán:
  - Celda sup-izq: $a \\cdot c$
  - Celda sup-der: $b \\cdot c$
  - Celda inf-izq: $a \\cdot d$
  - Celda inf-der: $b \\cdot d$
  
  La suma de estas 4 celdas es $ac + bc + ad + bd$, lo cual es exactamente el resultado de la propiedad distributiva. Si los binomios son, por ejemplo, $(x+4)$ y $(x+2)$, las celdas diagonales ($4x$ y $2x$) serán semejantes y se sumarán visualmente muy fácil.
procedimiento: |
  1. Dibuja un rectángulo dividido en 4 celdas cuadradas/rectangulares ($2 \\times 2$).
  2. Coloca los términos del primer binomio (incluyendo sus signos) en el borde superior de las columnas.
  3. Coloca los términos del segundo binomio (incluyendo sus signos) en el borde izquierdo de las filas.
  4. Rellena cada celda multiplicando la columna por su respectiva fila.
  5. Suma todos los contenidos de las celdas y reduce los términos semejantes para obtener el polinomio final.
ejemplos:
  - title: "Modelo con números positivos"
    text: "Multiplica $(x + 5)(x + 3)$ usando el modelo de área."
    steps:
      - "Columnas: $x$ y $+5$. Filas: $x$ y $+3$."
      - "Celda sup-izq ($x \\cdot x$): $x^2$"
      - "Celda sup-der ($5 \\cdot x$): $5x$"
      - "Celda inf-izq ($x \\cdot 3$): $3x$"
      - "Celda inf-der ($5 \\cdot 3$): $15$"
      - "Suma total: $x^2 + 5x + 3x + 15$."
      - "Reducción: $x^2 + 8x + 15$."
  - title: "Modelo con signos negativos"
    text: "Aplica el modelo para $(2x - 1)(x + 4)$"
    steps:
      - "Columnas: $2x$ y $-1$. Filas: $x$ y $+4$."
      - "Celda sup-izq: $(2x)(x) = 2x^2$"
      - "Celda sup-der: $(-1)(x) = -x$"
      - "Celda inf-izq: $(2x)(4) = 8x$"
      - "Celda inf-der: $(-1)(4) = -4$"
      - "Suma de términos: $2x^2 - x + 8x - 4$."
      - "Resultado: $2x^2 + 7x - 4$."
  - title: "Verdadero o Falso: Diagonal semejante"
    text: "En el modelo de área para $(ax + b)(cx + d)$, los términos de la diagonal que va desde abajo-izquierda hacia arriba-derecha siempre serán términos semejantes."
    steps:
      - "Celda inf-izq: base $ax \\cdot$ altura $d = adx$."
      - "Celda sup-der: base $b \\cdot$ altura $cx = bcx$."
      - "Ambos términos contienen $x$ a la potencia $1$, por lo tanto, son semejantes."
      - "La afirmación es Verdadera."
errores_frecuentes:
  - "Olvidar arrastrar el signo negativo hacia los bordes del modelo, lo que resulta en sumas en lugar de restas."
  - "Sumar los bordes en lugar de multiplicarlos para llenar las celdas."
  - "No reducir las diagonales semejantes en el resultado final."
""",
    "mat-alg-mult-polinomios-modelo-volumen-trinomial.yaml": """semantic_id: "MAT.ALG.MULT_POLINOMIOS.MODELO_VOLUMEN_TRINOMIAL"
titulo: "Expansión a modelos mayores (Rectángulo de 3x2)"
objetivo: "Extender el modelo de área para visualizar y calcular la multiplicación de un binomio por un trinomio."
introduccion: "El método de la cuadrícula no sirve solo para binomios. Si un polinomio tiene más términos, simplemente añadimos más columnas o filas a nuestro dibujo. Un trinomio por un binomio será un rectángulo de 3 columnas y 2 filas."
resumen: |
  El modelo de cuadrícula o tabla se puede extender a polinomios de cualquier tamaño.
  
  Para multiplicar un trinomio por un binomio:
  - Dibuja una tabla de $3 \\times 2$ (o $2 \\times 3$).
  - Coloca los 3 términos del trinomio en las columnas (bordes superiores).
  - Coloca los 2 términos del binomio en las filas (bordes laterales).
  - Calcula el área de las 6 celdas resultantes.
  - Suma y reduce los términos semejantes (que generalmente se alinean en diagonales).
explicacion: |
  Visualizar $(x^2 + 2x - 3)(x + 4)$ en una tabla asegura que realicemos exactamente las $3 \\times 2 = 6$ multiplicaciones parciales que la propiedad distributiva exige, eliminando casi por completo el riesgo de olvidar un término.
  
  La gran ventaja de este método es que auto-organiza los productos parciales. Si los polinomios están ordenados por grado, las diagonales de la cuadrícula contendrán automáticamente los términos semejantes, lo que hace la suma final extremadamente rápida y segura.
procedimiento: |
  1. Dibuja una tabla con tantas columnas como términos tenga el primer polinomio y tantas filas como tenga el segundo.
  2. Escribe los términos (con su signo) a lo largo de las columnas y filas.
  3. Multiplica la fila por la columna correspondiente en cada una de las celdas interiores.
  4. Extrae los términos de la tabla, sumando las diagonales si contienen términos semejantes.
  5. Escribe el polinomio final ordenado.
ejemplos:
  - title: "Trinomio por binomio"
    text: "Multiplica $(x^2 - 3x + 2)(2x + 1)$ con cuadrícula."
    steps:
      - "Tabla de $3 \\times 2$."
      - "Columnas: $x^2$, $-3x$, $+2$. Filas: $2x$, $+1$."
      - "Fila 1 (por $2x$): $2x^3$, $-6x^2$, $+4x$."
      - "Fila 2 (por $+1$): $x^2$, $-3x$, $+2$."
      - "Diagonal $x^2$: $-6x^2 + x^2 = -5x^2$."
      - "Diagonal $x$: $4x - 3x = x$."
      - "Polinomio final: $2x^3 - 5x^2 + x + 2$."
  - title: "Con variables distintas"
    text: "Resuelve $(a + b - c)(a + c)$"
    steps:
      - "Columnas: $a$, $b$, $-c$. Filas: $a$, $c$."
      - "Fila 1 (por $a$): $a^2$, $ab$, $-ac$."
      - "Fila 2 (por $c$): $ac$, $bc$, $-c^2$."
      - "En este caso, notamos los semejantes: $-ac$ y $ac$ se cancelan ($0$)."
      - "Suma total: $a^2 + ab + bc - c^2$."
errores_frecuentes:
  - "Pensar que las diagonales siempre son semejantes, incluso si los polinomios originales no estaban ordenados."
  - "Crear una tabla de tamaño incorrecto (ej. $2 \\times 2$ omitiendo un término del trinomio)."
""",
    "mat-alg-mult-polinomios-distributiva-incompleta-error.yaml": """semantic_id: "MAT.ALG.MULT_POLINOMIOS.DISTRIBUTIVA_INCOMPLETA_ERROR"
titulo: "Error común: Distributiva incompleta en polinomios"
objetivo: "Reconocer y corregir el error clásico de multiplicar solo los términos de igual grado al multiplicar dos polinomios."
introduccion: "Un error muy tentador al multiplicar $(x + 2)(x + 3)$ es simplemente multiplicar la $x$ con la $x$, el $2$ con el $3$, y decir que el resultado es $x^2 + 6$. ¡Faltan todas las multiplicaciones cruzadas!"
resumen: |
  La distributiva incompleta (o 'falsa distributiva') ocurre cuando un estudiante multiplica término a término sin cruzar, ignorando la propiedad distributiva real.
  
  - Forma incorrecta frecuente: $(a + b)(c + d) = ac + bd$
  - Forma correcta: $(a + b)(c + d) = ac + ad + bc + bd$
  
  Para evitarlo, utiliza un esquema de flechas o el método FOIL/cuadrícula que obligue a realizar todas las multiplicaciones cruzadas.
explicacion: |
  Este error es conceptualmente similar a creer que $(x+y)^2 = x^2 + y^2$. Nace de intentar tratar la multiplicación como una simple suma vertical, donde operamos columna por columna.
  
  En aritmética, esto sería como decir que $23 \\times 12$ se calcula multiplicando $2 \\times 1$ y $3 \\times 2$, lo que daría $26$. ¡El resultado real es $276$!
  
  En álgebra, si multiplicas $(2x - 3)(x + 4)$ y obtienes $2x^2 - 12$, estás ignorando que el $2x$ también debe multiplicar al $4$, y el $-3$ debe multiplicar a la $x$. Se pierden los términos del medio ($8x - 3x = 5x$).
procedimiento: |
  Para diagnosticar y corregir este error:
  1. Si ves una expresión como $(A + B)(C + D) = AC + BD$, estás ante un caso de distributiva incompleta.
  2. Recupera los términos perdidos trazando las flechas de los productos 'exteriores' e 'interiores'.
  3. Agrega los productos faltantes: $A \\cdot D$ y $B \\cdot C$.
  4. Suma todo y reduce para obtener el polinomio correcto.
ejemplos:
  - title: "Diagnóstico del error"
    text: "Identifica el error: $(3x + 1)(x - 5) = 3x^2 - 5$."
    steps:
      - "El error es la distributiva incompleta: el estudiante hizo $(3x)(x)$ y $(1)(-5)$."
      - "Faltan los cruces: $(3x)(-5) = -15x$ y $(1)(x) = x$."
      - "El resultado correcto es $3x^2 - 14x - 5$."
  - title: "Corrección paso a paso"
    text: "Si un alumno dice que $(m^2 + n)(m - n) = m^3 - n^2$, ¿qué términos le faltan?"
    steps:
      - "Desarrollamos completo: $(m^2)(m) + (m^2)(-n) + (n)(m) + (n)(-n)$."
      - "Resultado correcto: $m^3 - m^2n + mn - n^2$."
      - "Al alumno le faltaron los términos cruzados: $-m^2n + mn$."
  - title: "Verdadero o Falso: Cantidad de términos"
    text: "El error de distributiva incompleta en binomios produce un resultado con dos términos, mientras que la expansión correcta genera siempre cuatro términos antes de reducir."
    steps:
      - "La distributiva incompleta calcula $ac + bd$, que son dos términos."
      - "La expansión correcta de binomio $\\times$ binomio calcula $ac + ad + bc + bd$, que son cuatro términos."
      - "La afirmación es Verdadera."
errores_frecuentes:
  - "Creer que la multiplicación es análoga a la suma de polinomios, operando solo los que están 'en la misma posición'."
  - "Confundir la suma por su diferencia $(x+a)(x-a) = x^2-a^2$ (donde los del medio se cancelan) con una regla general aplicable a todos los binomios."
"""
}

def generate_exercises():
    exercises = []
    
    # 1. MULTIPLES_POLINOMIOS
    sid = "MAT.ALG.MULT_POLINOMIOS.MULTIPLES_POLINOMIOS"
    # CONC
    exercises.append({"stable_id": "MP-MP-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Al multiplicar tres polinomios, ¿cuál es el procedimiento estándar más recomendable?", "choices": ["A) Multiplicar los dos primeros, reducir semejantes y luego multiplicar el resultado por el tercero.", "B) Multiplicar el primer término de cada polinomio entre sí.", "C) Sumar los dos primeros y multiplicar por el tercero.", "D) Distribuir cada término del primer polinomio en todos los otros polinomios simultáneamente."], "correct_answer": "A) Multiplicar los dos primeros, reducir semejantes y luego multiplicar el resultado por el tercero.", "solution_steps": "La propiedad asociativa dicta agrupar de a dos, resolver y continuar con el siguiente.", "paes_style": False})
    exercises.append({"stable_id": "MP-MP-CONC-2", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "¿Por qué es crucial reducir términos semejantes después de multiplicar los dos primeros polinomios, antes de avanzar al tercero?", "choices": ["A) Para disminuir la cantidad de multiplicaciones en el siguiente paso y evitar errores.", "B) Porque si no se hace, el resultado final cambia de valor.", "C) Para cambiar el grado del polinomio.", "D) Porque es una regla estricta que anula la asociatividad si no se cumple."], "correct_answer": "A) Para disminuir la cantidad de multiplicaciones en el siguiente paso y evitar errores.", "solution_steps": "No reduce su valor matemático, pero reduce drásticamente la explosión de términos, facilitando el cálculo humano.", "paes_style": False})
    exercises.append({"stable_id": "MP-MP-CONC-3", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Si debes calcular $P(x) \\cdot Q(x) \\cdot R(x)$, y sabes que $Q(x)$ y $R(x)$ son una suma por su diferencia, ¿qué orden de multiplicación te conviene más?", "choices": ["A) Multiplicar primero $Q(x)$ y $R(x)$ para aprovechar el producto notable.", "B) Siempre operar estrictamente de izquierda a derecha.", "C) Multiplicar $P(x)$ con $Q(x)$ primero para no alterar los signos.", "D) El orden no importa en absoluto para la dificultad del cálculo."], "correct_answer": "A) Multiplicar primero $Q(x)$ y $R(x)$ para aprovechar el producto notable.", "solution_steps": "La asociatividad permite elegir el orden. Resolver un producto notable primero siempre simplifica la expresión rápidamente.", "paes_style": False})
    # REC
    exercises.append({"stable_id": "MP-MP-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Dada la expresión $(x)(x+1)(x-1)$, identifica el paso intermedio tras operar los dos últimos factores.", "choices": ["A) $x(x^2 - 1)$", "B) $(x^2 + x)(x-1)$", "C) $x(x^2 + 1)$", "D) $x(x - 1)$"], "correct_answer": "A) $x(x^2 - 1)$", "solution_steps": "Los dos últimos forman $(x+1)(x-1) = x^2 - 1$. Por ende queda $x(x^2 - 1)$.", "paes_style": False})
    # PROC
    exercises.append({"stable_id": "MP-MP-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula el producto completo: $2x(x + 3)(x - 2)$", "choices": ["A) $2x^3 + 2x^2 - 12x$", "B) $2x^3 + 6x^2 - 12x$", "C) $2x^3 + x^2 - 6x$", "D) $2x^3 - 2x^2 - 12x$"], "correct_answer": "A) $2x^3 + 2x^2 - 12x$", "solution_steps": "Binomios: $(x+3)(x-2) = x^2 + x - 6$. Por $2x$: $2x(x^2 + x - 6) = 2x^3 + 2x^2 - 12x$.", "paes_style": False})
    exercises.append({"stable_id": "MP-MP-PROC-2", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Desarrolla: $(a-1)(a+1)(a+2)$", "choices": ["A) $a^3 + 2a^2 - a - 2$", "B) $a^3 - a^2 - a + 2$", "C) $a^3 + a^2 - a - 2$", "D) $a^3 + 2a^2 + a - 2$"], "correct_answer": "A) $a^3 + 2a^2 - a - 2$", "solution_steps": "$(a-1)(a+1) = a^2 - 1$. Multiplicado por $(a+2)$: $(a^2 - 1)(a+2) = a^3 + 2a^2 - a - 2$.", "paes_style": False})
    exercises.append({"stable_id": "MP-MP-PROC-3", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Calcula el volumen de una caja rectangular con dimensiones $(x)$, $(x+4)$ y $(x-4)$.", "choices": ["A) $x^3 - 16x$", "B) $x^3 - 16$", "C) $x^3 + 16x$", "D) $x^3 - 4x^2 + 16$"], "correct_answer": "A) $x^3 - 16x$", "solution_steps": "Volumen = $x(x+4)(x-4)$. Primero binomios: $x^2 - 16$. Luego por $x$: $x^3 - 16x$.", "paes_style": False})
    # PAES
    exercises.append({"stable_id": "MP-MP-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M2", "prompt": "Si el lado de un cubo se incrementa en $2$, en $3$ y se reduce en $1$ en sus tres dimensiones, la expresión polinómica del nuevo volumen en función del lado original $x$ será:", "choices": ["A) $x^3 + 4x^2 + x - 6$", "B) $x^3 + 6x^2 - x - 6$", "C) $x^3 + 4x^2 - x + 6$", "D) $x^3 + 5x^2 + x - 6$"], "correct_answer": "A) $x^3 + 4x^2 + x - 6$", "solution_steps": "$(x+2)(x+3)(x-1)$. $(x^2+5x+6)(x-1) = x^3 - x^2 + 5x^2 - 5x + 6x - 6 = x^3 + 4x^2 + x - 6$.", "paes_style": True})
    exercises.append({"stable_id": "MP-MP-PAES-2", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "¿Cuál es el coeficiente de $x^2$ en el desarrollo de $(x-2)(x-3)(x-4)$?", "choices": ["A) $-9$", "B) $9$", "C) $-26$", "D) $24$"], "correct_answer": "A) $-9$", "solution_steps": "$(x-2)(x-3) = x^2 - 5x + 6$. $(x^2 - 5x + 6)(x - 4) = x^3 - 4x^2 - 5x^2 + 20x + 6x - 24$. El término de $x^2$ es $-4x^2 - 5x^2 = -9x^2$. Coeficiente $-9$.", "paes_style": True})
    exercises.append({"stable_id": "MP-MP-PAES-3", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "La expresión $(1-x)(1+x)(1+x^2)$ es equivalente a:", "choices": ["A) $1 - x^4$", "B) $1 + x^4$", "C) $1 - x^3$", "D) $x^4 - 1$"], "correct_answer": "A) $1 - x^4$", "solution_steps": "Los primeros dos: $1 - x^2$. Multiplicado por el tercero: $(1 - x^2)(1 + x^2)$. Es otra suma por diferencia: $1^2 - (x^2)^2 = 1 - x^4$.", "paes_style": True})

    # 2. LEYES_MULTIPLICACION.PROPIEDAD_ASOCIATIVA
    sid = "MAT.ALG.LEYES_MULTIPLICACION.PROPIEDAD_ASOCIATIVA"
    exercises.append({"stable_id": "LM-PA-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Qué enuncia formalmente la propiedad asociativa de la multiplicación?", "choices": ["A) $(a \\cdot b) \\cdot c = a \\cdot (b \\cdot c)$", "B) $a(b + c) = ab + ac$", "C) $a \\cdot b = b \\cdot a$", "D) $a \\cdot 1 = a$"], "correct_answer": "A) $(a \\cdot b) \\cdot c = a \\cdot (b \\cdot c)$", "solution_steps": "La asociatividad indica que el orden de agrupación no altera el producto final.", "paes_style": False})
    exercises.append({"stable_id": "LM-PA-CONC-2", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "En la resolución de $5 \\cdot (x-1) \\cdot 2x$, ¿qué agrupación facilita más rápido el cálculo mental debido a la asociatividad?", "choices": ["A) $(5 \\cdot 2x) \\cdot (x-1)$", "B) $(5 \\cdot (x-1)) \\cdot 2x$", "C) Distribuir el 5, luego distribuir el 2x.", "D) Multiplicar $5 \\cdot x \\cdot 2$."], "correct_answer": "A) $(5 \\cdot 2x) \\cdot (x-1)$", "solution_steps": "Agrupar los monomios $5 \\cdot 2x$ da $10x$, un multiplicador muy fácil de distribuir luego en $(x-1)$.", "paes_style": False})
    exercises.append({"stable_id": "LM-PA-CONC-3", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "¿Por qué un estudiante podría equivocarse al hacer $3(x+2)(x-4) = (3x+6)(3x-12)$?", "choices": ["A) Porque distribuyó el $3$ a ambos paréntesis a la vez, rompiendo la asociatividad.", "B) Porque sumó en lugar de multiplicar.", "C) Porque no redujo términos semejantes.", "D) Porque alteró el orden de los factores."], "correct_answer": "A) Porque distribuyó el $3$ a ambos paréntesis a la vez, rompiendo la asociatividad.", "solution_steps": "La forma correcta es agrupar: $[3(x+2)](x-4)$ o $3[(x+2)(x-4)]$. Multiplicar ambos implica insertar el factor dos veces.", "paes_style": False})
    exercises.append({"stable_id": "LM-PA-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Selecciona la expresión que demuestra un uso correcto de la asociatividad en $2(a+b)(a-b)$.", "choices": ["A) $2[(a+b)(a-b)]$", "B) $(2a+2b)(2a-2b)$", "C) $2a(b)(a-b)$", "D) $(a+b)(2a-b)$"], "correct_answer": "A) $2[(a+b)(a-b)]$", "solution_steps": "Se asocian los dos binomios juntos para resolver el producto notable primero.", "paes_style": False})
    exercises.append({"stable_id": "LM-PA-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Aplica asociatividad para resolver inteligentemente: $-4y \\cdot (x^2+y^2) \\cdot (-0.25y)$", "choices": ["A) $x^2y^2 + y^4$", "B) $4x^2y^2 - y^4$", "C) $-x^2y^2 - y^4$", "D) $x^2y + y^3$"], "correct_answer": "A) $x^2y^2 + y^4$", "solution_steps": "Asociamos los monomios: $(-4y) \\cdot (-0.25y) = 1y^2$. Luego $y^2(x^2+y^2) = x^2y^2 + y^4$.", "paes_style": False})
    exercises.append({"stable_id": "LM-PA-PROC-2", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula el resultado de $2x \\cdot 3x \\cdot (x - 5)$.", "choices": ["A) $6x^3 - 30x^2$", "B) $6x^2 - 30x$", "C) $5x^3 - 15x^2$", "D) $6x^3 - 5$"], "correct_answer": "A) $6x^3 - 30x^2$", "solution_steps": "Asociando monomios: $2x \\cdot 3x = 6x^2$. Luego $6x^2(x - 5) = 6x^3 - 30x^2$.", "paes_style": False})
    exercises.append({"stable_id": "LM-PA-PROC-3", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Desarrolla la expresión: $5(x - 3)(x + 3)$.", "choices": ["A) $5x^2 - 45$", "B) $5x^2 - 15$", "C) $25x^2 - 45$", "D) $5x^2 - 9$"], "correct_answer": "A) $5x^2 - 45$", "solution_steps": "Asociando binomios: $5[x^2 - 9]$. Distribuyendo: $5x^2 - 45$.", "paes_style": False})
    exercises.append({"stable_id": "LM-PA-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Un volumen se calcula como $\\frac{1}{3} \\cdot \pi r^2 \\cdot (3h + 6)$. Mediante agrupaciones de la asociatividad, una expresión equivalente más compacta es:", "choices": ["A) $\pi r^2 (h + 2)$", "B) $\pi r^2 (3h + 2)$", "C) $\\frac{\pi}{3} r^2 h + 6$", "D) $\pi r^2 h + 2$"], "correct_answer": "A) $\pi r^2 (h + 2)$", "solution_steps": "Podemos asociar $\\frac{1}{3}$ con el paréntesis: $\\pi r^2 \\cdot [\\frac{1}{3}(3h + 6)] = \pi r^2(h + 2)$.", "paes_style": True})
    exercises.append({"stable_id": "LM-PA-PAES-2", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Si $A = 2(x+1)$, $B = 3(x-1)$ y $C = x$, encuentra el producto $A \\cdot B \\cdot C$.", "choices": ["A) $6x^3 - 6x$", "B) $6x^3 - x$", "C) $6x^3 - 6$", "D) $5x^3 - 5x$"], "correct_answer": "A) $6x^3 - 6x$", "solution_steps": "$A \\cdot B \\cdot C = 2(x+1) \\cdot 3(x-1) \\cdot x$. Asociando números: $6x$. Binomios: $x^2-1$. Total: $6x(x^2-1) = 6x^3 - 6x$.", "paes_style": True})
    exercises.append({"stable_id": "LM-PA-PAES-3", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Para $x = \\sqrt{2}$, ¿cuál es el valor de $x \\cdot (x-\\sqrt{2}) \\cdot (x+\\sqrt{2})$?", "choices": ["A) $0$", "B) $2\\sqrt{2}$", "C) $2$", "D) $-2$"], "correct_answer": "A) $0$", "solution_steps": "Asociando, obtenemos $x(x^2 - 2)$. Sustituyendo $\\sqrt{2}$: $\\sqrt{2}((\\sqrt{2})^2 - 2) = \\sqrt{2}(2-2) = 0$. (También porque un factor es cero).", "paes_style": True})

    # 3. SIGNOS_AGRUPACION
    sid = "MAT.ALG.MULT_POLINOMIOS.SIGNOS_AGRUPACION"
    exercises.append({"stable_id": "MP-SA-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Al resolver operaciones combinadas con corchetes y paréntesis anidados, el orden correcto de eliminación es:", "choices": ["A) Desde los signos más internos hacia los más externos.", "B) Desde los signos más externos hacia los más internos.", "C) De izquierda a derecha indiferentemente.", "D) Todos los signos se eliminan simultáneamente."], "correct_answer": "A) Desde los signos más internos hacia los más externos.", "solution_steps": "La jerarquía exige resolver siempre el bloque más profundo (interior) primero.", "paes_style": False})
    exercises.append({"stable_id": "MP-SA-CONC-2", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Si tienes la expresión $- [2x(x-1)]$, el signo menos exterior:", "choices": ["A) Afectará a todos los términos resultantes de resolver el corchete.", "B) Multiplica solo al $2x$, pero no afecta al paréntesis.", "C) Desaparece al multiplicar el interior.", "D) Solo afecta al primer término final."], "correct_answer": "A) Afectará a todos los términos resultantes de resolver el corchete.", "solution_steps": "Primero se resuelve $2x(x-1) = 2x^2-2x$, y luego el menos exterior invierte todo: $-2x^2+2x$.", "paes_style": False})
    exercises.append({"stable_id": "MP-SA-CONC-3", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "¿Qué error conceptual se comete al decir que $2x - [x + 3(x-1)] = 2x - x + 3x - 3$?", "choices": ["A) No distribuir el signo menos del corchete a los términos resultantes de la multiplicación interior.", "B) Sumar las $x$ incorrectamente.", "C) Multiplicar $3$ por $x$ y no por $1$.", "D) Quitar los corchetes antes de multiplicar."], "correct_answer": "A) No distribuir el signo menos del corchete a los términos resultantes de la multiplicación interior.", "solution_steps": "Interior del corchete: $x + 3x - 3 = 4x - 3$. Con el menos exterior debe ser $2x - (4x - 3) = -2x + 3$.", "paes_style": False})
    exercises.append({"stable_id": "MP-SA-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Selecciona el desarrollo parcial correcto de la expresión $3x[2 - (x+4)]$ luego de eliminar el paréntesis interior.", "choices": ["A) $3x[2 - x - 4]$", "B) $3x[2 - x + 4]$", "C) $3x[-x - 2]$", "D) $6x - 3x^2 + 12x$"], "correct_answer": "A) $3x[2 - x - 4]$", "solution_steps": "El menos cambia signos: $-(x+4) = -x-4$. Corchete: $[2-x-4]$.", "paes_style": False})
    exercises.append({"stable_id": "MP-SA-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Simplifica la expresión: $2a[a - 3(a + 2)]$", "choices": ["A) $-4a^2 - 12a$", "B) $4a^2 - 12a$", "C) $-4a^2 + 12a$", "D) $-2a^2 - 6a$"], "correct_answer": "A) $-4a^2 - 12a$", "solution_steps": "Corchete: $a - 3a - 6 = -2a - 6$. Multiplicar: $2a(-2a - 6) = -4a^2 - 12a$.", "paes_style": False})
    exercises.append({"stable_id": "MP-SA-PROC-2", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Calcula y reduce: $x - \\{2x + x[x - (x - 1)]\\}$", "choices": ["A) $-2x - x^2$", "B) $-x - x^2$", "C) $x - x^2$", "D) $-2x + x^2$"], "correct_answer": "A) $-2x - x^2$", "solution_steps": "Paréntesis: $x - x + 1 = 1$. Multiplicado por x exterior al par.: $x(1) = x$. Corchete/llave: $\\{2x + x\\} = 3x$. Exterior: $x - 3x = -2x$. Wait, el $x[...]$ multiplica. Sí, $x(1) = x$. Pero hay $x^2$ en las opciones. Corrigiendo: $x[x-(x-1)] = x(1) = x$. Result: $x - \\{2x+x\\} = -2x$. Las alternativas están mal estructuradas para el cálculo... ajustaré el problema a $x[x-(x-x^2)]$.", "paes_style": False})
    # Fix the above step in the real array
    exercises[-1]["prompt"] = "Calcula y reduce: $x - \\{2x + [x - x(x - 1)]\\}$"
    exercises[-1]["solution_steps"] = "Paréntesis: $x(x-1) = x^2-x$. Corchete: $x - (x^2-x) = 2x - x^2$. Llave: $2x + 2x - x^2 = 4x - x^2$. Exterior: $x - (4x - x^2) = x - 4x + x^2 = x^2 - 3x$."
    exercises[-1]["choices"] = ["A) $x^2 - 3x$", "B) $-x^2 - 3x$", "C) $x^2 + 3x$", "D) $x^2 - x$"]
    exercises[-1]["correct_answer"] = "A) $x^2 - 3x$"

    exercises.append({"stable_id": "MP-SA-PROC-3", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Desarrolla: $- [ -a(a - b) - b(b - a) ]$", "choices": ["A) $a^2 - 2ab + b^2$", "B) $a^2 + b^2$", "C) $-a^2 - b^2$", "D) $a^2 + 2ab + b^2$"], "correct_answer": "A) $a^2 - 2ab + b^2$", "solution_steps": "Corchete: $-a^2 + ab - b^2 + ab = -a^2 + 2ab - b^2$. Menos exterior invierte: $a^2 - 2ab + b^2$.", "paes_style": False})
    exercises.append({"stable_id": "MP-SA-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M2", "prompt": "Al reducir la expresión $3m - [2m^2 - m(m - 3)]$, obtenemos un polinomio cuyo coeficiente del término lineal es:", "choices": ["A) $0$", "B) $3$", "C) $6$", "D) $-3$"], "correct_answer": "A) $0$", "solution_steps": "Corchete: $2m^2 - m^2 + 3m = m^2 + 3m$. Todo: $3m - (m^2 + 3m) = 3m - m^2 - 3m = -m^2$. El término lineal (con $m$) se cancela, su coeficiente es 0.", "paes_style": True})
    exercises.append({"stable_id": "MP-SA-PAES-2", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Si $P(x) = x[2 - (x+1)]$ y $Q(x) = -[x^2 - 2x]$, ¿cuál es el valor de $P(x) - Q(x)$?", "choices": ["A) $-x$", "B) $-3x$", "C) $x$", "D) $x^2 - x$"], "correct_answer": "A) $-x$", "solution_steps": "$P(x) = x[1-x] = x-x^2$. $Q(x) = -x^2+2x$. $P-Q = (x-x^2) - (-x^2+2x) = x-x^2+x^2-2x = -x$.", "paes_style": True})
    exercises.append({"stable_id": "MP-SA-PAES-3", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Un área total $A$ se calcula restando al área mayor $(2x)(3x)$ el área menor delimitada por $x[x - 2(x-1)]$. La expresión final de $A$ es:", "choices": ["A) $7x^2 - 2x$", "B) $5x^2 - 2x$", "C) $7x^2 + 2x$", "D) $5x^2 + 2x$"], "correct_answer": "A) $7x^2 - 2x$", "solution_steps": "Menor: $x[x - 2x + 2] = x[-x + 2] = -x^2 + 2x$. Mayor: $6x^2$. Resta: $6x^2 - (-x^2 + 2x) = 6x^2 + x^2 - 2x = 7x^2 - 2x$.", "paes_style": True})

    # 4. PROPIEDAD_DISTRIBUTIVA
    sid = "MAT.ALG.LEYES_MULTIPLICACION.PROPIEDAD_DISTRIBUTIVA"
    exercises.append({"stable_id": "LM-PD-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "La propiedad distributiva garantiza que al multiplicar un polinomio de $m$ términos por uno de $n$ términos, antes de cualquier reducción de semejantes, tendremos:", "choices": ["A) $m \\times n$ términos.", "B) $m + n$ términos.", "C) $m^n$ términos.", "D) $m - n$ términos."], "correct_answer": "A) $m \\times n$ términos.", "solution_steps": "Cada uno de los $m$ términos se multiplica por cada uno de los $n$ términos, dando $m \\times n$ productos.", "paes_style": False})
    exercises.append({"stable_id": "LM-PD-CONC-2", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Si en la distributiva omites multiplicar el último término del primer polinomio por el último del segundo polinomio, ¿qué consecuencia geométrica o algebraica inmediata tiene?", "choices": ["A) Se pierde el término constante (independiente) si los polinomios estaban ordenados.", "B) Se pierde el término de mayor grado.", "C) El grado total del polinomio disminuye.", "D) Todos los signos cambian."], "correct_answer": "A) Se pierde el término constante (independiente) si los polinomios estaban ordenados.", "solution_steps": "En polinomios ordenados, los últimos términos suelen ser los independientes. Omitir su producto pierde esa constante pura.", "paes_style": False})
    exercises.append({"stable_id": "LM-PD-CONC-3", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Al expandir $(a+b+c)(x+y+z+w)$, ¿qué afirmación es correcta sobre el proceso?", "choices": ["A) Se deben generar 12 productos cruzados en total.", "B) Se puede sumar $(a+x)$, $(b+y)$, etc.", "C) Se obtienen 7 términos.", "D) Solo se multiplican las mismas letras con las mismas letras."], "correct_answer": "A) Se deben generar 12 productos cruzados en total.", "solution_steps": "Polinomio de 3 por polinomio de 4. $3 \\times 4 = 12$ términos resultantes.", "paes_style": False})
    exercises.append({"stable_id": "LM-PD-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Cuál es el desarrollo crudo correcto (sin reducción) de $(x+1)(y-2)$?", "choices": ["A) $xy - 2x + y - 2$", "B) $xy - 2$", "C) $xy + y - 2$", "D) $x^2y - 2$"], "correct_answer": "A) $xy - 2x + y - 2$", "solution_steps": "$x \\cdot y = xy$, $x \\cdot -2 = -2x$, $1 \\cdot y = y$, $1 \\cdot -2 = -2$.", "paes_style": False})
    exercises.append({"stable_id": "LM-PD-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula y reduce: $(2x - 3)(x^2 + 4x - 1)$", "choices": ["A) $2x^3 + 5x^2 - 14x + 3$", "B) $2x^3 + 8x^2 - 14x + 3$", "C) $2x^3 - 5x^2 - 2x + 3$", "D) $2x^3 + 5x^2 - 2x - 3$"], "correct_answer": "A) $2x^3 + 5x^2 - 14x + 3$", "solution_steps": "$(2x)(x^2+4x-1) = 2x^3+8x^2-2x$. $(-3)(x^2+4x-1) = -3x^2-12x+3$. Sumando: $2x^3 + 5x^2 - 14x + 3$.", "paes_style": False})
    exercises.append({"stable_id": "LM-PD-PROC-2", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Desarrolla el producto de dos trinomios: $(x^2 - x + 1)(x^2 + x + 1)$", "choices": ["A) $x^4 + x^2 + 1$", "B) $x^4 - x^2 + 1$", "C) $x^4 + 2x^2 + 1$", "D) $x^4 + x^3 + x^2 + 1$"], "correct_answer": "A) $x^4 + x^2 + 1$", "solution_steps": "9 productos. $x^4+x^3+x^2 -x^3-x^2-x +x^2+x+1$. Se cancelan los $x^3$ y los $x$. Queda $x^4 + x^2 + 1$.", "paes_style": False})
    exercises.append({"stable_id": "LM-PD-PROC-3", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Halla el producto: $(m - n)(m^2 + mn + n^2)$", "choices": ["A) $m^3 - n^3$", "B) $m^3 + n^3$", "C) $m^3 - 2mn + n^3$", "D) $m^3 - m^2n - n^3$"], "correct_answer": "A) $m^3 - n^3$", "solution_steps": "Distribuyendo: $m^3+m^2n+mn^2 - m^2n-mn^2-n^3$. Se cancelan los centrales y queda la diferencia de cubos.", "paes_style": False})
    exercises.append({"stable_id": "LM-PD-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M2", "prompt": "Si el polinomio $P(x) = (ax + b)(cx^2 + dx + e)$ tiene grado 3, y calculamos su expansión, el coeficiente de $x^2$ corresponderá a la expresión:", "choices": ["A) $ad + bc$", "B) $ac + bd$", "C) $ae + bd$", "D) $bc + de$"], "correct_answer": "A) $ad + bc$", "solution_steps": "El término cuadrático se forma al multiplicar $(ax)(dx) = adx^2$ y $(b)(cx^2) = bcx^2$. Por tanto, el coeficiente es $ad + bc$.", "paes_style": True})
    exercises.append({"stable_id": "LM-PD-PAES-2", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Se sabe que al multiplicar $(x^2 - ax + 2)(x - 3)$, el coeficiente de $x$ resulta ser $11$. ¿Cuál es el valor de $a$?", "choices": ["A) $3$", "B) $-3$", "C) $1$", "D) $-1$"], "correct_answer": "A) $3$", "solution_steps": "Término en $x$: $(-ax)(-3) = 3ax$; $(2)(x) = 2x$. Suma: $3ax + 2x = (3a + 2)x$. Si $3a + 2 = 11 \\Rightarrow 3a = 9 \\Rightarrow a = 3$.", "paes_style": True})
    exercises.append({"stable_id": "LM-PD-PAES-3", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "¿Cuántos términos semejantes deberán sumarse o restarse al desarrollar $(a+b+c)^2$ como producto de dos trinomios idénticos?", "choices": ["A) Se formarán 3 pares de términos semejantes (los dobles productos).", "B) Se formarán 4 pares de semejantes.", "C) No hay términos semejantes.", "D) Todos los términos son semejantes."], "correct_answer": "A) Se formarán 3 pares de términos semejantes (los dobles productos).", "solution_steps": "$(a+b+c)(a+b+c) = a^2+ab+ac + ba+b^2+bc + ca+cb+c^2$. Semejantes: $ab$ y $ba$, $ac$ y $ca$, $bc$ y $cb$. 3 pares en total ($2ab, 2ac, 2bc$).", "paes_style": True})

    # 5. EXPONENTES_LITERALES
    sid = "MAT.ALG.MULT_POLINOMIOS.EXPONENTES_LITERALES"
    exercises.append({"stable_id": "MP-EL-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Al multiplicar potencias de igual base con exponentes algebraicos, la operación sobre los exponentes corresponde a:", "choices": ["A) Una suma algebraica de polinomios o expresiones.", "B) Una multiplicación de polinomios.", "C) Dejar el exponente de mayor grado.", "D) Una división de exponentes."], "correct_answer": "A) Una suma algebraica de polinomios o expresiones.", "solution_steps": "Conserva la base y suma algebraicamente los exponentes (ej: $(x+1) + (x-1)$).", "paes_style": False})
    exercises.append({"stable_id": "MP-EL-CONC-2", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "¿Es posible reducir como términos semejantes a $3x^{a+1}$ y $-2x^{a+2}$?", "choices": ["A) No, porque sus exponentes algebraicos son distintos.", "B) Sí, el resultado es $x^{2a+3}$.", "C) Sí, pero solo si $a=1$.", "D) No, porque los coeficientes son de distinto signo."], "correct_answer": "A) No, porque sus exponentes algebraicos son distintos.", "solution_steps": "Para ser semejantes, tanto la base como el exponente completo deben ser idénticos. $a+1 \\neq a+2$.", "paes_style": False})
    exercises.append({"stable_id": "MP-EL-CONC-3", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Si el factor externo es $x^{2a}$ y uno de los términos interiores es $1$, el producto resultante será:", "choices": ["A) $x^{2a}$", "B) $x^{2a+1}$", "C) $x^{2a+a}$", "D) $x^{0}$"], "correct_answer": "A) $x^{2a}$", "solution_steps": "El $1$ es el elemento neutro de la multiplicación. $x^{2a} \\cdot 1 = x^{2a}$. (No se suma $1$ al exponente porque no es $x^1$, es $x^0$).", "paes_style": False})
    exercises.append({"stable_id": "MP-EL-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Determina el exponente final al realizar $x^{m-3} \\cdot x^{m+5}$.", "choices": ["A) $2m + 2$", "B) $m^2 - 15$", "C) $2m - 15$", "D) $m + 2$"], "correct_answer": "A) $2m + 2$", "solution_steps": "Suma: $(m - 3) + (m + 5) = 2m + 2$.", "paes_style": False})
    exercises.append({"stable_id": "MP-EL-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Multiplica: $2x^a (x^{a+1} - 3x^a + 4)$", "choices": ["A) $2x^{2a+1} - 6x^{2a} + 8x^a$", "B) $2x^{a^2+a} - 6x^{a^2} + 8x^a$", "C) $2x^{2a+1} - 6x^a + 8x$", "D) $2x^{2a+1} - 5x^{2a} + 8x^a$"], "correct_answer": "A) $2x^{2a+1} - 6x^{2a} + 8x^a$", "solution_steps": "$(2)(1)x^{a+a+1} = 2x^{2a+1}$. $(2)(-3)x^{a+a} = -6x^{2a}$. $(2)(4)x^a = 8x^a$.", "paes_style": False})
    exercises.append({"stable_id": "MP-EL-PROC-2", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Calcula y reduce: $(x^n + 1)(x^n - 1)$", "choices": ["A) $x^{2n} - 1$", "B) $x^{n^2} - 1$", "C) $x^{2n} - 2x^n + 1$", "D) $x^{2n}$"], "correct_answer": "A) $x^{2n} - 1$", "solution_steps": "Suma por su diferencia: $(x^n)^2 - (1)^2 = x^{n+n} - 1 = x^{2n} - 1$.", "paes_style": False})
    exercises.append({"stable_id": "MP-EL-PROC-3", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Desarrolla: $(a^{x+1} - a^{x})(a^2 + a)$", "choices": ["A) $a^{x+3} - a^{x+1}$", "B) $a^{x+3} + a^{x+1}$", "C) $a^{2x+3} - a^{2x+1}$", "D) $a^{x+3} - a^{x}$"], "correct_answer": "A) $a^{x+3} - a^{x+1}$", "solution_steps": "$a^{x+1+2} + a^{x+1+1} - a^{x+2} - a^{x+1} = a^{x+3} + a^{x+2} - a^{x+2} - a^{x+1}$. Se reducen los del medio. Resultado: $a^{x+3} - a^{x+1}$.", "paes_style": False})
    exercises.append({"stable_id": "MP-EL-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M2", "prompt": "Si en la expansión de $(2x^k - 3)(x^k + 5)$ el término central se reduce a $7x^3$, ¿cuál es el valor de $k$?", "choices": ["A) $3$", "B) $6$", "C) $1.5$", "D) $4$"], "correct_answer": "A) $3$", "solution_steps": "El producto es $2x^{2k} + 10x^k - 3x^k - 15 = 2x^{2k} + 7x^k - 15$. El término central es $7x^k$. Como nos dicen que es $7x^3$, entonces $k=3$.", "paes_style": True})
    exercises.append({"stable_id": "MP-EL-PAES-2", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "¿Cuál es la expresión factorizada de $m^{2a+2} + m^{2a+1}$ luego de extraer como factor común al monomio de menor grado?", "choices": ["A) $m^{2a+1}(m + 1)$", "B) $m^{2a}(m^2 + m)$", "C) $m^{a+1}(m^{a+1} + m^a)$", "D) $m^{2a+1}(m)$"], "correct_answer": "A) $m^{2a+1}(m + 1)$", "solution_steps": "Revertimos la distribución. El menor grado es $2a+1$. Dividiendo obtenemos: $m^{(2a+2)-(2a+1)} + 1 = m^1 + 1$. Luego: $m^{2a+1}(m + 1)$.", "paes_style": True})
    exercises.append({"stable_id": "MP-EL-PAES-3", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Calcula el coeficiente del término en $x^{3n}$ en el desarrollo de $(x^n - 2)(x^{2n} + 2x^n + 4)$.", "choices": ["A) $1$", "B) $0$", "C) $-8$", "D) $2$"], "correct_answer": "A) $1$", "solution_steps": "Esto es la diferencia de cubos: $(x^n)^3 - (2)^3 = x^{3n} - 8$. El coeficiente de $x^{3n}$ es $1$.", "paes_style": True})

    # Write files
    for yaml_filename, yaml_content in YAMLS.items():
        with open(f"docs/conocimiento/contenido/{yaml_filename}", "w", encoding="utf-8") as f:
            f.write(yaml_content)
    print(f"Creados {len(YAMLS)} yamls T5...")
    
    jsonl_filename = "docs/conocimiento/ejercicios/mat-alg-multiplicacion-banco-gen-5.jsonl"
    with open(jsonl_filename, "w", encoding="utf-8") as f:
        for ex in exercises:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"{jsonl_filename} con {len(exercises)} ejercicios T5")

if __name__ == "__main__":
    generate_exercises()
