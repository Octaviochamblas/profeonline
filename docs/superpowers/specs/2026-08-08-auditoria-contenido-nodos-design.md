# Diseño: auditoría universal de contenido de nodos + autoregistro por commit

- **Fecha:** 2026-08-08 · **Redactado por:** 🏛️ Claude (brainstorming con el 🧑)
- **Origen:** el 🧑 está re-actualizando contenido masivamente porque varios recursos no cumplen
  el estándar de 12 secciones de la forma correcta (ver hallazgo de esta misma sesión: contenido
  de `func-exponencial` a medio reescribir, con `ejemplo_guiado` que retrocedió a texto genérico y
  una sección `ejemplos` con relleno sin terminar). Pidió una forma de saber en todo momento, para
  **cualquier** nodo, qué tiene y qué le falta, con registro persistente y que se autoactualice con
  cada cambio — no una auditoría puntual más que se pierda como las anteriores.

## 1. Objetivo

Una única fuente de verdad, ejecutable en cualquier momento, que determina — para **cualquier**
recurso hoja del árbol de `KnowledgeNode` (las 6 ramas: Fundamentos, Números, Álgebra, Geometría,
Probabilidad, Estadística; ~2200 recursos) — si cumple el checklist §5 de
`docs/conocimiento/pauta-contenido.md` completo (contenido pedagógico `NodeContent` + banco de
ejercicios), y deja un registro legible y versionado de lo que falta por recurso. El registro se
actualiza solo cada vez que se commitea contenido, sin paso manual adicional.

## 2. No-objetivos (explícitamente fuera de alcance de este spec)

- **No** implementa nada todavía — este documento es solo el diseño aprobado; la construcción es un
  paso posterior separado (plan de implementación).
- **No** bloquea commits ni pushes. El hook de pre-commit solo avisa por consola y deja el registro
  actualizado; nunca impide guardar contenido a medio terminar.
- **No** se agrega a CI (`.github/workflows/django_ci.yml`) en esta versión — es una herramienta de
  uso manual/local, no una barrera de despliegue. Se puede reconsiderar más adelante si el 🧑 lo pide.
- **No** corrige contenido automáticamente. Es de solo lectura: detecta y registra, nunca escribe ni
  reescribe YAML, ni toca `NodeContent`/`NodeExercise` en la DB.
- **No** reemplaza `load_node_content` ni `load_exercise_bank` — sigue siendo el único camino
  YAML/JSONL → DB.
- **No** agrega dependencias nuevas al proyecto (ver §5, formato CSV en vez de `.xlsx` nativo).

## 3. Hallazgos de contexto que informan el diseño

- El checklist ya existe y está bien definido: **`docs/conocimiento/pauta-contenido.md`, sección
  "5. Checklist antes de cargar un recurso"** — 12 campos de `NodeContent`, reglas de `checkpoints`
  (exactamente 2, 4 alternativas, 1 correcta), `ejemplos` (mínimo 2 tipo A + 2 tipo B),
  `errores_frecuentes` (exactamente 5), `afirmaciones_verdaderas` (mínimo 2), unicidad de
  `ejemplo_guiado.enunciado` dentro del sub-tema, y banco de ejercicios (10 por recurso, 3+1+3+3,
  `correct_answer` calza con `choices`, `stable_id` único en todo el banco).
- Ya existen **varios scripts de auditoría sueltos** en `scratch/` (`audit_all_nodes.py`,
  `audit_antigravity_12secciones.py`, `audit_node_03_strict.py`, `audit_node_04_strict.py`,
  `audit_pipeline_compliance.py`) que implementan fragmentos distintos e inconsistentes del mismo
  checklist, cada uno con un rango de nodos hardcodeado (`02.04`–`03.15`, o un subtema recibido por
  `argv`). `scratch/` está en `.gitignore` → ese trabajo de auditoría se pierde entre sesiones, que es
  exactamente el problema que el 🧑 quiere resolver. Este diseño los consolida en un solo lugar
  versionado, sin duplicar lógica.
- `NodeContent` ya tiene timestamps (`migración 0040`, mencionada en `ESTADO.md`) — no se necesita
  agregar campos nuevos al modelo para saber cuándo cambió un recurso.
- El repo ya usa el framework `pre-commit` (`.pre-commit-config.yaml`, hooks locales `django-check` /
  `django-migrations-check`, `entry: .venv\Scripts\python.exe manage.py <comando>`) — el hook nuevo
  sigue exactamente ese mismo patrón, no introduce un mecanismo distinto. El pre-commit se mantiene
  rápido a propósito (regla del proyecto) → el hook nuevo debe auditar **solo los YAML que cambiaron
  en ese commit**, nunca el árbol completo.
- El framework `pre-commit` soporta nativamente filtrar y pasar solo los archivos que matchean un
  patrón (`files: <regex>`, `pass_filenames: true`) — no hace falta lógica propia en Python para
  detectar qué YAML quedaron en stage.
- No hay `openpyxl` ni ninguna librería de Excel instalada (`requirements.txt`). El módulo `csv` de
  la librería estándar produce un archivo que Excel/Sheets abre igual de bien (filtra, ordena) sin
  agregar una dependencia nueva.
- Convención existente para auditorías versionadas: `docs/auditorias/YYYY-MM-DD-auditoria-*.md` (ya
  hay varias, ej. `2026-08-05-auditoria-contenido-12-secciones.md`) — el reporte Markdown de este
  diseño sigue esa misma convención de nombre y carpeta.

## 4. Arquitectura

**Una sola pieza de lógica, dos formas de invocarla — nada de comandos duplicados:**

1. **`apps/content/services/content_audit_service.py`** (nuevo) — función pura
   `audit_resource_fields(data: dict, siblings: list[dict]) -> list[str]` que implementa el
   checklist §5 completo y devuelve la lista de problemas encontrados (vacío = recurso OK). No
   depende de Django ORM directamente: recibe un `dict` con los valores de campo y la lista de
   recursos hermanos del mismo sub-tema (para el chequeo de `ejemplo_guiado` duplicado). Esto es lo
   que permite reusar la misma lógica tanto leyendo desde la DB como leyendo directo desde YAML en
   disco.
2. **`apps/content/management/commands/audit_node_content.py`** (nuevo) — un solo comando, dos
   modos:
   - **Sin argumentos** → barrida completa: recorre los ~2200 nodos hoja desde la DB
     (`NodeContent` + banco de ejercicios vía `NodeExercise`/`ItemGroup`), arma el `dict` de cada
     uno, llama `audit_resource_fields`, y escribe **ambas** salidas (§6).
   - **Con rutas de archivo como argumentos** (`manage.py audit_node_content <archivo1.yaml> ...`)
     → modo dirigido: parsea esos YAML directo de disco (no requiere que ya estén cargados en la
     DB), agrupa por sub-tema comparando `semantic_id`, corre el mismo checklist solo sobre esos
     recursos, y **actualiza únicamente esas filas** en el reporte Markdown del día (créandolo si no
     existe todavía).
3. **Hook de pre-commit nuevo** en `.pre-commit-config.yaml`, mismo patrón que los hooks locales
   existentes:
   ```yaml
   - id: audit-node-content-changed
     name: Auditoría de contenido (solo YAML modificados)
     entry: .venv\Scripts\python.exe manage.py audit_node_content
     language: system
     files: ^docs/conocimiento/contenido/.*\.ya?ml$
     pass_filenames: true
   ```
   `pre-commit` ya se encarga de pasarle solo los YAML en stage — el comando corre en modo dirigido
   automáticamente cuando recibe rutas. Imprime los problemas encontrados en consola (no bloquea) y
   deja el Markdown de auditoría del día modificado y listo para quedar en el mismo commit.

## 5. Checklist implementado (idéntico al §5 de la pauta, enumerado explícito)

- 12 campos de `NodeContent` completos (no vacíos, largo mínimo razonable, sin marcadores de
  placeholder tipo "lorem ipsum" / "pendiente de redacción" / nombre del recurso pegado en frase
  molde).
- `checkpoints`: exactamente 2 (`after_explicacion_formal`, `after_ejemplo_guiado`), 4 alternativas
  c/u, exactamente 1 `is_correct: true`, `explanation` menciona el texto de la correcta.
- `ejemplos`: mínimo 2 Tipo A (selección múltiple) + 2 Tipo B (Sí/No).
- `errores_frecuentes`: exactamente 5. `afirmaciones_verdaderas`: mínimo 2.
- `ejemplo_guiado.enunciado` con datos concretos propios y **único** frente a todos los hermanos del
  mismo sub-tema (no copiado).
- `al_terminar_debes_poder` no vacío.
- `estado: publicado`.
- Banco de ejercicios: 10 ítems por recurso (3+1+3+3 según los 4 `item_group`), `correct_answer`
  calza letra a letra con una de `choices`, `stable_id` único en todo el banco.

## 6. Formatos de salida

- **CSV** en `scratch/auditorias/YYYY-MM-DD-HHmm.csv` (no versionado — mismo tratamiento que el
  resto de `scratch/`). Una fila por recurso, una columna por punto del checklist, valor `OK` o el
  detalle del problema. Se abre directo en Excel/Sheets para filtrar y ordenar. Solo lo genera la
  barrida completa (modo sin argumentos) — el modo dirigido del hook no toca este archivo.
- **Markdown** en `docs/auditorias/YYYY-MM-DD-auditoria-nodos.md` (versionado, se commitea). Agrupado
  por bloque (`02.04`, `03.14`, `04.01`, …), con la lista de pendientes reales por recurso — funciona
  como el documento de tareas pendientes que pidió el 🧑. Tanto la barrida completa como el hook
  dirigido escriben/actualizan este mismo archivo del día; si ya existe uno para hoy, se actualizan
  solo las filas de los recursos tocados en vez de regenerarlo entero.

## 7. Pruebas

- Tests unitarios de `audit_resource_fields` sobre `dict`s de ejemplo: casos que deben pasar limpio,
  y un caso por cada regla del checklist que debe detectarse (campo vacío, checkpoints con 3
  alternativas, `ejemplo_guiado` duplicado entre hermanos, etc.) — sin necesidad de DB ni fixtures
  pesados, porque la función es pura.
- Un test de integración del comando en modo barrida completa contra un `KnowledgeNode` +
  `NodeContent` de prueba en la DB de test.
- Un test del modo dirigido contra un YAML de prueba en disco (sin depender de la DB).

## 8. Riesgos / rollback

- **Falsos positivos** en el chequeo de "placeholder" o "largo mínimo" si un recurso legítimo es
  breve — mitigado con umbrales generosos (ya probados en los scripts de `scratch/` existentes) y
  porque el hook solo avisa, nunca bloquea.
- **El hook agrega tiempo al commit** si se edita un lote grande de YAML de una sola vez — acotado
  porque corre solo sobre los archivos en stage, nunca el árbol completo.
- Rollback trivial: el comando y el servicio son código nuevo y aislado (no tocan modelos ni
  migraciones); si algo molesta, se quita la entrada de `.pre-commit-config.yaml` y/o se borra el
  comando sin efectos secundarios.
