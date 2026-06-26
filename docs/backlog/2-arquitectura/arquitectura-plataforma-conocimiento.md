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

Cinco capas. Las capas 1–4 son el **núcleo de dominio** (estable, compartido). La capa 5 son las
**presentaciones** (dos hoy/mañana, intercambiables).

```
┌─────────────────────────────────────────────────────────────────────┐
│  CAPA 5 — PRESENTACIÓN  (proyecciones; leen el núcleo, no lo definen) │
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
│  CAPA 4 — ESTADO DEL ALUMNO   StudentNodeState · AttemptHistory        │
│           (overlay personalizado sobre el grafo)                      │
│                                                                       │
│  CAPA 3 — EVALUACIÓN          Exercise (banco por nodo+tipo)           │
│           (mide dominio)      AssessmentRule (define "dominio")        │
│                                                                       │
│  CAPA 2 — CONTENIDO           NodeContent (explicación/ejemplos)       │
│           (qué enseña)        NodeMedia (videos/archivos/enlaces)      │
│                                                                       │
│  CAPA 1 — GRAFO DE CONOCIMIENTO   KnowledgeNode (árbol atómico)        │
│           (el esqueleto)          NodePrerequisite (aristas DAG)       │
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
| `semantic_id` | Char, **unique** | llave eterna (`MAT.NUM.RACIONALES.FRACCION_CONCEPTO`) |
| `code` | Char, unique | `EE.BB.TT.RR` para mostrar/ordenar (`02.03.01.01`) |
| `node_type` | Char | `eje` \| `bloque` \| `tema` \| `recurso` (recurso = hoja = unidad aprendible) |
| `parent` | FK self, null | null solo en `eje` |
| `name` | Char | |
| `slug` | Slug | para URLs limpias |
| `order` | Int | orden entre hermanos |
| `axis_abbr` | Char | `NUM/ALG/GEO/EST/FUND` (denormalizado, filtrado rápido) |
| `competencia` | Char | `M1/M2/U` — solo hojas |
| `dificultad` | Char | `basica/media/avanzada` — solo hojas |
| `cursos` | JSON | `[7B, 8B, 1M]` — solo hojas |
| `is_published` | Bool | |

> **Por qué una sola tabla autorreferente** (y no 4 tablas eje/bloque/tema/recurso): las operaciones
> son uniformes (recorrer, breadcrumb, render de árbol), la profundidad puede evolucionar, y
> contenido/prerrequisitos/estado se enganchan igual a cualquier nivel. Es el patrón estándar de
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

**`NodeMedia`** — videos/archivos/enlaces que apoyan un nodo. **Aquí entran los 27 videos actuales.**

| Campo | Tipo | Notas |
|---|---|---|
| `node` | FK KnowledgeNode | |
| `kind` | Char | `video_youtube` \| `file` \| `external` |
| `url` / `file` | | |
| `relation` | Char | `principal` \| `complementario` |
| `order` | Int | |

> Un video puede servir a varios nodos (los videos actuales cubren varias ideas atómicas) y un nodo
> puede tener varios medios. Por eso es relación N–N, no un campo en `Resource`.

### Capa 3 — Evaluación

**`Exercise`** — banco de ejercicios, etiquetado por **nodo + tipo**. (Adapta el `Question` actual.)

| Campo | Tipo | Notas |
|---|---|---|
| `node` | FK KnowledgeNode | hoja |
| `exercise_type` | Char | "tipo" dentro del nodo (`denominadores_pequenos`, `tipo_paes`…) |
| `format` | Char | `alternativa` \| `numerica` \| `algebraica` |
| `enunciado`, `solucion`, `respuesta_canonica`, `tolerancia`, `choices…` | | |
| `dificultad` | Char | |
| `purpose` | Char | `practica` \| `evaluacion` (pools separados: la evaluación usa ítems no vistos) |
| `estado` | Char | `borrador` \| `publicado` |

**`NodeAssessmentRule`** — define "dominio" como DATO, por nodo (principio #4).

| Campo | Tipo | Notas |
|---|---|---|
| `node` | O2O/FK KnowledgeNode | puede aplicar a hoja (dominio) o a tema/bloque (desafío de zona) |
| `min_score` | Float | default 0.75 |
| `require_type_coverage` | Bool | default True → debe cubrir los tipos principales |
| `num_questions` | Int | |
| `attempt_policy` | JSON | reintentos, enfriamiento, etc. |

> **Definición operativa de dominio** (la del 🧑): un nodo está **dominado** cuando el alumno resuelve
> ejercicios *nuevos* (pool `evaluacion`), sin ayuda, con `score ≥ min_score` **y** cubriendo los
> `exercise_type` principales del nodo. Esto es exactamente `NodeAssessmentRule` evaluado contra un
> intento.

### Capa 4 — Estado del alumno (overlay)

**`StudentNodeState`** — dominio por alumno y nodo. El substrato de personalización de **ambas**
presentaciones.

| Campo | Tipo | Notas |
|---|---|---|
| `user`, `node` | FK | unique together |
| `status` | Char | `no_iniciado` \| `en_progreso` \| `dominado` |
| `star_content` | Bool | leyó la explicación/ejemplos |
| `star_practice` | Bool | practicó cubriendo tipos |
| `star_mastery` | Bool | aprobó la evaluación de dominio |
| `mastery_score` | Float | último score |
| `types_covered` | JSON | tipos de ejercicio ya resueltos |
| `attempts` | Int | |
| `last_attempt_at` | DateTime | |

**`AssessmentAttempt`** — historial de evaluaciones (auditoría + analítica). Adapta `QuizAttempt`.

---

## 4. El contrato de desacople (lo que hace posible el juego "a futuro")

El núcleo emite **eventos de dominio**; nada del núcleo importa la gamificación.

```
Dominio emite:                    Suscriptores (capa 5, opcionales):
  node.content_viewed     ──────▶   gamificación → +XP, marca estrella
  node.practiced          ──────▶   gamificación → +XP, racha
  node.mastered           ──────▶   gamificación → +XP, insignia, desbloqueo
  zone.challenge_passed   ──────▶   gamificación → insignia de zona
```

- El **sitio de consulta** lee contenido + grafo + (si hay login) estado.
- El **mapa gamificado** (futuro) lee estado + DAG para pintar nodos, rutas y desbloqueos.
- La **mecánica de juego** (futuro) se _suscribe_ a los eventos y mantiene XP/insignias/rachas.

→ Se puede construir, cambiar o quitar la gamificación **sin tocar las capas 1–4**. Ese es el sentido
de "base sólida que escala al juego".

> Implementación concreta del bus de eventos: señales de Django (`django.dispatch`) o llamadas
> explícitas desde un `mastery_service`. El `gamification_service` actual ya existe y se conecta aquí
> como suscriptor — no se reescribe, se reubica conceptualmente en la capa 5.

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

## 7. Cómo encajan los activos existentes (sin desperdiciarlos)

| Activo actual | Rol en la nueva arquitectura |
|---|---|
| 27 videos `Resource` | `NodeMedia(kind=video_youtube)` enganchados a los nodos que enseñan |
| `Question`/`Choice` | se convierten/adaptan en `Exercise` (etiquetados por `node`+`exercise_type`+`purpose`) |
| `QuizAttempt`/`TopicEvaluationAttempt` | `AssessmentAttempt` (historial de dominio y desafíos de zona) |
| `progress_service` / `structured_progress_service` | base del cálculo de `StudentNodeState` |
| `gamification_service` + `XPEvent`/`UserSkill`/`UserStreak` | suscriptores de eventos (capa 5, futuro) |
| generación IA de preguntas | sigue igual, ahora produce `Exercise` por nodo |
| `Area/Subject/Topic/Resource` | conviven durante la transición; a futuro, las páginas viejas redirigen a `/aprender/…` (ya hay patrón `legacy_redirects`) |

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
   piloto** (recomendado `02.03 Racionales/Fracciones`).
3. **Páginas de consulta** — URLs `/aprender/…`, template, navegación, KaTeX, SEO, mobile. Solo
   lectura. _Gate del 🧑: validar el piloto en producción._
4. **Puente con activos** — `NodeMedia` (engancha los 27 videos) + etiquetado de `Question` por nodo.
5. **Estado del alumno** — `StudentNodeState` + estrellas 1 y 2 (contenido visto, práctica).
6. **Motor de dominio** — `NodeAssessmentRule` + evaluación (estrella 3) + emisión de eventos.
7. **Prerrequisitos** — `NodePrerequisite` + validación DAG + "antes de empezar" en la página.
8. **Escalado** — poblar el resto de bloques; redirigir páginas viejas.
9. **(Futuro, tarjeta aparte)** — Mapa gamificado + mecánica de juego, suscrita a los eventos.

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
