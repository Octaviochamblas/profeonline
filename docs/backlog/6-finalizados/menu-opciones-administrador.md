# Agrupar herramientas en “Opciones de Administrador”

- **Estado:** Construcción terminada — pendiente auditoría/cierre
- **Creado:** 2026-06-18
- **Prioridad:** P2 · **Cartera:** producto
- **Tipo:** producto · QA
- **Dueño:** 🧩 Codex construye → 🏛️ Claude audita/cierra

## Objetivo

Reducir el ruido del navbar agrupando las siete herramientas administrativas bajo un único
desplegable “Opciones de Administrador”, visible solo para staff.

## Fuentes a leer

- `templates/base.html`
- `static/css/estilos.css`
- `apps/core/tests.py`

## Propuesta

Usar `<details>/<summary>` nativo para mantener navegación por teclado y evitar JavaScript/CSP
adicional. En escritorio funciona como dropdown; en móvil, como acordeón dentro del drawer.

## No-objetivos

- No agrupar “Áreas”, porque no forma parte de la lista solicitada.
- No cambiar rutas, permisos ni contenido de las herramientas.

## Criterios de aceptación

- [x] Las siete herramientas aparecen dentro de un único agrupador.
- [x] El agrupador solo aparece para staff.
- [x] Funciona con teclado y sin JavaScript nuevo.
- [x] Desktop y móvil sin overflow.
- [x] Cache-buster CSS actualizado.
- [x] Tests focalizados y `apps.core` verdes.

## Qué se hizo

- Navbar reemplazado por un `<details class="admin-nav">`.
- Dropdown de escritorio y acordeón móvil responsivos.
- Cache-buster de `estilos.css` subido a `v=29`.
- Dos tests de regresión para staff/no-staff.
- QA Browser en escritorio y móvil, sin errores de consola.
- `apps.core`: 46 tests OK; `check` y `makemigrations --check` verdes.
