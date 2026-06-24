# Plan general — Biblioteca de Conocimiento (Matemática)

> **Tracker vivo.** Lista en orden todos los bloques a generar. Cada bloque sigue el mismo ciclo de
> 3 pasos. Claude marca el avance y lleva la cuenta del **próximo código libre**.
>
> Reglas y formato: documento **«Reglas y nomenclatura»** (en NotebookLM/ChatGPT) + memoria de Claude.
> Prompts: `_PROMPT-GENERACION.md`. Códigos ocupados: `_REGISTRO-CODIGOS.md`.

## El ciclo por bloque (siempre igual)
1. **NotebookLM** — pídele el bloque (sigue «Reglas y nomenclatura», con el código inicial). Te
   devuelve la lista atómica fiel a tus libros + fuentes + sección GAPS.
2. **ChatGPT** — pégale la salida de NotebookLM. Estandariza (ids, códigos, 3 ejes), completa los
   GAPS del temario PAES y auto-audita (control de calidad).
3. **Claude (yo)** — me traes el YAML de ChatGPT. Hago el control final (colisiones, ids, competencia
   dudosa), lo guardo como **archivo separado** en `docs/conocimiento/` y actualizo este plan.

---

## RAMA 01 — FUNDAMENTOS (FUND)
- [x] **Lógica y conjuntos** (01.01–01.12) → `fundamentos-atomico.yaml` ✅

## RAMA 02 — NÚMEROS (NUM)
- [x] Enteros: conjunto, orden, operatoria (02.01–02.02) → `numeros-enteros.yaml` ✅
- [x] Teoría de números (02.03–02.08) → `numeros-teoria-de-numeros.yaml` ✅
- [x] Racionales (02.09–02.21) → `numeros-racionales.yaml` ✅
- [x] Reales, Potencias, Raíces, Logaritmos, Complejos (02.22–02.33) → `numeros-reales-potencias-raices-logaritmos.yaml` ✅
- [x] Razones, Proporciones, Porcentajes, Finanzas, Interés (02.34–02.44) → `numeros-razones-porcentajes-finanzas.yaml` ✅  · **RAMA 02 COMPLETA**

## RAMA 03 — ÁLGEBRA Y FUNCIONES (ALG)  · reinicia en `03.01` · (tema por tema)
- [x] 1. Nomenclatura y conceptos básicos (03.01–03.05) → `algebra-nomenclatura-conceptos.yaml` ✅
- [x] 2. Lenguaje algebraico y valorización (03.06–03.08) → `algebra-lenguaje-valorizacion.yaml` ✅
- [x] 3. Operaciones con expresiones algebraicas (03.09–03.13) → `algebra-operaciones.yaml` ✅
- [x] 4. Multiplicación algebraica (03.14–03.17) → `algebra-multiplicacion.yaml` ✅
- [x] 5. Productos notables (03.18–03.23) → `algebra-productos-notables.yaml` ✅
- [x] 6. Factorización (03.24–03.29) → `algebra-factorizacion.yaml` ✅
- [ ] 7. M.C.D., m.c.m. y fracciones algebraicas  → empieza en `03.30`  ⏭️ **AQUÍ VAMOS**
- [ ] 8. Ecuaciones de primer grado y sistemas
- [ ] 9. Desigualdades e inecuaciones
- [ ] 10. Funciones

## RAMA 04 — GEOMETRÍA (GEO)  · reinicia en `04.01`
- [ ] Geometría plana (ángulos, triángulos, cuadriláteros, polígonos, circunferencia)
- [ ] Perímetros y áreas
- [ ] Congruencia, semejanza, Thales y Pitágoras
- [ ] Cuerpos geométricos (área y volumen)
- [ ] Transformaciones isométricas, homotecia y vectores
- [ ] Geometría analítica (plano cartesiano, distancia, punto medio, ecuación de la recta)
- [ ] Trigonometría (razones, teorema del seno/coseno, identidades)

## RAMA 05 — PROBABILIDAD Y ESTADÍSTICA (EST)  · reinicia en `05.01`
- [ ] Estadística descriptiva (datos, tablas de frecuencia, gráficos)
- [ ] Medidas de tendencia central, de posición y de dispersión
- [ ] Probabilidad (espacio muestral, Laplace, reglas aditiva/multiplicativa, condicional, árbol)
- [ ] Combinatoria / técnicas de conteo
- [ ] Variable aleatoria y distribuciones (M2/electivo)

---

## Pasadas finales (después del esqueleto completo)
- [ ] **Grafo de prerrequisitos** (`prerrequisitos: [id,...]`) sobre todos los `id` — DAG, validar
  existencia y ausencia de ciclos.
- [ ] **Anti-duplicados** entre bloques (ej. `INVERSO_MULTIPLICATIVO`, `RAIZ_NO_EXACTA`).
- [ ] **Validar `competencia`/`cursos`** marcados "baja certeza" contra el temario DEMRE.
- [ ] **Reconciliar/retirar** los YAML gruesos antiguos (`numeros.yaml`, `fundamentos.yaml`, etc.).

## Estado actual
**Rama 02 completa.** Rama 03 ÁLGEBRA: sub-temas 1–6 listos (03.01–03.29).
**Próximo paso:** Rama 03, sub-tema 7 **«M.C.D., m.c.m. y fracciones algebraicas»**, código inicial **`03.30`**.
