# Auditoría de arquitectura — ProfeOnline como plataforma de aprendizaje

- **Fecha:** 2026-07-24 · **Redactado por:** 🏛️ Claude
- **Tipo:** auditoría de arquitectura (rol: arquitecto de plataformas educativas)
- **Origen:** el 🧑 trajo un marco de 10 puntos + "regla cero" trabajado con ChatGPT
  (arquitectura del conocimiento, diseño de recursos, modelo pedagógico, modelo de evaluación,
  modelo de habilidades, diseño de ejercicios, modelo del estudiante, motor de recomendaciones,
  arquitectura técnica, escalabilidad) y pidió auditar la plataforma real contra ese marco.
- **Método:** lectura directa de modelos/servicios/vistas/URLs en `apps/`, más un grafo de
  imports generado con `graphify` (`apps/`, `templates/`, `config/`, `docs/` sin
  `docs/conocimiento/`) usado para **verificar con evidencia estructural** —no solo lectura—
  si dos subsistemas están realmente acoplados.

## Regla cero (marco de referencia)

> Cada decisión de diseño debe ayudar a responder: **qué sabe el estudiante, cómo lo sabemos
> (evidencia), qué le falta por aprender, y cuál es el siguiente recurso que más aumenta su
> aprendizaje.** Si una funcionalidad no mejora ninguna de esas cuatro, probablemente no aporta
> al núcleo y puede dejarse para después.

**Veredicto:** hoy la plataforma responde aproximadamente **0.5 de 4** preguntas. El esfuerzo
(~40.000 preguntas, 1.911 recursos) está concentrado en la capa que menos diferencia a un tutor
inteligente (contenido), mientras la infraestructura de tutoría (evidencia, estado del alumno,
recomendación) es casi inexistente.

## Punto por punto

| # | Punto | Nota | Hallazgo clave |
|---|---|---|---|
| 1 | Arquitectura del conocimiento | 6/10 | `KnowledgeNode` (una tabla autorreferente, `semantic_id` estable) es la decisión más acertada. Pero el DAG de prerrequisitos tiene **13 aristas para 1.911 nodos** (`docs/conocimiento/dag/`) — es un árbol taxonómico, no un grafo de conocimiento real. `min_mastery` no lo lee ningún código. |
| 2 | Diseño de recursos | 8/10 | El mejor punto: `NodeContent` es genuinamente atómico (objetivo/explicación/procedimiento/ejemplos/errores), 5-10 min, evaluación de 3 niveles al final. |
| 3 | Modelo pedagógico | 7/10 | Progresión bien pensada dentro del recurso (`ItemGroup`: comprender→reconocer→resolver→variar→aplicar→evaluar). Pero es **intra-recurso**; sin DAG poblado no hay secuencia real entre recursos. |
| 4 | Modelo de evaluación | 4/10 ⚠️ | Umbral/intentos/nº preguntas hardcodeados (`node_assessment_service.py`: `PASS_THRESHOLD=0.8`, `MAX_EVAL_ATTEMPTS=3`) en vez de datos por nodo. **Grave:** una vez aprobado el nivel, `submit_assessment` lanza `ValueError` y no permite reevaluarse nunca — imposible medir retención por diseño. La práctica (`NodeExercise`) no genera ningún registro de intento. |
| 5 | Modelo de habilidades | 2/10 | `UserSkill` es una fila por `Topic` (sistema legacy) con nombre libre. No es transversal, no observable, no conectado al grafo de conocimiento. |
| 6 | Diseño de ejercicios | 6/10 | `NodeExercise` bien modelado (6 formatos, dificultad, competencia M1/M2/U). Sin objetivo principal declarado por ejercicio; `kind=template`+`pattern` (generadores) sin runtime que lo use; `required_for_mastery` no lo lee nadie. |
| 7 | Modelo del estudiante | 1/10 ⚠️ | **No existe.** `StudentNodeState` fue diseñado en el handoff de arquitectura de junio y nunca se construyó. Las estrellas se recalculan al vuelo en cada carga de página. No hay página de progreso para el alumno. |
| 8 | Motor de recomendaciones | 0/10 | No existe ninguna línea de código. `_build_prerequisites()` en `apps/learn/views.py` lo dice explícito: "sin estado por alumno todavía, solo informativo, nunca bloquea". |
| 9 | Arquitectura técnica | 3/10 ⚠️ | **Dos plataformas completas en paralelo.** Ver sección siguiente — confirmado con el grafo de imports: 0 aristas de negocio compartidas entre el sistema legacy y `KnowledgeNode`. |
| 10 | Escalabilidad | 6/10 | Técnicamente escala (pipeline YAML→DB idempotente, `semantic_id` multi-asignatura). El cuello real es editorial: 21 preguntas manuales por nodo, formato horneado en código no parametrizable por disciplina. |

## Hallazgo confirmado con el grafo de imports (graphify, 2026-07-24)

Se generó un grafo de conocimiento del código (`apps/`, `templates/`, `config/`, `docs/` sin
`conocimiento/`) con `graphify`: 3.488 nodos, 6.317 aristas, 336 comunidades.

- **`KnowledgeNode`** (Sistema B): 38 aristas directas, ninguna toca `Resource`, `Question`,
  `Topic`, `QuizAttempt` ni `evaluation_service.py`.
- **`Resource`/`Question`/`Topic`** (Sistema A): 37+22+19 aristas, ninguna toca `apps/learn/`,
  `NodeExercise`, `ItemGroup` ni `node_assessment_service.py`.
- **Camino más corto entre `KnowledgeNode` y `Resource` en todo el grafo: longitud 2, pasando por
  `apps/content/models/__init__.py`** — es decir, la única conexión es el archivo que importa
  todos los modelos al mismo namespace de Python. **Cero lógica de negocio compartida.**
- **`gamification_service`/`XPEvent`/`UserStreak`**: únicos vecinos son `models/gamification.py`,
  `services/evaluation_service.py` (Sistema A) y tests. Cero conexión con `apps/learn/` o
  `node_assessment_service.py` — confirma que el motor de XP/skills/rachas nunca se dispara en
  `/aprender/`.
- **La capa de templates sí está parcialmente unificada** (`templates/pages/` y `templates/learn/`
  conviven en el mismo componente conexo vía `base.html`), mientras el dominio (modelos/servicios)
  está totalmente partido en dos. Es lo peor de ambos mundos: un solo sitio visual, dos motores de
  datos sin relación por debajo.
- La decisión D1 de la arquitectura basal de junio ("conviven, luego se reemplaza con redirects")
  nunca se activó: `legacy_redirects.py` existe pero es vecino solo de `Resource`, no de
  `KnowledgeNode` — el puente de salida está construido pero nadie lo usa para migrar tráfico.

## Hoja de ruta priorizada

### 🔴 Corregir (sin esto no hay tutor)
1. Tabla `Evidence` append-only (`user, item, node, skill, correct, context, created_at`) — única
   respuesta real a "cómo lo sabemos".
2. Quitar el bloqueo terminal de `submit_assessment` — permitir reintento con enfriamiento.
3. Poblar el DAG de prerrequisitos (13 → al menos 1 arista por recurso).
4. `NodeState` derivado (`mastery`, `last_seen`, `next_review_at`) recalculable desde `Evidence`.
5. Motor de recomendación v0: una consulta SQL (nodos desbloqueados, mastery bajo, repaso vencido).
6. Página "Mi progreso" / "Repasar hoy" para el alumno.

### 🟡 Simplificar
7. Etiqueta `skill` como columna simple en el ítem (4-6 valores transversales), no una tabla nueva.
8. Umbral/intentos/nº preguntas → campos de datos por nodo, no constantes en código.
9. Un solo modelo de ítem (`NodeExercise` y `NodeAssessmentQuestion` difieren solo en si la
   respuesta se ve — eso es un flag, no dos jerarquías de tablas).

### ⚫ Eliminar
10. Sacar el Sistema A del menú del alumno, redirigir a `/aprender/` (patrón `legacy_redirects` ya
    existe, activarlo).
11. Retirar las taxonomías legacy que el grafo ya subsume (Level, Area, Module).
12. Congelar el épico de guías interactivas (~5.000 LOC, colgando de `Topic`, sin conexión al
    grafo, fase 7 atascada en auditoría desde junio).
13. Borrar la flexibilidad muerta: `required_for_mastery`, `min_mastery`, `kind=template`+`pattern`
    sin runtime.

## Arquitectura propuesta (núcleo de 5 piezas)

```
KnowledgeNode ── NodeEdge (DAG)
      ├── Content
      ├── Item (fusiona NodeExercise + NodeAssessmentQuestion)
      └── Evidence (append-only) ──▶ NodeState (derivado, caché) ──▶ recomendación (1 consulta)
```

`Evidence` es la única verdad; todo lo demás (dominio, retención, recomendación, analítica) es una
*lectura* de esa tabla. Retención = una columna `next_review_at` (duplicar intervalo al acertar,
resetear al fallar) — no hace falta SM-2 ni curvas de olvido. No construir el mapa gamificado ni
motores adaptativos por IA antes de tener `Evidence` con datos reales de alumnos.

**Regla operativa sugerida:** si una tarjeta de backlog no escribe en `Evidence` ni lee de
`NodeState`, no es núcleo. Con ese filtro, de las tarjetas activas en `docs/backlog/` sobrevive
prácticamente solo `kb-f5-estado-alumno`.

## Qué se hizo

_(Documento de auditoría; no implica cambios de código. Al decidir ejecutar la hoja de ruta,
crear tarjetas en `docs/backlog/1-por-iniciar/` para cada punto priorizado.)_
