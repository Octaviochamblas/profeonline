# Auditoria Legal y Privacidad

Fecha de creacion: 2026-05-24
Estado: pendiente de ejecucion
Objetivo: preparar el sitio para operar con usuarios reales, datos personales, formularios, cookies y eventualmente estudiantes menores de edad.

## Alcance recomendado

- Registro de usuarios.
- Login y perfil.
- Formularios de contacto futuros.
- Cookies de sesion y CSRF.
- Google social auth.
- Analytics futuro.
- Archivos y recursos descargables.
- Footer legal.
- Politicas visibles.

## Documentos legales a definir

- Terminos de uso.
- Politica de privacidad.
- Politica de cookies si se agregan analytics o herramientas de terceros.
- Informacion de contacto.
- Bases o condiciones del servicio de clases particulares si aplica.
- Consentimiento para tratamiento de datos de estudiantes/menores si aplica.

## Datos personales a inventariar

- Nombre.
- Apellido.
- Email.
- Telefono.
- Ciudad.
- Institucion.
- Nivel educativo.
- Rol de usuario.
- Datos provistos por Google allauth.
- Logs tecnicos.
- Cookies de sesion/CSRF.

## Pasos de auditoria

1. Inventariar datos recolectados.
   - Modelo `User`.
   - Modelo `Profile`.
   - Formularios de registro/perfil.
   - Google allauth.
   - Logs y errores.

2. Definir base de tratamiento.
   - Para que se recolecta cada dato.
   - Donde se guarda.
   - Quien lo puede ver.
   - Cuanto tiempo se conserva.

3. Revisar consentimiento y transparencia.
   - Registro informa uso de datos.
   - Politica de privacidad accesible.
   - Contacto para solicitudes.
   - Consentimiento para menores si corresponde.

4. Revisar terceros.
   - Google allauth.
   - Google Fonts.
   - YouTube embeds.
   - Search Console.
   - Analytics futuro.
   - Hosting/base de datos.

5. Revisar cookies.
   - Sesion.
   - CSRF.
   - Cookies de terceros por YouTube/Google si aplica.
   - Cookies de analytics si se agregan.

6. Revisar derechos de usuario.
   - Acceso.
   - Rectificacion.
   - Eliminacion.
   - Contacto.

7. Revisar contenido y propiedad intelectual.
   - Recursos descargables.
   - Material educativo subido por admins.
   - Videos de YouTube.
   - Licencias o permisos.

## Checklist de hallazgos

| ID | Area | Riesgo | Recomendacion | Estado | Commit/documento |
| --- | --- | --- | --- | --- | --- |
| LEG-001 |  |  |  | Pendiente |  |

## Recomendaciones iniciales probables

- Crear rutas reales para `/terminos/`, `/privacidad/` y `/contacto/`.
- Cambiar footer legal de texto plano a enlaces cuando esas paginas existan.
- Agregar texto breve en registro apuntando a privacidad/terminos.
- No agregar analytics hasta decidir herramienta y politica de cookies.
- Documentar que Search Console no agrega tracking al usuario.
- Revisar si YouTube embed debe usar modo privacy-enhanced (`youtube-nocookie.com`).

## Criterios de aceptacion

- Politica de privacidad publicada y enlazada.
- Terminos de uso publicados y enlazados.
- Contacto visible.
- Datos recolectados y finalidad documentados.
- Cookies y terceros documentados.
- No hay scripts de medicion no declarados.

## Registro de cambios aplicados

| Fecha | Cambio | Archivo(s) | Validacion | Commit |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
