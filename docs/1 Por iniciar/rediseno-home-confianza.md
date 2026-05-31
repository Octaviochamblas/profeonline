# Rediseño del home: de "directorio" a "página que genera confianza"

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** Estética / Conversión
- **Prioridad:** 🔴 Alta

## Problema / Objetivo

El home actual (`templates/pages/home.html`) es, en esencia, **un directorio de navegación**:
hero con logo + texto + botones, y luego rejillas de tarjetas iguales (Recursos, Asignaturas,
Temas, Niveles, Recursos publicados). Funciona para *navegar*, pero **no vende ni genera
confianza**. Para un negocio de clases particulares, faltan los tres pilares de conversión:
**la persona detrás, la prueba social y una jerarquía que guíe**.

Objetivo: rediseñar el home para que un visitante nuevo entienda en segundos qué es, en quién
confiar y qué hacer, sin perder la utilidad de navegación que ya tiene.

## Diagnóstico del home actual

Lo que hay (`home.html`):
- Hero centrado: kicker, logo, título, párrafo, 3 botones, badges de asignaturas.
- `resume_card` (continuar donde quedaste) — buena pieza ya existente.
- 4 secciones de tarjetas (`home-link-card`) prácticamente idénticas en peso visual.

Lo que falta:
1. **La persona que enseña.** Cero foto, nombre, credenciales o trayectoria. En clases
   particulares, *la confianza es la cara del profe*.
2. **Prueba social.** Cero testimonios, cero "X estudiantes", cero resultados.
3. **Jerarquía visual.** Todas las tarjetas pesan igual: nada dice "empieza por aquí".
4. **Gancho en el hero.** Logo + párrafo genérico; no engancha en los primeros 3 segundos.
5. **Cómo funciona.** No se explica el proceso (regístrate → estudia con un plan → pide clase).

## Ruta de trabajo

### Fase 1 — Definir contenido real (bloqueante)
- Recopilar: foto del profe, bio corta, credenciales/experiencia, materias fuertes.
- Reunir 2–3 testimonios reales (con permiso) o resultados concretos.
- Definir el mensaje del hero (propuesta de valor en 1 frase).
- **Sin este contenido real, el rediseño se queda en placeholders.**

### Fase 2 — Estructura propuesta del nuevo home
1. **Hero** con propuesta de valor clara + CTA primario único ("Comienza gratis") y
   secundario ("Hablar por WhatsApp"). Apoyo visual (imagen/ilustración o métrica).
2. **"Quién te enseña"** — foto + bio + credenciales del profe.
3. **"Cómo funciona"** — 3 pasos simples.
4. **Prueba social** — testimonios / resultados.
5. **Empieza por aquí** — accesos de navegación (lo actual, pero con menos peso).
6. **Asignaturas / niveles / recursos destacados** (lo actual, condensado).
7. CTA final de WhatsApp (ya existe en `base.html`).

### Fase 3 — Implementación
- Construir las secciones nuevas con los patrones/tokens del CSS actual (o el resultado de
  `decision-tema-claro-oscuro.md`).
- Establecer jerarquía: el CTA primario y la sección del profe deben destacar; las rejillas
  de navegación, atenuarse.
- Mantener accesibilidad (encabezados, alt de la foto, contraste).

### Fase 4 — Medición
- Con la analítica instalada (`mejora-analytics-eventos.md`), comparar registros y clics a
  WhatsApp antes/después.

## Criterios de aceptación

- El home muestra quién enseña, prueba social y un proceso claro.
- Hay un CTA primario inequívoco; la jerarquía guía la mirada.
- Las secciones de navegación se conservan pero con peso visual secundario.
- Responsive y accesible (teclado, contraste, encabezados).

## Notas / Consideraciones

- **Depende de `decision-tema-claro-oscuro.md`**: definir el tema antes de maquetar.
- El cuello de botella real es el **contenido** (foto, bio, testimonios), no el código.
- No romper lo que ya funciona: `resume_card`, badges de asignaturas, accesos rápidos.

---

## Qué se hizo
_(Completar al finalizar, antes de mover a "3 Finalizados".)_
