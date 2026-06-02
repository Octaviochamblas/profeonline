# Cola Claude — Cierres pendientes

Esta cola acumula tareas que Claude debe revisar cuando vuelva a estar disponible.

## Criterios de entrada

Un PR/tarea entra aquí si:

- tiene `seguridad:requiere-claude`;
- toca settings, auth, webhooks, permisos, CI/CD o workflows;
- cambia arquitectura/gobernanza;
- requiere decisión pedagógica/producto;
- ya tiene `audit:aprobado`, pero falta cierre final, matriz, reporte o movimiento a finalizados.

## Pendientes actuales

| Fecha | PR/Tarea | Motivo | Estado |
| --- | --- | --- | --- |
| _sin pendientes registrados manualmente_ | — | — | — |

## Protocolo de Claude

1. Leer PR/tarea.
2. Revisar auditoría de Codex.
3. Validar riesgos de arquitectura/seguridad/producto.
4. Actualizar documentación de gobernanza si aplica.
5. Mover tarjeta a `6-finalizados`.
6. Cerrar con squash-merge si corresponde y CI está verde.
