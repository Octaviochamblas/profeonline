# C2 — Backups verificados + drill de restauración

> ✅ **Cerrado (2026-06-02, 🏛️ Claude):** código mergeado (PR #28: `backup_db`/`restore_db` con
> guardas anti-prod + runbook + drill local). Riesgo C2 en matriz queda **🟡** hasta que el 🧑 Usuario
> active backups automáticos del proveedor y ejecute un restore desde backup real.

- **Estado:** Finalizado (tooling + drill local) · 🟡 pendiente backups automáticos del proveedor
- **Creado:** 2026-06-02
- **Prioridad:** P0 · **Cartera:** continuidad operacional
- **Tipo:** infraestructura
- **Dueño sugerido:** 🧑 Usuario (provider) + 🔨 Antigravity (herramienta + doc) → 🧩 Codex → 🏛️ Claude

## Objetivo (una frase)
Garantizar que la base de datos tiene **backup diario** y que una **restauración realmente
funciona** (un backup sin restore probado no es un backup).

## Contexto
- Prod usa PostgreSQL (Railway/Supabase) vía `DATABASE_URL` (oblig.). Existe doc histórico
  `docs/_archivo/2026-05-30-documentos-antiguos/operaciones-backups-logs.md` (revisar como base).
- No hay evidencia reciente de backup activo ni de un restore probado.

## Alcance (lo que SÍ entra)
1. **🧑 Usuario:** confirmar/activar **backups automáticos diarios** en el provider (Railway/Supabase)
   y anotar dónde quedan y su retención.
2. **🔨 Antigravity:** añadir comandos de management de respaldo manual y documentar el drill:
   - `backup_db` → `pg_dump` usando `DATABASE_URL` a un archivo con timestamp.
   - `restore_db --file <ruta>` → `pg_restore`/`psql` a una **DB de prueba** (nunca a prod por defecto;
     exigir flag `--confirmar` y variable de destino distinta).
   - Documento `docs/gobernanza/runbook-backups.md`: cómo respaldar, cómo restaurar, y el resultado
     del **drill** (fecha, tamaño, tiempo, verificación de filas).
3. **🧑+🏛️:** ejecutar **un** drill real (restaurar un backup a una DB scratch) y registrar evidencia.

## Fuera de alcance
- Automatizar restores a prod. Backups de archivos estáticos (no hay datos de usuario en disco).

## Archivos a tocar
| Archivo | Cambio |
| --- | --- |
| `apps/core/management/commands/backup_db.py` (nuevo) | `pg_dump` a archivo |
| `apps/core/management/commands/restore_db.py` (nuevo) | `pg_restore` con guardas anti-prod |
| `docs/gobernanza/runbook-backups.md` (nuevo) | procedimiento + evidencia del drill |

## Criterios de aceptación
- [x] Barrera verde.
- [x] `backup_db` genera un dump válido desde `DATABASE_URL` local.
- [x] `restore_db` **rechaza** restaurar sobre la URL de prod sin `--confirmar` + destino explícito.
- [x] Runbook con el drill ejecutado y su evidencia (filas restauradas == origen).
- [ ] Backups automáticos del provider confirmados por el usuario (pendiente: Railway indica que los
  backups del volumen requieren plan Pro; mantener como cierre posterior cuando exista contenido real
  o se contrate/active un mecanismo externo).

## Plan de pruebas
1. `backup_db` local → archivo. 2. Crear DB scratch, `restore_db` ahí, comparar conteos.
3. Intentar `restore_db` apuntando a prod sin `--confirmar` → debe abortar.

## Riesgos / rollback
- Riesgo alto si `restore_db` apunta mal → **guardas obligatorias** (destino != prod, flag confirmar,
  dry-run por defecto). Rollback: comandos nuevos, sin efecto en la app; revertir PR.

## Checklist 🧩 Codex
- [x] `restore_db` no puede tocar prod por accidente (revisar guardas a fondo).
- [x] No se loguea `DATABASE_URL` ni credenciales.
- [ ] Label `audit:aprobado` si ok.

## Checklist 🏛️ Claude (cierre)
- [ ] Drill ejecutado y documentado. `matriz-riesgos.md`: C2 → 🟢.
