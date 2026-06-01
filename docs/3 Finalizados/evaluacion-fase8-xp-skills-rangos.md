# Evaluación gamificada · Fase 8 — XP, skills, rangos y rachas

- **Estado:** Finalizado
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
- Se crearon los modelos `XPEvent`, `UserSkill` y `UserStreak` en `apps/content` con migracion
  `0019_userstreak_xpevent_userskill`.
- Se agrego un ledger de XP idempotente mediante `event_key` para evitar duplicados por refrescos
  o reenvios HTMX.
- Se implementaron recompensas iniciales:
  - practica: 5 XP;
  - practica con 80% o mas: 15 XP;
  - repeticion de la misma seccion desde el cuarto intento: XP reducido anti-farmeo;
  - aprobar nivel 1/2/3: 25/40/60 XP una sola vez;
  - aprobar evaluacion final de tema: 100 XP una sola vez;
  - desbloquear skill de tema: bonus 50 XP una sola vez;
  - continuar racha diaria: bonus 10 XP.
- Se conecto la gamificacion a `submit_quiz()` y `submit_topic_exam()` para emitir XP, rachas y
  skills desde los flujos reales de evaluacion.
- Se agregaron rangos calculados por XP + skills: Explorador, Aprendiz, Practico, Avanzado y
  Experto.
- Se agrego resumen gamificado al perfil: XP total, rango, skills, racha actual y mejor racha.
- Se agrego administracion read-only para eventos XP, skills y rachas.
- Se agregaron tests para XP por practica, anti-farmeo, idempotencia, skill por tema, rango,
  racha y visualizacion en perfil.

## Verificacion

- `python manage.py test apps.content.tests.test_evaluation`: 60/60 OK.
- `python manage.py test`: 147/147 OK.
- `python manage.py check`: OK.
- `python manage.py makemigrations --check --dry-run`: sin cambios pendientes.
