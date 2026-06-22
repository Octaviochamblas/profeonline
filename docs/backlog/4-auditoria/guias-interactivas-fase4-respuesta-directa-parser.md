# Guías interactivas — Fase 4: respuesta directa (parser numérico/algebraico)

- **Estado:** 🟡 Construcción completada por 🧩 Codex (2026-06-22) · en auditoría · ⚠️ `seguridad:requiere-claude`
- **Creado:** 2026-06-22 · **Epic padre:** `1-por-iniciar/guias-interactivas-banco-estandarizado-items.md`
- **Prioridad:** P1 · **Cartera:** educativa · **Tipo:** producto · seguridad
- **Dueño:** 🧩 Codex (construye y audita, rama `codex/guias-fase4-parser`, por decisión del usuario) →
  🏛️ Claude (cierre y revisión de seguridad)

> **Alcance: motor de corrección de respuesta directa + edición/publicación mínima de esas preguntas
> + integración en la práctica no académica de Fase 3.** Las evaluaciones persistentes por nivel/final
> son Fase 5. La entrada pertenece al alumno: AST restringido y construcción explícita de objetos
> SymPy, **nunca `eval`, `exec`, `parse_expr`, `eval_expr` ni `sympify(<string>)`**.

## Objetivo

Corregir respuestas escritas por el alumno comparándolas con `Question.canonical_answer`:

- numéricas: enteros, decimales con coma o punto y fracciones, con tolerancia absoluta;
- algebraicas: expresiones polinómicas o racionales formalmente equivalentes.

## Código real y decisiones resueltas por preflight

- Los campos ya existen en `Question`: `question_type`, `canonical_answer` y `answer_tolerance`.
- `QuizAttemptAnswer.text_answer` y `EvaluationSessionAnswer.text_answer` ya existen para Fase 5,
  pero **la práctica de Fase 3 es efímera** y no crea intentos. En esta fase no se guarda
  `text_answer` en BD: se mantiene solo en memoria para renderizar el resultado actual.
- `visible_bank_service` genera hoy únicamente preguntas `alternativa` con cuatro `Choice`. Fase 4
  no cambia la mezcla generada por IA: el panel editorial permitirá convertir un borrador visible a
  `numerica`/`algebraica`, editar su respuesta canónica/tolerancia y volverlo a publicar manualmente.
- El reproductor detecta hoy respuestas únicamente mediante radios; debe generalizarse de forma
  retrocompatible para reconocer radios y campos de texto.
- SymPy no está instalado. Agregar `sympy==1.14.0` a `requirements.txt`; no se anticipa migración.
- SymPy documenta que `parse_expr` usa `eval`; queda expresamente prohibido incluso con diccionarios
  restringidos. `simplify()` general también se excluye por ser heurístico y potencialmente lento.

## 1. Contrato del servicio

Crear `apps/content/services/answer_grading_service.py`:

```python
def grade_answer(question, raw_text: str) -> dict:
    """
    {
        "correct": bool,
        "normalized": str,
        "reason": str,
    }
    """
```

`reason` es un código estable, no una excepción ni texto interno:

```text
correct
incorrect
empty
invalid_format
limits_exceeded
grading_timeout
invalid_canonical
unsupported_type
```

- Nunca propagar mensajes internos de AST/SymPy al alumno ni incluir la entrada en logs.
- `normalized` contiene una representación normalizada segura o `""` si el parseo falla.
- `alternativa` conserva el flujo existente; `grade_answer` atiende solo `numerica` y `algebraica`.
- Tanto la respuesta del alumno como `canonical_answer` pasan por el mismo parser restringido. La
  respuesta canónica es editorialmente confiable, pero no debe entrar por una API insegura.

## 2. Numéricas: gramática y tolerancia

Implementar con biblioteca estándar (`decimal.Decimal` y/o `fractions.Fraction`), sin SymPy:

- formatos admitidos: `-12`, `12.5`, `12,5`, `-3/4`, con espacios solo en los extremos;
- fracción: numerador y denominador enteros con signo; denominador distinto de cero;
- no admitir separadores de miles, `%`, notación científica, `NaN`, `Infinity` ni expresiones;
- máximo 100 caracteres y máximo 30 dígitos significativos;
- normalizar coma decimal a punto únicamente cuando el formato completo sea válido.

Semántica de `answer_tolerance`:

- es **tolerancia absoluta**, en las mismas unidades de la respuesta;
- `None` o `0` significa igualdad exacta;
- debe ser finita y `>= 0`; un valor inválido bloquea publicación y al corregir produce
  `invalid_canonical`;
- comparación: `abs(student - canonical) <= tolerance`, usando representación decimal/racional
  exacta y nunca `float` para la respuesta ingresada.

## 3. Algebraicas: parser seguro y equivalencia

### Gramática admitida

- números enteros/decimales, variables ASCII de una letra minúscula, `+ - * / **`, paréntesis y
  operadores unarios `+/-`;
- aceptar multiplicación implícita pedagógica (`2x`, `2(x+1)`, `(x+1)(x-1)`) mediante un
  **tokenizador propio acotado** que inserta `*` antes de `ast.parse`;
- aceptar `^` como alias de `**` antes del AST;
- no admitir LaTeX, `=`, comparaciones, booleanos, cadenas, listas, atributos, subscripts,
  comprehensions, lambdas, asignaciones, llamadas ni nombres de funciones/constantes.

### Construcción

1. Tokenizar y normalizar la cadena con código propio.
2. Ejecutar únicamente `ast.parse(normalized, mode="eval")`; parsear AST no ejecuta el código.
3. Recorrer con un visitor de lista blanca.
4. Construir nodo a nodo objetos `sympy.Integer`, `sympy.Rational`, `sympy.Symbol`,
   `sympy.Add`, `sympy.Mul` y `sympy.Pow`.
5. No pasar strings del usuario a ninguna función de parseo de SymPy.

Nodos AST permitidos:

```text
Expression, BinOp, UnaryOp, Constant, Name,
Add, Sub, Mult, Div, Pow, UAdd, USub, Load
```

Rechazar cualquier otro nodo por defecto.

### Límites duros

Definir constantes y comprobarlas antes/durante la construcción:

```text
MAX_ALGEBRA_LENGTH = 200
MAX_AST_NODES = 80
MAX_OPERATORS = 30
MAX_VARIABLES = 3
MAX_EXPONENT_ABS = 8
MAX_INTEGER_DIGITS = 12
MAX_NESTING = 12
MAX_RESULT_OPS = 120
GRADING_TIMEOUT_SECONDS = 0.5
```

- el exponente debe ser un literal entero, incluido entero negativo, nunca otra expresión;
- las variables del alumno deben ser subconjunto exacto de las variables de la respuesta canónica;
- rechazar resultados con `zoo`, `nan`, infinitos o denominador idénticamente cero;
- proteger la operación simbólica con timeout de pared en Linux (`signal.setitimer`, restaurando
  handler/timer en `finally`). En plataformas sin `SIGALRM`, permanecen obligatorios todos los
  límites estructurales; los tests de timeout pueden condicionarse por plataforma.

### Equivalencia

- comprobar primero `expr.is_rational_function(*symbols) is True` en ambas expresiones;
- comparar con simplificación dirigida:

```python
cancel(together(student_expr - canonical_expr)) == 0
```

- no usar `simplify()`;
- la equivalencia es la de **funciones racionales formales**: se aceptan cancelaciones con
  discontinuidades removibles, por ejemplo `(x**2 - 1)/(x - 1)` y `x + 1`.

## 4. Panel editorial y publicación

Extender el modo `scope=banco_visible` de `question_review`:

- editar `question_type`, `canonical_answer` y `answer_tolerance`;
- para `alternativa`, mantener cuatro alternativas, exactamente una correcta y sincronización de
  `canonical_answer`;
- para `numerica`, exigir respuesta canónica numérica válida; tolerancia opcional válida;
- para `algebraica`, exigir respuesta canónica algebraica válida y `answer_tolerance=None`;
- ocultar las alternativas para tipos directos, pero **no borrarlas automáticamente** al convertir:
  quedan ignoradas y permiten revertir a `alternativa` sin pérdida;
- cambiar tipo, respuesta canónica, tolerancia, enunciado o alternativas devuelve la pregunta a
  `borrador`;
- la publicación manual debe ejecutar la validación específica del tipo y bloquear datos inválidos.

Corregir al tocar este flujo el defecto existente en
`apps/content/views/question_review.py:add_choice_inline`: actualmente una pregunta visible se
archiva al intentar agregar una alternativa. Debe permitir alternativas solo en tipo `alternativa`
y devolver HTTP 400 para tipos directos, nunca archivar por esa acción.

No ampliar en esta fase la generación IA para decidir automáticamente el tipo de pregunta.

## 5. Integración en práctica visible

Plantilla:

- `alternativa`: radios actuales;
- `numerica`/`algebraica`: `<input type="text">` con el mismo nombre
  `question_<id>`, `autocomplete="off"`, longitud máxima y etiqueta accesible;
- no exponer `canonical_answer` en atributos HTML antes del submit.

Submit:

1. Cargar/revalidar primero las preguntas guardadas en sesión, como ya hace Fase 3.
2. Interpretar el valor según `question.question_type`, nunca según el aspecto del valor recibido.
3. Rechazar claves `question_*` ajenas y parámetros duplicados (`QueryDict.getlist()` con más de un
   valor para una pregunta).
4. En `alternativa`, validar que el ID corresponde a un `Choice` de la pregunta.
5. En tipos directos, pasar el texto a `grade_answer`.
6. Mantener resultados/recomendaciones efímeros; no crear `QuizAttempt`,
   `QuizAttemptAnswer`, `EvaluationSessionAnswer`, XP ni cambios de dominio.
7. Renderizar en resultados la respuesta ingresada, corrección y explicación. Las plantillas Django
   deben autoescapar el texto; no usar `safe`.

`static/js/quiz-player.js`:

- reemplazar el detector exclusivo de radios por un helper común basado en
  `[data-quiz-answer]`;
- un radio cuenta si está marcado; un texto cuenta si `value.trim()` no está vacío;
- escuchar `change` e `input` para actualizar revisión;
- conservar el contrato DOM, CSP, foco, cierre y comportamiento de quizzes legacy.
- subir cache-buster de `quiz-player.js` en `base.html`.

## 6. Página de guía

- Para tipos directos no renderizar una lista de alternativas vacía.
- “Ver solución” y el solucionario siguen mostrando `canonical_answer`.
- No agregar corrección interactiva fuera del reproductor en esta fase.

## 7. Aislamiento y alcance

- Solo preguntas `scope="banco_visible"` de temas con `structured_bank_enabled=True`.
- El quiz legacy continúa filtrando `scope=""` y no consume este parser.
- Fase 5 reutilizará `grade_answer` para `EvaluationSessionAnswer`, pero esa persistencia, puntaje,
  timers, intentos y dominio quedan explícitamente fuera.
- Sin red y sin IA durante la corrección.
- Sin migración prevista.

## Criterios de aceptación

- [ ] `sympy==1.14.0` fijado en requirements y barrera completa verde.
- [ ] Numéricas equivalentes: `1/2`, `0.5` y `0,5`; tolerancia absoluta documentada y testeada.
- [ ] Algebraicas equivalentes: `2(x+1)`, `2x+2` y formas racionales admitidas.
- [ ] No equivalentes e inválidas rechazadas con códigos estables.
- [ ] Cero uso de `eval`, `exec`, `parse_expr`, `eval_expr`, `lambdify` o `sympify(string)`.
- [ ] Límites estructurales y timeout probados; ninguna entrada ejecuta código.
- [ ] Canonical inválida o tolerancia no finita bloquean publicación.
- [ ] Preguntas directas editables y publicables manualmente desde el panel visible.
- [ ] Práctica mixta soporta alternativa + numérica + algebraica sin persistencia académica.
- [ ] Submit rechaza IDs, tipos y parámetros duplicados manipulados.
- [ ] `quiz-player.js` conserva quizzes legacy y reconoce respuestas de texto.
- [ ] Pista/solución, CSP, KaTeX y progreso siguen intactos.

## Plan mínimo de pruebas

- Numéricas: signo, entero, coma/punto, fracción, denominador cero, basura, vacío, exceso de
  longitud/dígitos, tolerancia nula/cero/positiva, `NaN`/infinito/notación científica.
- Algebraicas: expansión, factorización, multiplicación implícita, `^`, racionales, exponentes
  negativos acotados, variables no permitidas, no equivalentes y canonical inválida.
- Inyección: `__import__`, llamadas, atributos, subscripts, strings, lambda, comprehensions,
  asignación, `open`, `globals`, `Symbol`, funciones SymPy y payloads con saltos/separadores.
- Recursos: longitud, nodos, operadores, variables, profundidad, dígitos, exponente, operaciones
  resultantes y timeout.
- Editorial: conversión de tipo, vuelta a borrador, validación por tipo, `add_choice_inline` no
  archiva y tipos directos no aceptan alternativas nuevas.
- Runtime: práctica mixta, respuesta omitida, parámetros duplicados/ajenos, revalidación de estado,
  cero filas nuevas de intentos/respuestas y progreso idéntico antes/después.
- Frontend: revisión detecta texto, cierre advierte si hay texto, radios legacy sin regresión,
  cache-buster/CSP y presentación sin alternativas en tipos directos.

## No-objetivos

- Ecuaciones con `=`, sistemas, funciones (`sqrt`, trigonometría, logaritmos), unidades, complejos,
  matrices o LaTeX.
- Generación IA automática de preguntas directas.
- Evaluaciones por nivel/final, persistencia de respuestas, puntajes ponderados, timers o dominio.

## Rollback

- Desactivar `Topic.structured_bank_enabled` para el tema afectado.
- Volver editorialmente las preguntas a `question_type="alternativa"`; el sistema legacy permanece
  aislado mediante `scope=""`.

## Preflight 🧩 Codex — 2026-06-22

**Resultado:** listo para construir con este handoff refinado.

- El modelo ya contiene todos los campos y tablas futuras; no hace falta migración para Fase 4.
- La práctica visible no debe persistir `text_answer`; esa responsabilidad pertenece a Fase 5.
- Se definió un parser AST→SymPy sin APIs que evalúan strings y con límites/timeout concretos.
- Se resolvieron tolerancia absoluta, multiplicación implícita, equivalencia racional y contrato de
  errores.
- Se añadió el flujo editorial mínimo y la adaptación retrocompatible necesaria del reproductor.
- La rama sigue marcada `seguridad:requiere-claude`; 🏛️ Claude debe revisar el parser en cierre.

## Referencias primarias

- SymPy 1.14 — parsing: `parse_expr` usa `eval` y no es apto para entrada no confiable:
  https://docs.sympy.org/latest/modules/parsing.html
- SymPy — buenas prácticas: preferir `cancel`/operaciones dirigidas sobre `simplify` general:
  https://docs.sympy.org/latest/explanation/best-practices.html
- SymPy — deprecaciones y riesgos históricos del parseo de strings:
  https://docs.sympy.org/latest/explanation/active-deprecations.html
- SymPy 1.14.0 en PyPI:
  https://pypi.org/project/sympy/

## Qué se hizo — construcción 🧩 Codex (2026-06-22)

- Se agregó `sympy==1.14.0` y el servicio `answer_grading_service.py`.
- Numéricas con `Fraction`/`Decimal`: enteros, coma/punto, fracciones y tolerancia absoluta sin
  convertir la respuesta del alumno a `float`.
- Algebraicas mediante tokenizador propio, multiplicación implícita, AST de lista blanca y
  construcción nodo a nodo de objetos SymPy. No se usan APIs SymPy de parseo de strings ni
  ejecución dinámica.
- Límites implementados: longitud, dígitos, nodos AST, operadores, variables, exponentes,
  profundidad, operaciones resultantes y timeout Linux con restauración segura de señales.
- Panel editorial ampliado con tipo, respuesta canónica y tolerancia; validación por tipo antes de
  publicar; conversiones vuelven a borrador y conservan alternativas ignoradas.
- Corregido `add_choice_inline`: ya no archiva preguntas visibles; alternativas solo se mutan en
  preguntas de tipo `alternativa`.
- Práctica de Fase 3 ampliada para mezclar radios y respuestas de texto, rechazar parámetros
  duplicados/ajenos, corregir según el tipo almacenado y mantener cero persistencia académica.
- Reproductor actualizado con `data-quiz-answer`, eventos `input/change` y cache-buster `?v=2`;
  quizzes legacy conservan el mismo flujo.
- Página de guía oculta alternativas preservadas en preguntas directas; resultados autoescapan la
  entrada del alumno y muestran mensajes seguros de formato/límites/timeout.
- Aislamiento por `Topic.structured_bank_enabled` reforzado en mutaciones editoriales individuales.

### Evidencia de construcción

- Suite completa: **493 tests OK** en **377,622 s** (`1 skipped` local: prueba específica de
  `SIGALRM`, no disponible en Windows; se ejecuta en CI Linux).
- Tests focalizados finales: **34 OK**, `1 skipped` por la misma razón.
- `check --deploy --fail-level ERROR` con settings/variables de CI: exit 0; solo warning conocido
  `core.W001` por Redis ausente localmente.
- `makemigrations --check --dry-run`: `No changes detected`.
- `pip-audit -r requirements.txt`: `No known vulnerabilities found`.
- `pre-commit run --all-files`, Ruff, `node --check` y `git diff --check`: verdes.
