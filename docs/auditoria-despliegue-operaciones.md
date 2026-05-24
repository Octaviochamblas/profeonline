# Auditoria de Despliegue y Operaciones

Fecha de creacion: 2026-05-24
Estado: pendiente de ejecucion
Objetivo: dejar ProfeOnline preparado para operar en produccion con dominio real, HTTPS, base de datos, estaticos, backups, logs, monitoreo y rollback.

## Alcance recomendado

- Settings de produccion.
- Variables de entorno.
- Base de datos.
- Static files.
- Media files.
- Dominio y HTTPS.
- Search Console.
- Logs y errores.
- Backups/restauracion.
- Webhook y secretos.
- Proceso de deploy/rollback.

## Variables requeridas

- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`

## Variables recomendadas

- `DATABASE_URL`
- `CANONICAL_BASE_URL`
- `API_SECRET_TOKEN`
- `DJANGO_SECURE_SSL_REDIRECT`
- `DJANGO_USE_X_FORWARDED_PROTO`
- `DJANGO_SECURE_HSTS_SECONDS`
- `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `DJANGO_SECURE_HSTS_PRELOAD`
- `VIDEO_WEBHOOK_RATE_LIMIT_ATTEMPTS`
- `VIDEO_WEBHOOK_RATE_LIMIT_WINDOW`

## Pasos de auditoria

1. Confirmar hosting.
   - Proveedor.
   - Runtime Python.
   - WSGI/ASGI.
   - Variables de entorno.
   - Persistencia de archivos.

2. Confirmar dominio.
   - Dominio final.
   - www/no-www.
   - Redireccion canonica.
   - `CANONICAL_BASE_URL`.
   - `ALLOWED_HOSTS`.

3. Confirmar HTTPS.
   - Certificado valido.
   - Redirect HTTP -> HTTPS.
   - Proxy headers.
   - Cookies secure.
   - HSTS opt-in cuando corresponda.

4. Confirmar base de datos.
   - `DATABASE_URL`.
   - SSL requerido si usa PostgreSQL/Supabase.
   - Migraciones.
   - Backup.
   - Restauracion probada.

5. Confirmar estaticos.
   - `collectstatic`.
   - WhiteNoise.
   - Cache/compression.
   - `staticfiles/` fuera de Git.

6. Confirmar media.
   - Donde viven los archivos subidos.
   - Persistencia tras deploy.
   - Tamano maximo.
   - Estrategia si se migra a storage externo.

7. Confirmar observabilidad.
   - Logs de app.
   - Logs de webhook.
   - Errores 500.
   - Alertas basicas.
   - Auditoria de intentos 401/429.

8. Confirmar SEO operacional.
   - `/robots.txt`.
   - `/sitemap.xml`.
   - Search Console.
   - Sitemap enviado.
   - Canonical final.

9. Confirmar rollback.
   - Ultimo commit estable.
   - Backup previo.
   - Procedimiento para revertir deploy.
   - Procedimiento para revocar token webhook.

## Checklist de lanzamiento

| Item | Estado | Evidencia | Responsable | Fecha |
| --- | --- | --- | --- | --- |
| Variables obligatorias configuradas | Pendiente |  |  |  |
| HTTPS activo | Pendiente |  |  |  |
| `check --deploy` OK | Pendiente |  |  |  |
| `collectstatic` OK | Pendiente |  |  |  |
| Migraciones OK | Pendiente |  |  |  |
| Backup probado | Pendiente |  |  |  |
| `/robots.txt` OK | Pendiente |  |  |  |
| `/sitemap.xml` OK | Pendiente |  |  |  |
| Search Console configurado | Pendiente |  |  |  |

## Comandos de validacion

```powershell
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py test
.venv\Scripts\python.exe manage.py check --deploy --settings=config.settings.production
.venv\Scripts\python.exe manage.py collectstatic --noinput --settings=config.settings.production
```

## Recomendaciones iniciales probables

- No usar `runserver` en produccion.
- Definir `DJANGO_SECRET_KEY` largo y unico.
- Activar HSTS preload solo cuando el dominio y subdominios esten confirmados.
- Documentar backup y restore antes de publicar usuarios reales.
- Configurar logs persistentes y revisar alertas de 500/401/429.
- Mantener secretos fuera del repo.

## Criterios de aceptacion

- Deploy reproduce el sitio con `DEBUG=False`.
- Dominio real sirve HTTPS correctamente.
- Static files y media funcionan.
- Sitemap y robots responden 200.
- Search Console acepta sitemap.
- Existe plan de backup, restore y rollback.
- Existe procedimiento para rotar `API_SECRET_TOKEN`.

## Registro de cambios aplicados

| Fecha | Cambio | Archivo(s) | Validacion | Commit |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
