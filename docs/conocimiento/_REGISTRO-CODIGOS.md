# Registro de códigos — Biblioteca de Conocimiento

> Para que cualquier sesión (humano o IA) sepa **desde qué código seguir** sin recordar nada.
> Cada bloque se entrega como **archivo YAML separado** (regla permanente). Los `cod` no se
> reutilizan ni renumeran; el `id` semántico es la llave estable. Estándar completo: ver
> memoria `biblioteca-conocimiento-estandar.md` y `README.md`.

## Estándar en una línea
`RR.TT.rr` (rama.tema.recurso). Recurso: `id MAT.<ABREV>.<TEMA>.<SLUG>` (el id empieza con el id
del tema). 3 ejes por recurso: `competencia` (M1|M2|U), `dificultad` (basica|media|avanzada),
`cursos` ([1B..8B, 1M..4M]). Atomización máxima. `prerrequisitos` → pasada final (aún no).

## Rama 02 — NÚMEROS (abrev. NUM)

| Códigos | Bloque | Archivo | Estado |
|---|---|---|---|
| 02.01–02.02 | Enteros (conjunto/orden + operatoria) | `numeros-enteros.yaml` | ✅ guardado |
| 02.03–02.08 | Teoría de Números (divisibilidad, primos, factorización, m.c.m., M.C.D., aplicaciones) | `numeros-teoria-de-numeros.yaml` | ✅ guardado |
| 02.09–02.21 | Números Racionales (Q, fracciones, decimales, aproximaciones, error) | `numeros-racionales.yaml` | ✅ guardado |
| 02.22–02.33 | Reales, Potencias, Notación científica, Raíces, Racionalización, Logaritmos, Imaginarios, Complejos | `numeros-reales-potencias-raices-logaritmos.yaml` | ✅ guardado |
| 02.34–02.44 | Razones, Proporciones, Porcentajes, Finanzas, Interés simple y compuesto | `numeros-razones-porcentajes-finanzas.yaml` | ✅ guardado |

**Rama 02 NÚMEROS COMPLETA (02.01–02.44).**

## Rama 03 — ÁLGEBRA Y FUNCIONES (abrev. ALG)  · se trabaja sub-tema por sub-tema

| Códigos | Bloque | Archivo | Estado |
|---|---|---|---|
| 03.01–03.05 | Nomenclatura y conceptos básicos | `algebra-nomenclatura-conceptos.yaml` | ✅ guardado |
| 03.06–03.08 | Lenguaje algebraico y valorización | `algebra-lenguaje-valorizacion.yaml` | ✅ guardado |
| 03.09–03.13 | Operaciones con expresiones algebraicas | `algebra-operaciones.yaml` | ✅ guardado |
| 03.14–03.17 | Multiplicación algebraica | `algebra-multiplicacion.yaml` | ✅ guardado |
| 03.18–03.23 | Productos notables | `algebra-productos-notables.yaml` | ✅ guardado |
| 03.24–03.29 | Factorización | `algebra-factorizacion.yaml` | ✅ guardado |
| 03.30–03.37 | M.C.D., m.c.m. y fracciones algebraicas | `algebra-mcd-mcm-fracciones.yaml` | ✅ guardado |
| 03.38–03.44 | Ecuaciones de primer grado y sistemas | `algebra-ecuaciones-sistemas.yaml` | ✅ guardado |
| 03.45–03.51 | Desigualdades e inecuaciones | `algebra-inecuaciones.yaml` | ✅ guardado |
| 03.52–03.60 | Funciones | `algebra-funciones.yaml` | ✅ guardado |

**Rama 03 ÁLGEBRA Y FUNCIONES COMPLETA (03.01–03.60).** Siguiente: **rama 04 GEOMETRÍA, empieza en `04.01`.**

## Rama 01 — FUNDAMENTOS (abrev. FUND)
Versión atómica (12 temas `01.01`–`01.12`: lógica básica, conectivos, tablas de verdad,
razonamiento lógico, cuantificadores, conjuntos básicos, relaciones, diagramas de Venn,
operaciones, propiedades, cardinalidad, producto cartesiano) en `fundamentos-atomico.yaml` ✅.
El `fundamentos.yaml` que está en el repo es la versión **gruesa antigua** (a reemplazar en la
pasada de reconciliación).

## Ramas pendientes
- **03 ÁLGEBRA y Funciones** (ALG) — reinicia en `03.01`.
- **04 GEOMETRÍA** (GEO) — reinicia en `04.01`.
- **05 PROBABILIDAD y ESTADÍSTICA** (EST) — reinicia en `05.01`.

## Pasadas pendientes (post-esqueleto)
1. **Grafo de prerrequisitos** (`prerrequisitos: [id,...]`) sobre los `id` ya existentes — DAG,
   validar que cada id exista y que no haya ciclos.
2. **Anti-duplicado:** resolver recursos repetidos (ej. `INVERSO_MULTIPLICATIVO` en operatoria y
   propiedades de Q; `RAIZ_NO_EXACTA` en irracionales y raíces).
3. **Validar competencia/cursos** marcados "baja certeza" contra el temario DEMRE y los libros.
4. Reconciliar/retirar los YAML gruesos antiguos (`numeros.yaml`, `fundamentos.yaml`, etc.).
