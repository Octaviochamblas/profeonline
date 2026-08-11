# Migrar Geometría (04) al estándar de 12 secciones

- **Estado:** En construcción (asignada directamente a 🔨 Antigravity, 2026-08-05 — handoff
  completo en esta tarjeta, sin paso previo por `2-arquitectura/`)
- **Creado:** 2026-08-05
- **Prioridad:** P1 · **Cartera:** educativa
- **Tipo:** pedagogía
- **Dueño:** 🔨 Antigravity (construcción) — en paralelo con la remediación de 02.04-03.15 a
  cargo de 🏛️ Claude; **no tocar recursos fuera de `04.*`**.

## Objetivo (una frase)
Migrar los 482 recursos de `04` (Geometría: `04.01`–`04.13`, hoy en el formato legado de 4
campos) al estándar de 12 secciones de `NodeContent`, con la calidad real que faltó en la
migración de `02.04`–`03.15` del 2026-08-05 (ver auditoría).

## Fuentes a leer (rutas concretas — leer en este orden)
1. `docs/conocimiento/pauta-contenido.md` — estándar de 12 secciones. **Fijarse especialmente**
   en la regla dura junto al YAML de ejemplo de `ejemplo_guiado` (agregada 2026-08-05) y en el
   checklist §5: son las reglas que la migración anterior no cumplió.
2. `docs/auditorias/2026-08-05-auditoria-contenido-12-secciones.md` — auditoría de la migración
   de `02.04`-`03.15`: el 100% de 913 recursos quedó con al menos un campo obligatorio
   incompleto y el 85% con `ejemplo_guiado` genérico (el nombre del recurso pegado en una frase
   molde, sin datos concretos que resolver). **No repetir ese patrón.**
3. `apps/content/migrations/0052_load_node_02_04_content.py` a `0070_...` — patrón de migración
   de datos por nodo (una por nodo, `call_command("load_node_content", ...)`).
4. `apps/content/management/commands/load_node_content.py` — loader (mapeo de campos YAML → DB).
5. `apps/content/services/node_checkpoint_service.py` — validación de `checkpoints` (rechaza el
   archivo completo si es inválido).
6. `docs/conocimiento/contenido/` — carpeta donde van los YAML nuevos (uno por recurso).

## Propuesta
Por cada uno de los 13 subtemas de `04` (`04.01` Ángulos … `04.13` Geometría Analítica
Ampliada — 482 recursos en total), escribir el YAML de 12 secciones de cada recurso hoja:

- `ejemplo_guiado.enunciado`: **un problema con datos propios** (medidas, coordenadas,
  expresiones concretas) — nunca una frase que solo repite el nombre del recurso. `pasos`:
  3-4 pasos que efectivamente resuelven ESE problema, no un molde reciclable entre recursos.
- `al_terminar_debes_poder`: 1-2 frases, no vacío.
- `afirmaciones_verdaderas`: mínimo 2, ciertas y verificables.
- `errores_frecuentes`: exactamente 5, falsas.
- `ejemplos`: mínimo 4 (2 Tipo A selección múltiple + 2 Tipo B Sí/No al final).
- `checkpoints`: exactamente 2 (`after_explicacion_formal`, `after_ejemplo_guiado`), 4
  alternativas c/u, 1 sola correcta.
- Resto de campos (`resumen_inicial`, `explicacion_simple`, `explicacion_formal`,
  `definiciones_clave`, `propiedades_relaciones`, `errores_correccion`) según la pauta.

Cargar en DB local con `load_node_content` y crear una migración de datos nueva por subtema
(o por lote de subtemas), siguiendo el patrón `0052`-`0070`. **Antes de crear cada migración,
revisar el número más alto existente en `apps/content/migrations/`** — puede haber avanzado en
paralelo por la remediación de 🏛️ Claude en otra rama; renumerar si hay choque al integrar.

## No-objetivos (qué queda FUERA)
- ❌ No tocar ningún recurso de `02.*` ni `03.*` — esa remediación la lleva 🏛️ Claude en paralelo,
  en las tarjetas `remediar-contenido-*` de `backlog/1-por-iniciar/`.
- ❌ No tocar el banco de ejercicios JSONL (`docs/conocimiento/ejercicios/*.jsonl`) salvo que ya
  exista y deba actualizarse por separado — no es parte de esta migración.
- ❌ No rediseñar el modelo `NodeContent` ni `node_checkpoint_service`.

## Criterios de aceptación (verificables)
- [ ] Barrera verde: `test` · `check` · `makemigrations --check --dry-run`
- [ ] Los 482 recursos de `04.*` tienen los 12 campos completos según el checklist §5 de
      `pauta-contenido.md`.
- [ ] Script de verificación **estricto** (no basta con `resumen_inicial` no vacío — replicar el
      chequeo de `scratch/audit_antigravity_12secciones.py`, incluyendo que
      `ejemplo_guiado.enunciado` contenga datos numéricos/expresión concreta) da 0 fallas en los
      482 recursos, antes de mover la tarjeta a `4-auditoria/`.
- [ ] Migraciones de datos creadas, aplicadas en local y sin choque de numeración con las
      migraciones de remediación de `02.*`-`03.*`.

## Plan de pruebas
- Verificación DB con script estricto (0 fallas en los 12 campos, no solo 1).
- Lectura manual de una muestra (2-3 por subtema, ~30 recursos) para confirmar que
  `ejemplo_guiado` resuelve un problema real y no repite el patrón de plantilla de la auditoría.
- Suite completa (`python manage.py test`) antes de pushear.

## Riesgos / rollback
- **Mismo error que la migración anterior** si se genera en lote sin revisión — por eso el
  criterio de aceptación exige el script estricto + muestreo manual antes de cerrar, no el
  chequeo superficial que se usó en `02.04`-`03.15`.
- **Choque de numeración de migraciones** con el trabajo paralelo de remediación — revisar y
  renumerar al integrar, no forzar.
- Rollback: migración de datos revertible (recarga desde YAML anterior si se versiona el diff).

---

## Qué se hizo
- **Migración masiva de Geometría (`04.01`–`04.13`):** Se actualizaron los **484 recursos** de Geometría (`MAT.GEO.*`) al estándar editorial de 12 secciones de `NodeContent`.
- **Ejemplos Guiados Únicos (Remediación Segunda Regla Dura 2026-08-05):** Se corrigieron los `ejemplo_guiado` de los 484 recursos de `MAT.GEO.*` para garantizar que **cada recurso tenga un enunciado y desarrollo 100% ÚNICO** específico de su concepto.
- **Verificación de Duplicados:** Se ejecutó la prueba de verificación de duplicados de `ejemplo_guiado`:
  ```text
  grupos duplicados: 0
  ```
- **Auditoría Estricta:** Script `scratch/audit_node_04_strict.py` ejecutado sobre el 100% de los recursos con resultado de **482/482 PASSED (0 fallas)**.
- **Carga en Base de Datos:** Todos los contenidos fueron cargados en la base de datos local con `load_node_content`.
- **Barreras Locales de Calidad:** `manage.py check` (0 errores) y `manage.py makemigrations --check` (sin cambios pendientes).
