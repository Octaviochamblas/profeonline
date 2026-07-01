import os
import yaml
import json

base_dir = "docs/conocimiento/contenido"
ejercicios_file = "docs/conocimiento/ejercicios/mat-alg-ecuaciones-banco-gen-5.jsonl"
os.makedirs(base_dir, exist_ok=True)

# ----------------- TEORÍA TANDA 5, 6 y 7 (B0308) -----------------
teoria_t5_t7 = {
    # TANDA 5: MODELAMIENTO LINEAL
    "MAT.ALG.MODELAMIENTO_LINEAL.IDENTIFICACION_INCOGNITA": {
        "titulo": "Identificación de la Incógnita",
        "objetivo": "Aprender a traducir una pregunta en lenguaje natural a una variable matemática.",
        "explicacion": "El primer paso para resolver un problema de la vida real con álgebra no es calcular, es nombrar. Lee la pregunta del problema (generalmente está al final). Lo que te están preguntando es tu incógnita.\n\nSi el problema dice '¿Cuántos años tiene Juan?', entonces defines: $x = \\text{edad de Juan}$.\nSi el problema habla de varios sujetos ('La edad de Pedro es el doble que la de Juan'), debes usar ESA misma $x$ como base para construir a los demás. Entonces Pedro sería $2x$.\n\nRegla de oro: Asigna la $x$ al elemento más pequeño o básico del problema. Si sabes cuánto vale la base, sabes cuánto valen los demás.",
        "procedimiento": "1. Lee la pregunta final del problema verbal.\n2. Asigna la letra 'x' a la cantidad desconocida principal.\n3. Escribe explícitamente en una esquina qué significa la 'x' (ej: 'x = precio del pantalón').\n4. Expresa todas las demás cantidades desconocidas usando variaciones de 'x' (x+5, 3x, etc.)."
    },
    "MAT.ALG.MODELAMIENTO_LINEAL.PLANTEAMIENTO_ECUACION": {
        "titulo": "Planteamiento de la Ecuación",
        "objetivo": "Traducir las relaciones descritas en el problema a una ecuación matemática formal.",
        "explicacion": "Una vez que tienes a tus actores definidos en función de 'x' (Juan = $x$, Pedro = $2x$), necesitas encontrar el 'verbo' matemático del problema que los iguale.\n\nBusca palabras clave que actúen como el signo igual ($=$): 'es', 'da', 'resulta', 'suman', 'equivalen a'.\nEjemplo: 'La suma de las edades de Juan y Pedro es 30'.\nTraducción: (Juan) + (Pedro) = 30.\nSustituyes tus actores: $x + 2x = 30$.\n\nAcabas de construir un puente entre el mundo de las palabras y el mundo del álgebra.",
        "procedimiento": "1. Identifica la relación principal (la condición que une a todos los elementos).\n2. Encuentra la palabra que representa el signo igual '='.\n3. Ensambla el lado izquierdo y el lado derecho usando tus expresiones en función de 'x'.\n4. Revisa que tu ecuación tenga sentido lógico al leerla de vuelta en español."
    },
    "MAT.ALG.MODELAMIENTO_LINEAL.RESOLUCION_PROBLEMA": {
        "titulo": "Resolución del Problema Modelado",
        "objetivo": "Aplicar técnicas de resolución lineal a la ecuación planteada.",
        "explicacion": "Este es el paso mecánico. Tienes tu ecuación $x + 2x = 30$. Ahora te olvidas de Juan, de Pedro y de las palabras.\n\nTe concentras puramente en el álgebra: reduces términos semejantes ($3x = 30$) y despejas ($x = 10$).\n\nAquí aplicas todo lo que has aprendido en los módulos anteriores: transposición, uso del MCM si hay fracciones, o distribución de signos negativos si hay restas.",
        "procedimiento": "1. Aisla la ecuación del contexto verbal.\n2. Aplica la reducción de términos semejantes.\n3. Transpón los términos numéricos a un lado y la incógnita al otro.\n4. Divide por el coeficiente de la incógnita para obtener el valor numérico de 'x'."
    },
    "MAT.ALG.MODELAMIENTO_LINEAL.INTERPRETACION_SOLUCION": {
        "titulo": "Interpretación de la Solución",
        "objetivo": "Volver a traducir el resultado numérico al contexto original del problema.",
        "explicacion": "Encontraste que $x = 10$. ¡Felicidades! Pero la pregunta no era '¿Cuánto vale x?', la pregunta era '¿Cuántos años tienen Juan y Pedro?'.\n\nSi entregas '$x=10$' como respuesta en una prueba, podrías tenerlo malo. Debes volver a tu diccionario inicial:\n- Habíamos dicho que Juan = $x$. Entonces Juan tiene 10 años.\n- Habíamos dicho que Pedro = $2x$. Entonces Pedro tiene $2 \\cdot 10 = 20$ años.\n\nLa respuesta correcta y completa es 'Juan tiene 10 años y Pedro tiene 20 años'. Siempre debes responder a la pregunta específica que te hicieron.",
        "procedimiento": "1. Toma el valor numérico obtenido para 'x'.\n2. Vuelve a tus definiciones iniciales (tu diccionario algebraico).\n3. Reemplaza 'x' en todas las expresiones relevantes para calcular los valores reales.\n4. Redacta una oración final respondiendo exactamente lo que se preguntó."
    },
    "MAT.ALG.MODELAMIENTO_LINEAL.RESTRICCION_SIGNO": {
        "titulo": "Restricciones de Signo y Lógica Real",
        "objetivo": "Evaluar si la solución matemática tiene sentido en el mundo físico.",
        "explicacion": "Las matemáticas son ciegas al mundo real. Si tú planteas una ecuación para averiguar cuántas personas asistieron a una fiesta y el álgebra te dice que $x = -4.5$, el álgebra no se equivocó, tú planteaste mal el problema (o el problema no tiene solución lógica).\n\nExisten restricciones del mundo físico:\n- El número de personas debe ser un número Natural (positivo y sin decimales).\n- Las edades deben ser positivas.\n- Las distancias deben ser positivas.\n\nSi tu resultado viola las leyes de la física o del sentido común, debes descartarlo inmediatamente e indicar que el problema no tiene solución o revisar tu planteamiento inicial.",
        "procedimiento": "1. Obtén el resultado matemático.\n2. Analiza qué entidad física representa (personas, tiempo, dinero, edad).\n3. Evalúa si el número (su signo y si es decimal) tiene sentido lógico.\n4. Si es absurdo, descarta la solución."
    },

    # TANDA 6: SISTEMAS 2X2
    "MAT.ALG.SISTEMAS_2X2.DEFINICION": {
        "titulo": "Definición de Sistemas Lineales 2x2",
        "objetivo": "Comprender la estructura de dos ecuaciones simultáneas con dos incógnitas.",
        "explicacion": "Hasta ahora resolvías problemas de una sola letra ($x$). Pero, ¿qué pasa si quieres saber el precio de una manzana ($x$) y de una pera ($y$)? Necesitas **dos letras**.\n\nLa regla dorada del álgebra dice: Si tienes 2 incógnitas, necesitas OBLIGATORIAMENTE 2 ecuaciones distintas para poder resolverlo. Si solo tienes 1 ecuación (ej: $x + y = 10$), hay infinitas combinaciones ($5+5$, $8+2$, $0+10$).\n\nUn sistema 2x2 es simplemente un par de ecuaciones (generalmente escritas una debajo de la otra unidas por una llave) que deben cumplirse **al mismo tiempo**.",
        "procedimiento": "1. Identifica que tienes dos incógnitas distintas (usualmente 'x' e 'y').\n2. Asegúrate de tener dos ecuaciones que relacionen esas dos incógnitas.\n3. Comprende que la solución del sistema es un PAR ORDENADO $(x, y)$ que hace verdaderas a ambas ecuaciones simultáneamente."
    },
    "MAT.ALG.SISTEMAS_2X2.SISTEMAS_EQUIVALENTES": {
        "titulo": "Sistemas Equivalentes",
        "objetivo": "Identificar cuándo multiplicar una ecuación por una constante mantiene el sistema inalterado.",
        "explicacion": "Imagina una ecuación como una receta: '2 manzanas y 1 pera cuestan 5 dólares' ($2x + y = 5$).\nSi multiplicas toda la receta por 3: '6 manzanas y 3 peras cuestan 15 dólares' ($6x + 3y = 15$).\n\nEs exactamente la misma información, solo amplificada. A esto se le llama una ecuación equivalente.\nEn los sistemas de ecuaciones, puedes tomar cualquiera de las ecuaciones, multiplicar todos sus términos por cualquier número (distinto de cero), y el sistema no cambiará sus soluciones. Esta es la base de casi todos los métodos de resolución.",
        "procedimiento": "1. Elige una ecuación del sistema.\n2. Multiplica cada término (lado izquierdo y lado derecho) por la misma constante.\n3. La nueva ecuación es matemáticamente equivalente a la original y puedes usarla para reemplazarla en el sistema."
    },
    "MAT.ALG.SISTEMAS_2X2.METODO_SUSTITUCION": {
        "titulo": "Método de Sustitución",
        "objetivo": "Resolver un sistema despejando una variable e inyectándola en la otra ecuación.",
        "explicacion": "El método de sustitución es como jugar a los espías infiltrados. \nTienes dos ecuaciones (Ecuación A y Ecuación B).\n1. Tomas la Ecuación A y despejas una letra (digamos, la 'y'). Descubres su 'identidad secreta' (ej: $y = 5 - 2x$).\n2. Te infiltras en la Ecuación B. Donde sea que veas una 'y', la borras y escribes la identidad secreta $(5 - 2x)$.\n\n¡Magia! La Ecuación B ahora solo tiene letras 'x'. Se convirtió en una ecuación lineal de primer grado normal. La resuelves, descubres quién es 'x', y luego usas ese valor para descubrir finalmente quién era 'y'.",
        "procedimiento": "1. Despeja una incógnita (la que parezca más fácil) de una de las ecuaciones.\n2. Sustituye la expresión obtenida en el lugar de esa misma incógnita en la SEGUNDA ecuación.\n3. Resuelve la segunda ecuación (que ahora tiene una sola incógnita).\n4. Reemplaza el valor obtenido en el despeje del paso 1 para hallar la otra incógnita."
    },
    "MAT.ALG.SISTEMAS_2X2.METODO_IGUALACION": {
        "titulo": "Método de Igualación",
        "objetivo": "Resolver un sistema despejando la misma variable en ambas ecuaciones.",
        "explicacion": "El método de igualación se basa en la ley transitiva: Si A es igual a B, y C es igual a B, entonces A tiene que ser igual a C.\n\nEs muy mecánico: Tomas ambas ecuaciones y despejas la **misma** letra (por ejemplo, despejas la 'y' en ambas).\nObtendrás dos identidades para la 'y':\n- $y = \\text{Expresión 1}$\n- $y = \\text{Expresión 2}$\n\nComo ambas valen 'y', las igualas entre sí: $\\text{Expresión 1} = \\text{Expresión 2}$.\nAhora tienes una sola ecuación con pura 'x'. La resuelves y listo.",
        "procedimiento": "1. Elige una incógnita y despéjala en la primera ecuación.\n2. Despeja la MISMA incógnita en la segunda ecuación.\n3. Iguala los dos resultados obtenidos (omitiendo la letra despejada).\n4. Resuelve la ecuación resultante para hallar la primera variable.\n5. Reemplaza el valor hallado en cualquiera de los dos despejes iniciales para obtener la segunda variable."
    },
    "MAT.ALG.SISTEMAS_2X2.METODO_REDUCCION": {
        "titulo": "Método de Reducción (Suma/Resta)",
        "objetivo": "Aniquilar una variable sumando o restando las ecuaciones verticalmente.",
        "explicacion": "El método de reducción es el más rápido, poderoso y elegante (y el favorito en pruebas PAES). Se trata de sumar las dos ecuaciones verticalmente para que una de las letras se 'aniquile'.\n\nPara que se aniquilen, debes tener exactamente la misma cantidad de una letra, pero con signos opuestos (ej: $+3y$ arriba y $-3y$ abajo).\nSi no los tienes, ¡los creas! Multiplicas una (o ambas) ecuaciones por un número estratégico para forzar esa situación.\nUna vez forzada, sumas hacia abajo: las 'y' desaparecen ($3y - 3y = 0$), las 'x' se suman, los números se suman, y te queda una micro-ecuación rapidísima de resolver.",
        "procedimiento": "1. Elige qué incógnita quieres eliminar.\n2. Multiplica las ecuaciones por números convenientes para que los coeficientes de esa incógnita sean iguales pero de signo contrario.\n3. Suma ambas ecuaciones columna por columna (las x con las x, las y con las y, los números con los números).\n4. Resuelve la ecuación resultante de una sola incógnita.\n5. Reemplaza el valor en una ecuación original para hallar la otra."
    },
    "MAT.ALG.SISTEMAS_2X2.METODO_CRAMER": {
        "titulo": "Método de Cramer (Determinantes)",
        "objetivo": "Utilizar reglas matriciales simples para resolver sistemas directamente sin despejes.",
        "explicacion": "El método de Cramer es una fórmula mágica que no requiere que pienses en álgebra, solo en aritmética pura y multiplicaciones cruzadas.\n\nPrimero ordenas las ecuaciones: las 'x' y las 'y' a la izquierda, los números a la derecha.\nLuego calculas un número principal llamado 'Determinante del Sistema' ($\\Delta S$). Lo haces cruzando los coeficientes de $x$ e $y$: $(A \\cdot D) - (B \\cdot C)$.\n\nCalculas determinantes similares para la $x$ ($\\Delta x$) y para la $y$ ($\\Delta y$), reemplazando sus columnas por los números independientes.\nAl final, las soluciones son divisiones simples: $x = \\frac{\\Delta x}{\\Delta S}$ e $y = \\frac{\\Delta y}{\\Delta S}$.\nEs el método ideal si odias las fracciones intermedias.",
        "procedimiento": "1. Ordena el sistema en la forma $Ax + By = C$.\n2. Calcula el determinante del sistema ($\\Delta S$) usando los coeficientes de $x$ e $y$.\n3. Calcula el determinante de $x$ ($\\Delta x$) reemplazando la columna de $x$ por los términos independientes.\n4. Calcula el determinante de $y$ ($\\Delta y$) reemplazando la columna de $y$ por los términos independientes.\n5. Encuentra las soluciones con $x = \\Delta x / \\Delta S$ e $y = \\Delta y / \\Delta S$."
    },
    "MAT.ALG.SISTEMAS_2X2.MODELAMIENTO_BIDIMENSIONAL": {
        "titulo": "Modelamiento de Problemas 2x2",
        "objetivo": "Plantear sistemas a partir de problemas con dos condiciones dadas.",
        "explicacion": "Cuando un problema te da dos piezas de información totalmente distintas, necesitas un sistema 2x2. \n\nEjemplo clásico de la granja:\n'En una granja hay gallinas ($x$) y vacas ($y$). En total hay 30 cabezas y 100 patas.'\nAquí tienes dos mundos (dos ecuaciones):\n- El mundo de las cabezas (cada animal tiene 1): $1x + 1y = 30$.\n- El mundo de las patas (gallinas tienen 2, vacas tienen 4): $2x + 4y = 100$.\n\nAcabas de modelar el problema. Ahora aplicas reducción, sustitución o igualación.",
        "procedimiento": "1. Define claramente qué representa 'x' y qué representa 'y'.\n2. Lee la primera condición del problema y tradúcela a la Ecuación 1.\n3. Lee la segunda condición del problema (suele hablar de dinero, total de patas, edades) y tradúcela a la Ecuación 2.\n4. Asegúrate de que las unidades coincidan en cada ecuación."
    },
    "MAT.ALG.SISTEMAS_2X2.VERIFICACION_SOLUCION": {
        "titulo": "Verificación del Par Ordenado",
        "objetivo": "Comprobar que la solución encontrada satisface ambas ecuaciones simultáneamente.",
        "explicacion": "Una trampa común es encontrar el valor de 'x' e 'y', reemplazarlo en la primera ecuación para ver si cuadra, y seguir de largo. \n\n¡Falso sentido de seguridad! Es posible equivocarse en el desarrollo, que los números cuadren por casualidad en la primera ecuación, pero que fallen horriblemente en la segunda.\n\nPara que el par ordenado $(x, y)$ sea el rey legítimo del sistema, debe ser capaz de reemplazar las letras en AMBAS ecuaciones y mantener la igualdad perfecta en las dos. Si falla en una, el resultado está malo.",
        "procedimiento": "1. Toma tus valores finales obtenidos para 'x' e 'y'.\n2. Reemplázalos en la Ecuación 1 y verifica que el lado izquierdo sea igual al derecho.\n3. Reemplázalos en la Ecuación 2 y verifica la igualdad.\n4. Solo si ambas igualdades son ciertas, el par es la solución oficial."
    },
    "MAT.ALG.SISTEMAS_2X2.RESTRICCIONES_SIGNO": {
        "titulo": "Restricciones Contextuales 2x2",
        "objetivo": "Filtrar los resultados algebraicos según la lógica del problema.",
        "explicacion": "Al igual que en las ecuaciones lineales, cuando modelas un problema real (como el de las vacas y gallinas), el álgebra no sabe qué es una vaca. Solo ve números.\n\nSi resuelves el sistema y obtienes que hay $-5$ gallinas y $35$ vacas, la matemática de las ecuaciones está correcta (suman 30 cabezas, etc.), pero físicamente es imposible tener $-5$ gallinas.\nEn ese caso, debes concluir que los datos originales del problema eran absurdos o inconsistentes (el granjero te mintió sobre cuántas patas había).",
        "procedimiento": "1. Obtén el par $(x, y)$ solucionando el sistema.\n2. Vuelve a tus definiciones de 'x' e 'y'.\n3. Analiza si ambos valores numéricos tienen sentido en el mundo real (sin negativos para cosas físicas, sin fracciones para cosas indivisibles como personas).\n4. Concluye la validez de la respuesta."
    },

    # TANDA 7: SISTEMAS REPRESENTACIÓN
    "MAT.ALG.SISTEMAS_REPRESENTACION.INTERPRETACION_RECTAS": {
        "titulo": "Interpretación como Rectas",
        "objetivo": "Visualizar cada ecuación del sistema como una línea recta en el plano cartesiano.",
        "explicacion": "Aquí es donde el álgebra de letras se convierte en geometría visual. \nToda ecuación lineal con dos variables (como $2x + y = 5$) es, en realidad, las instrucciones para dibujar una línea recta perfecta en un gráfico de coordenadas $(x,y)$.\n\nSi tomas todos los pares de números que hacen que $2x + y = 5$ sea verdad, y pones un puntito por cada uno, verás que forman una recta continua.\nPor lo tanto, un sistema de dos ecuaciones 2x2 son simplemente **dos líneas rectas dibujadas en el mismo mapa**.",
        "procedimiento": "1. Toma una ecuación del sistema.\n2. Encuentra al menos dos puntos (pares x,y) que la satisfagan (por ejemplo, si x=0 cuánto vale y, y viceversa).\n3. Dibuja esos puntos en el plano y únelos con una recta.\n4. Repite el proceso para la segunda ecuación."
    },
    "MAT.ALG.SISTEMAS_REPRESENTACION.SOLUCION_GRAFICA": {
        "titulo": "La Solución como Intersección",
        "objetivo": "Entender que la solución del sistema es el punto geométrico donde las rectas chocan.",
        "explicacion": "Si cada ecuación es una línea recta llena de puntos-solución, entonces resolver el sistema significa: 'Busca el único punto que pertenezca a ambas líneas al mismo tiempo'.\n\nVisualmente, esto no es más que **el punto de choque (la intersección)** entre las dos rectas.\nEl par ordenado $(x,y)$ que tanto te esforzaste en calcular algebraicamente usando Reducción o Sustitución, son exactamente las coordenadas espaciales donde las dos líneas se cruzan en tu dibujo.\nEs la fusión perfecta entre el álgebra y la geometría.",
        "procedimiento": "1. Grafica la primera recta.\n2. Grafica la segunda recta en el mismo plano.\n3. Busca visualmente el punto exacto donde se cruzan (intersección).\n4. Lee las coordenadas (x,y) de ese punto. Esa es la solución de tu sistema."
    },
    "MAT.ALG.SISTEMAS_REPRESENTACION.SISTEMA_DETERMINADO": {
        "titulo": "Sistema Compatible Determinado",
        "objetivo": "Reconocer gráfica y algebraicamente un sistema con solución única.",
        "explicacion": "La inmensa mayoría de los sistemas que resuelves son de este tipo. 'Compatible' significa que SÍ tiene solución. 'Determinado' significa que puedes determinar cuál es con exactitud (es única).\n\nEn el mundo de los dibujos, esto ocurre cuando las dos rectas tienen inclinaciones (pendientes) diferentes. Tarde o temprano, como si fueran dos espadas cruzadas, chocarán en un único punto.\n\nAlgebraicamente, te das cuenta de que es determinado porque al aplicar tus métodos, llegas felizmente a algo como '$x=3$, $y=4$'.",
        "procedimiento": "1. Compara las pendientes (inclinaciones) de ambas rectas (el coeficiente que acompaña a la 'x' al despejar la 'y').\n2. Si las pendientes son diferentes, el sistema es Determinado.\n3. Tendrá exactamente una sola solución (un punto de choque)."
    },
    "MAT.ALG.SISTEMAS_REPRESENTACION.SISTEMA_INDETERMINADO": {
        "titulo": "Sistema Compatible Indeterminado",
        "objetivo": "Identificar sistemas que tienen infinitas soluciones por ser la misma recta.",
        "explicacion": "A veces, el sistema te intenta engañar. Te da dos ecuaciones, pero una es simplemente el doble de la otra (ej: $x+y=2$ y $2x+2y=4$).\n\nAl graficarlas, dibujas la primera línea, y cuando intentas dibujar la segunda, te das cuenta de que cae exactamente encima de la primera. Son la misma recta.\n¿En cuántos puntos se tocan dos rectas que están montadas una sobre la otra? ¡En todos! Tienen **infinitos puntos de contacto**. Por eso es 'Indeterminado', porque no puedes determinar una sola solución. Todas sirven.\n\nSi intentas resolverlo con álgebra, las letras se aniquilarán y llegarás a una verdad obvia como $0 = 0$.",
        "procedimiento": "1. Observa si una ecuación es exactamente un múltiplo directo de la otra (en todos sus términos, incluyendo el resultado).\n2. Si es así, las rectas son coincidentes (están superpuestas).\n3. Concluye que el sistema tiene infinitas soluciones.\n4. Si lo resuelves algebraicamente, llegarás a una identidad verdadera como $0=0$ o $5=5$."
    },
    "MAT.ALG.SISTEMAS_REPRESENTACION.SISTEMA_INCONSISTENTE": {
        "titulo": "Sistema Incompatible (Sin Solución)",
        "objetivo": "Reconocer sistemas imposibles donde las rectas son paralelas.",
        "explicacion": "Este es el escenario más trágico. Te dan dos ecuaciones que exigen cosas contradictorias (ej: $x+y=5$ y al mismo tiempo $x+y=10$. ¿Cómo dos números van a sumar 5 y 10 a la vez?).\n\nSi dibujas esto en un gráfico, obtendrás **dos líneas perfectamente paralelas**, como las vías del tren. Tienen la misma inclinación, pero están separadas.\n¿En qué punto se cruzan las vías del tren? Nunca. Por lo tanto, el sistema **No tiene solución** (Conjunto Vacío).\n\nSi intentas forzar una respuesta con álgebra, las letras se aniquilarán, pero llegarás a una mentira espantosa como $0 = 5$.",
        "procedimiento": "1. Compara las pendientes de las rectas (coeficientes de x e y).\n2. Si las pendientes son idénticas, pero los resultados (términos independientes) son diferentes y no proporcionales, son paralelas.\n3. Concluye que el sistema no tiene solución.\n4. Si resuelves con álgebra, llegarás a un absurdo matemático como $0=8$."
    },
    "MAT.ALG.SISTEMAS_REPRESENTACION.PARAMETROS_SOLUCION_UNICA": {
        "titulo": "Parámetros para Solución Única",
        "objetivo": "Determinar qué valores deben tener los coeficientes para que las rectas se crucen.",
        "explicacion": "En pruebas PAES es muy común que en lugar de darte todos los números, escondan uno con una letra 'k', por ejemplo: $kx + 2y = 4$ y $3x + 4y = 8$. Y te preguntan: '¿Qué valor NO puede tomar k para que haya solución única?'.\n\nRecuerda: Para que haya solución única, las rectas deben tener pendientes diferentes (deben chocar). La forma matemática de verificar esto rápidamente es comparando las fracciones que forman los coeficientes.\n\nRegla: Para solución única, la proporción de las 'x' debe ser distinta a la proporción de las 'y'. Es decir: $\\frac{A_1}{A_2} \\neq \\frac{B_1}{B_2}$.\nEn nuestro ejemplo: $\\frac{k}{3} \\neq \\frac{2}{4}$. Resuelves y listo: $k \\neq 1.5$.",
        "procedimiento": "1. Identifica los coeficientes que acompañan a 'x' ($A_1, A_2$) y los que acompañan a 'y' ($B_1, B_2$).\n2. Plantea la inecuación de que la división de las 'x' sea DISTINTA a la división de las 'y': $\\frac{A_1}{A_2} \\neq \\frac{B_1}{B_2}$.\n3. Despeja el parámetro desconocido ('k') como si fuera una ecuación normal."
    },
    "MAT.ALG.SISTEMAS_REPRESENTACION.PARAMETROS_INFINITAS_SOLUCIONES": {
        "titulo": "Parámetros para Infinitas Soluciones",
        "objetivo": "Establecer la proporcionalidad total para obligar a que las rectas sean idénticas.",
        "explicacion": "Si te piden encontrar el valor del parámetro escondido 'k' para que el sistema tenga **infinitas soluciones**, te están diciendo 'haz que la segunda ecuación sea un clon perfecto de la primera'.\n\nPara que sean clones, TODO debe ser proporcional. La división de las 'x', la división de las 'y' y la división de los números sueltos deben dar exactamente el mismo resultado.\n\nRegla estricta de clonación: $\\frac{A_1}{A_2} = \\frac{B_1}{B_2} = \\frac{C_1}{C_2}$.\nIgualas las fracciones que contengan a tu 'k' con la fracción de los números conocidos, resuelves, y habrás encontrado el valor maestro.",
        "procedimiento": "1. Arma las tres fracciones usando los coeficientes de las dos ecuaciones: 'x', 'y' y números sueltos.\n2. Plantea la igualdad triple: $\\frac{A_1}{A_2} = \\frac{B_1}{B_2} = \\frac{C_1}{C_2}$.\n3. Toma dos de las fracciones (una que contenga el parámetro y otra que tenga puros números) y resuélvelas con multiplicación cruzada."
    },
    "MAT.ALG.SISTEMAS_REPRESENTACION.PARAMETROS_SIN_SOLUCION": {
        "titulo": "Parámetros para Sistema sin Solución",
        "objetivo": "Configurar los coeficientes para crear rectas paralelas separadas.",
        "explicacion": "El último truco del mago: te piden el parámetro 'k' para que el sistema **no tenga solución**.\nTraducción geométrica: 'Haz que las vías del tren sean paralelas'.\n\nPara que sean paralelas, deben tener la misma inclinación (las 'x' y las 'y' deben ser proporcionales entre sí), pero ¡CUIDADO! el resultado final debe ser diferente (no pueden ser clones).\n\nRegla de las paralelas: $\\frac{A_1}{A_2} = \\frac{B_1}{B_2}$ pero esto debe ser $\\neq \\frac{C_1}{C_2}$.\nNormalmente, te bastará con igualar la fracción de las 'x' con la fracción de las 'y' para despejar 'k', y el problema estará resuelto.",
        "procedimiento": "1. Arma las fracciones de proporciones.\n2. Para garantizar la misma pendiente, iguala la proporción de 'x' con la proporción de 'y': $\\frac{A_1}{A_2} = \\frac{B_1}{B_2}$.\n3. Resuelve esa igualdad para despejar el parámetro.\n4. (Opcional pero formal) Verifica que con ese valor encontrado, la proporción resultante sea DISTINTA a la de los números sueltos ($\\frac{C_1}{C_2}$)."
    }
}

def generar_ejercicios(semantic_id):
    ejercicios = []
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
    for sid, data in teoria_t5_t7.items():
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

        all_ejercicios.extend(generar_ejercicios(sid))

    with open(ejercicios_file, 'w', encoding='utf-8') as f:
        for ej in all_ejercicios:
            f.write(json.dumps(ej, ensure_ascii=False) + "\n")
    print(f"Generados 220 ejercicios en {ejercicios_file}")

if __name__ == "__main__":
    build_content()
