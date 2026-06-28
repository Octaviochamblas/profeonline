# Poblar contenido: MAT.GEO — Geometría

## Metadata
- **Estado:** listo para ejecución
- **Dueño actual:** Antigravity
- **Scope:** 482 recursos — 13 bloques (B0401–B0413)
- **Rama sugerida:** `content/mat-geo`
- **Fecha:** 2026-06-28

---

## Antes de empezar — lee estos documentos

1. `docs/backlog/2-arquitectura/poblar-contenido-mat-num-b0201-b0202.md` — proceso completo, reglas YAML/JSONL, formato `stable_id`, criterios de aceptación.
2. `docs/conocimiento/pauta-contenido.md` — 9 campos obligatorios + 10 ejercicios por recurso.
3. Ejemplos de estilo: `mat-num-divisibilidad-multiplo-concepto.yaml` y `mat-num-teoria-numeros-banco-gen-1.jsonl`.

**Fuente matemática:** Geometría cubre 5° Básico a 4° Medio y preuniversitario. El agente tiene conocimiento suficiente para todo el contenido.

**Estrategia de ejecución:** Dado el volumen (482r, 13 bloques), procesar **un bloque completo por sesión de trabajo**, en orden B0401→B0413. Los bloques van de 23 a 53 recursos.

---

## Obtener lista de pendientes por bloque (ejecutar al inicio de cada bloque)

```bash
python manage.py shell -c "
from apps.content.models import KnowledgeNode
bloque_id = 'MAT.GEO.B0401'  # <-- cambiar por el bloque que toca
r = KnowledgeNode.objects.filter(node_type='recurso',
    parent__parent__semantic_id=bloque_id, content__isnull=True).order_by('order')
print(f'{bloque_id}: {r.count()} pendientes')
for x in r: print(x.semantic_id)
"
```

---

## Todos los bloques — resumen de scope

| Bloque | Recursos | Nombre | Tandas (~5r c/u) |
|---|---|---|---|
| MAT.GEO.B0401 | 53 | Ángulos: Fundamentos y Relaciones | 11 |
| MAT.GEO.B0402 | 34 | Triángulos: Propiedades y Clasificación | 7 |
| MAT.GEO.B0403 | 34 | Elementos Secundarios del Triángulo | 7 |
| MAT.GEO.B0404 | 36 | Perímetros, Áreas y Teoremas | 8 |
| MAT.GEO.B0405 | 46 | Congruencia, Semejanza y Homotecia | 10 |
| MAT.GEO.B0406 | 34 | Polígonos y Cuadriláteros | 7 |
| MAT.GEO.B0407 | 45 | Circunferencia y Círculo | 9 |
| MAT.GEO.B0408 | 36 | Geometría del Espacio y Cuerpos Geométricos | 8 |
| MAT.GEO.B0409 | 28 | Sistema Cartesiano y Vectores | 6 |
| MAT.GEO.B0410 | 25 | Transformaciones Isométricas | 5 |
| MAT.GEO.B0411 | 23 | Trigonometría en el Triángulo Rectángulo | 5 |
| MAT.GEO.B0412 | 39 | Trigonometría Ampliada | 8 |
| MAT.GEO.B0413 | 49 | Geometría Analítica Ampliada | 10 |
| **TOTAL** | **482** | | **~101 tandas** |

---

## Guía de subtemas por bloque (para agrupar tandas)

### B0401 — Ángulos (53r)
Subtemas: `ANGULOS_FUNDAMENTOS`, `ANGULOS_CLASIFICACION`, `ANGULOS_RELACIONES_METRICAS`, `ANGULOS_RELACIONES_POSICION`, `ANGULOS_PARALELAS`.

### B0402 — Triángulos (34r)
Subtemas: `TRIANGULOS_DEF`, `TRIANGULOS_ANGULOS`, `TRIANGULOS_CLASIFICACION`, `TRIANGULOS_METRICA`, `TRIANGULOS_EXTERIOR`.

### B0403 — Elementos Secundarios del Triángulo (34r)
Subtemas: `ALTURA_ORTOCENTRO`, `BISECTRIZ_INCENTRO`, `SIMETRAL_CIRCUNCENTRO`, `TRANSVERSAL_BARICENTRO`, `LINEA_EULER`.

### B0404 — Perímetros, Áreas y Teoremas (36r)
Subtemas: `PITAGORAS`, `RELACIONES_TR`, `AREAS_TRIANGULOS`, `TRIANGULOS_NOTABLES_METRICA`, `AREAS_POLIGONOS`, `TEOREMA_SENO_COSENO` (solo los que estén en el bloque).

### B0405 — Congruencia, Semejanza y Homotecia (46r)
Subtemas: `CONGRUENCIA_TRIANGULOS`, `TEOREMA_TALES`, `SEMEJANZA_TRIANGULOS_POLIGONOS`, `HOMOTECIA`, `APLICACIONES_SEMEJANZA`.

### B0406 — Polígonos y Cuadriláteros (34r)
Subtemas: `POLIGONOS_BASE`, `POLIGONOS_METRICA`, `PARALELOGRAMOS`, `TRAPECIOS_TRAPEZOIDES`, `AREAS_CUADRILATEROS`.

### B0407 — Circunferencia y Círculo (45r)
Subtemas: `CIRCULO_ELEMENTOS`, `CIRCULO_RECTAS`, `CIRCULO_METRICA`, `CIRCULO_ANGULOS`, `CIRCULO_POTENCIA`.

### B0408 — Geometría del Espacio (36r)
Subtemas: `ESPACIO_FUNDAMENTOS`, `POLIEDROS_PRISMAS`, `CUERPOS_REDONDOS_BASE`, `CUERPOS_REDONDOS_METRICA`, `PIRAMIDES_CONOS`.

### B0409 — Sistema Cartesiano y Vectores (28r)
Subtemas: `CARTESIANO_BASE`, `SEGMENTO_METRICA`, `VECTORES_BASE`, `VECTORES_OPERATORIA`.

### B0410 — Transformaciones Isométricas (25r)
Subtemas: `ISOMETRIA_TRASLACION`, `SIMETRIAS`, `ROTACION_PLANO`.

### B0411 — Trigonometría Triángulo Rectángulo (23r)
Subtemas: `TRIG_FUNDAMENTAL`, `TRIG_RECIPROCAS`, `TRIG_NOTABLES`, `TRIG_IDENTIDADES`, `TRIG_APLICACIONES`.

### B0412 — Trigonometría Ampliada (39r)
Subtemas: `TRIG_CUADRANTES`, `TRIG_IDENTIDADES_AMP`, `TRIG_OBLICUANGULOS`, `TRIG_APLICA_REAL`.

### B0413 — Geometría Analítica Ampliada (49r)
Subtemas: `RECTA_ECUACIONES`, `RECTA_RELACIONES`, `CIRCUNFERENCIA_ANALITICA`, `POSICIONES_RECTAS_CIRCUNFERENCIAS`, `PARABOLA_ANALITICA`, `ELIPSE_ANALITICA`.

---

## Naming de archivos YAML

Patrón: `mat-geo-{subtema-kebab}-{concepto-kebab}.yaml`

Ejemplos:
- `MAT.GEO.ANGULOS_FUNDAMENTOS.DEFINICION_RAYOS` → `mat-geo-angulos-fundamentos-definicion-rayos.yaml`
- `MAT.GEO.PITAGORAS.ENUNCIADO` → `mat-geo-pitagoras-enunciado.yaml`
- `MAT.GEO.HOMOTECIA.DEFINICION` → `mat-geo-homotecia-definicion.yaml`
- `MAT.GEO.TRIG_FUNDAMENTAL.SENO_DEFINICION` → `mat-geo-trig-fundamental-seno-definicion.yaml`
- `MAT.GEO.CIRCUNFERENCIA_ANALITICA.CENTRO_ORIGEN` → `mat-geo-circunferencia-analitica-centro-origen.yaml`

## Naming de archivos JSONL

Patrón: `mat-geo-{bloque-descriptor}-banco-gen-{N}.jsonl`

Ejemplos:
- `mat-geo-angulos-banco-gen-1.jsonl` (B0401, tanda 1)
- `mat-geo-triangulos-banco-gen-2.jsonl` (B0402, tanda 2)
- `mat-geo-trigonometria-ampliada-banco-gen-1.jsonl` (B0412, tanda 1)

---

## Proceso de ejecución por bloque

1. Ejecutar la query de pendientes → lista de semantic_ids
2. Agrupar en tandas de 5 por subtema
3. Para cada tanda: YAML → JSONL → `load_node_content` → `load_exercise_bank` → verificar → commit
4. Verificar cobertura del bloque antes de avanzar al siguiente

---

## Verificación de cobertura total

```bash
python manage.py shell -c "
from apps.content.models import KnowledgeNode
bloques = ['B0401','B0402','B0403','B0404','B0405','B0406',
           'B0407','B0408','B0409','B0410','B0411','B0412','B0413']
for b in bloques:
    sid = f'MAT.GEO.{b}'
    r = KnowledgeNode.objects.filter(node_type='recurso', parent__parent__semantic_id=sid)
    done = r.filter(content__isnull=False).count()
    print(f'{sid}: {done}/{r.count()}')
"
```

## Criterios de aceptación

- [ ] 482/482 recursos con `NodeContent` (13 bloques)
- [ ] Cada recurso: 10 ejercicios (3+1+3+3)
- [ ] `python manage.py check` sin errores
- [ ] No se tocó código ni archivos de otros ejes
