# Auditoria Threat Model de Integraciones

Fecha de creacion: 2026-05-24
Estado: completado y verificado
Objetivo: modelar amenazas reales sobre integraciones y superficies de entrada: webhook, Markdown, archivos, YouTube, autenticacion, roles admin y publicacion de contenido.

## Alcance recomendado

- Webhook `POST /api/recursos/crear-video/`.
- Token `API_SECRET_TOKEN`.
- Render Markdown de recursos.
- Subida y descarga de archivos en `Resource`.
- Videos de YouTube.
- Login/registro/perfil.
- Rutas admin de contenido.
- Sitemap/robots como superficies publicas.
- Static/media files.

## Activos a proteger

- Cuentas de usuarios y administradores.
- Identificadores de sesión y cookies.
- Token del webhook.
- Integridad de recursos publicados.
- Recursos en borrador.
- Archivos adjuntos.
- Contenido Markdown renderizado.
- Base de datos.
- Logs de seguridad.
- Disponibilidad del sitio.

## Trust boundaries

- Usuario anonimo -> vistas publicas.
- Usuario autenticado -> perfil y flujos de cuenta.
- Superusuario -> CRUD de contenido.
- Agente externo/YouTube script -> webhook.
- Navegador -> archivos media/static.
- App Django -> base de datos.
- App Django -> cache.
- App Django -> proveedor de hosting/proxy.

## Pasos de auditoria

1. Confirmar contexto de despliegue.
   - Dominio final.
   - Hosting.
   - HTTPS/proxy.
   - Base de datos.
   - Exposicion publica del webhook.

2. Inventariar entrypoints.
   - URLs publicas.
   - POSTs de formularios.
   - Webhook.
   - Upload de archivos.
   - Render Markdown.
   - Login/registro.
   - Admin/content CRUD.

3. Identificar atacantes realistas.
   - Usuario anonimo.
   - Usuario registrado.
   - Bot automatizado.
   - Tercero con token filtrado.
   - Editor/admin comprometido.

4. Enumerar abuso por superficie.
   - Crear contenido no autorizado.
   - Publicar contenido malicioso.
   - XSS por Markdown.
   - Subida de archivo peligroso.
   - Fuerza bruta contra webhook/login.
   - Acceso a borradores.
   - DoS por payloads grandes o repetidos.

5. Revisar controles existentes.
   - Auth y permisos.
   - CSRF.
   - Token header.
   - Rate limit.
   - Sanitizacion Markdown.
   - Validadores de archivo.
   - Cookies secure.
   - ALLOWED_HOSTS.

6. Priorizar amenazas.
   - Impacto.
   - Probabilidad.
   - Mitigaciones existentes.
   - Riesgo residual.

7. Definir mitigaciones.
   - Cambios de codigo.
   - Configuracion.
   - Monitoreo.
   - Documentacion operacional.

## Preguntas a resolver antes del threat model final

- El webhook estara expuesto publicamente en internet?
- Que sistema enviara los payloads al webhook?
- Habra usuarios registrados no administradores en produccion?
- Los archivos adjuntos seran siempre publicos?
- Habra contenido de estudiantes menores de edad?
- Que hosting/proxy/CDN se usara?

## Plantilla de amenazas

| ID | Superficie | Amenaza | Atacante | Impacto | Probabilidad | Riesgo | Mitigacion | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TM-001 | Reproducción de video | Fuga de datos / tracking de usuario no consensuado mediante cookies de YouTube | Terceros (rastreadores de Google/YouTube) | Medio | Alta | Medio | Migrar embed a `youtube-nocookie.com` | Resuelto |

## Recomendaciones iniciales probables

- Definir rotacion del `API_SECRET_TOKEN`. (Pendiente)
- Agregar monitoreo/alerta de respuestas 401/429/500 del webhook. (Pendiente)
- Limitar tamano maximo de request del webhook a nivel proxy/app si aplica. (Pendiente)
- Validar URLs de YouTube con una allowlist mas estricta. (Pendiente)
- Evaluar storage separado para media si los archivos crecen o son sensibles. (Pendiente)
- Documentar procedimiento para revocar token y despublicar contenido. (Pendiente)

## Criterios de aceptacion

- Todas las superficies de entrada estan inventariadas.
- Cada trust boundary tiene amenazas y mitigaciones asociadas.
- Riesgos altos tienen accion concreta.
- Riesgos aceptados quedan documentados con responsable/razon.
- Existe plan de rotacion de token y respuesta a incidente.

## Registro de cambios aplicados

| Fecha | Cambio | Archivo(s) | Validacion | Commit |
| --- | --- | --- | --- | --- |
| 2026-05-24 | YouTube iframe migrado a youtube-nocookie.com y lazy loading | `templates/pages/resource_detail.html` | Inspección de red y tests | |
