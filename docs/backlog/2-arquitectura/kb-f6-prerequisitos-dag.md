# F6 — Prerrequisitos y guía de ruta (piloto: 02.01 Números Enteros)

- **Estado:** Handoff — listo para preflight
- **Creado:** 2026-06-26
- **Prioridad:** P2 · **Cartera:** educativa · producto
- **Tipo:** infraestructura · producto
- **Dueño sugerido:** 🧩 Codex (preflight) → 🔨 Antigravity (construcción)
- **Requiere:** F5 completo (`StudentNodeState` en DB)

## Objetivo

Activar el DAG de prerrequisitos: crear el archivo YAML del piloto, el comando `load_prerequisites`
con validación transaccional de ciclos, y la UI "Antes de empezar" / "Siguiente recomendado" en la
página del nodo. El acceso nunca se bloquea — solo se avisa.

## Fuentes a leer

- `docs/backlog/2-arquitectura/arquitectura-plataforma-conocimiento.md` §3 Capa 1 (`NodePrerequisite`) + §1 principio #6
- `apps/content/models/knowledge.py` — `NodePrerequisite`, `KnowledgeNode`, `StudentNodeState`
- `apps/learn/templates/` y vistas del nodo (de F2) — punto de integración de la UI
- `docs/conocimiento/numeros-enteros.yaml` — para entender la estructura del bloque piloto

## Propuesta

### 1. Archivo DAG del piloto

Crear `docs/conocimiento/dag/num-enteros.yaml`:

```yaml
# DAG de prerrequisitos — Eje 02, Bloque 01: Números Enteros
# El tema de operatoria (02.01.02) requiere dominar el tema de conjunto y orden (02.01.01).
prerequisitos:
  - node: MAT.NUM.ENTEROS_OPERATORIA      # Operatoria en enteros
    requires: MAT.NUM.ENTEROS_CONJUNTO    # El conjunto de los enteros y orden
    kind: requerido
    min_mastery: 0.75
```

El DAG del piloto es simple (un solo prerrequisito intra-bloque). Los prerrequisitos entre bloques
distintos (ej: enteros → racionales) se agregan en F7 cuando el segundo bloque esté completo.

### 2. Comando `apps/content/management/commands/load_prerequisites.py`

Lógica:

1. Glob todos los `docs/conocimiento/dag/*.yaml`
2. Por cada arista: resolver `semantic_id` a `KnowledgeNode` para `node` y `requires`
3. Construir el grafo completo en memoria
4. Validar aciclicidad con `graphlib.TopologicalSorter` (stdlib Python ≥3.9; si no disponible, DFS propio)
5. Si hay ciclo: imprimir el ciclo detectado y **abortar sin guardar ningún cambio** (transacción atómica)
6. Si OK: upsert todos los `NodePrerequisite` por `(node, requires)` — idempotente

```python
from graphlib import TopologicalSorter, CycleError

def validate_dag(edges):
    graph = {}
    for node_id, requires_id in edges:
        graph.setdefault(node_id, set()).add(requires_id)
    ts = TopologicalSorter(graph)
    try:
        list(ts.static_order())  # Lanza CycleError si hay ciclo
    except CycleError as e:
        raise ValueError(f"Ciclo detectado en el DAG de prerrequisitos: {e}") from e
```

El comando reporta al final: `Creados: X, Actualizados: Y, Sin cambios: Z`.

### 3. UI en la página del nodo (modificar template de F2)

**"Antes de empezar"** — arriba del contenido, solo si el nodo tiene prerrequisitos:

```
Antes de empezar, asegúrate de dominar:
  ✓ El conjunto de los enteros y orden   ← (dominado por el alumno)
  ! Valor absoluto                        ← (no dominado — enlace a ese nodo)
```

- Con login: muestra `✓` o `!` según `StudentNodeState.status`
- Sin login: lista los prerrequisitos como links simples (sin estado)
- **Nunca bloquea el acceso** — si el prerrequisito no está cumplido, el alumno sigue pudiendo leer

**"Siguiente recomendado"** — al final de la página:

```
Siguiente: Operatoria en enteros →
```

Lógica:
1. Buscar nodos que tienen `este_nodo` como prerrequisito y no están dominados por el alumno
2. Si no hay ninguno: mostrar el siguiente hermano (mismo tema, `order` siguiente)
3. Si no hay hermano: mostrar el primer recurso del siguiente tema del bloque

## No-objetivos

- No bloquear el acceso al nodo si el prerrequisito no está cumplido (nunca candado duro)
- No poblar el DAG de todos los bloques — eso es F7 (se hace bloque a bloque)
- No UI del mapa gamificado (F8)
- No modificar `NodePrerequisite` ya creado en F1 (ya existe el modelo; aquí solo se carga el DAG)

## Criterios de aceptación

- [ ] Barrera verde: `python manage.py test` · `check` · `makemigrations --check --dry-run`
- [ ] `load_prerequisites` con `num-enteros.yaml` válido: crea el `NodePrerequisite` correctamente
- [ ] `load_prerequisites` con un ciclo artificial introducido en el YAML: aborta, no modifica la DB, imprime el ciclo
- [ ] `load_prerequisites` es idempotente (segunda ejecución: `Creados: 0, Actualizados: 1`)
- [ ] Página del nodo `MAT.NUM.ENTEROS_OPERATORIA` muestra sección "Antes de empezar"
- [ ] Sin login: prerrequisitos visibles como links (sin estado)
- [ ] Con login: estado del prerrequisito correcto (✓ dominado / ! pendiente)
- [ ] "Siguiente recomendado" lleva al nodo correcto
- [ ] Tests: detección de ciclos (con grafo con ciclo y sin ciclo), idempotencia del comando, UI con y sin login

## Plan de pruebas

- Unit: algoritmo de detección de ciclos (grafo simple, grafo con ciclo, grafo desconectado)
- Integration: `load_prerequisites` con el DAG del piloto
- Smoke manual: navegar la página y verificar que las secciones UI aparecen correctamente con usuario logueado y sin login

## Riesgos / rollback

- `graphlib` disponible desde Python 3.9 — verificar versión del entorno en preflight
- Prerrequisitos que referencian `semantic_id` que no existe en DB: advertir (no error fatal) y continuar
- Rollback: `NodePrerequisite` es tabla nueva (F1); sin impacto en tablas existentes. Eliminar el archivo YAML del DAG.

---

## Qué se hizo

_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_
