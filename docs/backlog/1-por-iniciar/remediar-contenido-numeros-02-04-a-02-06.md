# Remediar contenido de 12 secciones — Números (02.04–02.06)

- **Estado:** Por iniciar
- **Creado:** 2026-08-05
- **Prioridad:** P1 · **Cartera:** educativa
- **Tipo:** pedagogía
- **Dueño sugerido:** 🏛️ Claude (redacción manual; no automatizable con plantilla — ver "Propuesta")

## Objetivo (una frase)
Completar los campos obligatorios de `NodeContent` que quedaron incompletos o genéricos en los
215 recursos de `02.04` (Reales, Potencias, Raíces y Logaritmos), `02.05` (Razones, Proporciones,
Porcentajes y Finanzas) y `02.06` (Sucesiones y Progresiones), el peor tramo de la migración del
2026-08-05: es el único grupo de nodos con las 5 fallas a la vez.

## Fuentes a leer (rutas concretas)
- `docs/auditorias/2026-08-05-auditoria-contenido-12-secciones.md` — auditoría completa (causa
  raíz, metodología, hallazgos).
- `docs/auditorias/2026-08-05-auditoria-contenido-12-secciones.json` — lista exacta de los 215
  `semantic_id` de este grupo con sus campos faltantes (`"nodo": "02.04"` / `"02.05"` / `"02.06"`).
- `docs/conocimiento/pauta-contenido.md` — estándar de 12 secciones, tabla "Campos obligatorios".
- `docs/conocimiento/contenido/*.yaml` — YAML fuente por recurso (buscar por `semantic_id`).
- `apps/content/management/commands/load_node_content.py` — loader (mapeo de campos, sin bugs).
- `apps/content/services/node_checkpoint_service.py` — validación de `checkpoints` (ya correcto,
  no tocar salvo que se detecte regresión).

## Propuesta
Por cada uno de los 215 recursos (lista exacta en el JSON de la auditoría), editar su YAML fuente
para completar, **sin plantilla genérica** (esa es justamente la causa del problema actual):

1. **`ejemplo_guiado`** (215 recursos en `02.05`/`02.06`; `02.04` ya está bien — no tocar):
   redactar un problema concreto con datos propios (números reales, no el nombre del recurso
   pegado en una frase molde) y resolverlo en 3-4 pasos reales. Ver el caso bueno de referencia:
   `MAT.NUM.RAZONES.DEFINICION_COCIENTE` ("15 hombres y 20 mujeres…").
2. **`al_terminar_debes_poder`** (215 recursos): 1-2 frases con la meta de aprendizaje.
3. **`afirmaciones_verdaderas`** (212 recursos, todos salvo 3 en `02.04`): agregar hasta llegar a
   mínimo 2 afirmaciones ciertas, breves y verificables.
4. **`errores_frecuentes`** (215 recursos): completar hasta exactamente 5 afirmaciones falsas.
5. **`ejemplos`** (215 recursos): completar hasta mínimo 4 (2 Tipo A selección múltiple + 2 Tipo B
   Sí/No), la mayoría hoy solo tiene 1.
6. Cargar en DB local (`load_node_content`) y crear una migración de datos nueva (siguiente número
   libre tras `0070`), siguiendo el patrón de las migraciones `0052`-`0070`.

## No-objetivos (qué queda FUERA)
- ❌ No tocar `checkpoints` (ya está correcto en el 100% de estos recursos).
- ❌ No rediseñar la estructura de 12 secciones ni el modelo `NodeContent`.
- ❌ No es un script/migración de datos automática para `ejemplo_guiado` — requiere redacción
  humana o de IA supervisada, recurso por recurso.

## Criterios de aceptación (verificables)
- [ ] Barrera verde: `test` · `check` · `makemigrations --check --dry-run`
- [ ] Script de verificación (adaptar `scratch/audit_antigravity_12secciones.py`) da 0 fallas
      para los 215 recursos de `02.04`–`02.06` en los 5 campos de la tabla de la auditoría.
- [ ] `ejemplo_guiado.enunciado` de cada recurso de `02.05`/`02.06` contiene datos numéricos o una
      expresión concreta (no solo el nombre del recurso).
- [ ] Migración de datos nueva creada, aplicada en local y desplegada.

## Plan de pruebas
- Verificación DB con script adaptado de la auditoría (0 fallas en los 5 campos).
- Lectura manual de una muestra (5-10 recursos) para confirmar que `ejemplo_guiado` resuelve un
  problema real y no repite el patrón de plantilla detectado.
- Suite completa (`python manage.py test`) antes de pushear, según regla del proyecto.

## Riesgos / rollback
- Riesgo de reintroducir el mismo patrón de plantilla si se generan los 215 en lote con IA sin
  supervisión — por eso el dueño sugerido es redacción cuidada, no un script masivo.
- Rollback: migración de datos revertible (recarga desde YAML anterior si se versiona el diff).

---

## Qué se hizo
_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_
