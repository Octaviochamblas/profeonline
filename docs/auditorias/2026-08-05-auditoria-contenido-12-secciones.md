# Auditoría — contenido de 12 secciones migrado por Antigravity (nodos 02.04–03.15)

- **Fecha:** 2026-08-05
- **Autor:** 🏛️ Claude (auditoría solicitada por 🧑 Octavio sobre el trabajo de 🔨 Antigravity)
- **Alcance:** 913 recursos (`NodeContent`) de los 18 nodos migrados al estándar de 12 secciones
  el 2026-08-05: `02.04`, `02.05`, `02.06`, `03.01`–`03.15`. Ver cierre reportado en
  `reportes-sesion/2026-08-05.md` y `_coordinacion/ESTADO.md`.
- **Estado:** vigente
- **Datos completos:** [`2026-08-05-auditoria-contenido-12-secciones.json`](2026-08-05-auditoria-contenido-12-secciones.json)
  (913 `semantic_id` con el detalle de campos que fallan cada uno).

## Resumen

El cierre de sesión reportó "100% de cobertura" en los 18 nodos, verificado con scripts
`scratch/verify_XX.py` que **solo** comprueban `estado='publicado'` + `resumen_inicial` no
vacío. Esa verificación es real pero insuficiente: no valida los 12 campos obligatorios de
`docs/conocimiento/pauta-contenido.md`. Auditando contra la pauta completa:

- **913 / 913 recursos (100%) tienen al menos un campo obligatorio incompleto.**
- La causa está en el **YAML fuente** (`docs/conocimiento/contenido/*.yaml`), no en el loader
  ni en la migración: se verificó `load_node_content.py` (mapeo `data.get(...)` correcto) y un
  YAML de ejemplo (`aplicacion-de-la-regla-del-cuadrado-de-binomio-suma.yaml`) donde el campo
  simplemente no fue escrito.

| Campo obligatorio (pauta §"Campos obligatorios") | Requisito | Recursos que fallan |
| --- | --- | --- |
| `al_terminar_debes_poder` | 1-2 frases, no vacío | **913 / 913 (100%)** |
| `afirmaciones_verdaderas` | mínimo 2 | **910 / 913 (99,7%)** — 910 tienen exactamente 1 |
| `errores_frecuentes` | exactamente 5 | **545 / 913 (60%)** — mezcla de 1 a 4 |
| `ejemplos` | mínimo 4 (2 Tipo A + 2 Tipo B) | **215 / 913 (24%)** — 206 de esos tienen solo 1 |
| `checkpoints` | exactamente 2 | 0 fallas — este campo está correcto en el 100% |
| `ejemplo_guiado` | "Un solo problema resuelto paso a paso" (pauta) | **775 / 913 (85%) — ver hallazgo abajo, es genérico sin problema concreto** |

## Hallazgo añadido 2026-08-05 (tarde) — `ejemplo_guiado` genérico, corroborado a pedido de 🧑 Octavio

`ejemplo_guiado` pasó la auditoría estructural inicial (siempre tiene `enunciado` + 4 `pasos`, sin
duplicados exactos), pero una lectura de contenido revela que en la mayoría de los recursos **no
es un problema resuelto**: es una plantilla fija por sub-tema donde el nombre del propio recurso
se pega dentro de una frase molde, sin números ni expresión concreta que resolver. Ejemplo real
(`03.07 MAT.ALG.MCD_ALGEBRAICO.CONCEPTO_MCD`):

> enunciado: *"Simplifica o resuelve la expresión aplicando **concepto de m.c.d. algebraico**."*
> pasos: "Factorizar los numeradores y denominadores involucrados." / "Identificar
> restricciones del dominio…" / "Aplicar la regla o procedimiento correspondiente a **concepto
> de m.c.d. algebraico**." / "Simplificar los factores comunes…"

Los mismos 4 pasos molde se repiten (con el nombre del recurso insertado) en decenas de recursos
del mismo sub-tema — no hay un enunciado con datos propios que resolver.

**Detección:** proxy automático = `enunciado` sin ningún dígito (∴ sin datos numéricos concretos).
Verificado manualmente con muestras de 8 nodos distintos: el proxy coincide 100% con la lectura
manual — todos los casos sin dígito son plantilla vacía; el único caso con dígitos revisado
(`02.05 MAT.NUM.RAZONES.DEFINICION_COCIENTE`, "15 hombres y 20 mujeres…") sí es un problema real.

| Nodo | Recursos | `ejemplo_guiado` genérico (sin problema concreto) |
| --- | --- | --- |
| `02.04` | 93 | **0 (0%)** — único nodo limpio |
| `02.05` | 84 | 66 (78%) |
| `02.06` | 38 | 38 (100%) |
| `03.01` | 34 | 34 (100%) |
| `03.02` | 36 | 36 (100%) |
| `03.03` | 30 | 30 (100%) |
| `03.04` | 28 | 28 (100%) |
| `03.05` | 32 | 32 (100%) |
| `03.06` | 39 | 39 (100%) |
| `03.07` | 48 | 48 (100%) |
| `03.08` | 53 | 45 (84%) |
| `03.09` | 65 | 65 (100%) |
| `03.10` | 82 | 82 (100%) |
| `03.11` | 41 | 32 (78%) |
| `03.12` | 47 | 46 (97%) |
| `03.13` | 54 | 54 (100%) |
| `03.14` | 50 | 42 (84%) |
| `03.15` | 59 | 58 (98%) |
| **Total** | **913** | **775 (85%)** |

Este es, junto con `al_terminar_debes_poder`, el hallazgo más severo de la auditoría: el
`ejemplo_guiado` es la única sección pensada como "un modelo resuelto paso a paso" y en el 85%
de los casos no cumple su función pedagógica — no hay nada que el alumno pueda seguir como
modelo de resolución.

## Detalle por nodo

| Nodo | Nombre | Recursos | `al_terminar_debes_poder` vacío | `afirmaciones_verdaderas` < 2 | `errores_frecuentes` ≠ 5 | `ejemplos` < 4 |
| --- | --- | --- | --- | --- | --- | --- |
| `02.04` | Reales, Potencias, Raíces y Logaritmos | 93 | 93 | 90 | 93 | 93 |
| `02.05` | Razones, Proporciones, Porcentajes y Finanzas | 84 | 84 | 84 | 84 | 84 |
| `02.06` | Sucesiones y Progresiones | 38 | 38 | 38 | 38 | 38 |
| `03.01` | Nomenclatura y Conceptos Algebraicos | 34 | 34 | 34 | 0 | 0 |
| `03.02` | Lenguaje Algebraico y Valorización | 36 | 36 | 36 | 0 | 0 |
| `03.03` | Operaciones Algebraicas | 30 | 30 | 30 | 0 | 0 |
| `03.04` | Multiplicación Algebraica | 28 | 28 | 28 | 0 | 0 |
| `03.05` | Productos Notables | 32 | 32 | 32 | 0 | 0 |
| `03.06` | Factorización | 39 | 39 | 39 | 0 | 0 |
| `03.07` | MCD, MCM y Fracciones Algebraicas | 48 | 48 | 48 | 0 | 0 |
| `03.08` | Ecuaciones de Primer Grado y Sistemas | 53 | 53 | 53 | 0 | 0 |
| `03.09` | Desigualdades e Inecuaciones | 65 | 65 | 65 | 0 | 0 |
| `03.10` | Funciones | 82 | 82 | 82 | 79 | 0 |
| `03.11` | Ecuaciones de Segundo Grado | 41 | 41 | 41 | 41 | 0 |
| `03.12` | Función Cuadrática | 47 | 47 | 47 | 47 | 0 |
| `03.13` | Funciones Exponencial y Logarítmica | 54 | 54 | 54 | 54 | 0 |
| `03.14` | Función Potencia | 50 | 50 | 50 | 50 | 0 |
| `03.15` | Función Trigonométrica | 59 | 59 | 59 | 59 | 0 |

**Patrón observado:**
- `al_terminar_debes_poder` falta en el 100% de los 18 nodos sin excepción — parece un campo
  omitido sistemáticamente en la plantilla/prompt de generación usado por Antigravity.
- `afirmaciones_verdaderas` insuficiente en casi todos los nodos (solo 3 recursos de `02.04`
  tienen las 2 requeridas).
- `errores_frecuentes` incorrecto **solo** en `02.04`–`02.06` y `03.10`–`03.15` (números y
  funciones); los 9 nodos de álgebra base `03.01`–`03.09` sí tienen las 5 requeridas en el 100%
  de sus recursos.
- `ejemplos` insuficiente **solo** en `02.04`–`02.06` (números); ningún nodo de álgebra
  (`03.01`–`03.15`) tiene esta falla. La mayoría de esos 215 casos tiene solo 1 ejemplo en vez
  de 4.

Esto sugiere que la campaña se hizo en tandas y la calidad varió por tanda, no que sea un fallo
aleatorio uniforme — útil para priorizar la remediación (los nodos de números, `02.04`–`02.06`,
son los que acumulan las 4 fallas a la vez).

## Consecuencia funcional

Con `afirmaciones_verdaderas` en 1 (en vez de ≥2), la sección "Ejemplos Verdadero/Falso" de
`apps/learn/views.py::_true_false_items` tiene muy poca variedad real (solo 1 afirmación
verdadera para mezclar con las 5 falsas), aunque ya no da "Falso" siempre gracias al fix del
2026-08-04. No se detectó impacto en `checkpoints` (íntegros en el 100% de los casos).

## Fuera de alcance de esta auditoría

No se evaluó la **calidad pedagógica** del texto presente en los campos que sí están
completos (si `explicacion_formal`, `explicacion_simple`, etc. suenan a plantilla o están bien
anclados al contenido real de cada recurso, como se hizo manualmente en
`2026-06-21-lenguaje-algebraico-preguntas.md`). Esta auditoría es puramente estructural
(presencia/conteo de campos obligatorios), no de contenido.

## Metodología

Script `scratch/audit_antigravity_12secciones.py` (no versionado, gitignored) recorre los 18
nodos → subtemas → recursos hoja vía ORM (`config.settings.local`), lee cada `NodeContent` y
compara contra los requisitos de la pauta. Sin llamadas a LLM ni lectura manual masiva —
auditoría 100% determinística sobre datos ya cargados en la base local.

## Recomendación (orden de prioridad)

Cada hallazgo aquí es P1 (bloquea la calidad pedagógica prometida, no la disponibilidad del
sitio). Todos requieren **reescritura de contenido**, no un script — son huecos de redacción,
no de datos. Orden sugerido:

1. **`ejemplo_guiado` genérico (775 recursos, 85%) — máxima prioridad.** Es la sección que el
   alumno usa como modelo de resolución; en el 85% de los casos no resuelve nada. Requiere
   redactar un problema concreto (con datos propios, no el nombre del recurso) y resolverlo en
   3-4 pasos reales, por recurso — no es automatizable con una plantilla porque **la plantilla es
   justamente el problema**.
2. **`al_terminar_debes_poder` vacío (913, 100%)** — es la más barata de resolver (1-2 frases por
   recurso, sin necesitar ejemplos numéricos) y desbloquea la meta de aprendizaje visible en el
   cierre de cada recurso. Buen punto de partida antes del punto 1.
3. **`afirmaciones_verdaderas` insuficiente (910, 99,7%)** — falta 1 afirmación cierta adicional
   por recurso para completar el mínimo de 2; impacta directamente la variedad de la sección
   "Ejemplos Verdadero/Falso".
4. **`errores_frecuentes` incompleto (545, 60%)** — acotado a `02.04`–`02.06` y `03.10`–`03.15`;
   completar hasta 5 por recurso.
5. **`ejemplos` insuficiente (215, 24%)** — acotado a `02.04`–`02.06`; la mayoría solo tiene 1 de
   los 4 requeridos (2 Tipo A + 2 Tipo B).

**Por nodo:** `02.04`–`02.06` acumulan las 5 fallas a la vez (son los peores); `03.01`–`03.09`
solo tienen 3 fallas (`ejemplo_guiado`, `al_terminar_debes_poder`, `afirmaciones_verdaderas`) —
podrían remediarse más rápido. Sugerido crear una tarjeta en `backlog/1-por-iniciar/` por nodo o
por tanda de nodos, priorizando `02.04`–`02.06`. No se creó la tarjeta en esta sesión — pendiente
de decisión de 🧑 Octavio sobre quién la ejecuta.
