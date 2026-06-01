# Roadmap priorizado — carteras, prioridades y fases

> Documento **canónico** (Capa 1). Sustituye las listas P0–P3 dispersas en los 3 docs-estrategia.
> Insumos originales en [`_fuentes/`](_fuentes/). Última revisión: 2026-06-01.
>
> **Regla de oro:** ninguna feature grande de producto antes de cerrar la cartera de
> **Continuidad operacional (P0)**. Cada ítem P0/P1 debe existir como **tarjeta** en
> [`../backlog/1-por-iniciar/`](../backlog/1-por-iniciar/), no solo aquí.

## 1. Las 5 carteras

El proyecto no es una lista larga: son **5 carteras** con riesgos y métricas propias.

| Cartera | Objetivo | Ejemplos |
| --- | --- | --- |
| **Continuidad operacional** | Evitar caída, pérdida de datos o deploy inseguro | Backups+restore, seed idempotente, Redis, branch protection, staging |
| **Calidad de ingeniería** | Reducir regresiones y fricción de mantenimiento | Coverage, smoke Playwright, ruff, release tags, PR template |
| **Calidad educativa STEM** | Mejorar el aprendizaje real | KaTeX, scaffolding por prerrequisitos, feedback por distractor, skill tree |
| **Conversión y confianza** | Convertir visitantes en alumnos/contactos | Analytics fase 1, home de confianza, WhatsApp, verificación email |
| **Retención y gamificación** | Aumentar hábito y retorno | Rachas + notificaciones, dashboard, leaderboards |

## 2. Prioridades

### 🔴 P0 — Crítico (protege datos, deploy y control del repo)
| Iniciativa | Por qué | Evidencia de cierre | Dueño |
| --- | --- | --- | --- |
| Backups + drill de restauración | Sin restore probado, contenido y progreso en riesgo | Restore documentado en entorno de prueba | 🧑+🏛️ |
| Idempotencia de `seed_math_resources` | Corre en cada deploy; si pisa/duplica, daño silencioso | Auditoría del comando + reglas de no-sobrescritura | 🏛️+🔨 |
| `REDIS_URL` para rate-limit compartido | Sin cache compartida, el límite por worker da falsa seguridad | Prod usando Redis + prueba de contador compartido | 🧑 |
| Branch protection en GitHub | Hace obligatorio el flujo que hoy depende de disciplina | `main` exige CI verde + review | 🧑 |
| Tarjetas P0 explícitas | La estrategia sin tarjeta no se ejecuta | P0 creados en `backlog/1-por-iniciar/` | 🏛️ |

### 🟠 P1 — Necesario (calidad real del producto y menos regresiones)
| Iniciativa | Comentario | Orden |
| --- | --- | --- |
| Staging / preview deploys | Desbloquea QA serio antes de producción | **Primero** |
| QA accesibilidad/rendimiento UI gamificada | Ya hay tarjeta; cubre deuda concreta | Tras staging |
| Coverage + smoke tests Playwright | La suite Django no cubre JS/HTMX ni flujos críticos | Tras staging |
| KaTeX | STEM sin fórmulas renderizadas tiene techo pedagógico | Antes de expandir contenido científico |
| Scaffolding por prerrequisitos | Gamificación que enseña en secuencia, no premia clicks | Tras estabilizar tests |
| Verificación de email | Bajo riesgo (Brevo ya funciona) | Puede ir en paralelo |
| Analytics fase 1 | Definir eventos **antes** de rediseñar el home | Antes del rediseño |

### 🟡 P2 — Recomendado (eficiencia, observabilidad, producto)
Dashboard interno con `XPEvent`/`QuizAttempt` · Rachas visibles + notificaciones Brevo ·
`ruff` en pre-commit y CI · Release tags + changelog · Home de confianza (bloqueado por contenido
real + medición) · Confirmar pooler de DB antes de escalar workers.

### 🟢 P3 — Opcional (tras consolidar medición, staging y base pedagógica)
Skill tree visual avanzado · Pizarra/canvas en quizzes · Leaderboards/ligas · Feedback por
distractor avanzado.

## 3. Secuencia por fases

1. **Semana 1:** crear tarjetas P0, branch protection, verificar backups, auditar seed, definir Redis.
2. **Semanas 2–3:** staging/preview deploys, QA UI gamificada, coverage inicial, smoke tests.
3. **Mes 1:** verificación email, analytics fase 1, KaTeX acotado.
4. **Mes 2:** scaffolding de niveles, dashboard interno mínimo, preparar home con contenido real.
5. **Después:** skill tree, rachas avanzadas, notificaciones, canvas o ligas según datos de uso.

## 4. Regla de decisión para ideas nuevas

Clasificar **antes** de construir:
- **Crítico (P0):** evita pérdida de datos, caída, bypass de seguridad o deploy roto.
- **Necesario (P1):** sostiene aprendizaje, conversión, QA o una operación frecuente.
- **Recomendado (P2):** mejora eficiencia/retención/mantenibilidad sin bloquear lo anterior.
- **Opcional (P3):** diferenciación que puede esperar sin aumentar riesgo.

> Si una idea no tiene **métrica, dueño, criterio de aceptación y evidencia de cierre**, todavía no
> está lista para construcción.
