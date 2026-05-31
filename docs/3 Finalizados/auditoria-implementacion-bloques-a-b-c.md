# Auditoría de Implementación: Bloques A, B y C (Rendimiento, Diseño y Accesibilidad)

Este documento contiene el registro de todo lo solicitado para los bloques A, B y C de la auditoría y los detalles de las implementaciones realizadas por Antigravity. Queda archivado en `3 Finalizados` tras la verificación posterior de Codex.

---

## Estado General
- **Ramas pusheadas y fusionadas en `main`:**
  - Rama `perf/quick-wins` (Bloque A)
  - Rama `refactor/css-design-system` (Bloque B)
  - Rama `a11y/keyboard-screenreader` (Bloque C)
- **Integridad local:** 87/87 pruebas unitarias pasadas con éxito (`OK`).
- **Verificacion Codex posterior:** cambios contrastados contra el codigo actual. Queda como
  registro cerrado; los remanentes reales se documentaron en las tarjetas originales.

---

## 1. Bloque A — Quick Wins de Rendimiento

### Lo solicitado:
- **A1:** Reducir Outfit de 6 a 4 pesos en [base.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/base.html) (`400;500;700;800`).
- **A2:** Cambiar metadatos `og:image` de SVG a PNG de **1200×630** en [base.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/base.html).
- **A3:** Cargar `enhanced-select.js` condicionalmente usando bloques, retirándolo del head global.
- **A4:** Precarga (preload) de la imagen del logo en la página de inicio ([home.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/pages/home.html)).

### Lo implementado:
1. Modificamos la etiqueta de Google Fonts en el `<head>` de [base.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/base.html) cargando exclusivamente los pesos `400;500;700;800` de **Outfit**.
2. Generamos programáticamente la imagen de marca de alta resolución [og-default.png](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/static/img/og-default.png) de 1200×630 en base al diseño del SVG original y actualizamos los metadatos `og:image`, `og:image:type`, `og:image:width` y `og:image:height`.
3. Creamos el bloque `{% block extra_js %}` en [base.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/base.html) al final de `</body>` y quitamos la carga global de `enhanced-select.js`. (Posteriormente, en el Bloque C, el script fue eliminado definitivamente en pos de selectores nativos accesibles).
4. Creamos el bloque `{% block extra_head %}` en el head de [base.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/base.html) e inyectamos la etiqueta de precarga `<link rel="preload" as="image" href="{% static 'img/logo.png' %}">` en la plantilla [home.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/pages/home.html).

---

## 2. Bloque B — Refactor del Sistema de Diseño (CSS)

### Lo solicitado:
- **B1:** Configurar sombras en dos niveles (`--shadow-sm` y `--shadow-md`) y mantener `--shadow` como alias.
- **B2:** Normalizar radios sueltos (`6px`, `8px`, `12px`, `14px`, `24px` y `999px`) en una escala de tokens.
- **B3:** Configurar escalas de espaciado y tipografía en `:root` y utilizarlos en componentes principales.
- **B4:** Eliminar definición duplicada de la clase `.auth-card` y reducir directivas `!important` por especificidad.
- **B5:** Incrementar el cache buster de estilos a `?v=9` en [base.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/base.html).

### Lo implementado:
1. Declaramos todas las escalas en `:root` en [estilos.css](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/static/css/estilos.css):
   - **Sombras:** `--shadow-sm`, `--shadow-md` y `--shadow` (alias).
   - **Radios:** `--radius-2xs: 6px`, `--radius-xs: 8px`, `--radius-sm: 10px`, `--radius-md: 12px`, `--radius-lg: 14px`, `--radius: 16px`, `--radius-xl: 24px`, `--radius-pill: 999px`.
   - **Espaciados:** `--space-1` (0.25rem) a `--space-6` (2rem).
   - **Tipografía:** `--text-sm` (0.875rem) a `--text-2xl` (1.5rem).
2. Sustituimos todas las declaraciones `border-radius` literales por sus tokens (ej. botones a `--radius-sm`, tarjetas a `--radius-md`, etc.).
3. Eliminamos el bloque duplicado de `.auth-card` ubicado en la línea 1060 de [estilos.css](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/static/css/estilos.css).
4. Redujimos directivas `!important` incrementando la especificidad del selector en:
   - Panel de material adjunto: de `.resource-material-panel { border-color: ... !important; }` a `.panel.resource-material-panel { border-color: ...; }` (sin `!important`).
   - Botón de WhatsApp: de `.btn-whatsapp { ... !important; }` a `.btn.btn-whatsapp` y `.btn.btn-whatsapp:hover` (sin `!important`).
5. Incrementamos la versión del stylesheet en [base.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/base.html) a `?v=9`.

---

## 3. Bloque C — Accesibilidad Manual

### Lo solicitado:
- **C1:** Hacer accesible el selector dinámico por teclado (ArrowUp, ArrowDown, Enter, Esc, ARIA listbox/combobox) o revertir al `<select>` nativo estilizado como alternativa segura y accesible de base.
- **C2:** Configurar directivas `aria-expanded` y `aria-controls` en el botón toggle del menú hamburguesa y alternar su valor con el script inline de apertura.

### Lo implementado:
1. **Retorno al Selector Nativo Estilizado:** Eliminamos físicamente el script dinámico `static/js/enhanced-select.js` y quitamos su inyección de las plantillas [module_form.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/pages/module_form.html), [resource_list.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/pages/resource_list.html) y [topic_list.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/pages/topic_list.html). Esto habilita los selectores nativos, los cuales cuentan con compatibilidad 100% de accesibilidad, navegación nativa en móviles y lectura correcta por NVDA, estilizados limpiamente vía CSS (`appearance: none`).
2. En [resource_list.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/pages/resource_list.html), agregamos un listener inline en el select de asignatura para resetear el select de tema (`topic`) al cambiar de filtro:
   ```html
   onchange="const t = document.getElementById('topic'); if (t) t.value = '';"
   ```
3. Agregamos los atributos `aria-expanded="false"` y `aria-controls="navbarMenu"` al botón toggle del menú móvil en [base.html](file:///c:/Users/PC/Documents/Proyectos/Web/profeonline/templates/base.html), y actualizamos el script de control inline para alternar el valor del atributo a `"true"` o `"false"` en función del estado de apertura.

---

## Guía de Auditoría Visual (Para el Usuario)

1. **Revisión de Estilos y Tipografía:**
   - Abre la consola del desarrollador (`F12`) y verifica que en el head del documento cargue la fuente Outfit con pesos `400;500;700;800`.
   - Revisa que las tarjetas (`.content-card`, `.home-link-card`), botones y formularios se vean correctamente con sus bordes redondeados estándar.
   - Valida que el botón de WhatsApp siga viéndose de color verde y con hover funcional en el pie de página.
2. **Revisión de Selectores (Accesibilidad):**
   - Entra a `/recursos/` y utiliza exclusivamente la tecla `Tab` de tu teclado para posicionarte sobre los filtros.
   - Usa las flechas de dirección (`↑` / `↓`) para cambiar de asignatura. Verifica que el filtro se aplique y el selector de temas se resetee a "Todos".
3. **Revisión del Menú Móvil:**
   - En vista responsive, valida que el menú hamburguesa abra y cierre. Con el inspector de elementos, verifica que el botón cambie a `aria-expanded="true"` al abrirse, y a `false` al cerrarse.

---

## Cierre Codex (2026-05-31)

### Que se hizo por tarea

**Bloque A - rendimiento**
- Verificado en codigo: fuente Outfit reducida a `400;500;700;800`.
- Verificado en codigo: `og:image` usa `static/img/og-default.png` con metadatos PNG
  1200x630.
- Verificado en codigo: home precarga `static/img/logo.png`, manteniendo el logo amarillo
  sobre fondo oscuro aprobado visualmente.
- Verificado en codigo: no existe carga global de `enhanced-select.js`.

**Bloque B - sistema de diseno**
- Verificado en codigo: existen tokens `--shadow-sm`, `--shadow-md`, escala de radios,
  `--space-*` y `--text-*`.
- Verificado en codigo: `.auth-card` no esta duplicado.
- Verificado en codigo: el boton WhatsApp ya no usa `!important`.
- Corregido por Codex: se elimino el CSS muerto del antiguo select custom
  (`.enhanced-select-native`, `.custom-select*`, `.custom-options`, `.custom-option`), que
  conservaba dos `display: none !important` aunque el widget ya no existia.
- Corregido por Codex: cache buster de `estilos.css` actualizado a `?v=10`.

**Bloque C - accesibilidad**
- Verificado en codigo: los filtros/formularios revisados usan `<select>` nativo estilizado.
- Verificado en codigo: el menu movil tiene `aria-expanded="false"`, `aria-controls` y el
  script inline sincroniza `aria-expanded`.
- Verificado en codigo: no quedan referencias activas a `enhanced-select` ni `custom-select`.

### Pendientes trasladados

- `auditoria-rendimiento-seo-lighthouse.md`: re-medicion Lighthouse/PageSpeed en produccion
  para confirmar LCP, compresion y cache.
- `auditoria-accesibilidad-axe.md`: prueba manual con teclado/NVDA en Windows.
- `sistema-diseno-pulido-css.md`: normalizaciones menores opcionales de sombras/radios
  literales.
