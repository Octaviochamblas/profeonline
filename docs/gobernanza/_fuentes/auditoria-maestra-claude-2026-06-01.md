# Auditoría Maestra del Proceso + Plan Preventivo y Estandarización Multiagente

- **Fecha:** 2026-06-01
- **Autor:** Claude (rol: arquitecto + auditor)
- **Alcance:** Cómo hemos llevado el proceso, riesgos técnicos y de proceso, plan preventivo,
  estandarización de roles (Claude / Antigravity / Codex), carpeta de coordinación y
  automatización del flujo de trabajo.
- **Estado del repo al auditar:** rama `main`, CI verde, producción respondiendo 200.

> Este es el documento "raíz" de gobernanza. Las acciones que de aquí salgan se convierten en
> tarjetas del Kanban (`docs/1 Por iniciar/`). La carpeta de coordinación viva está en
> [`docs/_coordinacion/`](../_coordinacion/README.md).

---

## 1. Resumen ejecutivo

ProfeOnline está **mejor gobernado que el 90 % de los proyectos de su tamaño**. Tienen una
barrera de CI real, disciplina de ramas/PR, un Kanban en `docs/` que de verdad se usa, reportes
de sesión que recuperan contexto, y auditorías que **encuentran bugs antes de producción**
(el `300 %` de estrellas, la regresión de `font-weight`, el `assertContains` que se iba a romper).
Eso es una base sólida y poco común.

Lo que falta para pasar de "ordenado" a **"robusto y a prueba de fallos"** se concentra en cinco
frentes:

1. **No hay entorno de staging** — se audita y se hace QA directo contra producción.
2. **El despliegue corre `migrate` + `seed` en cada arranque sin red de seguridad** (backup/gate).
3. **El rate-limit del webhook es por-worker** si no hay Redis → más débil de lo que parece.
4. **Cobertura de tests sin medir y sin pruebas de frontend/JS** (el select accesible es JS puro).
5. **Coordinación entre agentes informal** → ya hubo colisiones de working tree (pisotones de docs).

El plan preventivo de la §4 ataca exactamente esos cinco frentes, priorizado P0/P1/P2.

---

## 2. Auditoría del proceso (cómo lo hemos llevado)

### 2.1. Lo que está funcionando bien (conservar)

| Práctica | Evidencia | Por qué importa |
| --- | --- | --- |
| **Barrera de CI real** | `django_ci.yml`: `pip-audit` + `check` + `check --deploy` (settings de prod) + suite completa. Railway con *Wait for CI*. | Nada llega a prod sin pasar la misma barrera que se corre local. |
| **Disciplina git** | rama → push → PR → CI verde → squash-merge → borrar rama. Sin commits sueltos a `main`. | Historial limpio, cada cambio revisable y reversible. |
| **Kanban + reportes de sesión** | `docs/1..4`, `git mv` para conservar historial, un reporte por sesión. | Resuelve el problema real de que los agentes no recuerdan sesiones. |
| **Auditoría con dientes** | Se detectaron y corrigieron bugs reales (`300 %` estrellas, `#16a34a` regresivo, test que iba a romper). | La separación "builder construye / auditor verifica" ya rinde frutos. |
| **Hardening de producción** | `DEBUG=False`, HSTS, cookies seguras, `SSL_REDIRECT`, `DATABASE_URL` obligatorio (sin fallback silencioso a SQLite), Sentry con `send_default_pii=False`, SSL a la DB. | Decisiones de seguridad correctas y documentadas con su "por qué". |
| **Webhook defensivo** | `secrets.compare_digest`, guard contra token por defecto, rate-limit, CSP con nonce. | Superficie de entrada externa tratada con cuidado. |
| **Dependabot + pip-audit** | `.github/dependabot.yml` (pip + actions, semanal) y `pip-audit` que rompe CI ante CVE. | Cadena de dependencias vigilada en dos capas. |
| **Modelos desacoplados** | Un archivo por modelo en `apps/content/models/`. | Fácil de auditar y de evitar `models.py` monstruo. |

### 2.2. Debilidades de proceso observadas (corregir)

1. **Colisión de working tree entre agentes.** En el reporte 2026-06-01 quedó registrado:
   *"Antigravity y este agente tocaron el mismo working tree a la vez, causando reversiones
   transitorias de ediciones de docs."* Es el síntoma #1 a estandarizar (ver §5 y §6).
2. **QA manual queda siempre pendiente.** Casi todos los reportes terminan con "QA visual
   logueado pendiente". Se acumula deuda de verificación humana porque no hay un paso forzado.
3. **Auditorías que envejecen.** Las auditorías de accesibilidad (axe) y rendimiento (Lighthouse)
   se cerraron **antes** de construir la UI gamificada → quedaron desfasadas. Ya se creó la tarjeta
   `qa-accesibilidad-rendimiento-ui-gamificada`, pero el patrón "auditar una vez y archivar" deja
   huecos. Las auditorías deben ser **recurrentes**, no de una sola vez (ver §8).
4. **Ramas viejas sin podar.** Hay ramas locales y remotas ya mergeadas (`perf/quick-wins`,
   `refactor/css-design-system`, `a11y/keyboard-screenreader`, `estandarizacion`). Conviene
   borrarlas para que el estado del repo refleje la realidad.
5. **Dos carpetas de auditorías compitiendo.** Existe `docs/3 Finalizados/Auditorías-2026-05-30/`
   y ahora `docs/Auditorias/` (sin tilde, creada por Codex/Antigravity). Hay que unificar el
   criterio de dónde viven las auditorías (propuesta: `docs/Gobernanza/auditorias/`).

---

## 3. Puntos críticos y posibles fallos futuros (auditoría técnica)

Hallazgos ordenados por severidad. Cada uno se convierte en acción en la §4.

### 🔴 Críticos (P0 — atender pronto, pueden causar pérdida de datos o caída)

- **C1 — `migrate` + `seed_math_resources` en cada arranque sin red de seguridad.**
  El *start command* (`Procfile`/`nixpacks.toml`) es
  `migrate && ensure_admin && ensure_site && seed_math_resources && gunicorn`.
  - Riesgo 1: una migración mal hecha se aplica **automáticamente** en prod, sin gate ni backup
    inmediato previo. Si rompe, la app no levanta y posiblemente ya alteró el esquema.
  - Riesgo 2: `seed_math_resources` corre en **cada** boot/redeploy. Hay que garantizar que es
    100 % idempotente (que nunca duplique ni pise datos editados a mano). Si crea/actualiza por
    `get_or_create` está bien; si hace `update` ciego, puede sobrescribir contenido curado.
  - **Mitigación:** verificar idempotencia del seed; confirmar que existe **backup automático
    diario** en la DB gestionada (Railway/Supabase) y **probar una restauración** al menos una vez;
    documentar el procedimiento de rollback de migración.

- **C2 — Sin backups verificados / sin drill de restauración.**
  La economía del proyecto depende de la base de datos (contenido, progreso de alumnos, XP).
  Existe doc archivado `operaciones-backups-logs.md`, pero no hay evidencia reciente de que el
  backup esté activo y, sobre todo, de que una **restauración funcione**. Un backup no probado no
  es un backup.

- **C3 — Rate-limit del webhook es por-proceso si no hay Redis.**
  `apps/content/views/api_video.py` usa `django.core.cache`. En `base.py` **no se define `CACHES`**,
  así que el default es `LocMemCache` (memoria por proceso). Con varios workers de gunicorn, el
  contador de 10 intentos es **por worker** → el límite efectivo es `10 × nº de workers` y se
  pierde en cada redeploy. Producción solo usa cache compartida si `REDIS_URL` está definido.
  - **Mitigación:** definir `REDIS_URL` en producción (y documentarlo como **requisito** del
    webhook), o degradar conscientemente y dejarlo anotado. Sin esto, el rate-limit da una falsa
    sensación de protección.

### 🟠 Altos (P1 — deuda que crecerá y dolerá)

- **A1 — No hay entorno de staging.** Toda la auditoría y el QA visual ocurren contra producción.
  Un *preview deploy* por PR (Railway lo soporta) o un servicio `staging` separado permitiría
  auditar y hacer QA **antes** del merge, no después.

- **A2 — Cobertura de tests sin medir.** ~165 tests en 12 archivos para una app con gamificación,
  evaluación por niveles, evaluación de tema, generación IA y un webhook. No hay umbral de
  cobertura en CI ni se sabe qué rutas críticas quedan sin test. Riesgo de regresión silenciosa.

- **A3 — Cero tests de frontend/JS.** `enhanced-select.js` (el patrón ARIA listbox por teclado)
  y la interactividad HTMX del quiz no tienen pruebas automáticas. Justo lo más frágil (a11y,
  estados de UI) es lo que solo se valida "a ojo" y por eso el QA queda eternamente pendiente.

- **A4 — Render de matemáticas (LaTeX/KaTeX) ausente.** Es un sitio STEM. La propia auditoría de
  gamificación pide explicaciones paso a paso con fórmulas. Sin un renderizador (KaTeX/MathJax),
  la calidad pedagógica del contenido tiene techo. Riesgo de producto, no de caída.

- **A5 — Scaffolding pedagógico no forzado.** Un alumno puede intentar Nivel 3 sin aprobar Nivel 1
  (hallazgo de la auditoría de gamificación). Riesgo de experiencia/retención.

- **A6 — Conexiones a DB y pooler.** `conn_max_age=600` con `sslmode=require`. Si se escala el
  número de workers/replicas y la DB es Supabase, conviene confirmar que se usa el **pooler
  (pgbouncer)** para no agotar conexiones. Hoy con poca carga no duele; al crecer, sí.

### 🟡 Medios (P2 — robustez y mantenibilidad)

- **M1 — Sin staging para correos.** Si `BREVO_API_KEY` está en prod y se prueban flujos de email,
  se mandan correos reales. Conviene un modo de prueba o dominio sandbox.
- **M2 — Sin linter/formatter de Python en CI** (ruff/black). El estilo se mantiene "a mano".
  Un `ruff check` rápido en pre-commit y CI evita discusiones y detecta bugs triviales.
- **M3 — Sin tagging de releases / CHANGELOG.** Las releases son implícitas (squash a `main`).
  Un tag por deploy facilita rollback ("volver al tag v2026.06.01") y trazabilidad con Sentry.
- **M4 — Branch protection no verificada.** Conviene exigir en GitHub: CI verde obligatorio,
  ≥1 review (puede ser el auditor), no push directo a `main`. Hace cumplir el flujo por sistema,
  no por costumbre.
- **M5 — Observabilidad parcial.** Sentry capta errores pero `traces_sample_rate=0` (sin
  performance). No hay panel de métricas de negocio (altas, quizzes aprobados, retención). El
  ledger (`XPEvent`/`QuizAttempt`) ya existe: explotarlo para un dashboard interno es barato.
- **M6 — `requirements.txt` con versiones pinneadas pero sin lock con hashes.** Aceptable hoy;
  un `constraints`/lock con hashes endurece la cadena de suministro.

---

## 4. Plan preventivo (priorizado y accionable)

Cada ítem está pensado para convertirse en una tarjeta del Kanban. Marca quién ejecuta:
🏛️ Claude (arquitecto/auditor), 🔨 Antigravity (builder), 🧩 Codex (apoyo/datos/integraciones),
🧑 Usuario (lo que requiere humano).

### P0 — Esta semana
1. **🧑+🏛️ Verificar backups de la DB y hacer un drill de restauración** (C2). Confirmar backup
   automático diario y restaurar una copia en una DB de prueba. Documentar el procedimiento.
2. **🏛️+🔨 Auditar idempotencia de `seed_math_resources`** (C1). Confirmar que solo usa
   `get_or_create`/`update_or_create` con claves estables y que **no pisa** contenido editado a
   mano. Si hay dudas, sacarlo del start command y correrlo a demanda.
3. **🧑 Definir `REDIS_URL` en producción** (C3) y volver a confirmar que el rate-limit del webhook
   cuenta de forma compartida. Documentarlo como requisito.
4. **🧑 Activar branch protection en GitHub** (M4): CI obligatorio + sin push directo a `main`.

### P1 — Próximas 2–3 semanas
5. **🧑+🏛️ Montar staging** (A1): un servicio `staging` en Railway o *preview deploys* por PR.
   La auditoría y el QA visual pasan a hacerse ahí **antes** del merge.
6. **🔨 Añadir medición de cobertura** (A2): `coverage` en CI, publicar el % y fijar un umbral
   inicial realista (p. ej. no bajar del actual). 🏛️ define qué rutas críticas exigir.
7. **🔨 Smoke tests de frontend** (A3): Playwright headless con 4–6 recorridos críticos (home,
   filtro de recursos con el select accesible por teclado, hacer un quiz, ver progreso de tema).
   Correrlos en CI contra staging.
8. **🔨 Integrar KaTeX** (A4): renderizar `$...$`/`$$...$$` en `content` y en explicaciones de
   `Question`. 🏛️ decide el alcance (¿solo explicaciones o todo el Markdown?).
9. **🔨 Forzar scaffolding** (A5): bloquear Nivel N si no se aprobó N-1 en `quiz` view, con HTML
   de bloqueo claro. 🏛️ revisa el diseño antes de construir.

### P2 — Backlog de robustez
10. **🔨 `ruff` en pre-commit y CI** (M2). Rápido, alto retorno.
11. **🏛️ Tag de release por deploy + CHANGELOG** (M3). Atar el tag al release de Sentry.
12. **🔨+🏛️ Dashboard interno de métricas** (M5) explotando `XPEvent`/`QuizAttempt`.
13. **🧩 Modo sandbox de email** (M1) para no mandar correos reales en pruebas.
14. **🏛️ Confirmar pooler de DB** (A6) antes de escalar workers.
15. **🔨 Lockfile con hashes** (M6) si se quiere endurecer la cadena de suministro.

---

## 5. Estandarización de roles (Claude / Antigravity / Codex)

La división ya existe de hecho; aquí se formaliza para que sea repetible y sin pisotones.

### 5.1. Quién hace qué

| Rol | Agente | Responsabilidad principal | NO hace |
| --- | --- | --- | --- |
| **🏛️ Arquitecto + Auditor** | **Claude** | Diseña el plan (specs, criterios de aceptación), **revisa el plan del builder antes de construir**, audita el diff contra la spec, corre la barrera de CI local, detecta bugs, mergea a `main`, escribe el reporte de sesión. | No es el que produce el grueso del código de features (lo delega al builder). |
| **🔨 Builder** | **Antigravity** | Implementa la spec en una rama propia, mantiene verde la barrera (`test` + `check` + `makemigrations --check`), sube cache-buster del CSS, deja el código listo para auditar. | No mergea a `main`, no cambia alcance sin avisar, no toca el working tree del auditor. |
| **🧩 Apoyo / Integraciones / Datos** | **Codex** | Importación de contenido (playlists de YouTube, webhook de videos), scripts de datos, tareas acotadas de integración, segunda opinión en auditorías. | No mergea a `main`; coordina por la carpeta de coordinación. |
| **🧑 Decisión y QA humano** | **Usuario** | Aprueba PRs, hace QA visual/teclado/NVDA, gestiona secretos y servicios (Railway, DNS, Brevo), decide producto. | — |

### 5.2. Flujo estándar de una tarea (el "happy path")

```
🏛️ Claude            🔨 Antigravity         🧑 Usuario
   │                     │                     │
   │ 1. Spec + criterios │                     │
   │    de aceptación    │                     │
   │  → handoff en       │                     │
   │    _coordinacion/   │                     │
   │─────────────────────▶                     │
   │                     │ 2. Propone plan     │
   │ 3. Revisa el plan   │    (antes de codear)│
   │    contra el código │◀────────────────────│
   │    (✋ corrige aquí) │                     │
   │─────────────────────▶ 4. Implementa en    │
   │                     │    rama propia +     │
   │                     │    barrera verde     │
   │ 5. Audita diff vs.  │◀──── PR ─────────────│
   │    spec + CI local  │                     │
   │    (corrige bugs)   │                     │
   │─────────────────────────────────────────▶ 6. QA visual / aprueba
   │ 7. Squash-merge a   │                     │
   │    main → deploy    │                     │
   │ 8. Reporte sesión   │                     │
```

**Regla de oro contra pisotones:** *un solo agente escribe en el working tree a la vez*.
Si dos necesitan trabajar en paralelo, **cada uno en su propia rama/worktree**. El estado de quién
tiene "el lápiz" se declara en `docs/_coordinacion/ESTADO.md` (§6).

### 5.3. Criterios de aceptación de un handoff (definición de "listo para auditar")

- Los 3 comandos de la barrera en verde: `test`, `check`, `makemigrations --check --dry-run`.
- Si tocó CSS: cache-buster `?v=N` subido.
- Diff acotado a la spec (nada de más).
- Doc de `2 En Proceso/` con su sección "Qué se hizo" completada.
- Nota en `_coordinacion/` de que el PR está listo y en qué rama.

---

## 6. Carpeta de coordinación entre agentes (`docs/_coordinacion/`)

El problema real a resolver: los agentes no comparten memoria y **ya colisionaron** editando el
mismo árbol. La solución es un "bus" de coordinación basado en archivos versionados (todos los
agentes ya saben leer/escribir archivos y usar git). Se crea junto con este documento:

```
docs/_coordinacion/
├── README.md         ← reglas del bus (leer SIEMPRE al iniciar sesión)
├── ESTADO.md         ← estado vivo: quién trabaja, en qué rama, quién tiene "el lápiz" (lock)
├── handoffs/         ← briefs arquitecto→builder (specs accionables)
│   └── _plantilla-handoff.md
└── bitacora/         ← log append-only de eventos entre agentes (decisiones, bloqueos, entregas)
    └── _plantilla-entrada.md
```

**Cómo se usa (protocolo mínimo):**
1. **Al iniciar sesión**, cualquier agente lee `_coordinacion/ESTADO.md` y el último reporte de
   `docs/4 Reportes por Sesión/`.
2. **Antes de tocar el working tree**, el agente declara el lock en `ESTADO.md` (su nombre, la
   rama y la hora). Si el lock ya está tomado por otro agente en la **misma rama**, espera o usa
   otra rama.
3. **El arquitecto deja la spec** como un archivo en `handoffs/` (basado en la plantilla). El
   builder responde en ese mismo archivo con su plan y, al terminar, con el enlace al PR.
4. **Eventos importantes** (decisión, bloqueo, entrega, bug encontrado) → una línea en
   `bitacora/AAAA-MM-DD.md`. Es append-only: nadie reescribe lo de otro.
5. **Al cerrar**, se libera el lock en `ESTADO.md` y se escribe el reporte de sesión normal.

> Nota: esto **no reemplaza** al Kanban ni a los reportes de sesión. El Kanban es el *qué*
> (tareas), los reportes son la *memoria histórica*, y `_coordinacion/` es el *canal en vivo*
> entre agentes durante el trabajo.

---

## 7. Automatización máxima del flujo

Objetivo: que la barrera y la verificación las haga la máquina, y que los agentes solo decidan y
construyan. Orden por relación esfuerzo/retorno.

### 7.1. En GitHub Actions (ya hay base sólida con `django_ci.yml`)
- **Branch protection** que exija el job de CI (hace el flujo obligatorio por sistema). *(P0-#4)*
- **Job de cobertura** que comente el % en el PR. *(P1-#6)*
- **Smoke E2E (Playwright)** contra staging en cada PR. *(P1-#7)*
- **Auditoría programada (cron semanal):** Lighthouse CI + axe-core contra producción/staging,
  que abra un issue si baja de umbral. Resuelve el problema de "auditorías que envejecen" (§2.2).
- **`ruff`** como step rápido. *(P2-#10)*
- **Plantillas de PR e issues** (`.github/PULL_REQUEST_TEMPLATE.md`) con el checklist de la §5.3,
  para que el builder no olvide la barrera ni el cache-buster.
- **Tag automático de release** al mergear a `main`, atado al release de Sentry. *(P2-#11)*

### 7.2. Con las herramientas de Claude Code (lado auditor)
- **`/code-review`** sobre el diff de cada rama del builder antes de aprobar (lo hace Claude).
- **`/security-review`** en cambios que toquen el webhook, settings, allauth o permisos.
- **`/loop`** o **routines programadas** para tareas recurrentes (p. ej. revisar PRs de Dependabot,
  o correr el smoke nightly y reportar). Útil para no depender de que alguien se acuerde.
- **Sentry MCP** ya disponible: el auditor puede triagear issues de producción directo desde la
  sesión y abrir la tarjeta correspondiente.

### 7.3. Integraciones de contenido (lado Codex)
- El **webhook de videos** y el comando `import_youtube_resources` ya existen. Automatizar:
  al publicar un video → Codex llama al webhook → recurso creado como **borrador** (`is_published:
  false`) → el usuario revisa y publica. Mantener el borrador-por-defecto evita publicar contenido
  sin curar.
- **Idempotencia y rate-limit** del webhook deben quedar sólidos (C1/C3) antes de subir el volumen.

### 7.4. Pre-commit (mantener rápido, ampliar con criterio)
- Hoy: `check` + `makemigrations --check` (bien, rápido a propósito).
- Añadir solo cosas baratas: `ruff` y los hooks de higiene ya presentes. **No** meter la suite
  completa aquí (eso es trabajo de CI) para no desincentivar commits.

---

## 8. Catálogo de auditorías recurrentes (qué auditar y cada cuánto)

El antídoto contra "auditar una vez y archivar". Cadencia sugerida:

| Auditoría | Cadencia | Cómo | Responsable |
| --- | --- | --- | --- |
| **Seguridad de dependencias** | Continua | `pip-audit` en CI + Dependabot semanal (ya activo) | 🤖 automático / 🏛️ revisa PRs |
| **`check --deploy`** | Cada PR | Ya en CI | 🤖 automático |
| **Accesibilidad (axe + teclado)** | Mensual + tras cada cambio grande de UI | axe-core en CI nightly; teclado/NVDA por el usuario | 🤖 + 🧑 |
| **Rendimiento (Lighthouse/CWV)** | Mensual | Lighthouse CI cron contra prod | 🤖 + 🏛️ |
| **Seguridad de superficie externa** (webhook, allauth, permisos) | Cada cambio relevante | `/security-review` | 🏛️ |
| **Backups / restauración** | Trimestral | Drill de restore documentado | 🧑 + 🏛️ |
| **Rotación de secretos** | Semestral | Inventario + rotación (API_SECRET_TOKEN, BREVO, Google) | 🧑 |
| **Cobertura de tests** | Cada PR | `coverage` en CI | 🤖 |
| **UX/gamificación vs. referentes** | Semestral | Tipo el reporte de gamificación-malla | 🏛️/🧩 |
| **Revisión de migraciones** | Cada migración | Diff + plan de rollback antes de mergear | 🏛️ |

---

## 9. Inventario de secretos (para la rotación de §8)

Mantener este inventario actualizado (no los valores, solo qué existe y dónde):

| Secreto | Uso | Dónde vive | Última rotación |
| --- | --- | --- | --- |
| `DJANGO_SECRET_KEY` | Firma de sesiones/CSRF | Railway env | — |
| `DATABASE_URL` | Conexión DB (obligatorio) | Railway env | — |
| `API_SECRET_TOKEN` | Auth del webhook de videos | Railway env | — |
| `BREVO_API_KEY` | Envío de correo (API HTTP) | Railway env | 2026-05-30 |
| `GOOGLE_CLIENT_ID` / `_SECRET` | Login con Google (allauth) | Railway env | — |
| `SENTRY_DSN` | Monitoreo de errores | Railway env | — |
| `YOUTUBE_API_KEY` | Importación de playlists | Railway env | — |
| `REDIS_URL` | Cache/rate-limit compartido (pendiente, C3) | Railway env | — |

---

## 10. Próximos pasos concretos (de este documento a la acción)

1. **Crear tarjetas en `docs/1 Por iniciar/`** para los P0 y P1 de la §4 (una por ítem, con la
   plantilla). Sugerencia de nombres:
   - `infra-backups-y-drill-restauracion.md` (C2)
   - `infra-seed-idempotente-y-gate-migraciones.md` (C1)
   - `infra-redis-rate-limit-webhook.md` (C3)
   - `infra-staging-y-preview-deploys.md` (A1)
   - `test-cobertura-y-smoke-frontend.md` (A2+A3)
   - `feat-katex-render-matematicas.md` (A4)
   - `feat-scaffolding-bloqueo-niveles.md` (A5)
2. **Crear y poblar `docs/_coordinacion/`** (hecho junto a este doc) y adoptar el protocolo de lock.
3. **Activar branch protection** y **definir `REDIS_URL`** (acciones del usuario).
4. **Podar ramas mergeadas** y unificar las carpetas de auditorías bajo `docs/Gobernanza/`.
5. **Revisar este documento cada trimestre** y actualizar el inventario de secretos y el catálogo
   de auditorías.

---

### Anexo — Checklists rápidos

**Pre-PR (builder):**
- [ ] `manage.py test` verde · `check` verde · `makemigrations --check --dry-run` sin cambios
- [ ] Si tocó CSS → `?v=N` subido
- [ ] Diff acotado a la spec, sin cambios de más
- [ ] Doc de `2 En Proceso/` con "Qué se hizo" completado
- [ ] Lock liberado en `_coordinacion/ESTADO.md` + nota de PR listo

**Pre-deploy / merge (auditor):**
- [ ] CI del PR verde
- [ ] Diff contrasta fielmente con la spec/handoff
- [ ] `/code-review` (y `/security-review` si toca superficie sensible) sin hallazgos abiertos
- [ ] Migraciones revisadas + plan de rollback si aplica

**Post-deploy:**
- [ ] CI de `main` verde → Railway desplegó (Wait for CI)
- [ ] Smoke en prod (rutas clave responden 200)
- [ ] QA visual logueado de lo nuevo
- [ ] Reporte de sesión escrito
