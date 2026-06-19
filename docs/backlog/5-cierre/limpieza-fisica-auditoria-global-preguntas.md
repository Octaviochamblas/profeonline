# Limpieza física y auditoría global del banco de preguntas

- **Estado:** Implementado y verificado · pendiente cierre
- **Creado:** 2026-06-19
- **Prioridad:** P1  ·  **Cartera:** educativa
- **Tipo:** QA · datos
- **Dueño sugerido:** 🧩 Codex

## Objetivo (una frase)
Eliminar físicamente las preguntas archivadas sin historial y auditar similitudes estructurales del banco activo sin borrar preguntas válidas automáticamente.

## Fuentes a leer (rutas concretas)
- `apps/content/models/question.py`
- `apps/content/models/evaluation.py`
- `apps/content/models/error_report.py`
- `scratch/curate_racionales_questions.py`

## Propuesta
Respaldar las preguntas archivadas con alternativas e identificadores, confirmar que no tengan
respuestas ni reportes, borrarlas en una transacción y exportar la auditoría del banco activo a
Markdown y JSON.

## No-objetivos (qué queda FUERA)
- Eliminar automáticamente preguntas activas por similitud estructural.
- Modificar niveles, modos, estados o alternativas de preguntas activas.

## Criterios de aceptación (verificables)
- [x] Respaldo legible de 1.351 preguntas archivadas.
- [x] Cero preguntas archivadas tras la limpieza.
- [x] 2.476 preguntas activas, sin cambios de conteo por recurso.
- [x] Cero respuestas históricas o reportes eliminados.
- [x] Cero alternativas huérfanas.
- [x] Informes Markdown y JSON con los grupos estructurales.
- [x] Producción responde HTTP 200.

## Plan de pruebas
Dry-run contra producción, validación de dependencias, transacción atómica, conteos antes/después,
integridad referencial y smoke HTTP.

## Riesgos / rollback
El borrado es irreversible en la base viva. El respaldo JSON completo se crea antes de abrir la
transacción y la operación se aborta si existe cualquier respuesta o reporte asociado.

---

## Qué se hizo
- Se creó `scratch/cleanup_archived_questions.py` con dry-run, conteos esperados, guardas de
  dependencias, respaldo JSON y confirmación explícita para producción.
- Se respaldaron 1.351 preguntas archivadas y 5.404 alternativas en
  `backups/archived_questions_before_delete_20260619T162832Z.json`.
- Se eliminaron físicamente las 1.351 preguntas archivadas dentro de una transacción. No existían
  respuestas de alumnos ni reportes asociados.
- Se auditaron las 2.476 preguntas activas: 0 duplicados textuales y 43 grupos estructuralmente
  similares que reúnen 812 preguntas. No se eliminó ninguna pregunta activa.
- Evidencia: `docs/auditorias/2026-06-19-auditoria-global-preguntas.md` y `.json`.
- Verificación final: 2.476 activas, 0 archivadas, 0 alternativas huérfanas y HTTP 200.
