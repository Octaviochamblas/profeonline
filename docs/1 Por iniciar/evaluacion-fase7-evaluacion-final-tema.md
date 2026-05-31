# Evaluación gamificada · Fase 7 — Evaluación final por tema

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** Producto pedagógico / Gamificación
- **Origen:** Fase 7 de la épica `sistema-evaluacion-gamificada` (MVP Fases 1–6 ya entregado y
  en `3 Finalizados/`).
- **Prioridad:** Media-alta (es el siguiente escalón natural sobre el MVP de evaluación por
  recurso).

## Problema / Objetivo

El MVP evalúa **por recurso y nivel** (1/2/3, 5/5 para aprobar). Falta la capa de cierre por
**tema**: una evaluación final que compile el dominio del alumno sobre todos los recursos del
`Topic`, registre nota e intentos, y traduzca la aprobación en señal visual y recompensa.

## Propuesta

- Crear evaluación final asociada a `Topic` (modelo nuevo o reutilizar `Question` con un modo
  `evaluacion_tema`, ya previsto en el MVP).
- Tomar preguntas de los recursos del tema o preguntas específicas de tema.
- Guardar por intento: nota/porcentaje, número de intento, mejor nota, aprobado/no aprobado,
  fecha.
- Umbral de aprobación recomendado: **80%**.
- Al aprobar:
  - marcar el tema como aprobado y aplicar color verde en `topic_detail` / listados;
  - aumentar el brillo/resplandor del tema según la nota (sin volver la UI ruidosa);
  - desbloquear la **skill** del tema (engancha con Fase 8);
  - otorgar XP (engancha con Fase 8).
- UI en `topic_detail`: bloque de "Evaluación final del tema" con estado, mejor nota e intentos.

## Notas / Consideraciones

- El modo `evaluacion_tema` ya está contemplado en el modelado del MVP — revisar
  `apps/content/models/question.py` y `evaluation.py` antes de añadir modelos nuevos.
- Depende parcialmente de Fase 8 para XP/skills; se puede entregar primero la mecánica de
  nota/intentos/estado verde y conectar XP/skill cuando exista la Fase 8.
- Mantener accesibilidad: estado del tema no solo por color (texto + icono).
- Tests: nota/intentos persistidos, umbral 80%, transición de tema a aprobado, idempotencia de
  recompensas (no duplicar skill/XP al reaprobar).

---

## Qué se hizo
_(Completar al finalizar, antes de mover a "3 Finalizados".)_
