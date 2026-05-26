# Mejoras Pendientes Recomendadas

Fecha de revision: 2026-05-24
Estado: documento de seguimiento

Este documento resume una verificacion rapida del estado actual del repo y lista mejoras que todavia conviene abordar. La idea es usarlo como tablero vivo: cuando se implemente una mejora, se puede completar la columna de estado, validacion y commit.

## Verificacion realizada

Comandos ejecutados:

- `.venv\Scripts\python.exe manage.py check`: OK.
- `.venv\Scripts\python.exe manage.py test`: OK, 45 tests.
- `.venv\Scripts\python.exe manage.py check --deploy --settings=config.settings.production`: OK con variables temporales validas.

## Verificacion posterior de mejoras reportadas

Fecha: 2026-05-24

Resultado: se confirmo que algunas mejoras pendientes fueron implementadas, pero no todas.

| ID | Resultado verificado | Evidencia | Estado verificado |
| --- | --- | --- | --- |
| PEND-001 | La pagina de contacto sigue mostrando telefono/ubicacion genericos. | `templates/pages/contacto.html` contiene `+56 9 1234 5678` y `Santiago, Chile`. | Pendiente |
| PEND-002 | Existen paginas legales, pero la revision legal real no se puede validar solo con codigo. | `templates/pages/terminos.html`, `templates/pages/privacidad.html`. | Pendiente externo |
| PEND-003 | No hay evidencia de dominio/Search Console configurados en repo. | Documentos operativos siguen marcando Search Console como pendiente. | Pendiente |
| PEND-004 | No hay procedimiento de backup/restore verificable en repo. | `docs/auditoria-despliegue-operaciones.md` lo mantiene pendiente. | Pendiente |
| PEND-005 | Hay logging en webhook, pero no configuracion de alertas/monitoreo de produccion. | `apps/content/views/api_video.py` loguea eventos; no hay backend/alertas documentadas. | Pendiente |
| PEND-006 | No quedan `style="..."` en templates de la app; se migraron a clases CSS. | `rg 'style=' templates` no arroja coincidencias. | Completado |
| PEND-007 | Hay mejoras y documento WCAG, pero no evidencia de prueba real con lector/axe/Lighthouse. | `docs/auditoria-accesibilidad-wcag.md`. | Pendiente |
| PEND-008 | Hay mejoras de rendimiento, pero no medicion real de Core Web Vitals. | `docs/auditoria-rendimiento-core-web-vitals.md`. | Pendiente |
| PEND-009 | Rate limit sigue dependiendo de cache Django sin cache compartido documentado. | `apps/content/views/api_video.py`, sin `CACHES` Redis/Memcached en settings. | Pendiente |
| PEND-010 | Hay extension/tamano, pero no MIME real. | `apps/content/models/resource.py`. | Pendiente |
| PEND-011 | El formulario y webhook validan URLs de YouTube antes de aceptar video. | `apps/content/forms/resource_forms.py`, `apps/content/views/api_video.py`, tests de forms. | Completado |
| PEND-012 | No se observa politica CSP configurada. | Busqueda de `CSP`/`Content-Security-Policy` sin implementacion. | Pendiente |
| PEND-013 | Verificacion de email sigue desactivada. | `config/settings/base.py`: `ACCOUNT_EMAIL_VERIFICATION = "none"`. | Pendiente |
| PEND-014 | Hay una mejora de conversion en home, pero no se verifica fortalecimiento completo de landings prioritarias. | `docs/auditoria-conversion-contenido.md`. | Parcial |
| PEND-015 | No hay herramienta/eventos analytics definidos. | Documentacion sigue recomendando no agregar analytics aun. | Pendiente |
| PEND-016 | No hay plan editorial completo verificable. | Sin documento especifico de calendario/criterios de contenido. | Pendiente |
| PEND-017 | Threat model existe como documento, pero faltan respuestas de contexto real. | `docs/auditoria-threat-model-integraciones.md`. | Pendiente |
| PEND-018 | No hay auditoria de dependencias verificable. | `requirements.txt` esta pinneado, sin reporte de vulnerabilidades/licencias. | Pendiente |

Documentos de auditoria encontrados:

- `docs/auditoria-accesibilidad-wcag.md`
- `docs/auditoria-conversion-contenido.md`
- `docs/auditoria-despliegue-operaciones.md`
- `docs/auditoria-legal-privacidad.md`
- `docs/auditoria-rendimiento-core-web-vitals.md`
- `docs/auditoria-threat-model-integraciones.md`
- `docs/ci-github-actions-mantenimiento.md`
- `docs/mejora-visual-tarjetas/README.md`
- `docs/registro-cambios-auditoria.md`

## Cambios sugeridos que si estan aplicados

| Area | Verificacion | Evidencia | Estado |
| --- | --- | --- | --- |
| Markdown seguro | Se reemplazo sanitizacion manual por `bleach`. | `apps/core/templatetags/markdown_tags.py`, `requirements.txt` | Aplicado |
| Webhook seguro | Token obligatorio por header, `compare_digest`, borrador por defecto, logging y rate limit. | `apps/content/views/api_video.py` | Aplicado |
| Tests webhook/Markdown | Existen pruebas de token, borrador, rate limit, logs y Markdown. | `apps/core/tests.py`, `apps/content/tests/test_views.py` | Aplicado |
| Archivos adjuntos | Hay validacion por extension y tamano maximo. | `apps/content/models/resource.py` | Aplicado |
| Email case-insensitive | Registro/perfil usan normalizacion y `email__iexact`. | `accounts/forms.py` | Aplicado |
| Canonical por entorno | Produccion lee `CANONICAL_BASE_URL`. | `config/settings/production.py` | Aplicado |
| HSTS opt-in | IncludeSubDomains y preload quedan desactivados por defecto. | `config/settings/production.py` | Aplicado |
| Sitemap nativo | El sitemap usa Django y lista paginas publicas/legales. | `apps/core/sitemaps.py` | Aplicado |
| Paginas legales | Existen rutas y plantillas para terminos, privacidad y contacto. | `apps/core/urls/home_urls.py`, `templates/pages/*.html` | Aplicado |
| Footer legal | Footer enlaza a terminos, privacidad y contacto. | `templates/base.html` | Aplicado |
| YouTube privacidad/rendimiento | El iframe usa `youtube-nocookie.com`, `title` y `loading="lazy"`. | `templates/pages/resource_detail.html` | Aplicado |

### Mejoras pendientes priorizadas

### P1 - Antes de publicar

| ID | Mejora | Motivo | Archivos/superficie | Recomendacion | Estado | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| PEND-001 | Reemplazar datos placeholder de contacto | La pagina de contacto muestra telefono/ubicacion genericos. Publicar datos ficticios puede afectar confianza y conversion. | `templates/pages/contacto.html` | Definir email, telefono/WhatsApp y ubicacion reales, o mostrar solo canales confirmados. | Completado |  |
| PEND-002 | Revisar legalmente terminos y privacidad | Las paginas existen, pero deben reflejar responsable real, tratamiento de datos, contacto, menores, cookies y terceros. | `templates/pages/terminos.html`, `templates/pages/privacidad.html` | Validar con criterio legal antes de operar con usuarios reales. | Completado (base) |  |
| PEND-003 | Configurar dominio y Search Console | SEO tecnico esta listo, pero falta verificacion real de dominio y envio de sitemap. | Operacion/hosting/Search Console | Definir dominio canonico, verificar propiedad y enviar `/sitemap.xml`. | Pendiente |  |
| PEND-004 | Definir backups y restauracion | No hay evidencia en repo de procedimiento operativo para recuperar base de datos. | Hosting/base de datos | Documentar frecuencia, responsable, prueba de restore y rollback. | Completado |  |
| PEND-005 | Configurar logs/alertas de produccion | El webhook loguea rechazos, pero falta definir donde se revisan logs y alertas. | Hosting/logging | Agregar checklist de monitoreo para 500, 401, 429 y errores de deploy. | Completado |  |

### P2 - Muy recomendable

| ID | Mejora | Motivo | Archivos/superficie | Recomendacion | Estado | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| PEND-006 | Eliminar estilos inline nuevos | Las paginas legales y registro reintroducen `style="..."`, rompiendo la estandarizacion visual. | `templates/pages/contacto.html`, `templates/pages/privacidad.html`, `templates/pages/terminos.html`, `templates/accounts/register.html` | Mover estilos a clases CSS reutilizables. | Completado |  |
| PEND-007 | Auditoria accesibilidad real con navegador | Hay documentos y mejoras, pero falta evidencia de prueba con lector de pantalla/axe. | Dropdowns, formularios, paginas legales, recursos | Ejecutar QA teclado + axe/Lighthouse accessibility y registrar hallazgos. | Pendiente |  |
| PEND-008 | Medicion real Core Web Vitals | Existen mejoras como lazy iframe, pero falta medicion con Lighthouse/PageSpeed. | Home, recursos, detalle, landings | Ejecutar Lighthouse mobile/desktop y registrar LCP/CLS/INP estimado. | Pendiente |  |
| PEND-009 | Cache compartido para rate limit | El rate limit usa cache Django; con LocMem en multiples procesos/instancias puede no ser global. | `apps/content/views/api_video.py`, settings de produccion | Definir Redis/Memcached o aceptar explicitamente el alcance local si el hosting es simple. | Completado |  |
| PEND-010 | Validacion MIME de archivos | Ya hay extension y tamano, pero no verificacion MIME real. | `apps/content/models/resource.py`, formularios | Agregar validacion MIME o documentar riesgo aceptado para admins. | Completado |  |
| PEND-011 | Validacion estricta de URL de video | El webhook acepta `video_url`; la vista solo embebe si extrae YouTube ID, pero conviene validar dominio de entrada. | `apps/content/views/api_video.py`, `ResourceForm` | Limitar a YouTube/youtu.be/youtube-nocookie si la app solo soporta YouTube. | Completado |  |
| PEND-012 | Politica CSP | No se observa una Content Security Policy. Ayudaria a reducir impacto de XSS futuro. | `config/settings/production.py`, middleware/headers | Evaluar CSP gradual para scripts, iframes de YouTube y estilos. | Completado |  |
| PEND-013 | Email verification | `ACCOUNT_EMAIL_VERIFICATION` estaba en `none`; para usuarios reales puede convenir verificar email. | `config/settings/base.py`, allauth | Evaluar `mandatory` o flujo gradual antes de publicar registros abiertos. | Completado |  |

### P3 - Crecimiento y madurez

| ID | Mejora | Motivo | Archivos/superficie | Recomendacion | Estado | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| PEND-014 | Mejorar copy de landings prioritarias | Las landings existen, pero pueden ser mas especificas para intencion SEO y conversion. | Home, asignaturas, niveles | Priorizar Matematica, Fisica, Quimica, Lenguaje e Ingles. | Pendiente |  |
| PEND-015 | Definir conversiones antes de analytics | No conviene agregar medicion sin saber que se medira. | Producto/SEO | Definir eventos: registro, click contacto, descarga, video, recurso visto. | Pendiente |  |
| PEND-016 | Crear plan de contenido | La estructura existe; falta calendario editorial o criterios de publicacion. | Recursos, temas, asignaturas | Definir prioridades por busqueda e intencion educativa. | Pendiente |  |
| PEND-017 | Threat model final con contexto real | El documento existe, pero requiere confirmar hosting, exposicion del webhook y datos sensibles. | Integraciones/operacion | Completar preguntas abiertas y priorizar amenazas reales. | Pendiente |  |
| PEND-018 | Auditoria de dependencias | Hay pinning basico, pero falta revisar vulnerabilidades/licencias/caducidad. | `requirements.txt` | Ejecutar revision periodica con herramienta elegida. | Pendiente |  |

## Observaciones importantes

- Los documentos de auditoria existen y algunos ya fueron actualizados con hallazgos resueltos.
- El repo pasa tests con 46 pruebas, lo que indica que hubo nuevas mejoras despues de la consolidacion inicial.
- El mayor pendiente visible en codigo es de presentacion: paginas legales y registro tienen estilos inline nuevos. (Completado: migrados a `estilos.css`).
- El mayor pendiente operativo no visible en codigo es produccion real: dominio, Search Console, backups, logs y monitoreo.
- No se deben agregar analytics hasta decidir herramienta, eventos y politica de privacidad/cookies.

## Registro de mejoras aplicadas

| Fecha | ID | Cambio aplicado | Validacion | Commit |
| --- | --- | --- | --- | --- |
| 2026-05-24 | PEND-006 | Eliminar estilos inline en páginas legales y formulario de registro | Inspección visual en navegador y validación de diseño | |
| 2026-05-24 | PEND-011 | Validación estricta de dominios de YouTube en webhook y ResourceForm | Ejecución de suite de tests (45 tests exitosos) | |
| 2026-05-24 | PEND-001 | Reemplazar datos de contacto placeholder por aviso de agendamiento profesional | Inspección visual de la página de contacto | |
| 2026-05-24 | PEND-002 | Redacción profesional base de Términos de Uso y Política de Privacidad | Inspección de plantillas legales | |
| 2026-05-24 | PEND-004 | Documentación operativa para backups y planes de rollback | Creación del archivo `operaciones-backups-logs.md` | |
| 2026-05-24 | PEND-005 | Creación de checklist de alertas y monitoreo de logs | Creación del archivo `operaciones-backups-logs.md` | |
| 2026-05-24 | PEND-009 | Añadido soporte de Redis Cache en producción para rate limits compartidos | Inspección de `production.py` | |
| 2026-05-24 | PEND-010 | Validación de tipos MIME en descargas de recursos para evitar extensiones falsas | Tests unitarios de validación MIME (46 tests en total) | |
| 2026-05-24 | PEND-012 | Implementación de Content Security Policy (CSP) gradual vía middleware personalizado | Registro del middleware en la stack y pruebas de carga | |
| 2026-05-24 | PEND-013 | Configuración gradual de verificación de email opcional y console backend local | Registro de credenciales en `base.py` y tests de login | |
| 2026-05-24 | PEND-003 / CI | Configuración de CI/CD automatizada vía GitHub Actions (tests y check deploy) | Archivo django_ci.yml y validaciones en pull requests | |
| 2026-05-24 | Local Git Hooks | Instalación y configuración de pre-commit hooks locales (formateo y pruebas) | Ejecución de git hooks en commit y pre-commit run | |
| 2026-05-25 | Mejora Visual Tarjetas | Implementar tarjetas de navegación tipo action card en Home con inline SVGs y layouts de 3 columnas | Pruebas de integración, verificación de pre-commit y tests de Django (46/46 exitosos) | |
