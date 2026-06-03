# Conversión a PWA (Progressive Web App) para acceso móvil rápido

- **Estado:** Handoff Ready (arquitectura)
- **Creado:** 2026-06-03 · **Handoff refinado:** 2026-06-03 (🏛️ Claude)
- **Prioridad:** P2 · **Cartera:** retención / continuidad
- **Tipo:** producto · infraestructura
- **Dueño sugerido:** 🧩 Codex (preflight) → 🔨 Antigravity (construcción `feat/pwa-basica`) → 🏛️ Claude (cierre)

> **Origen:** plan de 🔨 Antigravity (base) + **Plan v2 de 🧩 Codex** (arquitectura detallada),
> **refinado y corregido por 🏛️ Claude** contra el código real. Las correcciones de abajo son
> vinculantes: el plan original de Codex tenía supuestos desactualizados.

## Decisiones cerradas (🧑 + 🏛️, 2026-06-03)
1. **`theme_color` = `#0f766e`** (teal de marca, `--primary` actual). `background_color = #ffffff`.
2. **QA iOS = opcional post-merge** (no bloquea el cierre; el 🧑 valida "Agregar a inicio" en iPhone después).
3. **Shortcuts del manifest = v1.1** (fuera de v1, para diff acotado).
4. **Precache mínimo** (ver corrección C3): solo `/offline/` + iconos; el resto en runtime.

## 🔴 Correcciones al plan original (verificadas contra el código)
- **C1 — Color:** Codex propuso `theme_color: #ffc400` (amarillo). **INCORRECTO**: era el tema oscuro
  retirado. El `:root` actual usa `--primary: #0f766e`. **Usar `#0f766e`.**
- **C2 — apple-touch-icon:** `templates/base.html` línea 23 ya tiene
  `<link rel="apple-touch-icon" href="{% static 'img/favicon.svg' %}">`. **iOS no soporta SVG** aquí:
  **reemplazar** por un PNG 180×180 real (`apple-touch-icon.png`), no solo "agregar".
- **C3 — Precache de assets hasheados:** producción usa `CompressedManifestStaticFilesStorage`
  (`config/settings/production.py`), así que CSS/JS llevan hash en el nombre. **No precachear rutas
  estáticas fijas** (fallaría en cada build). El SW precachea **solo `/offline/` + iconos**; `/static/`
  se cachea **en runtime** (cache-first). El CSS hasheado se sirve normal por WhiteNoise.
- **C4 — `start_url: /?source=pwa`:** la analítica M5 elimina querystrings antes de registrar el
  `page_view`, así que ese parámetro **no se medirá**. Mantenerlo no daña; para medir uso PWA, detectar
  `display-mode: standalone` en `static/js/analytics.js` (mejora opcional, **no** en v1).

## Objetivo (una frase)
Que ProfeOnline.cl se pueda **instalar en móviles** como PWA (ícono propio, pantalla `standalone`,
fallback offline simple) **sin riesgo de dejar HTML/CSS viejo pegado por caché**.

## Fuentes a leer (rutas concretas)
- `templates/base.html` — `<head>` (líneas ~22-31) para manifest, theme-color y Apple meta; **corregir**
  el `apple-touch-icon` SVG existente (línea 23). Registro del SW al final, antes de `</body>`.
- `apps/core/urls/__init__.py` (`app_name = "core"`) y `apps/core/urls/home_urls.py` — añadir rutas.
- `apps/core/views/` (paquete; ver `home.py`, `analytics_views.py`) — crear `pwa.py` y exportarlo en `__init__.py`.
- `apps/core/middleware.py` — CSP: `script-src 'self' 'nonce-…'`; el `pwa.js` externo de `/static/` entra por `'self'` (no tocar CSP).
- `config/settings/production.py` (WhiteNoise manifest) — razón de servir el SW desde vista Django.
- `static/img/logo.png` — fuente para generar los iconos.

## Propuesta — arquitectura
### Vistas (`apps/core/views/pwa.py`)
- `manifest_json(request)` → JSON del manifest (abajo). `Content-Type: application/manifest+json`.
- `service_worker(request)` → sirve `pwa-sw.js`. Headers: `Content-Type: application/javascript; charset=utf-8`,
  `Cache-Control: no-cache`, `Service-Worker-Allowed: /`.
- `offline(request)` → renderiza `templates/pages/offline.html` (con `noindex`).

### Rutas (`apps/core/urls/home_urls.py`, namespace `core`)
- `manifest.json` → `name="manifest"`
- `service-worker.js` → `name="service_worker"`
- `offline/` → `name="offline"`

### Manifest
- `name`: "ProfeOnline.cl - Clases Particulares Online"
- `short_name`: "ProfeOnline" · `lang`: "es-CL" · `dir`: "ltr" · `categories`: ["education"]
- `description`: "Clases particulares online, apoyo escolar y recursos educativos organizados por asignatura."
- `start_url`: "/?source=pwa" · `scope`: "/" · `display`: "standalone"
- `theme_color`: **"#0f766e"** · `background_color`: "#ffffff"
- `icons`: 192 y 512 (`purpose: any`) + 192 y 512 (`purpose: maskable`)

### Service worker (estrategia conservadora)
- `install`: precachear **solo** `/offline/` + iconos. `self.skipWaiting()`.
- `activate`: borrar cachés con nombre antiguo + `clients.claim()`.
- `fetch`:
  - `request.mode === 'navigate'` → **network-first**, fallback a `/offline/`.
  - GET de `/static/` → **cache-first** con fallback a red (runtime, sin precache de nombres hasheados).
  - Ignorar no-GET y **no cachear**: `/admin/`, `/cuentas/`, `/accounts/`, login/logout, `/eventos/` (analítica), HTML autenticado.
- Caché: `profeonline-pwa-v1` (subir versión ante cada cambio de estrategia).

### Registro (CSP-safe)
- `static/js/pwa.js` (externo, **no inline**) registra el SW si `'serviceWorker' in navigator`.
- En `base.html` `<head>`: `<link rel="manifest" href="{% url 'core:manifest' %}">`, `<meta name="theme-color" content="#0f766e">`,
  `application-name`, `apple-mobile-web-app-capable`, `apple-mobile-web-app-title`, `apple-mobile-web-app-status-bar-style`,
  **reemplazar** `apple-touch-icon` por el PNG. Antes de `</body>`: `<script defer src="{% static 'js/pwa.js' %}?v=1"></script>`.

### Iconos (generar desde `logo.png`)
`static/img/icons/`: `icon-192.png`, `icon-512.png`, `icon-maskable-192.png`, `icon-maskable-512.png`
(con safe-zone), `apple-touch-icon.png` (180×180).

### Offline page (`templates/pages/offline.html`)
- `noindex` (meta robots). Título **"Sin conexión"**; texto **"No pudimos cargar esta página. Cuando
  recuperes internet, vuelve a intentarlo."**; botón **"Volver al inicio"** + link WhatsApp (`wa.me/56937503803`).
- Liviana, alineada a marca, sin depender de assets que requieran red.

## No-objetivos (FUERA de v1)
- ❌ Push notifications. ❌ Caché offline de videos/PDF/formularios/contenido dinámico autenticado.
- ❌ Google Play / App Store (TWA/Bubblewrap es iteración posterior). ❌ Reescritura a API + React Native/Flutter.
- ❌ Prompt agresivo de instalación. ❌ Shortcuts del manifest (van en v1.1). ❌ Tocar `script-src` de la CSP.

## Criterios de aceptación (verificables)
- [ ] `/manifest.json` → 200, `application/manifest+json` (o `application/json`), con `name, short_name, start_url, scope, display, theme_color (#0f766e), icons`.
- [ ] Al menos un icono 192, uno 512 y uno **maskable** declarados.
- [ ] `/service-worker.js` → 200, `application/javascript`, con `Cache-Control: no-cache` y `Service-Worker-Allowed: /`.
- [ ] `/offline/` → 200 y `noindex`.
- [ ] `base.html` incluye manifest, `theme-color #0f766e`, Apple meta tags, **apple-touch-icon PNG** (no SVG) y el `<script>` de registro.
- [ ] El SW se registra sin errores en Chrome DevTools; en modo Offline una navegación recargada muestra `/offline/`.
- [ ] Lighthouse PWA sin errores bloqueantes de instalabilidad; en Android/Chrome aparece "Instalar / Agregar a pantalla principal".
- [ ] **CSP intacta**: sigue usando nonce, sin `unsafe-eval`, sin nuevos inline (verificado por test).
- [ ] Barrera verde: `test` · `check --deploy` · `makemigrations --check --dry-run`.

## Plan de pruebas
- **Automáticas** (`apps/core/tests.py`): `test_manifest_json_served_with_required_fields`,
  `test_manifest_icons_are_declared` (192+512+maskable), `test_service_worker_served_from_root_with_no_cache_headers`
  (+ `Service-Worker-Allowed`), `test_offline_page_renders` (+ noindex), `test_base_template_links_manifest_and_pwa_script`,
  `test_csp_still_uses_nonce_without_unsafe_eval`.
- **QA manual:** DevTools→Application (manifest, SW activo, iconos); Network→Offline recarga `/`;
  Lighthouse PWA/Accessibility/Best-Practices; Android Chrome instalar+standalone.
- **iOS:** opcional post-merge (🧑): "Agregar a inicio" en Safari, ícono correcto, abre standalone.

## Riesgos / rollback
- **Caché agresiva** (principal): mitigada con network-first en navegación + `no-cache` en el SW + `skipWaiting`/`claim` + caché versionada.
- **CSP:** `pwa.js` externo de `/static/` ('self'); no se añade inline.
- **iOS:** apple-touch PNG + Apple meta tags; no depender solo del manifest.
- **WhiteNoise manifest:** SW servido desde vista Django (raíz), nunca desde `/static/`.
- **Rollback suave:** quitar el `<script>` de `pwa.js` de `base.html` (el manifest queda inerte).
- **Rollback fuerte:** publicar un `pwa.js` que desregistre SWs (`getRegistrations().then(rs=>rs.forEach(r=>r.unregister()))`) + SW que limpie cachés; retirar rutas en PR posterior.

## Preflight para 🧩 Codex
- Confirmar que no exista SW previo (✅ verificado por Claude: solo `htmx.min.js` y `analytics.js`).
- Que `base.html` sea el punto global de registro y la CSP permita `pwa.js` ('self') sin tocar `script-src`.
- Que WhiteNoise no sirva el SW desde `/static/`; que el precache no use nombres hasheados (corrección C3).
- Que los tests de SEO/CSP existentes no se rompan; que no se cacheen rutas privadas.

## Construcción para 🔨 Antigravity
Rama `feat/pwa-basica`, diff acotado: vistas+rutas PWA, iconos, `pwa.js` externo, `offline.html`,
registro en `base.html` (corrigiendo el apple-touch-icon), tests, barrera verde. Completar "Qué se hizo".

## Iteración posterior (v1.1+)
CTA suave "Agregar a inicio" por navegador · `shortcuts` del manifest · medición `display-mode: standalone`
en analytics · `screenshots` del manifest · TWA/Bubblewrap para Play Store si se valida valor comercial.

---

## Qué se hizo
_(Completar al finalizar, antes de mover a `backlog/6-finalizados/`.)_
