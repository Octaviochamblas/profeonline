# Auditoria SEO, UI/UX y Seguridad

Fecha: 2026-05-24
Rama revisada: `main`

## Resumen ejecutivo

La base del sitio avanzo bastante: hay URLs en espanol, landings por asignatura y nivel, sitemap con entidades publicas, robots.txt, canonical, metadata, UI oscura unificada, filtros de recursos corregidos, contenido semilla, HTMX local, WhiteNoise y settings de produccion separados.

El principal bloqueo para publicar no es SEO ni UI: es operativo/seguridad. `config/settings/production.py` tiene un `SyntaxError` por una llave sobrante, por lo que `check --deploy` no puede ejecutarse. Ademas, las dos integraciones nuevas de mayor riesgo, Markdown y webhook de videos, necesitan endurecimiento antes de exponer el sitio a internet.

## Validaciones ejecutadas

- `.venv\Scripts\python.exe manage.py check`: OK.
- `.venv\Scripts\python.exe manage.py test`: OK, 29 tests.
- `.venv\Scripts\python.exe manage.py check --deploy --settings=config.settings.production`: falla antes de correr por `SyntaxError: unmatched '}'` en `config/settings/production.py:73`.
- `git status --short`: limpio al momento de la auditoria.

## Cambios documentados revisados

Fuente principal revisada: `docs/actualizacion-auditoria-integraciones.md`.

El documento registra integraciones reales que ya aparecen en el codigo: PostgreSQL/Supabase por `DATABASE_URL`, WhiteNoise, validacion de email unico, allauth Google, HTMX local, `SECURE_REFERRER_POLICY`, archivos adjuntos, video URL, webhook de creacion de videos, buscador, Markdown, dropdowns accesibles, mensajes flash, sitemap nativo y robots.txt.

Riesgo documental: el archivo se ve con mojibake de codificacion (`DocumentaciÃ³n`, `ðŸ...`). Conviene normalizarlo a UTF-8 y usarlo como changelog tecnico, no como auditoria final, porque describe cambios pero no valida riesgos residuales.

## Hallazgos criticos

### C1. Produccion no puede iniciar con los settings actuales

Ubicacion: `config/settings/production.py:67-73`

Evidencia:

```python
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
}
```

Impacto: el entorno de produccion no puede importar settings, por lo que falla cualquier despliegue, `check --deploy`, `collectstatic` con settings de produccion o arranque WSGI/ASGI.

Correccion recomendada: eliminar la llave sobrante de la linea 73 y volver a ejecutar `check --deploy` con variables temporales.

## Hallazgos altos

### A1. Markdown renderiza HTML sin sanitizar

Ubicacion: `apps/core/templatetags/markdown_tags.py:12-13`, usado en `templates/pages/resource_detail.html:80-82`.

Evidencia:

```python
html = md.markdown(value, extensions=["fenced_code", "tables", "nl2br"])
return mark_safe(html)
```

Impacto: si el contenido de un recurso contiene HTML o JavaScript malicioso, se marca como seguro y se renderiza en la pagina publica. El riesgo aumenta porque el webhook tambien puede escribir `content`.

Correccion recomendada: sanitizar la salida con una lista permitida de tags/atributos, por ejemplo con `bleach`, o desactivar HTML crudo antes de usar `mark_safe`. Agregar test con payload tipo `<script>`.

### A2. El webhook permite token conocido por defecto y publica por defecto

Ubicacion: `apps/content/views/api_video.py:10-14`, `apps/content/views/api_video.py:26-30`, `apps/content/views/api_video.py:38`, `apps/content/urls/resource_urls.py:19`.

Evidencia:

```python
@csrf_exempt
expected_token = os.environ.get("API_SECRET_TOKEN", "default_secret_token_change_me")
...
if not token:
    token = data.get("token")
...
is_published = data.get("is_published", True)
```

Impacto: si `API_SECRET_TOKEN` no esta configurado, existe un token conocido. Ademas el endpoint esta exento de CSRF, acepta token en el cuerpo y publica recursos por defecto. Un abuso podria crear o modificar contenido publico.

Correccion recomendada: fallar cerrado si falta `API_SECRET_TOKEN`, exigir token solo por header, comparar con `secrets.compare_digest`, registrar intentos fallidos, limitar metodo/contenido/tamano y dejar `is_published=False` por defecto salvo aprobacion explicita.

## Hallazgos medios

### M1. Subida de archivos sin validacion de tipo ni tamano

Ubicacion: `apps/content/models/resource.py:35-40`, `apps/content/forms/resource_forms.py:6-18`, `templates/pages/resource_detail.html:68-75`.

Impacto: el formulario permite adjuntar archivos sin validadores visibles de extension, MIME o tamano. Aunque solo admins creen recursos, los archivos quedan servidos desde `MEDIA_ROOT` y enlazados publicamente.

Correccion recomendada: limitar a formatos esperados (`pdf`, `docx`, `pptx`, imagenes si aplica), definir tamano maximo, validar MIME cuando sea posible y servir descargas con cabeceras seguras si se requiere mas control.

### M2. Canonical fijo puede quedar desalineado con el dominio real

Ubicacion: `config/settings/base.py:175`, `apps/core/context_processors.py:4-12`, `templates/base.html:10`.

Evidencia: `CANONICAL_BASE_URL = "https://www.profeonline.cl"`.

Impacto SEO: si el dominio final, www/no-www o entorno de produccion no coincide exactamente, las canonicals y Open Graph pueden apuntar a una URL distinta de la URL servida. Esto confunde indexacion, sitemap y Search Console.

Correccion recomendada: mover `CANONICAL_BASE_URL` a variable de entorno obligatoria o documentada para produccion, y alinear dominio, redirects, `ALLOWED_HOSTS`, sitemap y Search Console.

### M3. HSTS preload e includeSubDomains estan activos por defecto

Ubicacion: `config/settings/production.py:43-49`.

Impacto: es bueno exigir HTTPS, pero `includeSubDomains` y `preload` por defecto pueden bloquear subdominios si todavia no estan preparados con HTTPS. Es un riesgo operativo antes de tener dominio definitivo.

Correccion recomendada: mantener HTTPS/cookies secure, pero hacer `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` y `DJANGO_SECURE_HSTS_PRELOAD` opt-in despues de validar dominio y subdominios.

### M4. Email unico es case-sensitive

Ubicacion: `accounts/forms.py:42-46`, `accounts/forms.py:85-93`.

Impacto: `User.objects.filter(email=email).exists()` puede permitir variantes por mayusculas/minusculas segun base de datos y collation. Puede generar duplicados logicos y problemas con login o recuperacion.

Correccion recomendada: normalizar email a lowercase y validar con `email__iexact`. Idealmente agregar constraint o indice case-insensitive si el flujo de cuentas sera relevante.

## Hallazgos SEO

### S1. Base SEO tecnica esta bien encaminada

Evidencia:

- `templates/base.html:3-16`: `lang="es-CL"`, title/meta defaults, robots, canonical y OG.
- `apps/core/sitemaps.py:6-36`: sitemap para asignaturas activas, niveles activos y recursos publicados.
- `templates/pages/subject_detail.html:3-10` y `templates/pages/level_detail.html:3-10`: metadata y JSON-LD por pagina.
- `templates/pages/resource_detail.html:4-11`: metadata y structured data para recurso.

Impacto: el sitio ya tiene una base indexable razonable para "clases particulares" por asignatura, nivel y recursos.

### S2. Sitemap incluye listados potencialmente delgados

Ubicacion: `apps/core/sitemaps.py:43-52`.

Incluye `area_list`, `topic_list` y `module_list`. Esto no es incorrecto, pero si esas paginas tienen poco contenido real o estados vacios, pueden consumir crawl budget con bajo valor.

Recomendacion: mantenerlas si tienen contenido semantico suficiente; si no, enriquecerlas o considerar `noindex` temporal hasta que tengan contenido real.

### S3. Sitemap manual antiguo quedo en codigo

Ubicacion: `apps/core/views/seo.py:36-86`.

Impacto: el sitemap real usa `django.contrib.sitemaps`, pero queda una funcion manual antigua. No rompe SEO hoy, pero puede causar confusion y tests duplicados.

Recomendacion: eliminar `sitemap_xml` manual o dejar comentario claro de deprecacion, manteniendo solo `robots_txt` si es la vista usada.

### S4. Home y landings estan correctas, pero aun genericas

Evidencia:

- Home: `templates/pages/home.html:21-43`, `templates/pages/home.html:46-68`.
- Asignatura: `templates/pages/subject_detail.html:46-50`, `templates/pages/subject_detail.html:54-107`.
- Nivel: `templates/pages/level_detail.html:35-40`, `templates/pages/level_detail.html:43-91`.

Impacto: funcionan bien como base, pero para competir por "clases particulares de matematica", "clases de fisica online", etc., cada landing necesita copy mas especifico, preguntas frecuentes y CTAs mas orientados a conversion.

## Hallazgos UI/UX

### U1. Quedan estilos inline importantes

Ubicacion: `templates/base.html:76-114`, `templates/pages/resource_detail.html:62-75`, `templates/pages/resource_list.html:35`.

Impacto: despues del trabajo de estandarizacion, estos estilos inline son deuda visual. Dificultan mantener consistencia, responsive y temas.

Recomendacion: moverlos a clases reutilizables: alerts, footer, video embed, attachment panel y spacing de busqueda.

### U2. El footer muestra elementos legales como texto clickeable sin destino real

Ubicacion: `templates/base.html:104-108`.

Impacto: "Terminos de uso", "Privacidad" y "Contacto" parecen acciones, pero son `span`. Esto genera expectativa rota y debilita confianza antes de publicar.

Recomendacion: crear paginas reales o quitar apariencia de enlace hasta tener contenido legal/contacto.

### U3. Busqueda HTMX no limita longitud visible ni comunica resultados

Ubicacion: `templates/pages/resource_list.html:25-44`, `apps/content/views/resource_list.py:40-47`.

Impacto: la busqueda funciona, pero no hay limite de longitud ni resumen tipo "resultados para X". En movil puede sentirse opaco cuando no hay resultados.

Recomendacion: limitar longitud del query, mostrar chip de busqueda activa ya existe parcialmente, y mejorar estado vacio con accion "Limpiar filtros".

### U4. Dropdown custom avanzado requiere QA de accesibilidad real

Ubicacion: `static/js/enhanced-select.js:54-203`.

Impacto: se agrego soporte de teclado y ARIA parcial, pero al ocultar el `<select>` nativo con `display:none` y reemplazarlo por botones/lista, conviene probar con lector de pantalla, foco, Escape/Tab y navegacion movil.

Recomendacion: hacer auditoria WCAG con teclado y Playwright, y si se detectan problemas, usar select nativo en movil o mejorar roles ARIA.

## Hallazgos de documentacion

### D1. La auditoria principal y la actualizacion de integraciones no estan sincronizadas

Ubicacion: `docs/auditoria-estandarizacion.md`, `docs/actualizacion-auditoria-integraciones.md`.

Impacto: una documenta el camino de estandarizacion y otra lista integraciones nuevas, pero no hay un unico estado final que priorice riesgos. Esta auditoria cubre ese hueco.

Recomendacion: despues de corregir C1/A1/A2, actualizar `docs/auditoria-estandarizacion.md` con el estado real y mover `actualizacion-auditoria-integraciones.md` a changelog o normalizarlo.

## Prioridad recomendada

1. Corregir `config/settings/production.py` y confirmar `check --deploy`.
2. Sanitizar Markdown y agregar tests anti-XSS.
3. Endurecer webhook de videos y agregar tests de token faltante/default/publicacion.
4. Validar archivos subidos por extension/tamano/MIME.
5. Mover `CANONICAL_BASE_URL` a configuracion por entorno.
6. Limpiar estilos inline y footer legal.
7. Afinar landings con copy mas especifico, FAQs y CTAs.
8. Quitar sitemap manual antiguo o documentar su deprecacion.

## Auditorias adicionales recomendadas

1. Auditoria de accesibilidad WCAG: teclado, foco, contraste, lector de pantalla, formularios, dropdowns custom y estados de error.
2. Auditoria de rendimiento/Core Web Vitals: peso CSS/JS, fuentes externas, cache, CLS, LCP, imagen OG/assets y respuesta del servidor.
3. Auditoria de contenido/conversion: claridad de oferta, CTAs, confianza, preguntas frecuentes, proceso de clases, contacto y rutas de captacion.
4. Threat model de integraciones: webhook, agente de YouTube, archivos, Markdown, roles admin y flujo de publicacion.
5. Auditoria legal/privacidad: terminos, politica de privacidad, cookies, tratamiento de datos de menores/estudiantes, contacto y consentimiento.
6. Auditoria de despliegue/operaciones: backups, restauracion, logs, monitoreo, alertas, rotacion de secretos, dominio, HTTPS y rollback.
7. Auditoria de dependencias: vulnerabilidades conocidas, caducidad de versiones, pinning, licencias y plan de actualizacion.
