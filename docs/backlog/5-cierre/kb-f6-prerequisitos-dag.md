# F6 — Prerrequisitos y guía de ruta (piloto: 02.01 Números Enteros)

- **Estado:** Cierre — subconjunto estructural construido; complemento con estado diferido a F5
- **Creado:** 2026-06-26
- **Prioridad:** P2 · **Cartera:** educativa · producto
- **Tipo:** infraestructura · producto
- **Dueño sugerido:** 🧩 Codex (preflight) → 🔨 Antigravity (construcción)
- **Requiere:** F1 completo (`NodePrerequisite`). La parte con estado requiere F5 y queda diferida.

## Objetivo

Activar el DAG de prerrequisitos: crear el archivo YAML del piloto, el comando `load_prerequisites`
con validación transaccional de ciclos, y la UI "Antes de empezar" / "Siguiente recomendado" en la
página del nodo. El acceso nunca se bloquea — solo se avisa.

> **Decisión de alcance D4:** F6 se cerró primero como infraestructura estructural independiente del
> estado del alumno. Los indicadores ✓/!, la lógica de dominio y "Siguiente recomendado" se
> implementarán junto con F5 (`StudentNodeState`), sin bloquear la consulta actual.

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

- [ ] Barrera verde en CI del PR de cierre
- [x] `load_prerequisites` con `num-enteros.yaml` válido: crea el `NodePrerequisite` correctamente
- [x] `load_prerequisites` con un ciclo artificial introducido en el YAML: aborta sin modificar la DB
- [x] `load_prerequisites` es idempotente
- [x] Página del nodo con prerrequisitos muestra sección "Antes de empezar"
- [x] Sin login: prerrequisitos visibles como links (sin estado)
- [ ] Con login: estado del prerrequisito correcto (✓ dominado / ! pendiente) — **diferido a F5**
- [ ] "Siguiente recomendado" lleva al nodo correcto — **diferido a F5**
- [x] Tests: detección de ciclos, atomicidad, idempotencia y UI estructural

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

- Se implementó `load_prerequisites` con carga YAML, resolución por `semantic_id`, validación de
  ciclos con `TopologicalSorter`, transacción atómica e idempotencia.
- Se creó el piloto `docs/conocimiento/dag/num-enteros.yaml` y se amplió la población con
  `fundamentos.yaml` (12 aristas de Lógica y Conjuntos).
- Se incorporó la caja informativa "Antes de empezar" con enlaces solo a prerrequisitos publicados;
  nunca bloquea el acceso.
- Se mejoró visualmente la caja y se unificó el breadcrumb del detalle de recursos con los chips del
  explorador, corrigiendo además su alineación vertical.
- La parte dependiente del alumno (✓/! y siguiente recomendado) queda explícitamente en F5.
- Verificación local de la entrega final: 18 tests focalizados verdes, `check` verde, sin migraciones.
