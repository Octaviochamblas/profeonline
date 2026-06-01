# Analytics y eventos de conversión (medir para dejar de ir a ciegas)

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** Producto / Negocio
- **Prioridad:** 🟡 Media-alta

## Problema / Objetivo

Hoy no hay analítica (PEND-015). No sabemos qué recursos se ven, dónde abandona la gente,
cuántos se registran ni cuántos hacen clic en WhatsApp. Sin esos datos, cualquier mejora de
diseño o contenido es a ciegas.

Objetivo: instalar una analítica **respetuosa con la privacidad** (compatible con nuestras
páginas legales y la CSP por nonce) y definir los eventos de conversión clave.

## Diagnóstico / contexto técnico

- **CSP con nonce** (`apps/core/middleware.py`): cualquier script de analítica debe respetar
  la política. Plausible/Umami se cargan como `<script>` externo simple (encaja bien;
  añadir el dominio a `script-src`/`connect-src`).
- **Páginas legales existentes** (términos, privacidad): habrá que mencionar la analítica si
  recopila datos, aunque sea sin cookies.
- **Puntos de conversión ya presentes** en el código:
  - Registro (`accounts/`), login con Google.
  - Botones de WhatsApp (`base.html`: barra superior y CTA inferior, `wa.me/56937503803`).
  - `tel:` (llamar directamente).
  - Apertura de recurso, video reproducido, descarga de adjunto.
  - `ResourceCompletion` (recurso completado) — ya medible internamente.

## Decisión abierta: ¿qué herramienta?

- **Plausible / Umami (recomendado):** sin cookies, ligero, sin banner de consentimiento,
  alineado con educación y privacidad de menores.
- **GA4:** más potente pero pesado, requiere banner de cookies y consentimiento.
- **Solo métricas internas (hoy mucho más viable):** ya existe un ledger rico —
  `ResourceView`, `ResourceCompletion`, `QuizAttempt`, `TopicEvaluationAttempt`, `XPEvent`,
  `UserSkill`, `UserStreak` — para un mini dashboard propio (sin terceros). Cero dependencias
  externas y sin temas de privacidad; falta solo la vista/panel. Buena opción de bajo costo.

## Ruta de trabajo

### Fase 1 — Definir qué medir (antes de instalar nada)
- Lista de eventos de conversión (actualizada — el quiz y la gamificación **ya existen**):
  - `signup` (registro completado), `login_google`.
  - `whatsapp_click`, `phone_click`.
  - `resource_view`, `video_play`, `attachment_download`.
  - `resource_comprendido` (antes "completado"; `ResourceCompletion`).
  - **Evaluación/gamificación (ya implementado):** `quiz_passed` (nivel de recurso aprobado),
    `topic_exam_passed` (evaluación final de tema), `skill_unlocked`, hitos de XP/rango y racha.
- Definir 1–2 "métricas norte" (ej.: registros/semana, clics a WhatsApp).

### Fase 2 — Elegir e instalar la herramienta
- Decidir Plausible/Umami vs interno.
- Añadir el snippet respetando la CSP (incluir dominio en las directivas).
- Verificar que carga sin violar CSP (revisar consola y Sentry).

### Fase 3 — Instrumentar eventos
- Marcar los clics de WhatsApp/teléfono y aperturas de recurso.
- Validar que los eventos llegan al panel.

### Fase 4 — Privacidad y legal
- Actualizar la política de privacidad mencionando la analítica y qué se recoge.
- Confirmar que no se usan cookies (o añadir consentimiento si la herramienta las usa).

## Criterios de aceptación

- La analítica registra visitas y los eventos de conversión definidos.
- No hay violaciones de CSP en consola por el script.
- La política de privacidad refleja la herramienta usada.
- Existe un panel donde ver registros, clics a WhatsApp y recursos más vistos.

## Notas / Consideraciones

- No instalar analítica "porque sí": primero definir eventos (Fase 1).
- Esta medición es **prerrequisito** para evaluar el impacto del rediseño del home.

---

## Qué se hizo
_(Completar al finalizar, antes de mover a "3 Finalizados".)_
