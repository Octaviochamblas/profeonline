# Runbook: Configuración y Operación del Entorno de Staging

Este runbook describe los objetivos, la arquitectura y los pasos necesarios para configurar, verificar y operar el entorno de **Staging** de ProfeOnline en Railway.

---

## 🎯 1. Objetivo de Staging

El entorno de staging sirve como una réplica de pre-producción. Su objetivo es:
*   Probar las integraciones de PRs y merges antes de que impacten al entorno de producción real.
*   Permitir auditorías manuales y QA visual en un servidor real antes de que existan alumnos en producción.
*   Habilitar el mecanismo de auto-merge con una red de seguridad intermedia para que no despleguemos cambios a ciegas en producción.

---

## 🏛️ 2. Arquitectura Esperada

La independencia absoluta de datos es obligatoria para evitar corrupción de base de datos de producción:

```
[ Entorno Producción ]
  └── Servicio Web Producción  --> apunta a --> Base de Datos PostgreSQL de Producción

[ Entorno Staging ]
  └── Servicio Web Staging     --> apunta a --> Base de Datos PostgreSQL de Staging (Independiente)
```

> [!CAUTION]
> **PROHIBIDO:** Conectar el servicio web de staging a la base de datos de producción. Cualquier cruce de credenciales anulará la seguridad y provocará la pérdida o corrupción de datos reales de alumnos.

---

## 🛠️ 3. Pasos Manuales en Railway (Pendiente Usuario)

El usuario debe realizar los siguientes pasos en la interfaz de Railway para inicializar el entorno:

1.  **Crear el Servicio Web de Staging**:
    *   En tu proyecto de Railway, añade un nuevo servicio apuntando al repositorio de GitHub `profeonline`.
    *   Configura la fuente del despliegue: se recomienda apuntar a la rama `main` (si staging representa lo último en main antes del release) o a una rama de staging dedicada (ej. `staging`).
2.  **Crear la Base de Datos de Staging**:
    *   Añade una nueva base de datos PostgreSQL en Railway dentro del mismo proyecto (o en un proyecto agrupado de staging).
    *   Verifica que sea una instancia **completamente independiente** de la base de datos de producción.
3.  **Conectar la DB al Servicio Web de Staging**:
    *   Copia la variable `DATABASE_URL` autogenerada por el servicio PostgreSQL de Staging y agrégala al entorno del servicio web de Staging.
4.  **Configurar Variables de Entorno del Servicio Web**:
    *   Configura las variables obligatorias y recomendadas descritas en la sección 4 utilizando placeholders y valores específicos de staging.
5.  **Configurar el Dominio de Staging**:
    *   Genera un dominio temporal provisto por Railway (ej. `staging-profeonline.up.railway.app`) en la pestaña "Settings" del servicio web.
6.  **Desplegar**:
    *   Inicia el despliegue del servicio web.
7.  **Verificación Inicial**:
    *   Una vez completado el deploy, accede a la raíz del sitio `/` y a `/admin/` para comprobar que levanta de forma correcta. Revisa los logs en busca de posibles fallos de migración o configuración.

---

## 📋 4. Variables de Entorno en Staging

Las variables del servicio web de staging deben dividirse y configurarse de la siguiente manera:

### A. Obligatorias
*   `DATABASE_URL`: Debe apuntar **únicamente** a la base de datos PostgreSQL exclusiva de Staging.
    *   *Formato:* `postgresql://user:password@host:port/database`
*   `DJANGO_SETTINGS_MODULE`: Debe establecerse en `config.settings.production` (el entorno en la nube usa el archivo de producción para empaquetar estáticos y configuraciones seguras).
*   `DJANGO_SECRET_KEY`: Clave única para firmas de staging. **No reutilices la SECRET_KEY de producción.**
*   `DJANGO_ALLOWED_HOSTS`: El dominio de staging.
    *   *Ejemplo:* `staging-profeonline.up.railway.app`
*   `DJANGO_CSRF_TRUSTED_ORIGINS`: El dominio de staging con el esquema correspondiente.
    *   *Ejemplo:* `https://staging-profeonline.up.railway.app`
*   `DJANGO_USE_X_FORWARDED_PROTO`: **`true`** — **obligatoria detrás del proxy de Railway.** Sin
    ella, Django (con `SECURE_SSL_REDIRECT`) no reconoce el `X-Forwarded-Proto: https` y entra en
    **loop de redirección 301 infinito**. (Ver hallazgo §8.1.)

### B. Recomendadas
*   `SENTRY_ENVIRONMENT`: Establécelo explícitamente en `staging` para agrupar reportes en Sentry.
*   `SENTRY_DSN`: Utiliza el mismo DSN del proyecto o uno separado para desarrollo/staging si está disponible.
*   `REDIS_URL`: Configura una base de datos Redis dedicada de staging para habilitar la caché compartida y probar los middlewares de rate-limit.
    *   *Ejemplo:* `redis://default:password@staging-redis.railway.internal:6379`
*   `CANONICAL_BASE_URL`: El URL absoluto de staging.
    *   *Ejemplo:* `https://staging-profeonline.up.railway.app`

### C. Opcionales
*   `BREVO_API_KEY`: API Key de Brevo. Si no se necesita probar correos, déjala en blanco (caerá en backend de consola y no enviará correos de verdad). Si se requiere probar, utilízala con extrema precaución para no enviar spam a usuarios reales.
*   **Google OAuth Callback (Login Social)**: Configura las credenciales de Google OAuth si se desea probar. Recuerda añadir el URI de redirección de staging en la consola de Google Developer (`https://staging-profeonline.up.railway.app/accounts/google/login/callback/`).

### D. PROHIBIDO USAR
*   `DATABASE_URL` de producción.
*   `DJANGO_SECRET_KEY` de producción.
*   Credenciales o API keys de producción que puedan modificar recursos reales de los alumnos.

---

## 🧪 5. Checklist de Verificación de Staging

Una vez desplegado staging, ejecuta esta lista para asegurar el correcto funcionamiento:

- [ ] **Acceso Web**: El sitio responde con un código de estado `200` en la URL pública de staging.
- [ ] **Acceso al Admin**: `/admin/` carga correctamente la pantalla de inicio de sesión.
- [ ] **Migraciones Aplicadas**: Las migraciones de base de datos se ejecutan en el arranque sin dar errores en los logs.
- [ ] **Comprobación de DB Independiente**: El comando `check_environment` muestra que estamos conectados a la base de datos de staging.
- [ ] **Comprobación de Caché**: Redis responde sin lanzar la advertencia `core.W001` de system check en staging (si Redis está configurado).
- [ ] **Emails Seguros**: Los correos de prueba no se envían a alumnos reales.
- [ ] **Check de Despliegue**: El comando `check --deploy` pasa con éxito.

---

## 🔒 6. Guardrail Anti-Producción

Para validar de forma fehaciente que el entorno de Staging **NO** está apuntando a la base de datos de producción por error, sigue este procedimiento:

1.  **Ejecutar Check de Diagnóstico**:
    Ejecuta el comando de diagnóstico en la consola del servicio staging:
    ```bash
    python manage.py check_environment
    ```
    *   Verifica que el **DB Host** y el **DB Name** correspondan a tu base de datos de staging y difieran del host y nombre de producción.
2.  **Verificación de Escritura Cruzada (Drill de Aislamiento)**:
    *   Inicia sesión en el admin de Staging y crea un registro de prueba (por ejemplo, un nuevo `Area` de prueba con el título `"Área de Prueba Staging Isolation"`).
    *   Verifica el administrador de Producción. **El registro creado no debe aparecer bajo ninguna circunstancia en producción.**
    *   Elimina el registro de prueba creado en Staging.
3.  **Prohibiciones de Operación**:
    *   **No ejecutes seeds destructivos** en staging si hay sospecha de cruce de entornos.
    *   **No restaures dumps de producción** sobre staging sin confirmación previa del equipo de operaciones y cambio del target de base de datos.

---

## 📊 7. Estado del Entorno

*   **Preparación Documental y de Configuración:** `COMPLETADA`.
*   **Creación Real del Servicio Staging en Railway:** ✅ `COMPLETADA (2026-06-02)`.
    *   Servicios: `Web-staging` (deploy desde `main`) + `Postgres-Staging` (DB aislada, host propio `postgres-staging.railway.internal`).
    *   Dominio: `https://web-staging-production-0dfc.up.railway.app` → **200** en `/` y `/admin/`.
    *   `check_environment` confirma: `DEBUG=False`, entorno **STAGING**, DB host de staging (no prod).
*   **Cierre de A1:** ✅ `CERRADO 🟢`.

---

## 🩺 8. Hallazgos del primer despliegue real (2026-06-02)

Al crear staging por primera vez aparecieron **dos diferencias con producción** que no estaban
documentadas. Ambas se deben a que un **servicio nuevo en Railway** no hereda ni la configuración del
servicio de prod ni (según el builder) la fase de build. Dejar esto resuelto evita repetir el dolor.

### 8.1 — Loop de redirección 301 (HTTPS) → falta `DJANGO_USE_X_FORWARDED_PROTO`
*   **Síntoma:** `/` y `/admin/` devuelven `301` a sí mismos en bucle (sitio inaccesible).
*   **Causa:** `production.py` solo activa `SECURE_PROXY_SSL_HEADER` si `DJANGO_USE_X_FORWARDED_PROTO=true`.
    Sin esa var, Django (detrás del proxy TLS de Railway) cree que la request es HTTP y `SECURE_SSL_REDIRECT`
    redirige a HTTPS infinitamente.
*   **Fix:** agregar la variable `DJANGO_USE_X_FORWARDED_PROTO=true` (ya en la lista de obligatorias §4.A).

### 8.2 — `500` en todas las páginas → `collectstatic` no corrió (builder)
*   **Síntoma:** tras arreglar 8.1, `/` y `/admin/` devuelven `500`; en consola: `UserWarning: No directory at: /app/staticfiles/`.
*   **Causa:** `production.py` usa `CompressedManifestStaticFilesStorage` (manifest), que **exige**
    `collectstatic`. Ese comando solo está en la **fase build** de `nixpacks.toml`. Un servicio nuevo
    puede usar otro builder (Railpack) que **no ejecuta esa fase**, dejando `staticfiles/` sin generar.
*   **Fix aplicado:** definir un **Custom Start Command** en el servicio de staging que colecte al
    arrancar (robusto ante el builder):
    ```
    python manage.py collectstatic --no-input && python manage.py migrate && python manage.py ensure_admin && python manage.py ensure_site && gunicorn config.wsgi:application
    ```
*   **Alternativa:** forzar el builder a **Nixpacks** en *Settings → Build* (replica exactamente prod).

### 8.3 — Cache (no bloqueante)
*   `check_environment` muestra `core.W001` (LocMemCache) porque staging no tiene `REDIS_URL`. Es
    **opcional** en staging; agregar un Redis de staging solo si se quiere probar el rate-limit del webhook.
