# F1 — KnowledgeNode: esqueleto del grafo de conocimiento

- **Estado:** Handoff — listo para preflight
- **Creado:** 2026-06-26
- **Prioridad:** P0 · **Cartera:** infraestructura
- **Tipo:** infraestructura
- **Dueño sugerido:** 🧩 Codex (preflight) → 🔨 Antigravity (construcción)
- **Bloquea:** F2, F3, F4, F5, F6 (todo lo demás)

## Objetivo

Crear el modelo `KnowledgeNode` autorreferente y el comando `import_knowledge_tree` que lee todos los
YAMLs de `docs/conocimiento/*.yaml` y carga los ~700 nodos en la base de datos. Sin esto no existe
ninguna otra capa.

## Fuentes a leer

- `docs/backlog/2-arquitectura/arquitectura-plataforma-conocimiento.md` §3 Capa 1
- `docs/conocimiento/numeros-enteros.yaml` — muestra la estructura YAML a parsear (2 temas, 36 recursos)
- `docs/conocimiento/_REGISTRO-CODIGOS.md` — mapeo completo de todos los ejes y bloques
- `apps/content/models/__init__.py` — modelos existentes (no tocar)

## Propuesta

### 1. Nuevo archivo `apps/content/models/knowledge.py`

**`KnowledgeNode`** — árbol autorreferente (adjacency list):

| Campo | Tipo | Notas |
|---|---|---|
| `semantic_id` | `CharField(max_length=120, unique=True)` | Llave eterna **única global**. Ej: `MAT.NUM.ENTEROS_CONJUNTO` |
| `code` | `CharField(max_length=20)` | Para mostrar/ordenar. Ej: `02.01.01`. **Único por asignatura**, no global |
| `node_type` | `CharField(choices)` | `asignatura \| eje \| bloque \| tema \| recurso` |
| `parent` | `FK('self', null=True, blank=True, related_name='children')` | Null solo en `asignatura` (raíz) |
| `name` | `CharField(max_length=200)` | Nombre legible |
| `slug` | `SlugField(max_length=220, unique=True)` | Auto-generado desde `semantic_id` |
| `order` | `PositiveSmallIntegerField(default=0)` | Orden entre hermanos |
| `subject_abbr` | `CharField(max_length=10)` | `MAT \| FIS \| QUI` — primer segmento del `semantic_id` |
| `axis_abbr` | `CharField(max_length=10, blank=True)` | `NUM \| ALG \| GEO \| EST \| FUND` — vacío en asignatura |
| `competencia` | `CharField(max_length=2, blank=True)` | `M1 \| M2 \| U` — solo hojas |
| `dificultad` | `CharField(max_length=10, blank=True)` | `basica \| media \| avanzada` — solo hojas |
| `cursos` | `JSONField(default=list)` | `["7B","8B"]` — solo hojas |
| `is_published` | `BooleanField(default=False)` | |

Meta: `ordering = ["subject_abbr", "code"]` · `UniqueConstraint(["subject_abbr", "code"])`

> **Jerarquía: `Asignatura > Eje > Bloque > Tema > Recurso`.** La asignatura es la raíz. Hoy solo
> `MAT`; `FIS`/`QUI` entran agregando YAML con su prefijo, sin tocar el modelo.
>
> **`semantic_id` sintético para nodos estructurales** (asignatura/eje/bloque no traen `id` en el YAML):
> - asignatura: `MAT` · code `MAT`
> - eje: `MAT.NUM` (subject + abreviatura) · code `02`
> - bloque: `MAT.NUM.B0201` (prefijo `B` + bloque_codigo sin punto) · code `02.01`
> - tema: `MAT.NUM.ENTEROS_CONJUNTO` (del YAML) · code `02.01.01`
> - recurso: `MAT.NUM.ENTEROS_CONJUNTO.NATURALES` (del YAML) · code `02.01.01.01`

**`NodePrerequisite`** — aristas del DAG (modelo vacío, sin UI aún; se activa en F6):

| Campo | Tipo | Notas |
|---|---|---|
| `node` | `FK(KnowledgeNode, related_name='prerequisites')` | El que tiene prerrequisitos |
| `requires` | `FK(KnowledgeNode, related_name='required_by')` | El que se necesita antes |
| `kind` | `CharField(choices: requerido\|recomendado, default='requerido')` | |
| `min_mastery` | `FloatField(default=0.75)` | Umbral para darlo por cumplido |

Meta: `UniqueConstraint(['node', 'requires'])`

### 2. Registrar en `apps/content/models/__init__.py`

Importar `KnowledgeNode` y `NodePrerequisite` para que aparezcan en migraciones.

### 3. Comando `apps/content/management/commands/import_knowledge_tree.py`

Lógica:
1. Glob todos los `docs/conocimiento/*.yaml` (excluir los que empiezan con `_`)
2. Por cada YAML (= un bloque), sintetizar/reusar la cadena de ancestros
   (asignatura → eje → bloque) y luego crear temas → recursos
3. Para cada nivel: `KnowledgeNode.objects.update_or_create(semantic_id=..., defaults={...})`
   — la asignatura y el eje se reusan entre archivos del mismo eje (idempotente)
4. `subject_abbr` se deriva del prefijo del `id` del primer tema/recurso (`MAT.…`);
   nombre de la asignatura desde un mapa `{MAT: "Matemáticas", FIS: "Física", QUI: "Química"}`
5. Auto-generar `slug` desde `semantic_id` con `slugify` + resolución de colisiones
6. Al final, imprimir resumen: `Creados: X, Actualizados: Y, Sin cambios: Z`

Mapeo YAML → campos del modelo:

```
YAML                    → KnowledgeNode
─────────────────────────────────────────
(prefijo del id)        → asignatura: semantic_id='MAT', code='MAT', name='Matemáticas'
abreviatura: "NUM"      → eje: semantic_id='MAT.NUM', axis_abbr='NUM'
codigo: "02"            → eje: code='02', node_type='eje'
bloque: "Enteros"       → bloque: name='Enteros', node_type='bloque'
bloque_codigo: "02.01"  → bloque: code='02.01', semantic_id='MAT.NUM.B0201'
tema.codigo: "02.01.01" → tema: code='02.01.01', node_type='tema'
recurso.cod: "02.01.01.01" → code='02.01.01.01', node_type='recurso'
recurso.id: "MAT.NUM.ENTEROS_CONJUNTO.NATURALES" → semantic_id
recurso.nombre: "..."   → name
recurso.competencia     → competencia
recurso.dificultad      → dificultad
recurso.cursos          → cursos (JSON)
```

El orden entre hermanos se asigna por posición en el YAML.

### 4. Admin en `apps/content/admin.py`

```python
@admin.register(KnowledgeNode)
class KnowledgeNodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'node_type', 'name', 'semantic_id', 'competencia', 'is_published']
    list_filter = ['node_type', 'axis_abbr', 'competencia', 'is_published']
    search_fields = ['semantic_id', 'code', 'name']
    raw_id_fields = ['parent']
```

### 5. Migración + tests

Un archivo de migración limpio. Tests en `apps/content/tests/test_knowledge_node.py`.

## No-objetivos

- No crear contenido pedagógico (F2)
- No URLs públicas ni templates
- No validar ciclos en `NodePrerequisite` (F6)
- No tocar ningún modelo existente: `Area`, `Subject`, `Topic`, `Resource`, `Question`, etc.

## Criterios de aceptación

- [ ] Barrera verde: `python manage.py test` · `check` · `makemigrations --check --dry-run`
- [ ] `python manage.py import_knowledge_tree` corre sin error
- [ ] `KnowledgeNode.objects.count()` ≥ 700 tras la primera ejecución
- [ ] Segunda ejecución: `Creados: 0` (idempotente — no duplica nodos)
- [ ] `KnowledgeNode.objects.filter(node_type='recurso').count()` ≥ 600
- [ ] Ningún nodo tiene `slug` vacío ni slug duplicado
- [ ] Admin muestra los nodos con filtros funcionales
- [ ] Tests: constraints de unicidad, árbol padre-hijo, idempotencia del comando

## Plan de pruebas

- Unit: unicidad de `semantic_id` y `code`, generación de slug, relación padre-hijo
- Integration: correr `import_knowledge_tree` contra los YAMLs reales en `docs/conocimiento/`
- Smoke: verificar en admin local que el árbol se ve correcto

## Riesgos / rollback

- YAML con formato inesperado: el comando debe fallar con mensaje claro (no silencioso) e indicar el archivo y línea
- Rollback: `migrate content 000X` (la migración anterior); tablas nuevas, sin impacto en tablas existentes

---

## Qué se hizo

**Construido y verificado (2026-06-26, 🏛️ Claude por pedido directo del 🧑).**

- `apps/content/models/knowledge.py` — modelos `KnowledgeNode` (árbol autorreferente con
  `semantic_id` único global, `code` único por asignatura, `node_type` de 5 niveles, slug
  auto-generado del nombre) y `NodePrerequisite` (esquema del DAG, sin UI aún).
- `apps/content/management/commands/import_knowledge_tree.py` — import idempotente por
  `semantic_id`. Sintetiza asignatura/eje/bloque; omite archivos legacy (sin `codigo`/
  `bloque_codigo`) con aviso. Opciones `--dir` y `--file`.
- `apps/content/admin.py` — `KnowledgeNodeAdmin` (filtros por tipo/asignatura/eje/competencia)
  y `NodePrerequisiteAdmin`.
- Migración `0037_knowledgenode_nodeprerequisite_and_more.py`.
- `apps/content/tests/test_knowledge_node.py` — 8 tests (constraints, slug, árbol, idempotencia,
  omisión de legacy, `--file`).

**Resultado del import real** (`python manage.py import_knowledge_tree`):
`1 asignatura · 5 ejes · 43 bloques · 248 temas · 1911 recursos = 2208 nodos`.
13 archivos legacy omitidos (incluido `fundamentos-atomico.yaml`, deprecado).
Barrera verde: 8/8 tests · `check` OK · `makemigrations --check` sin cambios.

Pendiente: auditoría (🧩 Codex) y merge. Siguiente fase: **F2** (contenido + páginas de consulta,
piloto números enteros).
