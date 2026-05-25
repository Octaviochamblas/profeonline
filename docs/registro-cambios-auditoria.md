# Auditoria Consolidada: Seguridad, SEO, UI/UX e Integraciones

Fecha de consolidacion: 2026-05-24
Rama actual: `main`
Estado: validado y listo para pruebas de integracion/despliegue
Tests actuales: 42 exitosos

Este documento consolida la informacion que antes estaba repartida en:

- `docs/auditoria-estandarizacion.md`
- `docs/actualizacion-auditoria-integraciones.md`
- `docs/auditoria-seo-uiux-seguridad.md`
- `docs/registro-cambios-auditoria.md`

## Resumen ejecutivo

ProfeOnline paso de una base Django funcional, pero con deuda de SEO, UI y produccion, a una plataforma bastante mas publicable: URLs en espanol, slugs publicos, landings por asignatura/nivel, sitemap nativo, robots.txt, canonical, datos estructurados, contenido semilla, UI oscura estandarizada, filtros de recursos corregidos, seguridad de borradores, settings de produccion, WhiteNoise, PostgreSQL/Supabase, HTMX local, Google allauth y webhook de videos endurecido.

Los hallazgos criticos y altos detectados en la auditoria quedaron resueltos. El proyecto ahora pasa `check`, `test`, `check --deploy` y `collectstatic` con variables temporales validas.

## Estado actual por area

### Seguridad

- Los recursos en borrador no son visibles para usuarios anonimos/no administradores.
- Los endpoints administrativos de recursos/modulos estan restringidos a superusuarios.
- `production.py` usa variables obligatorias para `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` y `DJANGO_CSRF_TRUSTED_ORIGINS`.
- Cookies de sesion y CSRF quedan seguras en produccion.
- `SECURE_SSL_REDIRECT` queda activo por defecto.
- HSTS `includeSubDomains` y `preload` quedaron como opt-in para evitar riesgos antes de validar dominio/subdominios.
- `SECURE_REFERRER_POLICY = "same-origin"`.
- Validacion de emails case-insensitive en registro y perfil.
- Archivos adjuntos limitados por extension y tamano maximo de 10 MB.
- Markdown se renderiza con `bleach==6.2.0`, usando allowlist de etiquetas, atributos y protocolos.
- Webhook `/api/recursos/crear-video/`:
  - falla cerrado si falta `API_SECRET_TOKEN` o si usa el valor por defecto debil;
  - acepta token solo por header;
  - usa `secrets.compare_digest`;
  - crea recursos en borrador por defecto;
  - registra intentos rechazados sin exponer tokens;
  - aplica rate limiting basico por IP con cache de Django.

### SEO

- `base.html` usa `lang="es-CL"`.
- Titulos y metadescripciones se orientaron a "clases particulares", apoyo escolar y recursos educativos.
- Se agregaron canonical, `og:url`, `og:image` por defecto y bloque `structured_data`.
- Login, registro y perfil quedaron fuera del foco SEO.
- Existen `/robots.txt` y `/sitemap.xml`.
- El sitemap usa el framework nativo de Django e incluye:
  - home;
  - listas publicas principales;
  - asignaturas activas;
  - niveles activos;
  - recursos publicados.
- Las URLs publicas quedaron en espanol:
  - `/recursos/`
  - `/asignaturas/`
  - `/temas/`
  - `/niveles/`
  - `/modulos/`
  - `/areas/`
- Recursos, asignaturas y niveles tienen detalle publico por slug.
- Las rutas legacy bajo `/content/...` redirigen a las URLs canonicas en espanol.
- Hay breadcrumbs visibles y JSON-LD `BreadcrumbList`.
- Los recursos publicos tienen JSON-LD `Article` cuando corresponde.
- `CANONICAL_BASE_URL` puede configurarse por entorno en produccion, con fallback a `https://www.profeonline.cl`.

### UI/UX

- Se consolido una capa visual reutilizable en `static/css/estilos.css`.
- La home, listados, detalle de recursos, formularios, login, registro, perfil y confirmaciones quedaron bajo una estructura visual comun.
- Se normalizaron formularios desde backend con clases compartidas.
- Se agregaron estados vacios, badges, tablas, paneles, paginacion y bloques de accion consistentes.
- Se corrigieron los selects/filtros dependientes de recursos.
- `/recursos/` muestra filtros activos y accion `Limpiar filtros`.
- La paginacion conserva solo filtros normalizados.
- Se movieron estilos inline remanentes a clases CSS.
- Footer legal dejo de simular enlaces si aun no hay paginas reales.
- HTMX se sirve localmente desde `static/js/htmx.min.js`.
- Dropdowns custom tienen soporte de accesibilidad completo (`aria-controls`, vinculación ID, y cierre automático con Tab).
- Anillo de foco `:focus-visible` visible y consistente en todos los botones, campos de entrada, enlaces y comboboxes.
- Atributo `title` en el iframe de YouTube en detalles de recursos.
- Inyección automatizada de `aria-required="true"` en todos los campos obligatorios de formularios Django.

### Integraciones y despliegue

- Soporte hibrido SQLite local / PostgreSQL-Supabase por `DATABASE_URL`.
- Si `DATABASE_URL` usa PostgreSQL, se aplica `sslmode=require`.
- WhiteNoise queda configurado para servir estaticos en produccion.
- `STATIC_ROOT = BASE_DIR / "staticfiles"`.
- `staticfiles/` queda ignorado por Git.
- Google social auth con `django-allauth` en `/accounts/`.
- Soporte de videos YouTube en recursos.
- Soporte de archivos descargables en recursos.
- Buscador de texto en recursos por titulo/descripcion.
- Alertas flash para acciones de cuenta.

## Cronologia resumida

### 2026-05-23

- Auditoria inicial de estandarizacion.
- Proteccion de borradores y endpoints administrativos.
- Base de titulos, robots y metadatos SEO.
- Settings de produccion con variables de entorno.
- Canonical, Open Graph, JSON-LD base, robots y sitemap inicial.
- URLs publicas en espanol y detalle de recursos por slug.
- Primeras pruebas reales de vistas y SEO.

### 2026-05-24

- Estandarizacion visual completa de las superficies principales.
- Landings publicas por asignatura y nivel.
- Breadcrumbs y structured data para recursos/asignaturas/niveles.
- Contenido semilla con `seed_content`.
- Redirecciones legacy `/content/...`.
- Correccion de filtros dependientes en recursos.
- UX de filtros activos, limpiar filtros y paginacion normalizada.
- Documentacion de medicion SEO y despliegue.
- Integraciones: Supabase/PostgreSQL, WhiteNoise, allauth Google, HTMX local, archivos, videos, webhook, Markdown y sitemap nativo.
- Auditoria completa de SEO, UI/UX y seguridad.
- Correccion de hallazgos criticos/altos/medios.
- Endurecimiento de webhook con Bleach, logging y rate limiting.
- Auditoría y resolución de hallazgos de accesibilidad WCAG (estilos de foco, iframe de YouTube, comportamiento Tab y aria-required en formularios).
- Implementación de sugerencias de las auditorías de Privacidad/Legal, Rendimiento y Conversión de Contenido:
  - Creación de páginas estáticas legales de Términos de Uso, Política de Privacidad y Contacto.
  - Registro de las rutas de páginas legales y su inclusión en el sitemap dinámico de Django (`StaticViewSitemap`).
  - Aviso legal de aceptación de términos y privacidad en el formulario de registro de usuario.
  - Activación de enlaces reales en el footer del sitio en lugar de textos estáticos.
  - Uso de iframe con `youtube-nocookie.com` y `loading="lazy"` para videos en el detalle de recursos para mitigar tracking y mejorar rendimiento.
  - Optimización de copy de propuesta de valor en H1 y párrafo introductorio de la Home para mejorar conversión.
  - Integración de CI/CD via GitHub Actions para ejecución automatizada de pruebas y comprobación de despliegue.
  - Configuración e instalación de Git hooks locales mediante pre-commit para automatizar chequeos de estilo, calidad y pruebas unitarias a nivel de commit.


## Hallazgos resueltos

### C1. Produccion no iniciaba por SyntaxError

Estado: resuelto.

- Se elimino una llave sobrante en `config/settings/production.py`.
- `check --deploy` vuelve a ejecutarse correctamente.
- `collectstatic` funciona con settings de produccion.

### A1. Markdown podia renderizar HTML peligroso

Estado: resuelto y endurecido.

- Antes: Markdown se marcaba como seguro con `mark_safe` sin sanitizacion robusta.
- Despues: `bleach==6.2.0` limpia la salida con allowlist.
- Se mantienen etiquetas utiles como enlaces seguros, listas, tablas, codigo y enfasis.
- Se neutralizan HTML crudo y protocolos peligrosos como `javascript:`.

### A2. Webhook tenia token por defecto y publicaba por defecto

Estado: resuelto y endurecido.

- Se elimino el token por defecto aceptado.
- Token solo por header.
- Comparacion en tiempo constante.
- Recursos creados como borrador por defecto.
- Logging de rechazos sin secretos.
- Rate limiting basico por IP.

### M1. Archivos sin control

Estado: resuelto parcialmente suficiente para produccion inicial.

- Se agrego `FileExtensionValidator`.
- Se agrego limite de 10 MB.
- Pendiente opcional futuro: validar MIME real y estrategia de almacenamiento privado si los archivos dejan de ser publicos.

### M2. Canonical fijo

Estado: resuelto.

- `CANONICAL_BASE_URL` puede leerse desde variable de entorno en produccion.
- Debe alinearse con dominio, redirects, `ALLOWED_HOSTS`, sitemap y Search Console.

### M3. HSTS preload/includeSubDomains activos por defecto

Estado: resuelto.

- `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` y `DJANGO_SECURE_HSTS_PRELOAD` quedaron en `False` por defecto.
- Se activan solo cuando el dominio y subdominios esten listos.

### M4. Email unico case-sensitive

Estado: resuelto.

- Registro y edicion de perfil normalizan email con `lower().strip()`.
- La validacion usa `email__iexact`.

### S3. Sitemap manual obsoleto

Estado: resuelto.

- Se elimino `sitemap_xml` manual antiguo.
- El sitemap queda servido por el framework nativo de Django.

### U1/U2. Estilos inline y footer legal

Estado: resuelto.

- Se movieron estilos inline remanentes a CSS.
- El footer legal dejo de verse como enlaces sin destino.

## Validaciones ejecutadas

Ultima validacion conocida:

- `.venv\Scripts\python.exe manage.py check`: OK.
- `.venv\Scripts\python.exe manage.py test`: OK, 42 tests.
- `.venv\Scripts\python.exe manage.py check --deploy --settings=config.settings.production`: OK con variables temporales validas.
- `.venv\Scripts\python.exe manage.py collectstatic --noinput --settings=config.settings.production`: OK.
- `git diff --check`: OK.

Notas:

- Para `check --deploy`, si no se activan `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=true` y `DJANGO_SECURE_HSTS_PRELOAD=true`, Django puede mostrar warnings. Eso es esperado porque esas opciones quedaron deliberadamente como opt-in.
- `collectstatic` genera `staticfiles/`, que no debe subirse al repositorio.

## Variables de entorno de produccion

Obligatorias:

- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`

Recomendadas/segun entorno:

- `DATABASE_URL`
- `CANONICAL_BASE_URL`
- `API_SECRET_TOKEN`
- `DJANGO_SECURE_SSL_REDIRECT`
- `DJANGO_USE_X_FORWARDED_PROTO`
- `DJANGO_SECURE_HSTS_SECONDS`
- `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `DJANGO_SECURE_HSTS_PRELOAD`

Configurables para webhook:

- `VIDEO_WEBHOOK_RATE_LIMIT_ATTEMPTS`
- `VIDEO_WEBHOOK_RATE_LIMIT_WINDOW`

Regla de seguridad: no guardar secretos, tokens, IDs reales ni credenciales dentro del repositorio.

## Checklist operativo antes de publicar

- Configurar dominio real y decidir www/no-www.
- Confirmar `CANONICAL_BASE_URL` con el dominio final.
- Configurar `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS`.
- Configurar `API_SECRET_TOKEN` fuerte.
- Confirmar HTTPS y proxy headers si aplica.
- Ejecutar `collectstatic`.
- Verificar `/robots.txt`.
- Verificar `/sitemap.xml`.
- Dar de alta dominio en Google Search Console.
- Enviar sitemap a Search Console.
- No agregar analytics hasta elegir herramienta.
- Definir backups y restauracion de base de datos.
- Definir logs/monitoreo para errores y webhook.

## Pendientes recomendados

### Corto plazo

- QA manual en navegador desktop/mobile:
  - `/`
  - `/recursos/`
  - `/asignaturas/`
  - `/niveles/`
  - detalle de recurso
  - login/registro/perfil
  - formularios de creacion/edicion/eliminacion
- Revisar accesibilidad real de dropdowns custom con teclado y lector de pantalla.
- Crear paginas reales de terminos, privacidad y contacto si el sitio va a publicar usuarios reales.
- Revisar que el dominio final redirija consistentemente a la version canonica.

### Mediano plazo

- Fortalecer copy de landings por asignatura y nivel con contenido mas especifico.
- Agregar FAQs cuando exista contenido visible que lo justifique.
- Evaluar landings por tema solo si hay contenido suficiente.
- Evitar paginas por ciudad/comuna hasta tener contenido local real.
- Agregar analytics solo tras decidir herramienta.

## Auditorias adicionales recomendadas

- Accesibilidad WCAG: teclado, foco, contraste, lector de pantalla, formularios, dropdowns y estados de error.
- Rendimiento/Core Web Vitals: CSS/JS, fuentes, cache, LCP, CLS, imagenes y respuesta del servidor.
- Contenido/conversion: claridad de oferta, CTAs, confianza, proceso de clases, contacto y FAQs.
- Threat model de integraciones: webhook, agente YouTube, Markdown, archivos, roles admin y publicacion.
- Legal/privacidad: terminos, politica de privacidad, cookies, datos de estudiantes/menores y consentimiento.
- Operaciones/despliegue: backups, restauracion, logs, alertas, rotacion de secretos, rollback y monitoreo.
- Dependencias: vulnerabilidades conocidas, pinning, licencias y plan de actualizacion.

## Archivos clave

- `config/settings/base.py`
- `config/settings/production.py`
- `templates/base.html`
- `static/css/estilos.css`
- `static/js/enhanced-select.js`
- `apps/core/sitemaps.py`
- `apps/core/views/seo.py`
- `apps/core/templatetags/markdown_tags.py`
- `apps/content/views/api_video.py`
- `apps/content/views/resource_list.py`
- `apps/content/views/resource_detail.py`
- `apps/content/views/subject_detail.py`
- `apps/content/views/level_detail.py`
- `apps/content/models/resource.py`
- `accounts/forms.py`
- `requirements.txt`

## Estado final

El proyecto queda con una base tecnica consistente para avanzar hacia publicacion: seguridad razonable para una primera salida, SEO tecnico y semantico preparado, UI unificada, integraciones documentadas y pruebas reales. El siguiente esfuerzo deberia concentrarse en QA responsive/accesibilidad, dominio real, Search Console, contenido de conversion y operacion de produccion.
