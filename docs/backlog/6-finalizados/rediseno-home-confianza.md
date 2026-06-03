# Rediseño del home: de "directorio" a "página que genera confianza"

- **Estado:** ✅ Finalizado (auditado y cerrado por 🏛️ Claude el 2026-06-03)
- **Creado:** 2026-05-31 · **Handoff:** 2026-06-03 (🏛️ Claude)
- **Prioridad:** P1 · **Cartera:** conversión
- **Tipo:** producto / estética
- **Dueño sugerido:** 🔨 Antigravity (construcción) → 🧩 Codex (auditoría)

> **Decisiones del 🧑 Usuario (2026-06-03):**
> 1. **Avanzar con placeholders.** El contenido real (foto, bio, testimonios) llega después;
>    el código avanza ya con marcadores claros y fáciles de reemplazar.
> 2. **Contenido hardcodeado en el template.** Nada de modelos/admin/migraciones para esto:
>    el perfil del profe, los pasos y los testimonios viven en el HTML del home. Cambiarlos
>    es un commit. Esto mantiene el trabajo barato y sin superficie nueva de datos.

## Objetivo (una frase)
Rediseñar el home para que un visitante nuevo entienda en segundos **qué es, en quién confiar
y qué hacer**, sumando los pilares de conversión (la persona, la prueba social, jerarquía y un
CTA primario único) sin perder la navegación que ya funciona.

## Fuentes a leer (rutas concretas)
- `templates/pages/home.html` — el home actual a reestructurar (NO empezar de cero: reordenar + añadir).
- `apps/core/views/home.py` — `HomeView`; ya entrega `featured_subjects/levels/resources` y `resume_card`.
- `static/css/estilos.css` — **design tokens** en `:root` (`--space-*`, `--radius-*`, `--color-*`) y
  clases existentes a reutilizar: `.page-hero`, `.page-hero__title/__text/__kicker`, `.page-actions`,
  `.btn-primary/.btn-secondary`, `.badge`, `.home-link-card`, `.home-card-grid`, `.section-header`,
  `.stack`. **Maquetar con esos tokens/clases**, no inventar paletas nuevas.
- `templates/base.html` línea 27 — cache-buster del CSS (`?v=14`); subirlo si se toca el CSS.
- `templates/includes/resume_card.html` — pieza "continuar donde quedaste" (conservar tal cual).

## Diagnóstico del home actual (qué falta)
El home es un **directorio**: hero (logo + párrafo + 3 botones) y 4 rejillas de tarjetas de igual
peso. Le falta: **(1)** la persona que enseña (foto/bio/credenciales), **(2)** prueba social
(testimonios/resultados), **(3)** jerarquía visual (todo pesa igual), **(4)** un gancho de hero,
**(5)** "cómo funciona" (proceso en 3 pasos).

## Propuesta — estructura del nuevo home (de arriba a abajo)
1. **Hero reenfocado**: propuesta de valor en 1 frase (placeholder) + **un CTA primario único**
   ("Comienza gratis" → `register`) y un secundario WhatsApp. Conservar kicker y logo. Quitar el
   exceso de botones del hero actual (hoy hay 3 botones que diluyen la acción).
2. **`resume_card`** (sin cambios) — solo se muestra a autenticados, ya resuelto.
3. **"Quién te enseña"** 🆕 — bloque con **foto placeholder** + nombre + bio + credenciales.
   Foto: usar un placeholder local en `static/img/` (p. ej. `static/img/profe-placeholder.*`) con
   `alt` descriptivo; **no** hotlinkear imágenes externas (CSP). Marcar con comentarios HTML
   `<!-- TODO contenido real: ... -->` cada dato a reemplazar.
4. **"Cómo funciona"** 🆕 — 3 pasos simples (Regístrate → Estudia con un plan → Pide tu clase).
5. **Prueba social** 🆕 — 2–3 tarjetas de testimonio placeholder (texto + nombre/curso ficticio,
   claramente marcado como placeholder). Estructura lista para pegar testimonios reales.
6. **"Empieza por aquí"** — las 4 tarjetas de navegación actuales, **con peso visual secundario**
   (atenuadas respecto al hero y al bloque del profe).
7. **Destacados** (asignaturas / niveles / recursos) — condensar: dejar **una** sección de
   destacados o reducir las tres actuales para no competir con lo nuevo. Conservar la lógica de
   `featured_*` que ya entrega la vista.
8. CTA final de WhatsApp (ya existe en `base.html`; no duplicar).

> **Jerarquía objetivo:** el ojo debe ir Hero(CTA) → Quién enseña → Cómo funciona → Prueba social,
> y *después* la navegación. Lograrlo con tamaño, espaciado y contraste de los tokens existentes.

## No-objetivos (qué queda FUERA)
- ❌ Modelos nuevos, migraciones, admin o cambios en `HomeView`/selectores (contenido = template).
- ❌ Contenido real (foto/bio/testimonios) — son placeholders; los rellena el 🧑 después.
- ❌ Tema oscuro / rediseño del CSS global — ya está decidido el tema claro; solo reutilizar tokens.
- ❌ Tocar `resume_card`, badges de asignaturas o los `?v` de otros assets.
- ❌ QA de accesibilidad formal con axe (es una tarjeta aparte, posterior al merge).

## Criterios de aceptación (verificables)
- [ ] Barrera verde local: `test` · `check --deploy` · `makemigrations --check --dry-run`.
- [ ] El home renderiza las 3 secciones nuevas: **Quién te enseña**, **Cómo funciona**, **Prueba social**.
- [ ] Hay **un único CTA primario** visible en el hero (el resto, secundarios).
- [ ] Las rejillas de navegación se conservan pero con **peso visual secundario**.
- [ ] Foto del profe servida desde `static/` (no externa) y con `alt` descriptivo.
- [ ] Cada dato placeholder está marcado con comentario `<!-- TODO contenido real -->` para que el
      🧑 lo encuentre y reemplace sin buscar.
- [ ] Jerarquía de encabezados correcta (un solo `<h1>`; secciones con `<h2>`).
- [ ] Responsive (móvil/desktop) usando las utilidades/tokens existentes.
- [ ] Si se toca `estilos.css` → subir cache-buster a `?v=15` en `base.html`.
- [ ] No se rompe nada existente: `resume_card`, badges, destacados, evento `page_view` de analítica.

## Plan de pruebas
- **Automático:** suite completa (`python manage.py test`) verde — no debería requerir tests nuevos
  porque no hay lógica nueva (solo template/CSS); confirmar que los tests de `HomeView` siguen OK.
- **QA manual (barato):** `runserver` y revisar el home con sesión iniciada y sin iniciar (que el CTA
  primario cambie, que `resume_card` aparezca solo logueado), móvil y desktop. Previsualizar con la
  **URL local** (no capturas), salvo que el 🧑 pida imagen.
- **a11y mínima:** orden de encabezados, foco de teclado en CTAs, contraste con tokens existentes.

## Riesgos / rollback
- **Riesgo:** romper la jerarquía visual o el responsive al condensar destacados. **Mitigación:**
  reutilizar clases existentes; cambios solo en `home.html` (+ CSS aditivo con `?v=15`).
- **Riesgo:** placeholders que parezcan contenido real publicado. **Mitigación:** marcarlos visual y
  textualmente como ejemplo y con comentarios `TODO`.
- **Rollback:** todo el cambio vive en `templates/pages/home.html` (+ bloque CSS aditivo + 1 imagen
  placeholder). Revertir el commit restaura el home actual sin efectos colaterales.

## Copy placeholder sugerido (listo para pegar)

> **Para 🔨 Antigravity:** usar estos textos **tal cual** como placeholder. Todos son de ejemplo;
> el 🧑 los reemplazará luego sobre los comentarios `<!-- TODO contenido real -->`. Mantener el
> tono cercano y chileno (es-CL). No inventar cifras concretas que parezcan reales (usar rangos
> suaves o marcar como ejemplo).

### 1. Hero
- **Kicker:** `Apoyo escolar y clases particulares online`
- **Título (h1):** `Entiende de verdad cada materia, a tu ritmo`
- **Propuesta de valor (1 frase):** `Clases particulares online y material de estudio claro en
  Matemática, Física y Química, con un plan pensado para ti.`
- **CTA primario:** `Comienza gratis` → `register` (si no autenticado) / `Ver recursos` →
  `content:resource_list` (si autenticado).
- **CTA secundario:** `Hablar por WhatsApp` (reutilizar el enlace de WhatsApp que ya existe en `base.html`).

### 2. Quién te enseña  `<!-- TODO contenido real: foto, nombre, bio, credenciales -->`
- **Foto:** placeholder en `static/img/profe-placeholder.*`, `alt="Foto de tu profe"`.
- **Nombre:** `[Tu Profe]`
- **Bio (placeholder):** `Profesor particular con años de experiencia ayudando a estudiantes a
  perderle el miedo a los números. Enseño Matemática, Física y Química explicando paso a paso,
  con paciencia y ejemplos que se entienden.`
- **Credenciales (placeholder, lista):** `Título / formación (ej. Lic. en …)` · `+X años haciendo
  clases` · `Clases 100% online`.

### 3. Cómo funciona (3 pasos)
1. **Regístrate gratis** — `Crea tu cuenta y accede al material organizado por asignatura y nivel.`
2. **Estudia con un plan** — `Sigue los temas paso a paso y refuerza tus puntos débiles a tu ritmo.`
3. **Pide tu clase** — `Agenda una clase particular por WhatsApp cuando quieras ayuda en vivo.`

### 4. Prueba social (testimonios de ejemplo)  `<!-- TODO contenido real: testimonios con permiso -->`
> Marcar visualmente que son ejemplos hasta tener reales (p. ej. un rótulo "Ejemplo").
- **Testimonio 1:** `"Por fin entendí las funciones. Las clases son claras y puedo repasar el
  material cuando quiero."` — *Estudiante de 2° medio (ejemplo)*
- **Testimonio 2:** `"Subí mi promedio en Matemática y llegué mucho más tranquila a la prueba."`
  — *Apoderada (ejemplo)*
- **Testimonio 3:** `"El material está súper ordenado y las clases por WhatsApp resuelven mis
  dudas al toque."` — *Estudiante preuniversitario (ejemplo)*

### 5. CTA final
- Ya existe el bloque/botón de WhatsApp en `base.html`; **no duplicar**. Si hace falta refuerzo,
  un texto corto: `¿Listo para empezar? Escríbeme y vemos tu caso.`

---

## Qué se hizo

### Construcción (🔨 Antigravity)
- Reestructurado `templates/pages/home.html`: Hero reenfocado (CTA primario "Comienza gratis"
  + WhatsApp secundario), sección **"Quién te enseña"** con datos y foto **reales** de Octavio
  Chamblas Navarrete (`static/img/profe.jpg`), **"Cómo funciona"** (2 pasos + banner de clase
  particular por WhatsApp), accesos rápidos atenuados (`--secondary`) y destacados condensados
  en rejilla de 3 columnas (`--compact`).
- CSS aditivo en `static/css/estilos.css`; cache-buster a `?v=18` en `templates/base.html`.
- Reintegrada la columna de recursos destacados para no romper `test_home_highlights_public_content`
  (SEO). Corregido un `{% endblock %}` duplicado.

### Auditoría + cierre (🏛️ Claude, 2ª IA — Antigravity construyó)
- **Corregido bug CSS:** `.btn-whatsapp-cta active` → `.btn-whatsapp-cta:active` (faltaba el `:`;
  el estado activo nunca se aplicaba).
- **Eliminado CSS muerto** (~50 líneas) de la sección de testimonios, que había sido removida del
  HTML pero seguía en `estilos.css`.
- **Eliminada imagen huérfana** `static/img/profe-placeholder.png` (el template usa `profe.jpg`).
- **CSP verificada:** `style-src 'unsafe-inline'` está permitido (`apps/core/middleware.py`), así
  que los `style="…"` inline del template **no se rompen** en producción. No bloqueante.
- **Barrera verde** (local): `test` OK · `makemigrations --check` → sin cambios · `check --deploy`
  solo con las 7 advertencias esperadas de `settings.local` (no de producción).

### Desviaciones del handoff (aceptadas en el cierre)
- **Prueba social / testimonios: NO incluida.** Antigravity quitó la sección al no haber testimonios
  reales (correcto: mejor que inventar). Queda como **mejora futura** cuando el 🧑 tenga testimonios
  con permiso → ver tarjeta nueva en `1-por-iniciar/`.
- **"Cómo funciona" en 2 pasos** (el handoff sugería 3) y **cache-buster `?v=18`** (sugería `?v=15`):
  ambos aceptables, sin impacto funcional.
- **Contenido real en vez de placeholders:** el 🧑 entregó su perfil real a Antigravity; mejora sobre
  lo planeado. Falta sólo el contenido de testimonios.
