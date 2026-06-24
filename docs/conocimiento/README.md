# Biblioteca de Conocimiento — Estructura de Matemática

Esqueleto universal de **Matemática preuniversitaria** (Fase 1 del proyecto
[Biblioteca de Conocimiento Estructurada](../backlog/1-por-iniciar/biblioteca-conocimiento-estructurada.md)).

Organizado **por conceptos** (no por curso); los cursos serán *vistas* sobre esta base.
Backbone: texto PAES 9ª ed. (Tomo 1+2); aditivo con Santillana (Aritmética y Álgebra) y
Carreño & Cruz (Álgebra). Índices fuente en `scratch/_indices/`.

## Archivos
- `matematica.yaml` — **índice maestro** (temas + `dificultad`, `prerrequisitos`, `objetivo`, `competencia`).
- Detalle por rama (temas → **recursos**, cada recurso = una lección/video):
  `fundamentos` · `numeros` · `proporcionalidad` · `algebra` · `funciones` · `geometria` ·
  `trigonometria` · `estadistica` · `probabilidad` · `progresiones` · `algebra-lineal`.

## Convenciones y nomenclatura

**Grano atómico** (decisión del 🧑): **1 recurso = 1 idea mínima = 1 video corto.**
Se separa todo "A y B" en recursos distintos (ej. "Adición de fracciones de igual
denominador" es su propio recurso). Objetivo: cubrir el espectro completo con núcleos mínimos.

**Código `RR.TT.rr`** (jerárquico decimal, numérico):

| Nivel | Formato | Ejemplo |
|---|---|---|
| Rama | `RR` (01–11) | `02` = Números |
| Tema | `RR.TT` | `02.08` = Fracciones |
| Recurso | `RR.TT.rr` | `02.08.04` |

**Numeración de las 11 ramas:**
`01` Fundamentos · `02` Números · `03` Proporcionalidad · `04` Álgebra · `05` Funciones ·
`06` Geometría · `07` Trigonometría · `08` Estadística · `09` Probabilidad · `10` Progresiones ·
`11` Álgebra Lineal.

- **Insertar/quitar:** agregar al final = siguiente número; insertar en medio = sub-código
  temporal (`02.08.04.1`) y luego renumerar; quitar = borrar. El `id` semántico estable evita
  romper referencias al renumerar.
- **dificultad:** `basica < media < avanzada`. **competencia:** `M1` (común) | `M2` (específica).
- **id:** identificador semántico estable (`MAT.<RAMA>.<TEMA>`), independiente del código numérico.

## ⏭️ Para continuar (próxima sesión) — handoff

La arquitectura ya está **diseñada y validada**; **solo falta atomizar las ramas 02–11**. Retomar es barato:

1. Leer **este README** + **`fundamentos.yaml`** (★ **la rama 01 es la PLANTILLA DE REFERENCIA**:
   ya está en grano atómico con códigos `RR.TT.rr`) + la tarjeta de backlog
   `../backlog/1-por-iniciar/biblioteca-conocimiento-estructurada.md`.
2. Replicar **ese mismo patrón** en las demás ramas (`numeros.yaml`, `algebra.yaml`, … hoy en grano
   grueso) → atomizar los "A y B" y agregar los códigos `RR.TT.rr`. **No rediseñar nada.**
3. Avanzar **incremental, una rama (o un tema) por vez**, validando con el 🧑.

## Totales (v1)
**11 ramas · 95 temas · 299 recursos.**

| Rama | Temas | Recursos |
|---|--:|--:|
| Fundamentos (lógica/conjuntos) | 3 | 8 |
| Números (Aritmética) | 19 | 66 |
| Proporcionalidad y porcentaje | 7 | 20 |
| Álgebra | 16 | 69 |
| Funciones | 10 | 31 |
| Geometría | 15 | 45 |
| Trigonometría | 7 | 13 |
| Estadística | 5 | 14 |
| Probabilidad | 6 | 14 |
| Progresiones | 4 | 10 |
| Álgebra Lineal (intro) | 3 | 9 |

## Pendiente (fases siguientes)
- **Enriquecer** cada recurso (objetivos múltiples + `conceptos_clave`).
- **4a — Ruta "desde 0":** orden topológico del grafo de prerrequisitos.
- **4b — Vistas de curso:** mapear cada nodo a básica/media (tag de curso).
- Reconciliar `matematica.yaml` (maestro) con los temas nuevos del detalle.
- Mapa de cobertura (Fase 2) + poblamiento de las 4 capas (Fase 3).
