# 🧭 ProfeOnline — Índice maestro de documentación

> **Empieza aquí.** Este archivo es el mapa. Te da el contexto del proyecto en una pantalla y te
> dice **qué leer según lo que vengas a hacer**, sin tener que leerlo todo.

## ¿Qué es ProfeOnline?

Plataforma educativa STEM (Matemática, Física, Química) en **Django**. Ofrece recursos en video
con apuntes, evaluación gamificada por niveles (Conceptos → Ejercicios → Problemas), progreso por
tema, XP, rachas y destrezas. Producción en **Railway**, dominio `profeonline.cl`.

### Snapshot técnico (para orientarte rápido)

| Tema | Valor |
| --- | --- |
| Framework | Django 6.0.5 · Python 3.12 |
| Settings | `config.settings.local` (dev, default) · `config.settings.production` (prod) |
| Apps | `apps/content` (modelos/vistas/lógica) · `apps/core` (middleware, email, CSP) |
| Base de datos | PostgreSQL (`DATABASE_URL` obligatorio; sin fallback a SQLite) |
| Deploy | push a `main` → Railway (con *Wait for CI*). Arranque: `migrate && ensure_admin && ensure_site && gunicorn` (el seed ya **no** corre en cada boot, C1) |
| Barrera CI | `pip-audit` + `check` + `check --deploy` + suite completa (~165 tests) |
| Email | API HTTP de Brevo · Errores | Sentry · Login | allauth + Google · CSP con nonce |

Detalle operacional completo → [`gobernanza/inventario-operacional.md`](gobernanza/inventario-operacional.md).

---

## 🧱 Documentación por capas (de lo general a lo profundo)

La documentación está ordenada en **4 capas**. Lees de arriba hacia abajo **solo hasta donde tu
tarea lo exige**. Cada capa apunta a la siguiente.

| Capa | Responde | Dónde vive |
| --- | --- | --- |
| **0 · Orientación** | "¿Qué es esto y dónde miro?" | **este `README.md`** |
| **1 · Reglas vigentes** (*el cómo*) | "¿Cómo trabajamos y hacia dónde vamos?" | [`gobernanza/`](gobernanza/) |
| **2 · Trabajo vivo** (*el qué, ahora*) | "¿En qué se trabaja y quién tiene el lápiz?" | [`backlog/`](backlog/) + [`_coordinacion/`](_coordinacion/) |
| **3 · Memoria y evidencia** (*el qué pasó*) | "¿Qué se hizo y qué auditamos?" | [`reportes-sesion/`](reportes-sesion/) · [`auditorias/`](auditorias/) · [`_archivo/`](_archivo/) |

---

## 🗺️ Mapa de lectura — "si vienes a hacer X, lee Y"

| Si vienes a… | Lee (en orden) |
| --- | --- |
| **Iniciar una sesión cualquiera** | 1) `_coordinacion/ESTADO.md` · 2) último de `reportes-sesion/` · 3) la tarjeta activa |
| **Entender el flujo de trabajo / roles** | `gobernanza/proceso-multiagente.md` |
| **Saber qué construir y con qué prioridad** | `gobernanza/roadmap-priorizado.md` |
| **Conocer riesgos técnicos y su mitigación** | `gobernanza/matriz-riesgos.md` |
| **Operar/desplegar/rotar secretos** | `gobernanza/inventario-operacional.md` |
| **Entender la automatización (CI, auto-merge, gate IA)** | `gobernanza/automatizacion-flujo.md` |
| **Construir una feature (builder)** | el handoff en `_coordinacion/handoffs/` + la tarjeta en `backlog/3-construccion/` |
| **Auditar un cambio** | el handoff de la tarea + `gobernanza/matriz-riesgos.md` |
| **Tomar/registrar una decisión de arquitectura** | `gobernanza/decisiones/` (ADRs) |
| **Hacer una auditoría recurrente** | `auditorias/README.md` (qué y cada cuánto) |

### 💸 Protocolo barato de lectura (NO leer todo)

Al iniciar sesión, lee **solo**: este `README.md` → `_coordinacion/ESTADO.md` → último reporte de
`reportes-sesion/` → la tarjeta activa → las rutas que esa tarjeta cite. **Nunca "leer todos los
documentos"** salvo que el usuario pida una auditoría global. Leer de más dispara tokens y ruido.

---

## 📁 Mapa de carpetas

```
docs/
├── README.md                  ← este índice (Capa 0)
│
├── gobernanza/                ← Capa 1: reglas vigentes (canónico, pocos docs)
│   ├── proceso-multiagente.md     · roles, flujo con gates, locks, DoR/DoD
│   ├── roadmap-priorizado.md      · carteras + P0..P3 + secuencia por fases
│   ├── matriz-riesgos.md          · riesgos técnicos + mitigación + dueño
│   ├── inventario-operacional.md  · secretos, servicios, env vars, deploy, cadencia
│   ├── decisiones/                · ADRs (decisiones duraderas)
│   └── _fuentes/                  · insumos históricos (auditorías-estrategia originales)
│
├── backlog/                   ← Capa 2: Kanban-pipeline (cada etapa = dueño activo)
│   ├── 1-por-iniciar/         · backlog de ideas
│   ├── 2-arquitectura/        · 🏛️ Claude (handoff + criterios)
│   ├── 3-construccion/        · 🔨 Antigravity (implementa)
│   ├── 4-auditoria/           · 🧩 Codex (audita el diff)
│   ├── 5-cierre/              · 🏛️ Claude (auditoría final + merge)
│   └── 6-finalizados/         · terminadas
│
├── _coordinacion/            ← Capa 2: canal vivo entre IAs (locks, handoffs, bitácora)
│
├── reportes-sesion/          ← Capa 3: memoria cronológica (AAAA-MM-DD.md)
├── auditorias/               ← Capa 3: auditorías recurrentes (por fecha y alcance)
└── _archivo/                 ← Capa 3: histórico congelado
```

## Roles en una línea
🏛️ **Claude** = arquitecto + cierre · 🔨 **Antigravity** = builder · 🧩 **Codex** = auditor
(preflight + construcción) · 🧑 **Usuario** = decide y hace QA humano.
Detalle → [`gobernanza/proceso-multiagente.md`](gobernanza/proceso-multiagente.md).

## Reglas de oro
1. **Un solo agente escribe en una rama a la vez** (lock en `_coordinacion/ESTADO.md`).
2. **Mover archivos siempre con `git mv`** (conserva historial).
3. **Rutas relativas** dentro del repo (portables); nada de `file:///` en docs versionados.
4. **No mezclar capas**: una tarjeta es futuro a implementar; un reporte es lo que pasó; una regla
   vigente vive en `gobernanza/`. Si algo envejece, va a `_archivo/`.
