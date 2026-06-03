# Verificación de email real en el registro

> ✅ **Cerrado 🟢 (2026-06-03, 🏛️ Claude).** Mergeado en `main` vía **PR #38**. Antigravity construyó,
> Codex auditó (P1 duplicados en migración, P2 anti-enumeración, P3 usuarios sin email), Antigravity
> corrigió, Claude cerró (superficie sensible). `mandatory` + Google exento; la migración marca como
> verificados a los usuarios actuales (sin lockout) y prod envía vía Brevo. Suite **202 tests** verde.

> 🏛️ **Handoff de arquitectura (Claude, 2026-06-03).** Es la **siguiente tarea del sprint** y la única
> sin bloqueantes. Construye 🔨 Antigravity (rama `feat/email-verification` **desde `main`**) → audita
> 🧩 Codex (toca allauth/settings → también `seguridad:requiere-claude`) → cierra 🏛️ Claude.
> ⚠️ **Colisión a vigilar:** M5 (PR #36) ya añadió el evento `signup` en `register_view`
> (`accounts/views.py`); intégrate ahí sin romperlo. **Decisión a tomar:** ¿`mandatory` para todos los
> registros por email o solo para nuevos? El detalle de fases/criterios de abajo sigue vigente.

- **Estado:** ✅ Finalizado y mergeado (🟢) — PR #38
- **Creado:** 2026-05-31
- **Área:** Producto / Seguridad
- **Prioridad:** 🟢 Media

## Problema / Objetivo

La verificación de email quedó configurada de forma gradual/laxa (PEND-013,
`ACCOUNT_EMAIL_VERIFICATION`). Con registro abierto, esto deja entrar cuentas con correos
falsos o con typos, ensucia la base de usuarios y abre la puerta a abuso. Como el envío de
email por la API HTTP de Brevo **ya funciona** (recuperación de contraseña operativa), activar
verificación es de bajo riesgo técnico.

Objetivo: exigir verificación de email en el registro, con una experiencia de usuario clara y
coherente con el diseño del sitio.

## Diagnóstico / contexto técnico

- `config/settings/base.py`: revisar el valor actual de `ACCOUNT_EMAIL_VERIFICATION`
  (estaba en `none`/gradual).
- Email funcionando vía `BrevoApiEmailBackend` (`apps/core/email_backends.py`) — ya probado
  con el flujo de recuperación de contraseña.
- Registro propio + allauth (`accounts/`, `templates/accounts/`).
- Login con Google ya entrega emails verificados por Google (no deberían requerir doble
  verificación — confirmar comportamiento de allauth).

## Ruta de trabajo

### Fase 1 — Decidir el modo
- `mandatory` (no puede iniciar sesión hasta verificar) vs `optional` (puede entrar, se le
  insiste). Recomendado: **mandatory** para registro por email; Google queda exento.
- Definir caducidad del enlace y reenvío.

### Fase 2 — Plantillas de email con el diseño del sitio
- Crear/ajustar el email de verificación reutilizando el estilo del email de recuperación de
  contraseña (`templates/accounts/password_reset_email.html`) para consistencia de marca.
- Asunto claro en español.

### Fase 3 — Flujo y mensajes
- Página "te enviamos un correo de verificación" con instrucciones y opción de reenvío.
- Manejo de enlace expirado/usado con mensaje claro.
- Confirmar que el login con Google **no** queda bloqueado por esto.

### Fase 4 — Tests
- Tests del flujo: registro → email enviado → verificación → login.
- Caso Google sin doble verificación.

## Criterios de aceptación

- Un registro por email no puede operar sin verificar (si se elige `mandatory`).
- El email de verificación usa el diseño del sitio y llega vía Brevo.
- Reenvío y enlace expirado manejados con mensajes claros.
- Login con Google no se ve afectado.
- Tests verdes.

## Notas / Consideraciones

- Verificar límites/cuota de envío de Brevo para no toparse con el plan gratuito.
- La rotación de `BREVO_API_KEY` (que pedía `auditoria-seguridad-dependencias.md`) **ya está
  hecha** (finalizada en Sesión 1) → este bloqueo ya no aplica; se puede enviar sin riesgo.

---

## Qué se hizo

- **Configuración de Seguridad en `base.py`:** Habilitada la verificación obligatoria para registros directos (`ACCOUNT_EMAIL_VERIFICATION = "mandatory"`) y exención explícita para accesos de Google OAuth (`SOCIALACCOUNT_EMAIL_VERIFICATION = "none"`).
- **Integración de Registro en `views.py`:** Ajustado `register_view` para crear y enviar dinámicamente la confirmación de email con `setup_user_email` y `.send_confirmation` de `django-allauth`. Se resguardó y mantuvo intacto el evento de analítica interna `AnalyticsEvent(name="signup")`.
- **Exclusividad de Acceso en `forms.py`:** En `StyledAuthenticationForm`, se añadió el bloqueo en el flujo de autenticación para que usuarios no verificados no puedan loguearse. Se eximió del chequeo a superusuarios para evitar bloqueos y facilitar pruebas y administración.
- **Reenvío Seguro de Enlace:** Implementada la vista `email_verification_resend_view` y el formulario `ResendEmailForm` con enmascaramiento anti-enumeración de usuarios en el reenvío de activación.
- **Migración de Datos Retroactiva:** Creada la migración `0004_auto_20260602_2311.py` con dependencia directa en `allauth` (`('account', '0001_initial')`) para verificar de forma segura todas las cuentas de usuarios activos en la base de datos y evitar lockouts retroactivos.
- **UI & Templates Premium:**
  - Diseñados `email_verification_sent.html` (pantalla de aviso tras registro), `email_confirm.html` (activación y manejo de tokens inválidos/expirados), y `email_verification_resend.html` (solicitud de reenvío de enlace).
  - Creados los templates de texto plano bajo `templates/account/email/` imitando el estilo exacto de recuperación de contraseña y el cierre de marca "El equipo de ProfeOnline".
- **QA & Suite de Pruebas:**
  - Se agregaron los tests `EmailVerificationFlowTests` cubriendo el registro, la denegación de login, la exención de Google, y el funcionamiento correcto de la migración de datos.
  - Se corrigió la sintaxis de importación de la migración y la firma de `assertFormError` para compatibilidad con Django 5.x.
  - La suite de 200 pruebas de ProfeOnline quedó en **VERDE** (OK).
