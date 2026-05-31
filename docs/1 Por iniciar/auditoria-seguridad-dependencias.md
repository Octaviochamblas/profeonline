# Auditoría de seguridad y dependencias

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** Auditoría
- **Prioridad:** 🔴 Alta (incluye deuda de seguridad pendiente del reporte anterior)

## Problema / Objetivo

Dos frentes:
1. **Secretos expuestos sin rotar** (pendiente explícito del reporte 2026-05-30): la clave
   SMTP vieja de Brevo (`xsmtpsib-…`) y la API key (`xkeysib-…`) aparecieron en capturas y
   **siguen sin rotarse**. Es la deuda de seguridad más urgente.
2. **Sin auditoría de dependencias verificable** (PEND-018): hay `requirements.txt` pinneado
   y Dependabot activo, pero no se corre un escáner de vulnerabilidades (`pip-audit`).

Objetivo: cerrar la exposición de secretos y dejar un proceso repetible de auditoría de
dependencias.

## Diagnóstico inicial

- **Secretos:** la API HTTP de Brevo usa `BREVO_API_KEY`. Aunque se migró de SMTP a API,
  la clave mostrada en capturas debe considerarse comprometida y rotarse igual.
- **Sentry duplicado:** queda un proyecto Sentry duplicado (`4511480748638208`) que conviene
  borrar para no dispersar alertas (también del reporte anterior).
- **Dependencias:** Dependabot abre PRs por versión, pero no reporta CVEs activos del set
  actual. Falta integrar `pip-audit` al CI (`.github/workflows/django_ci.yml`).
- **Headers/CSP:** ya hay CSP con nonce (`apps/core/middleware.py`) y HSTS opt-in — buen
  estado; conviene confirmar con `manage.py check --deploy` y un escáner de headers.

## Ruta de trabajo

### Fase 1 — Rotación de secretos (urgente)
- Generar **nueva** `BREVO_API_KEY` en el panel de Brevo y **revocar la antigua**.
- Revocar/eliminar la clave SMTP vieja de Brevo (ya no se usa, pero estaba expuesta).
- Actualizar la variable en Railway (producción) y en `.env` local.
- Verificar envío de email post-rotación (recuperación de contraseña como prueba E2E).
- Confirmar que ningún secreto está commiteado (revisar historial / `.gitignore`).

### Fase 2 — Limpieza de Sentry
- Borrar el proyecto Sentry duplicado `4511480748638208`, dejar solo `python-django`.
- Confirmar que el `SENTRY_DSN` en producción apunta al proyecto correcto.

### Fase 3 — Auditoría de dependencias
- Correr `pip-audit` (o `safety`) localmente contra `requirements.txt`.
- Registrar CVEs encontrados, severidad y versión que los corrige.
- Añadir `pip-audit` como paso del workflow de CI (que falle/avise en vulnerabilidades altas).
- Revisar licencias de las dependencias principales (evitar sorpresas legales).

### Fase 4 — Verificación de headers de seguridad
- `manage.py check --deploy --settings=config.settings.production`.
- Escanear headers (CSP, HSTS, X-Content-Type-Options, Referrer-Policy) con un scanner.

## Criterios de aceptación

- Claves de Brevo rotadas; la antigua revocada; email funcionando con la nueva.
- Proyecto Sentry duplicado eliminado.
- `pip-audit` corre en CI y no hay vulnerabilidades de severidad alta sin atender.
- `check --deploy` sin warnings críticos.

## Notas / Consideraciones

- La rotación de secretos no debe esperar a las demás fases: hacerla **primero**.
- Documentar el procedimiento de rotación para futuras exposiciones.

---

## Qué se hizo
_(Completar al finalizar, antes de mover a "3 Finalizados".)_
