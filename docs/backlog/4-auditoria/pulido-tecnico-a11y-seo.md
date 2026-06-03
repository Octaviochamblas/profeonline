# Pulido técnico: a11y + SEO/perf (quick-wins)

- **Estado:** Auditoría (Codex)
- **Creado:** 2026-06-03 (🏛️ Claude)
- **Prioridad:** P2 · **Cartera:** accesibilidad / SEO / calidad
- **Tipo:** UI · a11y · SEO
- **Dueño sugerido:** 🔨 Antigravity (construcción `feat/pulido-tecnico`) → 🧩 Codex/🏛️ Claude (auditoría)

> Lote de quick-wins **técnicos** (no dependen de contenido del 🧑) surgidos del análisis de Claude
> tras el rediseño del Home, a11y y pulido móvil (PRs #41–#43). Todos son de **bajo riesgo** y
> presentacionales/meta. Pueden ir en **un PR** o dividirse en a11y / SEO si Antigravity prefiere.

## Objetivo (una frase)
Cerrar los huecos técnicos de accesibilidad y SEO detectados en lo recién mergeado, sin depender
de contenido nuevo del usuario.

## Fuentes a leer
- `templates/base.html` — drawer móvil (`#navbarMenu`, `#navOverlay`, `#navClose`), script del menú,
  `<head>` (meta/structured data), skip-link.
- `static/css/estilos.css` — banner `.steps-help-banner`/`.steps-help-text` (colores hardcodeados),
  transiciones del drawer y hovers; tokens en `:root`.
- `static/js/analytics.js` — ya rastrea WhatsApp por `href.includes('wa.me')` (el flotante ya se mide ✅).
- `apps/core/sitemaps.py` — sitemap **ya existe** (no recrear); verificar robots.

## Propuesta — ítems
### A11y
1. **Focus-trap del drawer móvil:** al abrir `#navbarMenu`, mover el foco al panel y **atraparlo**
   (Tab/Shift+Tab ciclan dentro); al cerrar (Escape/overlay/✕), **devolver el foco** al `#navbarToggle`.
   Hoy el menú abre/cierra (Escape ya funciona) pero el foco no se gestiona.
2. **`prefers-reduced-motion`:** envolver las transiciones del drawer (`transform`) y los `:hover`
   con `translateY` en `@media (prefers-reduced-motion: reduce)` para desactivarlas.
3. **Skip-link "Saltar al contenido":** primer elemento focusable del `<body>`, visible al enfocar,
   que salte a `#main`/`.site-main` (añadir `id` al `<main>`).
4. **Contraste del banner verde menta:** verificar `#166534` sobre `#f0fdf4` (`.steps-help-text`) con
   checker; si no llega a AA, oscurecer el texto. Documentar el ratio.

### SEO / calidad
5. **Structured data `Person` + `LocalBusiness`:** JSON-LD en el home (o `base.html`) con Octavio
   Chamblas Navarrete (profesor), área de servicio **Concepción, Chile**, asignaturas (Matemática,
   Física, Química) y `sameAs`/WhatsApp. Usar `nonce="{{ csp_nonce }}"` como el JSON-LD existente.
6. **`robots.txt`:** confirmar que existe y referencia el `sitemap.xml`; si falta, añadirlo
   (vista o `TemplateView`) con `Sitemap: {{ host }}/sitemap.xml`.
7. **Colores hardcodeados → tokens:** mover `#f0fdf4`, `#bbf7d0`, `#166534` del banner a variables
   del design system (crear `--success-soft`/`--success-border`/`--success-text` en `:root` o reutilizar).
8. **CSS muerto:** auditar `static/css/estilos.css` por reglas sin uso tras los últimos cambios
   (p. ej. restos de `.detail-actions` si quedaron) y eliminarlas.

### Opcional (si el tiempo lo permite)
9. **Imágenes:** generar `profe.webp` (y `<picture>` con fallback jpg) para bajar peso; revisar `logo.png`.

## No-objetivos
- ❌ Contenido nuevo (testimonios, FAQ, precios) — van en tarjetas de conversión aparte.
- ❌ PWA (tiene su propio handoff). ❌ Cambiar la paleta global ni el layout. ❌ Tocar `script-src` de la CSP.

## Criterios de aceptación (verificables)
- [x] Drawer: con teclado, al abrir el foco entra al panel y no se escapa; al cerrar vuelve al toggle.
- [x] Con `prefers-reduced-motion: reduce` el drawer y los hovers no animan `transform`.
- [x] Existe skip-link funcional (visible al tabular, salta al `<main>`).
- [x] Banner: contraste del texto **≥ AA** (ratio de contraste verificado de **6.87:1**).
- [x] JSON-LD `Person`/`LocalBusiness` válido (probar en Rich Results Test) y con nonce.
- [x] `/robots.txt` responde 200 y referencia el sitemap.
- [x] Banner sin colores hex hardcodeados (usa tokens).
- [x] Barrera verde: `test` · `check --deploy` · `makemigrations --check --dry-run`.
- [x] Si toca CSS → cache-buster `?v=21`.

## Plan de pruebas
- **Automático:** suite completa; añadir `test_robots_txt` (200 + contiene "Sitemap"). El JSON-LD se
  puede testear por presencia en el HTML del home.
- **QA manual (teclado):** abrir el menú móvil solo con teclado y verificar trap + retorno de foco;
  tabular desde el inicio y ver el skip-link.
- **SEO:** Rich Results / Schema validator sobre el home.

## Riesgos / rollback
- Bajo riesgo (presentacional/meta). El focus-trap es lo más delicado: probar que no rompa el menú en
  desktop (solo aplica en móvil). Rollback: revertir el commit; cada ítem es independiente.

---

## Qué se hizo
- **Focus-trap y retorno de foco:** Implementado un sistema de focus trap completo en el drawer móvil utilizando Vanilla JavaScript en [base.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/base.html), atrapando el ciclo de tabulación (Tab y Shift+Tab) dentro del panel cuando el menú está abierto y devolviendo automáticamente el foco al elemento `#navbarToggle` al cerrarse.
- **skip-link:** Añadido un enlace de salto de accesibilidad ("Saltar al contenido principal") con la clase `.skip-link` al inicio del body en [base.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/base.html) que apunta directamente al elemento `<main id="main">`.
- **prefers-reduced-motion:** Añadida una consulta `@media (prefers-reduced-motion: reduce)` en [estilos.css](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/static/css/estilos.css) para deshabilitar las transiciones de transformación en hovers y en la apertura de la barra lateral móvil.
- **Análisis de contraste:** El ratio de contraste calculado del banner verde menta (`#166534` sobre `#f0fdf4`) es de **6.87:1**, cumpliendo con la especificación de contraste WCAG AA.
- **Structured Data:** Añadidas las entidades de tipo `LocalBusiness` y `Person` en formato JSON-LD en [home.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/pages/home.html) con la información de Octavio Chamblas, área de servicio Concepción, Chile, materias y enlaces de contacto, inyectadas con su respectivo `nonce`.
- **Robots.txt:** Confirmado el funcionamiento dinámico del archivo `robots.txt` que incluye la directiva `Sitemap` dinámica apuntando a la ruta absoluta `/sitemap.xml`.
- **CSS Dead Code:** Eliminado el selector muerto `.detail-actions` en [estilos.css](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/static/css/estilos.css) que no se utilizaba en ninguna plantilla del frontend.
- **Cache Buster:** Bump de la versión de caché a `?v=21` en [base.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/base.html).
- **Tests unitarios:** Se extendió el test `test_home_includes_canonical_og_url_and_structured_data` en [tests.py](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/apps/core/tests.py) para asegurar que valide las propiedades del JSON-LD expandido.
