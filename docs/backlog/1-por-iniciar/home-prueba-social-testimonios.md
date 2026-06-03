# Home: sección de prueba social (testimonios reales)

- **Estado:** Por iniciar
- **Creado:** 2026-06-03
- **Prioridad:** P2 · **Cartera:** conversión
- **Tipo:** producto
- **Dueño sugerido:** 🔨 Antigravity (construcción) · 🧑 Usuario (contenido, bloqueante)

> Surge del cierre del rediseño del Home (2026-06-03). El handoff original pedía una sección de
> **prueba social**; se omitió porque **no había testimonios reales** y mostrar testimonios
> inventados sería engañoso. Se retoma cuando exista contenido real.

## Objetivo (una frase)
Añadir al home una sección de **testimonios reales** (con permiso) para reforzar la confianza,
completando el pilar de prueba social que quedó fuera del primer rediseño.

## Fuentes a leer (rutas concretas)
- `templates/pages/home.html` — insertar la sección entre "Cómo funciona" y "Empieza por aquí".
- `static/css/estilos.css` — reutilizar tokens; las clases `.testimonial-*` fueron eliminadas en
  el cierre (eran CSS muerto), habrá que volver a crearlas o usar `.home-link-card`.

## Bloqueante
- **Contenido del 🧑:** 2–3 testimonios reales con permiso (texto + nombre/curso). Sin esto, no se inicia.

## No-objetivos
- ❌ Testimonios inventados o sin permiso.
- ❌ Modelos/admin: mantener hardcodeado en el template (igual que el resto del home).

## Criterios de aceptación (verificables)
- [ ] Barrera verde: `test` · `check --deploy` · `makemigrations --check --dry-run`.
- [ ] 2–3 testimonios reales renderizados, responsive y accesibles.
- [ ] Si toca CSS → cache-buster subido.

---

## Qué se hizo
_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_
