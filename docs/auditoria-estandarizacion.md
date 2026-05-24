# Auditoria inicial de estandarizacion

Fecha: 2026-05-23
Rama: `estandarizacion`

## Resumen ejecutivo

El proyecto tiene una base Django simple y razonable: separacion por apps, templates centralizados, modelos con slugs, vistas administrativas protegidas por mixins y CSRF activo en formularios POST. La deuda principal no esta en la arquitectura base, sino en la falta de estandarizacion de presentacion, metadata SEO incompleta, URLs publicas aun basadas en IDs, ausencia de sitemap/robots y configuracion de produccion todavia inmadura.

La prioridad recomendada es corregir primero filtrado de contenido publicado y configuracion de produccion, luego convertir slugs/metadata en una base SEO reutilizable, y finalmente consolidar UI/formularios.

## Avance implementado

### 2026-05-23 - P1 seguridad/publicacion

- `ResourceDetailView` ahora filtra recursos no publicados para usuarios anonimos o no administradores.
- Superusuarios pueden seguir viendo recursos en borrador desde detalle.
- `module_resource_list` y `resource_options` quedaron protegidos para superusuarios, alineados con el constructor administrativo de modulos.
- `LOGIN_URL` apunta al login real del proyecto para que los redirects de permisos usen `/cuentas/login/`.
- Se agregaron 8 tests de vistas para recursos publicados/borradores y endpoints JSON administrativos.
- `python manage.py test` ejecuta 8 tests y pasa correctamente.

### 2026-05-23 - SEO de titulos y robots

- `base.html` ahora usa `lang="es-CL"` y define un bloque `robots`.
- Las paginas publicas principales incluyen titulos de navegador y Open Graph orientados a "clases particulares", "apoyo escolar" y recursos educativos.
- Login, registro y perfil usan `noindex,nofollow` para no gastar crawl budget en flujos de cuenta.
- Se reinicio el servidor local y `/content/topics/` muestra `Temas para Clases Particulares | ProfeOnline`.

### 2026-05-23 - Configuracion segura de produccion

- `production.py` carga `DJANGO_SECRET_KEY` y `DJANGO_ALLOWED_HOSTS` desde variables de entorno obligatorias.
- `CSRF_TRUSTED_ORIGINS` se puede configurar con `DJANGO_CSRF_TRUSTED_ORIGINS`.
- Cookies de sesion y CSRF quedan marcadas como secure en produccion.
- `SECURE_SSL_REDIRECT` y HSTS quedan activos por defecto, con overrides por entorno.
- `SECURE_PROXY_SSL_HEADER` solo se activa si `DJANGO_USE_X_FORWARDED_PROTO` esta habilitado.
- `python manage.py check --deploy --settings=config.settings.production` pasa sin issues usando variables temporales de validacion.

### 2026-05-23 - Base SEO tecnica

- `base.html` incluye canonical sin querystring, `og:url`, bloque `og_image` y bloque `structured_data`.
- La home declara JSON-LD `WebSite` con idioma `es-CL`.
- Se agregaron `/robots.txt` y `/sitemap.xml` desde vistas de `apps.core`.
- `robots.txt` bloquea `/admin/` y `/cuentas/`, y apunta al sitemap.
- `sitemap.xml` lista las paginas publicas principales: home, recursos, areas, asignaturas, temas, niveles y modulos.
- Se agregaron tests para canonical/OG URL/JSON-LD, robots y sitemap.
- Se reinicio el servidor local y `/robots.txt` y `/sitemap.xml` responden 200.

### 2026-05-23 - URLs publicas en espanol y slugs

- Las rutas nombradas de contenido ahora resuelven a URLs publicas en espanol: `/recursos/`, `/asignaturas/`, `/temas/`, `/niveles/`, `/modulos/` y `/areas/`.
- El detalle publico de recurso usa slug: `/recursos/<slug>/`.
- Las URLs antiguas bajo `/content/...` se mantienen como compatibilidad temporal.
- Los enlaces de recursos en templates usan `resource.slug`.
- El sitemap pasa a listar las URLs canonicas en espanol.
- Se agregaron tests para reverses en espanol, detalle por slug y compatibilidad legacy.
- `python manage.py test` ejecuta 14 tests y pasa correctamente.

### 2026-05-24 - Estandarizacion visual

- Se consolidaron componentes visuales reutilizables en `static/css/estilos.css` para hero, paneles, tablas, badges, formularios, paginacion, detalles y estados vacios.
- Se eliminaron estilos inline de las vistas publicas y de cuenta mas visibles, reemplazandolos por clases compartidas.
- La home, listados, detalle de recursos, formularios de contenido, login, registro, perfil y confirmaciones ahora siguen una estructura visual mas uniforme.
- Los formularios de contenido y cuenta aplican clases comunes desde backend para inputs, selects, textareas y checkboxes.
- Se simplificaron controles complejos como los selects personalizados del listado de recursos para usar controles nativos con mejor estabilidad en mobile.
- `python manage.py check` y `python manage.py test` siguen pasando correctamente tras la estandarizacion visual.

### 2026-05-24 - SEO de contenido y estructura semantica

- Se agregaron landings publicas por asignatura y nivel con `slug`, por ejemplo `/asignaturas/matematica/` y `/niveles/primaria/`.
- `resource_detail` ahora usa slug publico y muestra breadcrumbs visibles.
- Se agregaron JSON-LD `BreadcrumbList` y `Article` en los recursos, ademas de `BreadcrumbList` en asignaturas y niveles.
- El sitemap incluye ahora paginas publicas de asignaturas, niveles y recursos publicados.
- Se agrego favicon y se limpio CSS legacy no usado de la base visual.
- `python manage.py check`, `python manage.py test` y `python manage.py check --deploy --settings=config.settings.production` pasan con 29 tests y variables de entorno temporales validas.

### 2026-05-24 - Contenido semilla y redirecciones legacy

- Se agrego el comando `seed_content` para poblar areas, asignaturas, niveles, temas, recursos y modulos con contenido real reutilizable.
- Las rutas legacy bajo `/content/...` ahora redirigen a las URLs canonicas en espanol, incluyendo detalles antiguos por ID hacia slugs publicos.
- Home, asignaturas, niveles, recursos y modulos ya muestran contenido real en la base local tras ejecutar la semilla.
- Se corrigio la plantilla de modulos para mostrar `module.title` y no dejar oculto el contenido semillado.
- `python manage.py check`, `python manage.py test` y `python manage.py check --deploy --settings=config.settings.production` pasan con 29 tests y variables de entorno temporales validas.

### 2026-05-24 - UX de filtros de recursos

- `ResourceListView` normaliza `subject`, `topic` y `level` antes de consultar recursos publicados.
- La vista de recursos ahora muestra filtros activos con etiquetas legibles y un enlace `Limpiar filtros`.
- La paginacion conserva solo los filtros normalizados y evita arrastrar combinaciones invalidas.
- Se agregaron tests para el enlace de limpieza y para la paginacion con filtros normalizados.

## Hallazgos prioritarios

### P1 - Borradores accesibles por URL directa

Estado: resuelto en la rama. `ResourceDetailView` ahora filtra recursos no publicados para usuarios anonimos o no administradores, y superusuarios conservan acceso al borrador.

Evidencia:
- `apps/content/views/resource_detail.py`: filtro por `is_published=True` para no admins
- `apps/content/tests/test_views.py`: tests de 404/200 para anonimo y superusuario

Recomendacion:
- Mantener la cobertura de tests al extender futuras vistas de detalle.

### P1 - Endpoint de recursos de modulo sin restriccion de publicacion/autorizacion

Estado: resuelto en la rama. `module_resource_list` y `resource_options` quedaron protegidos para superusuarios y se agregaron tests para usuarios anonimos, regulares y admin.

Evidencia:
- `apps/content/views/module_resource_list.py`: `@user_passes_test(is_admin)`
- `apps/content/views/resource_options.py`: `@user_passes_test(is_admin)`
- `apps/content/tests/test_views.py`: cobertura de permisos y JSON

Recomendacion:
- Mantener el mismo patron en cualquier nuevo endpoint administrativo.

### P1 - Produccion no esta lista para despliegue seguro

Estado: resuelto en `production.py` con variables de entorno obligatorias para `SECRET_KEY`, `ALLOWED_HOSTS` y origenes CSRF, ademas de cookies seguras y flags HTTPS.

Evidencia:
- `config/settings/production.py`: carga de variables de entorno y hardening HTTPS
- `python manage.py check --deploy --settings=config.settings.production`: pasa sin issues con variables temporales validas

Recomendacion:
- Definir secretos y hosts reales en el entorno de despliegue, no en el repo.

### P2 - SEO tecnico incompleto

Estado: resuelto en la base tecnica y ampliado con contenido semantico. Ya existen canonical, `og:url`, `og:image` por defecto, `structured_data`, JSON-LD de home, `robots.txt`, `sitemap.xml`, `BreadcrumbList` y `Article` donde corresponde.

Evidencia:
- `templates/base.html`: bloques SEO base y favicon
- `apps/core/views/seo.py`: `robots_txt` y `sitemap_xml`
- `apps/content/views/_seo.py`: helpers de JSON-LD

Recomendacion:
- Seguir ampliando structured data solo cuando el contenido visible lo justifique.

### P2 - URLs publicas no aprovechan slugs

Estado: resuelto para recursos, asignaturas y niveles. Los detalles publicos ahora usan slugs y las listas enlazan a esas landings.

Evidencia:
- `apps/content/urls/resource_urls.py`: `resources/<slug:slug>/`
- `apps/content/urls/subject_urls.py`: `asignaturas/<slug:slug>/`
- `apps/content/urls/level_urls.py`: `niveles/<slug:slug>/`
- `templates/pages/resource_list.html`, `subject_list.html`, `level_list.html`

Recomendacion:
- Evaluar despues si temas, areas o modulos necesitan landings publicas equivalentes.

### P2 - UX/UI inconsistente por exceso de estilos inline

Estado: resuelto en la interfaz publica principal. Se unifico la capa visual, se sacaron estilos inline relevantes y se consolidaron componentes reutilizables para formularios, tablas, badges, paneles y detalles.

Evidencia:
- `static/css/estilos.css`: sistema visual consolidado
- `templates/pages/home.html`, `resource_list.html`, `resource_detail.html`, `subject_detail.html`, `level_detail.html`
- `templates/accounts/*`: formularios y vistas alineadas

Recomendacion:
- Revisar futuras superficies administrativas o de edicion con el mismo sistema de clases.

### P2 - Arquitectura de contenido SEO aun no existe

Estado: resuelto en el primer tramo. Ya existen landings publicas por asignatura y nivel con recursos relacionados, breadcrumbs y JSON-LD basico.

Evidencia:
- `apps/content/views/subject_detail.py`
- `apps/content/views/level_detail.py`
- `templates/pages/subject_detail.html`
- `templates/pages/level_detail.html`

Recomendacion:
- Si hace falta crecer mas adelante, ampliar por tema o ciudad solo con contenido util y suficiente.

### P3 - Tests son placeholders

Estado: resuelto. Ahora `manage.py test` ejecuta 29 tests reales que cubren seguridad, SEO tecnico, URLs en espanol, landings de asignatura/nivel, contenido semilla, recursos publicados/borradores y filtros normalizados.

Recomendacion:
- Seguir aumentando cobertura cuando agreguemos nuevas landings o flujos de edicion.

## Fortalezas actuales

- Separacion por apps (`accounts`, `core`, `content`) clara.
- `AdminRequiredMixin` protege create/update/delete en contenido.
- Formularios POST incluyen `{% csrf_token %}`.
- Selectores para recursos publicados ya existen.
- Modelos ya tienen slugs, lo que facilita la migracion SEO.
- HTMX usa SRI y `crossorigin`.

## Plan de trabajo recomendado

1. Seguridad/publicacion:
   - Filtrar drafts en detalle y endpoints JSON.
   - Tests de acceso anonimo/admin.
   - Endurecer `production.py` con variables de entorno.

2. Base SEO:
   - Extender `base.html` con canonical, robots, OG completo y JSON-LD.
   - Agregar robots.txt y sitemap.
   - Noindex para cuentas/perfil.

3. URLs y arquitectura:
   - Migrar recursos a slug.
   - Definir paginas publicas de asignaturas/niveles con URLs semanticas.
   - Agregar breadcrumbs.

4. UI estandarizada:
   - Consolidado el sistema visual base y los formularios principales.
   - Revisar mobile, estados de carga y futuras pantallas administrativas que hereden el mismo sistema.

5. Contenido y conversion:
   - Home con propuesta clara para clases particulares.
   - CTAs por etapa: explorar recursos, crear cuenta, contactar/profesor.
   - Copys por asignatura/nivel.

6. Medicion SEO:
   - Documentar alta y verificacion en Google Search Console.
   - Mantener sitemap y robots alineados con las URLs publicas activas.
   - Verificar dominio real antes de abrir indexacion completa.

7. Preparacion de despliegue:
   - Definir `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` y `DJANGO_CSRF_TRUSTED_ORIGINS` en el entorno final.
   - Revisar HTTPS, static files, cookies secure, sitemap, robots y cache en produccion.
   - No guardar secretos, IDs ni tokens reales dentro del repositorio.

## Validaciones ejecutadas

- `python manage.py check`: sin issues.
- `python manage.py check --deploy --settings=config.settings.production`: sin issues con variables temporales validas.
- `python manage.py test`: 29 tests ejecutados y OK.
- `python manage.py showmigrations --plan`: migraciones aplicadas.
- Conteo local: datos de ejemplo semillados para validacion visual de areas, asignaturas, niveles, temas, recursos y modulos.
