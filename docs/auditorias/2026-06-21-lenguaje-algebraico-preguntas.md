# Poblado del banco de Lenguaje Algebraico — 21 de junio de 2026

- **Autor/agente:** Codex.
- **Alcance:** los 17 recursos del tema `lenguaje-algebraico`.
- **Estado:** vigente y aplicado en producción.

## Resultado

- Recursos poblados: **17**.
- Preguntas publicadas: **1.530**.
- Alternativas: **6.120**.
- Preguntas por recurso: **90**.
- Distribución por recurso y nivel: 10 `preparacion`, 10 `evaluacion` y
  10 `ambas`.
- Pool efectivo: 20 preguntas de preparación y 20 de evaluación por nivel.
- Recursos con cobertura completa: **17/17**.
- Preguntas duplicadas literalmente: **0**.
- Explicaciones vacías: **0**.
- Preguntas sin cuatro alternativas o sin una única correcta: **0**.
- Orden visible verificado:
  `1.x → 2.x → 3.x → 4.01 → 4.01a → 4.02 → 4.03 → 4.04`.

## Criterio pedagógico

- Nivel 1: conceptos, reglas, estructura y errores frecuentes.
- Nivel 2: cálculo y procedimiento mediante seis familias de tarea:
  resolución, justificación, comparación, corrección de error, evaluación de
  afirmación y selección de estrategia.
- Nivel 3: aplicación, validación de soluciones y análisis de procedimientos.
- Cada pregunta registra trazabilidad a la transcripción mediante su hash.

## Seguridad y reproducibilidad

El generador vive en `scratch/populate_lenguaje_algebraico_questions.py`.
Su modo predeterminado es dry-run; la escritura exige confirmación explícita,
crea un respaldo y aborta si detecta preguntas preexistentes. La publicación se
realiza dentro de una transacción y usa inserciones masivas.

El tema quedó configurado con `resource_ordering_method="manual"` y usa los
valores `Resource.order` existentes. Esto evita que el orden alfabético muestre
`4.01a` antes de `4.01`.

Respaldo previo:
`backups/lenguaje_algebraico_before_20260621T033745Z.json` (archivo local no versionado).
