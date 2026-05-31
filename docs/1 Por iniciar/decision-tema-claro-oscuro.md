# Decisión estratégica: tema claro vs oscuro

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** Estética / Negocio
- **Prioridad:** 🔴 Alta (es la palanca estética nº1 y condiciona todo el rediseño)

## Problema / Objetivo

El sitio usa un **tema oscuro** (`--bg #0f0f0f`, `--surface #1a1a1a`) con acento amarillo
(`--primary #FFD100`) y fuente Outfit. Es coherente y está bien ejecutado, pero
estéticamente lee "tech / gamer / SaaS", no "académico / confiable". En clases particulares,
**quien paga suele ser un apoderado**, y la confianza visual pesa. El tema oscuro puede estar
restando conversión sin que lo sepamos.

Objetivo: **decidir con criterio** (no a ciegas) si conviene migrar a un tema claro/híbrido o
mantener el oscuro pulido. Esta es una decisión de negocio, no técnica.

## Argumentos

### A favor de explorar tema claro
- Mayor sensación de confianza/seriedad académica para apoderados.
- Mejor legibilidad de textos largos (guías, contenido educativo).
- Más fácil cumplir contraste AA (ver `auditoria-accesibilidad-axe.md`).
- La mayoría de plataformas educativas de referencia (Khan Academy, Classroom) son claras.

### A favor de mantener oscuro
- Ya está implementado y pulido (≈2.200 líneas de CSS consistentes).
- Diferenciación visual respecto a la competencia.
- Menos trabajo: solo pulir, no migrar.

### Opción híbrida
- Contenido/lectura en claro; hero, footer y CTAs en oscuro con el amarillo de marca.
- Da lo mejor de ambos pero requiere diseño cuidadoso de transiciones.

## Ruta de trabajo

### Fase 1 — Investigación / referencia
- Reunir 4–5 referencias de plataformas educativas que transmitan la sensación deseada.
- Definir el adjetivo objetivo de marca (¿"cercano", "premium", "serio", "juvenil"?).

### Fase 2 — Prototipo comparativo
- Como el CSS ya usa tokens en `:root`, **crear una paleta clara alternativa** redefiniendo
  esas variables (sin reescribir componentes) para una maqueta rápida del home.
- Generar una versión clara y una híbrida del home para comparar lado a lado.

### Fase 3 — Decisión
- Comparar las versiones (idealmente con feedback de 2–3 personas del público objetivo).
- Documentar la decisión y sus motivos aquí mismo.

### Fase 4 — Habilitar el cambio (si aplica)
- Si se migra: el trabajo se canaliza por `sistema-diseno-pulido-css.md`.
- Considerar dejar ambos temas vía `prefers-color-scheme` / toggle (más esfuerzo).

## Criterios de aceptación

- Existe una maqueta comparable de al menos 2 opciones (oscuro pulido vs claro/híbrido).
- La decisión está tomada y justificada por escrito.
- Si hay cambio, queda una ruta clara hacia el sistema de diseño.

## Notas / Consideraciones

- **No** empezar el rediseño del home ni el pulido de CSS antes de cerrar esta decisión:
  el tema condiciona ambos.
- Aprovechar que el CSS ya está tokenizado en `:root` hace el prototipo barato.

---

## Qué se hizo
_(Completar al finalizar, antes de mover a "3 Finalizados".)_
