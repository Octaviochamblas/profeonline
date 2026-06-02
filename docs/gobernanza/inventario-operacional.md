# Inventario operacional

> Documento **canónico** (Capa 1). Servicios, secretos, variables y comandos para operar y
> desplegar. **No contiene valores secretos**, solo qué existe y dónde. Última revisión: 2026-06-01.

## 1. Servicios

| Servicio | Para qué | Notas |
| --- | --- | --- |
| **Railway (Producción)** | Hosting de la app y deploy | Push a `main` → deploy con *Wait for CI*. Bloquea puertos SMTP salientes. |
| **PostgreSQL (Producción)** (Railway/Supabase) | Base de datos principal | `DATABASE_URL` **obligatorio** (sin fallback a SQLite). SSL `require`. Confirmar pooler antes de escalar. |
| **Railway (Staging)** | Entorno de pruebas y QA visual | Pendiente creación por usuario (A1). Apunta a su propia DB PostgreSQL aislada. |
| **PostgreSQL (Staging)** | Base de datos de Staging | Base de datos PostgreSQL aislada, exclusiva para el servicio web de staging. |
| **Brevo** | Envío de email vía **API HTTP** (443) | Backend `apps.core.email_backends.BrevoApiEmailBackend`. |
| **Sentry** | Monitoreo de errores | Proyecto `python-django`, org `particular-lw`. `send_default_pii=False`, tracing off por defecto. |
| **Google (allauth)** | Login social | `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`. |
| **YouTube Data API** | Import de playlists/recursos | `YOUTUBE_API_KEY`. |
| **Redis** *(activo, C3)* | Cache compartida + rate-limit del webhook | `REDIS_URL` definido en prod (2026-06-02). **Requisito obligatorio** del rate-limit del webhook (evita rate-limit por-worker en producción); el `system check` avisa si falta. |

## 2. Inventario de secretos (rotación: semestral)

| Secreto | Uso | Dónde | Última rotación |
| --- | --- | --- | --- |
| `DJANGO_SECRET_KEY` | Firma sesiones/CSRF | Railway env | — |
| `DATABASE_URL` | Conexión DB (obligatorio) | Railway env | — |
| `API_SECRET_TOKEN` | Auth del webhook de videos | Railway env | — |
| `BREVO_API_KEY` | Envío de correo | Railway env | 2026-05-30 |
| `GOOGLE_CLIENT_ID` / `_SECRET` | Login con Google | Railway env | — |
| `SENTRY_DSN` | Monitoreo de errores | Railway env | — |
| `YOUTUBE_API_KEY` | Import de playlists | Railway env | — |
| `REDIS_URL` | Cache/rate-limit compartido | Railway env | 2026-06-02 |

## 3. Variables de entorno de seguridad (producción)

`DEBUG=False` · `DJANGO_ALLOWED_HOSTS` (req.) · `DJANGO_CSRF_TRUSTED_ORIGINS` ·
`SESSION/CSRF_COOKIE_SECURE=True` · `SECURE_SSL_REDIRECT` (def. true) · `SECURE_HSTS_SECONDS=31536000`
· `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` · `DJANGO_SECURE_HSTS_PRELOAD` ·
`DJANGO_USE_X_FORWARDED_PROTO` · `CANONICAL_BASE_URL`.
Detalle en `config/settings/production.py`.

## 4. Comandos clave

```bash
# Barrera local (la misma que CI). Correr antes de cada PR:
python manage.py test
python manage.py check
python manage.py makemigrations --check --dry-run

# Diagnóstico del entorno (desarrollo, staging o producción):
python manage.py check_environment

# Deploy check de producción o staging (como en CI):
python manage.py check --deploy --fail-level ERROR --settings=config.settings.production

# Arranque en Railway (Procfile / nixpacks.toml):
migrate && ensure_admin && ensure_site && gunicorn config.wsgi:application
```

- `ensure_admin` lee `DJANGO_ADMIN_*` y **nunca** reescribe contraseñas existentes.
- `seed_math_resources` **ya no** corre en el arranque (C1 mitigado): es idempotente (`get_or_create`,
  no pisa ediciones del staff) y se corre **a demanda**; usar `--refrescar-seo` para refrescar SEO.

## 5. Cadencia de auditorías recurrentes

Resumen; índice y plantillas en [`../auditorias/README.md`](../auditorias/README.md).

| Auditoría | Cadencia | Responsable |
| --- | --- | --- |
| Seguridad de dependencias (`pip-audit` + Dependabot) | Continua | 🤖 / 🏛️ |
| `check --deploy` | Cada PR | 🤖 |
| Accesibilidad (axe + teclado/NVDA) | Mensual + tras gran cambio de UI | 🤖 + 🧑 |
| Rendimiento (Lighthouse/CWV) | Mensual | 🤖 + 🏛️ |
| Seguridad de superficie externa (webhook, allauth, permisos) | Cada cambio relevante | 🏛️ |
| Backups / restauración | Trimestral | 🧑 + 🏛️ |
| Rotación de secretos | Semestral | 🧑 |
| Cobertura de tests | Cada PR | 🤖 |
| Revisión de migraciones | Cada migración | 🏛️ |
