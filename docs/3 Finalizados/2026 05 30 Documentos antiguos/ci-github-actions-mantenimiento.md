# Mantenimiento de GitHub Actions y CI

Fecha de referencia: 2026-05-26
Estado actual: `Django CI` pasa correctamente en `main`.
Ultimo run verificado: #8, commit `442dc99`, conclusion `success`.

Este documento resume que se debe mantener para que el workflow de Django CI no vuelva a fallar por los errores ya detectados.

## Estado esperado

El workflow `.github/workflows/django_ci.yml` debe:

- Ejecutarse en `push` y `pull_request` hacia `main`.
- Crear el job `test (3.12)`.
- Instalar dependencias desde `requirements.txt`.
- Ejecutar `python manage.py check`.
- Ejecutar `python manage.py check --deploy --fail-level ERROR --settings=config.settings.production`.
- Ejecutar `python manage.py test`.

Si GitHub envia correos de fallos antiguos, revisar siempre el run mas nuevo en Actions. Durante la correccion quedaron varios runs fallidos intermedios, pero el run #8 paso.

## Errores ya corregidos

### 1. `No jobs were run`

Causa:

- `max-parallel` quedo accidentalmente dentro de `matrix`.
- GitHub no pudo generar una matriz de jobs valida.

Debe mantenerse asi:

```yaml
strategy:
  max-parallel: 4
  matrix:
    python-version: [ "3.12" ]
```

No dejar `max-parallel` indentado bajo `matrix`.

### 2. `All jobs have failed` en `Run Production Deployment Check`

Causa inicial:

- `check --deploy` estaba importando URLs con settings de produccion.
- `apps/core/urls/home_urls.py` resolvia `static("img/favicon.svg")` al importar el modulo.
- En produccion se usa `CompressedManifestStaticFilesStorage`, que exige un manifest de `collectstatic`.
- En CI ese manifest no existe durante `check --deploy`, por lo que Django fallaba con:

```text
ValueError: Missing staticfiles manifest entry for 'img/favicon.svg'
```

Debe mantenerse asi:

- No resolver archivos estaticos con `static(...)` en tiempo de importacion si el modulo puede cargarse con `config.settings.production`.
- Para `favicon.ico`, mantener una vista que resuelva `static("img/favicon.svg")` dentro de `get_redirect_url`, no en el argumento `url=` de `RedirectView.as_view(...)`.
- No agregar consultas a base de datos, lecturas de manifest o dependencias de archivos generados durante el import de `urls.py`, sitemaps, settings o vistas importadas por URLs.

### 3. Warnings de HSTS en `check --deploy`

Contexto:

- `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` y `DJANGO_SECURE_HSTS_PRELOAD` quedan apagados por defecto en `production.py`.
- Esto es deliberado: solo deben activarse en produccion real cuando dominio y subdominios esten confirmados.

Para CI:

- El workflow usa valores temporales `"true"` para que el deploy check quede limpio.
- El comando usa `--fail-level ERROR`, de modo que warnings no rompan CI si Django los muestra.

Debe mantenerse en el paso `Run Production Deployment Check`:

```yaml
env:
  DJANGO_SECRET_KEY: "ci-test-secret-key-must-be-long-and-secure-in-production-check"
  DJANGO_ALLOWED_HOSTS: "localhost,127.0.0.1,testserver"
  DJANGO_CSRF_TRUSTED_ORIGINS: "http://localhost,http://127.0.0.1,http://testserver"
  DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS: "true"
  DJANGO_SECURE_HSTS_PRELOAD: "true"
run: |
  python manage.py check --deploy --fail-level ERROR --settings=config.settings.production
```

## Checklist antes de tocar CI

- Mantener Python `3.12` mientras el proyecto use Django 6.0+.
- No reintroducir Python `3.11` en la matriz.
- Validar YAML antes de hacer push.
- Confirmar que el deploy check no depende de `db.sqlite3`, `staticfiles/`, `media/` ni archivos ignorados por Git.
- Confirmar que `requirements.txt` contiene todo lo que GitHub necesita instalar en un runner limpio.
- No guardar secretos reales en `.github/workflows/django_ci.yml`; solo usar valores temporales de CI.
- Si se agregan nuevos settings obligatorios en `production.py`, agregarlos tambien al entorno temporal del paso `Run Production Deployment Check`.
- Si se agregan assets estaticos usados en import-time por error, mover esa resolucion a runtime o cubrirlo con `collectstatic` en un paso separado.

## Comandos de validacion local

En PowerShell:

```powershell
$env:DJANGO_SECRET_KEY='ci-test-secret-key-must-be-long-and-secure-in-production-check'
$env:DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1,testserver'
$env:DJANGO_CSRF_TRUSTED_ORIGINS='http://localhost,http://127.0.0.1,http://testserver'
$env:DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS='true'
$env:DJANGO_SECURE_HSTS_PRELOAD='true'

.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py check --deploy --fail-level ERROR --settings=config.settings.production
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe -m pre_commit run check-yaml --files .github/workflows/django_ci.yml
```

Para simular mejor GitHub Actions:

- Probar con un entorno limpio si el fallo solo aparece en GitHub.
- Recordar que el runner de GitHub no tiene `db.sqlite3`, `staticfiles/`, `.env`, `.venv` ni archivos ignorados por Git.

## Como leer futuros correos de GitHub

- `No jobs were run`: revisar sintaxis, triggers, `jobs`, `if` y matriz del workflow.
- `All jobs have failed`: abrir el run y mirar el paso exacto que fallo.
- `Process completed with exit code 1`: buscar el traceback o salida anterior a esa linea.
- Advertencias sobre Node.js de `actions/checkout` o `actions/setup-python`: no son el mismo fallo de Django CI, pero conviene actualizar las actions cuando haya versiones compatibles nuevas.

## Regla practica

El CI debe poder correr en una maquina limpia, sin archivos generados localmente. Si algo solo funciona porque existe `db.sqlite3`, `staticfiles/`, `.env` o `.venv`, todavia no esta listo para GitHub Actions.
