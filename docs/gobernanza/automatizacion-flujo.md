# Automatización del flujo multiagente

> Documento **canónico** (Capa 1). Cómo el flujo entre Claude, Antigravity y Codex se mueve
> **solo** vía GitHub, con auto-merge y un gate de auditoría IA. Última revisión: 2026-06-02.

## Idea central

**GitHub es el router; tú solo apareces en las decisiones que un humano debe tomar.**
Todo lo mecánico (rutear, vigilar CI, auto-mergear, etiquetar, digest) corre en **GitHub Actions
sin consumir tokens de IA**. La IA solo actúa en los puntos de juicio (auditar, firmar seguridad).

> ⚠️ **Fase actual = construcción, sin alumnos registrados.** Por eso la autonomía es alta
> (auto-merge en verde). Antes de registrar usuarios reales, ejecutar el **gate de go-live** (§6).

## 1. El recorrido de un PR (sin ti)

1. Una IA abre un PR desde su rama (`feat/*`, `fix/*`, `docs/*`).
2. **CI** corre (`test (3.12)` = barrera real) + `lint` (ruff) + coverage (reporte).
3. **`audit-gate`** (check requerido) evalúa:
   - PR **solo `docs/`** o de **Dependabot** → auto-aprobado.
   - En otro caso → exige el label **`audit:aprobado`**, que añade **una IA distinta a la que
     construyó** (Codex audita lo de Antigravity; Claude audita lo de Codex; o tú con 1 clic).
4. **Auto-merge** (`.github/workflows/auto-merge.yml`) ya está activado en el PR → cuando
   **todos** los checks requeridos pasan, GitHub hace `squash-merge` y **borra la rama** solo.
5. Railway despliega (con *Wait for CI*).
6. La IA dueña mueve su tarjeta del Kanban a `backlog/6-finalizados/` (parte de su PR de cierre).

## 2. Checks requeridos para mergear `main`

| Check | Qué garantiza | Bloquea merge |
| --- | --- | --- |
| `test (3.12)` | Suite Django + `check --deploy` + `pip-audit` | ✅ |
| `audit-gate` | Revisó una 2ª IA (o es docs/deps) | ✅ |
| `lint` (ruff) | Estilo Python | ❌ (reporte por ahora) |

Branch protection en `main`: requiere esos checks, sin push directo. `enforce_admins=false` → el
usuario conserva un **escape de emergencia** (puede mergear/forzar si algo se traba).

## 3. La barrera que NO se quita: revisión de una 2ª IA

Auto-merge en verde es ideal para velocidad, pero hay un modo de fallo real: **si la misma IA
escribe el código y sus tests, “CI verde” solo dice “hace lo que la IA creyó”.** Por eso el
`audit-gate` exige que **otra** IA ponga `audit:aprobado` en cambios de código. Sigue siendo
“tú no haces nada”, pero nunca es una sola IA sin control.

Quién pone `audit:aprobado`:
- **Codex** (auditor) tras revisar tests, N+1, migraciones, diff vs. handoff.
- **Claude** (cierre) si toca seguridad/arquitectura.
- **Tú**, con un clic, si ninguna IA está disponible (igual te ahorras todo lo demás).

## 4. Etiquetas (estado del pipeline en el PR)

| Label | Significado | Quién lo pone |
| --- | --- | --- |
| `etapa:construccion` / `:auditoria` / `:cierre` | Fase viva del PR | la IA dueña |
| `audit:aprobado` | 2ª IA revisó → habilita auto-merge | Codex / Claude / usuario |
| `seguridad:requiere-claude` | Toca webhook/settings/permisos/allauth | automático (workflow) |
| `necesita:usuario` | Espera decisión humana | cualquiera |

La carpeta del Kanban dice *dónde descansa la tarjeta*; las etiquetas dicen *la fase viva del PR*.

## 5. Digest diario

`.github/workflows/digest.yml` mantiene **un** Issue *“📋 Estado del día (multiagente)”* con los PRs
abiertos, su estado de checks, lo que necesita tu decisión y el tamaño del backlog. Corre por cron
(~09:00 Chile) y con *Run workflow* manual. **No usa IA → no gasta tokens.** Es tu único punto de
mirada: si nada te menciona, no tienes que hacer nada.

## 6. Gate de go-live (ANTES de registrar alumnos reales)

Mientras no haya usuarios, la autonomía es máxima. Antes de onboarding real, ejecutar:

- [ ] **Backups + restore probado** (riesgo C2) y **seed idempotente** (C1) cerrados.
- [ ] **Staging** en pie → el auto-merge deja de ir directo a prod sin un vistazo.
- [ ] `REDIS_URL` para rate-limit real (C3).
- [ ] Endurecer el gate: exigir `audit:aprobado` **también** por revisor humano o bot dedicado, y
      subir `lint`/coverage a **gating** (quitar el `|| true`).
- [ ] Revisar la lista de `seguridad:requiere-claude` de las últimas semanas.

Detalle de riesgos en [`matriz-riesgos.md`](matriz-riesgos.md); secuencia en
[`roadmap-priorizado.md`](roadmap-priorizado.md).

## 7. Interruptor de pánico

Si la automatización se descontrola:
```bash
# Desactivar auto-merge del repo (los PRs dejan de mergearse solos):
gh api repos/Octaviochamblas/profeonline -X PATCH -F allow_auto_merge=false
# O quitar la protección/branch para intervenir a mano:
gh api repos/Octaviochamblas/profeonline/branches/main/protection -X DELETE
```

## 8. Qué falta para el lazo 100% sin ti

Que **Codex y Antigravity** se disparen solos al ver su etiqueta (Codex Cloud por tarea de GitHub;
Antigravity con sub-agentes programados). Con eso, `audit:aprobado` y la construcción ocurren sin
intervención. Hoy ya corre solo: CI, auto-merge, etiquetado, digest y el gate.
