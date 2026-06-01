# Handoff — <título corto de la tarea>

- **De:** 🏛️ Claude (arquitecto)  →  **Para:** 🔨 Antigravity (builder) / 🧩 Codex
- **Fecha:** AAAA-MM-DD
- **Tarjeta Kanban relacionada:** `docs/backlog/2-arquitectura/<archivo>.md` (se irá moviendo por el pipeline)
- **Rama sugerida:** `tipo/nombre-descriptivo`

## Objetivo
<Qué problema resuelve, en 1–3 frases.>

## Alcance (lo que SÍ entra)
- ...

## Fuera de alcance (lo que NO entra)
- ...

## Archivos esperados a tocar
| Archivo | Cambio esperado |
| --- | --- |
| `...` | ... |

## Criterios de aceptación
- [ ] `manage.py test` verde · `check` verde · `makemigrations --check --dry-run` sin cambios
- [ ] Si toca CSS → cache-buster `?v=N` subido
- [ ] Diff acotado a este alcance (nada de más)
- [ ] <criterios funcionales específicos de esta tarea>

## Riesgos / cuidados
- <regresiones conocidas, tests que podrían romperse, decisiones de diseño a respetar>

---

## ✍️ Respuesta del builder (rellenar aquí)

### Plan propuesto (ANTES de codear — esperar visto bueno del arquitecto)
- ...

### Entrega
- **Rama:** `...`
- **PR:** #...
- **Notas / desviaciones del plan:** ...
- **Barrera:** test ⬜ · check ⬜ · makemigrations ⬜
