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

## Hallazgos prioritarios

### P1 - Borradores accesibles por URL directa

`ResourceListView` usa `get_published_resources()`, pero `ResourceDetailView` usa `DetailView` directo sobre `Resource`. Eso permite acceder por ID a recursos no publicados si existen.

Evidencia:
- `apps/content/views/resource_detail.py`: `model = Resource`
- `apps/content/models/resource.py`: `is_published = models.BooleanField(default=True)`
- `apps/content/urls/resource_urls.py`: `resources/<int:pk>/`

Recomendacion:
- Filtrar `ResourceDetailView.get_queryset()` por `is_published=True`, salvo para superusuarios.
- Agregar test de 404 para usuario anonimo ante recurso no publicado.

### P1 - Endpoint de recursos de modulo sin restriccion de publicacion/autorizacion

`module_resource_list` es publico y devuelve recursos asociados a cualquier `module_id`, sin validar que el modulo este publicado ni que los recursos asociados esten publicados.

Evidencia:
- `apps/content/views/module_resource_list.py`: `def module_resource_list(request, module_id)`
- `apps/content/views/module_resource_list.py`: `ModuleResource.objects.filter(module_id=module_id)`
- Los endpoints add/remove si tienen `@user_passes_test(is_admin)` y `@require_POST`.

Recomendacion:
- Si el endpoint es solo para admin, protegerlo igual que add/remove.
- Si es publico, filtrar modulo y recurso por `is_published=True`.

### P1 - Produccion no esta lista para despliegue seguro

`manage.py check --deploy --settings=config.settings.production` devuelve 6 warnings: HSTS no configurado, SSL redirect no configurado, `SECRET_KEY` insegura, cookies de sesion/CSRF no secure y `ALLOWED_HOSTS` vacio.

Evidencia:
- `config/settings/base.py`: `SECRET_KEY` hardcodeada con prefijo `django-insecure-`
- `config/settings/production.py`: `ALLOWED_HOSTS = []`
- Check deploy: `security.W004`, `W008`, `W009`, `W012`, `W016`, `W020`

Recomendacion:
- Cargar `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` y flags HTTPS desde variables de entorno.
- Mantener local simple; endurecer solo `production.py`.

### P2 - SEO tecnico incompleto

`base.html` tiene bloques para title/meta description/OG, pero faltan canonical, robots, `og:url`, `og:image`, structured data, sitemap y robots.txt. Ademas varias paginas no sobreescriben meta description.

Evidencia:
- `templates/base.html`: bloques `title`, `meta_description`, `og_title`, `og_description`
- No hay archivos ni rutas `robots.txt` o `sitemap.xml`
- Templates de login/register no definen title ni noindex.

Recomendacion:
- Agregar bloques SEO base: canonical, robots, OG url/image y structured_data.
- Crear sitemap para paginas publicas y robots.txt.
- Poner `noindex` en login, registro y perfil.

### P2 - URLs publicas no aprovechan slugs

Los modelos tienen `slug`, pero las URLs publicas y enlaces usan IDs numericos.

Evidencia:
- `Resource.slug`, `Subject.slug`, `Level.slug`, `Area.slug`, `Topic.slug`, `Module.slug`
- `apps/content/urls/resource_urls.py`: `resources/<int:pk>/`
- `templates/pages/resource_list.html`: link con `resource.pk`

Recomendacion:
- Migrar detalles publicos a slugs: por ejemplo `resources/<slug:slug>/`.
- Mantener redirects desde IDs si ya hay URLs compartidas.

### P2 - UX/UI inconsistente por exceso de estilos inline

La base CSS existe, pero muchas plantillas definen estilos inline, mezclan tema oscuro con tarjetas blancas y repiten patrones de formularios/tablas.

Evidencia:
- `templates/pages/home.html`: estilos inline en hero, H1, parrafo y CTA.
- `templates/pages/resource_list.html`: estilos inline extensos en filtros, tabla, paginacion y script local.
- `templates/pages/resource_detail.html` y `resource_form.html`: superficies blancas dentro de tema oscuro.
- `static/css/estilos.css`: tokens globales existen, pero no cubren todos los componentes usados.

Recomendacion:
- Crear componentes CSS: page-header, toolbar, form-panel, data-table, badge, pagination, detail-layout.
- Reemplazar estilos inline por clases.
- Mantener radios en 8px o menos salvo componentes grandes ya justificados.

### P2 - Arquitectura de contenido SEO aun no existe

Las listas de areas/asignaturas/niveles/temas son indices, no landing pages optimizadas por intencion de busqueda. No hay paginas por asignatura, nivel o ciudad/comuna con contenido unico.

Recomendacion:
- Empezar con paginas por asignatura y nivel antes que ciudad.
- Usar contenido real: modalidad, nivel, objetivos, recursos relacionados y CTA.
- Evitar paginas programaticas delgadas.

### P3 - Tests son placeholders

Los archivos de tests existen, pero no contienen pruebas ejecutables. `manage.py test` reporta `Ran 0 tests`.

Recomendacion:
- Agregar tests para permisos admin, drafts, filtros de recursos, registro/perfil y URLs SEO.

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
   - Extraer estilos inline a CSS.
   - Normalizar botones, formularios, tablas, cards y empty states.
   - Revisar mobile y estados de carga.

5. Contenido y conversion:
   - Home con propuesta clara para clases particulares.
   - CTAs por etapa: explorar recursos, crear cuenta, contactar/profesor.
   - Copys por asignatura/nivel.

## Validaciones ejecutadas

- `python manage.py check`: sin issues.
- `python manage.py check --deploy --settings=config.settings.production`: 6 warnings de seguridad.
- `python manage.py test`: 0 tests ejecutados.
- `python manage.py showmigrations --plan`: migraciones aplicadas.
- Conteo local: 0 recursos, 0 modulos, 0 asignaturas, 0 temas, 0 niveles, 0 areas, 1 usuario.
