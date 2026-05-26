# Mejora visual de tarjetas de navegacion

Fecha de creacion: 2026-05-26
Estado: propuesta de mejora visual pendiente de implementacion
Superficie principal: `templates/pages/home.html`

## Diagnostico

Las tarjetas actuales se ven poco trabajadas por tres razones:

- En desktop ocupan todo el ancho disponible, lo que deja demasiado espacio vacio.
- No tienen iconos, senales visuales ni una accion secundaria clara.
- Solo el titulo es clickeable, aunque visualmente toda la tarjeta parece una unidad interactiva.

La causa tecnica principal esta en `static/css/estilos.css`: `.card-grid` solo define `display: grid` y `gap`, pero no columnas. En `templates/pages/home.html`, las tarjetas son `<article class="content-card">` con un `<a>` solo dentro del `h3`.

## Sugerencia visual

Convertir estas tarjetas en accesos compactos tipo "action cards":

```text
+------------------------------------------------+
| [icono] Recursos                         ->    |
|         Guias, ejercicios y materiales...       |
|         Ver recursos                            |
+------------------------------------------------+
```

En desktop:

- Usar 3 columnas para "Empieza por aqui", areas, asignaturas y niveles destacados cuando haya 3 elementos.
- Mantener tarjetas compactas, con altura estable pero no exagerada.
- Usar icono a la izquierda, contenido al centro y flecha/CTA a la derecha.
- Hacer que toda la tarjeta sea un enlace.

En mobile:

- Mantener una columna.
- Conservar el icono, titulo, descripcion y flecha.
- Evitar textos largos que empujen demasiado la altura.

## Direccion recomendada

Crear una variante nueva para home, sin romper otras pantallas que ya usan `.content-card`:

- `.home-card-grid`
- `.home-link-card`
- `.home-link-card__icon`
- `.home-link-card__body`
- `.home-link-card__title`
- `.home-link-card__text`
- `.home-link-card__cta`

No conviene modificar `.content-card` globalmente como primer paso, porque se usa en listados, detalles, modulos, temas, niveles y recursos. Cambiarla globalmente podria alterar superficies administrativas y listados que tienen acciones secundarias.

## Acciones a tomar

1. Actualizar la seccion "Empieza por aqui" en `templates/pages/home.html`.
   - Cambiar cada `<article class="content-card">` por un `<a class="home-link-card">`.
   - Hacer clickeable toda la tarjeta.
   - Mantener texto descriptivo breve.
   - Agregar icono visual con `aria-hidden="true"`.

2. Actualizar "Areas destacadas".
   - Cambiar cada tarjeta destacada por enlace completo hacia `content:subject_list` con filtro `area`.
   - Agregar iconos por categoria cuando sea posible:
     - Matematicas: calculadora, grafico o simbolo numerico.
     - Ciencias: atomo, matraz o circulos conectados.
     - Lenguaje e idiomas: libro, globo o bocadillo de texto.
   - Si no hay mapeo exacto, usar un icono generico de area.

3. Actualizar "Asignaturas destacadas" y "Niveles destacados".
   - Usar la misma estructura visual para mantener consistencia.
   - Incluir metadatos cortos como chips, por ejemplo `Area: Ciencias` o `Nivel escolar`.
   - Evitar parrafos repetidos o demasiado largos.

4. Agregar estilos nuevos en `static/css/estilos.css`.
   - Desktop:
     - `grid-template-columns: repeat(3, minmax(0, 1fr));`
     - `gap: 0.875rem;`
   - Tablet:
     - `grid-template-columns: repeat(2, minmax(0, 1fr));`
   - Mobile:
     - `grid-template-columns: 1fr;`
   - Tarjeta:
     - `display: grid;`
     - `grid-template-columns: auto minmax(0, 1fr) auto;`
     - `align-items: start;`
     - `gap: 0.875rem;`
     - `padding: 1rem;`
     - `min-height: 120px;`
   - Hover/focus:
     - borde mas claro;
     - leve elevacion;
     - flecha desplazada 2px;
     - `:focus-visible` visible para teclado.

5. Resolver iconos sin dependencia nueva.
   - Opcion recomendada: inline SVG pequenos dentro del template o un partial reutilizable.
   - Alternativa: crear `static/img/icons.svg` como sprite y referenciar con `<svg><use ...></use></svg>`.
   - No usar emojis como iconos principales, porque se ven inconsistentes entre sistemas.

6. Ajustar accesibilidad.
   - La tarjeta completa debe ser un solo enlace.
   - No anidar enlaces dentro de enlaces.
   - El icono debe llevar `aria-hidden="true"` si es decorativo.
   - El texto visible debe explicar el destino: `Ver recursos`, `Explorar asignaturas`, `Ver niveles`.
   - El estado de foco debe ser evidente sin depender solo del color.

7. Validar visualmente.
   - Revisar home en desktop ancho, laptop, tablet y mobile.
   - Confirmar que no haya solapamiento de texto.
   - Confirmar que cada tarjeta completa sea clickeable.
   - Probar navegacion con Tab.
   - Confirmar que el orden visual coincide con el orden de tabulacion.

## Ejemplo de markup recomendado

```django
<a class="home-link-card home-link-card--resources" href="{% url 'content:resource_list' %}">
    <span class="home-link-card__icon" aria-hidden="true">
        <!-- icono SVG -->
    </span>
    <span class="home-link-card__body">
        <span class="home-link-card__title">Recursos</span>
        <span class="home-link-card__text">Guias, ejercicios y materiales para estudiar con orden.</span>
        <span class="home-link-card__cta">Ver recursos</span>
    </span>
    <span class="home-link-card__arrow" aria-hidden="true">-&gt;</span>
</a>
```

## Ejemplo de CSS base

```css
.home-card-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.875rem;
    margin-top: 1rem;
}

.home-link-card {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr) auto;
    gap: 0.875rem;
    align-items: start;
    min-height: 120px;
    padding: 1rem;
    color: var(--text);
    text-decoration: none;
    background: var(--surface-soft);
    border: 1px solid var(--border);
    border-radius: 12px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

.home-link-card:hover,
.home-link-card:focus-visible {
    border-color: var(--primary);
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.45);
}

.home-link-card__icon {
    display: grid;
    place-items: center;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 10px;
    background: rgba(250, 204, 21, 0.12);
    color: var(--primary);
}

.home-link-card__body {
    display: grid;
    gap: 0.35rem;
}

.home-link-card__title {
    color: var(--primary);
    font-weight: 800;
    font-size: 1.1rem;
}

.home-link-card__text {
    color: var(--muted);
    line-height: 1.45;
}

.home-link-card__cta {
    font-weight: 700;
}

.home-link-card__arrow {
    color: var(--primary);
    font-weight: 800;
    transition: transform 0.2s ease;
}

.home-link-card:hover .home-link-card__arrow,
.home-link-card:focus-visible .home-link-card__arrow {
    transform: translateX(2px);
}

@media (max-width: 900px) {
    .home-card-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 640px) {
    .home-card-grid {
        grid-template-columns: 1fr;
    }
}
```

## Criterios de aceptacion

- La home no muestra tarjetas gigantes de ancho completo cuando hay 3 elementos.
- Todas las tarjetas de navegacion destacada son clickeables completas.
- Cada tarjeta tiene icono, titulo, descripcion breve y CTA/flecha.
- El foco de teclado es visible.
- La solucion no rompe tarjetas administrativas con acciones de editar/eliminar.
- `python manage.py test` sigue pasando.
- La revision visual en desktop y mobile se ve mas densa, clara y profesional.
