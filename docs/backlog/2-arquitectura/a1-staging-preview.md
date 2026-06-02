# A1 — Entorno de staging / preview deploys

- **Estado:** Ready (handoff de arquitectura)
- **Creado:** 2026-06-02
- **Prioridad:** P1 · **Cartera:** continuidad operacional (habilitador de QA)
- **Tipo:** infraestructura
- **Dueño sugerido:** 🧑 Usuario (Railway) + 🔨 Antigravity (settings + doc) → 🧩 Codex → 🏛️ Claude

## Objetivo (una frase)
Tener un entorno **staging** (o preview por PR) para auditar y hacer QA visual **antes** de prod,
y habilitar el auto-merge sin que vaya directo a producción a ciegas.

## Contexto
- Hoy se audita/QA contra producción (riesgo A1). El auto-merge ya está activo: con staging, el
  flujo gana una red de seguridad real antes del go-live con alumnos.
- Settings: `config/settings/production.py` lee env vars; se puede parametrizar un entorno staging
  con su propia `DATABASE_URL` y `SENTRY_ENVIRONMENT=staging`.

## Alcance (lo que SÍ entra)
1. **🧑 Usuario (Railway):** crear un servicio **staging** con su **propia base de datos** (no la de
   prod), apuntado a la rama `main` (o a una `staging`) y sus env vars.
2. **🔨 Antigravity:** asegurar que los settings soportan staging sin duplicar lógica:
   - Reutilizar `production.py` con `SENTRY_ENVIRONMENT`, `ALLOWED_HOSTS` y `CANONICAL_BASE_URL`
     por env var (ya es así); documentar el set mínimo de variables para staging.
   - Doc `docs/gobernanza/runbook-entornos.md`: prod vs staging, qué var cambia, cómo promover.
3. **🏛️ Claude:** una vez exista staging, mover el QA visual de los PRs a staging (no a prod).

## Fuera de alcance
- Datos de prod en staging. CI/CD nuevo (el actual basta; staging despliega desde rama).

## Archivos a tocar
| Archivo | Cambio |
| --- | --- |
| `docs/gobernanza/runbook-entornos.md` (nuevo) | prod vs staging, variables, promoción |
| (posible) `config/settings/` | solo si hace falta un ajuste menor; evitar un settings nuevo si production.py ya sirve |

## Criterios de aceptación
- [ ] Staging responde 200 en su URL con **su propia** DB (no la de prod).
- [ ] Runbook documentado (variables mínimas + cómo promover a prod).
- [ ] Barrera verde si se toca código.

## Riesgos / rollback
- Riesgo: que staging comparta la DB de prod por error → **DB separada obligatoria**. Rollback:
  apagar el servicio staging; no afecta prod.

## Checklist 🧩 Codex
- [ ] Ninguna var de staging apunta a recursos de prod (DB, buckets). Label `audit:aprobado` si ok.

## Checklist 🏛️ Claude (cierre)
- [ ] QA de PRs migrado a staging. `matriz-riesgos.md`: A1 → 🟢.
