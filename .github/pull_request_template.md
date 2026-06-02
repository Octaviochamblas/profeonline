## Qué y por qué
<!-- 1–2 frases -->

## Tarjeta / handoff
- **Tarjeta:** `docs/backlog/.../<archivo>.md`
- **Etapa:** <!-- 2-arquitectura | 3-construccion | 4-auditoria | 5-cierre -->

## Checklist (Definition of Done)
- [ ] Barrera local verde: `test` · `check` · `makemigrations --check --dry-run`
- [ ] Diff acotado al handoff (nada de más)
- [ ] Si toca CSS → cache-buster `?v=N` subido
- [ ] Migraciones revisadas + plan de rollback (si aplica)

## Auditoría IA (gate de auto-merge)
> Este PR **se auto-mergea** cuando CI esté verde **y** una IA distinta a la que construyó
> añada el label **`audit:aprobado`**. PRs solo de `docs/` y de Dependabot se auto-aprueban.

## QA / notas
<!-- screenshots, QA manual, riesgos -->
