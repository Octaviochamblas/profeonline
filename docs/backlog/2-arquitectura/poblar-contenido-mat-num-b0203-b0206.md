# Poblar contenido: MAT.NUM B0203–B0206 (Racionales / Reales / Razones / Sucesiones)

## Metadata
- **Estado:** listo para ejecución
- **Dueño actual:** Antigravity
- **Scope:** 289 recursos — B0203 (74r) + B0204 (93r) + B0205 (84r) + B0206 (38r)
- **Rama sugerida:** `content/mat-num-b0203-b0206`
- **Fecha:** 2026-06-28
- **Prerequisito:** `content/mat-num-b0201-b0202` completado (o en paralelo, distinta rama)

---

## Antes de empezar — lee estos documentos

1. `docs/backlog/2-arquitectura/poblar-contenido-mat-num-b0201-b0202.md` — proceso completo, reglas YAML/JSONL, formato `stable_id`, criterios de aceptación.
2. `docs/conocimiento/pauta-contenido.md` — 9 campos obligatorios YAML + 10 ejercicios por recurso.
3. Ejemplos de estilo: `mat-num-divisibilidad-multiplo-concepto.yaml` y `mat-num-teoria-numeros-banco-gen-1.jsonl`.

**Fuente matemática:** Racionales, Potencias, Raíces, Logaritmos, Razones y Sucesiones son temas de 7°–4° Medio. El contenido se genera desde el conocimiento propio del agente.

---

## Obtener lista de pendientes por bloque

```bash
python manage.py shell -c "
from apps.content.models import KnowledgeNode
for sid in ['MAT.NUM.B0203','MAT.NUM.B0204','MAT.NUM.B0205','MAT.NUM.B0206']:
    r = KnowledgeNode.objects.filter(node_type='recurso',
        parent__parent__semantic_id=sid, content__isnull=True).order_by('order')
    print(f'\n--- {sid} ({r.count()} pendientes) ---')
    for x in r: print(x.semantic_id)
"
```

---

## MAT.NUM.B0203 — Racionales (74 recursos)

### Subtemas presentes

| Subtema | Cant | Descripción |
|---|---|---|
| RACIONALES_CONCEPTO | 5 | Definición ℚ, condición denominador≠0, enteros como racionales, signo, ℕ⊂ℤ⊂ℚ |
| FRACCIONES_CONCEPTO | 5 | Fracción parte-todo, numerador, denominador, unidad fraccionaria |
| FRACCIONES_CLASIFICACION | 7 | Propia, impropia, aparente, mixto, no definida, indeterminada, conversión |
| FRACCIONES_EQUIVALENCIA | 7 | Equivalentes, amplificación, simplificación, irreductible, productos cruzados, mixto↔impropia |
| FRACCIONES_COMPARACION | 5 | Igual denominador, igual numerador, distinto denominador, producto cruzado, densidad ℚ, recta |
| FRACCIONES_OPERATORIA | 9 | Adición/sustracción igual/distinto denominador, multiplicación, inverso mult, división, mixtos, jerarquía, fracción de cantidad |
| RACIONALES_PROPIEDADES | 10 | Clausura, conmutativa, asociativa, neutro aditivo/mult, inverso aditivo/mult, distributiva (×2) |
| DECIMALES_CLASIFICACION | 5 | Finito, periódico, semiperiódico, periodo, anteperiodo |
| DECIMALES_OPERATORIA | 4 | Adición, sustracción, multiplicación, división |
| FRACCION_DECIMAL | 4 | Conversión por división, denominador potencia 10, detección finito/periódico |
| DECIMAL_FRACCION | 3 | Finito→fracción, periódico→fracción, semiperiódico→fracción |
| APROXIMACIONES | 5 | Defecto, exceso, redondeo, regla del 5, truncamiento |
| ERROR_NUMERICO | 3 | Error absoluto, relativo, porcentual |

### Tandas sugeridas (15 tandas, ~5r cada una)

| Tanda | Subtema(s) | JSONL |
|---|---|---|
| 1 | RACIONALES_CONCEPTO + FRACCIONES_CONCEPTO (5+4r) | `mat-num-racionales-banco-gen-1.jsonl` |
| 2 | FRACCIONES_CONCEPTO (1r) + FRACCIONES_CLASIFICACION (4r) | `mat-num-racionales-banco-gen-2.jsonl` |
| 3 | FRACCIONES_CLASIFICACION (3r) + FRACCIONES_EQUIVALENCIA (2r) | `mat-num-racionales-banco-gen-3.jsonl` |
| 4 | FRACCIONES_EQUIVALENCIA (5r) | `mat-num-racionales-banco-gen-4.jsonl` |
| 5 | FRACCIONES_COMPARACION (5r) | `mat-num-racionales-banco-gen-5.jsonl` |
| 6 | FRACCIONES_OPERATORIA pt1 (5r) | `mat-num-racionales-banco-gen-6.jsonl` |
| 7 | FRACCIONES_OPERATORIA pt2 (4r) + RACIONALES_PROPIEDADES (1r) | `mat-num-racionales-banco-gen-7.jsonl` |
| 8 | RACIONALES_PROPIEDADES pt1 (5r) | `mat-num-racionales-banco-gen-8.jsonl` |
| 9 | RACIONALES_PROPIEDADES pt2 (4r) + DECIMALES_CLASIFICACION (1r) | `mat-num-racionales-banco-gen-9.jsonl` |
| 10 | DECIMALES_CLASIFICACION (4r) + DECIMALES_OPERATORIA (1r) | `mat-num-racionales-banco-gen-10.jsonl` |
| 11 | DECIMALES_OPERATORIA (3r) + FRACCION_DECIMAL pt1 (2r) | `mat-num-racionales-banco-gen-11.jsonl` |
| 12 | FRACCION_DECIMAL (2r) + DECIMAL_FRACCION (3r) | `mat-num-racionales-banco-gen-12.jsonl` |
| 13 | APROXIMACIONES (5r) | `mat-num-racionales-banco-gen-13.jsonl` |
| 14 | ERROR_NUMERICO (3r) — tanda corta | `mat-num-racionales-banco-gen-14.jsonl` |

---

## MAT.NUM.B0204 — Reales, Potencias, Raíces y Logaritmos (93 recursos)

### Subtemas presentes

| Subtema | Cant | Descripción |
|---|---|---|
| IRRACIONALES | 5 | Definición, decimal infinito no periódico, √no exacta, π, e, número áureo |
| REALES | 6 | Definición, ℚ∪ℚ', inclusión conjuntos, recta numérica, orden, operaciones |
| POTENCIAS_CONCEPTO | 12 | Definición, base, exponente, exp=1/0/natural, base cero, base negativa, signo, base racional, exp entero negativo, exp racional |
| POTENCIAS_PROPIEDADES | 7 | Mult igual base, div igual base, potencia de potencia, pot de producto, pot de cociente, mult igual exp, div igual exp |
| NOTACION_CIENTIFICA | 6 | Concepto, números grandes/pequeños, conversión, mult, div, ad/sust |
| RAICES_CONCEPTO | 8 | Definición raíz n-ésima, inversa de potencia, índice, radicando, cuadrada principal, existencia (índice par/impar), exacta/no exacta, exp fraccionario |
| RAICES_PROPIEDADES | 8 | Mult/div igual índice, raíz de raíz, raíz de potencia, extracción factor, ingreso factor, descomposición radicando, semejantes, ad/sust semejantes |
| RACIONALIZACION | 3 | Monomio raíz cuadrada, monomio raíz n-ésima, binomio conjugado |
| LOGARITMOS_CONCEPTO | 8 | Definición, relación con potencia, formas logarítmica↔exponencial, restricciones (base>0, base≠1, arg>0), log de 1, log de la base, log decimal, log natural |
| LOGARITMOS_PROPIEDADES | 7 | Producto, cociente, potencia, raíz, cambio de base, pot de base logarítmica, log de potencia misma base |
| IMAGINARIOS | 4 | Unidad imaginaria i, i², raíz de -1, potencias de i |
| COMPLEJOS | 8 | Definición, forma binomial, parte real/imaginaria, representación cartesiana, plano complejo, conjugado, módulo |

### Tandas sugeridas (19 tandas)

| Tanda | Subtema(s) | JSONL |
|---|---|---|
| 1 | IRRACIONALES (5r) + REALES (1r) | `mat-num-reales-banco-gen-1.jsonl` |
| 2 | REALES (5r) | `mat-num-reales-banco-gen-2.jsonl` |
| 3 | POTENCIAS_CONCEPTO pt1 (5r) | `mat-num-reales-banco-gen-3.jsonl` |
| 4 | POTENCIAS_CONCEPTO pt2 (5r) | `mat-num-reales-banco-gen-4.jsonl` |
| 5 | POTENCIAS_CONCEPTO pt3 (2r) + POTENCIAS_PROPIEDADES (3r) | `mat-num-reales-banco-gen-5.jsonl` |
| 6 | POTENCIAS_PROPIEDADES (4r) + NOTACION_CIENTIFICA (1r) | `mat-num-reales-banco-gen-6.jsonl` |
| 7 | NOTACION_CIENTIFICA (5r) | `mat-num-reales-banco-gen-7.jsonl` |
| 8 | RAICES_CONCEPTO pt1 (5r) | `mat-num-reales-banco-gen-8.jsonl` |
| 9 | RAICES_CONCEPTO pt2 (3r) + RAICES_PROPIEDADES (2r) | `mat-num-reales-banco-gen-9.jsonl` |
| 10 | RAICES_PROPIEDADES (5r) | `mat-num-reales-banco-gen-10.jsonl` |
| 11 | RAICES_PROPIEDADES (1r) + RACIONALIZACION (3r) + LOGARITMOS_CONCEPTO (1r) | `mat-num-reales-banco-gen-11.jsonl` |
| 12 | LOGARITMOS_CONCEPTO pt1 (5r) | `mat-num-reales-banco-gen-12.jsonl` |
| 13 | LOGARITMOS_CONCEPTO pt2 (2r) + LOGARITMOS_PROPIEDADES (3r) | `mat-num-reales-banco-gen-13.jsonl` |
| 14 | LOGARITMOS_PROPIEDADES (4r) + IMAGINARIOS (1r) | `mat-num-reales-banco-gen-14.jsonl` |
| 15 | IMAGINARIOS (3r) + COMPLEJOS (2r) | `mat-num-reales-banco-gen-15.jsonl` |
| 16 | COMPLEJOS (5r) | `mat-num-reales-banco-gen-16.jsonl` |
| 17 | COMPLEJOS (1r) — tanda corta | `mat-num-reales-banco-gen-17.jsonl` |

---

## MAT.NUM.B0205 — Razones, Proporciones, Porcentajes y Finanzas (84 recursos)

### Subtemas presentes

| Subtema | Cant | Descripción |
|---|---|---|
| RAZONES | 5 | Definición cociente, antecedente, consecuente, valor, serie de razones, suma términos |
| PROPORCIONES | 8 | Definición, extremos/medios, producto cruzado, cuarta/tercera proporcional, media proporcional, composición/descomposición |
| PROP_DIRECTA | 5 | Concepto, constante, reconocimiento tabular, gráfico recta, modelo algebraico, problemas |
| PROP_INVERSA | 5 | Concepto, constante, reconocimiento tabular, gráfico hipérbola, modelo algebraico, problemas |
| PROP_COMPUESTA | 5 | Concepto, relación directa/inversa, variable constante, fórmula generalizada, problemas |
| REPARTO_ESCALAS | 6 | Directo, inverso, parte desconocida, escala como razón, longitud plano/real, escala desconocida |
| PORCENTAJES | 8 | Razón/100, representación (gráfica/decimal/fraccionaria), cálculo valor/porcentaje/total, porcentaje de porcentaje, cálculo mental 10/1 |
| VARIACION_PORCENTUAL | 7 | Aumento, disminución, descuento, cambio absoluto/relativo, valor final (aumento/descuento), porcentajes sucesivos, IVA |
| FINANZAS_PERSONALES | 7 | Tipos gasto/ingreso/deuda, presupuesto, balance/flujo, IPC, rentabilidad, tasa interés real, cotización AFP, proyección previsional |
| INTERES_SIMPLE | 5 | Concepto, cálculo interés, monto final, capital inicial, tasa, tiempo |
| INTERES_COMPUESTO | 7 | Concepto, monto, interés, modelo exponencial, tasa periódica, número periodos, comparación regímenes, anualidad, amortización |

### Tandas sugeridas (17 tandas)

| Tanda | Subtema(s) | JSONL |
|---|---|---|
| 1 | RAZONES (5r) + PROPORCIONES (1r) | `mat-num-razones-banco-gen-1.jsonl` |
| 2 | PROPORCIONES (5r) | `mat-num-razones-banco-gen-2.jsonl` |
| 3 | PROPORCIONES (2r) + PROP_DIRECTA (3r) | `mat-num-razones-banco-gen-3.jsonl` |
| 4 | PROP_DIRECTA (3r) + PROP_INVERSA (2r) | `mat-num-razones-banco-gen-4.jsonl` |
| 5 | PROP_INVERSA (3r) + PROP_COMPUESTA (2r) | `mat-num-razones-banco-gen-5.jsonl` |
| 6 | PROP_COMPUESTA (3r) + REPARTO_ESCALAS (2r) | `mat-num-razones-banco-gen-6.jsonl` |
| 7 | REPARTO_ESCALAS (4r) + PORCENTAJES (1r) | `mat-num-razones-banco-gen-7.jsonl` |
| 8 | PORCENTAJES (5r) | `mat-num-razones-banco-gen-8.jsonl` |
| 9 | PORCENTAJES (2r) + VARIACION_PORCENTUAL (3r) | `mat-num-razones-banco-gen-9.jsonl` |
| 10 | VARIACION_PORCENTUAL (4r) + FINANZAS_PERSONALES (1r) | `mat-num-razones-banco-gen-10.jsonl` |
| 11 | FINANZAS_PERSONALES (5r) | `mat-num-razones-banco-gen-11.jsonl` |
| 12 | FINANZAS_PERSONALES (1r) + INTERES_SIMPLE (4r) | `mat-num-razones-banco-gen-12.jsonl` |
| 13 | INTERES_SIMPLE (1r) + INTERES_COMPUESTO (4r) | `mat-num-razones-banco-gen-13.jsonl` |
| 14 | INTERES_COMPUESTO (3r) — tanda corta | `mat-num-razones-banco-gen-14.jsonl` |

---

## MAT.NUM.B0206 — Sucesiones y Progresiones (38 recursos)

### Subtemas presentes

| Subtema | Cant | Descripción |
|---|---|---|
| SUCESIONES_BASE | 7 | Definición, orden, notación subíndice, término general (concepto/cálculo), regularidad numérica/gráfica, recursiva, comparación explícita/recursiva |
| PROG_ARITMETICA | 9 | Definición, diferencia común, reconocimiento, término general, cálculo 1er término/índice, suma finita, modelo cambio lineal, interpretación diferencia |
| PROG_GEOMETRICA | 8 | Definición, razón geométrica, reconocimiento, término general, cálculo 1er término/índice, suma finita, modelo crecimiento, interpretación razón |
| SERIE_GEOMETRICA | 5 | Concepto serie, finita, infinita (concepto), condición convergencia, suma infinita, interpretación límite |
| PROGRESIONES_COMPARACION | 5 | PA vs PG, cambio aditivo/multiplicativo, elección modelo, interpolación aritmética/geométrica |

### Tandas sugeridas (8 tandas)

| Tanda | Subtema(s) | JSONL |
|---|---|---|
| 1 | SUCESIONES_BASE pt1 (5r) | `mat-num-sucesiones-banco-gen-1.jsonl` |
| 2 | SUCESIONES_BASE pt2 (2r) + PROG_ARITMETICA (3r) | `mat-num-sucesiones-banco-gen-2.jsonl` |
| 3 | PROG_ARITMETICA (5r) | `mat-num-sucesiones-banco-gen-3.jsonl` |
| 4 | PROG_ARITMETICA (1r) + PROG_GEOMETRICA (4r) | `mat-num-sucesiones-banco-gen-4.jsonl` |
| 5 | PROG_GEOMETRICA (4r) + SERIE_GEOMETRICA (1r) | `mat-num-sucesiones-banco-gen-5.jsonl` |
| 6 | SERIE_GEOMETRICA (4r) + PROGRESIONES_COMPARACION (1r) | `mat-num-sucesiones-banco-gen-6.jsonl` |
| 7 | PROGRESIONES_COMPARACION (4r) — tanda corta | `mat-num-sucesiones-banco-gen-7.jsonl` |

---

## Naming de archivos YAML

Patrón: `mat-num-{subtema-kebab}-{concepto-kebab}.yaml`

Ejemplos:
- `MAT.NUM.RACIONALES_CONCEPTO.DEFINICION_Q` → `mat-num-racionales-concepto-definicion-q.yaml`
- `MAT.NUM.IRRACIONALES.PI` → `mat-num-irracionales-pi.yaml`
- `MAT.NUM.POTENCIAS_PROPIEDADES.MULTIPLICACION_IGUAL_BASE` → `mat-num-potencias-propiedades-mult-igual-base.yaml`
- `MAT.NUM.INTERES_COMPUESTO.MODELO_EXPONENCIAL` → `mat-num-interes-compuesto-modelo-exponencial.yaml`

---

## Proceso de ejecución

Idéntico al de `poblar-contenido-mat-num-b0201-b0202.md`. Trabajar bloque a bloque (primero B0203 completo, luego B0204, etc.). Hacer commit al final de cada tanda.

---

## Verificación de cobertura total

```bash
python manage.py shell -c "
from apps.content.models import KnowledgeNode
for sid in ['MAT.NUM.B0203','MAT.NUM.B0204','MAT.NUM.B0205','MAT.NUM.B0206']:
    r = KnowledgeNode.objects.filter(node_type='recurso', parent__parent__semantic_id=sid)
    done = r.filter(content__isnull=False).count()
    print(f'{sid}: {done}/{r.count()}')
"
```

## Criterios de aceptación

- [ ] B0203: 74/74 recursos con `NodeContent`
- [ ] B0204: 93/93 recursos con `NodeContent`
- [ ] B0205: 84/84 recursos con `NodeContent`
- [ ] B0206: 38/38 recursos con `NodeContent`
- [ ] Cada recurso: 10 ejercicios (3+1+3+3)
- [ ] No se tocó código ni archivos de otros ejes
