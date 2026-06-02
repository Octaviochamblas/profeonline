# Auditorías

> Ubicación **canónica** de auditorías (Capa 3 — memoria/evidencia). Antes estaban dispersas en dos
> lugares; ahora viven todas aquí. Última revisión: 2026-06-01.

## Convención de nombres

```
AAAA-MM-DD-<alcance>.md      → ej. 2026-06-01-gamificacion-malla.md
```

Cada auditoría debe declarar al inicio: **fecha**, **autor/agente**, **alcance** y **estado**
(vigente / superada por <fecha>). Una auditoría no se borra: cuando envejece, se anota su estado y,
si procede, se mueve a `_archivo-AAAA-MM-DD/`.

## Índice

| Fecha | Alcance | Archivo | Estado |
| --- | --- | --- | --- |
| 2026-06-02 | seed_content idempotente C1b | [`2026-06-02-seed-content-idempotente-c1b.md`](2026-06-02-seed-content-idempotente-c1b.md) | vigente |
| 2026-06-02 | Seed idempotente C1 (`seed_math_resources`) | [`2026-06-02-seed-idempotente-c1.md`](2026-06-02-seed-idempotente-c1.md) | vigente |
| 2026-06-01 | Gamificación + malla curricular vertebral (vs. Khan/Duolingo) | [`2026-06-01-gamificacion-malla.md`](2026-06-01-gamificacion-malla.md) | vigente |
| 2026-05-30 | Rendimiento, accesibilidad, legal, threat-model, conversión, despliegue | [`_archivo-2026-05-30/`](_archivo-2026-05-30/) | histórico |

## Cadencia recurrente

El antídoto contra "auditar una vez y archivar". (Tabla completa en
[`../gobernanza/inventario-operacional.md`](../gobernanza/inventario-operacional.md) §5.)

| Auditoría | Cadencia |
| --- | --- |
| Seguridad de dependencias | Continua (CI + Dependabot) |
| Accesibilidad (axe + teclado/NVDA) | Mensual + tras cada gran cambio de UI |
| Rendimiento (Lighthouse/CWV) | Mensual |
| Backups / restauración | Trimestral |
| Rotación de secretos | Semestral |
| UX/gamificación vs. referentes | Semestral |

## Relación con el resto

- Una auditoría **detecta** problemas → cada hallazgo P0/P1 se convierte en una **tarjeta** en
  [`../backlog/1-por-iniciar/`](../backlog/1-por-iniciar/) y/o entra en
  [`../gobernanza/matriz-riesgos.md`](../gobernanza/matriz-riesgos.md).
- La auditoría es **evidencia**; la mitigación es **trabajo** (backlog); el riesgo vivo es
  **gobernanza**. No mezclar los tres.
