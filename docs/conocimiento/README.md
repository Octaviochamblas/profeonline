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

## Convenciones
- **id:** `MAT.<RAMA>.<TEMA>` (estable). Recursos: `Tema.NN`.
- **dificultad:** rango `[min, max]` sobre `basica < media < avanzada`.
- **competencia:** `M1` (núcleo PAES / común) | `M2` (electiva / específica). *Tags preliminares.*
- **prerrequisitos:** grafo de aprendizaje (habilita la ruta "desde 0").

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
