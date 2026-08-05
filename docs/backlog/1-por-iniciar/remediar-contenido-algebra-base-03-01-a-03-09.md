# Remediar contenido de 12 secciones — Álgebra base (03.01–03.09)

- **Estado:** Por iniciar
- **Creado:** 2026-08-05
- **Prioridad:** P1 · **Cartera:** educativa
- **Tipo:** pedagogía
- **Dueño sugerido:** 🏛️ Claude (redacción manual; no automatizable con plantilla — ver "Propuesta")

## Objetivo (una frase)
Completar los campos obligatorios de `NodeContent` que quedaron incompletos o genéricos en los
365 recursos de `03.01` a `03.09` (Nomenclatura, Lenguaje Algebraico, Operaciones, Multiplicación,
Productos Notables, Factorización, MCD/MCM, Ecuaciones de Primer Grado, Desigualdades) — el grupo
con menos fallas de los tres (`errores_frecuentes` y `ejemplos` ya están correctos aquí).

## Fuentes a leer (rutas concretas)
- `docs/auditorias/2026-08-05-auditoria-contenido-12-secciones.md` — auditoría completa (causa
  raíz, metodología, hallazgos).
- `docs/auditorias/2026-08-05-auditoria-contenido-12-secciones.json` — lista exacta de los 365
  `semantic_id` de este grupo con sus campos faltantes (`"nodo"` entre `03.01` y `03.09`).
- `docs/conocimiento/pauta-contenido.md` — estándar de 12 secciones, tabla "Campos obligatorios".
- `docs/conocimiento/contenido/*.yaml` — YAML fuente por recurso (buscar por `semantic_id`).
- `apps/content/management/commands/load_node_content.py` — loader (mapeo de campos, sin bugs).

## Propuesta
Por cada uno de los 365 recursos (lista exacta en el JSON de la auditoría), editar su YAML fuente
para completar, **sin plantilla genérica** (esa es justamente la causa del problema actual):

1. **`ejemplo_guiado`** (365 recursos, 100% de este grupo): redactar un problema concreto con
   datos propios (expresión algebraica específica, no el nombre del recurso pegado en una frase
   molde) y resolverlo en 3-4 pasos reales. Ejemplo del defecto actual
   (`03.07 MAT.ALG.MCD_ALGEBRAICO.CONCEPTO_MCD`): *"Simplifica o resuelve la expresión aplicando
   concepto de m.c.d. algebraico"* — sin expresión que simplificar.
2. **`al_terminar_debes_poder`** (365 recursos, 100%): 1-2 frases con la meta de aprendizaje.
3. **`afirmaciones_verdaderas`** (365 recursos, 100%): agregar hasta llegar a mínimo 2
   afirmaciones ciertas, breves y verificables (hoy casi todos tienen solo 1).
4. Cargar en DB local (`load_node_content`) y crear una migración de datos nueva, siguiendo el
   patrón de las migraciones `0052`-`0070`.

## No-objetivos (qué queda FUERA)
- ❌ No tocar `errores_frecuentes` ni `ejemplos` — ya están correctos en el 100% de este grupo.
- ❌ No tocar `checkpoints` (correcto en el 100%).
- ❌ No rediseñar la estructura de 12 secciones ni el modelo `NodeContent`.
- ❌ No es un script/migración de datos automática para `ejemplo_guiado` — requiere redacción
  humana o de IA supervisada, recurso por recurso.

## Criterios de aceptación (verificables)
- [ ] Barrera verde: `test` · `check` · `makemigrations --check --dry-run`
- [ ] Script de verificación (adaptar `scratch/audit_antigravity_12secciones.py`) da 0 fallas
      para los 365 recursos de `03.01`–`03.09` en los 3 campos de la tabla de la auditoría.
- [ ] `ejemplo_guiado.enunciado` de cada recurso contiene una expresión algebraica o datos
      concretos (no solo el nombre del recurso).
- [ ] Migración de datos nueva creada, aplicada en local y desplegada.

## Plan de pruebas
- Verificación DB con script adaptado de la auditoría (0 fallas en los 3 campos).
- Lectura manual de una muestra (5-10 recursos) para confirmar que `ejemplo_guiado` resuelve un
  problema real y no repite el patrón de plantilla detectado.
- Suite completa (`python manage.py test`) antes de pushear, según regla del proyecto.

## Riesgos / rollback
- Riesgo de reintroducir el mismo patrón de plantilla si se generan los 365 en lote con IA sin
  supervisión — por eso el dueño sugerido es redacción cuidada, no un script masivo.
- Rollback: migración de datos revertible (recarga desde YAML anterior si se versiona el diff).

---

## Qué se hizo
_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_
