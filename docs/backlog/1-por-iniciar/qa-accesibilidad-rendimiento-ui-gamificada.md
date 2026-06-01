# QA de accesibilidad y rendimiento de la UI gamificada nueva

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** Accesibilidad / Rendimiento / QA
- **Prioridad:** 🟡 Media

## Problema / Objetivo

Las auditorías de **accesibilidad (axe)** y **rendimiento (Lighthouse)** se cerraron
(`backlog/3-finalizados/auditoria-accesibilidad-axe.md`, `...-rendimiento-seo-lighthouse.md`) **antes**
de construir toda la UI de evaluación gamificada. Esa UI nueva **nunca pasó por QA manual de
teclado/lector de pantalla** ni por una re-medición de rendimiento contra producción.

Objetivo: cerrar ese hueco con una pasada manual acotada sobre lo nuevo, sin reabrir las
auditorías originales.

## Alcance (UI agregada desde el cierre de las auditorías)

- **Quiz / evaluación** (`quiz_section.html`, niveles, práctica vs evaluación, feedback HTMX,
  reporte de error por pregunta).
- **Examen final de tema** (`topic_exam*`).
- **Barra de acciones del recurso** (Ir a Ejercitación / Evaluación / Marcar como comprendido).
- **Barras de progreso** (tarjetas de tema `_topic_card.html` y panel multibarra de
  `topic_detail.html`).
- **Panel de gamificación del perfil** (XP, rango, skills, racha).
- **Página de nivel reestructurada** (Asignaturas/Temas + buscador) — cuando se mergee
  `correcciones-visuales-recurso-tema-nivel.md`.

## Ruta de trabajo

### Fase 1 — Accesibilidad manual (lo que axe automático no cubre)
- **Teclado:** navegar y operar todo el flujo de quiz/evaluación sin mouse (foco visible, orden
  lógico, enviar respuestas, abrir/cerrar feedback, reportar error).
- **Lector de pantalla (NVDA en Windows):** que las barras (`role="progressbar"` +
  `aria-valuenow`) se anuncien bien; que badges Visto/Comprendido/Aprobado/estrellas tengan
  texto, no solo color; que el buscador de temas tenga `label`/`aria-label`.
- **Contraste AA** de los estados nuevos (verde `--success`, ámbar CTA, barras) en tema claro.
- Re-correr **axe** sobre `/recursos/<r>/`, `/temas/<t>/`, `/niveles/<n>/` y `/cuentas/perfil/`.

### Fase 2 — Rendimiento (re-medición)
- Re-medir **Lighthouse/PageSpeed contra producción** tras el CSS/DOM nuevo (barras, panel,
  página de nivel). Confirmar que no se degradó LCP/CLS ni el peso del CSS.
- Revisar que el cache-buster del CSS esté al día y que WhiteNoise comprima en prod.

## Criterios de aceptación
- Todo el flujo de quiz/evaluación es operable solo con teclado, con foco visible.
- NVDA anuncia correctamente barras de progreso, estados y el buscador.
- Sin flancos de contraste AA en los estados nuevos.
- Lighthouse/PageSpeed en prod sin regresión relevante vs. la medición previa.

## Notas / Consideraciones
- Es **QA manual** (no automatizable acá): requiere navegador + NVDA en Windows del usuario.
- No reabrir las auditorías viejas; esta tarjeta solo cubre el delta de UI gamificada.
- Si aparecen fixes, hacerlos en rama propia → PR → CI verde, como siempre.

---

## Qué se hizo
_(Completar al finalizar, antes de mover a "3 Finalizados".)_
