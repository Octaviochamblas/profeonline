# Hacer visible la ejercitación, evaluación y progreso (recurso, tema y tarjetas de tema)

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** Producto pedagógico / UX / Frontend
- **Origen:** mejora sobre el MVP de evaluación gamificada (Fases 1–9 ya en `3 Finalizados/`).
- **Prioridad:** Media-alta (el contenido ya existe pero el alumno no lo descubre).

## Problema / Objetivo

Los ejercicios ya existen (`Question` por recurso, nivel 1/2/3 y modo `preparacion`/
`evaluacion`/`ambas`, renderizados en `quiz_section.html`, generados por IA como borrador), pero
están **poco visibles**. El alumno no entiende de inmediato dónde **practicar**, dónde
**evaluarse**, ni qué significa **"comprendido"** (auto-reporte) vs **"aprobado"** (evidencia por
evaluación). Además, las **tarjetas de tema** (`home-link-card`) no muestran ningún progreso
(ver captura: hueco al pie de cada tarjeta), así que el alumno no sabe cuánto lleva de cada tema.

Objetivo: que en una mirada el alumno entienda qué hacer en cada recurso y cuánto domina cada
tema, sin inflar la cantidad de estados ni romper la barrera de CI.

## Diagnóstico aterrizado al código

- **Estados/señales actuales:** `get_resource_progress_map` devuelve
  `{resource_id: {viewed, max_level, stars}}` con **`stars = max_level`** (nivel más alto
  aprobado, tope 3) — ver `apps/content/selectors/evaluation_selectors.py:50`. **No** es suma de
  estrellas.
- **Agregación por tema ya existe:** un selector en
  `apps/content/selectors/evaluation_selectors.py:59` ya devuelve
  `recursos_total / vistos / aprobados / estrellas_total`. **Reusar/extender esto**, no inventar
  fórmulas en el template.
- **Niveles variables:** `Resource.levels` es M2M; **no todos los recursos tienen los 3 niveles**.
- **Examen de tema:** ya existe "Tema dominado · N%" con brillo (Fase 7) en `topic_detail`.
- **Tarjetas de tema duplicadas en 3 templates:** `templates/pages/topic_list.html` (~l.103),
  `templates/pages/area_detail.html` (~l.49/83), `templates/pages/subject_detail.html` (~l.63),
  todas con `home-link-card`. Cualquier cambio debe cubrir las 3 → conviene extraer un
  **partial** (`templates/pages/_topic_card.html`) e incluirlo en las tres.
- **Tests acoplados a copy:** `apps/content/tests/test_completion.py` afirma literalmente
  `"Completado"` y `"1 de 1 completados"` → el renombrado **romperá la suite** (la barrera real de
  CI) si no se actualizan en el mismo PR.
- **Borradores IA:** confirmado en auditoría — las evaluaciones compilan solo `status="publicada"`
  (`evaluation_service.py:42` y `:268`), así que los borradores nunca llegan al alumno. Esto es
  **regresión a proteger**, no funcionalidad nueva.

---

## Decisiones cerradas (sin ambigüedad)

1. **Vocabulario único — se migra, no se duplica.** Todo "completado/Completado" pasa a
   "comprendido/Comprendido", **incluido** el texto legacy "N de M completados" → **"N de M
   comprendidos"**. Se actualizan las aserciones de `apps/content/tests/test_completion.py`
   (`"Completado"`, `"1 de 1 completados"`) en el mismo PR. No conviven dos vocabularios.

2. **Jerarquía de señales (qué se muestra y dónde).** Cuatro señales con prioridad fija:
   - **Visto** (amarillo): abrió el recurso. La más débil.
   - **Comprendido** (neutro/azul): auto-reporte (`ResourceCompletion`). **Sin XP.**
   - **Aprobado / estrellas ★** (verde): evidencia por evaluación. **Señal dominante** donde hay
     preguntas publicadas.
   - **Tema dominado · N%** (verde con brillo): examen final aprobado (Fase 7). Señal superior.

   Reparto exacto por superficie:
   - **Tarjetas de tema** (`home-link-card`, los 3 listados): **SOLO** el **% comprendido** +
     texto "N/M comprendidos". Nada más, para no recargar la tarjeta. El badge "Tema dominado"
     **NO** va aquí.
   - **`topic_detail`**: barra pedagógica completa donde **aprobado/estrellas es lo visualmente
     dominante**; "comprendidos" como línea secundaria; "Tema dominado · N%" arriba si aplica.
   - **Tarjetas de recurso dentro del tema**: las 3 señales chicas (Visto / Comprendido / ★),
     siempre con texto+ícono (no solo color).

3. **"Comprendido" se conserva, con rol acotado.** Es señal débil (auto-reporte), pero es el
   **único progreso posible en recursos sin preguntas publicadas** → se mantiene. Donde hay
   evaluación, "aprobado/estrellas" manda visualmente y "comprendido" queda subordinado. Nunca
   otorga XP (evita farmeo del toggle).

---

## Propuesta por fases

### Fase A — Barra de acciones en el recurso + renombrado de lenguaje

- Al final del contenido del recurso (justo después del contenido principal, **antes** de la
  navegación anterior/siguiente), una barra clara de 3 acciones:
  - **Izquierda: Ejercitación** → ancla/scroll a la zona de práctica.
  - **Centro: Evaluación** → ancla/scroll a la zona de evaluación.
  - **Derecha: Marcar como comprendido** → reutiliza `ResourceCompletion` (crear/eliminar), solo
    cambia el lenguaje visible.
- **Verificar que ambas zonas existan en el DOM** al hacer scroll. Si `quiz_section` se carga por
  HTMX bajo demanda, el botón debe disparar la carga **y luego** hacer scroll (no anclar a vacío).
- Renombrado de copy (todo en el mismo PR que actualiza los tests):
  - "Marcar como completado" → **Marcar como comprendido**
  - "Completado" → **Comprendido**
  - "Demuestra lo aprendido" → **Ejercitación y evaluación**
- **`Comprendido` NO otorga XP** (es auto-reporte togglable; daría farmeo de un clic). Mantener el
  XP solo en práctica/aprobación reales (Fase 8 ya lo hace).

### Fase B — `quiz_section.html` más legible

- Cada nivel rotulado por su intención: **"Nivel 1: Conceptos"**, **"Nivel 2: Ejercicios
  simples"**, **"Nivel 3: Problemas de aplicación"**.
- Separar visualmente **Practicar** (preparación) de **Rendir evaluación** dentro de cada nivel.
- Estado vacío por nivel: **"Aún no hay ejercicios publicados para este nivel"**.
- **Hint solo-staff** (si `user.is_staff` y hay borradores sin publicar): "Hay N preguntas en
  borrador; publícalas para que aparezcan en ejercitación/evaluación" — cierra el lazo con la
  generación IA de la Fase 9.

### Fase C — Barra de progreso en las tarjetas de TODOS los temas  ⟵ (lo pedido en la captura)

- En `home-link-card` de cada tema, agregar al pie una **barra delgada de progreso** con el
  **% comprendido** del tema: `comprendidos / recursos_total * 100`.
- Texto compacto bajo la barra: **"N/M comprendidos"**.
- **Plomería de datos (clave):** crear un selector batch
  `get_topics_progress_map(user, topic_ids)` y anotarlo en las 3 vistas que listan temas
  (`TopicListView`, `area_detail`, `subject_detail`) para **evitar N+1**. Reusar la agregación ya
  existente (`evaluation_selectors.py:59`) por tema.
- **Anónimos / sin progreso:** no romper; ocultar la barra o mostrarla en 0% sin estrellar la
  página.
- **Extraer partial** `_topic_card.html` e incluirlo en los 3 templates (DRY).
- **Accesibilidad:** la barra con `role="progressbar"`, `aria-valuenow/min/max` y **texto** (no
  solo color); contraste AA.
- **Decidido (ver Decisión 2):** la tarjeta de tema muestra **solo** el % comprendido. El badge
  "Tema dominado · N%" **no** va en las tarjetas; vive en `topic_detail` (Fase D).

### Fase D — Progreso pedagógico dentro de `topic_detail` + señales en tarjetas de recurso

- Reemplazar/complementar la barra actual de `topic_detail` (que mide solo "completados") por una
  mini barra con 3 lecturas:
  - **Comprendidos:** recursos marcados manualmente.
  - **Aprobados:** recursos con `max_level ≥ 1` (al menos nivel 1 aprobado).
  - **Estrellas (progreso):** estrellas acumuladas sobre el total **realmente alcanzable**.
- **Fórmula corregida (importante):** NO usar `total_recursos * 3`. El máximo de estrellas por
  recurso = nº de niveles **publicados** que ofrece ese recurso (puede ser 1, 2 o 3). Denominador
  = suma de esos máximos. **Guardar contra división por cero** (tema sin recursos / sin preguntas
  publicadas → 0% sin crash).
- Renombrar para evitar **colisión de "dominio"**: el examen ya usa "Tema **dominado**". Llamar a
  la barra de estrellas **"Progreso"** o **"Estrellas"**, no "Dominio".
- Texto compacto: **"2/5 comprendidos · 1/5 aprobados · 4/12 estrellas"** (el denominador de
  estrellas es el alcanzable, no `recursos*3`).
- En las tarjetas de recurso dentro del tema, hasta **3 señales pequeñas** con **texto+ícono**
  (no solo color): "Visto", "Comprendido", "★/★★/★★★".

---

## Correcciones críticas a no olvidar (resumen)

1. **Fórmula de estrellas:** denominador = niveles publicados por recurso, no `recursos*3`;
   guardar división por cero.
2. **Renombrado — archivos exactos:** el texto visible vive en
   `templates/includes/completion_button.html`, `templates/includes/resume_card.html` y
   `templates/pages/topic_detail.html` (NO en la vista ni en el modelo). Actualizar también las
   aserciones de `test_completion.py` (`"Completado"`, `"1 de 1 completados"`) en el mismo PR.
3. **No tocar el modelo:** prohibido cambiar `models/completion.py` / `verbose_name` → genera
   migración y rompe `makemigrations --check` en CI.
4. **DRY tarjetas de tema:** un solo partial `_topic_card.html` para los 3 templates.
5. **N+1:** selector batch `get_topics_progress_map`; en `topic_list` los temas van **agrupados**
   → juntar TODOS los `topic_ids` de todos los grupos en **una** llamada, no una por grupo.
6. **"Comprendido" no da XP.**
7. **Accesibilidad:** nada de color-only; barras con `role="progressbar"` +
   `aria-valuenow/min/max` + texto; señales con texto+ícono.
8. **Anclas reales:** asegurar que práctica/evaluación estén en el DOM antes del scroll.
9. **No mezclar conceptos:** Comprendido = auto-reporte; Aprobado = evidencia por evaluación.
10. **`check --deploy` necesita env vars** (`DJANGO_SECRET_KEY`, `DATABASE_URL`,
    `DJANGO_ALLOWED_HOSTS`…) o crashea con `ImproperlyConfigured`; setearlas como en
    `django_ci.yml` y usar `--fail-level ERROR --settings=config.settings.production`.

## Plan de pruebas

- "Marcar como comprendido" sigue creando/eliminando `ResourceCompletion`.
- "Ejercitación" y "Evaluación" llevan a la sección correcta (no a un ancla vacía).
- Recurso sin preguntas publicadas → estado vacío correcto por nivel.
- **Barra de tarjeta de tema:** % comprendido correcto; tema con 0 recursos → 0% sin crash;
  usuario anónimo → sin error.
- **Barra de `topic_detail`:** estrellas calculadas sobre el total alcanzable (recurso con <3
  niveles cuenta bien); división por cero protegida.
- Tarjetas de recurso muestran visto/comprendido/aprobado de forma independiente.
- **Regresión:** preguntas IA en borrador NO aparecen al alumno hasta publicarse.
- "Comprendido" **no** genera `XPEvent`.
- Navegación por teclado de la barra de acciones y de los enlaces de tarjeta (a11y).
- Sin N+1: el listado de temas no dispara una query por tarjeta (assert con
  `assertNumQueries`).

## Supuestos

- Navegación dentro de la misma página del recurso (ancla/scroll), sin página nueva.
- `ResourceCompletion` se conserva; solo cambia su lenguaje visible a "comprendido".
- "Aprobado" sigue dependiendo de las evaluaciones por nivel (`max_level ≥ 1`).
- La generación IA sigue siendo staff/admin, nunca visible para el alumno.
- A futuro, una página dedicada de "Banco de ejercitación" solo si la práctica crece mucho; por
  ahora todo vive dentro del recurso.

---

## Prompt para Antigravity (implementación)

> Pegar tal cual. Es autocontenido; no asume contexto de esta conversación.

```
Trabajas en el repo Django ProfeOnline (Windows, settings por defecto config.settings.local;
producción config.settings.production). Implementa la tarjeta
docs/2 En Proceso/visibilidad-ejercitacion-evaluacion-progreso.md COMPLETA. Léela primero de
arriba a abajo: respeta sin excepción las secciones "Decisiones cerradas" y "Correcciones
críticas". Todos los paths de abajo están verificados contra el código real: úsalos tal cual.

Reglas de proceso (obligatorias):
- Crea una rama propia: feat/visibilidad-ejercitacion-progreso. NO trabajes sobre main ni toques
  ramas de otros agentes. (La tarjeta ya está en docs/2 En Proceso/.)
- Implementa las 4 fases (A barra de acciones + renombrado; B quiz_section legible; C barra de
  % comprendido en las tarjetas de TODOS los temas; D progreso pedagógico en topic_detail +
  señales en tarjetas de recurso).

RENOMBRADO — archivos y textos EXACTOS (no buscar a ciegas):
- templates/includes/completion_button.html:
  "Completado" -> "Comprendido"
  "Marcar como completado" -> "Marcar como comprendido"
  "Lo marcaste como completado. Pulsa para desmarcar." -> "Lo marcaste como comprendido. Pulsa para desmarcar."
- templates/includes/resume_card.html:  "✓ Completado" -> "✓ Comprendido"
- templates/pages/topic_detail.html:
  "N de M completados" (el texto "{{ completed_count }} de {{ total_count }} completados") -> "... comprendidos"
  badge "✓ Completado" del listado de recursos -> "✓ Comprendido"
- apps/content/tests/test_completion.py: actualizar en el MISMO commit las aserciones
  assertContains(response, "Completado") y assertContains(response, "1 de 1 completados") al
  nuevo vocabulario.
- PROHIBIDO tocar apps/content/models/completion.py (incl. verbose_name del modelo): cambiarlo
  genera una migración y rompe `makemigrations --check` en CI. El texto visible NO vive ahí.
- La vista HTMX apps/content/views/resource_completion.py NO contiene texto: solo hace
  render_to_string("includes/completion_button.html"). No pongas strings ahí.

Detalles técnicos que NO puedes incumplir:
- Tarjetas de tema: extrae UN partial templates/pages/_topic_card.html e inclúyelo en
  templates/pages/topic_list.html, area_detail.html y subject_detail.html (hoy está duplicado en
  las 3 como .home-link-card).
- Crea un selector batch get_topics_progress_map(user, topic_ids) en
  apps/content/selectors/evaluation_selectors.py (reusa la agregación
  recursos_total/vistos/aprobados/estrellas_total ya presente ahí) y anótalo en get_context_data
  de las 3 vistas class-based: TopicListView (apps/content/views/topic_list.py),
  AreaDetailView (area_detail.py) y SubjectDetailView (subject_detail.py).
- OJO N+1 en topic_list: los temas vienen AGRUPADOS ({% for topic in group.topics %}). Junta
  TODOS los topic_ids de TODOS los grupos y haz UNA sola llamada a get_topics_progress_map; no
  una por grupo (eso reintroduce el N+1).
- % comprendido de la tarjeta = comprendidos / recursos_total * 100. Maneja anónimo y tema con 0
  recursos sin crashear (sin división por cero). Barra accesible OBLIGATORIA:
  role="progressbar", aria-valuenow, aria-valuemin="0", aria-valuemax="100" y texto visible
  "N de M comprendidos" (NUNCA solo color).
- Fórmula de estrellas en topic_detail: el máximo por recurso = nº de niveles PUBLICADOS de ese
  recurso (1, 2 o 3), NO recursos*3. Denominador = suma de esos máximos; guarda división por cero.
  Ojo: en el código, stars = max_level (ver evaluation_selectors.py).
- Jerarquía de señales (Decisión 2): en topic_detail "aprobado/estrellas" es la señal
  DOMINANTE en la cabecera; "comprendidos" va como línea secundaria; "Tema dominado · N%" arriba
  si el examen final está aprobado. En las tarjetas de tema va SOLO el % comprendido (sin badge
  de "Tema dominado"). En tarjetas de recurso, las 3 señales chicas (Visto/Comprendido/★) con
  texto+ícono, no solo color.
- "Marcar como comprendido" reutiliza ResourceCompletion y NO emite XPEvent (es togglable;
  daría farmeo). Barra de acciones del recurso en templates/pages/resource_detail.html, justo
  tras el contenido y antes de la navegación prev/next; incluye el partial
  includes/completion_button.html para el toggle.
- Si la zona de quiz se carga por HTMX, el botón "Ejercitación"/"Evaluación" dispara la carga y
  LUEGO hace scroll (no anclar a un nodo vacío).
- Las preguntas IA siguen naciendo status="borrador" y no aparecen al alumno; las evaluaciones
  solo compilan status="publicada". No cambies eso.
- En templates/includes/quiz_section.html: rotula niveles (Nivel 1: Conceptos / Nivel 2:
  Ejercicios simples / Nivel 3: Problemas de aplicación), separa Practicar vs Rendir evaluación,
  estado vacío "Aún no hay ejercicios publicados para este nivel", y hint solo-staff
  (user.is_staff y draft_questions_count > 0): "Hay N preguntas en borrador; publícalas para que
  aparezcan en ejercitación/evaluación".

Tests a agregar/actualizar en apps/content/tests/test_visibilidad.py (la suite es la barrera de CI):
- % comprendido correcto en tarjeta; tema con 0 recursos -> 0% sin crash; usuario anónimo sin error.
- assertNumQueries en el listado de temas para probar que NO hay N+1 (una sola query del mapa).
- estrellas en topic_detail con recurso de <3 niveles publicados; división por cero protegida.
- "comprendido" no crea XPEvent.
- regresión: preguntas en borrador no aparecen al alumno.
- test_completion.py actualizado al nuevo vocabulario ("Comprendido", "1 de 1 comprendidos").

Verificación antes de entregar (corre y deja TODO verde — es la barrera real de CI):
  .venv\Scripts\python.exe manage.py test
  .venv\Scripts\python.exe manage.py check
  .venv\Scripts\python.exe manage.py makemigrations --check --dry-run
El check --deploy con settings de producción REQUIERE env vars o crashea con
ImproperlyConfigured (Missing DJANGO_SECRET_KEY). Setealas igual que .github/workflows/
django_ci.yml antes de correrlo (PowerShell):
  $env:DJANGO_SECRET_KEY="ci-test-secret-key-must-be-long-and-secure-in-production-check"
  $env:DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,testserver"
  $env:DJANGO_CSRF_TRUSTED_ORIGINS="http://localhost,http://127.0.0.1,http://testserver"
  $env:DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS="true"; $env:DJANGO_SECURE_HSTS_PRELOAD="true"
  $env:DATABASE_URL="postgres://user:pass@localhost:5432/ci_dummy"
  .venv\Scripts\python.exe manage.py check --deploy --fail-level ERROR --settings=config.settings.production

Entrega:
- Completa la sección "Qué se hizo" de la tarjeta y muévela a docs/3 Finalizados/ con `git mv`.
- Abre un PR contra main con resumen por fase y resultado de los tests. NO hagas squash-merge:
  deja el PR abierto para auditoría. Indica el número de PR y la rama.
```

---

## Qué se hizo

### Fase A — Barra de acciones en el recurso + renombrado de lenguaje
- Se renombró "Completado" a "Comprendido" de manera global en todos los templates visibles al usuario (`completion_button.html`, `resume_card.html`, `topic_detail.html`).
- Se actualizaron las aserciones de `apps/content/tests/test_completion.py` para usar el nuevo vocabulario.
- Se implementó la barra de 3 acciones (Ejercitación, Evaluación, Marcar como comprendido) en `templates/pages/resource_detail.html`.
- Se aseguró que `ResourceCompletion` no otorga XP.

### Fase B — `quiz_section.html` más legible
- Se rotularon las cabeceras de los niveles: Nivel 1: Conceptos, Nivel 2: Ejercicios simples, Nivel 3: Problemas de aplicación.
- Se separaron visualmente los modos "Practicar" y "Evaluación".
- Se implementó un estado vacío claro ("Aún no hay ejercicios publicados para este nivel").
- Se agregó el hint para staff cuando hay preguntas en borrador.

### Fase C — Barra de progreso en las tarjetas de TODOS los temas
- Se extrajo el partial `templates/pages/_topic_card.html` unificando la maquetación duplicada en `topic_list.html`, `area_detail.html` y `subject_detail.html`.
- Se integró la barra de progreso de comprensión (`% comprendido`) en el partial de la tarjeta del tema.
- Se implementó el selector en lote `get_topics_progress_map(user, topic_ids)` en `evaluation_selectors.py` para prevenir consultas N+1.
- Se agregó accesibilidad (role="progressbar", aria-valuenow/min/max y texto descriptivo).

### Fase D — Progreso pedagógico dentro de `topic_detail`
- Se rediseñó el panel de progreso en `topic_detail.html` para incorporar 3 barras de progreso: Estrellas (como la señal dominante), Aprobados y Comprendidos.
- Se corrigió la fórmula para el denominador de las estrellas: ahora es la suma del número de niveles publicados por recurso, no `recursos * 3`.
- Se implementó la visualización de la barra con porcentaje y texto compacto exacto: `N/M comprendidos · A/B aprobados · S/T estrellas`.
- Se agregaron las 3 señales independientes con texto+ícono en las tarjetas de recursos dentro del tema.

### Pruebas y Verificación
- Se creó una suite de pruebas completa en `apps/content/tests/test_visibilidad.py` cubriendo la lógica de porcentajes en tarjetas, N+1 query safety (`assertNumQueries`), cálculo de denominador de estrellas, prevención de XP para "comprendidos" y regresión de borradores IA.
- Se ejecutó exitosamente el comando `check --deploy` simulando el entorno de producción con variables de entorno mockeadas.
