# Prompt-plantilla para generar bloques de la Biblioteca de Conocimiento

> Úsalo en NotebookLM (grounded en los libros) o ChatGPT. Para cada bloque nuevo solo cambias
> los 3 datos del recuadro `>>> DATOS DE ESTE BLOQUE <<<`. **El dato clave es "EMPIEZA EN EL
> TEMA 02.XX"** — evita el 90% de los errores (colisión de códigos). Próximo código libre: ver
> `_REGISTRO-CODIGOS.md`.

```
Continúa la Biblioteca de Conocimiento de Matemática. Genera UN bloque nuevo respetando AL PIE
DE LA LETRA el estándar de los bloques anteriores. No regeneres lo ya hecho.

>>> DATOS DE ESTE BLOQUE (lo único que cambia cada vez) <<<
- RAMA: 02 NÚMEROS  (abreviatura NUM)
- BLOQUE A GENERAR: «Razones, Proporciones y Porcentajes (+ Matemática Financiera)»
- EMPIEZA EN EL TEMA: 02.34   ← CRÍTICO: los códigos anteriores YA están ocupados.
  Numera los temas correlativos desde ahí. NO reutilices códigos previos.

>>> NOMENCLATURA (fija) <<<
- Tema:    codigo "02.TT"  + id MAT.NUM.<TEMA_ID>
- Recurso: cod "02.TT.rr"  + id MAT.NUM.<TEMA_ID>.<SLUG>
- El id del recurso DEBE empezar con el id COMPLETO de su tema (no lo aplanes).
- El id es la llave estable; el cod es solo orden. SLUG en MAYÚSCULAS, describe la idea, no el número.

>>> TRES EJES POR RECURSO (ortogonales) <<<
- dificultad: basica | media | avanzada   (complejidad cognitiva)
- competencia: M1 | M2 | U  (M1 común PAES · M2 específica PAES · U fuera de temario PAES).
  Se declara en el tema y se hereda; ponla inline SOLO si el recurso difiere.
- cursos: lista [1B..8B, 1M..4M]  (dónde se introduce/revisita; currículo espiral).
- Comentario "# Fuente: ..." cuando el recurso venga de un libro cargado.

>>> REGLAS DE CONTENIDO <<<
- ATOMIZACIÓN MÁXIMA: 1 recurso = 1 idea = 1 video. Separa todo "A y B / , / o".
  PERO no separes conceptos espejados que sean el mismo procedimiento (esos = 1 recurso).
- ANTI-DUPLICADO: no redefinas un recurso que ya exista en un bloque anterior; si una idea ya
  tiene id, omítela aquí.
- NO incluyas el campo "prerrequisitos" todavía (se hará en una pasada final aparte).
- Lo que el temario PAES pida pero no esté en las fuentes: ponlo al final en una sección "GAPS".

>>> FLUJO <<<
1. Primero dame en 2-3 líneas la lista de temas (02.34, 02.35, …) que propondrás.
2. Luego entrega el bloque COMPLETO en YAML, con la cabecera (rama/codigo/abreviatura/temas).
3. Espera mi visto bueno antes de pasar al siguiente bloque.
```
