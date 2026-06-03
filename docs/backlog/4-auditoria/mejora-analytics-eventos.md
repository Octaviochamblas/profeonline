# M5 — Analítica interna y eventos de conversión

> 🏛️ **Handoff de arquitectura (Claude, 2026-06-02).** Decisión cerrada con 🧑 Usuario:
> **panel interno propio** (sin terceros). Se descarta Plausible/Umami para no añadir infra ni
> dependencias externas (coherente con haber descartado C1/C2) y por privacidad (público posible
> menor de edad). Mitiga el riesgo **M5** de `../../gobernanza/matriz-riesgos.md`.
> Es **prerrequisito** del rediseño del home (medir el "antes/después"): `rediseno-home-confianza.md`.

- **Estado:** 🏛️→🔨 Ready para construir
- **Creado:** 2026-05-31 · **Handoff:** 2026-06-02
- **Prioridad:** 🟡 Media-alta · **Cartera:** producto / negocio (medición)
- **Tipo:** feature (backend + JS mínimo + dashboard staff)
- **Dueño sugerido:** 🔨 Antigravity (construye) → 🧩 Codex (audita) → 🏛️ Claude (cierre)

## Objetivo (una frase)
Medir visitas y los **eventos de conversión clave** con un panel **propio** (sin terceros, sin
cookies), reutilizando el ledger ya existente, para dejar de decidir a ciegas.

## Contexto
- Hoy no hay analítica (PEND-015): no sabemos qué se ve, dónde se abandona, cuántos se registran
  ni cuántos hacen clic en WhatsApp.
- **Ya existe un ledger interno rico** que cubre ~80% server-side: `ResourceView`,
  `ResourceCompletion`, `QuizAttempt`, `TopicEvaluationAttempt`, `XPEvent`, `UserSkill`, `UserStreak`.
- **Falta** lo que ocurre en el cliente y no genera request propio: clics a **WhatsApp**
  (`wa.me/56937503803`) y **teléfono** (`tel:`), `video_play`, `attachment_download`, y pageviews
  de páginas no-recurso (p. ej. home).
- **CSP con nonce** (`apps/core/middleware.py`): cualquier `<script>` propio debe llevar el nonce
  por petición; nada de inline handlers.

## Decisión de diseño (cerrada)
**Panel interno propio**, NO herramienta externa. Razón: cero dependencias/costo, sin banner de
cookies, sin enviar datos de menores a terceros, y no pelea con la CSP. (Plausible Cloud = costo
recurrente; Umami self-host = más infra que mantener, justo lo que se evitó al descartar C1/C2.)

## Alcance (lo que SÍ entra)
1. **Modelo `AnalyticsEvent`** (en `apps/core` o app nueva `analytics`): `name` (validado por
   allowlist), `path`, `created_at`, `user` (FK nullable), `metadata` (JSON pequeño).
   **Sin IP, sin user-agent crudo, sin querystrings, sin PII.**
2. **Endpoint `POST` ligero** (p. ej. `/eventos/`) para eventos de cliente: valida `name` contra la
   **allowlist**, aplica **throttling**, responde `204`. Acepta anónimos. Sin efectos colaterales
   (solo INSERT).
3. **JS mínimo con nonce CSP** (`static/js/analytics.js`): instrumentar clics de WhatsApp / `tel:`,
   `video_play` y `attachment_download`. Usar `navigator.sendBeacon` (fallback `fetch`).
4. **Server-side**: registrar `signup` desde la vista de registro (sin JS); `resource_view` puede
   reutilizar el `ResourceView` ya existente.
5. **Dashboard solo-staff** (`/panel/analitica/` con `staff_member_required`, o una vista del
   AdminSite): registros/semana, clics WhatsApp/tel, recursos más vistos y un embudo básico —
   **agregando el ledger existente + los eventos nuevos** (no duplicar lo que ya está medido).
6. **Privacidad/legal**: actualizar la política de privacidad (analítica propia, sin cookies de
   terceros).

## Allowlist de eventos (v1)
`signup`, `login_google`, `whatsapp_click`, `phone_click`, `resource_view`, `video_play`,
`attachment_download`, `resource_comprendido`.
La gamificación (`quiz_passed`, `topic_exam_passed`, `skill_unlocked`, hitos de XP/rango/racha) **ya
vive en el ledger**; el dashboard la lee de ahí, **no se reinstrumenta**.

## Fuera de alcance
- Herramientas de terceros (Plausible / Umami / GA4). Cookies. Banner de consentimiento.
- Retención por cohortes / dashboards avanzados (v2). Tracking cross-device.

## Archivos a tocar (orientativo)
| Archivo | Cambio |
| --- | --- |
| `apps/core/models.py` (o app nueva `analytics`) | modelo `AnalyticsEvent` + migración |
| `apps/core/views.py` + `config/urls.py` | endpoint `POST` (allowlist + throttling) + vista dashboard staff |
| `static/js/analytics.js` (nuevo) | beacon de eventos de cliente, cargado con nonce |
| `templates/base.html` | data-hooks en botones WhatsApp/`tel:`; include del script con nonce |
| `templates/pages/resource_detail.html` | marcar `video_play` / `attachment_download` |
| `templates/.../panel_analitica.html` (nuevo) | dashboard staff |
| `templates/legal/` (privacidad) | mención de la analítica propia |
| tests | endpoint (allowlist/throttle), agregaciones del dashboard, sin violar CSP |

## Criterios de aceptación
- [ ] Evento de cliente se persiste **sin IP ni PII**; `user` opcional (anónimo por defecto).
- [ ] El endpoint **rechaza** nombres fuera de la allowlist y aplica **throttling** (con tests).
- [ ] El JS de tracking carga **con el nonce CSP**; **cero violaciones** en consola/Sentry.
- [ ] Dashboard **solo-staff** muestra registros/semana, clics WhatsApp/tel y recursos más vistos,
      reutilizando el ledger (sin duplicar `QuizAttempt`/`XPEvent`).
- [ ] Política de privacidad actualizada (sin cookies de terceros).
- [ ] **Suite completa verde** + `check --deploy`.

## Riesgos / rollback
- **Spam al endpoint** (público para anónimos): mitigar con allowlist + throttling + payload
  mínimo y sin efectos secundarios. Rollback: quitar el include del script y deshabilitar la URL.
- **Fuga de PII**: la allowlist y el esquema acotado lo previenen; **no** guardar IP ni querystrings.

## Checklist 🧩 Codex
- [ ] No se guarda PII/IP; `metadata` acotado. Allowlist real (no acepta nombres arbitrarios).
- [ ] Throttling efectivo; endpoint sin bypass inseguro de CSRF y sin efectos colaterales.
- [ ] El script respeta el nonce; no introduce inline-handlers que rompan la CSP.
- [ ] Dashboard restringido a staff. Tests cubren allowlist, throttle y agregación. → `audit:aprobado`.

## Checklist 🏛️ Claude (cierre)
- [ ] Squash-merge. `matriz-riesgos.md`: **M5 → 🟢**. Confirmar eventos llegando en staging.
- [ ] Avisar al 🧑 Usuario: con la línea base midiendo, desbloquear `rediseno-home-confianza.md`.

## Qué se hizo

🔨 **Antigravity completó la construcción con éxito:**
- **Modelo de Datos:** Creado `AnalyticsEvent` en `apps.core.models.py` para almacenar eventos sin almacenar direcciones IP ni datos personales identificables (PII).
- **Ratelimit centralizado:** Extraído el patrón de throttling en `apps/core/ratelimit.py` (`get_client_ip`, `is_rate_limited` e `increment_rate_limit`) y refactorizado el webhook de video `api_video.py` para usarlo.
- **Endpoint POST /eventos/:** Desarrollado endpoint en `apps/core/views/analytics_views.py` para recibir y persistir eventos de cliente con allowlist estricta y throttling de 60 peticiones/minuto, validando CSRF nativamente.
- **Señal Google OAuth:** Registrado handler en `apps/core/signals.py` para capturar la señal `user_logged_in` de `allauth` e insertar el evento `login_google` para logins recurrentes y nuevos.
- **Registro Signup:** Integrado registro server-side directo del evento `signup` en `register_view` de `accounts/views.py`.
- **Registro Page View:** Añadido registro server-side del evento `page_view` en el `get` de `HomeView` de `apps/core/views/home.py` acotado al home.
- **Script JS de Tracking:** Creado `static/js/analytics.js` con el nonce dinámico del CSP para capturar clicks de WhatsApp (`wa.me` / `api.whatsapp.com`), llamadas (`tel:`), descargas de archivos adjuntos (`download` o `/media/`), y reproducciones de YouTube con validación estricta del origen (`https://www.youtube-nocookie.com`).
- **Dashboard Staff:** Creado `/panel/analitica/` en `apps/core/views/analytics_views.py` e interfaz visual premium en `templates/core/panel_analitica.html` consumiendo el ledger existente de `ResourceView` (sin duplicaciones), `User.objects` y `AnalyticsEvent`.
- **Integraciones:** Añadida metaetiqueta CSRF en `base.html`, habilitado el parámetro `enablejsapi=1` en el detalle de recursos, y actualizada la política de privacidad.
- **Calidad y Verificación:** Aumentada la suite a 191 pruebas en `apps/core/tests.py`, cubriendo endpoint de eventos, límite de tasa configurado por settings override, signals mockeadas con RequestFactory y acceso restringido al dashboard. Suite completa 100% en verde localmente.

🩹 **Cura de Auditoría (Codex):**
- **Sanitización de Metadata:** Se implementó `sanitize_metadata` en `apps/core/views/analytics_views.py` para descartar claves con datos PII y limitar la metadata a un máximo de 5 claves con strings ≤ 150 caracteres.
- **Signals Robustas:** Modificada la señal `login_google` en `apps/core/signals.py` para leer `sociallogin` desde `kwargs`, solucionando fallos en logins recurrentes de allauth.
- **Corrección de Links en Dashboard:** Corregidos los enlaces del top 10 en `panel_analitica.html` para usar `resource.resource__slug` en lugar de `resource.resource_id`.
- **Tests Reales de CSRF:** Agregadas pruebas específicas en `apps/core/tests.py` que validan el rechazo de peticiones sin token CSRF y la aceptación con token válido usando `Client(enforce_csrf_checks=True)`.
