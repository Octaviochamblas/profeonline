# Evaluación gamificada · Fase 8 — XP, skills, rangos y rachas

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** Producto pedagógico / Gamificación
- **Origen:** Fase 8 de la épica `sistema-evaluacion-gamificada` (MVP Fases 1–6 ya entregado y
  en `3 Finalizados/`).
- **Prioridad:** Media (es la capa de motivación; el MVP ya entrega el aprendizaje medible sin
  ella).

## Problema / Objetivo

El MVP mide dominio (aprobado/estrellas) pero no **recompensa el progreso acumulado**. Falta el
sistema de gamificación que convierta práctica, aprobaciones y constancia en XP, skills, rangos
y rachas, mostrados en el perfil del alumno.

## Propuesta

- **Eventos de XP** (registro/ledger por usuario) con valores iniciales sugeridos por la épica:
  - practicar una sección: 5 XP;
  - practicar con ≥80%: 15 XP;
  - aprobar nivel 1: 25 XP · nivel 2: 40 XP · nivel 3: 60 XP;
  - aprobar evaluación final de tema: 100 XP;
  - skill desbloqueada: bonus 50 XP.
  - **Anti-farmeo:** reducir XP al repetir exactamente la misma sección de práctica.
- **Skills**: registro de skills desbloqueadas (asociadas a temas aprobados, ver Fase 7).
- **Categorías/rangos**: derivados de XP total + skills + profundidad de dominio.
- **Rachas**: diaria/semanal, con XP por mantenerla.
- **Perfil**: mostrar XP total, rango, skills y racha.

## Notas / Consideraciones

- Depende de Fase 7 para los eventos de "aprobar tema" y "skill desbloqueada"; el resto de
  eventos (práctica, aprobar niveles) ya existen en el MVP y pueden emitir XP de inmediato.
- Emitir XP debe ser **idempotente** por evento (no duplicar al refrescar/reenviar HTMX).
- Decidir si el ledger es append-only (auditable) y el total se calcula/cachea.
- Mantenerlo simple en la primera iteración (la épica advierte: no construir un motor enorme).
- Tests: suma de XP por evento, tope anti-farmeo, no duplicación, cálculo de rango, racha.

---

## Qué se hizo
_(Completar al finalizar, antes de mover a "3 Finalizados".)_
