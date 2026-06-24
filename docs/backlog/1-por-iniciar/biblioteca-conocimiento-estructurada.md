# Biblioteca de Conocimiento Estructurada (Matemática preuniversitaria)

- **Estado:** Por iniciar
- **Creado:** 2026-06-23
- **Prioridad:** P1 · **Cartera:** educativa
- **Tipo:** producto · pedagogía · datos
- **Dueño sugerido:** 🏛️ Claude (estructura/contenido) + 🧑 Usuario (validación por gate)

> Proyecto grande, por fases con **gate de validación del dueño entre fase y fase**.
> No se avanza de fase sin OK del 🧑.

## Objetivo (una frase)
Construir una **biblioteca de conocimiento navegable** en ProfeOnline, organizada por una
**estructura universal por conceptos** (no por curso), donde cada recurso tenga teoría,
ejercicios estructurados, prácticas aleatorias y evaluación; partiendo por **Matemática
hasta nivel preuniversitario** (lo necesario para entrar a la Universidad).

## Decisiones del dueño (firmes)
1. **Empezar SOLO con Matemática.** Luego extrapolar a Física, Química y más áreas.
2. **Techo: preuniversitario completo** (entrar a la U). **NO** universitario aún.
3. **Construir DESDE 0** la estructura/contenido. Lo existente se integra **al final** (Fase 5).
4. **Granularidad: una sección = un recurso** (unidad enseñable ≈ una lección/video).
5. **Fuente del esqueleto: los ÍNDICES** de los libros (no los libros enteros).
6. **Reusar el software existente** (no reconstruir la app).
7. **Contenido ORIGINAL** informado por los libros, **nunca copia textual** (copyright).
8. **Economía de tokens**: extracción local; estructurar/redactar incremental por rama.
9. **Gates de validación del dueño** entre fases.

## Modelo: 4 capas por recurso
1. **Recurso teórico** — materia en texto + ejemplos, redactada original desde los libros → `Resource.content` (KaTeX).
2. **Banco de ejercicios estructurados** — ejercicios clasificados por tipo, de los libros → `Question` (por ítem/tipo).
3. **Prácticas con ejercicios aleatorios** — variaciones generadas desde los tipos → práctica mixta.
4. **Evaluación** — del **banco existente** (~2.500) → `Question` modo evaluación.

## Estructura universal (esqueleto)
- Concepto-primero y universal; un concepto existe **una sola vez**; los cursos son **vistas**.
- Ramas (preu): Números/Aritmética, Álgebra, Geometría, Trigonometría, Funciones,
  Probabilidad y Estadística (+ Cálculo introductorio si el PAES lo incluye).
- **Grafo** (prerrequisitos), no solo árbol. Dificultad como **rango** `[min, max]`.
- IDs estables `MAT.<RAMA>.<TEMA>`. Jerarquía ≤ 4 niveles.
- Vive en `docs/conocimiento/matematica.yaml` (versionado, fuente de verdad).

## Clasificación de ejercicios — 6 ejes
`Concepto` · `Tipo/patrón` · `Representación` (algebraico/gráfico/contextual/geométrico/tabular/numérico) ·
`Método` · `Dificultad` (básica/media/avanzada/desafío) · `Rol` (ejemplo resuelto/propuesto/evaluación).
Cada ejercicio queda **registrado** (reutilizable) **y** sirve de **molde** para replicar más del
mismo tipo (generación "modo documento" con semillas).

## Mapa de cobertura (tablero acordeón)
Tabla acordeón: cada categoría muestra el **resumen** de total de recursos vs cuántos
**completos** en cada una de las 4 capas (teórico / banco estructurado / práctica aleatoria /
evaluación). Estado por recurso/capa: `faltante · borrador · publicado`. Arranca como archivo;
luego **panel admin in-app** (reusando el patrón del "Resumen del banco"; paneles propios, no Django admin).

## Fuentes a leer (rutas concretas)
- `apps/content/models/` (`Resource` con `content`/`is_published`, `Question`, `ExerciseItem`).
- `apps/content/services/guide_service.py` (`extract_guide_text`, `pypdf`).
- `apps/content/services/ai_generation_service.py` (generación "modo documento" para replicar).
- `apps/content/management/commands/` (`import_quiz_guide`, `import_questions_json`, `generate_ai_questions`).
- Patrón de panel acordeón: `templates/pages/` del "Resumen del banco" (`bank_coverage`).

## Propuesta — Plan de trabajo por fases
```
Índices → [F1 Esqueleto] → ✅🧑 → [F2 Mapa] → [F3 1 rama completa] → ✅🧑 → [F4 Escalar] → [F5 Integrar existente] → [F6 Videos+dashboard]
```
- **Fase 0 — Convenciones (hecho):** sección=recurso · 6 ejes · 4 capas · techo preu · IDs · `docs/conocimiento/`.
- **Fase 1 — Esqueleto de Matemática:** desde los índices → `matematica.yaml` (ramas → secciones=recursos, con dificultad/prereqs/objetivos). **Gate del 🧑.**
- **Fase 2 — Mapa de cobertura:** tablero acordeón con las 4 capas, todo en "faltante".
- **Fase 3 — Plantilla (1 rama completa):** una rama (ej. Álgebra) llenada de punta a punta las 4 capas, vía **comando local**, como **borradores**. **Gate del 🧑.**
- **Fase 4 — Escalar:** rama por rama, guiado por el mapa, hasta cubrir todo preu.
- **Fase 5 — Integrar lo existente:** crosswalk de recursos/preguntas actuales → reusar o archivar.
- **Fase 6 — Videos + dashboard vivo:** clasificación de videos sobre los recursos + panel acordeón en la app.

## Manejo de fuentes y tokens
- Esqueleto: **solo índices** (foto/pegar/extraer índice del PDF con `pypdf`).
- Contenido/ejercicios: libros completos → texto local en `docs/fuentes/` (gitignored si copyright), leídos **por tramos**.
- **Sin pegar libros en el chat.** PDF escaneado → OCR (Adobe) o visión.
- Poblar la DB con **comandos locales** ("a cuentagotas desde el PC"), no por la web (evita timeout de gunicorn).

## No-objetivos (qué queda FUERA)
- Física y Química (se hacen después de consolidar Matemática).
- Nivel universitario (Cálculo universitario, Álgebra Lineal, etc.).
- Integrar la taxonomía/recursos existentes al inicio (se hace en Fase 5).
- Reconstruir software de la app (se reusa lo que hay).

## Criterios de aceptación (verificables)
- [ ] **Fase 1:** `matematica.yaml` con IDs únicos, prerrequisitos consistentes, rangos de dificultad válidos, validado por el 🧑.
- [ ] **Fase 2:** mapa de cobertura generado del esqueleto (4 capas por recurso).
- [ ] **Fase 3:** una rama completa (4 capas) como borradores; el 🧑 valida formato/calidad.
- [ ] Contenido **original** (sin copia textual de los libros).
- [ ] Barrera verde en cada cambio de software: `test` · `check` · `makemigrations --check --dry-run`.

## Plan de pruebas
- Validación del esqueleto: script que verifica unicidad de IDs y consistencia de prerrequisitos.
- Fase 3: QA visual del recurso (teoría con KaTeX, banco estructurado, práctica, evaluación) en runserver local.
- Tests de los comandos locales de poblamiento.

## Riesgos / rollback
- **Volumen/tokens:** se mitiga con extracción local + trabajo incremental por rama + gates.
- **Copyright:** contenido original, libros solo como fuente; carpeta de fuentes gitignored.
- **Datos:** poblar como **borrador** (`is_published=False`); nada se publica sin revisión del 🧑.
- **Rollback:** la estructura vive en archivos versionados; el contenido en borradores reversibles.

## Acción inmediata
El 🧑 entrega los **índices** de los libros de matemática (preu/escolar) → 🏛️ genera
**esqueleto v1 + mapa de cobertura vacío** en `docs/conocimiento/` → gate de validación.

---

## Qué se hizo
_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_
