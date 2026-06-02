# Auditoría C2 - Backups verificados + drill de restauración

- **Fecha:** 2026-06-02
- **Autor/agente:** Codex
- **Alcance:** rama `feat/backups-restore-drill`
- **Estado:** vigente

## Resumen

Antigravity implementó comandos Django para respaldar y restaurar la base de datos:

- `backup_db`: genera dumps SQLite o PostgreSQL sin poner la contraseña en la línea de comando.
- `restore_db`: restaura SQLite/PostgreSQL con guardas para destinos remotos o producción.
- `docs/gobernanza/runbook-backups.md`: documenta el procedimiento y un drill local.
- Tests unitarios en `apps/core.tests.BackupRestoreCommandTests`.

## Hallazgos

### P1 - El runbook afirmaba backups automáticos activos sin evidencia real

Railway indicó al usuario que los backups del volumen solo están disponibles en plan Pro. Por eso no
corresponde marcar C2 como cerrado por completo. Se corrigió el runbook y la tarjeta para dejar
backups automáticos como pendiente explícito.

### P1 - Restore remoto necesitaba una confirmación más explícita

La implementación original permitía restaurar en una base remota/producción con `--confirmar` y
`--destino`. Se endureció el comando agregando `--permitir-remoto`, de modo que cualquier restore
remoto requiera tres señales explícitas y quede reservado a una emergencia revisada.

### P2 - Dumps locales podían aparecer en `git status`

La carpeta `backups/` no estaba en `.gitignore`. Se agregó para prevenir commits accidentales de
respaldos.

## Verificación

- `.venv\Scripts\python.exe manage.py test apps.core.tests.BackupRestoreCommandTests --verbosity 1`: OK, 6 tests.
- `.venv\Scripts\python.exe manage.py check`: sin issues.
- `.venv\Scripts\python.exe manage.py makemigrations --check --dry-run`: sin cambios detectados.
- `git diff --check`: sin problemas de whitespace; solo avisos normales de conversión LF/CRLF en Windows.

## Decisión

C2 queda aprobable como herramienta manual y drill local, pero no debe cerrarse como mitigación total
hasta activar backups automáticos del proveedor o una alternativa externa y probar restore desde un
backup real. El label `audit:aprobado` es razonable si el PR se describe como C2a/manual tooling,
no como cierre completo de continuidad operacional.
