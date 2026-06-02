# Automatización del flujo multiagente (Fase 1: Router seguro)

- **Estado:** Auditoría
- **Creado:** 2026-06-02
- **Prioridad:** P0  ·  **Cartera:** continuidad operacional / ingeniería
- **Tipo:** infraestructura
- **Dueño sugerido:** 🔨 Antigravity (constructor) -> 🧩 Codex (auditoría) -> 🏛️ Claude (cierre)

## Objetivo (una frase)
Implementar la primera fase de automatización mecánica del flujo multiagente mediante GitHub Actions sin consumo de tokens de IA para optimizar el ruteo de tareas, el digest diario y la cola de Claude de forma 100% segura.

## Fuentes a leer (rutas concretas)
- `.github/workflows/pipeline.yml`
- `.github/workflows/digest.yml`
- `docs/gobernanza/automatizacion-flujo.md`

## Propuesta
Implementar un router en GitHub Actions que de forma idempotente cree y asigne etiquetas de etapa y agente en PRs y tareas, re-estructure el digest diario para que sea altamente accionable, cree una cola física para Claude y registre los límites seguros de esta fase.

## No-objetivos (qué queda FUERA)
- Conectar APIs externas o ejecutar scripts con llamadas de Inteligencia Artificial (LLM).
- Añadir secretos o credenciales a los runners de GitHub Actions.
- Otorgar permisos amplios de escritura (`contents: write`) salvo los indispensables para el router.
- Activar auto-merge o etiquetado de aprobación automático sin control.

## Criterios de aceptación (verificables)
- [x] El archivo `.github/workflows/agent-router.yml` existe y está bien formado.
- [x] El router asegura de forma idempotente las 10 etiquetas necesarias para la coordinación.
- [x] El router etiqueta PRs de código para Codex (`etapa:auditoria` + `agente:codex`).
- [x] El router etiqueta PRs sensibles para Claude (`seguridad:requiere-claude` + `etapa:cierre` + `agente:claude`).
- [x] El digest diario (`digest.yml`) incluye secciones para "Acción humana requerida", "Listos para Codex", "Pendientes de Claude", "PRs bloqueados", "Kanban" y "Lock vivo".
- [x] El digest actualiza un único issue existente en lugar de duplicar issues diarios.
- [x] La cola diferida de Claude existe en `docs/_coordinacion/cola-claude.md`.
- [x] La documentación en `docs/gobernanza/automatizacion-flujo.md` describe los alcances y límites de esta fase.

## Plan de pruebas
1. Validar la sintaxis de los workflows de GitHub Actions.
2. Comprobar que no hay errores de lint en la rama local (`git diff --check`).
3. Verificar que la suite de pruebas local continúe pasando (smoke tests).

## Riesgos / rollback
- **Riesgo:** Un error de sintaxis en el archivo YAML de los workflows puede detener las automatizaciones existentes.
  - **Mitigación:** Validar los archivos antes del commit.
  - **Rollback:** Revertir los cambios en los archivos `.github/workflows/*` y restaurar las versiones anteriores.

---

## Qué se hizo
- Se creó el workflow `.github/workflows/agent-router.yml` para gestionar de manera automática e idempotente las etiquetas de agentes, etapas y ruteo de PRs abiertos de código y sensibles.
- Se actualizó el workflow `.github/workflows/digest.yml` para consolidar el estado del día agrupando por responsabilidad de agente, estado de bloqueo de checks, conteo de Kanban (excluyendo plantillas) y el contenido del lock vivo de `docs/_coordinacion/ESTADO.md`.
- Se creó el documento de coordinación `docs/_coordinacion/cola-claude.md` como cola diferida.
- Se actualizó `docs/gobernanza/automatizacion-flujo.md` añadiendo la descripción de la fase actual (router mecánico y seguro) y sus límites.
- Se resolvió la eliminación del archivo vacío `file` de la raíz del repositorio.
