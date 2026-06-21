# Poblado del banco de Lenguaje Algebraico — 21 de junio de 2026

- **Autor/agente:** Codex.
- **Alcance:** los 17 recursos del tema `lenguaje-algebraico`.
- **Estado:** superada por la revisión v2 aplicada en producción el 21 de junio
  de 2026; se conserva como evidencia del primer poblado.

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

## Revisión v2 aplicada

Tras comparar el banco inicial con cinco preguntas editoriales más concretas, se
detectó que varias preguntas v1 eran correctas pero demasiado genéricas. Se creó
un paquete v2 y se revisó antes de publicarlo mediante un HTML local navegable.

Resultado del reemplazo:

- preguntas v2 publicadas: **1.530**;
- preguntas anteriores archivadas: **1.535**;
- respuestas históricas preservadas: **5**;
- recursos completos: **17/17**;
- preguntas v2 con trazabilidad: **1.530**;
- alternativas inválidas: **0**;
- explicaciones vacías: **0**;
- duplicados literales dentro de cada recurso: **0**.

Las cinco preguntas editoriales usadas como referencia fueron incorporadas al
paquete v2; la mención ambigua “mínimo común denominador (MCD)” se corrigió a
“mínimo común denominador”.

Herramientas:

- `scratch/build_lenguaje_algebraico_review_v2.py`: genera el paquete de revisión
  sin tocar producción.
- `scratch/apply_lenguaje_algebraico_review_v2.py`: valida hashes, respalda,
  archiva el banco anterior y publica el paquete aprobado en una transacción.

Respaldo v2:
`backups/lenguaje_algebraico_before_v2_20260621T043147Z.json`
(archivo local no versionado).
