# 📡 Canal de coordinación entre agentes (Claude · Antigravity · Codex)

Esta carpeta es el **canal en vivo** entre los agentes mientras se trabaja. Existe para resolver
un problema real y ya observado: los agentes **no comparten memoria** y han llegado a **editar el
mismo working tree a la vez**, pisándose cambios. El bus de coordinación basado en archivos lo
evita.

> Empieza por el índice maestro [`docs/README.md`](../README.md). Este canal no reemplaza nada:
> - **Kanban** (`docs/backlog/`) = el *qué* (tareas).
> - **Reportes de sesión** (`docs/reportes-sesion/`) = la *memoria histórica*.
> - **`_coordinacion/`** = el *canal en vivo* entre agentes durante el trabajo.
> - **`docs/gobernanza/`** = las *reglas vigentes* (proceso, roadmap, riesgos, inventario).

## Roles (resumen)

- **🏛️ Claude** — arquitecto + cierre. Diseña specs, revisa el plan **antes** de construir,
  auditoría final, mergea a `main`, escribe el reporte.
- **🔨 Antigravity** — builder. Implementa la spec en una rama propia, deja la barrera verde.
- **🧩 Codex** — auditor (preflight + construcción): tests, N+1, migraciones, diff; + integraciones/datos.
- **🧑 Usuario** — decide, hace QA humano (visual/teclado/NVDA) y gestiona servicios y secretos.

Detalle completo en [`docs/gobernanza/proceso-multiagente.md`](../gobernanza/proceso-multiagente.md).

## Protocolo (mínimo y obligatorio)

1. **Al iniciar sesión:** leer `ESTADO.md` (este directorio) **y** el último reporte de
   `docs/reportes-sesion/`.
2. **Antes de tocar el working tree:** declarar el lock en `ESTADO.md` (tu nombre + rama + hora).
   - 🔒 **Regla de oro:** *un solo agente escribe en el working tree a la vez.* Si necesitan
     paralelizar, **cada agente en su propia rama/worktree**. No editar la rama de otro.
3. **Specs (arquitecto → builder):** dejar el brief en `handoffs/` usando `_plantilla-handoff.md`.
   El builder responde **en el mismo archivo** con su plan y, al terminar, el enlace al PR.
4. **Eventos relevantes** (decisión, bloqueo, entrega, bug encontrado): una línea en
   `bitacora/AAAA-MM-DD.md`. Es **append-only**: nadie reescribe lo de otro.
5. **Al cerrar:** liberar el lock en `ESTADO.md` y escribir el reporte de sesión normal.

## Estructura

```
_coordinacion/
├── README.md                     ← este archivo (leer al iniciar)
├── ESTADO.md                     ← estado vivo + lock del working tree
├── handoffs/
│   └── _plantilla-handoff.md     ← spec arquitecto→builder
└── bitacora/
    └── _plantilla-entrada.md     ← formato de una entrada de bitácora
```
