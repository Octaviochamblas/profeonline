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

**Decisión (2026-05-31): se migra a TEMA CLARO.** El amarillo de marca se reserva para
CTAs/acentos y se usa azul para títulos/enlaces.

### Cómo se decidió
Se generó un prototipo real del **home** (no una maqueta aparte) redefiniendo los tokens del
`:root` mediante un CSS de preview temporal, y se compararon capturas oscuro vs claro
(guardadas en `Desktop\tema-profeonline\`: `1-oscuro-actual.png`, `2-claro.png`).

### Por qué claro
- Lee más profesional/confiable y académico (clave para apoderados).
- Los **CTAs amarillos resaltan más sobre blanco** que sobre oscuro → mejor conversión.
- Mejor legibilidad para contenido educativo largo.
- Reservar amarillo solo para CTAs + azul como acento da jerarquía mucho más clara.

### Paleta clara acordada (punto de partida para la implementación)
```
--bg: #f8fafc;  --surface: #ffffff;  --surface-soft: #f1f5f9;  --border: #e2e8f0;
--text: #0f172a;  --muted: #475569;  --primary: #FFD100 (CTAs);  acento azul: #1d4ed8;
--shadow: 0 10px 30px rgba(2,6,23,0.08);
```

### Lo que la implementación deberá resolver (se canaliza por `sistema-diseno-pulido-css.md`)
1. Redefinir tokens del `:root` a la paleta clara.
2. **Retargetear el amarillo-como-texto** (links, `.home-link-card__title`,
   `.topic-resource-card__title`, `.area-card h2`, `.resource-navigation__title`,
   `.legal-article h3`, etc.) a azul `#1d4ed8`.
3. Encabezados hardcodeados en blanco (`h1,h2,h3`, `.page-hero__kicker`,
   `.bottom-contact-cta__title`) → color oscuro.
4. Chips/badges oscuros (`.badge--neutral`, meta-badges) → claros.
5. Header y burbujas de icono a versión clara.
6. **Variante del logo** para fondo claro (el actual amarillo pierde contraste en blanco).
7. De paso resuelve **A11Y-1** (contraste botón WhatsApp) y se revisa el resto del contraste.

### Estado
Decisión **cerrada**. La implementación del tema claro es la fase siguiente (tarjeta
`sistema-diseno-pulido-css.md`), idealmente antes del rediseño del home.
