# C3 — Redis para rate-limit real del webhook

- **Estado:** Ready (handoff de arquitectura)
- **Creado:** 2026-06-02
- **Prioridad:** P0 · **Cartera:** continuidad operacional
- **Tipo:** infraestructura / seguridad
- **Dueño sugerido:** 🔨 Antigravity (código) + 🧑 Usuario (Railway) → 🧩 Codex → 🏛️ Claude

## Objetivo (una frase)
Que el rate-limit del webhook de videos cuente de forma **compartida** entre workers, en vez de
por-proceso (hoy da una falsa sensación de protección).

## Contexto / diagnóstico (anclado en código real)
- `apps/content/views/api_video.py` usa `django.core.cache` (líneas ~36-52) para contar intentos.
- `config/settings/base.py` **no define `CACHES`** → el default de Django es `LocMemCache`
  (memoria por proceso). Con N workers de gunicorn, el límite de 10 intentos es **10 × N** y se
  reinicia en cada redeploy.
- `config/settings/production.py` (líneas ~168-176) **solo** define `CACHES` (Redis) **si**
  `REDIS_URL` está presente. Hoy no lo está.

## Alcance (lo que SÍ entra)
1. **🧑 Usuario (Railway):** crear un servicio Redis y definir `REDIS_URL` en las env vars de prod.
2. **🔨 Antigravity (código):** que la app **avise** si corre en producción sin cache compartida:
   - Añadir un Django **system check** (`apps/core/checks.py` o similar, registrado en `AppConfig.ready`)
     que emita un `Warning` cuando `not DEBUG` y el backend de cache sea `LocMemCache`.
   - El check NO debe romper `manage.py check --deploy` del CI (es Warning, no Error).
3. **🔨 Documentar** en `docs/gobernanza/inventario-operacional.md` que `REDIS_URL` es **requisito**
   para el rate-limit del webhook.

## Fuera de alcance
- Cambiar la lógica de rate-limit de `api_video.py` (ya es correcta; solo le falta cache compartida).
- Usar Redis para sesiones u otra cosa.

## Archivos a tocar
| Archivo | Cambio |
| --- | --- |
| `apps/core/` (nuevo `checks.py` + registro en `apps.py` `ready()`) | system check de cache en prod |
| `docs/gobernanza/inventario-operacional.md` | `REDIS_URL` como requisito del webhook |

## Criterios de aceptación
- [ ] Barrera verde (`test` · `check` · `makemigrations --check`).
- [ ] Con settings de prod **sin** `REDIS_URL`, `manage.py check` muestra el Warning (no Error).
- [ ] Con `REDIS_URL` definido, el Warning desaparece.
- [ ] Test que verifica que el check se dispara con `LocMemCache` + `DEBUG=False`.
- [ ] `check --deploy --fail-level ERROR` sigue dando **exit 0** (el Warning no rompe CI).

## Plan de pruebas
1. `DJANGO settings=production` sin `REDIS_URL` → `check` lista el Warning.
2. Con `REDIS_URL=redis://localhost:6379/0` → sin Warning.
3. Suite completa.

## Riesgos / rollback
- Riesgo bajo: un check mal escrito podría romper el arranque. Mitigación: que sea `Warning` y
  cubierto por test. Rollback: revertir el PR.

## Checklist 🧩 Codex
- [ ] El check es Warning (no Error) y no afecta `check --deploy` del CI.
- [ ] No hay import circular al registrar el check en `ready()`.
- [ ] Label `audit:aprobado` si ok.

## Checklist 🏛️ Claude (cierre)
- [ ] Confirmar con el usuario que `REDIS_URL` quedó en Railway.
- [ ] `matriz-riesgos.md`: C3 → 🟢 cuando Redis esté en prod.
