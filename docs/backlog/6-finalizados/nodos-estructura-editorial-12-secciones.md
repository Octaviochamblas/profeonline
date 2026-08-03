# Nodos de conocimiento — nueva estructura editorial de 12 secciones

- **Estado:** CERRADO 🟢 — construido por 🏛️ Claude directamente (2026-08-03), rama `feat/nodos-estructura-12-secciones`
- **Creado:** 2026-08-03
- **Prioridad:** P1 · **Cartera:** contenido · calidad pedagógica
- **Tipo:** infraestructura (modelo + plantilla) — la reescritura masiva de contenido es un proyecto aparte, ver "No-objetivos"
- **Dueño:** 🏛️ Claude (diseño + construcción, a pedido explícito del 🧑 de saltar el pipeline multiagente para esta fase)
- **Requiere:** nada — `NodeContent` y `node_detail.html` ya existen y son estables

## Objetivo

Adaptar la estructura editorial de `NodeContent` (contenido pedagógico de un nodo hoja del árbol de
conocimiento, `/aprender/...`) para que se alinee con la estructura canónica ya usada en las guías de
`Resource` (`docs/reportes-sesion/2026-08-01.md`, `apps/content/services/editorial_guide_service.py`),
agregando además dos "Comprueba tu avance" intermedios (mismo patrón que
`reading_checkpoint_service.py`).

## Fuentes a leer

- `apps/content/models/knowledge.py` — `NodeContent` (líneas 167-224), estructura actual
- `templates/learn/node_detail.html` — orden de render actual, incluida la sección
  "Ejemplos Verdadero/Falso" que hoy se deriva de `errores_frecuentes` (líneas 434-460)
- `apps/content/services/reading_checkpoint_service.py` — esquema y validación de checkpoints en
  `Resource` (`CHECKPOINT_PLACEMENTS`, `normalize_reading_checkpoints`), patrón a replicar para nodos
- `apps/content/services/editorial_guide_service.py` — precedente de validación de estructura de guía
  por secciones (no se reutiliza directo porque `NodeContent` usa campos separados, no un solo markdown)
- `apps/content/models/node_bank.py` — `ItemGroup`/`NodeExercise` (banco de práctica), **no se toca**
- `apps/content/models/knowledge.py` — `NodeAssessmentQuestion` y relacionados (evaluación de dominio),
  **no se toca**, solo se reordena su posición en la plantilla

## Propuesta

### 1. Estructura final (orden de renderizado en `node_detail.html`)

1. Resumen inicial
2. Explicación en palabras simples
3. Explicación formal
4. **Comprueba tu avance** (`checkpoints[placement=after_explicacion_formal]`)
5. Definiciones clave
6. Propiedades y relaciones importantes
7. Ejemplo guiado
8. **Comprueba tu avance** (`checkpoints[placement=after_ejemplo_guiado]`)
9. Procedimiento
10. Errores frecuentes y cómo corregirlos
11. Ejemplos — **sin cambios**
12. Ejemplos Verdadero/Falso — **sin cambios** (sigue derivando de `errores_frecuentes`)
13. Al terminar debes poder
14. Evaluación de dominio — **sin cambios de datos**, solo se reubica en el flujo si hace falta

### 2. Cambios de esquema en `NodeContent` (migración aditiva)

| Campo nuevo | Tipo | Origen / notas |
|---|---|---|
| `resumen_inicial` | `TextField(blank=True)` | Fusiona `objetivo` + `introduccion` + `resumen` (los tres se eliminan tras migrar sus datos) |
| `explicacion_simple` | `TextField(blank=True)` | Mitad de la actual `explicacion` |
| `explicacion_formal` | `TextField(blank=True)` | Otra mitad de la actual `explicacion` |
| `definiciones_clave` | `TextField(blank=True)` (markdown) | Nuevo |
| `propiedades_relaciones` | `TextField(blank=True)` (markdown) | Nuevo |
| `ejemplo_guiado` | `JSONField(default=dict, blank=True)` | Nuevo — forma `{"enunciado": str, "pasos": [str, ...]}` |
| `errores_correccion` | `TextField(blank=True)` (markdown) | Nuevo — texto "error + cómo corregirlo"; **no reemplaza** `errores_frecuentes` |
| `al_terminar_debes_poder` | `TextField(blank=True)` | Nuevo |
| `checkpoints` | `JSONField(default=list, blank=True)` | Nuevo — lista de 2 objetos, mismo esquema que `reading_checkpoint_service.CHECKPOINT_PLACEMENTS` pero con `placement` en `("after_explicacion_formal", "after_ejemplo_guiado")` |

**Campos que quedan intactos** (esquema y contenido, no se tocan): `procedimiento`, `ejemplos`,
`errores_frecuentes`, `estado`, `fuente`, `node`, `created_at`, `updated_at`, `published_at`.

**Campos que se eliminan** (tras backfill de datos a `resumen_inicial` y split a
`explicacion_simple`/`explicacion_formal`): `objetivo`, `introduccion`, `resumen`, `explicacion`.

Migración en dos pasos (Django estándar para evitar pérdida de datos):
1. Migración aditiva: agrega los campos nuevos, deja los viejos.
2. Script de backfill (uno por uno, no automático con IA — cada nodo publicado ya tiene contenido
   humano curado): copia `objetivo`+`introduccion`+`resumen` → `resumen_inicial` (concatenado o el que
   el redactor decida al reescribir) y `explicacion` → `explicacion_simple`/`explicacion_formal` según
   corresponda. Recién cuando el backfill esté verificado, migración que elimina los campos viejos.

### 3. Servicio de checkpoints para nodos

Nuevo módulo `apps/content/services/node_checkpoint_service.py`, análogo a
`reading_checkpoint_service.py` pero con:
- `CHECKPOINT_PLACEMENTS = ("after_explicacion_formal", "after_ejemplo_guiado")` (2, no 3)
- misma validación de forma (pregunta + 4 alternativas + 1 correcta + explicación que menciona la
  respuesta correcta), reutilizando la lógica de `normalize_reading_checkpoints` si es sencillo
  parametrizar el número de placements, o duplicando la función con el set reducido si acoplarla
  complica el código de `Resource` (decisión de implementación, no bloquea el handoff).

### 4. Plantilla `node_detail.html`

Reordenar los `{% if content.xxx %}` según la lista de la sección 1, insertando el bloque de
checkpoint (nuevo partial reutilizable, ej. `learn/includes/_checkpoint.html`) en los dos puntos
indicados. El checkpoint se comporta igual que un ejercicio interactivo existente (botones,
`data-format="multiple_choice"`), reutilizando el CSS/JS ya presente en la página (`.ex-choice`,
`.learn-exercise__feedback`) — no requiere JS nuevo.

## No-objetivos

- **No incluye la reescritura de contenido de los ~2200 nodos ya publicados.** Este handoff cubre
  solo el cambio de esquema + plantilla. La campaña de contenido (qué se regenera con qué criterio,
  en qué orden, con qué gate de historial de alumnos) es un **proyecto de contenido aparte**, a
  planificar cuando este handoff esté construido y verificado en al menos un nodo piloto.
- No se toca `ejemplos` ni `errores_frecuentes` (fuente del V/F) — ni esquema ni contenido.
- No se toca `NodeAssessmentQuestion`/`ItemGroup`/`NodeExercise` (evaluación de dominio y banco de
  práctica) — se mantienen como modelos separados, solo se ubican en el nuevo orden de la página.
- No se automatiza el backfill con IA — es dato editorial curado, requiere reescritura humana/dirigida
  por sesión, igual que el resto del contenido del sitio.

## Criterios de aceptación

- [ ] Barrera verde: `python manage.py test`, `check --deploy`, `makemigrations --check --dry-run`
- [ ] Migración aditiva aplica sin downtime sobre los ~2200 `NodeContent` existentes (campos nuevos
      quedan vacíos, la página no se rompe con secciones vacías — mismo patrón `{% if content.xxx %}`
      que ya usa la plantilla)
- [ ] Nodo piloto reescrito manualmente con las 12 secciones + 2 checkpoints se ve correcto en
      `/aprender/.../<recurso>/` en el orden definido
- [ ] `node_checkpoint_service` valida: exactamente 2 checkpoints, placements únicos y del set
      permitido, 4 alternativas con 1 correcta, explicación menciona la alternativa correcta
      (mismas reglas que `reading_checkpoint_service`, adaptadas)
- [ ] Nodos sin datos en los campos nuevos (todo el catálogo antes del backfill) siguen mostrando
      igual que hoy sin errores ni secciones rotas
- [ ] Tests de regresión para: fusión de `objetivo`/`introduccion`/`resumen` en el backfill (script
      probado con al menos un caso real), validación de checkpoints (casos válidos e inválidos)

## Plan de pruebas

- Unit: `NodeContent` con los campos nuevos vacíos vs. completos — la plantilla no rompe en ningún caso
- Unit: `node_checkpoint_service` — checkpoint válido, placement repetido, placement fuera del set,
  alternativas incorrectas en cantidad, sin alternativa correcta, explicación que no menciona la
  respuesta correcta
- Integration: página de un nodo piloto con las 12 secciones completas, click en cada checkpoint,
  verificación de feedback correcto/incorrecto (reutiliza el JS existente de `.learn-exercise`)
- Script de backfill: probarlo primero en modo dry-run contra 3-5 nodos reales antes de correrlo
  sobre el catálogo completo

## Riesgos / rollback

- Migración de eliminación de campos viejos (`objetivo`, `introduccion`, `resumen`, `explicacion`) es
  **irreversible sin backup** — correr solo después de verificar el backfill completo, y con dump de
  la tabla `NodeContent` antes de aplicarla.
- Si `node_checkpoint_service` termina duplicando casi todo `reading_checkpoint_service`, evaluar en
  la construcción si conviene parametrizar un único servicio compartido — no es un no-objetivo, es una
  decisión de implementación que puede tomar 🔨 Antigravity con preflight de 🧩 Codex.
- Rollback de esta fase (antes del backfill masivo): revertir la migración aditiva, eliminar
  `node_checkpoint_service.py` y el partial `_checkpoint.html`. No hay riesgo sobre contenido
  publicado porque los campos viejos no se tocan hasta el backfill.

## Qué se hizo

Construido en la rama `feat/nodos-estructura-12-secciones`, siguiendo el plan
`docs/superpowers/plans/2026-08-03-nodos-estructura-12-secciones.md` (TDD, un commit por tarea):

1. **Modelo:** 9 campos nuevos en `NodeContent` (`resumen_inicial`, `explicacion_simple`,
   `explicacion_formal`, `definiciones_clave`, `propiedades_relaciones`, `ejemplo_guiado`,
   `errores_correccion`, `al_terminar_debes_poder`, `checkpoints`) + migración `0050` aditiva.
   `objetivo`/`introduccion`/`resumen`/`explicacion` **no se tocaron** (quedan para cuando se
   verifique el backfill real).
2. **Servicio:** `apps/content/services/node_checkpoint_service.py` — calco de
   `reading_checkpoint_service.py` con 2 placements (`after_explicacion_formal`,
   `after_ejemplo_guiado`) en vez de 3. 7 tests unitarios.
3. **Vista:** `apps/learn/views.py` (`_recurso_view`) calcula `checkpoint_after_formal` /
   `checkpoint_after_ejemplo` y los pasa al contexto.
4. **Plantilla:** `templates/learn/node_detail.html` reordenado a las 12 secciones + 2
   checkpoints, con fallback automático a los campos legacy (`objetivo`/`introduccion`/
   `explicacion`) cuando los nuevos están vacíos — verificado que un nodo real sin backfill
   (`Identificación de los Números Naturales (N)`) se ve exactamente igual que antes. Partial
   nuevo `templates/learn/includes/_node_checkpoint.html`, reutiliza el CSS/JS de ejercicios
   existente (sin JS nuevo).
5. **Verificación manual:** nodo QA temporal (5 niveles, creado y borrado en la BD local) con
   las 12 secciones + 2 checkpoints llenos — orden correcto, ambos checkpoints responden con
   feedback correcto/incorrecto igual que los ejercicios existentes.
6. **Barrera completa:** `python manage.py test` → **696 OK (1 skip)**, `check --deploy` → 0
   errores (solo warnings esperables de `settings.local`), `makemigrations --check --dry-run` →
   sin cambios pendientes.

**Pendiente explícito (no objetivo de esta fase):** reescribir el contenido de los ~2200 nodos
existentes con las 12 secciones reales, empezando por el bloque `enteros` (`MAT.NUM` `02.01`,
36 recursos: `ENTEROS_CONJUNTO` 15 + `ENTEROS_OPERATORIA` 21) — proyecto de contenido aparte.
