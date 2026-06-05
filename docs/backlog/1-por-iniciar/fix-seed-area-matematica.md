# Fix: el seed crea "Matemáticas" (plural) duplicando el área "Matemática"

- **Estado:** Por iniciar
- **Creado:** 2026-06-05
- **Prioridad:** P2  ·  **Cartera:** continuidad
- **Tipo:** infraestructura · QA
- **Dueño sugerido:** 🔨 Antigravity (construcción) → 🧩 Codex (auditoría) → 🏛️ Claude (cierre)

> Una tarjeta está **Ready** solo si todos los campos están completos. Ver
> `docs/gobernanza/proceso-multiagente.md` §3.

## Objetivo (una frase)
Eliminar el área duplicada **"Matemáticas"** (plural, vacía) que aparece junto a la real
**"Matemática"** (singular, con 9 asignaturas y 127 recursos), corrigiendo su origen.

## Causa raíz (verificada 2026-06-05)
`apps/content/management/commands/seed_math_resources.py` (línea ~216) crea el área como
`name="Matemáticas"` (plural) y **corre en cada deploy** (Custom Start Command). Por eso la
duplicada reaparece aunque se borre a mano. La asignatura ya se normalizó a singular
("Matemáticas Escolar" → "Matemática Escolar", líneas ~220-234), pero el **área** quedó en plural.

## Fuentes a leer (rutas concretas)
- `apps/content/management/commands/seed_math_resources.py` (creación del área + bloque de fusión de la asignatura).
- `apps/content/migrations/0021_seed_areas.py` (comentario sobre el seed de Matemáticas).
- Modelo `apps/content/models/area.py`.

## Propuesta
- Cambiar el área del seed a **"Matemática"** (singular).
- Agregar paso **idempotente de fusión/renombrado**: si existe el área "Matemáticas", mover sus
  asignaturas (si las hubiera) a "Matemática" y **eliminar** la plural (mismo patrón que ya se usa
  para la asignatura). Que sea seguro de correr múltiples veces.
- Verificar que no rompa slugs/URLs (`/areas/matematica/` ya es la canónica).

## No-objetivos (qué queda FUERA)
- Renombrar asignaturas/temas (ya está hecho). Tocar otras áreas.

## Criterios de aceptación (verificables)
- [ ] Tras correr `seed_math_resources` (incluso 2 veces), existe **solo** "Matemática" (singular); no se recrea la plural.
- [ ] Las 9 asignaturas y 127 recursos quedan bajo "Matemática".
- [ ] Barrera verde: `test` · `check --deploy` · `makemigrations --check --dry-run`.

## Plan de pruebas
- Test de management command: sembrar, verificar que no exista "Matemáticas" y que la fusión sea idempotente.
- QA manual: correr el comando local; confirmar el dropdown del Estudio de publicación con una sola "Matemática".

## Riesgos / rollback
- **Pérdida de datos** si la fusión borra el área equivocada → la lógica debe mover asignaturas
  antes de borrar y solo borrar la plural vacía/fusionada. Rollback: revertir el commit del seed.
- En prod, ejecutar con cuidado (el seed corre en el deploy); validar primero en staging.

---

## Qué se hizo
_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_
