# Handoff para Antigravity — Pendientes de auditoría y sistema de diseño

- **Creado:** 2026-05-31
- **Para:** Antigravity (ejecuta) → Claude (verifica)
- **Repo:** ProfeOnline (Django). Settings dev por defecto: `config.settings.local`.

## Cómo trabajar (LEER PRIMERO)

1. **Una rama por bloque** (A, B, C). No mezclar bloques en un mismo PR.
2. **Tras cada cambio de CSS**, subir el cache-buster: en `templates/base.html` el `<link>`
   de `estilos.css` usa `?v=N` (hoy `?v=8`). Incrementar a `?v=9`, `?v=10`, etc.
3. **Verificación obligatoria antes de cada PR** (es la barrera de CI):
   ```
   .venv\Scripts\python.exe manage.py test
   .venv\Scripts\python.exe manage.py check
   .venv\Scripts\python.exe manage.py makemigrations --check --dry-run
   ```
   Los 3 deben pasar (la suite son ~87 tests). CI corre lo mismo + `check --deploy` + `pip-audit`.
4. **No romper nada visual.** Tras tocar CSS, levantar `runserver` y revisar a ojo: home,
   `/recursos/`, detalle de recurso, login, registro.
5. **No tocar** `requirements.txt` salvo que un bloque lo pida explícitamente.
6. Flujo git del repo: rama → push → PR a `main` → CI verde → squash-merge. Railway despliega
   solo tras CI verde (Wait for CI activado).

---

## BLOQUE A — Quick wins de rendimiento

Rama sugerida: `perf/quick-wins`. Cierra casi todo `auditoria-rendimiento-seo-lighthouse.md`
y parte de la Fase 4 de `sistema-diseno-pulido-css.md`. Bajo riesgo.

### A1 — Reducir Outfit de 6 a 3 pesos ⭐ (el cambio de mayor impacto)
- **Dónde:** `templates/base.html` línea 24.
- **Hoy:**
  ```html
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  ```
- **Ya verificado (2026-05-31)** qué pesos usa `estilos.css`:
  - `font-weight: 500` en líneas **451, 1175, 1935**.
  - `font-weight: 800` en líneas **1647, 1735, 1976** (títulos de tarjetas — peso visible/importante).
  - No usa `300`.
- **DECISIÓN (elegir una):**
  - **Opción 1 (recomendada, 4 pesos):** cargar `400;500;700;800`. Conserva el `500` (medio) y
    el `800` (títulos bold, que se notan). Cambiar el `<link>` a:
    ```html
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;700;800&display=swap" rel="stylesheet">
    ```
    Esto elimina los pesos 300 y 600 que NO se usan, sin tocar el CSS. (El doc original pedía
    "6→3" pero el 800 de los títulos se vería degradado si se baja a 700; 4 pesos es el punto
    correcto.)
  - **Opción 2 (estricta, 3 pesos):** cargar `400;600;700` y **reasignar en el CSS** las 6
    reglas: `500`→`600` (líneas 451, 1175, 1935) y `800`→`700` (líneas 1647, 1735, 1976).
    Los títulos quedarán algo menos gruesos. Solo si se prioriza el ahorro al máximo.
- `display=swap` ya está; mantenerlo.
- Si se elige Opción 2 se toca `estilos.css` → subir `?v=`. La Opción 1 no toca CSS.
- `display=swap` ya está; mantenerlo.
- **Por qué:** ataca el render-blocking (~1.4 s) y el LCP. Es PERF-1.

### A2 — `og:image` en PNG 1200×630 (en vez de SVG)
- **Dónde:** `templates/base.html` líneas 15-19 (bloque `og_image`).
- **Problema:** WhatsApp/Facebook/X no renderizan `og:image` en SVG. Es PERF-B / PERF-2 del doc.
- **Hacer:**
  1. Crear `static/img/og-default.png` de **1200×630** con el branding (logo amarillo sobre
     fondo `#0f0f0f`, mismo look del hero). Puede generarse desde el SVG existente
     `static/img/og-default.svg` con cualquier conversor a PNG 1200×630.
  2. Actualizar el meta:
     ```html
     <meta property="og:image" content="{{ request.scheme }}://{{ request.get_host }}{% static 'img/og-default.png' %}">
     <meta property="og:image:type" content="image/png">
     <meta property="og:image:width" content="1200">
     <meta property="og:image:height" content="630">
     ```
  3. Mantener `og:image:alt`.
- **No borrar** el SVG todavía (favicon u otros usos); solo cambiar el `og:image`.

### A3 — Cargar `enhanced-select.js` solo donde hay `<select>`
- **Dónde:** `templates/base.html` línea 27 (`<script defer src=".../enhanced-select.js">`).
- **Problema:** se carga en TODAS las páginas, pero solo se usa donde hay `<select>` (filtros,
  formularios staff). Es PERF-C / PERF-3.
- **Hacer:** mover ese `<script>` de `base.html` a un bloque que solo carguen las plantillas
  con select. Patrón sugerido: definir en `base.html` un `{% block extra_js %}{% endblock %}`
  antes de `</body>`, quitar el script del `<head>`, y en las plantillas que tienen `<select>`
  añadir el script dentro de `{% block extra_js %}`.
- **Plantillas con `<select>` a confirmar** (buscar con
  `grep -rln "<select\|custom-select\|enhanced-select" templates/`): listados con filtros
  (`resource_list`, `subject_list`, etc.) y formularios de creación/edición staff
  (`*_form.html`).
- ⚠️ **Cuidado:** si una página con filtros se queda sin el script, el select custom no se
  inicializa. Verificar a ojo cada página de filtros tras el cambio.

### A4 — `preload` del logo del home (elemento LCP)
- **Dónde:** el logo del hero (`templates/pages/home.html`, `static/img/logo.png`) es el LCP
  del home (PERF-4).
- **Hacer:** añadir en el `<head>` (vía un `{% block head_extra %}` en home, o condicional)
  un preload del logo solo en el home:
  ```html
  <link rel="preload" as="image" href="{% static 'img/logo.png' %}">
  ```
- **Opcional (si da el tiempo):** generar `logo.webp` y usar `<picture>` en el hero. Si se hace,
  el preload debe apuntar al WebP. Si no, dejar el PNG.

### Quedan FUERA del Bloque A (no requieren código ahora)
- **Minificar CSS** y **re-medir compresión/cache (PERF-6/7)**: son artefactos del runserver;
  WhiteNoise ya comprime en producción. Se verifican con PageSpeed Insights contra el dominio
  en vivo, no tocando código. Dejar anotado, no implementar.

### Verificación del Bloque A
- Los 3 comandos de la sección "Cómo trabajar" en verde.
- `runserver` + revisar home y una página con filtros (que el select custom siga funcionando).
- Subir `?v=` del CSS solo si se tocó `estilos.css` (A1 si reasignó font-weights).

---

## BLOQUE B — Fase 3-4 de sistema de diseño (refactor CSS)

Rama sugerida: `refactor/css-design-system`. Cierra las Fases 3-4 de
`sistema-diseno-pulido-css.md`. Bajo riesgo, pero revisar visualmente.

### B1 — Sombras en dos niveles
- **Dónde:** `:root` en `static/css/estilos.css` líneas 1-22. Hoy solo existe
  `--shadow: 0 10px 30px rgba(2, 6, 23, 0.08);` (línea 18).
- **Hacer:** añadir dos tokens y migrar usos:
  ```css
  --shadow-sm: 0 1px 3px rgba(2, 6, 23, 0.06), 0 1px 2px rgba(2, 6, 23, 0.04);
  --shadow-md: 0 10px 30px rgba(2, 6, 23, 0.08);
  ```
  Mantener `--shadow` como alias de `--shadow-md` para no romper usos existentes, o reemplazar
  todos los `var(--shadow)` por `var(--shadow-md)`. Usar `--shadow-sm` en hovers/estados sutiles.
- Hay sombras hardcodeadas (p. ej. `box-shadow: 0 8px 20px rgba(...)` en `.content-card:hover`,
  `0 10px 24px rgba(...)`). Migrar las que apliquen a los tokens.

### B2 — Unificar radios sueltos a la escala
- **Tokens actuales:** `--radius: 16px`, `--radius-sm: 10px` (líneas 19-20).
- **Radios sueltos reales (verificado 2026-05-31), normalizar a tokens:**
  - `6px` → líneas **1690, 1788** → `var(--radius-xs)` (nuevo).
  - `8px` → líneas **129, 946, 981** → `var(--radius-xs)` o `var(--radius-sm)`.
  - `12px` → líneas **1563, 1612, 1712, 1864, 2159** → `var(--radius-md)` (nuevo).
  - `14px` → líneas **236, 382, 487, 885, 1024, 1077** → `var(--radius-md)`.
  - `24px` → línea **193** (caja del logo del hero, hecho a propósito) → dejar literal o
    `var(--radius-lg)`; **no es urgente**.
  - `999px` (pills/badges) → líneas **332, 803, 2084, 2091** → `var(--radius-pill)` (nuevo).
  - Nota: decidir si `6px` y `8px` colapsan a un solo `--radius-xs`, y `12px`/`14px` a
    `--radius-md`. Mantener el aspecto: si dos valores se ven distintos a propósito, conservar
    dos tokens. No cambiar px que alteren visiblemente un componente.
- **Decisión:** lo más limpio es definir la escala completa en `:root`:
  ```css
  --radius-xs: 8px;
  --radius-sm: 10px;
  --radius-md: 12px;
  --radius: 16px;     /* = --radius-lg */
  --radius-pill: 999px;
  ```
  y reemplazar cada valor literal por su token. No cambiar el aspecto visual (mismos px).

### B3 — Escala de espaciado y tipográfica en `:root`
- Añadir escalas (no es obligatorio migrar TODO el CSS de golpe; al menos dejar los tokens y
  migrar los componentes principales):
  ```css
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem;
  --space-4: 1rem; --space-5: 1.5rem; --space-6: 2rem;
  --text-sm: 0.875rem; --text-base: 1rem; --text-lg: 1.125rem;
  --text-xl: 1.25rem; --text-2xl: 1.5rem;
  ```
- Migrar los valores sueltos más repetidos (`0.5rem`, `1rem`, `1.5rem`, etc.) a estos tokens
  en los componentes principales. Objetivo: ritmo coherente, sin cambiar el aspecto.

### B4 — Dedup de `.auth-card` y reducir `!important`
- **`.auth-card` está definido DOS veces:** líneas **577** y **1060** de `estilos.css`
  (ambas con `border-radius: var(--radius)` + `box-shadow: var(--shadow)`). Comparar ambos
  bloques, fusionar en uno solo y borrar el duplicado. Verificar login/registro tras el cambio.
- **`!important` (10 usos reales, verificado 2026-05-31):**
  - Líneas **732** y **741**: `display: none !important` (ocultar select nativo en el widget
    custom). Probablemente necesarios; intentar quitar subiendo especificidad; si rompe, dejar.
  - Línea **1285**: `border-color: var(--primary) !important`. Revisar contexto; intentar
    resolver por especificidad.
  - Líneas **1429-1431**: `outline`/`outline-offset`/`box-shadow !important` (estado de foco).
    El foco visible es importante para a11y; probablemente vale dejarlos. Evaluar.
  - Líneas **2001-2003** y **2007**: `background`/`color`/`border !important` del botón WhatsApp
    (`.btn-whatsapp`, verde `#15803d` ya AA). Intentar resolver por especificidad sobre
    `.btn-primary`; si no se puede sin riesgo, dejarlos.
- **Regla:** no eliminar un `!important` si rompe el estilo. La meta es reducir, no romper.

### Verificación del Bloque B
- Los 3 comandos en verde.
- `runserver` + revisar: home, tarjetas (`.content-card`, `.home-link-card`), badges/pills
  (que sigan redondeados), login y registro (`.auth-card`), y un formulario con select.
- Subir `?v=` del CSS.

---

## BLOQUE C — Accesibilidad manual (lo que axe NO detecta)

Rama sugerida: `a11y/keyboard-screenreader`. Cierra las fases manuales de
`auditoria-accesibilidad-axe.md`. **Es el bloque más complejo y el único que requiere prueba
interactiva.** Los hallazgos automáticos (A11Y-1 WhatsApp, A11Y-2 "Ver más") YA están resueltos.

### C1 — Select custom accesible por teclado (`static/js/enhanced-select.js`) — ALTO ESFUERZO
- **Problema:** `enhanced-select.js` reemplaza el `<select>` nativo por un widget propio
  (`estilos.css` lo oculta con `display:none !important`, líneas 733/746). Hay que garantizar
  el patrón **ARIA listbox** y manejo de teclado:
  - El disparador (`<button>`) con `role="combobox"` o botón + `aria-haspopup="listbox"`,
    `aria-expanded` que cambie true/false al abrir/cerrar, `aria-controls` apuntando al listado.
  - El contenedor de opciones con `role="listbox"`; cada opción `role="option"` y
    `aria-selected`.
  - **Teclado:** Enter/Espacio abre; ↑/↓ mueven el foco activo (`aria-activedescendant`);
    Enter selecciona; Esc cierra y devuelve foco al disparador; Tab cierra y avanza. Home/End
    opcional.
  - Sincronizar la selección con el `<select>` nativo oculto para que el form envíe el valor.
- **Alternativa válida y más barata** (si hacerlo accesible resulta caro/riesgoso): **volver al
  `<select>` nativo estilizado** con `appearance: none` + flecha por CSS (ya existe base de
  estilo). El nativo es accesible por defecto. Documentar la decisión.
- **Verificar:** navegar un filtro de `/recursos/` y un form staff SOLO con teclado.

### C2 — `aria-expanded` / `aria-controls` en el menú hamburguesa
- **Dónde:** `templates/base.html` el toggle `<button class="navbar-toggle" aria-label="Abrir menú" id="navbarToggle">` (~línea 45) y su JS asociado (buscar `navbarToggle` en
  `templates/base.html` o en el JS inline/archivo).
- **Hacer:** el botón debe tener `aria-expanded="false"` por defecto y `aria-controls="<id del
  menú>"`; el JS que abre/cierra debe alternar `aria-expanded` a `true`/`false`.
- Bajo esfuerzo. Verificar con teclado que el menú abre/cierra y el atributo cambia.

### C3 — Lector de pantalla (NVDA) — REQUIERE AL USUARIO
- Esto **no lo puede hacer Antigravity ni Claude**: requiere ejecutar NVDA en Windows y
  escuchar. Dejar como tarea para el usuario: recorrer registro, abrir un recurso y usar un
  filtro con NVDA, confirmando que el select anuncia label/estado/opción.
- Antigravity solo deja el código listo (C1/C2); el usuario valida con NVDA.

### Verificación del Bloque C
- Los 3 comandos en verde.
- Navegación por teclado completa en home, `/recursos/` (filtro) y un form staff.
- (Usuario) prueba con NVDA.

---

## Resumen de archivos que se tocan

| Bloque | Archivos principales |
| --- | --- |
| A | `templates/base.html`, `templates/pages/home.html`, plantillas con `<select>`, `static/img/og-default.png` (nuevo), posible `static/css/estilos.css` (font-weights) |
| B | `static/css/estilos.css` (tokens + migración), `templates/base.html` (cache `?v=`) |
| C | `static/js/enhanced-select.js`, `templates/base.html` (menú móvil), plantillas con select |

## Qué verifica Claude después
- Que CI esté verde en cada PR.
- Diff de cada bloque contra este brief (que se haya hecho lo pedido y nada de más).
- Revisión visual con `runserver` de las páginas afectadas.
- Que los documentos de `2 En Proceso/` se actualicen (sección "Qué se hizo") y se muevan a
  `3 Finalizados/` cuando su alcance quede cubierto.
