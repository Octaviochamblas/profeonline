# Auditoria de Conversion y Contenido

Fecha de creacion: 2026-05-24
Estado: completado y verificado
Objetivo: convertir la base SEO y visual en una experiencia que ayude a estudiantes/padres a entender la oferta y tomar una accion clara.

## Alcance recomendado

- Home.
- Landings de asignatura.
- Landings de nivel.
- Listado y detalle de recursos.
- Registro/login.
- Footer.
- Navegacion principal.
- CTAs.
- Mensajes de estados vacios.

## Intenciones SEO/comerciales principales

- "clases particulares online"
- "clases particulares de matematica"
- "clases particulares de fisica"
- "clases particulares de quimica"
- "clases particulares de ingles"
- "apoyo escolar"
- "reforzamiento [nivel]"
- "recursos para clases particulares"

## Pasos de auditoria

1. Revisar propuesta de valor.
   - Que ofrece ProfeOnline?
   - Para quien es?
   - Que problema resuelve?
   - Cual es la accion siguiente?

2. Revisar CTAs.
   - Home.
   - Asignatura.
   - Nivel.
   - Recurso.
   - Registro/login.
   - Estados vacios.

3. Revisar confianza.
   - Explicacion del proceso.
   - Beneficios concretos.
   - Material disponible.
   - Modalidad online.
   - Senales de seguridad/privacidad si corresponde.

4. Revisar interlinking.
   - Home -> asignaturas/niveles/recursos.
   - Asignatura -> temas/niveles/recursos.
   - Nivel -> asignaturas/recursos.
   - Recurso -> asignatura/tema/nivel/relacionados.

5. Revisar contenido por pagina.
   - H1 claro.
   - Intro especifica.
   - Texto util, no relleno SEO.
   - Recursos o temas relacionados.
   - CTA contextual.

6. Revisar formularios y conversion.
   - Registro no debe sentirse excesivo si el usuario solo quiere explorar.
   - Login/registro con mensajes claros.
   - Contacto futuro si se decide.

7. Revisar medicion.
   - Definir conversiones antes de agregar analytics.
   - Ejemplos: registro, click a asignatura, descarga, reproduccion de video, contacto.

## Checklist de hallazgos

| ID | Pagina | Problema | Recomendacion | Prioridad | Estado | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| CONV-001 | Home | Propuesta de valor genérica y poco atractiva en el banner principal | Ajustar el H1 y la descripción corta para reflejar mejor "Clases particulares online y material de apoyo a tu medida" | Media | Resuelto | |

## Recomendaciones iniciales probables

- Mejorar la home con una frase mas concreta sobre clases particulares online. (Completado)
- Agregar CTAs contextuales: "Ver recursos de Matematica", "Explorar niveles", "Crear cuenta". (Completado)
- Agregar FAQs en home/asignaturas cuando haya contenido visible que las respalde. (Pendiente)
- En asignaturas prioritarias, explicar problemas tipicos del estudiante y resultados esperados. (Completado)
- En niveles, conectar necesidades comunes con asignaturas y recursos. (Completado)
- Evitar paginas por ciudad/comuna hasta tener contenido local real. (Completado)

## Criterios de aceptacion

- En menos de 5 segundos se entiende que ofrece el sitio.
- Cada pagina publica tiene una accion siguiente clara.
- Las landings prioritarias tienen copy especifico y enlaces internos utiles.
- No hay CTAs repetitivos o contradictorios.
- El contenido no promete precios, disponibilidad, profesores o resultados no modelados.

## Registro de cambios aplicados

| Fecha | Cambio | Archivo(s) | Validacion | Commit |
| --- | --- | --- | --- | --- |
| 2026-05-24 | Optimización de título y copy de propuesta de valor en Home | `templates/pages/home.html` | Inspección visual y semántica | |
