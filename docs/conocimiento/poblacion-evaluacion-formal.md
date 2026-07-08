# Población de evaluación formal (F4) — procedimiento estándar

> Procedimiento para poblar `NodeAssessmentQuestion` (evaluación de 3 niveles por recurso, ver
> `docs/backlog/6-finalizados/kb-f4-evaluacion-formal.md`). A diferencia de `estrategia-poblacion.md`
> (banco de práctica, flujo manual NotebookLM → ChatGPT → YAML), esto es **100% automático**: un
> comando de Django llama a la IA directamente y guarda. Cualquiera de las tres IAs (Claude, Codex,
> Antigravity) puede ejecutar este mismo procedimiento con los mismos resultados.

## Decisiones ya cerradas (no volver a preguntar)

- **Publicación directa** (`--publish`): las preguntas generadas quedan disponibles para rendir de
  inmediato, sin cola de revisión editorial previa. Mismo criterio que el resto del banco de
  contenido de este proyecto.
- **Se corre contra producción** (Railway), no en local — el objetivo es que los alumnos reales
  tengan preguntas, no poblar una sqlite descartable.
- **Piloto primero**: bloque `MAT.NUM.ENTEROS` (36 recursos) antes de escalar al resto del árbol.

## Prerrequisito: sesión de Railway autenticada

`railway whoami` puede fallar con `invalid_grant` si el token expiró. Quien vaya a ejecutar esto
corre primero, en su propia terminal (requiere navegador, no lo puede hacer una IA sola):

```bash
railway login
railway link   # si el proyecto no está ya enlazado en este directorio
```

## Comando

```bash
# 1. Dry-run SIEMPRE primero — muestra el déficit sin gastar cuota de IA
railway run python manage.py generate_node_assessment_questions --node MAT.NUM.ENTEROS_CONJUNTO.NATURALES --dry-run

# 2. Un nodo puntual, publicado directo
railway run python manage.py generate_node_assessment_questions --node <semantic_id> --publish

# 3. Un bloque completo: no existe filtro por bloque en el comando (solo --node/--all).
#    Iterar sobre los semantic_id del bloque, uno por uno, o pedir que se agregue --bloque
#    si esto se vuelve rutina (no construir la opción hasta que haga falta de verdad).
#    Bash: for id in <lista>; do railway run python manage.py generate_node_assessment_questions --node "$id" --publish; done

# 4. Todo el árbol (recién después de validar el piloto)
railway run python manage.py generate_node_assessment_questions --all --publish
```

### Lista de `semantic_id` del bloque piloto (`MAT.NUM.ENTEROS`, 36 recursos)

```
MAT.NUM.ENTEROS_CONJUNTO.NATURALES
MAT.NUM.ENTEROS_CONJUNTO.CARDINALES
MAT.NUM.ENTEROS_CONJUNTO.DEFINICION
MAT.NUM.ENTEROS_CONJUNTO.POSITIVOS_NEGATIVOS
MAT.NUM.ENTEROS_CONJUNTO.RECTA_UBICACION
MAT.NUM.ENTEROS_CONJUNTO.RECTA_CONVENCION
MAT.NUM.ENTEROS_CONJUNTO.ORDEN_LOGICA
MAT.NUM.ENTEROS_CONJUNTO.TRICOTOMIA
MAT.NUM.ENTEROS_CONJUNTO.VALOR_ABSOLUTO_DEF
MAT.NUM.ENTEROS_CONJUNTO.VALOR_ABSOLUTO_NOTACION
MAT.NUM.ENTEROS_CONJUNTO.VALOR_ABSOLUTO_OPUESTOS
MAT.NUM.ENTEROS_CONJUNTO.PARES
MAT.NUM.ENTEROS_CONJUNTO.IMPARES
MAT.NUM.ENTEROS_CONJUNTO.SUCESOR
MAT.NUM.ENTEROS_CONJUNTO.ANTECESOR
MAT.NUM.ENTEROS_OPERATORIA.ADICION_IGUAL_SIGNO
MAT.NUM.ENTEROS_OPERATORIA.ADICION_DISTINTO_SIGNO
MAT.NUM.ENTEROS_OPERATORIA.CONMUTATIVA_ADICION
MAT.NUM.ENTEROS_OPERATORIA.ASOCIATIVA_ADICION
MAT.NUM.ENTEROS_OPERATORIA.NEUTRO_ADITIVO
MAT.NUM.ENTEROS_OPERATORIA.INVERSO_ADITIVO
MAT.NUM.ENTEROS_OPERATORIA.SUSTRACCION_REGLA
MAT.NUM.ENTEROS_OPERATORIA.MULT_SIGNOS_IGUALES
MAT.NUM.ENTEROS_OPERATORIA.MULT_SIGNOS_DISTINTOS
MAT.NUM.ENTEROS_OPERATORIA.CONMUTATIVA_MULT
MAT.NUM.ENTEROS_OPERATORIA.ASOCIATIVA_MULT
MAT.NUM.ENTEROS_OPERATORIA.NEUTRO_MULT
MAT.NUM.ENTEROS_OPERATORIA.ABSORBENTE_CERO
MAT.NUM.ENTEROS_OPERATORIA.DISTRIBUTIVA_MULT_ADICION
MAT.NUM.ENTEROS_OPERATORIA.DIV_SIGNOS_IGUALES
MAT.NUM.ENTEROS_OPERATORIA.DIV_SIGNOS_DISTINTOS
MAT.NUM.ENTEROS_OPERATORIA.DIVISION_POR_CERO
MAT.NUM.ENTEROS_OPERATORIA.PAPOMUDAS_ORDEN
MAT.NUM.ENTEROS_OPERATORIA.PARENTESIS_MAS
MAT.NUM.ENTEROS_OPERATORIA.PARENTESIS_MENOS
MAT.NUM.ENTEROS_OPERATORIA.PARENTESIS_ANIDADOS
```
```

- `--dry-run` no llama a la IA: solo informa cuántas preguntas faltan por nivel.
- Es idempotente (`generation_key`): re-correr no duplica lo ya generado.
- Ritmo fijo de **6 segundos entre llamadas a la IA** (no configurable por flag hoy) para no
  saturar la cuota — está en `DEFAULT_REQUEST_INTERVAL_SECONDS` de
  `generate_node_assessment_questions.py`.

## Dimensionamiento (para decidir cuánto correr por sesión)

| Alcance | Recursos | Llamadas IA (3 niveles c/u) | Tiempo mínimo (solo espera, sin latencia real) |
|---|---|---|---|
| Piloto — MAT.NUM.ENTEROS | 36 | 108 | ~11 min |
| Árbol completo (MAT) | 1.911 | 5.733 | ~9.5 h |

El árbol completo **no se corre de una sola sesión** — trocear por bloque, en el mismo orden de
prioridad ya definido en `estrategia-poblacion.md §Orden de prioridad de bloques`, respetando la
cuota gratuita de Gemini si no hay plan pago (se resetea a medianoche hora Pacífico).

## Control de calidad post-piloto (obligatorio antes de escalar)

Como la publicación es directa (sin cola de revisión), después del piloto alguien debe revisar a
ojo una muestra antes de seguir con más bloques:

1. En el admin (`/admin/content/nodeassessmentquestion/`), filtrar por el nodo piloto y leer 5-10
   preguntas al azar de cada nivel: ¿el enunciado tiene sentido? ¿la alternativa marcada correcta
   realmente lo es? ¿el LaTeX renderiza bien (KaTeX)?
2. En el navegador, rendir una evaluación real en un nodo del piloto y confirmar que la sección
   "Evaluación de dominio" funciona de punta a punta (formulario → envío → resultado → estrellas).
3. Si algo falla sistemáticamente (ej. LaTeX mal escapado, nivel 3 con preguntas de nivel 1), NO
   seguir escalando — hay que ajustar el prompt en `_build_node_assessment_prompt`
   (`apps/content/services/ai_generation_service.py`) primero.

## Registro de avance

| Bloque | Recursos | Preguntas generadas | Estado |
|---|---|---|---|
| MAT.NUM.ENTEROS (piloto) | 36 | 0/108 | ⚪ Pendiente |
| *(resto del árbol, mismo orden que estrategia-poblacion.md)* | ~1.875 | 0 | ⚪ Pendiente |

> Actualizar esta tabla a medida que se completan bloques.
