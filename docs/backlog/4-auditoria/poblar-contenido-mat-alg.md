# Poblar contenido: MAT.ALG — Álgebra y Funciones

## Metadata
- **Estado:** `698/698` recursos poblados — MAT.ALG.B0301–B0315 completo. B0301–B0308 auditados por Codex;
  B0309–B0315 pendientes de auditoría.
- **Dueño actual:** por asignar auditoría de B0309–B0315 (Codex)
- **Scope:** 698 recursos — 15 bloques (B0301–B0315)
- **Rama:** `content/mat-alg-b0309`
- **Fecha:** 2026-06-28

### Avance auditado — 2026-07-01

- B0301–B0308: `300/300` recursos con estructura completa y contenido cargado.
- B0309: `65/65` recursos poblados con YAMLs y JSONL ejercicios.
- B0308 tandas 3–7: `350/350` ejercicios placeholder reemplazados sobre sus IDs originales.

### Cierre del scope global — 2026-07-02

- **B0310–B0315 poblados: `291/291` recursos** (B0310 Funciones 82, B0311 Ec. 2º grado 41, B0312 Func. Cuadrática 47,
  B0313 Func. Exp/Log 54, B0314 Func. Potencia 50, B0315 Func. Trigonométrica 59), vía `/loop` autónomo.
- **MAT.ALG.B0301–B0315 queda 100% poblado: `698/698` recursos.** Detalle de B0313–B0315 (143 recursos, última
  tanda de esta sesión) en `reportes-sesion/2026-07-02.md`.
- `check` OK y suite completa `python manage.py test` — 617 tests OK (1 skip), sin regresiones, verificada al
  cerrar cada bloque completo (B0313, B0314, B0315).
- **Pendiente:** auditoría de Codex para B0309–B0315 (B0301–B0308 ya auditados) y apertura del PR de
  `content/mat-alg-b0309` a `main`.

---

## Antes de empezar — lee estos documentos

1. `docs/backlog/2-arquitectura/poblar-contenido-mat-num-b0201-b0202.md` — proceso completo, reglas YAML/JSONL, formato `stable_id`, criterios de aceptación.
2. `docs/conocimiento/pauta-contenido.md` — 9 campos obligatorios + 10 ejercicios por recurso.
3. Ejemplos de estilo: `mat-num-divisibilidad-multiplo-concepto.yaml` y `mat-num-teoria-numeros-banco-gen-1.jsonl`.

**Fuente matemática:** Álgebra cubre 7° Básico a 4° Medio y preuniversitario. El agente tiene conocimiento suficiente para generar todo el contenido.

**Estrategia de ejecución:** Dado el volumen (698r, 15 bloques), procesar **un bloque completo por sesión de trabajo**, en orden B0301→B0315. Cada bloque tiene entre 28 y 82 recursos.

---

## Obtener lista de pendientes por bloque (ejecutar al inicio de cada bloque)

```bash
python manage.py shell -c "
from apps.content.models import KnowledgeNode
bloque_id = 'MAT.ALG.B0301'  # <-- cambiar por el bloque que toca
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
| MAT.ALG.B0301 | 34 | Nomenclatura y Conceptos Algebraicos | 7 |
| MAT.ALG.B0302 | 36 | Lenguaje Algebraico y Valorización | 7 |
| MAT.ALG.B0303 | 30 | Operaciones Algebraicas | 6 |
| MAT.ALG.B0304 | 28 | Multiplicación Algebraica | 6 |
| MAT.ALG.B0305 | 32 | Productos Notables | 7 |
| MAT.ALG.B0306 | 39 | Factorización | 8 |
| MAT.ALG.B0307 | 48 | MCD, MCM y Fracciones Algebraicas | 10 |
| MAT.ALG.B0308 | 53 | Ecuaciones de Primer Grado y Sistemas | 11 |
| MAT.ALG.B0309 | 65 | Desigualdades e Inecuaciones | 13 |
| MAT.ALG.B0310 | 82 | Funciones | 17 |
| MAT.ALG.B0311 | 41 | Ecuaciones de Segundo Grado | 9 |
| MAT.ALG.B0312 | 47 | Función Cuadrática | 10 |
| MAT.ALG.B0313 | 54 | Funciones Exponencial y Logarítmica | 11 |
| MAT.ALG.B0314 | 50 | Función Potencia | 10 |
| MAT.ALG.B0315 | 59 | Función Trigonométrica | 12 |
| **TOTAL** | **698** | | **~144 tandas** |

---

## Guía de subtemas por bloque (para agrupar tandas)

### B0301 — Nomenclatura (34r)
Subtemas: `FUNDAMENTOS`, `TERMINO`, `EXPRESIONES`, `POLINOMIOS`, `COEFICIENTE`, `VARIABLE`, `GRADO_TERMINO`.

### B0302 — Lenguaje Algebraico (36r)
Subtemas: `LENGUAJE_OPERACIONES`, `LENGUAJE_RELACIONES`, `VALORIZACION`.

### B0303 — Operaciones Algebraicas (30r)
Subtemas: `SIMILARIDAD`, `REDUCCION_OPERATIVA`, `AGRUPACION`, `ADICION_POL`, `SUSTRACCION_POL`, `MULTIPLICACION_POL_SIMPLE`.

### B0304 — Multiplicación Algebraica (28r)
Subtemas: `LEYES_MULTIPLICACION`, `MULT_MONOMIOS`, `MULT_MON_POL`, `MULT_POLINOMIOS`, `DIVISION_POLINOMIOS`.

### B0305 — Productos Notables (32r)
Subtemas: `CUADRADO_BINOMIO`, `SUMA_DIFERENCIA`, `TERMINO_COMUN`, `CUBO_BINOMIO`, `BINOMIO_NEWTON`.

### B0306 — Factorización (39r)
Subtemas: `FACTOR_COMUN`, `FACTOR_AGRUPACION`, `FACTOR_CUADRADOS`, `FACTOR_TRINOMIOS`, `FACTOR_CUBO`, `ESTRATEGIA_GLOBAL`.

### B0307 — MCD, MCM y Fracciones Algebraicas (48r)
Subtemas: `MCD_ALGEBRAICO`, `MCM_ALGEBRAICO`, `FRACCIONES_BASE`, `FRACCIONES_MULT`, `FRACCIONES_DIV`, `FRACCIONES_SUMA`, `FRACCIONES_SIMPLIFICACION`.

### B0308 — Ecuaciones de Primer Grado y Sistemas (53r)
Subtemas: `ECUACION_BASE`, `RESOLUCION_LINEAL`, `ECUACIONES_FRACCIONARIAS`, `ECUACIONES_LITERALES`, `SISTEMAS_LINEALES`, `METODOS_SISTEMAS`, `PROBLEMAS_CONTEXTO`.

### B0309 — Desigualdades e Inecuaciones (65r)
Subtemas: `ORDEN_FUNDAMENTOS`, `DESIG_PROPIEDADES`, `INTERVALOS`, `INECUACIONES_LINEALES`, `INECUACIONES_CUADRATICAS`, `SISTEMAS_INECUACIONES`, `VALOR_ABSOLUTO_INEC`.

### B0310 — Funciones (82r)
Subtemas: `FUNCION_CONCEPTOS`, `FUNCION_EVALUACION`, `FUNCION_REPRESENTACION`, `FUNCION_RECTAS_BASE`, `FUNCION_LINEAL`, `FUNCION_AFIN`, `FUNCION_INVERSA`, `COMPOSICION`, `DOMINIO_RECORRIDO`, `PARIDAD`.

### B0311 — Ecuaciones de Segundo Grado (41r)
Subtemas: `EC_CUADR_BASE`, `EC_CUADR_RESOL_FACTOR`, `EC_CUADR_METODOS`, `EC_CUADR_DISCRIMINANTE`, `EC_CUADR_APLICACIONES`, `RELACIONES_VIETA`.

### B0312 — Función Cuadrática (47r)
Subtemas: `FUNC_CUADR_BASE`, `FUNC_CUADR_GRAFICA`, `FUNC_CUADR_VERTICE`, `FUNC_CUADR_FORMAS`, `FUNC_CUADR_INTERSECCIONES`, `FUNC_CUADR_TRANSFORMACIONES`, `FUNC_CUADR_APLICACIONES`.

### B0313 — Funciones Exponencial y Logarítmica (54r)
Subtemas: `FUNC_EXPONENCIAL_BASE`, `FUNC_EXPONENCIAL_GRAFICA`, `LOGARITMOS_PROPIEDADES`, `FUNC_LOGARITMICA_BASE`, `FUNC_LOGARITMICA_GRAFICA`, `ECUACIONES_EXP_LOG`, `APLICACIONES_EXP_LOG`.

### B0314 — Función Potencia (50r)
Subtemas: `FUNC_POTENCIA_BASE`, `FUNC_POTENCIA_ENTERA_POSITIVA`, `FUNC_POTENCIA_NEG_FRAC`, `FUNC_POTENCIA_TRANSFORM`, `FUNC_RAIZ`, `APLICACIONES_POTENCIA`.

### B0315 — Función Trigonométrica (59r)
Subtemas: `TRIG_CIRCULO_ANGULOS`, `TRIG_COORDENADAS`, `FUNC_SENO_ANALISIS`, `FUNC_COSENO_ANALISIS`, `FUNC_TANGENTE_ANALISIS`, `TRIG_IDENTIDADES_ALG`, `ECUACIONES_TRIG`, `FUNC_TRIG_INVERSAS`.

---

## Naming de archivos YAML

Patrón: `mat-alg-{subtema-kebab}-{concepto-kebab}.yaml`

Ejemplos:
- `MAT.ALG.FUNDAMENTOS.DEFINICION_ALGEBRA` → `mat-alg-fundamentos-definicion-algebra.yaml`
- `MAT.ALG.CUADRADO_BINOMIO.SUMA_DEFINICION` → `mat-alg-cuadrado-binomio-suma-definicion.yaml`
- `MAT.ALG.SISTEMAS_LINEALES.METODO_SUSTITUCION` → `mat-alg-sistemas-lineales-metodo-sustitucion.yaml`
- `MAT.ALG.FUNC_SENO_ANALISIS.DEFINICION_FUNCIONAL` → `mat-alg-func-seno-analisis-definicion-funcional.yaml`

## Naming de archivos JSONL

Patrón: `mat-alg-{bloque-descriptor}-banco-gen-{N}.jsonl`

Ejemplos:
- `mat-alg-nomenclatura-banco-gen-1.jsonl` (B0301, tanda 1)
- `mat-alg-ecuaciones-primer-grado-banco-gen-3.jsonl` (B0308, tanda 3)
- `mat-alg-funciones-banco-gen-7.jsonl` (B0310, tanda 7)

---

## Proceso de ejecución por bloque

1. Ejecutar la query de pendientes para el bloque → obtener lista de semantic_ids
2. Agrupar en tandas de 5 por subtema (usar el prefijo del semantic_id como agrupador)
3. Para cada tanda: generar YAMLs → generar JSONL → `load_node_content` → `load_exercise_bank` → verificar → commit
4. Al terminar el bloque, verificar cobertura del bloque antes de pasar al siguiente

---

## Verificación de cobertura total

```bash
python manage.py shell -c "
from apps.content.models import KnowledgeNode
bloques = ['B0301','B0302','B0303','B0304','B0305','B0306','B0307','B0308',
           'B0309','B0310','B0311','B0312','B0313','B0314','B0315']
for b in bloques:
    sid = f'MAT.ALG.{b}'
    r = KnowledgeNode.objects.filter(node_type='recurso', parent__parent__semantic_id=sid)
    done = r.filter(content__isnull=False).count()
    print(f'{sid}: {done}/{r.count()}')
"
```

## Criterios de aceptación

- [ ] 698/698 recursos con `NodeContent` (15 bloques)
- [ ] Cada recurso: 10 ejercicios (3+1+3+3)
- [ ] `python manage.py check` sin errores
- [ ] No se tocó código ni archivos de otros ejes
