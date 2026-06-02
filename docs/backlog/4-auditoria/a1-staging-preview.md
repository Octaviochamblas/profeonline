# A1 — Entorno de staging / preview deploys

- **Estado:** Auditoría
- **Creado:** 2026-06-02
- **Prioridad:** P1 · **Cartera:** continuidad operacional (habilitador de QA)
- **Tipo:** infraestructura
- **Dueño sugerido:** 🧑 Usuario (Railway) + 🔨 Antigravity (settings + doc) → 🧩 Codex → 🏛️ Claude

## Objetivo (una frase)
Tener un entorno **staging** (o preview por PR) para auditar y hacer QA visual **antes** de prod, y habilitar el auto-merge sin que vaya directo a producción a ciegas.

## Contexto
- Hoy se audita/QA contra producción (riesgo A1). El auto-merge ya está activo: con staging, el flujo gana una red de seguridad real antes del go-live con alumnos.
- Settings: `config/settings/production.py` lee env vars; se puede parametrizar un entorno staging con su propia `DATABASE_URL` y `SENTRY_ENVIRONMENT=staging`.

## Alcance (lo que SÍ entra)
1. **🧑 Usuario (Railway):** crear un servicio **staging** con su **propia base de datos** (no la de prod), apuntado a la rama `main` (o a una `staging`) y sus env vars.
2. **🔨 Antigravity:** asegurar que los settings soportan staging sin duplicar lógica:
   - Reutilizar `production.py` con `SENTRY_ENVIRONMENT`, `ALLOWED_HOSTS` y `CANONICAL_BASE_URL` por env var (ya es así); documentar el set mínimo de variables para staging.
   - Doc `docs/gobernanza/runbook-staging.md`: prod vs staging, qué var cambia, cómo promover.
3. **🏛️ Claude:** una vez exista staging, mover el QA visual de los PRs a staging (no a prod).

## Fuera de alcance
- Datos de prod en staging. CI/CD nuevo (el actual basta; staging despliega desde rama).

## Archivos a tocar
| Archivo | Cambio |
| --- | --- |
| `docs/gobernanza/runbook-staging.md` (nuevo) | prod vs staging, variables, promoción |
| `apps/core/management/commands/check_environment.py` (nuevo) | comando de diagnóstico del entorno |

## Criterios de aceptación
- [ ] Staging responde 200 en su URL con **su propia** DB (no la de prod). (Pendiente del usuario en Railway)
- [x] Runbook documentado (variables mínimas + cómo promover a prod).
- [x] Barrera verde si se toca código.

## Qué se hizo
- Se implementó el comando de diagnóstico `check_environment` para imprimir la información no sensible de la base de datos y variables de entorno del servidor.
- Se agregaron las pruebas unitarias correspondientes en `apps/core/tests.py` para validar el comando bajo desarrollo, staging y producción.
- Se creó el runbook detallado en `docs/gobernanza/runbook-staging.md` explicando la arquitectura, los pasos manuales en Railway, las variables de entorno esperadas, las validaciones anti-producción y la lista de verificación.
- Se actualizó el inventario operacional `docs/gobernanza/inventario-operacional.md`.

## Qué queda pendiente del usuario
- Crear el servicio de Staging Web y la base de datos PostgreSQL exclusiva de Staging en Railway.
- Configurar las variables de entorno asociadas en Railway.
- Validar el acceso al sitio y al panel de administración en staging.

## Riesgos / rollback
- Riesgo: que staging comparta la DB de prod por error → **DB separada obligatoria**. Rollback: apagar el servicio staging; no afecta prod.

## Checklist 🧩 Codex
- [ ] Ninguna var de staging apunta a recursos de prod (DB, buckets). Label `audit:aprobado` si ok.

## Checklist 🏛️ Claude (cierre)
- [ ] QA de PRs migrado a staging. `matriz-riesgos.md`: A1 → 🟢.
