# Navegación anterior y siguiente entre recursos

- **Estado:** Construido; pendiente de auditoría
- **Creado:** 2026-07-02
- **Prioridad:** P1  ·  **Cartera:** educativa
- **Tipo:** producto
- **Dueño sugerido:** Codex

## Objetivo (una frase)
Permitir avanzar o retroceder entre los recursos ordenados de un mismo tema sin volver al listado.

## Fuentes a leer (rutas concretas)
- `apps/content/models/knowledge.py`
- `apps/learn/views.py`
- `templates/learn/node_detail.html`
- `apps/learn/tests.py`

## Propuesta
Calcular los vecinos entre recursos hermanos por `order`, `code`, mostrar enlaces al final de la ficha y omitir nodos no publicados para alumnos.

## No-objetivos (qué queda FUERA)
- Navegar automáticamente entre temas o bloques distintos.
- Cambiar el orden almacenado de los nodos.

## Criterios de aceptación (verificables)
- [x] Anterior y siguiente respetan `order`, `code`.
- [x] Alumnos nunca reciben enlaces a recursos no publicados; staff sí puede recorrerlos.
- [x] En los extremos solo aparece el enlace disponible.
- [x] Tests focalizados, `check` y ausencia de migraciones, OK.

## Plan de pruebas
Tests de recurso intermedio, extremos, empate de orden, visibilidad staff/alumno y QA responsive en navegador.

## Riesgos / rollback
Riesgo bajo y sin migraciones. Rollback: retirar cálculo de vecinos y bloque de plantilla.

---

## Qué se hizo
- Se calculan los vecinos inmediatos con dos consultas acotadas al mismo tema.
- Los enlaces muestran dirección y nombre del recurso destino al final de la ficha.
- En móvil se apilan en una columna y no producen scroll horizontal.
- Validación: 17 tests focalizados, `check`, `makemigrations --check` y QA navegador, OK.
