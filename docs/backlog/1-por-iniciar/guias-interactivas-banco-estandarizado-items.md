# Guías interactivas y banco estandarizado por ítems

- **Estado:** Por iniciar (EPIC — requiere descomposición en fases antes de construir)
- **Creado:** 2026-06-22
- **Prioridad:** P1 · **Cartera:** educativa
- **Tipo:** producto · pedagogía · seguridad
- **Dueño sugerido:** 🏛️ Claude (handoff por fase) → 🧩 Codex (preflight) → 🔨 Antigravity (construye) → 🧩 Codex (audita) → 🏛️ Claude (cierre)

> ⚠️ **No es una sola tarjeta de construcción.** Es un epic grande. La construcción se hará
> **fase por fase**, cada una con su propio handoff Ready y su gate. Esta tarjeta es la visión
> maestra; al arrancar cada fase se crea (o deriva) su tarjeta hija.

## Objetivo (una frase)
Convertir cada guía subida (privada) en una fuente que la IA analiza para producir ítems de
aprendizaje revisados por el profesor, una guía ProfeOnline **original** (no copia), un banco
visible por ítem/dificultad y bancos ocultos para evaluaciones por nivel + prueba final, con
corrección de respuesta directa y dominio académico ponderado.

## Fuentes a leer (rutas concretas)
- `apps/content/models/` (Question, Resource, Topic, QuizGuide, publication_pipeline).
- `apps/content/services/ai_generation_service.py` · `publication_pipeline_service.py` ·
  `guide_service.py` (reuso de prompts, `_loads_ai_json`, modo JSON, KaTeX ya integrado).
- `apps/content/services/progress_service.py` y selectores de progreso (dominio actual 30/70).
- `static/js/quiz-player.js` + plantillas de quiz (reproductor fullscreen existente).
- Preferencia del 🧑: **paneles admin propios** (no Django admin), config-driven.
- Decisión vigente: **publicar directo** (no borradores) — revisar contra "nada se publica
  automáticamente" de este epic (ver Riesgos / decisiones abiertas).

## Propuesta — descomposición en fases (cada una = handoff + gate propio)

Cada fase es aditiva y queda **detrás del flag por tema** (los temas no activados conservan el
sistema actual intacto).

- **Fase 0 — Esquema y flag.** Modelos `ExerciseItem`, `ResourceExerciseItem`, `LearningGuide`;
  ampliación de `Question` (ítem, tipo, dificultad, respuesta canónica/tolerancia/pista/puntaje/
  minutos, ámbito, guía de origen); sesiones de evaluación; ampliación de respuestas de intentos;
  config por tema (10 min/3 intentos nivel, 45 min/2 intentos final). **Migraciones aditivas**, sin
  tocar legacy. Sin UI todavía.
- **Fase 1 — Extracción y aprobación de ítems.** Subir/importar guía privada → IA propone ítems,
  nivel, dificultad, recursos, cantidad detectada, recomendaciones y errores frecuentes → panel
  admin propio para editar/fusionar/rechazar/aprobar.
- **Fase 2 — Guía ProfeOnline original + validación de originalidad.** IA genera borrador
  estructurado (intro, fórmulas KaTeX, ejemplos resueltos, ejercicios por ítem/dificultad, desafíos,
  solucionario) + **chequeo anti-copia** (sin fragmentos extensos ni marcas/nombres/imágenes ajenas)
  + publicación **manual**. ⚠️ Núcleo legalmente sensible.
- **Fase 3 — Banco visible + experiencia de estudio.** Página de guía propia (logo, KaTeX,
  imprimible); banco agrupado por ítem/dificultad (normales + desafíos); "Ver pista"/"Ver solución";
  estudiar todo / practicar un ítem / práctica mixta equilibrada.
- **Fase 4 — Respuesta directa (parser numérico/algebraico).** Motor de corrección con **AST +
  SymPy**, sin `eval`, con límites de longitud/operadores/variables/exponentes; numéricas (enteros,
  decimal coma/punto, fracciones, tolerancia) y algebraicas (polinómicas/racionales equivalentes).
  ⚠️ Superficie de seguridad → `seguridad:requiere-claude`.
- **Fase 5 — Evaluaciones por nivel + prueba final.** Pools ocultos, cuotas fijas por ítem,
  no-repetición hasta agotar pool, pool reservado distinto para la final, distribución 20/50/30,
  ensamblado a 45 min ±10%, **timers server-side** (consumo de intento, vencimiento, 15 s de
  tolerancia de red). Dominio 60/40 y condición de aprobación (≥80% ponderado **y** final ≥80%).
- **Fase 6 — Exportación PDF.** `html2pdf.js` autoalojado; descarga tras render de KaTeX; portada
  ProfeOnline + solucionario; **sin** almacenar PDFs en el FS efímero de Railway.
- **Fase 7 — Migración legacy + gate de activación + piloto.** Clasificación manual de preguntas
  antiguas por ítem/ámbito (duplicar/archivar; las de modo `ambas` no entran automáticamente); gate
  que verifica ítems aprobados, ejercicios visibles completos, reserva para 3 pruebas, cuotas
  válidas, distribución 20/50/30, duración estimada y cero publicadas sin clasificar. Activar el
  piloto en **un** tema.

## No-objetivos (qué queda FUERA, al menos en v1)
- Copiar literalmente texto, imágenes, logos o nombres institucionales del original ("clonar" =
  reproducir estructura/cobertura pedagógica, **nunca** copia literal).
- Álgebra avanzada en el parser: funciones arbitrarias, sistemas y ecuaciones → fase posterior.
- Almacenar PDFs server-side; la **web es la fuente canónica/accesible**, el PDF es visual.
- Publicación automática de cualquier cosa generada.

## Criterios de aceptación (verificables — se afinan por fase)
- [ ] Barrera verde por fase: `test` · `check` · `makemigrations --check --dry-run`.
- [ ] Flag por tema: temas no activados mantienen el sistema actual (banco legacy intacto).
- [ ] Migraciones aditivas; ninguna pregunta histórica se borra (archivar, nunca `delete`).
- [ ] Originalidad: validación bloquea fragmentos extensos copiados y marcas ajenas (Fase 2).
- [ ] Parser sin `eval`; rechaza manipulación/expresiones inválidas/fuera de límites (Fase 4).
- [ ] Evaluaciones: cuotas + no-repetición + timers server-side + dominio 60/40 (Fase 5).
- [ ] Gate de activación con todas las verificaciones (Fase 7).
- [ ] Si toca CSS → cache-buster `?v=N`.

## Plan de pruebas (las "Pruebas obligatorias" del spec, por fase)
Extracción/aprobación de ítems · originalidad y ausencia de marcas ajenas · generación/publicación
de guía · filtros ítem/dificultad · respuestas numéricas y algebraicas equivalentes · manipulación/
expresiones inválidas/límites del parser · selección por cuotas y no-repetición · timers/expiración/
intentos · dominio 60/40 y aprobación · banco legacy intacto fuera del piloto · PDF con logo/fórmulas/
saltos de página · suite completa + QA móvil.

## Riesgos / rollback / decisiones abiertas
- **Originalidad (legal):** la validación anti-copia es el riesgo central; si es débil, se publica
  material derivado. Rollback: la publicación es manual y el flag desactiva el tema.
- **Parser (seguridad):** entrada del alumno evaluada → AST restringido + SymPy; ver advertencia de
  deprecaciones de SymPy. `seguridad:requiere-claude`.
- **Costo IA:** ítems + guía + 3 bancos de evaluación por tema = uso alto de Gemini → generar a
  cuentagotas (patrón del 🧑).
- **Decisión RESUELTA (2026-06-22):** el flujo "nada se publica automáticamente"
  (revisión→publicación manual) aplica **solo al sistema nuevo**. El banco/sistema actual **sigue
  publicando directo** (no cambia la política vigente).
- **Decisión RESUELTA (2026-06-22):** ítems y guías se administran con **paneles propios in-app**
  (solo-admin, config-driven; sin Django admin).
- **Rollback global:** todo detrás del flag por tema; desactivar el flag restaura el sistema actual.

## Referencias
- [html2pdf.js](https://github.com/ekoopmans/html2pdf) · [WeasyPrint deps](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html)
  (alternativa server-side descartada por FS efímero) · [SymPy active deprecations](https://docs.sympy.org/latest/explanation/active-deprecations.html).

---

## Apéndice — Especificación original del 🧑 (fuente de verdad, verbatim)

### Resumen
Convertir cada guía subida en una fuente privada que la IA analiza para producir:
1. Ítems de aprendizaje revisados por el profesor.
2. Una guía nueva y original con identidad ProfeOnline.
3. Un banco visible de ejercicios organizado por ítem y dificultad.
4. Bancos reservados para evaluaciones por nivel y prueba final.

La guía nueva replicará cobertura, estructura y cantidad aproximada de ejercicios, pero no copiará
textos, imágenes, logos ni nombres institucionales del original.

### Modelos e interfaces
- `ExerciseItem`: tema, nivel 1/2/3, objetivo, recomendación, errores frecuentes, orden, dificultad y
  estado `propuesto/aprobado/archivado`.
- `ResourceExerciseItem`: relaciona ítem y recurso; define cuotas para práctica y evaluación.
- `LearningGuide`: guía ProfeOnline generada, fuentes privadas utilizadas, tema, recursos, contenido
  estructurado, visibilidad `interna/pública` y estado `borrador/publicada`.
- Ampliar `Question` con: ítem; tipo `alternativa/numérica/algebraica`; dificultad
  `básica/intermedia/avanzada/desafío`; respuesta canónica, tolerancia, pista, puntaje y minutos
  estimados; ámbito `banco visible/evaluación de nivel/prueba final`; guía ProfeOnline de origen.
- Ampliar respuestas de intentos para guardar texto ingresado y crear respuestas detalladas para la
  prueba final.
- Añadir sesiones de evaluación con preguntas seleccionadas, inicio, vencimiento y estado.
- Configuración: evaluaciones por nivel 10 min y 3 intentos; prueba final 45 min y 2 intentos; todo
  configurable antes de activar cada tema.

### Flujo editorial
1. Subir o importar una guía y vincularla obligatoriamente a un tema y opcionalmente a recursos.
2. Mantener el original privado; solo se extraen texto, estructura y ejercicios.
3. La IA propone: ítems; nivel y dificultad; recursos relacionados; cantidad de ejercicios detectada;
   recomendaciones y errores frecuentes.
4. El profesor edita, fusiona, rechaza o aprueba los ítems.
5. La IA genera un borrador original de la guía ProfeOnline con: introducción y resumen; fórmulas;
   ejemplos resueltos; ejercicios por ítem y dificultad; desafíos; solucionario.
6. Validar que no existan fragmentos extensos copiados ni referencias visuales/institucionales ajenas.
7. El profesor revisa y publica.
8. El número inicial de ejercicios visibles por ítem replica el detectado en la guía original, pero
   puede editarse.
9. Generar y revisar bancos ocultos suficientes para tres evaluaciones completas sin repetir.
10. Activar el nuevo sistema únicamente cuando toda la cobertura esté completa.

Nada generado se publica automáticamente.

### Experiencia del estudiante
- En tema y recurso aparecerán únicamente las guías ProfeOnline públicas.
- Cada guía tendrá una página propia con logo, KaTeX y diseño imprimible.
- El banco mostrará todos los ejercicios agrupados por: ítem; dificultad; ejercicios normales y
  desafíos.
- Cada ejercicio tendrá "Ver pista" y "Ver solución"; revelar soluciones no afecta el dominio
  académico.
- El alumno podrá: estudiar todo el banco; practicar un ítem concreto; iniciar una práctica mixta
  equilibrada.
- Después de evaluaciones, el sistema recomendará los ítems y dificultades con menor rendimiento.

#### PDF
- La página web será la versión canónica.
- Se incorporará `html2pdf.js` autoalojado para descargar automáticamente una versión PDF después de
  que KaTeX haya renderizado las fórmulas.
- El PDF incluirá portada ProfeOnline y solucionario final.
- No se almacenarán PDFs en el filesystem efímero de Railway.

### Selección, corrección y dominio
- Las prácticas seleccionan aleatoriamente ejercicios del banco visible respetando el ítem solicitado.
- Las evaluaciones usan exclusivamente variantes ocultas y cuotas fijas por ítem.
- No se repite una variante al mismo alumno hasta agotar el pool correspondiente.
- La prueba final usa un pool reservado diferente al de las evaluaciones por nivel.
- Distribución de la prueba final por puntaje: 20% conceptual; 50% mecánico; 30% aplicación.
- El ensamblador respetará 45 minutos estimados con tolerancia de ±10%.

#### Respuesta directa
- Numéricas: enteros, decimales con coma o punto y fracciones, con tolerancia configurable.
- Algebraicas: expresiones polinómicas o racionales equivalentes.
- Se usará un parser restringido basado en AST y SymPy: sin `eval`; longitud, operadores, variables y
  exponentes limitados; sin funciones arbitrarias, ecuaciones ni código.
- Las preguntas conceptuales podrán seguir usando alternativas.

#### Progreso
- Banco visible y prácticas: entrenamiento sin peso académico.
- Evaluaciones por nivel: 60% del dominio.
- Prueba final: 40%.
- Evaluaciones requeridas no rendidas aportan cero.
- Tema dominado solamente si: promedio ponderado ≥80%; prueba final ≥80%.

El servidor controlará el tiempo. Una evaluación iniciada consume intento; al vencer, las respuestas
pendientes se consideran incorrectas, con 15 segundos de tolerancia de red.

### Compatibilidad, piloto y pruebas
- Añadir un flag por tema para activar el banco estructurado.
- Los temas no activados mantienen el sistema actual.
- Antes de activar el piloto, todas las preguntas antiguas deberán clasificarse manualmente por ítem y
  ámbito, duplicarse si corresponde o archivarse.
- Las preguntas antiguas con modo `ambas` no podrán entrar automáticamente en el sistema nuevo.
- El gate de activación verificará: todos los ítems aprobados; ejercicios visibles completos; reserva
  para tres pruebas; cuotas válidas; distribución final 20/50/30; duración estimada; cero preguntas
  publicadas sin clasificar.

Pruebas obligatorias: extracción y aprobación de ítems; originalidad y ausencia de marcas ajenas;
generación y publicación de guía; filtros por ítem/dificultad; respuestas numéricas y algebraicas
equivalentes; manipulación, expresiones inválidas y límites del parser; selección por cuotas y no
repetición; temporizadores, expiración e intentos; dominio 60/40 y condición de aprobación; banco
legacy intacto fuera del piloto; PDF con logo, fórmulas y saltos de página; suite completa y QA móvil.

### Supuestos técnicos
- "Clonar" significa reproducir estructura pedagógica y cobertura, nunca copiar literalmente.
- El material original siempre permanece privado.
- La primera versión algebraica admite operaciones básicas, potencias acotadas y expresiones
  racionales; funciones, sistemas y ecuaciones quedan para una fase posterior.
- La exportación PDF será visual; la versión web continuará siendo la fuente accesible y canónica.
