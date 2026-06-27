# Arquitectura basal — Plataforma de Conocimiento ProfeOnline

- **Estado:** Diseño de arquitectura (no es tarjeta de construcción todavía)
- **Creado:** 2026-06-26 · **Redactado por:** 🏛️ Claude
- **Tipo:** arquitectura · fundación
- **Reemplaza:** el handoff anterior `biblioteca-contenidos-dominio-prerrequisitos.md` (eliminado;
  partía de supuestos falsos sobre el código).

> **Objetivo de este documento:** definir la **base de datos y de dominio más sólida posible**
> para que ProfeOnline escale en dos formas que comparten un mismo fundamento:
> **(A) sitio web de consulta** (hoy) y **(B) experiencia gamificada** (futuro).
> La gamificación NO se construye ahora, pero la arquitectura se diseña para que entre sin
> reescribir nada del núcleo.

---

## 0. Hallazgos del código real (estado actual, 2026-06-26)

Antes de diseñar, lo que **realmente** existe hoy (auditado en `apps/content/`):

1. **El árbol taxonómico (700 recursos, `MAT.NUM…`) vive SOLO en `docs/conocimiento/*.yaml`.**
   **No está en la base de datos.** Ningún comando lo importa. Es documentación, no datos vivos.
2. **El sitio vivo es otra cosa:** `seed_math_resources` crea **27 videos de YouTube** hardcodeados
   (Enteros y Racionales) como `Resource`, bajo `Area → Subject → Topic → Resource`.
3. **`Resource` NO tiene `semantic_id`.** No hay forma de unir un video con un nodo del árbol.
4. **Ya existe maquinaria pedagógica:** banco de preguntas (`Question`/`Choice` con tipo, nivel,
   dificultad, ámbito), intentos (`QuizAttempt`, `TopicEvaluationAttempt`), sesiones de evaluación,
   guías de aprendizaje, ítems (`ExerciseItem`), y servicios (`progress_service`,
   `gamification_service`, `evaluation_*`).
5. **Ya existe gamificación parcial:** `XPEvent`, `UserSkill`, `UserStreak`.

**Conclusión:** hay **dos mundos desconectados** — el árbol (planificación) y el sitio (videos).
La arquitectura basal debe resolver esto: **el árbol atómico debe convertirse en el esqueleto vivo
del sistema**, y todo lo demás (contenido, videos, ejercicios, progreso, gamificación) cuelga de él.

> El 🧑 indicó que **no es obligatorio conservar lo actual**: se puede reescribir sobre esta nueva
> arquitectura. Lo que ya funciona (banco, evaluación, XP) se reaprovecha como _adaptadores_, no como
> restricción.

---

## 1. Principios de diseño (las reglas que hacen que escale)

Estos seis principios son el corazón. Todo lo demás se deriva de ellos.

1. **El nodo atómico es la unidad canónica.**
   Contenido, ejercicios, prerrequisitos, dominio y progreso cuelgan **del nodo**, nunca del video
   ni del tema. Un video es un _adjunto_ a uno o varios nodos; no al revés.

2. **El dominio es independiente de la presentación.**
   El grafo de conocimiento y el estado del alumno **no saben** que existe una "página" o un "mapa"
   o "XP". La presentación lee el dominio; el dominio nunca depende de la presentación. → se puede
   agregar el juego después sin tocar la base.

3. **Identidad estable y permanente.**
   `semantic_id` (`MAT.NUM.RACIONALES.FRACCION_CONCEPTO`) es la llave eterna. Sobrevive a renombres,
   reordenamientos y migraciones. Es el punto de unión entre YAML, DB, contenido, ejercicios y
   cualquier referencia externa. El `code` (`02.03.01.01`) es solo para mostrar y ordenar.

4. **El contenido y las reglas son DATOS, no código.**
   La explicación, los ejemplos y **la definición de "dominio"** (umbral, cobertura de tipos) viven
   como datos editables y versionables, no como `if` repartidos por el código.

5. **El estado del alumno es un overlay desacoplado.**
   El progreso es una capa que se _superpone_ al grafo. Las dos presentaciones la leen. La
   gamificación es una **proyección** de ese estado, no un sistema paralelo.

6. **El grafo de prerrequisitos es un DAG validado.**
   Las relaciones "necesitas saber X antes de Y" forman un grafo acíclico dirigido, validado contra
   ciclos. Es la base tanto del aviso "antes de empezar" (sitio) como del desbloqueo (mapa).

---

## 2. Arquitectura en capas

Seis capas. Las capas 1–5 son el **núcleo de dominio** (estable, compartido). La capa 6 son las
**presentaciones** (dos hoy/mañana, intercambiables).

```
┌─────────────────────────────────────────────────────────────────────┐
│  CAPA 6 — PRESENTACIÓN  (proyecciones; leen el núcleo, no lo definen) │
│                                                                       │
│   (A) Sitio de consulta  ──┐              ┌── (B) Mapa gamificado     │
│       público, SEO,        │              │      (FUTURO)             │
│       anónimo-friendly     │              │      login, rutas         │
│                            │              │                           │
│   Mecánica de juego (FUTURO): XP · insignias · rachas · desbloqueo    │
│   → reacciona a EVENTOS del dominio; el dominio no la conoce          │
└───────────────────────────┼──────────────┼───────────────────────────┘
                            │   eventos    │   lecturas
┌───────────────────────────┼──────────────┼───────────────────────────┐
│  NÚCLEO DE DOMINIO  (estable, una sola fuente de verdad)              │
│                                                                       │
│  CAPA 5 — ESTADO DEL ALUMNO   StudentNodeState (solo rendimiento real) │
│           sin "visto" ni "practicó"; solo qué aprobó y qué falló      │
│                                                                       │
│  CAPA 4 — EVALUACIÓN          AssessmentExercise · AssessmentAttempt   │
│           (formal, puntaje)   AssessmentRule · failed_exercise_types   │
│                                                                       │
│  CAPA 3 — BANCO DE EJERCICIOS BookExercise (de libros, con respuestas)│
│           referencia/práctica libre; respuestas siempre visibles       │
│                                                                       │
│  CAPA 2 — CONTENIDO           NodeContent (explicación/ejemplos)       │
│           (qué enseña)        NodeMedia (explicacion · ejerc_resueltos)│
│                                                                       │
│  CAPA 1 — GRAFO DE CONOCIMIENTO   KnowledgeNode (árbol atómico)        │
│           (esqueleto organizador)  NodePrerequisite (aristas DAG)      │
└───────────────────────────────────────────────────────────────────────┘
                            ▲
                            │ importación idempotente por semantic_id
              docs/conocimiento/*.yaml  (taxonomía, fuente de verdad editorial)
```

---

## 3. Modelo de datos fundacional

Diseño objetivo (nombres y forma; los tipos exactos se afinan en preflight). Todo en `apps/content`.

### Capa 1 — Grafo de conocimiento

**`KnowledgeNode`** — árbol atómico autorreferente (adjacency list). Es el esqueleto vivo.

| Campo | Tipo | Notas |
|---|---|---|
| `semantic_id` | Char, **unique global** | llave eterna (`MAT.NUM.RACIONALES.FRACCION_CONCEPTO`) |
| `code` | Char | `EE.BB.TT.RR` para mostrar/ordenar (`02.03.01.01`). **Único por asignatura**, no global (Física reusa 01–05) |
| `node_type` | Char | `asignatura` \| `eje` \| `bloque` \| `tema` \| `recurso` (recurso = hoja = unidad aprendible) |
| `parent` | FK self, null | null solo en `asignatura` (la raíz) |
| `subject_abbr` | Char | `MAT/FIS/QUI` — asignatura (denormalizado en todos los nodos) |
| `name` | Char | |
| `slug` | Slug | para URLs limpias |
| `order` | Int | orden entre hermanos |
| `axis_abbr` | Char | `NUM/ALG/GEO/EST/FUND` (denormalizado, filtrado rápido; vacío en asignatura) |
| `competencia` | Char | `M1/M2/U` — solo hojas |
| `dificultad` | Char | `basica/media/avanzada` — solo hojas |
| `cursos` | JSON | `[7B, 8B, 1M]` — solo hojas |
| `is_published` | Bool | |

> **La asignatura es el nivel raíz.** La jerarquía completa es
> `Asignatura > Eje > Bloque > Tema > Recurso`. Hoy solo existe Matemáticas (`MAT`); Física (`FIS`)
> y Química (`QUI`) entran a futuro agregando sus YAML con el prefijo correspondiente en el
> `semantic_id`, sin tocar el modelo. El import sintetiza los nodos `asignatura`/`eje`/`bloque`
> (que no tienen `id` propio en el YAML) con un `semantic_id` determinista y estable.

> **Por qué una sola tabla autorreferente** (y no 5 tablas asignatura/eje/bloque/tema/recurso): las
> operaciones son uniformes (recorrer, breadcrumb, render de árbol), la profundidad puede evolucionar,
> y contenido/prerrequisitos/estado se enganchan igual a cualquier nivel. Es el patrón estándar de
> "skill tree". Migración única, importación trivial desde el YAML.

**`NodePrerequisite`** — aristas del DAG.

| Campo | Tipo | Notas |
|---|---|---|
| `node` | FK KnowledgeNode | el que tiene prerrequisitos |
| `requires` | FK KnowledgeNode | el que se necesita antes |
| `kind` | Char | `requerido` \| `recomendado` |
| `min_mastery` | Float | umbral para darlo por cumplido (default 0.75) |
| | unique(`node`,`requires`) | + validación de aciclicidad |

### Capa 2 — Contenido

**`NodeContent`** — O2O con nodo hoja. La "ficha AlonsoFormula".

| Campo | Tipo | Notas |
|---|---|---|
| `node` | O2O KnowledgeNode | |
| `objetivo` | Text | "Al finalizar serás capaz de…" |
| `explicacion` | Text | Markdown + KaTeX (reusa pipeline existente) |
| `procedimiento` | JSON | pasos ordenados |
| `ejemplos` | JSON | `[{titulo, enunciado, solucion_pasos:[]}]` |
| `errores_frecuentes` | JSON | lista |
| `estado` | Char | `borrador` \| `publicado` (borrador = `noindex`) |
| `fuente` | Text | referencia bibliográfica (auditable) |

**`NodeMedia`** — videos y archivos que apoyan un nodo. Al menos 1 video de explicación por recurso;
videos de ejercicios resueltos se agregan progresivamente.

| Campo | Tipo | Notas |
|---|---|---|
| `node` | FK KnowledgeNode | |
| `kind` | Char | `video_youtube` \| `file` \| `external` |
| `video_kind` | Char | `explicacion` \| `ejercicios_resueltos` \| `complementario` — solo si `kind=video_*` |
| `url` / `file` | | |
| `order` | Int | |

> Un nodo puede tener varios videos (explicación + ejercicios resueltos + complementarios).
> Los videos de ejercicios resueltos se agregan a cuentagotas, no son obligatorios desde el inicio.

### Capa 3 — Banco de ejercicios

**`BookExercise`** — ejercicios extraídos de libros (Moraleja, Santillana, Baldor, Carreño), para
referencia y práctica libre. Las respuestas son **siempre visibles** — no se evalúa formalmente.

| Campo | Tipo | Notas |
|---|---|---|
| `node` | FK KnowledgeNode | hoja |
| `exercise_type` | Char | tipo dentro del nodo (`suma_enteros`, `resta_enteros`…) |
| `enunciado` | Text | enunciado del ejercicio |
| `solucion` | Text | desarrollo paso a paso |
| `respuesta` | Char | resultado final |
| `fuente` | Char | `moraleja` \| `santillana` \| `baldor` \| `carreño` |
| `dificultad` | Char | `basica` \| `media` \| `avanzada` |
| `order` | Int | orden sugerido de práctica |
| `estado` | Char | `borrador` \| `publicado` |

> El banco no genera puntaje ni registro. Es material de referencia: el alumno lo usa para
> ejercitarse a su ritmo viendo las respuestas. La cantidad es el objetivo — muchos ejercicios
> mecánicos por tipo.

### Capa 4 — Evaluación (formal)

**`AssessmentExercise`** — ejercicios de evaluación formal. **Respuesta oculta hasta enviar.**
Distintos de los del banco — el alumno no los ha visto al practicar.

| Campo | Tipo | Notas |
|---|---|---|
| `node` | FK KnowledgeNode | hoja |
| `exercise_type` | Char | tipo dentro del nodo (mismo vocabulario que `BookExercise`) |
| `format` | Char | `alternativa` \| `numerica` \| `algebraica` |
| `enunciado`, `solucion`, `respuesta_canonica`, `tolerancia`, `choices…` | | |
| `dificultad` | Char | |
| `estado` | Char | `borrador` \| `publicado` |

**`NodeAssessmentRule`** — define "dominio" como DATO, por nodo.

| Campo | Tipo | Notas |
|---|---|---|
| `node` | O2O KnowledgeNode | hoja |
| `min_score` | Float | default 0.75 |
| `require_type_coverage` | Bool | default True → debe cubrir los tipos principales |
| `num_questions` | Int | |
| `attempt_policy` | JSON | reintentos, enfriamiento, etc. |

**`AssessmentAttempt`** — historial de evaluaciones formales (auditoría + analítica).

| Campo | Tipo | Notas |
|---|---|---|
| `user`, `node` | FK | |
| `score` | Float | porcentaje de acierto |
| `passed` | Bool | |
| `failed_exercise_types` | JSON | tipos de ejercicio que falló → retroalimentación |
| `attempt_number` | Int | |
| `created_at` | DateTime | |

> **Definición operativa de dominio**: un nodo está **dominado** cuando el alumno resuelve
> ejercicios *de evaluación* (no vistos en el banco), sin ayuda, con `score ≥ min_score` **y**
> cubriendo los `exercise_type` principales. `failed_exercise_types` le dice exactamente qué repasar.

### Capa 5 — Estado del alumno (solo rendimiento real)

**`StudentNodeState`** — estado por alumno y nodo, basado **exclusivamente en resultados de evaluación**.
Sin registro de "vio" ni "practicó" — eso no mide aprendizaje.

| Campo | Tipo | Notas |
|---|---|---|
| `user`, `node` | FK | unique together |
| `status` | Char | `no_iniciado` \| `en_progreso` \| `dominado` |
| `mastery_score` | Float | mejor score alcanzado en evaluación formal |
| `passed` | Bool | aprobó según `NodeAssessmentRule` |
| `failed_exercise_types` | JSON | tipos que falló en el último intento → "repasa esto" |
| `attempts` | Int | número de evaluaciones formales realizadas |
| `last_attempt_at` | DateTime | |

---

## 4. El contrato de desacople (lo que hace posible el juego "a futuro")

El núcleo emite **eventos de dominio**; nada del núcleo importa la gamificación.

```
Dominio emite:                    Suscriptores (capa 6, opcionales):
  node.mastered           ──────▶   gamificación → +XP, insignia, desbloqueo
  zone.challenge_passed   ──────▶   gamificación → insignia de zona
```

> `node.content_viewed` y `node.practiced` se eliminan — no son señales significativas de aprendizaje.
> El único evento que vale es `node.mastered` (aprobó la evaluación formal).

- El **sitio de consulta** lee contenido + grafo + (si hay login) estado de evaluación.
- El **mapa gamificado** (futuro) lee `StudentNodeState` + DAG para pintar nodos, rutas y desbloqueos.
- La **mecánica de juego** (futuro) se _suscribe_ a los eventos y mantiene XP/insignias/rachas.

→ Se puede construir, cambiar o quitar la gamificación **sin tocar las capas 1–5**. Ese es el sentido
de "base sólida que escala al juego".

> Implementación concreta: señales de Django (`django.dispatch`) desde `mastery_service`. El
> `gamification_service` existente se conecta aquí como suscriptor — se reubica en capa 6, no se
> reescribe.

---

## 5. Identidad y pipeline de contenido

Todo se ancla en `semantic_id` y todo es idempotente (re-ejecutable sin duplicar).

```
docs/conocimiento/*.yaml (taxonomía)
   └─ comando import_knowledge_tree  →  KnowledgeNode + NodePrerequisite
docs/conocimiento/contenido/*.yaml (contenido pedagógico, generado en NotebookLM + revisado)
   └─ comando load_node_content      →  NodeContent  (upsert por semantic_id)
docs/conocimiento/dag/*.yaml (o inline en taxonomía)
   └─ comando load_prerequisites     →  NodePrerequisite  (valida ciclos antes de guardar)
ejercicios (generación IA existente, ahora etiquetada por node + exercise_type + purpose)
   └─ adapta generate_pending_questions / generate_ai_questions
```

Reglas del pipeline:
- **Upsert por `semantic_id`**, nunca por posición ni por nombre.
- **Idempotente**: correrlo dos veces no duplica ni rompe.
- **Borrador por defecto**: contenido sin revisar entra como `borrador` (`noindex`).
- **Aciclicidad transaccional**: `load_prerequisites` aborta entero si detecta un ciclo.

---

## 6. Las dos presentaciones

### (A) Sitio de consulta — se construye ahora

- Público, indexable, **no requiere cuenta** para leer.
- URL limpia y jerárquica: `/aprender/<eje>/<bloque>/<tema>/<recurso>/`.
- Render del nodo: objetivo → explicación → procedimiento → ejemplos → **practica** (ejercicios por
  tipo) → errores frecuentes → video(s) `NodeMedia` → "antes de empezar" (prerrequisitos) →
  "siguiente recomendado".
- Con login: guarda `StudentNodeState` (estrellas, dominio). Sin login: solo lectura/práctica libre.
- SEO real: cada nodo atómico es una URL — cientos de páginas long-tail ("cómo sumar fracciones con
  distinto denominador").

### (B) Mapa gamificado — futuro (tarjeta aparte)

- Requiere login. Lee `StudentNodeState` + `NodePrerequisite`.
- Pinta el grafo: dominado / disponible / recomendado-después / nivelación-previa.
- Desbloqueo **blando** (nunca candado duro): "te faltan estas llaves" + ruta puente + "demostrar
  dominio con diagnóstico".
- Reutiliza `XPEvent`/`UserSkill`/`UserStreak` (ya existen) como proyección de eventos de dominio.

> Ambas presentaciones son **lectores** del mismo núcleo. No duplican contenido ni lógica.

---

## 7. Qué se conserva y qué se parte de cero

| Activo actual | Decisión |
|---|---|
| 27 videos `Resource` | Se reformulan desde cero — los recursos existentes no se heredan |
| `Question`/`Choice` | Reutilizable como base de `AssessmentExercise` (etiquetado por `node`+`exercise_type`) |
| `QuizAttempt`/`TopicEvaluationAttempt` | Base de `AssessmentAttempt` (historial de evaluación formal) |
| `progress_service` / `structured_progress_service` | Reaprovechable como base del cálculo de `StudentNodeState` |
| `gamification_service` + `XPEvent`/`UserSkill`/`UserStreak` | Suscriptores de eventos (capa 6, futuro) — no se tocan por ahora |
| Generación IA de preguntas | Sigue igual, ahora etiqueta ejercicios por `node`+`exercise_type` |
| `Area/Subject/Topic/Resource` | Conviven durante la transición; a futuro, páginas viejas redirigen a `/aprender/…` |

---

## 8. Decisión abierta principal (a ratificar por 🧑 + preflight)

**D1 — ✅ DECIDIDO (🧑, 2026-06-26): Grafo nuevo conviviendo, luego reemplazo.**

Se crea `KnowledgeNode` y las capas nuevas en paralelo. El sitio viejo (videos bajo `Topic`) sigue
vivo mientras se puebla el árbol; cuando un eje está completo y validado, sus URLs viejas **redirigen**
a `/aprender/…` (ya existe el patrón `legacy_redirects`). Razón: menos riesgo, valor incremental y no
rompe el SEO existente. La reescritura limpia se descartó como primer paso (más riesgo, sitio en obra).

**D2 — ¿Los ejercicios reusan `Question` extendido o se crea `Exercise` nuevo?**
Recomendado: **extender `Question`** con FK `knowledge_node` + `exercise_type` + `purpose` (aditivo,
sin romper el banco actual) en vez de una tabla nueva. Menos migración, reusa todo el flujo de
generación/corrección existente. El nombre "`Exercise`" en este doc es conceptual.

---

## 9. Orden de construcción sugerido (alto nivel)

No es el detalle de tarjetas (eso se hace al aprobar la arquitectura). Es la **secuencia basal**:

1. **Esqueleto** — `KnowledgeNode` + `import_knowledge_tree` (los 700 nodos viven en DB). Vista admin
   de árbol para verificar. _Nada público aún._
2. **Contenido** — `NodeContent` + `load_node_content` + formato YAML de contenido. Poblar **1 bloque
   piloto** (recomendado el bloque de **números enteros**).
3. **Páginas de consulta** — URLs `/aprender/…`, template, navegación, KaTeX, SEO, mobile. Solo
   lectura. _Gate del 🧑: validar el piloto en producción._
4. **Videos** — `NodeMedia` (video propio para el bloque piloto; los recursos actuales se parten
   de cero, no se heredan).
5. **Banco de ejercicios** — `BookExercise` + `load_book_exercises`. Poblar el piloto con ejercicios
   de libros, respuestas visibles, por tipo.
6. **Evaluación formal** — `AssessmentExercise` + `NodeAssessmentRule` + `AssessmentAttempt`.
7. **Estado del alumno** — `StudentNodeState` (solo rendimiento real: `passed`, `failed_exercise_types`).
   Emisión de `node.mastered`.
8. **Prerrequisitos** — `NodePrerequisite` + validación DAG + "antes de empezar" en la página.
9. **Escalado** — poblar el resto de bloques; redirigir o reemplazar páginas viejas.
10. **(Futuro, tarjeta aparte)** — Mapa gamificado + mecánica de juego, suscrita a los eventos.

Cada paso es pequeño, desplegable y con barrera verde (`test` · `check --deploy` · `makemigrations`).

---

## 10. Por qué esta base escala (resumen)

- **Un solo esqueleto** (`KnowledgeNode`) → no hay dos verdades.
- **Todo cuelga del nodo** → contenido, videos, ejercicios, dominio y progreso son intercambiables y
  ampliables sin tocar el resto.
- **Dominio desacoplado de presentación vía eventos** → el sitio de consulta hoy y el mapa gamificado
  mañana son dos lectores; el juego entra sin reescribir el núcleo.
- **Identidad estable + pipeline idempotente** → poblar 700 nodos a cuentagotas, sin miedo a romper.
- **Reglas y contenido como datos** → afinar "qué es dominio" o editar una explicación no es un deploy
  de código.

---

## Qué se hizo

_(Este documento es diseño. Al aprobarse, se derivan las tarjetas de construcción por paso.)_
