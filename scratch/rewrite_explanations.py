import glob
import re
import sys

explanations = {
    # ------------------- CUADRADO DE BINOMIO -------------------
    "mat-alg-cuadrado-binomio-suma-definicion.yaml": """Elevar un binomio al cuadrado, $(a+b)^2$, significa multiplicar el binomio por sí mismo: $(a+b)(a+b)$.

Si desarrollamos esto multiplicando término a término mediante la propiedad distributiva, tenemos:
$(a+b)(a+b) = a \\cdot a + a \\cdot b + b \\cdot a + b \\cdot b = a^2 + ab + ba + b^2$

Como $ab$ y $ba$ son el mismo término (porque la multiplicación es conmutativa), podemos sumarlos. Esto nos da como resultado el famoso **Trinomio Cuadrado Perfecto**:

**Fórmula:** $(a+b)^2 = a^2 + 2ab + b^2$

**Significado:** Esto nos demuestra que el cuadrado de una suma NUNCA es simplemente la suma de los cuadrados ($a^2 + b^2$). Siempre se genera un \"término cruzado\" que representa las interacciones cruzadas entre $a$ y $b$.""",
    
    "mat-alg-cuadrado-binomio-regla-suma.yaml": """La regla del cuadrado de un binomio suma es un atajo (o *producto notable*) para no tener que multiplicar término a término cada vez que vemos una expresión de la forma $(a+b)^2$.

**Fórmula de la regla:** $(a+b)^2 = a^2 + 2ab + b^2$

**Regla en palabras (para memorizar):**
1. **El cuadrado del primer término:** $(a)^2$
2. **Más el doble del producto del primero por el segundo:** $2(a)(b)$
3. **Más el cuadrado del segundo término:** $(b)^2$

**¿Cómo aplicarla?**
Si tienes $(3x + 5)^2$:
- El primer término es $3x$. Su cuadrado es $(3x)^2 = 9x^2$.
- El doble del producto es $2(3x)(5) = 30x$.
- El cuadrado del segundo término es $(5)^2 = 25$.
- Juntando todo: $9x^2 + 30x + 25$. ¡Rápido y sin multiplicar polinomios largos!""",

    "mat-alg-cuadrado-binomio-representacion-area.yaml": """Podemos demostrar geométricamente que $(a+b)^2 = a^2 + 2ab + b^2$ pensando en el área de un cuadrado.

Imagina un cuadrado grande cuyo lado mide $(a+b)$.
El área total de ese cuadrado es, por definición, base por altura: $(a+b) \\cdot (a+b) = (a+b)^2$.

Ahora, si dividimos cada lado de ese cuadrado en un segmento de longitud $a$ y otro de longitud $b$, podemos trazar líneas interiores que dividen el cuadrado grande en cuatro figuras más pequeñas:
1. Un cuadrado de lado $a$, cuya área es **$a^2$**.
2. Un cuadrado de lado $b$, cuya área es **$b^2$**.
3. Dos rectángulos iguales, cuyos lados son $a$ y $b$. El área de cada rectángulo es $ab$. Al ser dos, suman un área de **$2ab$**.

Al sumar el área de las cuatro figuras interiores obtenemos el área total del cuadrado grande:
**Área Total = $a^2 + ab + ab + b^2 = a^2 + 2ab + b^2$**.
¡Esta representación visual es la mejor forma de recordar por qué existe el término central $2ab$!""",

    "mat-alg-cuadrado-binomio-diferencia-definicion.yaml": """El cuadrado de un binomio con una resta (diferencia) se expresa como $(a-b)^2$. Igual que en la suma, esto significa multiplicar el binomio por sí mismo: $(a-b)(a-b)$.

Aplicando la propiedad distributiva término a término, pero teniendo mucho cuidado con los signos:
$(a-b)(a-b) = a(a) + a(-b) + (-b)(a) + (-b)(-b)$
$= a^2 - ab - ba + b^2$

Como la multiplicación es conmutativa, $-ab$ y $-ba$ son términos semejantes. Al juntarlos, obtenemos un solo término negativo: $-2ab$. El último término, $(-b)(-b)$, se vuelve positivo ($+b^2$) porque negativo por negativo es positivo.

**Fórmula:** $(a-b)^2 = a^2 - 2ab + b^2$

**Conclusión:** La única diferencia respecto al cuadrado de una suma es el signo negativo del término central o \"doble producto\". Los extremos ($a^2$ y $b^2$) siempre serán positivos.""",

    "mat-alg-cuadrado-binomio-regla-diferencia.yaml": """La regla para resolver el cuadrado de una diferencia, $(a-b)^2$, es idéntica a la regla de la suma, salvo por el signo del término central.

**Fórmula:** $(a-b)^2 = a^2 - 2ab + b^2$

**Regla en palabras (para memorizar):**
1. **El cuadrado del primer término:** $(a)^2$.
2. **MENOS el doble producto del primero por el segundo:** $- 2(a)(b)$.
3. **MÁS el cuadrado del segundo término:** $+ (b)^2$.

**¿Cómo aplicarla de manera segura?**
Cuando utilices esta regla, puedes pensar que el segundo término es \"$b$\" (positivo) y aplicas el signo menos directamente en la fórmula. 
Ejemplo para $(4x - 7)^2$:
- Cuadrado del primero: $(4x)^2 = 16x^2$.
- Menos el doble producto: $-2(4x)(7) = -56x$.
- Más el cuadrado del segundo: $(7)^2 = +49$.
Resultado final: $16x^2 - 56x + 49$.""",

    "mat-alg-cuadrado-binomio-simetria-diferencia.yaml": """Existe una propiedad de simetría muy interesante en el cuadrado de un binomio diferencia: **elevar $(a-b)$ al cuadrado produce exactamente el mismo resultado que elevar $(b-a)$ al cuadrado**. 

Matemáticamente, esto se escribe: $(a-b)^2 = (b-a)^2$.

**¿Por qué sucede esto?**
Recordemos que sacar el negativo de una resta invierte sus términos: $(b-a) = -(a-b)$.
Si tomamos esa expresión y la elevamos al cuadrado, obtenemos:
$(-(a-b))^2 = (-1)^2 \\cdot (a-b)^2 = 1 \\cdot (a-b)^2 = (a-b)^2$.

**Desarrollo comprobatorio:**
Desarrollemos ambos para comparar:
$(a-b)^2 = a^2 - 2ab + b^2$
$(b-a)^2 = b^2 - 2ba + a^2$
Si ordenamos los términos, vemos que son algebraicamente idénticos: $a^2 - 2ab + b^2$. Esta propiedad simétrica es muy útil para reordenar restas dentro de paréntesis cuadrados sin afectar el resultado (por ejemplo, para evitar coeficientes principales negativos).""",

    "mat-alg-cuadrado-binomio-omision-doble-producto.yaml": """El error algebraico más famoso en matemáticas es, sin duda, la omisión del doble producto al elevar un binomio al cuadrado. También se le llama "El sueño del estudiante novato".

El error consiste en creer falsamente que el exponente se puede distribuir sobre la suma o la resta, escribiendo:
$(a+b)^2 \\neq a^2 + b^2$
$(a-b)^2 \\neq a^2 - b^2$

**¿Por qué este es un error grave?**
Un exponente nos indica cuántas veces se multiplica *la base entera* por sí misma. En $(a+b)^2$, la base es el bloque $(a+b)$. Al distribuirla correctamente como $(a+b)(a+b)$ sabemos que aparecen los términos cruzados $ab + ba$ que originan el $+2ab$. 

Si omitimos el doble producto, estamos ignorando los dos rectángulos interiores que aparecen al representar esto geométricamente. Para evitar este error, siempre recuerda la regla del producto notable, o, en caso de duda, escribe los dos paréntesis y multiplica término a término.""",

    # ------------------- SUMA POR DIFERENCIA -------------------
    "mat-alg-suma-diferencia-definicion-conjugados.yaml": """La \"suma por su diferencia\" ocurre cuando multiplicamos dos binomios que son exactamente iguales en sus términos, pero uno es una suma y el otro es una resta. 

Matemáticamente se escribe como: $(a+b)(a-b)$. En álgebra, a la expresión $(a-b)$ se le llama el **conjugado** de $(a+b)$, y viceversa.

**¿De dónde sale su nombre y regla?**
Si multiplicamos ambos binomios aplicando la propiedad distributiva:
$(a+b)(a-b) = a(a) + a(-b) + b(a) + b(-b)$
$= a^2 - ab + ab - b^2$

Nota lo que sucede en el medio: los términos cruzados $-ab$ y $+ab$ son idénticos pero con signos opuestos, por lo que **se cancelan mutuamente** (dan cero). Lo único que sobrevive de toda la expansión son los cuadrados de los extremos.

**Fórmula:** $(a+b)(a-b) = a^2 - b^2$""",

    "mat-alg-suma-diferencia-identificacion-conjugados.yaml": """Para aplicar correctamente el atajo de la suma por diferencia, es vital aprender a **identificar visualmente binomios conjugados**.

Dos binomios son conjugados si cumplen tres condiciones estrictas:
1. **Tienen exactamente los mismos dos términos.** Si uno tiene $3x$ y $5y$, el otro también debe tener $3x$ y $5y$.
2. **Uno de los binomios los suma, y el otro los resta.** El orden de los factores no importa. Ejemplos válidos: $(a+b)(a-b)$ o $(a-b)(a+b)$.
3. **El orden interno de los términos restados no importa si reacomodamos los sumados.** Es decir, $(x+y)(x-y)$ es un conjugado directo. Sin embargo, $(x+y)(y-x)$ requiere que primero reordenemos la suma a $(y+x)(y-x)$ para reconocer que el primer término es $y$ y el segundo es $x$.

**Tip práctico:** El término que mantiene el mismo signo en ambos paréntesis será el minuendo (el positivo en el resultado final), y el término que cambia de signo será el sustraendo (el que lleva el signo negativo).""",

    "mat-alg-suma-diferencia-regla-diferencia-cuadrados.yaml": """La regla de suma por diferencia es posiblemente el producto notable más rápido y útil del álgebra. Nos permite saltarnos por completo el proceso de multiplicar término a término cuando detectamos binomios conjugados.

**Fórmula de la regla:** $(a+b)(a-b) = a^2 - b^2$
Al resultado de esta operación se le conoce formalmente como **Diferencia de Cuadrados**.

**Regla en palabras:**
El producto de una suma por su diferencia es igual al cuadrado del primer término (el que no cambia de signo) menos el cuadrado del segundo término (el que sí cambia de signo en los paréntesis).

**Ejemplo de aplicación rápida:**
Resuelve $(5x + 2y)(5x - 2y)$.
- Primer término: $5x$. Su cuadrado es $(5x)^2 = 25x^2$.
- Segundo término: $2y$. Su cuadrado es $(2y)^2 = 4y^2$.
- Resultado final: ¡Solo los restas! $\\rightarrow 25x^2 - 4y^2$. No hay término central porque se cancela automáticamente.""",

    "mat-alg-suma-diferencia-representacion-area.yaml": """Podemos visualizar algebraicamente por qué $(a+b)(a-b) = a^2 - b^2$ utilizando el concepto de áreas geométricas. 

1. Empecemos imaginando un cuadrado grande de lado $a$. Su área original es $a^2$.
2. De una esquina de este cuadrado, recortemos (quitemos) un cuadrado más pequeño de lado $b$. El área restante es ahora exactamente **$a^2 - b^2$**.
3. Nuestra figura sobrante tiene forma de \"L\". Si tomamos el rectángulo vertical que forma una de las patas de la \"L\" y lo reacomodamos junto a la pata horizontal, se forma un único rectángulo continuo.
4. Las dimensiones de este nuevo rectángulo serán exactamente $(a+b)$ de base y $(a-b)$ de altura. Por lo tanto, el área de este rectángulo se calcula multiplicando su base por su altura: $(a+b)(a-b)$.

Dado que el área de la \"L\" es la misma que la del nuevo rectángulo, concluimos geométricamente que:
**$(a+b)(a-b) = a^2 - b^2$**.""",

    "mat-alg-suma-diferencia-error-signo.yaml": """Al usar la regla de suma por diferencia, es común cometer errores relacionados con los signos si no se identifica correctamente qué término juega el rol de "primer término" y cuál de "segundo término".

**El error principal:**
Si tienes la multiplicación $(-x + y)(-x - y)$, un error común es decir que el resultado es $x^2 + y^2$ o $-x^2 - y^2$.

**Cómo hacerlo correctamente:**
Debes fijarte en qué término cambia de signo entre los dos paréntesis y cuál se mantiene constante.
- El término constante es el minuendo (va primero y positivo al elevar al cuadrado).
- El término que cambia de signo es el sustraendo (va después del signo menos).

En $(-x + y)(-x - y)$:
- El término que no cambia es $-x$. Su cuadrado es $(-x)^2 = x^2$.
- El término que sí cambia de signo es $y$ (en un paréntesis es $+y$, en el otro es $-y$). Su cuadrado es $y^2$.
- Restamos: $x^2 - y^2$.

No te dejes engañar por el orden visual; confía siempre en quién cambia de signo y quién no.""",

    # ------------------- TERMINO COMUN -------------------
    "mat-alg-termino-comun-definicion.yaml": """El producto de dos binomios con un término en común ocurre cuando multiplicamos dos expresiones que comparten exactamente un sumando idéntico, pero el otro sumando es diferente. 

Su estructura general se representa como: **$(x+a)(x+b)$**
Aquí, '$x$' representa el término que se repite en ambos paréntesis (el término común), mientras que '$a$' y '$b$' son términos distintos (los términos no comunes).

**¿De dónde sale la regla?**
Si multiplicamos $(x+a)(x+b)$ usando distributividad completa, tenemos:
$x(x) + x(b) + a(x) + a(b)$
$= x^2 + bx + ax + ab$

Si agrupamos los dos términos centrales (que contienen la variable $x$) factorizando esa $x$, obtenemos:
$= x^2 + (a+b)x + ab$

Esta estructura es el origen del **Trinomio de la forma $x^2 + px + q$**, que es fundamental para factorizar más adelante.""",

    "mat-alg-termino-comun-identificacion-estructura.yaml": """Para usar la regla del término común, el primer paso es aprender a identificar su estructura y diferenciarla de otros productos notables.

La expresión clave es **$(x+a)(x+b)$**.
Para confirmar que estás frente a un producto con término común, hazte estas dos preguntas:
1. **¿Hay exactamente un término que es idéntico en ambos binomios (mismo signo y exponente)?** Ese será tu término común.
2. **¿Los otros dos términos son diferentes entre sí?** Estos serán tus términos no comunes. (Si fueran iguales, sería un Cuadrado de Binomio; si fueran iguales pero con distinto signo, sería una Suma por Diferencia).

**Ejemplo de análisis:**
En $(2y^2 - 7)(2y^2 + 4)$:
- El término común es $2y^2$, ya que aparece exactamente igual en ambos lados.
- Los términos no comunes son $-7$ y $+4$. (Atención: ¡el signo siempre acompaña al término no común!).
Sabiendo esto, puedes aplicar el atajo de inmediato.""",

    "mat-alg-termino-comun-regla-general.yaml": """La regla del término común es un atajo directo que convierte la multiplicación $(x+a)(x+b)$ en un trinomio ordenado en un solo paso mental.

**Fórmula de la regla:** $(x+a)(x+b) = x^2 + (a+b)x + ab$

**Regla en palabras (los tres pasos):**
El desarrollo consta siempre de tres partes:
1. **El cuadrado del término común:** Toma el término que se repite y elévalo al cuadrado.
2. **La suma por el común:** Suma (algebraicamente, respetando signos) los dos términos no comunes. El resultado de esa suma se multiplica por el término común.
3. **El producto:** Multiplica los dos términos no comunes entre sí (respetando la regla de los signos).

**Ejemplo rápido:** $(x + 5)(x - 2)$
- Cuadrado del común: $x^2$.
- Suma por el común: $(+5 - 2) = +3$. Se multiplica por $x \\rightarrow +3x$.
- Producto: $(+5)(-2) = -10$.
Resultado: $x^2 + 3x - 10$.""",

    "mat-alg-termino-comun-manejo-signos-no-comunes.yaml": """Al aplicar la regla del término común $(x+a)(x+b) = x^2 + (a+b)x + ab$, el principal desafío es manejar correctamente los signos de los términos no comunes ($a$ y $b$). 

**Reglas de oro para los signos:**
Recuerda que debes incluir el signo junto al número o variable en tus cálculos mentales. 

1. **Para el coeficiente central (La Suma):** Usa las reglas de suma y resta.
   - Si ambos son del mismo signo, se suman sus valores absolutos y se conserva el signo. Ej: $(-4 - 3) = -7$.
   - Si tienen signos distintos, se restan y se conserva el signo del mayor en valor absoluto. Ej: $(+8 - 5) = +3$.
   
2. **Para el término independiente (El Producto):** Usa las reglas de multiplicación.
   - Mismo signo $\\rightarrow$ resultado positivo $(+ \\cdot + = +) \\text{ o } (- \\cdot - = +)$.
   - Distinto signo $\\rightarrow$ resultado negativo $(+ \\cdot - = -)$.

Ejemplo en $(x - 6)(x - 4)$:
- Central: $(-6) + (-4) = -10$.
- Final: $(-6) \\cdot (-4) = +24$.
- Trinomio: $x^2 - 10x + 24$.""",

    "mat-alg-termino-comun-caso-general-lineal.yaml": """El caso general de binomios lineales con término común se da cuando el término que se repite no es simplemente una letra suelta (como '$x$'), sino un término que incluye un coeficiente numérico (como '$3x$' o '$5y$').

Por ejemplo, $(ax+b)(ax+c)$. La lógica sigue siendo exactamente la misma que la fórmula básica, pero debes tener cuidado con las multiplicaciones.

**Pasos en el caso general:**
Tomemos $(3x + 2)(3x - 7)$:
1. **Cuadrado del común:** El término común es $3x$. Su cuadrado es $(3x)^2 = 9x^2$. (¡No olvides elevar también el coeficiente numérico!).
2. **Suma por el común:** Los no comunes son $+2$ y $-7$. La suma algebraica es $(2 - 7) = -5$. Ahora multiplicamos eso por el término común: $-5(3x) = -15x$.
3. **Producto:** Multiplicamos los no comunes: $(+2)(-7) = -14$.

Resultado final: $9x^2 - 15x - 14$. 
Este caso nos recuerda que el "término común" actúa como un bloque inseparable durante los primeros dos pasos de la regla.""",

    # ------------------- CUBO DE BINOMIO -------------------
    "mat-alg-cubo-binomio-suma-definicion.yaml": """El cubo de un binomio suma se representa como $(a+b)^3$. El exponente 3 indica que la base $(a+b)$ se multiplica por sí misma tres veces: $(a+b)(a+b)(a+b)$.

**¿Cómo llegamos a la fórmula final?**
Para desarrollarlo, primero calculamos el cuadrado del binomio (los dos primeros factores):
$(a+b)^2 = a^2 + 2ab + b^2$

Luego, multiplicamos ese trinomio por el binomio restante $(a+b)$:
$(a^2 + 2ab + b^2)(a + b) = a^3 + a^2b + 2a^2b + 2ab^2 + ab^2 + b^3$

Al agrupar los términos semejantes (sumando los coeficientes de $a^2b$ por un lado, y los de $ab^2$ por otro), obtenemos el resultado clásico del cubo de un binomio.

**Fórmula del cubo de suma:**
$(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3$

El polinomio resultante siempre tiene **cuatro términos**. Como los términos originales estaban sumando, el resultado solo tiene signos positivos.""",

    "mat-alg-cubo-binomio-regla-suma.yaml": """Desarrollar el cubo de un binomio sumado multiplicando término a término es largo y propenso a errores. Por ello, memorizar la regla de $(a+b)^3$ es fundamental.

**Fórmula de la regla:** $(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3$

**La regla en palabras (El poema algebraico):**
El cubo de la suma de dos términos es igual a:
1. El cubo del primer término ($a^3$).
2. Más el triple del producto del cuadrado del primero por el segundo ($3a^2b$).
3. Más el triple del producto del primero por el cuadrado del segundo ($3ab^2$).
4. Más el cubo del segundo término ($b^3$).

**Mnemotecnia visual (Los exponentes bailan):**
Fíjate en los grados de cada término individual. Si seguimos los cuatro términos de izquierda a derecha:
- El exponente de $a$ va bajando: 3, 2, 1, 0.
- El exponente de $b$ va subiendo: 0, 1, 2, 3.
- Los coeficientes en el centro siempre son 3. ¡Todo suma grado absoluto 3!""",

    "mat-alg-cubo-binomio-diferencia-definicion.yaml": """El cubo de un binomio con resta, o diferencia, se representa como $(a-b)^3$. Su significado base es multiplicar $(a-b)$ tres veces por sí mismo.

**Desarrollo algebraico:**
Partimos de $(a-b)^2 = a^2 - 2ab + b^2$. Ahora multiplicamos eso por el tercer factor $(a-b)$:
$(a^2 - 2ab + b^2)(a - b) = a^3 - a^2b - 2a^2b + 2ab^2 + ab^2 - b^3$

Al agrupar y sumar los términos semejantes, la estructura matemática que emerge es casi idéntica a la del cubo de una suma, pero con una alteración crucial en los signos, ya que algunos factores negativos se elevaron al cuadrado (volviéndose positivos) y otros al cubo (manteniéndose negativos).

**Fórmula del cubo de diferencia:**
$(a-b)^3 = a^3 - 3a^2b + 3ab^2 - b^3$

Notarás que el polinomio resultante también tiene cuatro términos, pero en vez de ser todos positivos, sus signos **se alternan** empezando siempre por positivo.""",

    "mat-alg-cubo-binomio-regla-diferencia.yaml": """La regla para desarrollar el cubo de una resta, $(a-b)^3$, conserva la misma estructura matemática y las mismas magnitudes que el cubo de una suma. La única modificación necesaria es el patrón de los signos.

**Fórmula:** $(a-b)^3 = a^3 - 3a^2b + 3ab^2 - b^3$

**Regla en palabras:**
1. El cubo del primero ($a^3$).
2. **MENOS** el triple del cuadrado del primero por el segundo ($-3a^2b$).
3. **MÁS** el triple del primero por el cuadrado del segundo ($+3ab^2$).
4. **MENOS** el cubo del segundo ($-b^3$).

**La regla mágica de los signos alternados:**
Siempre que tengas una resta elevada al cubo, los signos de los cuatro términos del resultado final SIEMPRE seguirán el patrón de alternancia: `+, -, +, -`.
El primer y el tercer término son positivos. El segundo y el cuarto término son negativos. No necesitas multiplicar signos manualmente, solo aplica la estructura.""",

    "mat-alg-cubo-binomio-manejo-signos.yaml": """En el cubo de un binomio de resta $(a-b)^3 = a^3 - 3a^2b + 3ab^2 - b^3$, los signos alternados no aparecen por arte de magia; tienen un origen algebraico profundo en la regla de potencias.

Si pensamos en $(a-b)$ como una suma oculta $(a + (-b))$, podemos usar la regla de la suma aplicando las potencias al número negativo $(-b)$:
1. Término 1: $a^3$ (no involucra a $b$, queda igual).
2. Término 2: $3(a^2)(-b)^1$. Como el exponente 1 es impar, el signo negativo se escapa, dando **$-3a^2b$**.
3. Término 3: $3(a)(-b)^2$. El exponente 2 es par. Todo número negativo elevado a una potencia par se vuelve positivo, por lo que $(-b)^2$ se convierte en $+b^2$. Por esto queda **$+3ab^2$**.
4. Término 4: $(-b)^3$. El exponente 3 es impar, el signo negativo prevalece. Por lo que queda **$-b^3$**.

Comprender que los exponentes pares e impares controlan el destino del signo negativo es la clave para dominar este producto notable y no memorizar a ciegas.""",

    "mat-alg-cubo-binomio-error-terminos-mixtos.yaml": """Un error muy habitual, incluso en estudiantes que ya dominan el cuadrado de un binomio, es olvidar los cuadrados internos en los términos centrales del cubo de un binomio.

**El error:**
Sabiendo que un cubo tiene coeficiente 3 en el centro, el estudiante escribe apresuradamente:
$(a+b)^3 = a^3 + 3ab + 3ab + b^3$ (¡incorrecto!)

**Por qué es un error grave:**
La matemática requiere equilibrio dimensional. En álgebra, la suma de los exponentes de las variables en cada término de un producto notable homogéneo debe ser igual al grado de la expresión completa (grado absoluto 3).
- En el término $a^3$, el grado es 3.
- En el término incorrecto $3ab$, el grado es 2 ($a^1 + b^1 = 2$). Falta una dimensión.

**La corrección:**
El desarrollo correcto es $a^3 + 3a^2b + 3ab^2 + b^3$. Aquí puedes revisar que en cada término la suma de exponentes es exactamente 3: (3), (2+1=3), (1+2=3), y (3). Si recuerdas esto, jamás olvidarás los cuadrados en los términos mixtos centrales.""",

    # ------------------- CUADRADO DE TRINOMIO -------------------
    "mat-alg-cuadrado-trinomio-definicion.yaml": """El cuadrado de un trinomio se representa como $(a+b+c)^2$. Su significado intrínseco es multiplicar un polinomio de tres términos por sí mismo: $(a+b+c)(a+b+c)$.

**Desarrollo algebraico por distributividad:**
Si distribuimos cada elemento del primer paréntesis a todos los elementos del segundo (es decir, $a$ por los tres, $b$ por los tres, y $c$ por los tres), generaremos en total 9 términos intermedios:
$a^2 + ab + ac + ba + b^2 + bc + ca + cb + c^2$

Si ordenamos esta expresión y agrupamos los términos semejantes (ya que $ab=ba$, $ac=ca$ y $bc=cb$), obtenemos un polinomio estructurado, simétrico y ordenado de seis términos finales.

**Fórmula del Cuadrado de Trinomio:**
$(a+b+c)^2 = a^2 + b^2 + c^2 + 2ab + 2ac + 2bc$

El resultado consta de la suma de los cuadrados individuales de cada término original, seguidos por el doble producto de cada combinación de pares posibles.""",

    "mat-alg-cuadrado-trinomio-regla-general.yaml": """La regla del cuadrado de un trinomio es una de las fórmulas más elegantes por su perfecta simetría matemática.

**Fórmula:** $(a+b+c)^2 = a^2 + b^2 + c^2 + 2ab + 2bc + 2ac$

**La regla en palabras (El patrón visual):**
Para desarrollarlo rápidamente en tu cabeza, divide el resultado en dos grandes bloques lógicos:
1. **El bloque de los cuadrados individuales:** Primero eleva cada uno de los tres términos al cuadrado y súmalos ($a^2 + b^2 + c^2$).
2. **El bloque de los dobles productos:** Luego, imagina que los tres términos forman combinaciones de a dos (parejas). Debes escribir el doble de cada una de esas tres parejas posibles ($2ab$, $2bc$, y $2ac$).

Esta regla nos ahorra tener que efectuar y reducir los nueve términos de la multiplicación distributiva, simplificando enormemente expansiones algebraicas mayores.""",

    "mat-alg-cuadrado-trinomio-representacion-area.yaml": """La fórmula $(a+b+c)^2$ se puede visualizar y demostrar fácilmente utilizando geometría de áreas, extendiendo la misma lógica del cuadrado del binomio.

Imagina un gran cuadrado cuyo lado está dividido en tres segmentos consecutivos de longitudes $a$, $b$, y $c$. Su área total es $(a+b+c)^2$.
Si trazamos líneas rectas cruzando el cuadrado en las divisiones de cada segmento, el cuadrado grande quedará parcelado en una grilla interior de 9 áreas más pequeñas (3x3):
- La diagonal contendrá **tres cuadrados perfectos**, de áreas $a^2$, $b^2$, y $c^2$.
- Fuera de la diagonal, encontraremos **rectángulos que vienen en pares idénticos**:
  - Dos rectángulos de lados $a$ y $b$ (área $2ab$).
  - Dos rectángulos de lados $b$ y $c$ (área $2bc$).
  - Dos rectángulos de lados $a$ y $c$ (área $2ac$).

Al sumar estas 9 piezas geométricas formamos la fórmula completa: $a^2 + b^2 + c^2 + 2ab + 2bc + 2ac$. Esta visualización explica por qué siempre hay "dobles productos".""",

    "mat-alg-cuadrado-trinomio-manejo-signos.yaml": """Cuando elevamos un trinomio al cuadrado que incluye restas, como $(a-b-c)^2$, no hace falta memorizar una fórmula nueva con diferentes signos. Podemos usar la misma regla original $(a+b+c)^2$ con un principio clave: **cada término incluye su propio signo**.

**¿Cómo proceder?**
En $(a - b - c)^2$, considera que los tres términos son: $+a$, $-b$, y $-c$. Aplica la regla normal incorporando estos signos:

1. **Bloque de cuadrados (Siempre positivos):**
   $(a)^2 + (-b)^2 + (-c)^2 = a^2 + b^2 + c^2$. *(¡Todo número real al cuadrado es positivo!)*

2. **Bloque de dobles productos (Dependen de las parejas):**
   - Par 1: $2(a)(-b) = -2ab$
   - Par 2: $2(a)(-c) = -2ac$
   - Par 3: $2(-b)(-c) = +2bc$ *(Menos por menos da más)*

**Resultado final ensamblado:**
$a^2 + b^2 + c^2 - 2ab - 2ac + 2bc$.
El bloque inicial siempre será positivo. Los signos de los dobles productos cambiarán naturalmente al multiplicar las combinaciones.""",

    "mat-alg-cuadrado-trinomio-omision-productos-dobles.yaml": """El error algebraico más crítico al enfrentar un cuadrado de un trinomio $(a+b+c)^2$ es asumir, por falta de rigor o prisa, que el exponente se puede repartir directamente sobre cada sumando.

**El error en cuestión:**
$(a+b+c)^2 \\neq a^2 + b^2 + c^2$

**Por qué es incorrecto:**
Distribuir potencias solo es matemáticamente válido a través de multiplicaciones o divisiones (ej. $(abc)^2 = a^2b^2c^2$), NUNCA a través de sumas o restas. Si omites los dobles productos ($2ab+2ac+2bc$), estás ignorando deliberadamente seis de los nueve términos que se originan de la distributividad real $(a+b+c)(a+b+c)$.

Si un estudiante comete este error calculando áreas o valores numéricos, estaría perdiendo gran parte del valor total. Para recordarlo, asimila que las sumas "generan puentes" (términos cruzados) entre las variables al elevarse a una potencia.""",

    # ------------------- GENERALIZACIONES -------------------
    "mat-alg-generalizaciones-productos-binomio-newton.yaml": """El Teorema del Binomio de Newton es la generalización definitiva. Nos ofrece una fórmula maestra para desarrollar un binomio elevado a cualquier número entero positivo $n$, es decir: $(a+b)^n$.

Imagina tener que calcular $(a+b)^7$ multiplicando paso a paso. Sería eterno y abrumador. El Teorema de Newton sistematiza este proceso utilizando combinatoria matemática (coeficientes binomiales).

**La Fórmula General:**
$(a+b)^n = \\sum_{k=0}^{n} \\binom{n}{k} a^{n-k}b^k$

**Traducción del comportamiento estructural:**
Si despliegas la sumatoria, notarás tres patrones en cada término:
1. **Los exponentes bailan:** En el primer término, '$a$' tiene exponente $n$ y '$b$' tiene exponente $0$. A medida que avanzas en la suma, el exponente de '$a$' disminuye en $1$, mientras que el de '$b$' aumenta en $1$. Al final, '$a$' llega a $0$ y '$b$' llega a $n$. La suma de ambos siempre es $n$.
2. **Los coeficientes:** El número grande que multiplica cada término se calcula resolviendo combinatorias $\\binom{n}{k}$, las cuales pueden ser extraídas fácilmente del Triángulo de Pascal.
3. **Cantidad de términos:** El polinomio desarrollado siempre tendrá $(n+1)$ términos totales.""",

    "mat-alg-generalizaciones-productos-pascal-coeficientes.yaml": """El Triángulo de Pascal es un esquema geométrico de números que nos brinda una forma visual e instantánea de encontrar los coeficientes (los números grandes al frente) de la expansión de cualquier $(a+b)^n$. 

**¿Cómo se construye el triángulo?**
Se empieza con un $1$ en la cima. Cada fila nueva comienza y termina con un $1$. Todos los números interiores se obtienen simplemente sumando los dos números que están justo por encima de él en la fila anterior.

**Relación con los binomios (Los niveles mágicos):**
Cada nivel o "fila" del triángulo nos da los coeficientes exactos para un exponente particular $n$. (Empezamos a contar las filas desde $0$):
- **Fila 0 (Para $n=0$):** `1` -> $(a+b)^0 = 1$
- **Fila 1 (Para $n=1$):** `1, 1` -> $(a+b)^1 = 1a + 1b$
- **Fila 2 (Para $n=2$):** `1, 2, 1` -> $(a+b)^2 = 1a^2 + 2ab + 1b^2$ (El cuadrado)
- **Fila 3 (Para $n=3$):** `1, 3, 3, 1` -> $(a+b)^3$ (El cubo)
- **Fila 4 (Para $n=4$):** `1, 4, 6, 4, 1`

Cuando expandas $(a+b)^n$, solo necesitas observar la fila $n$ del triángulo para conocer tus coeficientes de antemano.""",

    "mat-alg-generalizaciones-productos-termino-general.yaml": """Cuando desarrollamos un binomio elevado a una potencia alta como $(a+b)^{12}$, muchas veces no nos interesa expandir todo el polinomio (que tendría 13 términos), sino que un problema nos pedirá encontrar **un término en específico**, como el quinto término.

Para evitar hacer todo el desarrollo, utilizamos la fórmula del **Término General**, derivada directamente del Binomio de Newton.

**Fórmula del Término de posición $(k+1)$:**
$$T_{k+1} = \\binom{n}{k} a^{n-k} b^k$$

**¿Cómo funciona esta fórmula?**
1. **$n$:** Es el exponente global del binomio original.
2. **$k$:** ¡Cuidado aquí! El valor de $k$ es siempre **uno menos** que la posición que buscas. Si te piden el 5º término ($T_5$), entonces debes usar $k=4$. Si te piden el término 8, usas $k=7$.
3. **El Coeficiente $\\binom{n}{k}$:** Es una combinatoria.
4. **Las potencias:** El primer término interno ($a$) queda elevado a la diferencia $(n-k)$, y el segundo término interno ($b$) se eleva directamente a $k$.

Esta fórmula es el equivalente a un francotirador algebraico: apunta y calcula exactamente lo que necesitas sin esfuerzo extra.""",

    "mat-alg-generalizaciones-productos-cubo-trinomio.yaml": """La generalización del cubo de un trinomio, $(a+b+c)^3$, es una de las expansiones más voluminosas que verás en álgebra básica. Su desarrollo total, a través de multiplicaciones iterativas, genera inicialmente 27 términos que, tras ser agrupados por semejanza, se reducen a 10 términos simétricos.

**Fórmula de expansión:**
$(a+b+c)^3 = a^3 + b^3 + c^3 + 3(a+b)(b+c)(c+a)$

O si la expandimos en formato sumatorio clásico:
$= a^3 + b^3 + c^3 + 3a^2b + 3ab^2 + 3a^2c + 3ac^2 + 3b^2c + 3bc^2 + 6abc$

**El patrón oculto (Análisis de la simetría):**
Para comprender esta enorme fórmula sin memorizarla, nota cómo se compone su estructura:
1. **Cubo de cada elemento:** Aparecen todos los cubos individuales ($a^3, b^3, c^3$).
2. **Interacciones binarias:** Aparecen todas las interacciones donde un término está al cuadrado y otro lineal, al igual que en un cubo de binomio. Cada par posible tiene estas interacciones multiplicadas por 3 (ej. $3a^2b + 3ab^2$).
3. **Interacción trinaria central:** El término especial final es la interacción conjunta única donde los tres elementos se multiplican de forma lineal: $6abc$. Esta es la huella digital exclusiva de los trinomios cúbicos."""
}

files = glob.glob('docs/conocimiento/contenido/mat-alg-*.yaml')
updated_count = 0

for f in files:
    filename = f.split('\\')[-1].split('/')[-1]
    if filename in explanations:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Buscar el bloque explicacion:
        match = re.search(r'^explicacion:\s*\|(.*?)^\w+:', content, re.MULTILINE | re.DOTALL)
        if not match:
            continue
            
        new_text = explanations[filename]
        # Reemplazar comillas simples con ''
        new_text = new_text.replace("'", "''")
        
        # Indent every line with two spaces
        indented_text = "\n".join("  " + line for line in new_text.split("\n"))
        
        new_block = "explicacion: |\n" + indented_text + "\n"
        new_content = content[:match.start()] + new_block + content[match.end()-len(match.group(0).split('\n')[-1]):]
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        updated_count += 1

print(f"Updated {updated_count} files.")
