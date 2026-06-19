# Generador universal de preguntas por tema

- **Estado:** Por iniciar
- **Creado:** 2026-06-19
- **Prioridad:** P1  ·  **Cartera:** educativa
- **Tipo:** producto · pedagogía · QA
- **Dueño sugerido:** 🧩 Codex

## Objetivo (una frase)
Generar y completar bancos de preguntas para cualquier tema usando sus recursos, transcripciones y guías, con auditoría pedagógica automática antes de publicar.

## Fuentes a leer (rutas concretas)
- `apps/content/management/commands/generate_pending_questions.py`
- `apps/content/services/ai_generation_service.py`
- `apps/content/models/resource_quiz_config.py`

## Propuesta
Crear `generate_topic_questions --topic SLUG`: descubre los recursos publicados del tema, reúne
transcripciones y guías, genera candidatos con IA y completa la matriz nivel/modo configurada.
Una segunda etapa valida fundamento, respuesta, distractores, dificultad, diversidad y duplicados
literales o pedagógicos; regenera déficits y publica únicamente lotes completos y válidos.

La interfaz prevista incluye `--dry-run`, `--resource`, `--questions-per-resource`,
`--curate-existing`, `--allow-without-source` y confirmación explícita para producción.
La curación crea respaldo JSON y archiva preguntas repetidas en vez de borrarlas.

## No-objetivos (qué queda FUERA)
- Plantillas deterministas específicas programadas a mano para cada tema.
- Generar sin fuente salvo autorización explícita.
- Borrar historial de respuestas de alumnos.

## Criterios de aceptación (verificables)
- [ ] Selección obligatoria de tema y filtro opcional de recurso.
- [ ] Matriz exacta por nivel y modo, basada en `ResourceQuizConfig`.
- [ ] Cuatro alternativas distintas y exactamente una correcta.
- [ ] Cuotas de familias cognitivas y ninguna familia sobre el 30 % de un nivel.
- [ ] Detección de duplicados literales y pedagógicos.
- [ ] Publicación automática solo si el lote completo supera las validaciones.
- [ ] Dry-run sin llamadas a IA ni escrituras.
- [ ] Respaldo y transacción para toda curación de preguntas existentes.

## Plan de pruebas
Cubrir tema inexistente, recurso puntual, ausencia de fuentes, lote ambiguo, regeneración incompleta,
duplicados, rollback, dry-run y distribución exacta por nivel/modo.

## Riesgos / rollback
La revisión automática puede aceptar preguntas pedagógicamente débiles. Mitigar con fuentes
obligatorias, doble validación, métricas de diversidad e informes por corrida. No retirar bancos
existentes hasta que el reemplazo completo esté validado.

---

## Qué se hizo
_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_
