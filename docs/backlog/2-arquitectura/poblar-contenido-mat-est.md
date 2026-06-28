# Poblar contenido: MAT.EST — Probabilidad y Estadística

## Metadata
- **Estado:** listo para ejecución
- **Dueño actual:** Antigravity
- **Scope:** 260 recursos — 7 bloques (B0501–B0507)
- **Rama sugerida:** `content/mat-est`
- **Fecha:** 2026-06-28

---

## Antes de empezar — lee estos documentos

1. `docs/backlog/2-arquitectura/poblar-contenido-mat-num-b0201-b0202.md` — proceso completo, reglas YAML/JSONL, formato `stable_id`, criterios de aceptación.
2. `docs/conocimiento/pauta-contenido.md` — 9 campos obligatorios + 10 ejercicios por recurso.
3. Ejemplos de estilo: `mat-num-divisibilidad-multiplo-concepto.yaml` y `mat-num-teoria-numeros-banco-gen-1.jsonl`.

**Fuente matemática:** Estadística y Probabilidad son temas de 2°–4° Medio y preuniversitario. El contenido se genera desde el conocimiento propio del agente. Los recursos de B0507 (Distribución Normal) requieren conocimiento de la función de densidad gaussiana y tablas Z.

---

## Obtener lista de pendientes por bloque

```bash
python manage.py shell -c "
from apps.content.models import KnowledgeNode
for sid in ['MAT.EST.B0501','MAT.EST.B0502','MAT.EST.B0503',
            'MAT.EST.B0504','MAT.EST.B0505','MAT.EST.B0506','MAT.EST.B0507']:
    r = KnowledgeNode.objects.filter(node_type='recurso',
        parent__parent__semantic_id=sid, content__isnull=True).order_by('order')
    print(f'\n--- {sid} ({r.count()} pendientes) ---')
    for x in r: print(x.semantic_id)
"
```

---

## MAT.EST.B0501 — Estadística Descriptiva (42 recursos)

### Subtemas y tandas

| Subtema | Cant | Descripción |
|---|---|---|
| RECOLECCION_BASE | 6 | Población, muestra, representatividad, sesgo, encuesta, censo vs. muestra |
| VARIABLES_TIPOS | 5 | Cualitativa (id/nominal/ordinal), cuantitativa (id/discreta/continua) |
| TABLAS_NO_AGRUPADAS | 8 | Dato, frecuencia, absoluta, abs. acumulada, relativa, relativa acumulada, porcentual, tabulación total |
| DATOS_AGRUPADOS | 4 | Intervalo, límites, amplitud, marca de clase, construcción tabla |
| GRAFICOS_BASE | 6 | Barras simples/dobles, circular (def/ángulos), pictograma, líneas de tendencia |
| GRAFICOS_CONTINUOS | 4 | Histograma (const/áreas), polígono frecuencia, transición tabla→gráfico |
| REPRESENTACIONES_AVANZADAS | 3 | Tallo y hoja, ojiva (lectura) |
| INTERPRETACION_CRITICA | 5 | Extracción info, errores de escala, sesgo visual, inferencia contexto, evaluación crítica |

| Tanda | Subtema(s) | JSONL |
|---|---|---|
| 1 | RECOLECCION_BASE (6r) | `mat-est-descriptiva-banco-gen-1.jsonl` |
| 2 | VARIABLES_TIPOS (5r) + TABLAS_NO_AGRUPADAS (1r) | `mat-est-descriptiva-banco-gen-2.jsonl` |
| 3 | TABLAS_NO_AGRUPADAS (5r) | `mat-est-descriptiva-banco-gen-3.jsonl` |
| 4 | TABLAS_NO_AGRUPADAS (2r) + DATOS_AGRUPADOS (3r) | `mat-est-descriptiva-banco-gen-4.jsonl` |
| 5 | DATOS_AGRUPADOS (2r) + GRAFICOS_BASE (3r) | `mat-est-descriptiva-banco-gen-5.jsonl` |
| 6 | GRAFICOS_BASE (3r) + GRAFICOS_CONTINUOS (2r) | `mat-est-descriptiva-banco-gen-6.jsonl` |
| 7 | GRAFICOS_CONTINUOS (2r) + REPRESENTACIONES_AVANZADAS (2r) + INTERPRETACION_CRITICA (1r) | `mat-est-descriptiva-banco-gen-7.jsonl` |
| 8 | INTERPRETACION_CRITICA (4r) — tanda corta | `mat-est-descriptiva-banco-gen-8.jsonl` |

---

## MAT.EST.B0502 — Medidas de Tendencia Central (27 recursos)

### Subtemas y tandas

| Subtema | Cant | Descripción |
|---|---|---|
| MEDIA_PROMEDIO | 7 | Definición, cálculo no agrupados, tabla frecuencia, datos agrupados, ponderada, dato faltante, suma cte, mult cte, media geométrica |
| MODA_ANALISIS | 6 | Definición, unimodal, bimodal, amodal, tabla frecuencia, intervalo modal |
| MEDIANA_ANALISIS | 6 | Definición, ordenamiento, cálculo impar/par, tabla frecuencia, intervalo mediano |
| MTC_PROPIEDADES | 5 | Valores extremos, estabilidad mediana, comparación medidas, elección adecuada, comparación grupos, simetría distribución |

| Tanda | Subtema(s) | JSONL |
|---|---|---|
| 1 | MEDIA_PROMEDIO pt1 (5r) | `mat-est-mtc-banco-gen-1.jsonl` |
| 2 | MEDIA_PROMEDIO pt2 (4r) + MODA_ANALISIS (1r) | `mat-est-mtc-banco-gen-2.jsonl` |
| 3 | MODA_ANALISIS (5r) | `mat-est-mtc-banco-gen-3.jsonl` |
| 4 | MEDIANA_ANALISIS (5r) | `mat-est-mtc-banco-gen-4.jsonl` |
| 5 | MEDIANA_ANALISIS (1r) + MTC_PROPIEDADES (4r) — tanda corta | `mat-est-mtc-banco-gen-5.jsonl` |
| 6 | MTC_PROPIEDADES (2r) — tanda corta | `mat-est-mtc-banco-gen-6.jsonl` |

---

## MAT.EST.B0503 — Medidas de Posición y Dispersión (34 recursos)

### Subtemas y tandas

| Subtema | Cant | Descripción |
|---|---|---|
| PERCENTILES | 6 | Definición, interpretación, cálculo posición, datos no agrupados, tabla frecuencia, intervalo, percentil50=mediana |
| CUARTILES | 6 | Definición, Q1/Q2/Q3, equivalencia percentil, cálculo no agrupados, tabla frecuencia, comparación grupos |
| DIAGRAMA_CAJA | 6 | 5 números, lectura, construcción, RIC, interpretación dispersión, simetría, outliers |
| DISPERSION_BASE | 6 | Rango (concepto/cálculo), desviación media, varianza (concepto/cálculo), desviación estándar (concepto/cálculo) |
| DISPERSION_COMPARATIVA | 5 | CV definición/cálculo, comparación relativa, homogeneidad contexto, comparación medidas |

| Tanda | Subtema(s) | JSONL |
|---|---|---|
| 1 | PERCENTILES (5r) | `mat-est-dispersion-banco-gen-1.jsonl` |
| 2 | PERCENTILES (2r) + CUARTILES (3r) | `mat-est-dispersion-banco-gen-2.jsonl` |
| 3 | CUARTILES (3r) + DIAGRAMA_CAJA (2r) | `mat-est-dispersion-banco-gen-3.jsonl` |
| 4 | DIAGRAMA_CAJA (4r) + DISPERSION_BASE (1r) | `mat-est-dispersion-banco-gen-4.jsonl` |
| 5 | DISPERSION_BASE (5r) | `mat-est-dispersion-banco-gen-5.jsonl` |
| 6 | DISPERSION_BASE (1r) + DISPERSION_COMPARATIVA (4r) — tanda corta | `mat-est-dispersion-banco-gen-6.jsonl` |
| 7 | DISPERSION_COMPARATIVA (1r) — tanda muy corta, fusionar con tanda 6 | `mat-est-dispersion-banco-gen-6.jsonl` |

---

## MAT.EST.B0504 — Probabilidad Básica (31 recursos)

### Subtemas y tandas

| Subtema | Cant | Descripción |
|---|---|---|
| PROBA_FUNDAMENTOS | 8 | Exp. aleatorio/determinista, espacio muestral, cardinalidad, evento (concepto/seguro/imposible/mutuamente excluyentes/equiprobables), complemento |
| LAPLACE_MUESTRALES | 8 | Casos favorables/totales, Laplace, fracción/decimal, rango valores, complemento, monedas, dados |
| REPRESENTACION_CONTEO | 3 | Diagrama árbol (espacio/probabilidades), principio multiplicativo |
| REGLAS_PROBABILIDAD | 5 | Suma excluyentes, suma general, producto independientes, eventos dependientes, extracción sin reposición |
| TABLAS_CONTINGENCIA | 5 | Estructura doble, totales marginales, probabilidad simple, conjunta, interpretación |

| Tanda | Subtema(s) | JSONL |
|---|---|---|
| 1 | PROBA_FUNDAMENTOS pt1 (5r) | `mat-est-probabilidad-banco-gen-1.jsonl` |
| 2 | PROBA_FUNDAMENTOS pt2 (3r) + LAPLACE_MUESTRALES (2r) | `mat-est-probabilidad-banco-gen-2.jsonl` |
| 3 | LAPLACE_MUESTRALES (5r) | `mat-est-probabilidad-banco-gen-3.jsonl` |
| 4 | LAPLACE_MUESTRALES (1r) + REPRESENTACION_CONTEO (3r) + REGLAS_PROBABILIDAD (1r) | `mat-est-probabilidad-banco-gen-4.jsonl` |
| 5 | REGLAS_PROBABILIDAD (4r) + TABLAS_CONTINGENCIA (1r) | `mat-est-probabilidad-banco-gen-5.jsonl` |
| 6 | TABLAS_CONTINGENCIA (4r) — tanda corta | `mat-est-probabilidad-banco-gen-6.jsonl` |

---

## MAT.EST.B0505 — Probabilidad Condicional y Regla de Bayes (41 recursos)

### Subtemas y tandas

| Subtema | Cant | Descripción |
|---|---|---|
| PROBA_COND_BASE | 7 | Concepto restricción, notación, lectura, evento condicionante/condicionado, fórmula intersección, condición prob. positiva, cálculo directo, interpretación denominador |
| INDEPENDENCIA_CONDICIONAL | 7 | Definición, verificación condicional/producto, dependencia, tabla contingencia, totales marginales, probabilidad conjunta tabla, interpretación |
| PROBA_COMPUESTA_CONDICIONAL | 7 | Regla multiplicativa general, producto condicional, sin reposición, actualización casos, árbol condicional, ramas producto, suma rutas, interpretación |
| PROBABILIDAD_TOTAL | 6 | Partición espacio, casos, enunciado teorema, descomposición evento, aplicación fórmula/árbol, interpretación |
| REGLA_BAYES | 7 | Problema inverso, priori, posteriori, enunciado fórmula, denominador total, aplicación árbol, diagnóstico médico, control calidad, toma decisiones |

| Tanda | Subtema(s) | JSONL |
|---|---|---|
| 1 | PROBA_COND_BASE pt1 (5r) | `mat-est-cond-bayes-banco-gen-1.jsonl` |
| 2 | PROBA_COND_BASE pt2 (2r) + INDEPENDENCIA_CONDICIONAL (3r) | `mat-est-cond-bayes-banco-gen-2.jsonl` |
| 3 | INDEPENDENCIA_CONDICIONAL (4r) + PROBA_COMPUESTA_CONDICIONAL (1r) | `mat-est-cond-bayes-banco-gen-3.jsonl` |
| 4 | PROBA_COMPUESTA_CONDICIONAL (5r) | `mat-est-cond-bayes-banco-gen-4.jsonl` |
| 5 | PROBA_COMPUESTA_CONDICIONAL (1r) + PROBABILIDAD_TOTAL (4r) | `mat-est-cond-bayes-banco-gen-5.jsonl` |
| 6 | PROBABILIDAD_TOTAL (2r) + REGLA_BAYES (3r) | `mat-est-cond-bayes-banco-gen-6.jsonl` |
| 7 | REGLA_BAYES (4r) + INDEPENDENCIA (1r restante) | `mat-est-cond-bayes-banco-gen-7.jsonl` |
| 8 | REGLA_BAYES (3r restantes) — tanda corta | `mat-est-cond-bayes-banco-gen-8.jsonl` |

---

## MAT.EST.B0506 — Técnicas de Conteo y Distribución Binomial (44 recursos)

### Subtemas y tandas

| Subtema | Cant | Descripción |
|---|---|---|
| CONTEO_BASE | 5 | Principio aditivo, multiplicativo, diferencia, conectores lógicos, conteo con restricciones |
| PERMUTACIONES_VARIACIONES | 9 | Factorial (def/cálculo/simplificación), permutación lineal/con repetidos/circular, variación sin/con repetición, orden importa |
| COMBINACIONES | 9 | Definición, fórmula general, cálculo factorial, orden no importa, P vs C, coeficiente binomial, Pascal (construcción/coeficientes), simetría |
| BINOMIAL_BASE | 9 | Bernoulli, éxito, fracaso, prob. fracaso, n ensayos, independencia, prob. constante, variable éxitos, notación, identificación parámetros, función probabilidad, modelamiento |
| BINOMIAL_ANALISIS | 7 | Esperanza/media, varianza, desviación estándar, prob. exacta, a lo más, al menos, entre valores, uso complemento, interpretación |

| Tanda | Subtema(s) | JSONL |
|---|---|---|
| 1 | CONTEO_BASE (5r) + PERMUTACIONES (1r) | `mat-est-conteo-binomial-banco-gen-1.jsonl` |
| 2 | PERMUTACIONES pt1 (5r) | `mat-est-conteo-binomial-banco-gen-2.jsonl` |
| 3 | PERMUTACIONES pt2 (3r) + COMBINACIONES (2r) | `mat-est-conteo-binomial-banco-gen-3.jsonl` |
| 4 | COMBINACIONES pt1 (5r) | `mat-est-conteo-binomial-banco-gen-4.jsonl` |
| 5 | COMBINACIONES pt2 (2r) + BINOMIAL_BASE (3r) | `mat-est-conteo-binomial-banco-gen-5.jsonl` |
| 6 | BINOMIAL_BASE pt1 (5r) | `mat-est-conteo-binomial-banco-gen-6.jsonl` |
| 7 | BINOMIAL_BASE pt2 (4r) + BINOMIAL_ANALISIS (1r) | `mat-est-conteo-binomial-banco-gen-7.jsonl` |
| 8 | BINOMIAL_ANALISIS (5r) | `mat-est-conteo-binomial-banco-gen-8.jsonl` |
| 9 | BINOMIAL_ANALISIS (2r) — tanda corta | `mat-est-conteo-binomial-banco-gen-9.jsonl` |

---

## MAT.EST.B0507 — Distribución Normal (41 recursos)

### Subtemas y tandas

| Subtema | Cant | Descripción |
|---|---|---|
| NORMAL_BASE | 12 | Variable continua, recorrido, función densidad, prob. como área, área total, curva Gauss, simetría, parámetros (media/desviación), colas, prob. puntual = 0, reglas 68/95/99.7 |
| NORMAL_ESTANDAR | 7 | Notación N(μ,σ²), parámetros μ/σ, modelo Z, media=0, desviación=1, fórmula Z, calculo Z, interpretación Z, desestandarización |
| NORMAL_CALCULO | 8 | Lectura tabla, fila/columna, P(X<a), P(X>a), P(a<X<b), Z negativo, intervalo simétrico, área colas, búsqueda inversa Z, interpretación probabilidad |
| NORMAL_APLICACIONES | 6 | Reconocimiento modelo, variables biológicas, puntajes estandarizados, control calidad, umbral crítico, comparación valores Z, validez modelo |

| Tanda | Subtema(s) | JSONL |
|---|---|---|
| 1 | NORMAL_BASE pt1 (5r) | `mat-est-normal-banco-gen-1.jsonl` |
| 2 | NORMAL_BASE pt2 (5r) | `mat-est-normal-banco-gen-2.jsonl` |
| 3 | NORMAL_BASE pt3 (2r) + NORMAL_ESTANDAR (3r) | `mat-est-normal-banco-gen-3.jsonl` |
| 4 | NORMAL_ESTANDAR (4r) + NORMAL_CALCULO (1r) | `mat-est-normal-banco-gen-4.jsonl` |
| 5 | NORMAL_CALCULO (5r) | `mat-est-normal-banco-gen-5.jsonl` |
| 6 | NORMAL_CALCULO (2r) + NORMAL_APLICACIONES (3r) | `mat-est-normal-banco-gen-6.jsonl` |
| 7 | NORMAL_APLICACIONES (3r) — tanda corta | `mat-est-normal-banco-gen-7.jsonl` |

---

## Naming de archivos YAML

Patrón: `mat-est-{subtema-kebab}-{concepto-kebab}.yaml`

Ejemplos:
- `MAT.EST.RECOLECCION_BASE.POBLACION_DEF` → `mat-est-recoleccion-base-poblacion-def.yaml`
- `MAT.EST.PROBA_FUNDAMENTOS.ESPACIO_MUESTRAL` → `mat-est-proba-fundamentos-espacio-muestral.yaml`
- `MAT.EST.NORMAL_CALCULO.MENOR_QUE` → `mat-est-normal-calculo-menor-que.yaml`
- `MAT.EST.REGLA_BAYES.DIAGNOSTICO_MEDICO` → `mat-est-regla-bayes-diagnostico-medico.yaml`

---

## Proceso de ejecución

Idéntico al de `poblar-contenido-mat-num-b0201-b0202.md`. Trabajar bloque a bloque en orden (B0501→B0507). Commit al final de cada tanda.

---

## Verificación de cobertura total

```bash
python manage.py shell -c "
from apps.content.models import KnowledgeNode
for sid in ['MAT.EST.B0501','MAT.EST.B0502','MAT.EST.B0503',
            'MAT.EST.B0504','MAT.EST.B0505','MAT.EST.B0506','MAT.EST.B0507']:
    r = KnowledgeNode.objects.filter(node_type='recurso', parent__parent__semantic_id=sid)
    done = r.filter(content__isnull=False).count()
    print(f'{sid}: {done}/{r.count()}')
"
```

## Criterios de aceptación

- [ ] 260/260 recursos con `NodeContent` (7 bloques)
- [ ] Cada recurso: 10 ejercicios (3+1+3+3)
- [ ] `python manage.py check` sin errores
- [ ] No se tocó código ni archivos de otros ejes
