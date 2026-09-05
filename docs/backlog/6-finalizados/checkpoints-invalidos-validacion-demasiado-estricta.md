# Checkpoints inválidos: la validación exige el texto literal de la alternativa correcta

- **Estado:** ✅ Cerrado (2026-09-05, 🏛️ Claude)
- **Creado:** 2026-09-05
- **Prioridad:** P1  ·  **Cartera:** educativa
- **Tipo:** infraestructura + pedagogía
- **Dueño sugerido:** 🏛️ Claude (fix del validador + loader) · 🔨 Antigravity (repaso de los 15 YAML)

## Objetivo (una frase)
`load_node_content` **salta el archivo completo** (12 secciones, no solo los checkpoints)
cuando la validación de checkpoints falla con *"la explicación debe mencionar la
alternativa correcta"*. Hoy son **15 nodos** cuyas páginas de `/aprender/` quedan con el
fallback genérico aunque su `semantic_id` esté bien.

## Contexto / causa raíz
`apps/content/services/node_checkpoint_service.py:66`:
```python
if correct_text.casefold() not in explanation.casefold():
    raise ValueError(f"Comprobación {index}: la explicación debe mencionar la alternativa correcta.")
```
Es un **substring literal** del texto COMPLETO de la alternativa (con delimitadores KaTeX,
paréntesis, sufijos y todo) dentro de la `explanation`. El contenido **no está mal
pedagógicamente** — todas las explicaciones sí derivan/citan la respuesta — pero el match
literal se rompe por:

| Sub-causa | Ejemplo | `correct_text` | `explanation` |
| --- | --- | --- | --- |
| Delimitadores `$` alrededor de toda la expresión, no del valor | `calculo-del-cambio-absoluto.yaml` | `$-7^\circ\text{C}$` | `$\Delta T = 18 - 25 = -7^\circ\text{C}$.` |
| Cita truncada (falta el `$` de cierre) | `definicion-de-sucesion-numerica-...yaml` | `...\{1, 2, 3, \dots\}$` | `...La alternativa correcta es '...\{1, 2, 3, \dots\}'.` |
| Cita parcial (se omite el sufijo entre paréntesis) | `calculo-de-reparto-proporcional-directo.yaml` | `$k = \frac{T}{\sum c_i}$ (Total dividido por la suma de los índices)` | `La alternativa correcta es '$k = \frac{T}{\sum c_i}$'.` |

Efecto en el loader (`apps/content/management/commands/load_node_content.py:65-66`):
```python
except ValueError as exc:
    self.stderr.write(f"{path.name}: checkpoints inválidos — {exc}")
    continue   # <-- salta TODO el NodeContent, no solo los checkpoints
```

El mismo check literal está duplicado en
`apps/content/services/reading_checkpoint_service.py:77` (checkpoints de lectura de
`Resource`).

## Los 15 archivos (a 2026-09-05)
`aplicacion-del-impuesto-al-valor-agregado`, `calculo-de-porcentaje-de-un-porcentaje`,
`calculo-de-reparto-proporcional-directo`, `calculo-del-c-de-una-cantidad`,
`calculo-del-cambio-absoluto`, `calculo-del-cambio-relativo`,
`calculo-del-valor-final-con-aumento-porcentual`,
`calculo-del-valor-final-con-descuento-porcentual`,
`calculo-del-valor-final-por-porcentajes-sucesivos`, `concepto-de-aumento-porcentual`,
`concepto-de-descuento-porcentual`, `concepto-de-disminucion-porcentual`,
`concepto-de-porcentaje-como-razon-de-denominador-100`,
`definicion-de-sucesion-numerica-como-lista-ordenada-de-terminos`,
`representacion-grafica-de-porcentajes` — todos `.yaml` en `docs/conocimiento/contenido/`.

> 5 de estos (`aplicacion-del-impuesto-...`, `calculo-de-porcentaje-de-un-porcentaje`,
> `calculo-de-reparto-proporcional-directo`, `calculo-del-c-de-una-cantidad`,
> `representacion-grafica-de-porcentajes`) también estaban en el frente
> `reparar-desfase-semantic-id-contenido` (ya cerrado): tienen el `semantic_id` correcto
> pero **siguen sin cargar** por este bug. El resto ya tenía `semantic_id` bueno y este
> es el único bloqueo.

## Fuentes a leer (rutas concretas)
- `apps/content/services/node_checkpoint_service.py` (líneas ~46-69).
- `apps/content/services/reading_checkpoint_service.py` (línea ~77, mismo check).
- `apps/content/management/commands/load_node_content.py` (líneas ~61-67, el `continue`).
- `apps/content/tests/test_node_checkpoint_service.py:77` (test que fija el comportamiento estricto).

## Propuesta
1. **Relajar el check** en `node_checkpoint_service`: normalizar ambos lados antes del `in`
   — quitar `$`, colapsar espacios, y comparar contra el **núcleo** de la alternativa (p.ej.
   quitar sufijos entre paréntesis y quedarse con la parte matemática/clave). Alternativa
   mínima: exigir solo que el texto de la alternativa **sin delimitadores `$` ni
   paréntesis finales** aparezca en la explicación igualmente normalizada. Extraer un
   helper compartido y usarlo también en `reading_checkpoint_service`.
2. **El loader no debe tirar las 12 secciones por un checkpoint malo**: cargar el
   `NodeContent` con `checkpoints = []` (o los válidos) y dejar el `stderr.write` como
   warning, en vez de `continue`.
3. Ajustar `test_node_checkpoint_service.py` al nuevo criterio + test de regresión con un
   caso KaTeX real (`$-7^\circ\text{C}$` dentro de un bloque `$...$` mayor).
4. Repaso rápido de los 15 YAML: si alguna `explanation` de verdad **no** menciona la
   respuesta (no es el caso en la muestra revisada, pero confirmar los 15), corregir la
   redacción.
5. `import_knowledge_tree && load_node_content` local → `checkpoints inválidos: 0`.

## No-objetivos (qué queda FUERA)
- Rediseñar el formato de checkpoints o su UI.
- Tocar el resto de validaciones de `normalize_node_checkpoints` (placement, 4 alternativas,
  1 correcta, no duplicados) — esas están bien.

## Criterios de aceptación (verificables)
- [ ] Barrera verde: `test` · `check` · `makemigrations --check --dry-run`
- [ ] `python manage.py load_node_content` → **0** líneas `checkpoints inválidos`
- [ ] Un checkpoint cuya explicación referencia la respuesta con notación KaTeX distinta
      (delimitadores, sufijo entre paréntesis) **pasa** la validación
- [ ] Un checkpoint cuya explicación de verdad no menciona la respuesta **sigue fallando**
- [ ] El loader carga el `NodeContent` aunque un checkpoint sea inválido (con warning)
- [ ] Las 15 páginas de `/aprender/` afectadas muestran contenido de 12 secciones en prod

## Plan de pruebas
- Unit: `test_node_checkpoint_service` con casos KaTeX (pasa) y explicación vacía de
  respuesta (falla).
- `load_node_content` local antes/después (15 → 0).
- Suite completa antes de pushear.
- Smoke en prod tras el deploy.

## Riesgos / rollback
- **Riesgo:** aflojar demasiado el check y dejar pasar checkpoints cuya explicación no
  ayuda. Mitiga: comparar contra el núcleo de la alternativa (no string vacío), mantener
  el caso negativo en tests.
- **Rollback:** `git revert`; nada toca esquema ni datos, solo lógica de validación y
  YAML de contenido.

---

## Qué se hizo (2026-09-05)
- **Helper compartido** `apps/content/services/checkpoint_matching.py` —
  `explanation_mentions_answer(correct_text, explanation)`:
  - Si la alternativa trae spans `$...$`: cada span (sin ruido KaTeX: `$ {} \` y
    espacios) debe aparecer en la explicación normalizada. Cubre delimitadores
    distintos (`$1,25$` vs `... = 1,25$.`), prosa envolviendo la fórmula
    (`Dividir el valor final por $1,15$` vs `$V_i = V_f/1,15$`) y `\$` (peso
    dentro de KaTeX).
  - Si no trae `$`: substring de la cadena normalizada completa, conservando el
    paréntesis final si **es** toda la respuesta (par ordenado `(0, 7)`).
- `node_checkpoint_service.py` y `reading_checkpoint_service.py` usan el helper en
  vez del `correct_text.casefold() not in explanation.casefold()`.
- `load_node_content.py`: un checkpoint inválido ya **no descarta el NodeContent
  entero** — carga con `checkpoints = []` y deja el warning.
- Tests: 4 casos nuevos en `test_node_checkpoint_service.py` (KaTeX distinto,
  gloss entre paréntesis, par ordenado, prosa + span). `test_reading_checkpoints`
  sigue verde.
- **Verificado:** `load_node_content` → **0** `checkpoints inválidos` (antes 15
  saltaban el archivo completo; `Actualizados: 1917`). Suite completa OK.
- **No hizo falta** editar ningún YAML de contenido: todas las explicaciones sí
  referenciaban la respuesta, era el validador el estricto.
