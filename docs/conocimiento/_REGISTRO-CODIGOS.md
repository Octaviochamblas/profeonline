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
| **02.34+** | **Razones, Proporciones, Porcentajes y Matemática Financiera** | — | **⏭️ PRÓXIMO** |

**Próximo código libre en rama 02: `02.34`.**

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
