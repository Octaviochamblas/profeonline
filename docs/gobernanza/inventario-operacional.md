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

## 6. Contrato de Orden de Lote (Upload Batch V1)

Esquema de datos JSON (`profeonline.upload-batch/v1`) utilizado por el script local de Codex para procesar e iniciar la publicación de un lote:

```json
{
  "schema": "profeonline.upload-batch/v1",
  "batch_id": "7f0d8c4c0ab31a6db57af241",
  "files": [
    "clase1.mp4",
    "clase2.mp4"
  ],
  "taxonomy": {
    "area_slug": "fisica",
    "subject_slug": "fisica-escolar",
    "topic_slug": "sonido",
    "module_slug": null
  },
  "youtube": {
    "playlist_id": "PLxxxx",
    "playlist_title": "Fisica",
    "create_playlist": false,
    "new_playlist": null
  },
  "instructions": "texto libre aplicado a todos los videos del lote",
  "publication": {
    "initial_privacy": "unlisted",
    "publish_only_when_validated": true
  }
}
```

*   `batch_id`: Huella estable del contenido de la orden. Junto con el nombre del archivo forma la
    clave idempotente del ítem; reenviar el mismo lote no duplica recursos, guías ni preguntas.
*   `taxonomy.module_slug`: Opcional (puede ser `null`).
*   `files`: Nombres de archivos seleccionados localmente. No contiene rutas absolutas ni sube contenido de video al servidor.
*   `youtube.playlist_id`: ID normalizado de una playlist existente. La UI acepta un enlace completo de YouTube o el ID directo.
*   `youtube.create_playlist`: Si es `true`, el agente local debe crear una playlist nueva en YouTube antes de agregar los videos.
*   `youtube.new_playlist`: `null` cuando se usa una playlist existente. Si `create_playlist` es `true`, contiene `title` obligatorio y `description` opcional.
*   `instructions`: Texto libre opcional.
*   `publication`: Política obligatoria del pipeline integrado. El agente local sube como
    `unlisted`; solo cambia a `public` después de que el servidor informa `questions_ready`.

### Pipeline educativo integrado

1. El **cliente de subida** (el uploader Node `profeonline-uploader`, a extender para este flujo)
   consume el JSON, sube el video no listado, guarda un sidecar local de reanudación, obtiene la
   transcripción desde la IP local y llama a `/api/recursos/crear-video/`. Reejecutar el mismo lote
   reutiliza `video_id` e ítem existentes. *(Existe un prototipo Python de referencia,
   `scripts/process_upload_batch.py`, no integrado al repo; el cliente canónico es el uploader Node.)*
2. El webhook hace *upsert* por ID de YouTube y por `batch_id + source_filename`; el recurso queda
   siempre en borrador.
3. `python manage.py process_publication_pipeline --limit 1` genera documento canónico, metadatos,
   guía y preguntas auditadas. Si la transcripción es insuficiente queda en `transcript_pending`.
4. El agente consulta `/api/publicacion/<id>/`. Al recibir `questions_ready`, actualiza título y
   descripción de YouTube, cambia el video a público y confirma en
   `/api/publicacion/<id>/confirmar/`.
5. La confirmación publica recurso y preguntas en una transacción local. Los reintentos son
   aditivos/idempotentes y nunca eliminan respuestas históricas.

Credenciales locales del cliente de subida: OAuth de YouTube fuera del repo,
`PROFEONLINE_BASE_URL` y `PROFEONLINE_API_TOKEN`. No ejecutar contra producción sin autorización
explícita.
