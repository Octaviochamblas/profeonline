# Rediseñar explorador visual de Aprende

- **Estado:** Finalizado
- **Creado:** 2026-07-02
- **Prioridad:** P1  ·  **Cartera:** educativa
- **Tipo:** producto
- **Dueño sugerido:** 🧩 Codex

## Objetivo (una frase)
Convertir las pantallas de selección de `/aprender/` en un catálogo atractivo, compacto y fácil de recorrer.

## Fuentes a leer (rutas concretas)
- `templates/learn/home.html`
- `templates/learn/node_list.html`
- `apps/learn/tests.py`

## Propuesta
Tarjetas clickeables en grid responsive, breadcrumb horizontal desplazable y estética azul/teal con animación respetuosa de movimiento reducido.

## No-objetivos (qué queda FUERA)
- Modificar la ficha pedagógica de cada recurso.
- Cambiar modelos, orden o visibilidad de nodos.

## Criterios de aceptación (verificables)
- [x] Grid de dos columnas en escritorio y una en móvil.
- [x] Toda tarjeta es clickeable, con foco visible y hover elegante.
- [x] Breadcrumb horizontal compacto, con nivel actual y scroll móvil.
- [x] `prefers-reduced-motion` desactiva animaciones.
- [x] Tests focalizados, `check` y migraciones en verde.
- [x] CSS dedicado con cache-buster `?v=2`.

## Plan de pruebas
Tests de plantillas y visibilidad; QA navegador en escritorio/móvil, teclado, títulos largos, vacío y consola.

## Riesgos / rollback
Riesgo visual bajo, sin migraciones. Rollback: retirar el CSS dedicado y restaurar el markup de listas.

---

## Qué se hizo
- `home` y todos los listados jerárquicos usan un catálogo de tarjetas completas clickeables.
- Hero azul/teal con jerarquía tipográfica, códigos compactos, flecha y estados vacíos diseñados.
- Breadcrumb en chips con separadores, nivel actual y desplazamiento horizontal sin barra visible.
- Responsive 2→1 columnas, foco visible y respeto de `prefers-reduced-motion`.
- Validación: 11 tests focalizados, barreras Django y QA navegador escritorio/móvil, OK.
