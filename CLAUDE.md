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
- **Tests:** La suite completa (`python manage.py test`) + `check --deploy` son la
  **barrera real en CI** (`.github/workflows/django_ci.yml`); Railway está configurado con
  *Wait for CI* para no desplegar si CI falla. El **pre-commit** se mantiene rápido a
  propósito: solo corre `check` + `makemigrations --check` (el entry usa
  `.venv\\Scripts\\python.exe`). Aun así, corre los tests localmente antes de pushear.
- **Despliegue:** push a `main` → Railway despliega. El *Custom Start Command*
  corre `migrate && ensure_admin && ensure_site && seed_math_resources && gunicorn`.
- **Email:** API HTTP de Brevo (`BREVO_API_KEY`); Railway bloquea puertos SMTP.
- **Errores:** Sentry (`SENTRY_DSN`) — proyecto `python-django` en org `particular-lw`.
- **Login con Google:** allauth, credenciales en `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`.
- **CSP:** con nonce por petición (`apps/core/middleware.py`).
- **Auditorías antiguas:** archivadas en `docs/3 Finalizados/Auditorías-2026-05-30/`.

## 💸 Economía de tokens (seguir SIEMPRE)

El consumo de tokens es una prioridad. Reglas para no dispararlo:

1. **Nunca usar llamadas "de relleno"** (`echo q1`, `echo flush`, etc.) para forzar/ordenar
   la salida de otras herramientas. Si los resultados llegan desordenados, esperar; no
   spamear comandos vacíos. Cada llamada cuesta tokens.
2. **Búsquedas acotadas:** Grep/Glob con `path`, `glob` y `head_limit` reducidos; pedir
   contexto (`-C`) solo cuando hace falta. Evitar barridos de todo el repo.
3. **Leer antes de editar** el fragmento exacto para que el `Edit` no falle y no haya que
   re-leer y reintentar. No re-leer archivos ya leídos sin cambios.
4. **Avisar ANTES de operaciones caras** (suites largas, builds, lectura de archivos
   grandes, muchas capturas, agentes/subagentes) y proponer una alternativa más barata para
   que el usuario decida.
5. **Si una sola tarea empieza a inflarse** (muchos reintentos o llamadas), detenerse, avisar
   al usuario el gasto aproximado y barajar un enfoque más económico antes de continuar.
6. **Previsualizar visualmente con URL local** (levantar runserver y pasar el link) en vez de
   capturas, salvo que el usuario pida una imagen.
