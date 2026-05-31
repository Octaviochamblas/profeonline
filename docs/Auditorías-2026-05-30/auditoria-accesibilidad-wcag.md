# Auditoria de Accesibilidad WCAG

Fecha de creacion: 2026-05-24
Estado: pendiente de ejecucion
Objetivo: detectar y corregir barreras de acceso para usuarios que navegan con teclado, lector de pantalla, zoom, dispositivos moviles o baja vision.

## Alcance recomendado

- Home.
- Listado de recursos.
- Filtros y buscador de recursos.
- Detalle de recurso.
- Landings de asignatura y nivel.
- Login, registro, perfil y edicion de perfil.
- Formularios de crear/editar/eliminar contenido.
- Dropdowns custom de `static/js/enhanced-select.js`.
- Mensajes flash, errores de formulario, estados vacios y paginacion.

## Pasos de auditoria

1. Revisar navegacion solo con teclado.
   - Tab, Shift+Tab, Enter, Space, Escape y flechas.
   - Confirmar que el foco visible nunca se pierde.
   - Confirmar que no hay trampas de foco.

2. Revisar semantica HTML.
   - Un solo `h1` por pagina.
   - Orden logico de headings.
   - Formularios con `label` asociado.
   - Botones reales para acciones y enlaces reales para navegacion.

3. Revisar contraste y legibilidad.
   - Texto normal contra fondo.
   - Texto en badges, botones y tablas.
   - Estados hover/focus/disabled.
   - Mensajes de error/exito.

4. Revisar formularios.
   - Errores visibles y asociados al campo.
   - Campos obligatorios claros.
   - Inputs, selects, textareas y checkboxes usables en movil.
   - No depender solo de color para comunicar error o estado.

5. Revisar componentes dinamicos.
   - Dropdowns custom con roles ARIA adecuados.
   - Texto visible sincronizado con select nativo.
   - Compatibilidad con lector de pantalla.
   - Escape cierra menus.
   - Tab avanza al siguiente control esperado.

6. Revisar zoom y responsive.
   - 200% de zoom en desktop.
   - Mobile pequeno.
   - Sin texto cortado, solapado o controles fuera del viewport.

7. Revisar contenido no textual.
   - Imagenes con `alt` util cuando correspondan.
   - Iconos decorativos ocultos si no aportan significado.
   - Iframes de YouTube con `title` descriptivo.

## Herramientas sugeridas

- Playwright para navegacion desktop/mobile.
- DevTools Lighthouse Accessibility.
- axe DevTools o `@axe-core/playwright`.
- Navegacion manual con teclado.
- Lector de pantalla: NVDA en Windows o VoiceOver en macOS.

## Checklist de hallazgos

| ID | Pagina/componente | Problema | Severidad | Recomendacion | Estado | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| A11Y-001 | Detalle de recurso | Iframe de YouTube sin atributo `title` descriptivo | Media | Agregar `title` descriptivo | Resuelto | |
| A11Y-002 | Selectores custom | Sin mapeo `aria-controls` al listbox de opciones | Media | Asociar `aria-controls` | Resuelto | |
| A11Y-003 | Selectores custom | Bloqueo al tabular para avanzar si el dropdown está abierto | Alta | Cerrar el select al presionar Tab | Resuelto | |
| A11Y-004 | Formularios Django | Campos obligatorios no informan su estado a lectores de pantalla | Baja | Agregar `aria-required="true"` automáticamente | Resuelto | |
| A11Y-005 | Estilos globales | Ausencia de un anillo de foco consistente y visible en teclado | Alta | Implementar estilos `:focus-visible` unificados | Resuelto | |

## Recomendaciones iniciales probables

- Agregar `title` al iframe de YouTube en detalle de recurso. (Completado)
- Confirmar que dropdowns custom tengan comportamiento equivalente al select nativo. (Completado)
- Revisar si `aria-hidden="true"` en selects ocultos afecta lectores de pantalla. (Completado)
- Crear estilos de foco visibles y consistentes para botones, enlaces y campos. (Completado)
- Mejorar mensajes de error de formulario con asociacion semantica. (Completado)

## Criterios de aceptacion

- Toda accion principal se puede completar con teclado.
- El foco visible es claro en todas las paginas auditadas.
- Los formularios anuncian errores de forma comprensible.
- No hay texto solapado ni controles inaccesibles en mobile.
- Lighthouse Accessibility no muestra errores criticos.
- Los hallazgos abiertos quedan documentados con prioridad.

## Registro de cambios aplicados

| Fecha | Cambio | Archivo(s) | Validacion | Commit |
| --- | --- | --- | --- | --- |
| 2026-05-24 | Agregar title al iframe de YouTube | `resource_detail.html` | Visual e inspección HTML | |
| 2026-05-24 | aria-controls y Tab key en dropdowns | `enhanced-select.js` | Test de navegación con teclado | |
| 2026-05-24 | aria-required="true" dinámico en forms | `apps/core/forms.py` | Test unitario automatizado | |
| 2026-05-24 | Estilos globales focus-visible | `estilos.css` | Inspección visual de foco | |
