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

**Eje 03 ÁLGEBRA Y FUNCIONES COMPLETO (03.01–03.10).** Siguiente bloque: `03.11` (libre).

---

## Eje 04 — GEOMETRÍA (abrev. GEO)

| Bloque | Código BB | Temas | Archivo | Estado |
|--------|-----------|-------|---------|--------|
| Ángulos: Fundamentos y Relaciones | 04.01 | 04.01.01–04.01.07 | `geometria-angulos.yaml` | ✅ guardado |

**Siguiente bloque en eje 04:** `04.02` (Triángulos: Propiedades y Clasificación).

---

## Ejes pendientes

- **05 PROBABILIDAD y ESTADÍSTICA** (EST) — empieza en `05.01.01`.

## Pasadas pendientes (post-esqueleto)

1. **Grafo de prerrequisitos** (`prerrequisitos: [id,...]`) sobre los `id` ya existentes — DAG,
   validar que cada id exista y que no haya ciclos.
2. **Anti-duplicado:** resolver recursos repetidos (ej. `INVERSO_MULTIPLICATIVO` en operatoria y
   propiedades de Q; `RAIZ_NO_EXACTA` en irracionales y raíces).
3. **Validar competencia/cursos** marcados "baja certeza" contra el temario DEMRE y los libros.
4. Reconciliar/retirar los YAML gruesos antiguos (`numeros.yaml`, `fundamentos.yaml`, etc.).
