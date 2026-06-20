# Auditoría editorial persistente por recurso

- **Estado:** finalizada y desplegada el 20 de junio de 2026.
- **Prioridad:** P1.
- **Cartera:** contenido educativo / operaciones.
- **Responsable:** Codex.

## Objetivo

Permitir que el panel del banco de preguntas indique de forma verificable si cada
recurso tiene transcripción y si sus títulos y descripciones fueron auditados en la
web y en YouTube.

## Qué se hizo

- Se añadió `Resource.editorial_audit` como registro JSON persistente y extensible.
- Se migró el inventario publicado usando la auditoría global del 20 de junio.
- El panel de cobertura muestra cinco marcas, estado agregado, métricas y filtro.
- Las ediciones posteriores invalidan las marcas que dejan de ser confiables.
- El cierre del pipeline editorial registra automáticamente una auditoría completa.
- Se documentó y versionó la evidencia global de los 111 recursos.

## Criterios verificados

- [x] Transcripción disponible y auditada.
- [x] Título y descripción web auditados.
- [x] Título y descripción YouTube auditados.
- [x] Estado pendiente visible por componente.
- [x] Filtro y métricas actualizados en el navegador.
- [x] Invalidación automática ante cambios editoriales.
- [x] Backfill idempotente mediante migración aditiva.
- [x] 32 pruebas focalizadas aprobadas.
- [x] Staging y producción desplegados correctamente.

## Resultado en producción

Al finalizar el despliegue:

- recursos en el panel: 111;
- auditoría completa: 111;
- auditoría pendiente: 0.
