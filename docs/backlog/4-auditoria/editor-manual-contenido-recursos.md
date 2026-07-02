# Editor manual de contenido desde cada recurso

- **Estado:** Construido; pendiente de auditoría
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
Añadir una acción visible solo para staff que enlace al editor seguro de Django Admin: modificar el `NodeContent` existente o crearlo con el nodo preseleccionado.

## No-objetivos (qué queda FUERA)
- Crear un segundo formulario/editor paralelo al Admin.
- Editar bancos de ejercicios, multimedia o la jerarquía del nodo.
- Sincronizar ediciones de base de datos hacia YAML versionado.

## Criterios de aceptación (verificables)
- [x] Barrera verde: tests focalizados · `check` · `makemigrations --check --dry-run`
- [x] Staff autorizado ve una acción de edición en cada recurso y llega al registro correcto.
- [x] Si no existe contenido, staff autorizado llega al alta con el nodo preseleccionado.
- [x] Usuarios no autorizados no ven la acción.

## Plan de pruebas
Tests de vista para visitante, staff con contenido y staff sin contenido; `check` y comprobación de migraciones.

## Riesgos / rollback
Una carga YAML posterior puede sobrescribir ediciones en base de datos; se advierte en la interfaz. Rollback: retirar el enlace y sus tests.

---

## Qué se hizo
- Se añadió a la ficha una acción editorial protegida por permisos de `NodeContent`.
- La acción abre Django Admin en el contenido correcto o en el alta con el nodo preseleccionado.
- La interfaz avisa que una importación YAML posterior puede sobrescribir cambios guardados en la base.
- Se cubrieron visitante, administrador con/sin contenido y staff sin permiso mediante 4 regresiones nuevas.
- Validación: 12 tests de `NodeDetailViewTests`, `check` y ausencia de migraciones, OK.
