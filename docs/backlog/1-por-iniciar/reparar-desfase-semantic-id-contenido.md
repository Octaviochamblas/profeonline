# Reparar desfase de `semantic_id` entre YAML de contenido y árbol atómico

- **Estado:** Por iniciar
- **Creado:** 2026-09-04
- **Prioridad:** P1  ·  **Cartera:** educativa
- **Tipo:** pedagogía + infraestructura
- **Dueño sugerido:** 🔨 Antigravity (mapeo masivo) · 🏛️ Claude (diseño del mapa + criterios)

## Objetivo (una frase)
95 archivos de `docs/conocimiento/contenido/` traen un `semantic_id` que **no existe
en el árbol** (`KnowledgeNode`), así que su contenido de 12 secciones nunca se carga
y esas páginas de `/aprender/` muestran el fallback genérico. Hay que mapear cada
uno al `semantic_id` atómico correcto (o crear el nodo faltante en el skeleton).

## Contexto / causa raíz
- `load_node_content` hace `KnowledgeNode.objects.get(semantic_id=...)` — match **exacto**.
- `import_knowledge_tree` **omite 13 skeletons "no atómicos"** (`proporcionalidad.yaml`,
  `numeros.yaml`, `progresiones.yaml`, `algebra.yaml`, …). Los bloques que vivían ahí
  se re-modelaron en skeletons atómicos con **prefijos e ids de hoja distintos**.
- El contenido de esas áreas quedó escrito contra los ids viejos. No es regresión de
  ningún commit reciente — el `preDeployCommand` y las 96 migraciones borradas
  chocaban con la misma pared (`semantic_id no encontrado: 95` en todos los deploys).
- Reproducir el diagnóstico: `.venv/Scripts/python.exe scripts/audit_content_semantic_ids.py`

## Alcance (95 archivos, 3 baldes)
| Balde | N | Qué hacer |
| --- | --- | --- |
| `rename_directo` | 35 | El leaf existe igual bajo otro bloque de la misma rama. Cambio mecánico de `semantic_id:` en el YAML. Ej: `MAT.ALG.CLASIFICACION.EXPRESION_ENTERA` → `MAT.ALG.CLASIFICACION_TECNICA.EXPRESION_ENTERA`; `MAT.NUM.NUMEROS_COMPLEJOS.*` → `MAT.NUM.COMPLEJOS.*`; `MAT.NUM.FINANZAS.*` → `MAT.NUM.FINANZAS_PERSONALES.*`; `MAT.ALG.POLINOMIOS.IDENTIFICACION_*` → `MAT.ALG.EXPRESIONES.IDENTIFICACION_*`. |
| `revisar` | 1 | `MAT.NUM.NUMEROS_COMPLEJOS.DEFINICION` → destino claro `MAT.NUM.COMPLEJOS.DEFINICION` (el leaf `DEFINICION` existe en varias ramas). |
| `sin_destino` | 59 | El leaf **no existe** en la rama. Requiere leer el contenido y decidir: (a) mapear a un nodo atómico con nombre distinto, o (b) crear el nodo en el skeleton atómico. Concentrado en `MAT.NUM.RAZONES_PROPORCIONES.*` (PROP_DIRECTA/INVERSA/COMPUESTA, ESCALA_*, MODELO/GRAFICO/TABLA/PROBLEMAS_PROP_*), `MAT.NUM.PORCENTAJES.*` (CALC_PARTE/TASA/TOTAL, REP_*, CALC_MENTAL_*), `MAT.NUM.PROG_ARITMETICA.*` (CALCULO_A1/POSICION, MODELAMIENTO_LINEAL), `MAT.NUM.NUMEROS_IMAGINARIOS.*`. |

Los skeletons atómicos relevantes: `numeros-razones-porcentajes-finanzas.yaml`
(bloques `MAT.NUM.RAZONES`, `PROPORCIONES`, `PROP_DIRECTA`, `PROP_INVERSA`,
`PROP_COMPUESTA`, `REPARTO_ESCALAS`, `PORCENTAJES`, `VARIACION_PORCENTUAL`,
`FINANZAS_PERSONALES`, `INTERES_*`), `numeros-sucesiones-progresiones.yaml`,
`numeros-reales-potencias-raices-logaritmos.yaml` (`IMAGINARIOS`, `COMPLEJOS`,
`LOGARITMOS_*`), `algebra-nomenclatura-conceptos.yaml`, `algebra-lenguaje-valorizacion.yaml`.

## Fuentes a leer (rutas concretas)
- `apps/content/management/commands/load_node_content.py` (línea ~53, el `.get()`).
- `apps/content/management/commands/import_knowledge_tree.py` (regla de "no atómicos").
- `docs/conocimiento/numeros-razones-porcentajes-finanzas.yaml` y demás skeletons de arriba.
- `docs/conocimiento/contenido/*.yaml` — los 95 archivos (lista completa desde el script).
- Memoria de proyecto: `biblioteca-conocimiento-estandar`, `biblioteca-archivos-separados`.

## Propuesta
1. Correr `scripts/audit_content_semantic_ids.py`, volcar los 3 baldes a un TSV.
2. **Balde `rename_directo` (35):** `sed`/script que reescribe `semantic_id:` en cada YAML
   según el mapa 1:1. Revisión rápida del diff.
3. **Balde `sin_destino` (59):** por sub-área, comparar los ids de contenido contra los
   leaves reales del skeleton atómico correspondiente. Para cada uno: renombrar el
   `semantic_id` del contenido, o agregar el leaf al skeleton (respetando nomenclatura
   `RR.TT.rr` + id semántico). Priorizar `RAZONES_PROPORCIONES` (41) y `PORCENTAJES` (9)
   por volumen.
4. Correr `import_knowledge_tree && load_node_content` en local; iterar hasta
   `semantic_id no encontrado: 0`.
5. Deploy normal (el `preDeployCommand` sincroniza). Verificar en prod 3-4 páginas de
   las áreas tocadas.

## No-objetivos (qué queda FUERA)
- Reescribir la calidad del contenido (eso es `remediar-contenido-*`). Acá solo se
  arregla el enganche al árbol.
- Los ~10 `checkpoints inválidos` ("la explicación debe mencionar la alternativa
  correcta") — bug de datos aparte, listar y derivar.
- Tocar `load_node_content` / `import_knowledge_tree` (el matching exacto está bien).

## Criterios de aceptación (verificables)
- [ ] Barrera verde: `test` · `check` · `makemigrations --check --dry-run`
- [ ] `python manage.py import_knowledge_tree && python manage.py load_node_content`
      reporta `semantic_id no encontrado: 0`
- [ ] `scripts/audit_content_semantic_ids.py` → 0 orphans
- [ ] 3-4 páginas de `/aprender/` de Razones/Proporciones, Porcentajes, Finanzas y
      Números Complejos muestran contenido de 12 secciones en prod (no el fallback)
- [ ] Los `checkpoints inválidos` quedaron listados en una tarjeta/nota aparte

## Plan de pruebas
- `scripts/audit_content_semantic_ids.py` antes/después.
- Loader local en verde (0 no encontrados).
- Suite completa una vez antes de pushear.
- Smoke manual en prod tras el deploy.

## Riesgos / rollback
- **Riesgo:** mapear un contenido al nodo equivocado → página muestra contenido de otro
  tema. Mitiga: revisión del diff del balde `sin_destino` por un humano que conozca el
  temario; el balde `rename_directo` es seguro (mismo leaf, misma rama).
- **Rollback:** `git revert` del commit de contenido; el `preDeployCommand` recarga el
  estado anterior en el siguiente deploy. Nada de esto toca esquema.

---

## Qué se hizo
_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_
