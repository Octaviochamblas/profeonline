# Biblioteca de Aprendizaje — Contenidos, Dominio y Prerrequisitos

- **Estado:** Handoff Ready (arquitectura)
- **Creado:** 2026-06-26 · **Redactado por:** 🏛️ Claude
- **Prioridad:** P1 · **Cartera:** educativa / retención
- **Tipo:** producto · pedagogía
- **Épico:** 3 fases en orden; el mapa gamificado (F4) es tarjeta separada posterior.
- **Dueño:** 🧩 Codex (preflight por fase) → 🔨 Antigravity (construcción) → 🏛️ Claude (cierre)

> **Origen:** conversación 2026-06-25/26. El árbol taxonómico (700 recursos, 37 bloques, 5 ejes)
> ya existe en `docs/conocimiento/` y en DB vía `seed_math_resources`. Esta tarjeta construye
> la **capa de aprendizaje** encima: contenido pedagógico, evaluación de dominio y prerrequisitos.
> El mapa gamificado NO está en alcance aquí; se retoma cuando F1–F3 estén validados en producción.

---

## Decisiones cerradas (🧑 + 🏛️, 2026-06-26)

1. **Fuente del contenido:** bibliografía en NotebookLM. Se genera texto pedagógicamente ordenado
   (como AlonsoFormula): explicación → procedimiento → ejemplos resueltos → errores frecuentes.
   No video por ahora; texto + ejercicios.
2. **Definición de dominio:** el alumno demuestra que puede resolver ejercicios *nuevos* de ese
   recurso, sin ayuda, con nivel suficiente de acierto **y cubriendo los tipos principales** de
   ejercicio de ese recurso. No basta con ver el contenido ni resolver un solo tipo.
3. **Secuencia:** F1 (contenido + páginas públicas) → F2 (dominio) → F3 (prerrequisitos DAG).
   El mapa gamificado viene después de validar F1–F3 en producción.
4. **Experiencia pública:** página sobria por recurso, sin necesidad de cuenta. Con cuenta se
   guarda el progreso y se desbloquea la ruta personalizada (eso es F4, fuera de alcance aquí).
5. **Una sola base de contenido:** el mismo contenido sirve para la vista pública y (en el futuro)
   para el mapa gamificado. No duplicar.

---

## Objetivo

Convertir el esqueleto taxonómico YAML (700 recursos atómicos) en una **biblioteca web pública
de aprendizaje matemático**, donde cada recurso tiene contenido pedagógico generado desde
bibliografía real, ejercicios por tipo, evaluación de dominio y prerrequisitos explícitos, de modo
que cualquier persona pueda llegar, aprender y medir su avance — y que esa misma base sirva de
fundamento al mapa gamificado posterior.

---

## Fuentes a leer (rutas concretas)

**Árbol taxonómico:**
- `docs/conocimiento/_REGISTRO-CODIGOS.md` — índice de todos los bloques y sus archivos YAML
- `docs/conocimiento/*.yaml` — un archivo por bloque; estructura EE.BB.TT.RR + id semántico

**Modelos existentes a entender antes de diseñar:**
- `apps/subjects/models.py` — `Subject`, `Topic`, `Resource`; cómo están relacionados y qué campos ya tiene `Resource`
- `apps/questions/models.py` — `Question`, `QuizAttempt`; banco de preguntas y estructura de intentos
- `apps/questions/services/progress_service.py` — lógica de progreso ya existente (no duplicar)
- `apps/questions/views/` — cómo se sirven preguntas hoy (reusar en el motor de evaluación)

**Seed y pipeline:**
- `apps/subjects/management/commands/seed_math_resources.py` — cómo se carga el árbol YAML a DB; el `id` semántico (`MAT.NUM...`) debe ser el enlace entre YAML y contenido
- `config/settings/local.py` y `config/settings/production.py` — settings relevantes

**Referencia de diseño:**
- Página de recurso existente (`apps/subjects/views/` o similar) — punto de partida visual

---

## Arquitectura propuesta

### Modelo de datos nuevos

#### `ResourcePage`
Contenido pedagógico de un recurso. Uno a uno con `Resource` (por `resource_semantic_id`).

```
ResourcePage
  resource          → FK(Resource, unique=True)
  objetivo          → TextField  ("Al finalizar, el alumno será capaz de…")
  explicacion       → TextField  (Markdown; texto pedagógico principal)
  procedimiento     → JSONField  (lista ordenada de pasos ["Paso 1: …", "Paso 2: …"])
  ejemplos          → JSONField  (lista de {titulo, enunciado, solucion_pasos: []})
  errores_frecuentes → JSONField (lista de strings)
  estado            → CharField  choices: borrador | publicado
  fuente_notebooklm → TextField  (referencia a la fuente usada para auditoría)
  created_at / updated_at
```

> **Nota:** `explicacion` en Markdown; el template lo renderiza con la misma pipeline KaTeX
> que ya existe. No inventar un nuevo parser.

#### `ResourcePrerequisite`
DAG de prerrequisitos entre recursos.

```
ResourcePrerequisite
  recurso           → FK(Resource, related_name='prerrequisitos_entrantes')
  requiere          → FK(Resource, related_name='prerrequisitos_salientes')
  tipo              → CharField  choices: requerido | recomendado
  mastery_minimo    → FloatField  default=0.75  (umbral para considerar el prerrequisito cumplido)
  class Meta: unique_together = ('recurso', 'requiere')
```

#### `StudentResourceState`
Estado de un alumno en un recurso.

```
StudentResourceState
  student           → FK(settings.AUTH_USER_MODEL)
  resource          → FK(Resource)
  estado            → CharField  choices: no_iniciado | en_progreso | dominado
  estrella_contenido → BooleanField  default=False  (leyó la explicación y ejemplos)
  estrella_practica  → BooleanField  default=False  (completó práctica cubriendo tipos principales)
  estrella_dominio   → BooleanField  default=False  (aprobó evaluación de dominio)
  mastery_score     → FloatField   null=True  (último score de evaluación de dominio)
  intentos_evaluacion → PositiveIntegerField  default=0
  ultimo_intento    → DateTimeField  null=True
  tipos_cubiertos   → JSONField   default=list  (qué tipos de ejercicio ha resuelto)
  class Meta: unique_together = ('student', 'resource')
```

---

### Definición técnica de dominio

Un recurso se considera **dominado** (`estrella_dominio = True`) cuando la evaluación de dominio retorna:

1. **Score ≥ umbral del recurso** (default 0.75; configurable por recurso en `ResourcePage` si es necesario).
2. **Cobertura de tipos:** la evaluación incluyó al menos 1 ejercicio de cada `tipo` marcado como
   principal en el banco de preguntas de ese recurso. Si hay tipos sin preguntas, se omiten.
3. La evaluación usa preguntas **distintas a las de práctica** (banco separado por flag `es_evaluacion=True`
   vs `es_practica=True` en `Question`). Si el banco no tiene suficientes preguntas distintas hoy,
   se acepta reusar pero se registra la limitación.

El motor de evaluación de dominio **reutiliza** el banco de preguntas existente y `QuizAttempt`;
no es un sistema nuevo, es una nueva _configuración_ del sistema existente.

---

### Pipeline de generación de contenido (NotebookLM → DB)

El contenido se genera fuera del repo (NotebookLM + revisión humana) y se carga mediante
un comando de gestión. El flujo es:

```
NotebookLM (bibliografía) → prompt estructurado → texto pedagógico por recurso
→ revisión/edición manual por el 🧑
→ archivo YAML de contenido (uno por bloque, en docs/conocimiento/contenido/)
→ comando: python manage.py load_resource_content <bloque>
→ crea/actualiza ResourcePage en DB
```

**Estructura del YAML de contenido** (`docs/conocimiento/contenido/numeros-fracciones.yaml`):

```yaml
bloque_codigo: "02.03"
recursos:
  - resource_id: MAT.NUM.RACIONALES.FRACCION_CONCEPTO
    objetivo: "Comprender qué es una fracción como parte de un entero."
    explicacion: |
      Una fracción representa una o varias partes iguales de un todo...
    procedimiento:
      - "Identifica el entero (el todo)."
      - "Determina en cuántas partes iguales se divide."
      - "Cuenta cuántas partes se toman."
    ejemplos:
      - titulo: "Fracción de una pizza"
        enunciado: "Si una pizza se divide en 8 trozos y comes 3, ¿qué fracción comiste?"
        solucion_pasos:
          - "El todo son 8 trozos."
          - "Tomamos 3 trozos."
          - "La fracción es 3/8."
    errores_frecuentes:
      - "Confundir numerador y denominador."
      - "Pensar que el denominador indica cuántas partes se tomaron."
    fuente: "Santillana 7B pág. 112"
    estado: publicado
```

**Comando `load_resource_content`:**
- Lee el YAML de contenido del bloque indicado.
- Para cada entrada, busca el `Resource` por `resource_semantic_id` (campo que ya existe o
  debe agregarse al modelo `Resource`).
- Crea o actualiza `ResourcePage` (upsert por resource).
- Imprime resumen: cuántos creados, cuántos actualizados, cuántos no encontraron Resource.

---

### Páginas públicas (modo "Aprender")

**URL:** `/aprender/<eje-slug>/<bloque-slug>/<recurso-slug>/`
Ejemplo: `/aprender/numeros/fracciones/fraccion-concepto/`

**Template de recurso** (`templates/aprender/recurso_detalle.html`):

```
Título del recurso
Competencia · Dificultad · Cursos
Objetivo de aprendizaje

[ Antes de empezar: prerrequisitos recomendados con estado del alumno si tiene cuenta ]

Explicación
  (texto pedagógico, renderizado con KaTeX)

Procedimiento
  1. Paso uno
  2. Paso dos
  ...

Ejemplos resueltos
  [Ejemplo 1 — con solución paso a paso expandible]
  [Ejemplo 2 …]

Practica
  [Ejercicios por tipo — reutiliza el banco existente]
  Tipo 1: concepto básico (N ejercicios)
  Tipo 2: aplicación
  Tipo N: tipo PAES

Errores frecuentes
  [Lista]

[ Si tiene cuenta: botón "Evaluar dominio" ]
[ Si no tiene cuenta: "Crea una cuenta para guardar tu avance" ]

Siguiente recurso recomendado →
```

---

### Prerrequisitos DAG — carga desde YAML

Los YAMLs de `docs/conocimiento/` ya tienen campo `prerrequisitos` planificado (ver
`_REGISTRO-CODIGOS.md`, "Pasadas pendientes"). La pasada de prerrequisitos:

1. Se añade `prerrequisitos` a cada recurso en los YAML de contenido (o en un YAML
   separado `docs/conocimiento/dag/prerrequisitos.yaml`).
2. Comando `load_prerequisites` crea `ResourcePrerequisite` en DB.
3. La vista del recurso consulta los prerrequisitos y muestra su estado si el alumno
   tiene cuenta (verde = dominado, amarillo = en progreso, gris = no iniciado).
4. No hay bloqueo duro: si el alumno no tiene los prerrequisitos, ve el recurso igual
   pero con aviso "Te recomendamos completar antes: [lista con links]".

---

## Fases y gates

### F1 — Contenido + Páginas públicas (piloto 1 bloque)

**Alcance:** 1 bloque piloto (~8–12 recursos). Recomendado: `02.03 — Racionales / Fracciones`
(alta conexión con otros contenidos, muy buscado en Google, permite probar todo el pipeline).

**Entregables:**
- Modelo `ResourcePage` + migración
- Comando `load_resource_content`
- URLs `/aprender/...`
- Template de recurso (sobrio, con KaTeX, mobile-first)
- Seed del bloque piloto con contenido real
- Tests: página carga (200), KaTeX renderiza, contenido del ResourcePage se muestra

**Gate de salida F1:** el 🧑 valida el bloque piloto en producción. El contenido se ve bien,
pedagógicamente ordenado, en móvil y desktop. Solo entonces se continúa con F2.

---

### F2 — Motor de dominio

**Alcance:** `StudentResourceState` + evaluación de dominio + estrellas.

**Entregables:**
- Modelo `StudentResourceState` + migración
- Lógica de dominio en `apps/questions/services/mastery_service.py`:
  - `get_or_create_state(student, resource)` → `StudentResourceState`
  - `mark_content_viewed(student, resource)` → estrella 1
  - `evaluate_mastery(student, resource, quiz_attempt)` → actualiza score, tipos cubiertos, estrella 3
  - `is_mastered(student, resource)` → bool
- Integración en la vista de recurso: botón "Evaluar dominio" (solo usuarios con cuenta)
- La evaluación arma un quiz con preguntas del banco existente, respetando la cobertura de tipos
- Al completar el quiz: actualiza `StudentResourceState`, muestra resultado y estrellas ganadas
- Tests: `mark_content_viewed` otorga estrella 1; evaluación con score ≥ 0.75 y tipos cubiertos
  otorga estrella 3; evaluación fallida no regresa a estado anterior

**Gate de salida F2:** al menos 5 alumnos reales (o el 🧑) completan el flujo
contenido → práctica → evaluación en el bloque piloto. El sistema registra correctamente
el estado de dominio.

---

### F3 — Prerrequisitos DAG

**Alcance:** `ResourcePrerequisite` + visualización en la vista de recurso.

**Entregables:**
- Modelo `ResourcePrerequisite` + migración
- Comando `load_prerequisites <bloque>` que lee YAML y carga el DAG
- Validación: sin ciclos (detectar ciclos en el grafo antes de guardar)
- En la vista de recurso: sección "Antes de empezar" con estado del alumno por prerrequisito
- Comando `validate_dag` que recorre todo el grafo y reporta ciclos o ids rotos
- Tests: carga de prerrequisitos desde YAML, detección de ciclo, vista muestra estado correcto

**Gate de salida F3:** el DAG del bloque piloto + 1 eje completo están cargados y validados.
La vista de recurso muestra correctamente los prerrequisitos con su estado.

---

### F4 — Mapa gamificado (tarjeta futura, NOT IN SCOPE aquí)

Se abre una nueva tarjeta en `backlog/1-por-iniciar/` cuando F1–F3 estén en producción y
validados. Reutiliza toda la base construida aquí: `StudentResourceState`, `ResourcePrerequisite`
y `ResourcePage` son los insumos del mapa. No se construye nada de F4 en esta tarjeta.

---

## No-objetivos (FUERA de esta tarjeta)

- ❌ Mapa visual gamificado, estrellas en interfaz tipo videojuego, XP, insignias (F4)
- ❌ Diagnóstico inicial automático (F4)
- ❌ Generación automática de contenido con IA en tiempo real (el contenido se genera offline
  en NotebookLM y se carga manualmente; la IA no escribe la explicación en tiempo real)
- ❌ Videos propios o curaduría de terceros (se decide en F1 post-piloto si se agrega)
- ❌ Rutas puente automáticas generadas por IA (F4)
- ❌ Poblar los 700 recursos de golpe (MVP es 1 bloque piloto en F1, luego escalar)
- ❌ Ranking, competencia entre alumnos, monedas (F4+)
- ❌ Integración con el sistema de guías interactivas existente (son sistemas paralelos;
  no fusionar en esta tarjeta)

---

## Criterios de aceptación

### F1
- [ ] `ResourcePage` existe en DB y tiene migración limpia
- [ ] `load_resource_content numeros-fracciones` carga el bloque piloto sin errores
- [ ] `/aprender/numeros/fracciones/<slug>/` devuelve 200 para usuarios anónimos
- [ ] KaTeX renderiza fórmulas en la página de recurso (verificar con al menos 1 fórmula real)
- [ ] La página muestra: objetivo, explicación, procedimiento, ejemplos con solución, errores frecuentes
- [ ] Mobile-first: se ve bien en 360px
- [ ] CSP intacta (nonce, sin `unsafe-eval`)
- [ ] Barrera verde: `test` · `check --deploy` · `makemigrations --check`

### F2
- [ ] `StudentResourceState` existe con los campos descriptos
- [ ] Ver la explicación completa → `estrella_contenido = True` (registrado en DB)
- [ ] Completar evaluación con score ≥ 0.75 y cobertura de tipos → `estrella_dominio = True`
- [ ] Completar evaluación con score < 0.75 → `estrella_dominio` no cambia; se registra el intento
- [ ] El estado persiste entre sesiones (no se pierde al cerrar sesión)
- [ ] Usuario anónimo ve el contenido pero no puede evaluar dominio (botón redirige al login)
- [ ] Barrera verde

### F3
- [ ] `ResourcePrerequisite` existe; `load_prerequisites` carga desde YAML sin errores
- [ ] `validate_dag` detecta un ciclo artificial introducido en test y lo reporta
- [ ] La vista de recurso muestra los prerrequisitos con el estado del alumno (verde/amarillo/gris)
- [ ] Un recurso sin prerrequisitos cargados no muestra la sección (no error, simplemente ausente)
- [ ] Barrera verde

---

## Plan de pruebas

### Automáticos (por fase)

**F1:**
- `test_resource_page_public_access` — anónimo ve la página (200)
- `test_resource_page_content_rendered` — objetivo, explicación y ejemplos presentes en HTML
- `test_load_resource_content_command` — carga YAML piloto, verifica count de `ResourcePage`
- `test_csp_intact_on_resource_page` — nonce presente, sin `unsafe-eval`

**F2:**
- `test_mark_content_viewed_grants_star` — star 1 tras ver contenido
- `test_mastery_eval_pass_grants_star` — star 3 tras score ≥ 0.75 y cobertura completa
- `test_mastery_eval_fail_no_regression` — score < 0.75 no cambia estado anterior
- `test_anonymous_cannot_submit_mastery` — 302 a login
- `test_student_state_persists` — state existe en DB tras evaluación

**F3:**
- `test_load_prerequisites_creates_relations`
- `test_validate_dag_detects_cycle`
- `test_resource_page_shows_prerequisites_with_state`

### QA manual (el 🧑 valida en producción antes de cada gate)

- F1: leer una página de recurso en móvil y desktop; verificar que el contenido pedagógico
  es claro y las fórmulas renderizan.
- F2: completar el flujo completo de un recurso (leer → practicar → evaluar) y verificar
  que las estrellas se otorgan correctamente.
- F3: entrar a un recurso con prerrequisitos incompletos y verificar que el aviso aparece
  con los recursos faltantes correctamente identificados.

---

## Riesgos / rollback

- **Contenido de baja calidad desde NotebookLM:** el contenido pasa por revisión manual
  del 🧑 antes de marcarse como `publicado`. El comando carga con `estado: borrador` por
  defecto si el YAML no lo especifica; las páginas con `borrador` no son indexables
  (meta robots `noindex`).
- **`resource_semantic_id` no existe en `Resource`:** si el campo no está, `load_resource_content`
  falla ruidosamente. El preflight de Codex debe confirmar qué campo del modelo existente
  mapea al id semántico del YAML, o si hay que agregar un campo nuevo.
- **Banco de preguntas insuficiente por recurso:** para F2, si un recurso tiene <10 preguntas
  en el banco, la evaluación de dominio lo advierte pero igual funciona con las disponibles.
  Documentar en `ResourcePage.advertencias` (campo opcional).
- **Ciclo en el DAG:** el comando `load_prerequisites` valida ciclos antes de guardar;
  si detecta uno, aborta y reporta sin guardar nada (transacción atómica).
- **Rollback F1:** si la vista de recurso tiene bug, se desactiva desde el URLconf en 1 línea.
  El modelo `ResourcePage` es aditivo; no toca modelos existentes.
- **Rollback F2:** `StudentResourceState` es aditivo. Si hay bug en el motor de dominio,
  se desactiva el botón "Evaluar dominio" desde el template con un flag de settings.

---

## Preflight para 🧩 Codex (antes de cada fase)

**F1:**
- Confirmar cómo está modelado `Resource` hoy: ¿tiene campo `semantic_id` o `resource_id` que mapee a `MAT.NUM...`? Si no, proponer la adición mínima.
- Confirmar que `seed_math_resources` ya carga los recursos del YAML; si no, revisar qué carga.
- Confirmar que el pipeline KaTeX (`katex-init.js`) aplica a templates nuevos automáticamente o si hay que incluirlo explícitamente.
- Confirmar namespace de URLs para no colisionar con el sistema de guías existente.

**F2:**
- Confirmar la estructura de `QuizAttempt` y `progress_service`: qué campos son reutilizables para el motor de dominio sin duplicar lógica.
- Confirmar que el banco de preguntas tiene campo de `tipo` por ejercicio y flag `es_evaluacion` / `es_practica` o equivalente; si no, proponer la migración mínima.

**F3:**
- Confirmar que no existe ya algún modelo de prerrequisito en el código.
- Confirmar que la validación de ciclos no es costosa para el volumen esperado (~700 nodos, ~2000 aristas estimadas al completar todos los ejes).

---

## Construcción para 🔨 Antigravity

- **F1:** rama `feat/biblioteca-f1-contenido-paginas`
  - Modelos + migraciones: `ResourcePage`
  - Comando `load_resource_content`
  - URLs + vistas + template de recurso
  - Seed del bloque piloto en `docs/conocimiento/contenido/numeros-fracciones.yaml`
  - Tests F1 listados arriba
  - Barrera verde antes de PR

- **F2:** rama `feat/biblioteca-f2-dominio` (después del gate F1)
  - Modelos + migraciones: `StudentResourceState`
  - `mastery_service.py`
  - Integración en vista de recurso
  - Tests F2 listados arriba

- **F3:** rama `feat/biblioteca-f3-prerrequisitos` (después del gate F2)
  - Modelos + migraciones: `ResourcePrerequisite`
  - Comandos `load_prerequisites` y `validate_dag`
  - Integración en vista de recurso
  - Tests F3 listados arriba

---

## Qué se hizo

_(Completar al cerrar cada fase, antes de mover a `backlog/6-finalizados/`.)_

**F1:**

**F2:**

**F3:**
