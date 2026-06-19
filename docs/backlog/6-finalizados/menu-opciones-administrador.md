# Agrupar herramientas en “Opciones de Administrador”

- **Estado:** Cerrada
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

## Ajustes consolidados en la rama

- Plantilla de allauth renombrada a `account/verification_sent.html`, con regresión que confirma
  que extiende `base.html`.
- Pacing configurable y backoff ampliado para generación con IA, con pruebas de `Retry-After`.
- Nuevo comando `import_questions_json`, endurecido en auditoría con validación, transacción y
  tres pruebas de importación/rollback.
- Generador local de preguntas de Números enteros, manual y sin consumo de API.

## Auditoría final

- **P0 corregido:** se retiró la migración de datos `0029`, que borraba todas las preguntas
  existentes de diez recursos durante el arranque de producción, generaba contenido aleatorio y
  no tenía reversa.
- El generador manual ahora conserva lo existente, usa una semilla estable, omite enunciados ya
  presentes y agrega cada recurso dentro de una transacción.
- Se retiró el script redundante `populate_numeros_enteros.py`.
- 90 tests focalizados verdes; compilación Python y `git diff --check` verdes.
- Suite completa: **331 tests OK**; `check`, `makemigrations --check` y `check --deploy`
  sin errores.
- `pip-audit`: sin vulnerabilidades conocidas.
- Validador pedagógico: 350 preguntas candidatas, exactamente una respuesta correcta por
  pregunta y alternativas sin duplicados.
