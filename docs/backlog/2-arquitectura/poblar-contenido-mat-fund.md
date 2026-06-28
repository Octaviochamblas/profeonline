# Poblar contenido: MAT.FUND — Fundamentos (Lógica + Conjuntos)

## Metadata
- **Estado:** listo para ejecución
- **Dueño actual:** Antigravity
- **Scope:** 106 recursos — B0101 Lógica (43r) + B0102 Conjuntos (63r)
- **Rama sugerida:** `content/mat-fund`
- **Fecha:** 2026-06-28

---

## Antes de empezar — lee estos documentos

1. `docs/backlog/2-arquitectura/poblar-contenido-mat-num-b0201-b0202.md` — proceso completo, reglas YAML/JSONL, formato `stable_id`, criterios de aceptación. **Este card hereda todo eso; no se repite aquí.**
2. `docs/conocimiento/pauta-contenido.md` — 9 campos obligatorios YAML + 10 ejercicios por recurso.
3. `docs/conocimiento/contenido/mat-num-divisibilidad-multiplo-concepto.yaml` — ejemplo de estilo.
4. `docs/conocimiento/ejercicios/mat-num-teoria-numeros-banco-gen-1.jsonl` — ejemplo de JSONL.

**Fuente matemática:** Lógica y Conjuntos son temas de 1°–2° Medio. El contenido se genera a partir del conocimiento propio del agente.

---

## Obtener lista de pendientes por bloque (ejecutar al inicio de cada bloque)

```bash
python manage.py shell -c "
from apps.content.models import KnowledgeNode
for sid in ['MAT.FUND.B0101', 'MAT.FUND.B0102']:
    r = KnowledgeNode.objects.filter(node_type='recurso',
        parent__parent__semantic_id=sid, content__isnull=True).order_by('order')
    print(f'\n--- {sid} ({r.count()} pendientes) ---')
    for x in r: print(x.semantic_id)
"
```

---

## Recursos — MAT.FUND.B0101 — Lógica (43 recursos)

### Subtemas presentes (usar como guía para agrupar tandas)

| Subtema | Cantidad | Descripción |
|---|---|---|
| LOGICA_BASICA | 7 | Proposición, expresión, simple/compuesta, valor de verdad, variable, formalización |
| CONECTIVOS_LOGICOS | 7 | Negación, conjunción, disyunción inclusiva/exclusiva, condicional, bicondicional, prioridad, paréntesis |
| TABLAS_VERDAD | 8 | Tablas de cada conectivo, filas 2/3 variables, construcción, tautología, contradicción, contingencia |
| RAZONAMIENTO_LOGICO | 8 | Equivalencia, doble negación, De Morgan (×2), recíproco, inverso, contrarrecíproco, Modus Ponens, Modus Tollens |
| CUANTIFICADORES | 6 | Universal, existencial, dominio, negación universal/existencial, contraejemplo |

### Tandas sugeridas

| Tanda | Subtemas incluidos | JSONL |
|---|---|---|
| B01-1 | LOGICA_BASICA (7r) | `mat-fund-logica-basica-banco-gen-1.jsonl` |
| B01-2 | CONECTIVOS_LOGICOS (7r) | `mat-fund-conectivos-logicos-banco-gen-1.jsonl` |
| B01-3 | TABLAS_VERDAD pt1 (4r) | `mat-fund-tablas-verdad-banco-gen-1.jsonl` |
| B01-4 | TABLAS_VERDAD pt2 (4r) | `mat-fund-tablas-verdad-banco-gen-2.jsonl` |
| B01-5 | RAZONAMIENTO_LOGICO pt1 (4r) | `mat-fund-razonamiento-banco-gen-1.jsonl` |
| B01-6 | RAZONAMIENTO_LOGICO pt2 (4r) | `mat-fund-razonamiento-banco-gen-2.jsonl` |
| B01-7 | CUANTIFICADORES (6r) | `mat-fund-cuantificadores-banco-gen-1.jsonl` |

---

## Recursos — MAT.FUND.B0102 — Conjuntos (63 recursos)

### Subtemas presentes

| Subtema | Cantidad | Descripción |
|---|---|---|
| CONJUNTOS_BASICOS | 13 | Definición, notación, elemento, pertenencia, extensión/comprensión, vacío, unitario, universal, finito, infinito, cardinalidad, potencia |
| RELACIONES_CONJUNTOS | 7 | Igualdad, subconjunto (propio/impropio), disjuntos, no disjuntos, partición |
| DIAGRAMAS_VENN | 6 | 1 conjunto, 2 disjuntos, 2 intersectados, 3 conjuntos, regiones 2/3 |
| OPERACIONES_CONJUNTOS | 5 | Unión, intersección, diferencia, complemento, diferencia simétrica |
| PROPIEDADES_CONJUNTOS | 9 | Conmutativa (×2), asociativa (×2), distributiva (×2), idempotencia (×2), neutro (×2), absorción (×2), De Morgan (×2) |
| CARDINALIDAD_CONJUNTOS | 8 | Unión disjunta, inclusión-exclusión 2/3, Venn 2/3, regiones exclusivas, región ninguno, región exactamente 2 |
| PRODUCTO_CARTESIANO | 6 | Par ordenado, igualdad, definición, elementos, cardinalidad, representación plano |

### Tandas sugeridas

| Tanda | Subtemas incluidos | JSONL |
|---|---|---|
| B02-1 | CONJUNTOS_BASICOS pt1 (5r) | `mat-fund-conjuntos-basicos-banco-gen-1.jsonl` |
| B02-2 | CONJUNTOS_BASICOS pt2 (5r) | `mat-fund-conjuntos-basicos-banco-gen-2.jsonl` |
| B02-3 | CONJUNTOS_BASICOS pt3 (3r) + RELACIONES_CONJUNTOS pt1 (2r) | `mat-fund-conjuntos-relaciones-banco-gen-1.jsonl` |
| B02-4 | RELACIONES_CONJUNTOS pt2 (5r) | `mat-fund-conjuntos-relaciones-banco-gen-2.jsonl` |
| B02-5 | DIAGRAMAS_VENN (6r) | `mat-fund-diagramas-venn-banco-gen-1.jsonl` |
| B02-6 | OPERACIONES_CONJUNTOS (5r) | `mat-fund-operaciones-conjuntos-banco-gen-1.jsonl` |
| B02-7 | PROPIEDADES_CONJUNTOS pt1 (5r) | `mat-fund-propiedades-conjuntos-banco-gen-1.jsonl` |
| B02-8 | PROPIEDADES_CONJUNTOS pt2 (4r) | `mat-fund-propiedades-conjuntos-banco-gen-2.jsonl` |
| B02-9 | CARDINALIDAD_CONJUNTOS (5r) | `mat-fund-cardinalidad-banco-gen-1.jsonl` |
| B02-10 | CARDINALIDAD_CONJUNTOS (3r) + PRODUCTO_CARTESIANO pt1 (2r) | `mat-fund-cardinalidad-producto-banco-gen-1.jsonl` |
| B02-11 | PRODUCTO_CARTESIANO pt2 (4r) | `mat-fund-producto-cartesiano-banco-gen-2.jsonl` |

---

## Naming de archivos YAML

Patrón: `mat-fund-{subtema-kebab}-{concepto-kebab}.yaml`

Ejemplos:
- `MAT.FUND.LOGICA_BASICA.PROPOSICION_MATEMATICA` → `mat-fund-logica-basica-proposicion-matematica.yaml`
- `MAT.FUND.CONECTIVOS_LOGICOS.CONJUNCION` → `mat-fund-conectivos-logicos-conjuncion.yaml`
- `MAT.FUND.TABLAS_VERDAD.TAUTOLOGIA` → `mat-fund-tablas-verdad-tautologia.yaml`
- `MAT.FUND.PROPIEDADES_CONJUNTOS.DE_MORGAN_COMPLEMENTO_UNION` → `mat-fund-propiedades-de-morgan-complemento-union.yaml`

---

## Campos especiales por subtema

- **TABLAS_VERDAD**: el `procedimiento` debe incluir los pasos para construir la tabla (columnas, filas = 2^n, evaluación conectivo por conectivo).
- **RAZONAMIENTO_LOGICO**: el `procedimiento` debe mostrar la cadena de equivalencias o el esquema de inferencia.
- **DIAGRAMAS_VENN**: los `ejemplos` Tipo A deben describir zonas del diagrama con lenguaje de conjuntos; los Tipo B deben ser afirmaciones sobre pertenencia o cardinalidad.
- **CUANTIFICADORES**: los `errores_frecuentes` deben incluir la confusión entre ∀ y ∃ y la negación incorrecta de cada uno.

---

## Proceso de ejecución

El proceso es idéntico al de `poblar-contenido-mat-num-b0201-b0202.md` §"Proceso de ejecución". Resumen:
1. Generar YAMLs en `docs/conocimiento/contenido/`
2. Generar JSONL en `docs/conocimiento/ejercicios/`
3. `python manage.py load_node_content`
4. `python manage.py load_exercise_bank --file docs/conocimiento/ejercicios/ARCHIVO.jsonl`
5. Verificar + commit de la tanda

---

## Verificación de cobertura total

```bash
python manage.py shell -c "
from apps.content.models import KnowledgeNode
for sid in ['MAT.FUND.B0101', 'MAT.FUND.B0102']:
    r = KnowledgeNode.objects.filter(node_type='recurso', parent__parent__semantic_id=sid)
    done = r.filter(content__isnull=False).count()
    print(f'{sid}: {done}/{r.count()}')
"
```

## Criterios de aceptación

- [ ] B0101: 43/43 recursos con `NodeContent`
- [ ] B0102: 63/63 recursos con `NodeContent`
- [ ] Cada recurso: ≥ 10 ejercicios (3 conceptuales + 1 reconocimiento + 3 procedimiento + 3 tipo_paes)
- [ ] `python manage.py check` sin errores
- [ ] No se tocó código Python, HTML ni archivos de otros ejes
