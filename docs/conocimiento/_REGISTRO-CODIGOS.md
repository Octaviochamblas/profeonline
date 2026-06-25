# Registro de códigos — Biblioteca de Conocimiento

> Para que cualquier sesión (humano o IA) sepa **desde qué código seguir** sin recordar nada.
> Cada bloque se entrega como **archivo YAML separado** (regla permanente). Los `cod` no se
> reutilizan ni renumeran; el `id` semántico es la llave estable.

## Estándar en una línea

`EE.BB.TT.RR` (eje.bloque.tema.recurso). Recurso: `id MAT.<ABREV>.<TEMA>.<SLUG>` (el id empieza
con el id del tema). 3 ejes por recurso: `competencia` (M1|M2|U), `dificultad`
(basica|media|avanzada), `cursos` ([1B..8B, 1M..4M]). Atomización máxima.
`prerrequisitos` → pasada final (aún no).

> **Nota migración (2026-06-24):** sistema renumerado de `RR.TT.rr` → `EE.BB.TT.RR`. El
> `bloque_codigo` (EE.BB) aparece ahora en la cabecera de cada YAML. Temas reinician en `.01`
> dentro de cada bloque, por lo que insertar un bloque nuevo no afecta la numeración de los demás.

---

## Eje 01 — FUNDAMENTOS (abrev. FUND)

| Bloque | Código BB | Temas | Archivo | Estado |
|--------|-----------|-------|---------|--------|
| Lógica | 01.01 | 01.01.01–01.01.05 | `fundamentos-logica.yaml` | ✅ guardado |
| Conjuntos | 01.02 | 01.02.01–01.02.07 | `fundamentos-conjuntos.yaml` | ✅ guardado |

`fundamentos-atomico.yaml` = archivo antiguo reemplazado (solo redirige a los dos nuevos).

**Siguiente bloque en eje 01:** `01.03` (libre).

---

## Eje 02 — NÚMEROS (abrev. NUM)

| Bloque | Código BB | Temas | Archivo | Estado |
|--------|-----------|-------|---------|--------|
| Enteros | 02.01 | 02.01.01–02.01.02 | `numeros-enteros.yaml` | ✅ guardado |
| Teoría de Números | 02.02 | 02.02.01–02.02.06 | `numeros-teoria-de-numeros.yaml` | ✅ guardado |
| Racionales | 02.03 | 02.03.01–02.03.13 | `numeros-racionales.yaml` | ✅ guardado |
| Reales, Potencias, Raíces y Logaritmos | 02.04 | 02.04.01–02.04.12 | `numeros-reales-potencias-raices-logaritmos.yaml` | ✅ guardado |
| Razones, Proporciones, Porcentajes y Finanzas | 02.05 | 02.05.01–02.05.11 | `numeros-razones-porcentajes-finanzas.yaml` | ✅ guardado |

**Eje 02 NÚMEROS COMPLETO (02.01–02.05).** Siguiente bloque: `02.06` (libre).

---

## Eje 03 — ÁLGEBRA Y FUNCIONES (abrev. ALG)

| Bloque | Código BB | Temas | Archivo | Estado |
|--------|-----------|-------|---------|--------|
| Nomenclatura y Conceptos Algebraicos | 03.01 | 03.01.01–03.01.05 | `algebra-nomenclatura-conceptos.yaml` | ✅ guardado |
| Lenguaje Algebraico y Valorización | 03.02 | 03.02.01–03.02.03 | `algebra-lenguaje-valorizacion.yaml` | ✅ guardado |
| Operaciones Algebraicas | 03.03 | 03.03.01–03.03.05 | `algebra-operaciones.yaml` | ✅ guardado |
| Multiplicación Algebraica | 03.04 | 03.04.01–03.04.04 | `algebra-multiplicacion.yaml` | ✅ guardado |
| Productos Notables | 03.05 | 03.05.01–03.05.06 | `algebra-productos-notables.yaml` | ✅ guardado |
| Factorización | 03.06 | 03.06.01–03.06.06 | `algebra-factorizacion.yaml` | ✅ guardado |
| M.C.D., m.c.m. y Fracciones Algebraicas | 03.07 | 03.07.01–03.07.08 | `algebra-mcd-mcm-fracciones.yaml` | ✅ guardado |
| Ecuaciones de Primer Grado y Sistemas | 03.08 | 03.08.01–03.08.07 | `algebra-ecuaciones-sistemas.yaml` | ✅ guardado |
| Desigualdades e Inecuaciones | 03.09 | 03.09.01–03.09.07 | `algebra-inecuaciones.yaml` | ✅ guardado |
| Funciones | 03.10 | 03.10.01–03.10.09 | `algebra-funciones.yaml` | ✅ guardado |
| Ecuaciones de Segundo Grado | 03.11 | 03.11.01–03.11.06 | `algebra-ecuaciones-cuadraticas.yaml` | ✅ guardado (M1 + ext. M2; 41 recursos) |
| Función Cuadrática | 03.12 | 03.12.01–03.12.06 | `algebra-funcion-cuadratica.yaml` | ✅ guardado (M1; 47 recursos) |
| Funciones Exponencial y Logarítmica | 03.13 | 03.13.01–03.13.05 | `algebra-funciones-exp-log.yaml` | ✅ guardado (M2; 54 recursos) |
| Función Potencia | 03.14 | 03.14.01–03.14.05 | `algebra-funcion-potencia.yaml` | ✅ guardado (M2; 50 recursos) |

**Eje 03 ÁLGEBRA Y FUNCIONES COMPLETO (03.01–03.14).** Siguiente bloque: `03.15` (libre).

---

## Eje 04 — GEOMETRÍA (abrev. GEO)

| Bloque | Código BB | Temas | Archivo | Estado |
|--------|-----------|-------|---------|--------|
| Ángulos: Fundamentos y Relaciones | 04.01 | 04.01.01–04.01.07 | `geometria-angulos.yaml` | ✅ guardado |
| Triángulos: Propiedades y Clasificación | 04.02 | 04.02.01–04.02.06 | `geometria-triangulos.yaml` | ✅ guardado |
| Elementos Secundarios del Triángulo | 04.03 | 04.03.01–04.03.07 | `geometria-elementos-secundarios.yaml` | ✅ guardado |
| Perímetros, Áreas y Teoremas | 04.04 | 04.04.01–04.04.06 | `geometria-areas-pitagoras.yaml` | ✅ guardado (04.04.04 usa TRIANGULOS_NOTABLES_METRICA) |
| Congruencia, Semejanza y Homotecia | 04.05 | 04.05.01–04.05.04 | `geometria-congruencia-semejanza.yaml` | ✅ guardado |
| Polígonos y Cuadriláteros | 04.06 | 04.06.01–04.06.04 | `geometria-poligonos-cuadrilateros.yaml` | ✅ guardado |
| Circunferencia y Círculo | 04.07 | 04.07.01–04.07.05 | `geometria-circunferencia-circulo.yaml` | ✅ guardado |
| Geometría del Espacio y Cuerpos Geométricos | 04.08 | 04.08.01–04.08.04 | `geometria-espacio-cuerpos.yaml` | ✅ guardado |
| Sistema Cartesiano y Vectores | 04.09 | 04.09.01–04.09.04 | `geometria-cartesiano-vectores.yaml` | ✅ guardado |
| Transformaciones Isométricas | 04.10 | 04.10.01–04.10.03 | `geometria-isometrias.yaml` | ✅ guardado |
| Trigonometría en el Triángulo Rectángulo | 04.11 | 04.11.01–04.11.05 | `geometria-trigonometria.yaml` | ✅ guardado |

**Eje 04 GEOMETRÍA COMPLETO (04.01–04.11).** Siguiente eje: `05` (PROBABILIDAD Y ESTADÍSTICA).

---

## Eje 05 — PROBABILIDAD Y ESTADÍSTICA (abrev. EST)

| Bloque | Código BB | Temas | Archivo | Estado |
|--------|-----------|-------|---------|--------|
| Estadística Descriptiva | 05.01 | 05.01.01–05.01.08 | `estadistica-descriptiva.yaml` | ✅ guardado (temas 09–11 retirados → 05.02/05.03) |
| Medidas de Tendencia Central (MTC) | 05.02 | 05.02.01–05.02.04 | `estadistica-tendencia-central.yaml` | ✅ guardado |
| Medidas de Posición y Dispersión | 05.03 | 05.03.01–05.03.05 | `estadistica-posicion-dispersion.yaml` | ✅ guardado |
| Probabilidad Básica | 05.04 | 05.04.01–05.04.05 | `probabilidad-basica.yaml` | ✅ guardado (solo M1; Pascal → 05.06; condicional → 05.05) |
| Probabilidad Condicional y Regla de Bayes | 05.05 | 05.05.01–05.05.05 | `probabilidad-condicional-bayes.yaml` | ✅ guardado |
| Técnicas de Conteo y Distribución Binomial | 05.06 | 05.06.01–05.06.05 | `probabilidad-conteo-binomial.yaml` | ✅ guardado |
| Distribución Normal | 05.07 | 05.07.01–05.07.04 | `estadistica-normal.yaml` | ✅ guardado (solo M2, 4M; 41 recursos) |

**Eje 05 PROBABILIDAD Y ESTADÍSTICA COMPLETO (05.01–05.07).** Siguiente bloque: `05.08` (libre).

---

## Ejes pendientes

_(ninguno — todos los ejes iniciados. Bloques 05.02–05.06 pendientes de generación.)_

## Pasadas pendientes (post-esqueleto)

1. **Grafo de prerrequisitos** (`prerrequisitos: [id,...]`) sobre los `id` ya existentes — DAG,
   validar que cada id exista y que no haya ciclos.
2. **Anti-duplicado:** resolver recursos repetidos (ej. `INVERSO_MULTIPLICATIVO` en operatoria y
   propiedades de Q; `RAIZ_NO_EXACTA` en irracionales y raíces).
3. **Validar competencia/cursos** marcados "baja certeza" contra el temario DEMRE y los libros.
4. Reconciliar/retirar los YAML gruesos antiguos (`numeros.yaml`, `fundamentos.yaml`, etc.).
