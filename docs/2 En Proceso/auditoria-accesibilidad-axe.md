# Auditoría real de accesibilidad (axe + teclado + contraste)

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** Auditoría
- **Prioridad:** 🔴 Alta

## Problema / Objetivo

La auditoría WCAG previa (PEND-007) nunca se validó con herramientas reales (axe, lector de
pantalla, navegación por teclado). Hay buenas intenciones en el CSS (`:focus-visible` global,
`aria-label` en varios sitios), pero **falta evidencia**. El punto más riesgoso es el
dropdown custom (`static/js/enhanced-select.js`), que reemplaza el `<select>` nativo y suele
romper el acceso por teclado y lector.

Objetivo: detectar y corregir barreras de accesibilidad reales, priorizando teclado, lector
de pantalla y contraste.

## Diagnóstico inicial (a confirmar)

1. **Select custom (riesgo principal).** `estilos.css` oculta el select nativo
   (`.enhanced-select-native { display: none !important; }`, `.custom-select-wrapper > select
   { display: none }`) y dibuja uno propio con `<button>`/divs. Hay que verificar:
   navegación con Tab/flechas/Enter/Escape, `role="listbox"`/`aria-expanded`,
   anuncio de la opción seleccionada por lector, y comportamiento sin JS.
2. **Contraste de color (probable hallazgo AA).** Pares a verificar con un checker:
   - Texto `--muted #9ca3af` sobre `--surface #1a1a1a` → cercano al límite AA (4.5:1).
   - `.top-contact-bar` usa `--muted` sobre `#0f0f0f`.
   - Amarillo `--primary #FFD100` como **texto** sobre superficies oscuras (enlaces, títulos
     de tarjetas) → verificar; como texto necesita 4.5:1.
   - Badges con texto de color tenue (`#86efac`, `#fca5a5`) sobre fondos translúcidos.
3. **Menú hamburguesa.** El toggle en `base.html` usa `<button aria-label="Abrir menú">` pero
   le falta `aria-expanded`/`aria-controls` que se actualice al abrir/cerrar.
4. **Jerarquía de encabezados.** Verificar que cada página tenga un único `<h1>` y no se salte
   niveles (el home usa varios `<h2>` correctamente, revisar el resto).
5. **Foco visible.** Ya existe regla global `:focus-visible` (buena base) — confirmar que no
   se anula en componentes custom.
6. **Imágenes/iconos.** Los SVG decorativos usan `aria-hidden="true"` (correcto en el home);
   revisar que el logo tenga `alt` significativo (lo tiene).

## Ruta de trabajo

### Fase 1 — Escaneo automatizado
- Pasar **axe DevTools** (o `@axe-core/playwright`) por: home, `resource_list`,
  `resource_detail`, `subject_detail`, login, registro, formularios de creación (staff).
- Registrar violaciones por severidad (critical/serious/moderate).

### Fase 2 — Pruebas manuales de teclado
- Recorrer cada página **solo con teclado** (Tab, Shift+Tab, Enter, Espacio, flechas, Esc).
- Foco especial en el select custom y en el menú móvil.
- Verificar orden de foco lógico y que no haya trampas de foco.

### Fase 3 — Lector de pantalla
- Probar con NVDA (Windows) las rutas críticas: registro, abrir un recurso, usar un filtro.
- Confirmar que el select custom anuncia label, estado y opción elegida.

### Fase 4 — Contraste
- Verificar todos los pares de color del `:root` con un contrast checker (objetivo AA 4.5:1
  texto normal, 3:1 texto grande/UI).
- Ajustar `--muted` o los usos de amarillo-como-texto donde no cumplan.

### Fase 5 — Correcciones y re-test
- Corregir por orden de severidad; re-pasar axe y teclado.

## Checklist de hallazgos

| ID | Componente | Criterio WCAG | Problema | Recomendación | Estado |
| --- | --- | --- | --- | --- | --- |
| A11Y-A | enhanced-select | 2.1.1, 4.1.2 | Posible falta de soporte teclado/ARIA | Implementar patrón listbox accesible o volver a `<select>` estilizado | Hecho: vuelta a `<select>` nativo estilizado |
| A11Y-B | Paleta | 1.4.3 | `--muted` y amarillo-texto cerca del límite | Ajustar tokens de color | Hecho: tema claro + WhatsApp AA |
| A11Y-C | Menú móvil | 4.1.2 | Falta `aria-expanded`/`aria-controls` dinámico | Sincronizar atributo en el toggle JS | Hecho |

## Criterios de aceptación

- Cero violaciones **critical/serious** en axe en las páginas clave.
- Todas las funciones se pueden usar **solo con teclado**, incluido el select custom.
- Todos los pares de color cumplen AA (o se documenta excepción justificada).
- El select custom anuncia correctamente con lector de pantalla.

## Notas / Consideraciones

- Si el select custom resulta inviable de hacer accesible, evaluar **volver al `<select>`
  nativo estilizado** (suficiente con el `appearance: none` + flecha CSS que ya existe).
- Relacionado con `sistema-diseno-pulido-css.md` (los ajustes de contraste tocan los tokens).

---

## Qué se hizo

### Escaneo automatizado realizado (2026-05-31, axe-core vía Lighthouse, mobile)

Puntaje de accesibilidad **95–96/100** en las 4 páginas auditadas (home, recursos, detalle
de recurso, detalle de asignatura). Dos hallazgos concretos:

| ID | Audit (WCAG) | Elemento exacto | Diagnóstico | Fix propuesto |
| --- | --- | --- | --- | --- |
| A11Y-1 | `color-contrast` (1.4.3) | Botón **WhatsApp** `<a class="btn btn-primary btn-whatsapp">` (texto blanco sobre `#25d366`) — aparece en todas las páginas vía `base.html` | Blanco sobre verde `#25d366` no llega a 4.5:1 | Oscurecer el verde o usar texto oscuro; ajustar `.btn-whatsapp` en `estilos.css` |
| A11Y-2 | `label-content-name-mismatch` (2.5.3) | Tarjetas "Ver más" en home: `<a class="home-more-card" aria-label="Ver todas las asignaturas">` (texto visible "Ver más") | El nombre accesible (aria-label) no contiene el texto visible "Ver más" | Que el `aria-label` incluya "Ver más" (p. ej. "Ver más: asignaturas") o quitarlo |

> **Hallazgo notable:** el problema de contraste **no** era el gris `--muted` ni el amarillo
> que sospechábamos en el diagnóstico inicial (esos pasan AA). El único contraste que falla
> es el **botón verde de WhatsApp**. Buen recordatorio de medir antes de asumir.

### Lo que ESTE escaneo NO cubre (sigue pendiente)

axe automatizado detecta ~30–40% de los problemas de accesibilidad. **Quedan por hacer las
fases manuales** del documento, que son las que de verdad importan aquí:

- **Navegación por teclado** completa (Tab/flechas/Enter/Esc), con foco en el **select custom**
  (`enhanced-select.js`) y el menú móvil. *Lighthouse no lo prueba.*
- **Lector de pantalla** (NVDA): confirmar que el select custom anuncia label/estado/opción.
- **`aria-expanded`/`aria-controls`** en el toggle del menú móvil (no lo flaggeó axe, pero es
  del diagnóstico).

### Estado
Fase de escaneo automatizado **completa y documentada**. Las fases manuales (teclado, lector,
select custom) quedan pendientes — requieren prueba interactiva. Los dos fixes A11Y-1 y A11Y-2
son rápidos y se pueden agrupar con `sistema-diseno-pulido-css.md`.

### Verificacion posterior de Bloque C (2026-05-31)

Se contrasto el handoff de Antigravity con el codigo actual:
- El selector custom ya no esta activo: no existe `static/js/enhanced-select.js` y las
  plantillas revisadas usan `<select>` nativo.
- Se elimino el CSS muerto que podia volver a ocultar selects con `.enhanced-select-native` o
  `.custom-select-wrapper > select`.
- El toggle movil en `templates/base.html` tiene `aria-expanded="false"` y
  `aria-controls="navbarMenu"`; el script inline alterna `aria-expanded`.
- Las tarjetas "Ver mas" del home ya no tienen mismatch de nombre accesible.

Pendiente real: prueba manual con teclado/NVDA por parte del usuario en Windows para validar
la experiencia anunciada por lector de pantalla.
