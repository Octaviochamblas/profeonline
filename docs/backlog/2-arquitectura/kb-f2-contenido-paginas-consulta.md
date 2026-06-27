# F2 — Contenido pedagógico y páginas de consulta (piloto: 02.01 Números Enteros)

- **Estado:** Handoff Ready — verificado contra código real (2026-06-26)
- **Creado:** 2026-06-26
- **Prioridad:** P0 · **Cartera:** educativa · producto
- **Tipo:** infraestructura · producto
- **Dueño sugerido:** 🧩 Codex (preflight) → 🔨 Antigravity (construcción)
- **Requiere:** F1 completo (KnowledgeNode en DB)
- **Bloquea:** F3, F4, F5, F6

## Objetivo

Crear los modelos de contenido pedagógico (`NodeContent`, `NodeMedia`), el comando de carga, las
páginas públicas `/aprender/…` y el template de nodo — usando el bloque 02.01 (Números Enteros,
36 recursos) como piloto. **Gate del usuario:** validar el piloto en producción antes de escalar.

## Fuentes a leer

- `docs/backlog/2-arquitectura/arquitectura-plataforma-conocimiento.md` §3 Capa 2 + §6 (A)
- `docs/conocimiento/numeros-enteros.yaml` — estructura del piloto (2 temas, 36 recursos)
- `apps/content/models/knowledge.py` — `KnowledgeNode` (de F1)
- `apps/content/models/__init__.py` — modelos existentes (no tocar)
- Cualquier template existente que use KaTeX — reusar el pipeline de renderizado

## Propuesta

### 1. Modelos nuevos en `apps/content/models/knowledge.py`

**`NodeContent`** — O2O con nodo hoja. El texto pedagógico tipo AlonsoFormula:

| Campo | Tipo | Notas |
|---|---|---|
| `node` | `OneToOneField(KnowledgeNode, related_name='content')` | Solo hojas (`node_type='recurso'`) |
| `objetivo` | `TextField` | "Al finalizar serás capaz de…" |
| `explicacion` | `TextField` | Markdown + KaTeX |
| `procedimiento` | `JSONField(default=list)` | `[{"paso": 1, "texto": "..."}]` |
| `ejemplos` | `JSONField(default=list)` | `[{"titulo":"...","enunciado":"...","solucion_pasos":[...]}]` |
| `errores_frecuentes` | `JSONField(default=list)` | Lista de errores comunes |
| `estado` | `CharField(choices: borrador\|publicado, default='borrador')` | Borrador → `noindex` |
| `fuente` | `TextField(blank=True)` | Referencia bibliográfica auditable |

**`NodeMedia`** — videos y archivos que apoyan un nodo. Varios por nodo:

| Campo | Tipo | Notas |
|---|---|---|
| `node` | `FK(KnowledgeNode, related_name='media')` | |
| `kind` | `CharField(choices: video_youtube\|file\|external)` | |
| `video_kind` | `CharField(choices: explicacion\|ejercicios_resueltos\|complementario, blank=True)` | Solo si `kind=video_*` |
| `url` | `URLField(blank=True)` | |
| `file` | `FileField(blank=True)` | |
| `order` | `PositiveSmallIntegerField(default=0)` | |

Meta: `ordering = ['order']`

Registrar ambos en `apps/content/models/__init__.py`.

### 2. Formato YAML de contenido (crear `docs/conocimiento/contenido/`)

Un archivo YAML por recurso o por tema (definir en preflight cuál es más cómodo para la carga desde
NotebookLM). Propuesta por recurso:

```yaml
# docs/conocimiento/contenido/mat-num-enteros-conjunto-naturales.yaml
semantic_id: MAT.NUM.ENTEROS_CONJUNTO.NATURALES
objetivo: "Al finalizar serás capaz de identificar los números naturales y distinguirlos de otros conjuntos numéricos."
explicacion: |
  Los **números naturales** son los números que usamos para contar: 1, 2, 3, ...

  $$\mathbb{N} = \{1, 2, 3, 4, \ldots\}$$

  Algunos autores incluyen el cero ($$\mathbb{N}_0$$) y otros no.
procedimiento:
  - "Verifica que el número sea positivo (mayor que cero)"
  - "Verifica que no tenga parte decimal"
  - "Si ambas condiciones se cumplen, el número pertenece a ℕ"
ejemplos:
  - titulo: "¿Pertenece 7 a los números naturales?"
    enunciado: "Clasifica el número 7."
    solucion_pasos:
      - "7 es positivo: ✓"
      - "7 no tiene decimales: ✓"
      - "Por lo tanto, 7 ∈ ℕ"
  - titulo: "¿Pertenece −3 a los números naturales?"
    enunciado: "Clasifica el número −3."
    solucion_pasos:
      - "−3 es negativo: ✗"
      - "Por lo tanto, −3 ∉ ℕ"
errores_frecuentes:
  - "Incluir el cero sin verificar la convención del texto"
  - "Confundir ℕ con ℤ (ℤ incluye los enteros negativos)"
fuente: "Moraleja p. 21"
estado: publicado
```

### 3. Comando `apps/content/management/commands/load_node_content.py`

1. Glob todos los `docs/conocimiento/contenido/*.yaml`
2. Por cada archivo: `node = KnowledgeNode.objects.get(semantic_id=data['semantic_id'])`
3. `NodeContent.objects.update_or_create(node=node, defaults={...})`
4. Idempotente: segunda ejecución actualiza sin duplicar
5. Resumen: `Creados: X, Actualizados: Y, semantic_id no encontrado: Z (advertencia, no error)`

### 4. Nueva app `apps/learn/`

Crear `apps/learn/` para las páginas públicas (evita interferir con `apps/content/`).
Agregar a `INSTALLED_APPS` en `config/settings/local.py` y `config/settings/production.py`.

### 5. URLs y vistas (en `apps/learn/`)

La asignatura es el primer nivel de la URL. Hoy solo existe `matematicas`; Física y Química
entran en el futuro sin cambiar la estructura.

```
GET /aprender/                                              → lista de asignaturas (MAT, FIS, QUI…)
GET /aprender/<asignatura-slug>/                            → ejes de la asignatura
GET /aprender/<asignatura-slug>/<eje-slug>/                 → bloques del eje
GET /aprender/<asignatura-slug>/<eje-slug>/<bloque-slug>/   → temas del bloque
GET /aprender/<asignatura-slug>/<eje-slug>/<bloque-slug>/<tema-slug>/          → recursos del tema
GET /aprender/<asignatura-slug>/<eje-slug>/<bloque-slug>/<tema-slug>/<recurso-slug>/  → página del nodo
```

Ejemplo concreto del piloto:
```
/aprender/matematicas/numeros/enteros/conjunto-y-orden/identificacion-numeros-naturales/
```

La vista del nodo (`NodeDetailView`) muestra:
1. Breadcrumb navegable (eje → bloque → tema → recurso)
2. `NodeContent.objetivo` (si existe)
3. `NodeContent.explicacion` renderizado con Markdown + KaTeX
4. `NodeContent.procedimiento` (lista numerada)
5. `NodeContent.ejemplos` (acordeón o lista)
6. `NodeMedia` de `video_kind='explicacion'` (embed YouTube si existe)
7. Placeholder si no hay `NodeContent` (nodo en borrador)

### 6. SEO y robots

- `<title>` = `{node.name} | ProfeOnline`
- `<meta name="description">` = `{node.objetivo[:155]}` (o descripción del bloque/tema si es intermedio)
- `<meta name="robots" content="noindex, nofollow">` si `NodeContent.estado='borrador'` o `not node.is_published`
- URL canónica

### 7. KaTeX

Verificar en preflight que el nonce del CSP middleware (`apps/core/middleware.py`) cubre el script
de KaTeX en los templates nuevos. Reusar el mismo pipeline que el resto de la app.

## No-objetivos

- No banco de ejercicios (F3)
- No evaluación formal (F4)
- No estado del alumno (F5)
- No prerrequisitos UI (F6)
- No poblar contenido para bloques distintos de 02.01 en este sprint
- No redirigir ni tocar las páginas viejas (`Area/Subject/Topic/Resource`)

## Criterios de aceptación

- [ ] Barrera verde: `python manage.py test` · `check` · `makemigrations --check --dry-run`
- [ ] `GET /aprender/matematicas/numeros/enteros/conjunto-y-orden/<slug>/` → 200
- [ ] Página muestra breadcrumb, objetivo, explicación, KaTeX renderizado, video embed
- [ ] Nodo sin `NodeContent` → placeholder (no 500)
- [ ] Nodo en `borrador` → `<meta name="robots" content="noindex">`
- [ ] `load_node_content` es idempotente (dos ejecuciones seguidas no crean duplicados)
- [ ] Template responsive: sin scroll horizontal en mobile (375px)
- [ ] Tests: `NodeContent` constraints, `load_node_content` idempotencia, vistas 200/404

## Plan de pruebas

- Unit: `NodeContent` / `NodeMedia` constraints; lógica de SEO
- Integration: `load_node_content` con los YAMLs reales del piloto
- Smoke manual: navegar `/aprender/…`, verificar KaTeX renderiza, verificar video embeds

## Riesgos / rollback

- KaTeX + CSP nonce: verificar antes de deployar que el nonce se aplica al script de KaTeX
- Si el contenido del piloto no está listo: el comando corre vacío (borrador + noindex); el sitio
  existe pero muestra placeholder — no bloquea el merge
- Rollback: revertir migraciones + eliminar app `learn`; sin impacto en el sitio existente

---

## Reutilización verificada (código real, 2026-06-26)

- **Wiring de URLs:** `config/urls.py` incluye apps en la raíz (`path("", include("apps.content.urls"))`).
  Agregar **una línea**: `path("aprender/", include("apps.learn.urls"))`. Crear `apps/learn/` y
  registrarla en `INSTALLED_APPS` (local + production).
- **KaTeX YA está cableado una sola vez** en `templates/base.html` (+ `static/js/katex-init.js` con nonce,
  que renderiza al cargar y en cada `htmx:afterSwap`). Las plantillas de F2 **solo extienden
  `base.html`** y emiten `$...$` / `$$...$$`. **NO** re-incluir KaTeX ni tocar la CSP.
- **SEO:** reutilizar los helpers de `apps/content/views/_seo.py` (ya usados por las vistas actuales).
- **Plantilla de referencia:** `apps/content/views/resource_detail.py` + sus templates muestran el patrón
  de breadcrumb + secciones; replicar el estilo, no el modelo.
- **Redirect de páginas viejas:** `apps/content/views/legacy_redirects.py` ya existe — se usará en F7
  (escalado), **no** en F2.

## Qué se hizo

_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_
