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
_(Completar al finalizar, antes de mover a "3 Finalizados".)_
