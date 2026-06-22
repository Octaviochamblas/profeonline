# Guías interactivas — Fase 4: respuesta directa (parser numérico/algebraico)

- **Estado:** 🟢 Ready para construir (handoff de arquitectura) · ⚠️ `seguridad:requiere-claude`
- **Creado:** 2026-06-22 · **Epic padre:** `1-por-iniciar/guias-interactivas-banco-estandarizado-items.md`
- **Prioridad:** P1 · **Cartera:** educativa · **Tipo:** producto · **seguridad**
- **Dueño:** 🧩 Codex (preflight) → 🔨 Antigravity (construye, rama `feat/guias-fase4-parser`) → 🧩 Codex (audita) → 🏛️ Claude (cierre, **revisa seguridad del parser**)

> **Alcance: SOLO el motor de corrección de respuesta directa + su integración en la práctica del
> banco visible (Fase 3).** Las evaluaciones por nivel/final que lo consumen son Fase 5. La entrada
> es del alumno → superficie de seguridad: AST restringido + SymPy, **nunca `eval`**.

## Objetivo (una frase)
Corregir respuestas escritas por el alumno comparándolas con la respuesta canónica del ítem:
**numéricas** (enteros, decimales con coma o punto, fracciones, con tolerancia) y **algebraicas**
(expresiones polinómicas o racionales equivalentes), mediante un parser restringido y seguro.

## Fuentes a leer
- `apps/content/models/question.py` — campos Fase 0: `question_type` (`alternativa`/`numérica`/
  `algebraica`), `canonical_answer` (TextField), `answer_tolerance` (FloatField), `points`.
- `apps/content/models/evaluation.py` — `QuizAttemptAnswer.text_answer` (ya existe) para guardar lo
  ingresado.
- Reproductor/práctica de Fase 3 (dónde se ingresa y muestra el resultado).
- [SymPy active deprecations](https://docs.sympy.org/latest/explanation/active-deprecations.html).

## Alcance de construcción
1. **Servicio `answer_grading_service.py`** con `grade_answer(question, raw_text) -> dict`
   (`{"correct": bool, "normalized": str, "reason": str}`):
   - **Numéricas:** normaliza coma/punto, fracciones (`a/b`), enteros/decimales; compara con
     `canonical_answer` usando `answer_tolerance` (absoluta o relativa, definir).
   - **Algebraicas:** parsea con un **AST restringido** (lista blanca de operadores `+ - * / **`,
     paréntesis, variables permitidas) → SymPy → compara por **equivalencia simbólica**
     (`simplify(expr - canonical) == 0`). Polinómicas y racionales.
   - **Sin `eval`/`exec`/`sympify` inseguro.** Límites duros: longitud de entrada, nº de
     operadores, nº de variables, exponente máximo. Rechaza funciones arbitrarias, ecuaciones,
     llamadas, atributos, código.
2. **Integración en la práctica (Fase 3):** input de texto para `numérica`/`algebraica`; guarda
   `text_answer`; muestra corrección. Las `alternativa` siguen igual.
3. **Tests de seguridad y corrección** (ver plan).

## Criterios de aceptación
- [ ] Barrera verde. Migraciones, si hay, aditivas.
- [ ] Numéricas equivalentes aceptadas (1/2 = 0.5 = 0,5 dentro de tolerancia); incorrectas rechazadas.
- [ ] Algebraicas equivalentes aceptadas (`2(x+1)` ≡ `2x+2`); no equivalentes rechazadas.
- [ ] **Seguridad:** entradas maliciosas / fuera de límites / funciones-código rechazadas SIN ejecutar
  nada; sin `eval`. Tests explícitos de inyección y de límites.
- [ ] Sin red; determinista. CSP/KaTeX intactos.

## Plan de pruebas
Numéricas (enteros, coma/punto, fracciones, tolerancia) · algebraicas equivalentes y no equivalentes ·
**manipulación/expresiones inválidas/límites** (longitud, operadores, variables, exponentes,
intentos de llamar funciones o acceder atributos) · que nunca se ejecute código del alumno.

## No-objetivos
- Ecuaciones, sistemas y funciones arbitrarias (fase posterior).
- Evaluaciones por nivel/final, timers, dominio (Fase 5).

## Riesgos / rollback
- **Seguridad (central):** AST restringido + SymPy; revisar deprecaciones de SymPy. Cierre lo audita
  🏛️ Claude. Rollback: deshabilitar tipos `numérica`/`algebraica` (volver a solo `alternativa`).
