# Documentación de Cambios: Auditoría de Seguridad, UX/UI, SEO e Integración con YouTube

Este documento detalla todas las modificaciones y mejoras implementadas en **ProfeOnline** para resolver los hallazgos de la auditoría y añadir las nuevas integraciones automáticas.

---

## 🔒 1. Seguridad e Infraestructura

1. **Soporte Híbrido PostgreSQL (Supabase) / SQLite**:
   * **Archivo**: `config/settings/production.py` y `config/settings/base.py`.
   * **Descripción**: Se configuraron los settings de producción para leer la variable de entorno `DATABASE_URL` usando `dj-database-url`. Si la base de datos es PostgreSQL (como en Supabase), se añade de forma automática la opción `sslmode: require` para despliegues en la nube.
   * **Desarrollo Local**: Si no se detecta la variable `DATABASE_URL` en el entorno, el sistema utiliza `db.sqlite3` automáticamente para mantener un desarrollo local simplificado.

2. **Configuración de Servido de Estáticos (`STATIC_ROOT` y WhiteNoise)**:
   * **Archivos**: `config/settings/base.py`, `config/settings/production.py` y `requirements.txt`.
   * **Descripción**: Se definió `STATIC_ROOT = BASE_DIR / 'staticfiles'` para que `collectstatic` funcione correctamente. Se integró la librería `whitenoise` en el middleware de Django para que el servidor pueda servir, comprimir y cachear los archivos estáticos en producción de forma autónoma.
   * **Aislamiento**: Para evitar fallos en el entorno de pruebas local, la configuración de almacenamiento comprimido se aisló exclusivamente en los settings de producción.

3. **Validación de Email Único en Formularios**:
   * **Archivo**: `accounts/forms.py`.
   * **Descripción**: Se agregaron métodos de validación `clean_email()` en `CustomUserCreationForm` (registro) y `ProfileUpdateForm` (perfil) para evitar que se registren correos duplicados. Esto previene colisiones e inconsistencias con el flujo de recuperación de contraseña de Django.

4. **Integración con Google Social Auth**:
   * **Archivos**: `config/settings/base.py` y `config/urls.py`.
   * **Descripción**: Se configuró `django-allauth` con el backend de autenticación social de Google, mapeándolo bajo la ruta `/accounts/` para evitar conflictos con las URLs customizadas de `/cuentas/`.

5. **HTMX Autocontenido (Local)**:
   * **Archivos**: `static/js/htmx.min.js` y `templates/base.html`.
   * **Descripción**: Se descargó la librería HTMX localmente. La plantilla base ahora carga HTMX desde los archivos estáticos locales en lugar de depender del CDN de unpkg, haciendo que el proyecto sea autónomo ante caídas externas de red.

6. **Referrer-Policy**:
   * **Archivo**: `config/settings/production.py`.
   * **Descripción**: Se estableció `SECURE_REFERRER_POLICY = 'same-origin'` para proteger la privacidad de los usuarios evitando el envío de URLs privadas en enlaces externos.

---

## 🎨 2. Experiencia de Usuario (UX/UI) y Nuevas Características

1. **Subida y Descarga de Archivos Adjuntos (PDF, Word, PPT)**:
   * **Archivos**: `apps/content/models/resource.py`, `apps/content/forms/resource_forms.py`, `templates/pages/resource_form.html` y `templates/pages/resource_detail.html`.
   * **Descripción**: Se añadió un campo `file` de tipo `FileField` al modelo `Resource` y se actualizó el formulario del editor para permitir subir archivos con `enctype="multipart/form-data"`. En el detalle del recurso, si existe un archivo, se muestra un botón destacado para descargarlo.

2. **Integración YouTube responsivo**:
   * **Archivos**: `apps/content/models/resource.py`, `apps/content/views/resource_detail.py` y `templates/pages/resource_detail.html`.
   * **Descripción**: Se añadió el campo `video_url` al recurso. La vista de detalles extrae el ID de YouTube usando expresiones regulares y renderiza un reproductor responsivo de YouTube en la cabecera.

3. **API/Webhook Seguro para Creación de Recursos Automática**:
   * **Archivos**: `apps/content/views/api_video.py`, `apps/content/urls/resource_urls.py` y `apps/content/views/__init__.py`.
   * **Descripción**: Se diseñó el endpoint POST `/api/recursos/crear-video/` protegido por un token de seguridad (`API_SECRET_TOKEN`). Permite que un agente externo (como tu script de YouTube) envíe un JSON con los datos del video y cree/actualice automáticamente la página del recurso en la web.

4. **Buscador de Texto e Interpretación de Markdown**:
   * **Archivos**: `apps/content/selectors/resource_selectors.py`, `apps/content/views/resource_list.py`, `templates/pages/resource_list.html` y `apps/core/templatetags/markdown_tags.py`.
   * **Descripción**: 
     * Se añadió un buscador por texto que consulta título y descripción.
     * Se integró en la interfaz de filtros mediante un input con trigger dinámico en tiempo real (`keyup delay:500ms`) de HTMX.
     * Se programó un filtro de plantilla personalizado `|markdown` para interpretar el texto plano de los recursos en HTML enriquecido (listas, tablas, negritas).

5. **Accesibilidad en Dropdowns Customizados**:
   * **Archivo**: `static/js/enhanced-select.js`.
   * **Descripción**: Se añadió soporte completo de navegación de teclado (flechas `ArrowDown`, `ArrowUp` y tecla `Escape`), cumpliendo con los estándares ARIA Combobox sin cambiar la lógica ni el diseño de estilos original.

6. **Alertas Flash (Notificaciones)**:
   * **Archivos**: `templates/base.html` y `accounts/views.py`.
   * **Descripción**: Se insertó un contenedor elegante de alertas en la plantilla base que despliega notificaciones instantáneas de éxito/error ante acciones como el registro y la edición del perfil.

7. **Paginación HTMX e Interfaz Premium (Fonts & Footer)**:
   * **Archivos**: `templates/pages/resource_list.html`, `templates/base.html` y `static/css/estilos.css`.
   * **Descripción**: 
     * Se decoraron los enlaces de paginación con HTMX para transiciones fluidas.
     * Se importó la tipografía premium **Outfit** en `base.html` y se aplicó al body en el CSS.
     * Se diseñó e integró un pie de página (footer) responsivo e institucional.

---

## 🔍 3. Optimización para Buscadores (SEO)

1. **Sitemap XML Nativo y Escalable**:
   * **Archivos**: `apps/core/sitemaps.py` y `apps/core/urls/home_urls.py`.
   * **Descripción**: Se reemplazó la generación manual síncrona por el framework nativo de Django, registrando sitemaps para asignaturas, niveles, recursos y páginas estáticas. Cuenta con soporte para paginación y caché para evitar la sobrecarga de consultas a la base de datos.

2. **Directivas en `robots.txt`**:
   * **Archivo**: `apps/core/views/seo.py`.
   * **Descripción**: Se añadieron exclusiones de rastreo en `robots.txt` para rutas administrativas y endpoints de edición (`*/crear/`, `*/editar/`, `*/eliminar/`, `*/opciones/`), ahorrando presupuesto de rastreo de los bots.

3. **URLs Canónicas Estables**:
   * **Archivos**: `apps/core/context_processors.py`, `config/settings/base.py` y `templates/base.html`.
   * **Descripción**: Se implementó una constante `CANONICAL_BASE_URL` ("https://www.profeonline.cl") que se inyecta en todas las plantillas. En entornos locales o de prueba, el context processor hereda la URL del request dinámicamente para facilitar las pruebas del desarrollador.

---

## 🐞 4. Corrección de Errores de Configuración Encontrados
* **Archivos**: `apps/content/views/topic_update.py`, `apps/content/views/subject_update.py` y `apps/content/views/level_update.py`.
* **Descripción**: Se corrigió el error `ImproperlyConfigured` en las vistas genéricas `TopicUpdateView`, `SubjectUpdateView` y `LevelUpdateView` importando sus modelos respectivos y especificando la propiedad `model = ...`.
