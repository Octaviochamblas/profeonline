# Editor manual de contenido desde cada recurso

- **Estado:** Construido; pendiente de auditoría (suite global pendiente en CI)
- **Creado:** 2026-07-01
- **Prioridad:** P1  ·  **Cartera:** continuidad
- **Tipo:** producto
- **Dueño sugerido:** Codex

## Objetivo (una frase)
Permitir que el personal autorizado abra la edición manual del contenido directamente desde cada ficha de recurso.

## Fuentes a leer (rutas concretas)
- `apps/learn/views.py`
- `templates/learn/node_detail.html`
- `apps/content/admin.py`
- `apps/learn/tests.py`

## Propuesta
Añadir un modal amplio en la propia ficha, protegido por permisos de `NodeContent`, para editar todos sus campos con controles visuales y proteger las ediciones manuales frente a importaciones YAML.

## No-objetivos (qué queda FUERA)
- Editar bancos de ejercicios, multimedia o la jerarquía del nodo.
- Sincronizar ediciones de base de datos hacia YAML versionado.

## Criterios de aceptación (verificables)
- [x] Barrera focal verde: 36 tests · `check --deploy` · migraciones · sintaxis JS.
- [ ] Suite completa: dos intentos locales excedieron 2 y 5 minutos sin emitir fallos; ejecutar en CI/auditoría.
- [x] Staff autorizado edita todo `NodeContent` sin abandonar la ficha.
- [x] Procedimientos, ejemplos, soluciones y errores usan controles visuales reordenables.
- [x] Guardado inmediato, validado y protegido contra ediciones concurrentes.
- [x] Importación YAML omite ediciones manuales salvo `--force-manual`.
- [x] Usuarios no autorizados no ven ni pueden invocar el editor.

## Plan de pruebas
Tests de permisos, CSRF, creación, edición, validación, concurrencia e importador; QA real de guardado,
reordenamiento, Escape, foco y viewport móvil.

## Riesgos / rollback
Las ediciones manuales pueden divergir del YAML; `manual_override` las protege y `--force-manual` permite volver
explícitamente a la fuente versionada. Rollback: revertir la migración y restaurar el enlace al Admin.

---

## Qué se hizo
- Modal amplio dentro de la ficha para todos los campos de `NodeContent`, sin entrar al Admin.
- Controles visuales para crear, borrar y reordenar pasos, ejemplos, soluciones y errores.
- Endpoint JSON transaccional con permisos, CSRF, validación y conflicto `409` mediante `updated_at`.
- Migración `0043`: protección manual, fecha y autor; importador omite protegidos salvo `--force-manual`.
- QA real corrigió Escape/retorno de foco y el pie fuera de pantalla en móvil.
- Validación: 36 tests focalizados, barreras Django y QA navegador OK; suite global pendiente por timeout local.
