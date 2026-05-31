# Guía para Claude — ProfeOnline

## 📋 Flujo de trabajo de tareas (Kanban en `docs/`)

Las ideas y tareas del proyecto se gestionan con carpetas numeradas en `docs/`:

- **`1 Por iniciar/`** — ideas y tareas pendientes (backlog). Cada idea es un `.md` propio (usar `_plantilla.md`).
- **`2 En Proceso/`** — tareas en las que se está trabajando ahora.
- **`3 Finalizados/`** — tareas terminadas.
- **`4 Reportes por Sesión/`** — un reporte por sesión (`AAAA-MM-DD.md`).

### Reglas (seguir siempre)

1. **Al INICIAR una sesión:** leer el reporte más reciente de `4 Reportes por Sesión/`
   para recuperar el contexto (Claude no recuerda sesiones anteriores).
2. **Idea nueva** → crear un `.md` en `1 Por iniciar/` basado en `_plantilla.md`.
3. **Al empezar a trabajar una idea** → moverla con `git mv` a `2 En Proceso/`.
4. **Al terminar** → completar la sección **"Qué se hizo"** del documento y moverlo
   con `git mv` a `3 Finalizados/`.
5. **Al FINALIZAR una sesión:** escribir `4 Reportes por Sesión/AAAA-MM-DD.md`
   (usar `_plantilla-reporte.md`) con todo lo avanzado **desde el reporte anterior**.

> Mover archivos siempre con `git mv` para conservar el historial.

## ⚙️ Convenciones técnicas del proyecto

- **Settings:** `config.settings.local` (dev, por defecto en `manage.py`) /
  `config.settings.production` (producción en Railway).
- **Tests:** `python manage.py test` deben pasar antes de commitear
  (hay pre-commit hook que corre `check` + tests). El entry usa `.venv\\Scripts\\python.exe`.
- **Despliegue:** push a `main` → Railway despliega. El *Custom Start Command*
  corre `migrate && ensure_admin && ensure_site && seed_math_resources && gunicorn`.
- **Email:** API HTTP de Brevo (`BREVO_API_KEY`); Railway bloquea puertos SMTP.
- **Errores:** Sentry (`SENTRY_DSN`) — proyecto `python-django` en org `particular-lw`.
- **Login con Google:** allauth, credenciales en `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`.
- **CSP:** con nonce por petición (`apps/core/middleware.py`).
- **Auditorías antiguas:** archivadas en `docs/3 Finalizados/Auditorías-2026-05-30/`.
