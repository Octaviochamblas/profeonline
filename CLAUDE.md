# Guía para Claude — ProfeOnline

## 📋 Documentación y flujo de tareas

> **Lee primero `docs/README.md`** — es el índice maestro: da el contexto del proyecto y el mapa
> de qué leer según tu tarea. Las reglas de trabajo vigentes están en `docs/gobernanza/`.

El trabajo se gestiona con un **Kanban-pipeline** en `docs/backlog/` (cada etapa = dueño activo;
la IA dueña mueve la tarjeta con `git mv` al pasar su gate):

- **`backlog/1-por-iniciar/`** — backlog de ideas. Cada idea es un `.md` propio (usar `_plantilla.md`).
- **`backlog/2-arquitectura/`** — 🏛️ Claude redacta handoff + criterios (🧩 Codex hace preflight).
- **`backlog/3-construccion/`** — 🔨 Antigravity implementa en una rama.
- **`backlog/4-auditoria/`** — 🧩 Codex audita el diff (tests, N+1, migraciones).
- **`backlog/5-cierre/`** — 🏛️ Claude auditoría final + `squash-merge`.
- **`backlog/6-finalizados/`** — terminadas.
- **`reportes-sesion/`** — un reporte por sesión (`AAAA-MM-DD.md`).

### Reglas (seguir siempre)

1. **Al INICIAR una sesión:** seguir el *protocolo barato de lectura* de `docs/README.md`:
   `docs/_coordinacion/ESTADO.md` + el reporte más reciente de `reportes-sesion/` + la tarjeta
   activa (Claude no recuerda sesiones anteriores). **No "leer todo".**
2. **Idea nueva** → crear un `.md` en `backlog/1-por-iniciar/` basado en `_plantilla.md`.
3. **Cada IA, al pasar su gate, mueve la tarjeta** con `git mv` a la siguiente etapa
   (detalle del pipeline en `docs/gobernanza/proceso-multiagente.md`).
4. **Al cerrar (merge)** → completar **"Qué se hizo"** y mover con `git mv` a `backlog/6-finalizados/`.
5. **Al FINALIZAR una sesión:** escribir `reportes-sesion/AAAA-MM-DD.md`
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
- **Auditorías:** vigentes en `docs/auditorias/`; las antiguas en `docs/auditorias/_archivo-2026-05-30/`.

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
