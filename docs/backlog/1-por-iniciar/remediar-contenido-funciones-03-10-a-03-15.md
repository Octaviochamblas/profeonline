# Remediar contenido de 12 secciones — Funciones (03.10–03.15)

- **Estado:** Por iniciar
- **Creado:** 2026-08-05
- **Nota 2026-08-05 (noche):** `al_terminar_debes_poder` salió del alcance — era un typo de
  clave (`_ponder`→`_poder`), ya corregido globalmente sin necesitar redacción. Quedan 3 campos,
  no 4.
- **Prioridad:** P1 · **Cartera:** educativa
- **Tipo:** pedagogía
- **Dueño sugerido:** 🏛️ Claude (redacción manual; no automatizable con plantilla — ver "Propuesta")

## Objetivo (una frase)
Completar los campos obligatorios de `NodeContent` que quedaron incompletos o genéricos en los
333 recursos de `03.10` a `03.15` (Funciones, Ecuaciones de Segundo Grado, Función Cuadrática,
Funciones Exponencial/Logarítmica, Función Potencia, Función Trigonométrica).

## Fuentes a leer (rutas concretas)
- `docs/auditorias/2026-08-05-auditoria-contenido-12-secciones.md` — auditoría completa (causa
  raíz, metodología, hallazgos).
- `docs/auditorias/2026-08-05-auditoria-contenido-12-secciones.json` — lista exacta de los 333
  `semantic_id` de este grupo con sus campos faltantes (`"nodo"` entre `03.10` y `03.15`).
- `docs/conocimiento/pauta-contenido.md` — estándar de 12 secciones, tabla "Campos obligatorios".
- `docs/conocimiento/contenido/*.yaml` — YAML fuente por recurso (buscar por `semantic_id`).
- `apps/content/management/commands/load_node_content.py` — loader (mapeo de campos, sin bugs).

## Propuesta
Por cada uno de los 333 recursos (lista exacta en el JSON de la auditoría), editar su YAML fuente
para completar, **sin plantilla genérica** (esa es justamente la causa del problema actual):

1. **`ejemplo_guiado`** (309 de 333, 78-100% según nodo): redactar un problema concreto con datos
   propios (función/ecuación específica con coeficientes reales, no el nombre del recurso pegado
   en una frase molde) y resolverlo en 3-4 pasos reales.
2. **`afirmaciones_verdaderas`** (333 recursos, 100%): agregar hasta llegar a mínimo 2
   afirmaciones ciertas, breves y verificables (hoy todos tienen solo 1).
3. **`errores_frecuentes`** (330 de 333): completar hasta exactamente 5 afirmaciones falsas.
4. Cargar en DB local (`load_node_content`) y crear una migración de datos nueva, siguiendo el
   patrón de las migraciones `0052`-`0070`.

## No-objetivos (qué queda FUERA)
- ❌ No tocar `ejemplos` — ya está correcto (mínimo 4) en el 100% de este grupo.
- ❌ No tocar `checkpoints` (correcto en el 100%).
- ❌ No rediseñar la estructura de 12 secciones ni el modelo `NodeContent`.
- ❌ No es un script/migración de datos automática para `ejemplo_guiado` — requiere redacción
  humana o de IA supervisada, recurso por recurso.

## Criterios de aceptación (verificables)
- [ ] Barrera verde: `test` · `check` · `makemigrations --check --dry-run`
- [ ] Script de verificación (adaptar `scratch/audit_antigravity_12secciones.py`) da 0 fallas
      para los 333 recursos de `03.10`–`03.15` en los 3 campos de la tabla de la auditoría.
- [ ] `ejemplo_guiado.enunciado` de cada recurso contiene datos numéricos/coeficientes concretos
      (no solo el nombre del recurso).
- [ ] Migración de datos nueva creada, aplicada en local y desplegada.

## Plan de pruebas
- Verificación DB con script adaptado de la auditoría (0 fallas en los 3 campos).
- Lectura manual de una muestra (5-10 recursos) para confirmar que `ejemplo_guiado` resuelve un
  problema real y no repite el patrón de plantilla detectado.
- Suite completa (`python manage.py test`) antes de pushear, según regla del proyecto.

## Riesgos / rollback
- Riesgo de reintroducir el mismo patrón de plantilla si se generan los 333 en lote con IA sin
  supervisión — por eso el dueño sugerido es redacción cuidada, no un script masivo.
- Rollback: migración de datos revertible (recarga desde YAML anterior si se versiona el diff).

---

## Qué se hizo
_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_
