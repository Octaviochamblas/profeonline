# F3 — Banco de ejercicios de libros (piloto: 02.01 Números Enteros)

- **Estado:** Handoff Ready — verificado contra código real (2026-06-26)
- **Creado:** 2026-06-26
- **Prioridad:** P1 · **Cartera:** educativa
- **Tipo:** infraestructura · producto
- **Dueño sugerido:** 🧩 Codex (preflight) → 🔨 Antigravity (construcción)
- **Requiere:** F2 completo (páginas del nodo en pie)

## Objetivo

Crear el modelo `BookExercise` (ejercicios extraídos de Moraleja, Santillana, Baldor, Carreño) y la
sección de banco integrada en la página del nodo. Respuestas siempre visibles — sin login, sin
evaluación formal, sin registro de intentos. El alumno practica a su ritmo.

## Fuentes a leer

- `docs/backlog/2-arquitectura/arquitectura-plataforma-conocimiento.md` §3 Capa 3
- `apps/content/models/knowledge.py` — `KnowledgeNode` (de F1)
- `apps/learn/templates/` y vistas del nodo (de F2) — punto de integración de la UI

## Propuesta

### 1. Modelo `BookExercise` (en `apps/content/models/knowledge.py`)

| Campo | Tipo | Notas |
|---|---|---|
| `node` | `FK(KnowledgeNode, related_name='book_exercises')` | Solo hojas (`node_type='recurso'`) |
| `exercise_type` | `CharField(max_length=60)` | Slug del tipo. Ej: `adicion_mismo_signo` |
| `enunciado` | `TextField` | Puede contener KaTeX |
| `solucion` | `TextField` | Desarrollo paso a paso. Puede contener KaTeX |
| `respuesta` | `CharField(max_length=200)` | Resultado final limpio |
| `fuente` | `CharField(choices: moraleja\|santillana\|baldor\|carreño)` | |
| `dificultad` | `CharField(choices: basica\|media\|avanzada)` | |
| `order` | `PositiveSmallIntegerField(default=0)` | Orden de práctica sugerido |
| `estado` | `CharField(choices: borrador\|publicado, default='borrador')` | |

Meta: `ordering = ['exercise_type', 'dificultad', 'order']`

Registrar en `apps/content/models/__init__.py`.

### 2. Admin de Django

Registrar `BookExercise` en admin con:
- `list_display = ['node', 'exercise_type', 'fuente', 'dificultad', 'estado', 'order']`
- `list_filter = ['node__axis_abbr', 'exercise_type', 'fuente', 'dificultad', 'estado']`
- `search_fields = ['enunciado', 'node__semantic_id']`

También como inline dentro de `KnowledgeNodeAdmin` para carga cómoda de ejercicios.

> Nota: la carga inicial de ejercicios la hace el usuario desde el admin (no hay comando CLI en este
> sprint). Si en preflight se prefiere un YAML de ejercicios, definir el formato entonces.

### 3. Sección de banco en la página del nodo (modificar template de F2)

Agregar después de la explicación y ejemplos:

**"Ejercicios para practicar"** (solo si hay `BookExercise` publicados para el nodo):
- Agrupados por `exercise_type` (tabs o acordeón horizontal)
- Dentro de cada grupo, ordenados por `dificultad` luego `order`
- Cada ejercicio muestra:
  - `enunciado` (con KaTeX)
  - Botón **"Ver solución"** → despliega `solucion` + `respuesta` (toggle JS, sin petición al servidor)
- Si no hay ejercicios para el nodo: sección no aparece (no muestra "sin ejercicios")
- Sin login requerido

```html
<!-- Pseudotemplate -->
{% if node.book_exercises.filter(estado='publicado').exists %}
<section id="banco-ejercicios">
  <h2>Ejercicios para practicar</h2>
  {% for tipo, ejercicios in ejercicios_por_tipo.items %}
    <details>
      <summary>{{ tipo_display }}</summary>
      {% for ej in ejercicios %}
        <div class="ejercicio">
          <div class="enunciado">{{ ej.enunciado|katex }}</div>
          <button class="toggle-solucion">Ver solución</button>
          <div class="solucion hidden">
            {{ ej.solucion|katex }}
            <strong>Respuesta: {{ ej.respuesta }}</strong>
          </div>
        </div>
      {% endfor %}
    </details>
  {% endfor %}
</section>
{% endif %}
```

El toggle JS puede ser vanilla (no requiere framework).

## No-objetivos

- No scoring ni registro de intentos (eso es F4)
- No login obligatorio
- No ejercicios de evaluación formal (pool separado en F4)
- No poblar ejercicios para bloques distintos de 02.01 en este sprint

## Criterios de aceptación

- [ ] Barrera verde: `python manage.py test` · `check` · `makemigrations --check --dry-run`
- [ ] Sección "Ejercicios para practicar" visible en la página del nodo cuando hay ejercicios publicados
- [ ] Botón "Ver solución" muestra/oculta correctamente (sin recarga de página)
- [ ] KaTeX renderiza fórmulas en enunciados y soluciones
- [ ] Sin login: funciona exactamente igual que con login
- [ ] Nodo sin ejercicios: sección no aparece (sin errores)
- [ ] Admin: CRUD de ejercicios operativo, incluyendo inline en `KnowledgeNodeAdmin`
- [ ] Tests: constraints del modelo, vista del nodo incluye ejercicios en contexto

## Plan de pruebas

- Unit: constraints (`exercise_type` no vacío, `node` de tipo `recurso`)
- Smoke manual: cargar 3–5 ejercicios desde admin para un nodo del piloto y verificar UI

## Riesgos / rollback

- Si la cantidad de ejercicios es grande (>50 por nodo): usar paginación o lazy-load dentro del acordeón
- Rollback: revertir migración (tabla nueva, FK a `KnowledgeNode` que también es nueva — sin impacto en tablas existentes)

---

## Reutilización verificada (código real, 2026-06-26)

- **Existe un "banco visible" estructurado:** `apps/content/services/visible_bank_service.py` +
  modelos `ExerciseItem`/`ResourceExerciseItem`, anclado a `Topic`/`Resource` con cuotas de
  práctica/evaluación e ítems de aprendizaje. **Decisión:** F3 **NO** reutiliza ese sistema (distinto
  anclaje y propósito; está atado a la jerarquía vieja). F3 crea `BookExercise` propio, anclado a
  `KnowledgeNode`, **más simple** (ejercicio con respuesta siempre visible, sin cuotas ni ítems).
- **Referencia de UI:** la página pública de guía (`apps/content/views/learning_guide_student.py` y su
  template) muestra un banco agrupado con práctica — sirve como referencia visual del acordeón por tipo.
- **KaTeX:** igual que F2 — extender `base.html`, emitir `$...$`. No re-cablear.
- **Toggle "Ver solución":** JS vanilla con nonce (patrón CSP del sitio); sin librerías nuevas.

## Qué se hizo

_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_
