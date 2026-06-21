# Rediseño compacto de tema y progreso académico

- **Estado:** Finalizado
- **Creado:** 2026-06-21
- **Prioridad:** P1 · **Cartera:** educativa / retención
- **Tipo:** producto · pedagogía · QA
- **Dueño sugerido:** 🧩 Codex

## Objetivo (una frase)

Hacer que la página de tema sea clara y compacta en móvil, con progreso académico coherente y recursos sin información repetida.

## Fuentes a leer (rutas concretas)

- `apps/content/views/topic_detail.py`
- `apps/content/services/progress_service.py`
- `apps/content/selectors/evaluation_selectors.py`
- `templates/pages/topic_detail.html`
- `static/css/estilos.css`
- `apps/content/management/commands/seed_content.py`
- `apps/content/management/commands/seed_resources.json`

## Propuesta

- Condensar la cabecera del tema y trasladar allí asignatura y nivel.
- Calcular el avance contra todos los recursos publicados.
- Resumir recursos iniciados, prácticas preparadas y evaluaciones aprobadas por nivel disponible.
- Simplificar las tarjetas y limpiar títulos editoriales conservando sus slugs.
- Mantener la fuente del seed y los datos existentes sincronizados mediante un comando idempotente con `--dry-run`.

## No-objetivos (qué queda FUERA)

- Eliminar la mecánica de estrellas o XP del backend.
- Cambiar la ponderación práctica 30% / evaluación 70%.
- Cambiar URLs públicas existentes.
- Rediseñar las páginas de asignatura, nivel o recurso.

## Criterios de aceptación (verificables)

- [x] Barrera verde: `test` · `check` · `check --deploy` · `makemigrations --check --dry-run`
- [x] Un recurso al 30% dentro de un tema de 19 recursos muestra 2% global.
- [x] Los denominadores usan solo modos y niveles con preguntas publicadas.
- [x] La página no muestra breadcrumbs, “Ruta de aprendizaje”, descripciones repetidas ni estrellas.
- [x] Los títulos se limpian sin modificar slugs y el seed sigue siendo idempotente.
- [x] QA visual a 320, 360 y 390 px.
- [x] Cache-buster de CSS incrementado.

## Plan de pruebas

Tests de progreso y vista, comando editorial en `--dry-run` y aplicación, seed repetido, checks Django, suite completa y smoke visual móvil.

## Riesgos / rollback

La limpieza masiva podría recortar títulos legítimos. Se limita a reglas v1 versionadas, permite previsualización y preserva slugs. La migración de datos es deliberadamente no reversible; ante rollback se revierte el código y se restauran títulos desde el respaldo de base de datos o las fuentes editoriales.

---

## Qué se hizo

- Se reemplazó la cabecera extensa por título, enlace pequeño a temas, asignatura y nivel común.
- El avance global ahora divide el progreso ponderado por todos los recursos publicados; los no iniciados aportan cero.
- Se agregaron indicadores por disponibilidad real: recursos iniciados, prácticas preparadas y evaluaciones aprobadas.
- Las tarjetas conservan su secuencia y muestran solo título y estado académico, sin descripción, asignatura, nivel ni estrellas.
- Se agregó limpieza editorial v1, comando con dry-run, migración de datos y seed compatible con slugs históricos.
- La limpieza local detectó y aplicó 133 cambios; una segunda ejecución detectó cero.
- QA responsive: 320/360/390 px sin overflow; tarjetas de 83 px y títulos limitados a tres líneas.
- Reproductor validado a pantalla completa (320×780, `position: fixed`).
- Verificación: 398 tests OK, `check` OK, `check --deploy` solo con los 7 warnings esperados de settings locales, sin migraciones pendientes.
- Integrado a `main` mediante squash-merge del PR #77 (`dea2ec8`, 2026-06-21).
