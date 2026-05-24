# Registro de Cambios: Auditoría de Seguridad, SEO y UI/UX

Fecha: 2026-05-24  
Estado del proyecto: **Validado y listo para pruebas de integración**  
Tests totales: **41 exitosos (100% OK)**

Este documento contiene la explicación detallada de todos los cambios técnicos realizados para subsanar los hallazgos descritos en el reporte `docs/auditoria-seo-uiux-seguridad.md`.

---

## 1. Infraestructura y Configuración de Producción

### 1.1. Corrección del Bloqueo de Base de Datos (C1)
*   **Archivo modificado**: [production.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/config/settings/production.py)
*   **Problema anterior**: Había una llave de cierre sobrante (`}`) en la línea 73 dentro del bloque `else` de base de datos que provocaba un `SyntaxError` al intentar cargar la configuración de producción.
*   **Solución**: Se eliminó la llave de cierre incorrecta. Tras esto, la app corre de manera limpia y pasa el comando de validación `collectstatic` y `check --deploy` sin errores.

### 1.2. HSTS como Opt-In (M3)
*   **Archivo modificado**: [production.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/config/settings/production.py)
*   **Problema anterior**: Las opciones de `SECURE_HSTS_INCLUDE_SUBDOMAINS` y `SECURE_HSTS_PRELOAD` estaban activas por defecto. Esto representaba un riesgo operativo ya que podía bloquear el acceso a subdominios del sitio que no estuviesen aún listos con HTTPS.
*   **Solución**: Se definieron ambas variables en `False` por defecto, permitiendo activarlas opcionalmente (opt-in) mediante las variables de entorno `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` y `DJANGO_SECURE_HSTS_PRELOAD` respectivamente una vez configurado el dominio final.

### 1.3. Canonical URL Dinámica en Producción (M2)
*   **Archivo modificado**: [production.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/config/settings/production.py)
*   **Problema anterior**: La URL canónica estaba fija únicamente en los archivos base.
*   **Solución**: Se expuso la constante `CANONICAL_BASE_URL` para que intente leer la variable de entorno `CANONICAL_BASE_URL` en producción. Si no está configurada, realiza un fallback seguro a `"https://www.profeonline.cl"` en lugar de romper el sistema.

---

## 2. Endurecimiento de Seguridad (XSS y API)

### 2.1. Sanitización de Renderizado Markdown contra XSS (A1)
*   **Archivo modificado**: [markdown_tags.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/apps/core/templatetags/markdown_tags.py)
*   **Problema anterior**: El filtro personalizado de plantilla `|markdown` marcaba la salida directamente como segura (`mark_safe`) sin realizar ninguna limpieza. Si un recurso de estudio o un payload inyectado por la API de videos contenía etiquetas HTML crudas (como `<script>`), el navegador las ejecutaba (vulnerabilidad XSS).
*   **Solución**: 
    1.  Se insertó un preprocesador regex que identifica cualquier etiqueta HTML cruda (caracteres `<` seguidos de letras, barra invertida o signos de admiración/interrogación) y los escapa convirtiéndolos en entidades HTML seguras (`&lt;` y `&gt;`).
    2.  Se añadió un filtro regex para interceptar y neutralizar enlaces en formato Markdown con esquemas de protocolos maliciosos `javascript:` (como `[click](javascript:alert(1))`), transformándolos en enlaces inocuos `#invalid-scheme-`.
*   **Tests agregados**: En [tests.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/apps/core/tests.py) se creó `MarkdownSecurityFilterTests` para validar el escapado seguro de `<script>`, `<iframe>` y protocolos `javascript:`.

### 2.2. Robustecimiento del Webhook de Videos de YouTube (A2)
*   **Archivo modificado**: [api_video.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/apps/content/views/api_video.py)
*   **Problema anterior**: El webhook permitía un token por defecto si la variable de entorno no estaba configurada, leía el token desde el cuerpo del JSON, realizaba una comparación vulnerable a ataques de temporización e inicializaba recursos automáticos como publicados por defecto.
*   **Solución**:
    1.  **Fallo Cerrado**: La aplicación devuelve HTTP 500 si la variable de entorno `API_SECRET_TOKEN` no está configurada en el servidor o contiene el valor predeterminado débil.
    2.  **Cabeceras Obligatorias**: Se eliminó la lectura de token desde el cuerpo JSON. Ahora solo se admite la verificación a través de los headers `X-Api-Token` o `Authorization: Bearer <token>`.
    3.  **Comparación Segura**: Se reemplazó el comparador de igualdad normal por `secrets.compare_digest` para evitar ataques de temporización en la verificación del secreto.
    4.  **Borradores por Defecto**: Todos los recursos creados a través de este webhook se guardan con `is_published = False` (Borrador), forzando a que un administrador valide el material antes de indexarse públicamente.
*   **Tests agregados**: En [test_views.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/apps/content/tests/test_views.py) se creó `YouTubeWebhookSecurityTests` para validar de forma automatizada los rechazos de token inválidos, la ausencia de variables y el estado borrador inicial.

---

## 3. Validaciones de Datos en Formularios y Modelos

### 3.1. Validación de Extensiones y Tamaño de Archivos Adjuntos (M1)
*   **Archivo modificado**: [resource.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/apps/content/models/resource.py)
*   **Problema anterior**: El editor administrativo de recursos permitía adjuntar cualquier tipo de archivo sin control de peso ni tipo.
*   **Solución**:
    1.  Se agregó el validador `FileExtensionValidator` para limitar las subidas únicamente a formatos educativos estándar: `pdf, doc, docx, xls, xlsx, ppt, pptx, png, jpg, jpeg, zip`.
    2.  Se programó el método validador `validate_file_size` para limitar el tamaño de subida a un máximo de **10MB**.
*   **Tests agregados**: En [test_views.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/apps/content/tests/test_views.py) se creó `ResourceModelFileValidationTests` para verificar que el sistema rechace la subida de archivos que excedan el límite de tamaño.

### 3.2. Unicidad Case-Insensitive en Correos de Usuarios (M4)
*   **Archivo modificado**: [forms.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/accounts/forms.py)
*   **Problema anterior**: Las validaciones de correo de Django en el formulario de registro y perfil eran sensibles a mayúsculas/minúsculas. Esto permitía crear cuentas separadas con correos lógicamente idénticos (ej. `Ana@example.com` y `ana@example.com`).
*   **Solución**: Se normalizaron los métodos `clean_email()` de `CustomUserCreationForm` y `ProfileUpdateForm` para pasar a minúsculas los correos ingresados (`.lower().strip()`) y realizar la consulta de exclusión usando el modificador insensible a mayúsculas `email__iexact`.
*   **Tests agregados**: En [tests.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/accounts/tests.py) se crearon pruebas para validar que el sistema rechace la creación y actualización de perfiles con variaciones de mayúsculas de correos existentes.

---

## 4. UI/UX y Estilos CSS (U1, U2)

### 4.1. Limpieza de Estilos Inline
*   **Archivos modificados**: 
    *   [base.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/base.html) (Footer y notificaciones)
    *   [resource_detail.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/pages/resource_detail.html) (Contenedor de video y panel de descarga de materiales)
    *   [resource_list.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/pages/resource_list.html) (Barra de búsqueda)
    *   [estilos.css](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/static/css/estilos.css)
*   **Problema anterior**: Había múltiples bloques de atributos `style="..."` directamente en los templates HTML, dificultando la consistencia del tema visual y el diseño responsivo.
*   **Solución**: Se removieron todos los estilos inline y se modularizaron bajo nuevas clases reutilizables añadidas al final de la hoja de estilos:
    *   `.messages-container` y `.messages-container .badge` (Alertas)
    *   `.site-footer`, `.site-footer__content`, `.site-footer__links`, etc. (Footer)
    *   `.video-container` y `.video-container iframe` (YouTube Responsivo)
    *   `.resource-material-panel`, `.resource-material-stack`, etc. (Materiales)
    *   `.search-field-wrapper` (Campo de búsqueda)

### 4.2. Corrección del Footer Legal
*   **Archivo modificado**: [base.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/base.html)
*   **Problema anterior**: Los enlaces legales de "Términos de uso", "Privacidad" y "Contacto" se mostraban como spans con `cursor: pointer;`, simulando ser enlaces clickeables interactivos sin tener un destino real.
*   **Solución**: Se eliminó la interactividad visual (removiendo `cursor: pointer` y hover de links) y se les aplicó la clase de texto plano `.site-footer__text-muted` para que se rendericen como texto informativo y no rompan la experiencia de navegación del usuario.

---

## 5. Limpieza de Código Muerto (S3)

### 5.1. Remoción del Sitemap XML Manual
*   **Archivos modificados**:
    *   [seo.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/apps/core/views/seo.py)
    *   [__init__.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/apps/core/views/__init__.py)
*   **Problema anterior**: A pesar de que el sitemap se sirve a través del framework nativo oficial de Django en `sitemap.xml`, persistía en el código la función síncrona manual antigua `sitemap_xml` que no se utilizaba.
*   **Solución**: Se eliminó por completo la función `sitemap_xml` del archivo de vistas del core y se removió de su importación para evitar confusiones y código duplicado en el futuro.

---

## 6. Git e Ignorados

### 6.1. Exclusión de Static Files Compilados
*   **Archivo modificado**: [.gitignore](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/.gitignore)
*   **Solución**: Se agregó la línea `staticfiles/` a la lista de archivos ignorados para evitar que los archivos estáticos colectados localmente para pruebas de despliegue en producción se suban por error al repositorio.

---

## 7. Endurecimiento Residual Antes de Producción

### 7.1. Sanitización Markdown con Allowlist
*   **Archivos modificados**: [markdown_tags.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/apps/core/templatetags/markdown_tags.py) y [requirements.txt](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/requirements.txt).
*   **Mejora aplicada**: La sanitización por expresiones regulares se reemplazó por `bleach==6.2.0`, usando una lista explícita de etiquetas, atributos y protocolos permitidos. Esto mantiene Markdown útil (`strong`, listas, tablas, código y enlaces seguros) y neutraliza HTML crudo o enlaces `javascript:` con una estrategia más robusta.
*   **Tests agregados**: Se añadió una prueba para confirmar que los enlaces HTTPS válidos siguen funcionando después del endurecimiento.

### 7.2. Rate Limiting y Logging del Webhook
*   **Archivo modificado**: [api_video.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/apps/content/views/api_video.py).
*   **Mejora aplicada**: El webhook ahora registra intentos rechazados sin exponer tokens y aplica un límite básico de intentos fallidos por IP usando cache de Django. El límite se puede ajustar con `VIDEO_WEBHOOK_RATE_LIMIT_ATTEMPTS` y `VIDEO_WEBHOOK_RATE_LIMIT_WINDOW`.
*   **Tests agregados**: Se añadieron pruebas para verificar logs sin secretos y bloqueo `429` tras intentos fallidos repetidos.
