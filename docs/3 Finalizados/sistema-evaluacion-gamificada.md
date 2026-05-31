# Sistema de evaluacion gamificada por recurso y tema

- **Estado:** Finalizado como MVP (Fases 1-6). Fases 7-9 separadas a tarjetas propias en
  `1 Por iniciar/` (`evaluacion-fase7-...`, `evaluacion-fase8-...`, `evaluacion-fase9-...`).
- **Creado:** 2026-05-31
- **Cerrado:** 2026-05-31 (MVP entregado a `main`)
- **Area:** Producto pedagogico / Gamificacion
- **Prioridad:** Alta (convierte recursos vistos en aprendizaje demostrado)

## Problema / Objetivo

Hoy el sitio distingue principalmente entre recurso visto (`ResourceView`) y recurso marcado
como completado (`ResourceCompletion`). Eso no prueba que el alumno haya entendido el video o
material. Para matematicas y ciencias, completar debe significar **demostrar dominio**:
entender conceptos, resolver ejercicios directos y aplicar lo aprendido en problemas.

Objetivo: crear un sistema con dos capas, **preparacion** y **evaluacion**, donde el alumno
pueda practicar, evaluarse, ganar experiencia, desbloquear skills y ver su dominio por recurso
y por tema.

## Propuesta

### Estados visuales del recurso

- **Sin ver:** no mostrar badge ni estado.
- **Visto:** mostrar badge amarillo "Visto".
- **Aprobado nivel 1:** mostrar verde + 1 estrella + marco simple.
- **Aprobado nivel 2:** mostrar verde + 2 estrellas + marco con brillo moderado.
- **Aprobado nivel 3:** mostrar verde + 3 estrellas + marco/resplandor destacado.

El color verde indica aprobacion. La cantidad de estrellas indica profundidad de dominio. El
brillo debe aumentar por nivel, sin volver la interfaz ruidosa.

### Capas del sistema

**Preparacion**
- Banco amplio de ejercicios por recurso y por nivel.
- Practica repetible, sin bloqueo.
- Feedback inmediato con respuesta correcta y explicacion breve.
- Otorga XP, pero con limite anti-farmeo para repetir la misma pregunta.
- Sirve para recuperar intentos de evaluacion si el alumno queda bloqueado.

**Evaluacion**
- Evaluacion formal por recurso, separada por nivel.
- Siempre seleccion multiple en la primera version.
- Cada evaluacion tiene 5 preguntas.
- Para aprobar se exige 5/5.
- Al enviar, mostrar cuales respuestas estuvieron correctas/incorrectas y una explicacion
  breve por pregunta.
- Permitir hasta 3 intentos por nivel.
- Si falla 3 veces, bloquear esa evaluacion de nivel.
- Para recuperar 1 intento, el alumno debe completar una seccion de preparacion del mismo
  nivel con al menos 80% correcto.

### Niveles por recurso

**Nivel 1: Conceptos e interpretacion**
- 5 preguntas conceptuales.
- Seleccion multiple.
- Evalua definiciones, interpretaciones, lectura de graficos, unidades y sentido fisico o
  matematico.
- Ejemplo: "Que representa la pendiente en esta grafica?".

**Nivel 2: Ejercicios directos**
- 5 ejercicios faciles o ligeros.
- Seleccion multiple.
- Evalua aplicacion directa de formulas, procedimientos y calculos cortos.
- Ejemplo: "Calcula la aceleracion si la velocidad cambia de 2 m/s a 10 m/s en 4 s".

**Nivel 3: Problemas aplicados**
- 5 problemas con enunciado.
- Seleccion multiple.
- Evalua interpretar datos, elegir el concepto correcto y resolver una situacion aplicada.
- Ejemplo: "Un objeto cae desde cierta altura; identifica que modelo usar y calcula el tiempo".

### Evaluacion final por tema

- Compila preguntas de los recursos del tema.
- Guarda nota/porcentaje, numero de intentos, mejor nota y fecha.
- Umbral recomendado de aprobacion: 80%.
- Al aprobar, el tema cambia a verde.
- Mientras mejor sea la nota, mas brillante/resplandeciente se muestra el tema.
- Al aprobar el tema, se desbloquea una skill relacionada con ese tema.

### Gamificacion

- Otorgar XP por:
  - practicar;
  - aprobar nivel 1/2/3 de recurso;
  - recuperar intentos con practica;
  - aprobar evaluacion final de tema;
  - mantener racha diaria/semanal.
- Crear skills asociadas a temas aprobados.
- Subir categoria/rango segun XP, skills y profundidad de dominio.
- Mostrar progreso por tema como:
  - recursos vistos;
  - recursos aprobados;
  - estrellas acumuladas;
  - evaluacion final aprobada;
  - skill desbloqueada.

### Reportes de errores de evaluacion

- Cada pregunta debe tener boton "Reportar error".
- Motivos sugeridos:
  - respuesta correcta equivocada;
  - enunciado confuso;
  - alternativas ambiguas;
  - error de redaccion/formato;
  - explicacion insuficiente.
- Guardar el reporte en base de datos con estado:
  - nuevo;
  - revisando;
  - resuelto;
  - descartado.
- Mostrar reportes en el admin para revision del staff.
- Enviar email a `contacto@profeonline.cl` usando la configuracion de email existente
  (Brevo/API HTTP).

## Tareas de implementacion

### Fase 1 - Modelado de datos

- Mantener `ResourceView` como fuente de "visto".
- Mantener compatibilidad con `ResourceCompletion`, pero evolucionar hacia progreso evaluado.
- Definir modelos para:
  - preguntas de quiz/evaluacion;
  - alternativas;
  - intentos;
  - respuestas de intentos;
  - sesiones de preparacion;
  - reportes de error;
  - XP/eventos de gamificacion;
  - skills desbloqueadas;
  - progreso final por tema.
- Registrar intentos por usuario, recurso, nivel y modo (`preparacion`, `evaluacion`,
  `evaluacion_tema`).
- Guardar:
  - puntaje;
  - aprobado/no aprobado;
  - numero de intento;
  - fecha;
  - intentos restantes;
  - intentos recuperados por practica.

### Fase 2 - Autoria de preguntas

- Permitir al staff crear preguntas desde el admin.
- Cada pregunta debe tener:
  - recurso o tema asociado;
  - nivel 1/2/3;
  - modo (`preparacion`, `evaluacion`, ambas);
  - enunciado;
  - alternativas;
  - alternativa correcta;
  - explicacion breve;
  - estado (`borrador`, `publicada`, `archivada`).
- Las preguntas generadas por IA quedan como `borrador` hasta revision humana.
- Permitir banco grande de preguntas para que la evaluacion tome 5 al azar por nivel.

### Fase 3 - Evaluacion por recurso

- Renderizar en `resource_detail` una seccion "Demuestra lo aprendido".
- Mostrar tabs o bloques:
  - Preparacion nivel 1/2/3.
  - Evaluacion nivel 1/2/3.
- La evaluacion formal debe seleccionar 5 preguntas disponibles del nivel correspondiente.
- Aprobar solo con 5/5.
- Mostrar feedback por pregunta despues de enviar.
- Registrar intento y actualizar estrellas si aprueba.
- Bloquear evaluacion del nivel tras 3 fallos.
- Mostrar llamada a la accion para recuperar intento mediante preparacion.

### Fase 4 - Preparacion y recuperacion de intentos

- Crear secciones de practica por nivel.
- La practica puede repetirse sin limite.
- Registrar porcentaje de practica.
- Si la practica del mismo nivel alcanza al menos 80%, recuperar 1 intento de evaluacion.
- Evitar que el alumno acumule intentos infinitos: maximo recomendado de intentos disponibles
  por nivel = 3.
- Otorgar XP por practica, con reduccion si repite exactamente la misma seccion muchas veces.

### Fase 5 - UI de progreso y estrellas

- Actualizar tarjetas de recurso para mostrar:
  - nada si no visto;
  - badge amarillo "Visto";
  - estado verde si aprobado;
  - 1/2/3 estrellas segun maximo nivel aprobado;
  - marco/resplandor segun nivel.
- Actualizar detalle de tema para mostrar:
  - progreso de recursos vistos;
  - progreso de recursos aprobados;
  - estrellas acumuladas;
  - evaluacion final;
  - skill desbloqueada.
- El feedback visual no debe depender solo de color: usar texto, iconos/estrellas y labels.

### Fase 6 - Reportes de errores

- Crear formulario/modal "Reportar error" asociado a pregunta.
- Guardar reporte en base de datos.
- Enviar email a `contacto@profeonline.cl`.
- Permitir al staff cambiar estado del reporte desde admin.
- Guardar datos utiles:
  - usuario;
  - pregunta;
  - recurso/tema;
  - intento relacionado;
  - motivo;
  - comentario;
  - fecha;
  - estado.

### Fase 7 - Evaluacion final por tema

- Crear evaluacion final para `Topic`.
- Tomar preguntas de los recursos del tema o preguntas especificas de tema.
- Guardar:
  - nota/porcentaje;
  - intento;
  - mejor nota;
  - aprobado/no aprobado;
  - fecha.
- Si aprueba con 80% o mas:
  - marcar tema como aprobado;
  - aplicar color verde;
  - aumentar brillo segun nota;
  - desbloquear skill del tema;
  - otorgar XP.

### Fase 8 - Gamificacion

- Crear registro de eventos XP.
- Definir valores iniciales sugeridos:
  - practicar una seccion: 5 XP;
  - practicar con 80% o mas: 15 XP;
  - aprobar nivel 1: 25 XP;
  - aprobar nivel 2: 40 XP;
  - aprobar nivel 3: 60 XP;
  - aprobar evaluacion final de tema: 100 XP;
  - skill desbloqueada: bonus 50 XP.
- Crear categorias/rangos por XP total y skills aprobadas.
- Mostrar XP y skills en perfil.

### Fase 9 - Generacion asistida de preguntas

- Codex/IA puede preparar preguntas, alternativas, respuesta correcta y explicacion breve a
  partir de:
  - titulo del recurso;
  - contenido escrito;
  - transcripcion del video si existe;
  - nivel educativo;
  - objetivo de aprendizaje.
- Las preguntas generadas no se publican automaticamente.
- Deben quedar como borrador para revision de staff.

## Criterios de aceptacion

- Un recurso visto muestra badge amarillo.
- Un recurso aprobado muestra verde y estrellas segun nivel maximo aprobado.
- La evaluacion de recurso exige 5/5.
- El alumno tiene 3 intentos por nivel.
- Tras 3 fallos, la evaluacion queda bloqueada.
- La practica con 80% correcto recupera 1 intento.
- Cada pregunta permite reportar error.
- El reporte queda en admin y envia email.
- La evaluacion final de tema registra nota e intentos.
- Aprobar un tema desbloquea una skill y otorga XP.
- La UI es accesible por teclado y no depende solo del color.

## Tests necesarios

- Modelos:
  - estados visto/aprobado/estrellas;
  - limite de 3 intentos;
  - bloqueo tras 3 fallos;
  - recuperacion con practica >= 80%;
  - evaluacion final de tema;
  - XP y skills.
- Vistas:
  - recurso sin ver no muestra badge;
  - recurso visto muestra amarillo;
  - aprobacion nivel 1/2/3 muestra estrellas correctas;
  - evaluacion falla con menos de 5/5;
  - evaluacion aprueba con 5/5;
  - practica recupera intento;
  - reportar error guarda y envia email.
- Admin:
  - staff puede crear preguntas/opciones;
  - staff puede revisar reportes;
  - preguntas generadas por IA quedan en borrador.
- Manual:
  - navegacion por teclado;
  - lector de pantalla;
  - contraste de badges/estrellas/brillos;
  - flujo completo recurso -> practica -> evaluacion -> tema.

## Notas / Consideraciones

- No construir un motor de examenes enorme en la primera iteracion. Implementar por fases.
- Prioridad recomendada:
  1. Estados visuales y progreso evaluado.
  2. Evaluacion por recurso nivel 1.
  3. Niveles 2 y 3.
  4. Preparacion y recuperacion de intentos.
  5. Reportes.
  6. Evaluacion final por tema.
  7. XP/skills/rangos.
- El sistema debe evitar que el alumno memorice siempre las mismas 5 respuestas: usar banco
  amplio y seleccion aleatoria controlada.
- Para matematicas/ciencias, la explicacion breve por pregunta es parte central del valor
  pedagogico.

---

## Que se hizo

### MVP Fases 1-6 implementado en rama `feat/evaluacion-gamificada-mvp` (2026-05-31)

- Se movio la epica desde `docs/1 Por iniciar/` a `docs/2 En Proceso/`.
- Se agregaron modelos para preguntas, alternativas, intentos, respuestas y reportes de error:
  `Question`, `Choice`, `QuizAttempt`, `QuizAttemptAnswer`, `QuestionErrorReport`.
- Se genero la migracion `0017_evaluacion_gamificada`.
- Se agrego logica de negocio para seleccionar preguntas, enviar intentos, bloquear tras 3
  fallos, recuperar intento con practica >= 80% y calcular dominio/estrellas.
- Se agregaron selectores de progreso para renderizar visto/aprobado/estrellas en listados y
  detalle de tema.
- Se agrego admin para preguntas con alternativas inline, intentos read-only y reportes de
  error gestionables por estado.
- Se agregaron vistas HTMX para iniciar quiz, enviar respuestas, refrescar estado, recuperar
  intento y reportar error.
- Se agregaron templates de seccion/formulario/resultados/bloqueos/errores/confirmacion.
- Se integro la seccion "Demuestra lo aprendido" en el detalle de recurso.
- Se integro estado visual en `resource_list` y `topic_detail`: visto amarillo, aprobado verde
  y 1/2/3 estrellas con brillo progresivo.
- Se agregaron estilos CSS para quiz, opciones, resultados, bloqueos, badges y estrellas.
- Se actualizo el cache buster de `estilos.css` a `?v=11`.
- Se corrigio una validacion de seguridad: una alternativa de otra pregunta ya no puede contar
  como correcta si se manipula el POST.
- Se corrigio el envio con preguntas sin responder: quedan registradas como incorrectas y se
  muestran como "Sin responder".
- Se corrigio el refresco de nivel ya aprobado para usar `quiz_section.html` existente.

### Verificacion

- `apps.content.tests.test_evaluation`: 37/37 OK.
- `apps.content.tests.test_completion` + `apps.content.tests.test_evaluation`: 41/41 OK.
- Suite completa: 124/124 OK.
- `.venv\Scripts\python.exe manage.py check`: sin issues.
- `.venv\Scripts\python.exe manage.py makemigrations --check --dry-run`: sin cambios.

### Pendiente fuera del MVP (separado a tarjetas propias)

Al cerrar el MVP, las fases restantes se movieron a `1 Por iniciar/` como tarjetas
independientes (la epica advierte: "implementar por fases", no construir el motor completo de
una vez):

- Fase 7 -> `docs/1 Por iniciar/evaluacion-fase7-evaluacion-final-tema.md`.
- Fase 8 -> `docs/1 Por iniciar/evaluacion-fase8-xp-skills-rangos.md`.
- Fase 9 -> `docs/1 Por iniciar/evaluacion-fase9-generacion-ia-preguntas.md`.

### Pendiente del MVP que requiere al usuario (no bloquea el cierre)

- Verificacion manual en navegador: flujo alumno/staff, teclado, lector de pantalla y revision
  visual fina de badges/estrellas. No se pudo automatizar (sin herramienta de navegador en la
  sesion de cierre); queda como QA del usuario sobre lo ya desplegado.
