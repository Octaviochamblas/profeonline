# Sistema de diseño y pulido fino del CSS

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** Estética
- **Prioridad:** 🟡 Media (alto retorno, bajo riesgo)

## Problema / Objetivo

`static/css/estilos.css` (~2.187 líneas) está bien hecho y es consistente, pero tiene
detalles que, pulidos, elevan la percepción de "profesional / premium". No es un rediseño:
son ajustes de **ritmo, color y profundidad** sobre la base existente.

Objetivo: convertir el CSS actual en un pequeño **sistema de diseño** con escalas coherentes,
y aplicar pulido fino que se note de inmediato.

## Diagnóstico del CSS actual

1. **Espaciado sin escala.** Conviven valores sueltos: `0.875rem`, `0.9rem`, `0.85rem`,
   `1.25rem`, `1.5rem`, `0.625rem`… Falta una escala de espaciado (`--space-1…6`) que dé
   ritmo visual uniforme.
2. **Sobreuso del amarillo.** `--primary #FFD100` aparece en títulos, enlaces, badges, iconos,
   bordes, foco… Usado con moderación se ve premium; saturado, cansa y resta jerarquía.
   Conviene reservar el amarillo para acciones/acentos, no para todo texto destacado.
3. **Sombras muy duras.** `--shadow: 0 10px 30px rgba(0,0,0,0.5)` y hovers con
   `rgba(0,0,0,0.6)`. Sombras más suaves y en capas (dos niveles) se ven más modernas.
4. **Solo dos radios** (`--radius 16px`, `--radius-sm 10px`) usados de forma despareja
   (aparecen `12px`, `14px`, `999px` sueltos). Unificar la escala de radios.
5. **Tipografía.** 6 pesos de Outfit cargados; jerarquía de tamaños correcta pero mejorable
   con escala tipográfica explícita y mejor `line-height` en texto largo.
6. **Reglas duplicadas / `!important`.** Hay bloques repetidos (`.auth-card` definido dos
   veces) y varios `!important` (botones WhatsApp, focus) que conviene consolidar.

## Ruta de trabajo

### Fase 1 — Tokens del sistema de diseño
- Añadir al `:root` escalas: `--space-*`, `--radius-*`, `--shadow-sm/--shadow-md`, y una
  escala tipográfica (`--text-sm/base/lg/xl…`).
- Si se decidió tema claro/híbrido (`decision-tema-claro-oscuro.md`), definir aquí la paleta.

### Fase 2 — Refactor de color
- Reservar el amarillo para CTAs, foco y acentos puntuales.
- Para títulos/enlaces de tarjetas, evaluar texto claro normal en vez de amarillo constante.
- Ajustar `--muted` para cumplir contraste AA (coordinar con auditoría de accesibilidad).

### Fase 3 — Profundidad y radios
- Migrar a `--shadow-sm`/`--shadow-md` en capas.
- Unificar radios sueltos (`12px`/`14px`) a la escala.

### Fase 4 — Limpieza
- Eliminar la definición duplicada de `.auth-card` y reglas muertas.
- Reducir `!important` consolidando especificidad.
- Reducir Outfit a 3 pesos si la auditoría de rendimiento lo confirma.

### Fase 5 — Verificación visual
- Revisar todas las páginas clave tras los cambios (no romper componentes existentes).
- Subir el `?v=` del CSS en `base.html` para bustear cache.

## Criterios de aceptación

- `:root` tiene escalas coherentes de espaciado, radios, sombras y tipografía.
- El amarillo se usa con intención (acentos/CTAs), no en todo.
- Contraste de texto cumple AA.
- Sin reglas duplicadas ni `!important` innecesarios.
- Ninguna página clave se rompe visualmente.

## Notas / Consideraciones

- **Depende de `decision-tema-claro-oscuro.md`** para la paleta final.
- Es refactor de bajo riesgo si se hace por fases y se revisa visualmente cada una.
- Trabajar sobre los tokens evita tocar componente por componente.

---

## Qué se hizo

### Migración a TEMA CLARO — paleta C endurecida (2026-05-31, sesión 2) — ✅ EN VIVO

Se implementó y desplegó el tema claro (PR #9, squash `17936e1`, mergeado a `main`;
Railway desplegó tras CI verde). Cubre **Fase 1 (tokens)** y **Fase 2 (refactor de color)**
del documento, más los fixes de accesibilidad.

**Decisión de color (sobre el feedback del prototipo C):** el usuario eligió la paleta C
(teal + ámbar) pero marcó dos fallos de contraste (botones oscuros con texto verde, y texto
del header). Se diagnosticó que **no eran del teal**, sino restos del tema oscuro que el
prototipo (override solo de `:root`) no podía tocar. Paleta final:
- Neutros: `--bg #f8fafc`, `--surface #fff`, `--surface-soft #f1f5f9`, `--border #e2e8f0`,
  `--text #0f172a` (17:1), `--muted #475569` (7.5:1).
- **`--primary` → teal `#0f766e`** (5.5:1): reusa todos los `var(--primary)` existentes
  (enlaces, títulos, bordes, foco) → el amarillo-como-texto desapareció solo.
- **Nuevo `--cta` ámbar `#f59e0b`** + `--cta-contrast #422006` (6.8:1), solo en `.btn-primary`.
- Sombras de negro duro → slate suave (`rgba(2,6,23,…)`).

**Colores hardcodeados arreglados** (no heredaban de `:root`): header a blanco frosted;
encabezados blancos (`h1-h3`, `.page-hero__kicker`, `.bottom-contact-cta__title`, hover de
navegación, 2 `h2` inline en `subject_list`/`topic_list`) → oscuro; badges/chips oscuros,
zebra de tablas, hovers y skeleton → claros; tints amarillos → teal; rojos de error y verdes
de "completado" oscurecidos para AA.

**Accesibilidad (cierra hallazgos de `auditoria-accesibilidad-axe.md`):**
- **A11Y-1**: verde WhatsApp `#25d366` → `#15803d` (blanco 5:1, AA).
- **A11Y-2**: aria-labels "Ver más" ahora incluyen el texto visible.

**Extra (hallazgos de la revisión visual):**
- Logo del hero: `drop-shadow` **provisional** para que el wordmark amarillo se separe del
  fondo blanco (pendiente la variante de asset definitiva).
- `/accounts/login/` y `/accounts/signup/` de allauth salían **sin estilo** → se redirigen al
  flujo propio estilizado (`/cuentas/login/`, `/cuentas/registro/`), mismo patrón que el
  reset de contraseña. Verificado con curl (302) y 87 tests OK.

Cache CSS `?v=6` → `?v=7`.

### Variante del logo para fondo claro (2026-05-31, sesión 3) — ✅ HECHO

El wordmark original (`static/img/logo.png`) es amarillo `#FFD100` plano sobre transparente;
sobre el hero claro perdía contraste (parche provisional `drop-shadow`). Se generó una
variante **slate `#0f172a`** (≈17:1 contra el fondo, el mismo `--text`), recoloreando la
máscara alfa del PNG con `scripts/recolor_logo.py` (Pillow, herramienta local; no va a
`requirements.txt`). Resultado: `static/img/logo-dark.png`.

- `templates/pages/home.html` ahora usa `img/logo-dark.png` en el hero.
- Eliminado el `drop-shadow` provisional de `.page-hero__logo` en `estilos.css`.
- El amarillo queda reservado a los CTAs (filosofía del tema).
- Cache CSS `?v=7` → `?v=8`.

### Pendiente en esta tarjeta (Fases 3-4, NO hechas) — sigue en `2 En Proceso/`
- **Fase 3 (profundidad/radios):** unificar radios sueltos (`12px`/`14px`/`999px`) a escala;
  sombras en dos niveles `--shadow-sm`/`--shadow-md`.
- **Fase 4 (limpieza):** escala de espaciado `--space-*` y tipográfica `--text-*`;
  **dedup de `.auth-card`** (definido 2 veces); reducir `!important`; **reducir Outfit de 6→3
  pesos** (también ataca el render-blocking de la auditoría de rendimiento).

> Se mantiene en **En Proceso**: el grueso (tema + contraste + a11y) está en vivo, pero las
> fases de sistema de diseño/limpieza siguen pendientes.
