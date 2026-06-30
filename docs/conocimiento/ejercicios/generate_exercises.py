import json
import os

def generate():
    # Tanda B01-3
    tanda_1 = []

    # 1. TABLA_NEGACION (TNEG)
    sem_id = "MAT.FUND.TABLAS_VERDAD.TABLA_NEGACION"
    abbr = "TNEG"

    # conceptuales (3)
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-1", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿Qué función cumple el conectivo de negación lógica?",
        "choices": [
            "Invertir el valor de verdad de una proposición",
            "Duplicar el valor de verdad de una proposición",
            "Unir dos proposiciones mediante el operador 'y'",
            "Demostrar que una proposición siempre es verdadera"
        ],
        "correct_answer": "Invertir el valor de verdad de una proposición",
        "solution_steps": "La negación lógica es un conectivo unario que invierte el valor de verdad de la proposición original. Si $p$ es verdadera, $\\neg p$ es falsa; si $p$ es falsa, $\\neg p$ es verdadera.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-2", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "Si una proposición $p$ es verdadera, ¿cuál es el valor de verdad de $\\neg(\\neg(\\neg p))$?",
        "choices": ["Falso", "Verdadero", "Contingente", "No se puede determinar"],
        "correct_answer": "Falso",
        "solution_steps": "Evaluando secuencialmente de adentro hacia afuera: como $p$ es $V$, la primera negación $\\neg p$ es $F$. La segunda negación $\\neg(\\neg p)$ vuelve a ser $V$. La tercera negación $\\neg(\\neg(\\neg p))$ es $F$.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-3", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "Si la proposición $p$ representa 'La Luna es de queso', ¿cómo se denota simbólicamente su negación?",
        "choices": ["$\\neg p$", "$p \\land p$", "$p \\lor p$", "$p \\rightarrow p$"],
        "correct_answer": "$\\neg p$",
        "solution_steps": "La negación lógica se representa mediante el símbolo $\\neg$ antepuesto a la variable proposicional, resultando en $\\neg p$.",
        "status": "ready", "source_kind": "manual"
    })

    # reconocimiento (1)
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-REC-1", "semantic_id": sem_id, "item_group": "reconocimiento",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "Identifique cuál de las siguientes opciones describe correctamente la tabla de verdad para $\\neg p$.",
        "choices": [
            "Si $p$ es $V$ entonces $\\neg p$ es $F$; si $p$ es $F$ entonces $\\neg p$ es $V$",
            "Si $p$ es $V$ entonces $\\neg p$ es $V$; si $p$ es $F$ entonces $\\neg p$ es $F$",
            "Si $p$ es $V$ entonces $\\neg p$ es $F$; si $p$ es $F$ entonces $\\neg p$ es $F$",
            "Si $p$ es $F$ entonces $\\neg p$ es $V$; si $p$ es $V$ entonces $\\neg p$ es $V$"
        ],
        "correct_answer": "Si $p$ es $V$ entonces $\\neg p$ es $F$; si $p$ es $F$ entonces $\\neg p$ es $V$",
        "solution_steps": "La tabla de verdad de la negación invierte los valores de verdad: el valor resultante es siempre el contrario del original.",
        "status": "ready", "source_kind": "manual"
    })

    # procedimiento_basico (3)
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-1", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que si $p$ es Falso, entonces $\\neg p$ es Verdadero?",
        "correct_answer": "Verdadero",
        "solution_steps": "Por definición, el operador de negación lógica invierte el valor de Falso ($F$) a Verdadero ($V$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-2", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que $\\neg(\\neg p)$ siempre tiene el valor de verdad opuesto a $p$?",
        "correct_answer": "Falso",
        "solution_steps": "Por la ley de la doble negación, $\\neg(\\neg p) \\equiv p$. Por lo tanto, tiene exactamente el mismo valor de verdad que $p$, no el opuesto.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-3", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que la negación de una tautología es una contradicción?",
        "correct_answer": "Verdadero",
        "solution_steps": "Una tautología es siempre verdadera ($V$). Al negarla, todos sus valores se convierten en Falso ($F$), lo que por definición corresponde a una contradicción.",
        "status": "ready", "source_kind": "manual"
    })

    # tipo_paes (3)
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-1", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Una alarma de seguridad se activa si y solo si la proposición $p$: 'La puerta está cerrada' es falsa. Si denotamos por $p$ a dicha proposición, ¿cuál de las siguientes opciones representa formalmente la condición lógica para que la alarma se encienda?",
        "choices": ["$\\neg p$", "$p$", "$p \\lor \\neg p$", "$p \\land \\neg p$"],
        "correct_answer": "$\\neg p$",
        "solution_steps": "La alarma se enciende cuando $p$ es falsa, lo que equivale a decir que su negación $\\neg p$ es verdadera. Por lo tanto, la condición formal de activación es $\\neg p$.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-2", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Considera la proposición $p$: 'El candidato A ganará la elección'. ¿Cuál de las siguientes afirmaciones en lenguaje natural expresa correctamente la negación de $p$ en lógica proposicional?",
        "choices": [
            "No es cierto que el candidato A ganará la elección",
            "El candidato A perderá por muchos votos",
            "El candidato B ganará la elección",
            "Ningún candidato ganará la elección"
        ],
        "correct_answer": "No es cierto que el candidato A ganará la elección",
        "solution_steps": "La negación de una proposición $p$ niega la veracidad del enunciado completo, lo que se traduce formalmente como 'No es cierto que $p$'. Decir que el candidato B ganará o que perderá por mucho introduce información adicional que no es lógicamente equivalente a simplemente negar $p$.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-3", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "En un circuito de control lógico, la señal de salida es el resultado de negar la entrada $A$. Si la entrada $A$ es verdadera ($V$), ¿cuál de las siguientes afirmaciones describe de manera correcta el comportamiento del circuito?",
        "choices": [
            "La señal de salida será falsa porque el inversor lógico cambia el estado de verdadero a falso",
            "La señal de salida será verdadera porque la negación conserva el valor de verdad en circuitos de entrada única",
            "La señal de salida será inestable ya que una sola entrada requiere dos negaciones para definirse",
            "La señal de salida será verdadera porque la corriente eléctrica se duplica"
        ],
        "correct_answer": "La señal de salida será falsa porque el inversor lógico cambia el estado de verdadero a falso",
        "solution_steps": "El circuito realiza la función de negación lógica. Si la entrada es verdadera ($V$), al aplicar el operador de negación $\\neg A$ el resultado es Falso ($F$).",
        "status": "ready", "source_kind": "manual"
    })

    # 2. TABLA_CONJUNCION (TCONJ)
    sem_id = "MAT.FUND.TABLAS_VERDAD.TABLA_CONJUNCION"
    abbr = "TCONJ"

    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-1", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿Bajo qué única condición es verdadera la conjunción $p \\land q$?",
        "choices": [
            "Cuando tanto $p$ como $q$ son verdaderas",
            "Cuando al menos una de las dos es verdadera",
            "Cuando tanto $p$ como $q$ son falsas",
            "Cuando $p$ es verdadera y $q$ es falsa"
        ],
        "correct_answer": "Cuando tanto $p$ como $q$ son verdaderas",
        "solution_steps": "La conjunción lógica (operador 'y') exige rigurosamente que ambas proposiciones componentes sean verdaderas para resultar verdadera. En cualquier otro caso es falsa.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-2", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿Cuál es el resultado de evaluar la expresión $p \\land \\neg p$ para cualquier proposición $p$?",
        "choices": [
            "Falso en todos los casos",
            "Verdadero en todos los casos",
            "Depende del valor de verdad de $p$",
            "Es una contradicción solo si $p$ es falsa"
        ],
        "correct_answer": "Falso en todos los casos",
        "solution_steps": "Como una proposición $p$ y su negación $\\neg p$ tienen valores de verdad opuestos, una de ellas siempre será falsa. Por lo tanto, la conjunción $p \\land \\neg p$ siempre será falsa ($V \\land F \\equiv F$ o $F \\land V \\equiv F$), tratándose de una contradicción.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-3", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "Si se sabe que la proposición compuesta $p \\land q$ es verdadera, ¿qué se puede afirmar sobre las proposiciones $p$ y $q$?",
        "choices": [
            "Ambas son verdaderas",
            "Al menos una de ellas es verdadera",
            "Ambas son falsas",
            "No se puede afirmar nada sobre sus valores de verdad individuales"
        ],
        "correct_answer": "Ambas son verdaderas",
        "solution_steps": "Para que una conjunción sea verdadera, la única fila de la tabla de verdad que lo cumple es aquella donde tanto $p$ como $q$ son verdaderas ($V \\land V \\equiv V$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-REC-1", "semantic_id": sem_id, "item_group": "reconocimiento",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "Selecciona el valor de verdad correcto de la conjunción $p \\land q$ para la fila donde la variable $p$ es Falsa y la variable $q$ es Verdadera.",
        "choices": ["Falso", "Verdadero", "Contingente", "Invalido"],
        "correct_answer": "Falso",
        "solution_steps": "Evaluando $p \\land q$ con $p = F$ y $q = V$, tenemos $F \\land V$. Como uno de los componentes es falso, el resultado de la conjunción es Falso ($F$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-1", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que si $p$ es Verdadero y $q$ es Falso, la conjunción $p \\land q$ es Falsa?",
        "correct_answer": "Verdadero",
        "solution_steps": "Por la regla de la conjunción, si una de las proposiciones simples es falsa ($q = F$), entonces toda la conjunción $p \\land q$ es Falsa ($V \\land F \\equiv F$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-2", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que la conjunción es conmutativa, es decir, $p \\land q \\equiv q \\land p$?",
        "correct_answer": "Verdadero",
        "solution_steps": "La conjunción lógica es simétrica. El orden de las proposiciones no altera el resultado de su tabla de verdad, por lo que $p \\land q$ y $q \\land p$ son equivalentes.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-3", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que si $p \\land q$ es falso, entonces obligatoriamente tanto $p$ como $q$ deben ser falsas?",
        "correct_answer": "Falso",
        "solution_steps": "Para que la conjunción sea falsa, basta con que una sola de las proposiciones sea falsa (por ejemplo, si $p=V$ y $q=F$). No es necesario que ambas sean falsas.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-1", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Un sistema de riego automático se enciende si se cumplen simultáneamente dos condiciones: $p$: 'La humedad es menor al 40%' y $q$: 'La temperatura supera los 25 °C'. Si un día la humedad medida es del 35% y la temperatura registrada es de 22 °C, ¿cuál de las siguientes opciones describe de manera correcta el estado del riego y su justificación lógica?",
        "choices": [
            "El riego permanecerá apagado porque no se cumple la condición de temperatura, haciendo falsa la conjunción",
            "El riego se encenderá porque se cumple al menos la condición de humedad, haciendo verdadera la disyunción",
            "El riego permanecerá apagado porque ambas condiciones deben ser falsas para que el riego funcione",
            "El riego se encenderá porque la humedad del 35% es menor al 40% y la temperatura no influye"
        ],
        "correct_answer": "El riego permanecerá apagado porque no se cumple la condición de temperatura, haciendo falsa la conjunción",
        "solution_steps": "Dado que el sistema exige que ambas condiciones se cumplan simultáneamente ('y'), estamos ante una conjunción $p \\land q$. Como la temperatura (22 °C) no supera los 25 °C, $q$ es falsa. La conjunción $V \\land F$ es falsa, por lo que el sistema no se enciende.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-2", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "En una postulación a una beca de excelencia académica, se exige que el postulante sea menor de 25 años ($p$) y tenga un promedio de notas superior a 6.0 ($q$). Si Juan tiene 24 años y un promedio de notas de 5.8, ¿cuál de las siguientes expresiones formales representa la situación de Juan con respecto a los requisitos de la beca?",
        "choices": [
            "Se cumple $p$ pero no $q$, por lo que $p \\land q$ es falsa y no obtiene la beca",
            "Se cumple $q$ pero no $p$, por lo que $p \\land q$ es verdadera y obtiene la beca",
            "No se cumple ninguna de las condiciones, por lo que no obtiene la beca",
            "Se cumplen ambas condiciones, obteniendo la beca de forma automática"
        ],
        "correct_answer": "Se cumple $p$ pero no $q$, por lo que $p \\land q$ es falsa y no obtiene la beca",
        "solution_steps": "Juan tiene 24 años, lo cual es menor de 25 ($p$ es verdadera). Su promedio es 5.8, lo cual no es superior a 6.0 ($q$ es falsa). Como se exige la conjunción $p \\land q$ para obtener la beca, y esta resulta ser $V \\land F \\equiv F$, Juan no califica.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-3", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Si se sabe que la proposición compuesta $p \\land q$ es verdadera, ¿cuál de las siguientes proposiciones compuestas es obligatoriamente verdadera?",
        "choices": ["$p \\lor \\neg q$", "$\\neg p \\land q$", "$\\neg p \\lor \\neg q$", "$p \\oplus q$"],
        "correct_answer": "$p \\lor \\neg q$",
        "solution_steps": "Si $p \\land q$ es verdadera, entonces $p$ es verdadera ($V$) y $q$ es verdadera ($V$). Evaluamos las opciones:\n- $p \\lor \\neg q \\equiv V \\lor F \\equiv V$ (Verdadera).\n- $\\neg p \\land q \\equiv F \\land V \\equiv F$ (Falsa).\n- $\\neg p \\lor \\neg q \\equiv F \\lor F \\equiv F$ (Falsa).\n- $p \\oplus q \\equiv V \\oplus V \\equiv F$ (Falsa).",
        "status": "ready", "source_kind": "manual"
    })

    # 3. TABLA_DISYUNCION_INCLUSIVA (TDINC)
    sem_id = "MAT.FUND.TABLAS_VERDAD.TABLA_DISYUNCION_INCLUSIVA"
    abbr = "TDINC"

    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-1", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿En qué único caso la disyunción inclusiva $p \\lor q$ resulta ser falsa?",
        "choices": [
            "Cuando tanto $p$ como $q$ son falsas",
            "Cuando al menos una de las dos es verdadera",
            "Cuando tanto $p$ como $q$ son verdaderas",
            "Cuando $p$ es falsa y $q$ es verdadera"
        ],
        "correct_answer": "Cuando tanto $p$ como $q$ son falsas",
        "solution_steps": "La disyunción inclusiva (operador 'o') da como resultado verdadero si al menos uno de sus componentes lo es. Solo resulta falsa cuando ambos componentes son falsos ($F \\lor F \\equiv F$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-2", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿Qué significa que el conectivo 'o' sea inclusivo en lógica proposicional?",
        "choices": [
            "Que permite que ambas proposiciones sean verdaderas al mismo tiempo",
            "Que excluye la posibilidad de que ambas proposiciones sean verdaderas",
            "Que exige que el antecedente sea verdadero",
            "Que une las proposiciones para formar una contradicción"
        ],
        "correct_answer": "Que permite que ambas proposiciones sean verdaderas al mismo tiempo",
        "solution_steps": "La palabra 'inclusivo' hace referencia a que la disyunción $p \\lor q$ sigue siendo verdadera si ambos componentes son verdaderos ($V \\lor V \\equiv V$), a diferencia de la disyunción exclusiva.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-3", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "Si se sabe que la disyunción inclusiva $p \\lor q$ es verdadera y la variable $q$ es falsa, ¿qué valor de verdad debe tener obligatoriamente la variable $p$?",
        "choices": ["Verdadero", "Falso", "Contingente", "No se puede determinar"],
        "correct_answer": "Verdadero",
        "solution_steps": "Para que $p \\lor q$ sea verdadera, se necesita que al menos una variable sea verdadera. Si $q$ es falsa, la única forma de que se cumpla la disyunción es que $p$ sea Verdadera ($V$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-REC-1", "semantic_id": sem_id, "item_group": "reconocimiento",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "Selecciona el valor de verdad correcto de la disyunción inclusiva $p \\lor q$ para la fila donde $p$ es Verdadera y $q$ es Falsa.",
        "choices": ["Verdadero", "Falso", "Contingente", "Nulo"],
        "correct_answer": "Verdadero",
        "solution_steps": "Evaluamos $p \\lor q$ con $p=V$ y $q=F$. Al ser al menos una de las proposiciones verdadera, el resultado de la disyunción inclusiva es Verdadero ($V$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-1", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que la disyunción inclusiva de una proposición verdadera y una falsa es verdadera?",
        "correct_answer": "Verdadero",
        "solution_steps": "Sí, de acuerdo con la tabla de verdad de la disyunción inclusiva, basta que al menos uno de los términos sea verdadero para que el resultado sea Verdadero ($V \\lor F \\equiv V$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-2", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que si $p \\lor q$ es verdadera, entonces obligatoriamente ambas variables deben ser verdaderas?",
        "correct_answer": "Falso",
        "solution_steps": "La disyunción inclusiva es verdadera incluso si solo uno de sus componentes lo es (ej: $p=V, q=F$). No requiere que ambos lo sean.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-3", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que la proposición $p \\lor \\neg p$ es verdadera para cualquier proposición $p$?",
        "correct_answer": "Verdadero",
        "solution_steps": "Sí, una proposición $p$ y su negación $\\neg p$ tienen valores contrarios, por lo que una de ellas es siempre verdadera. Así, la disyunción $p \\lor \\neg p$ es siempre verdadera, representando la ley del tercero excluido.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-1", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Para entrar a un concierto de música, los asistentes deben cumplir con presentar al menos uno de los siguientes documentos: entrada digital ($p$) o entrada física ($q$). Si una persona llega al control con ambos documentos (digital y físico), ¿cuál de las siguientes afirmaciones describe de manera correcta su situación de ingreso?",
        "choices": [
            "Podrá ingresar porque la disyunción inclusiva es verdadera cuando ambos componentes son verdaderos",
            "No podrá ingresar porque al tener ambos documentos se genera un conflicto de disyunción exclusiva",
            "Podrá ingresar únicamente si anula la entrada física, ya que en lógica no se permiten dos entradas verdaderas",
            "No podrá ingresar porque la regla exige estrictamente tener uno solo de los dos formatos"
        ],
        "correct_answer": "Podrá ingresar porque la disyunción inclusiva es verdadera cuando ambos componentes son verdaderos",
        "solution_steps": "La regla de acceso utiliza el conectivo 'o' de forma inclusiva (presentar 'al menos uno'). En lógica, esto se representa como la disyunción inclusiva $p \\lor q$. Como la persona tiene ambos documentos, se evalúa $V \\lor V \\equiv V$, por lo que su ingreso es válido.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-2", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Un sistema informático de alerta temprana envía un mensaje si la temperatura del servidor supera los 80 °C ($p$) o si el porcentaje de memoria RAM utilizada supera el 95% ($q$). Si en un instante la temperatura registrada es de 82 °C y el uso de memoria RAM es del 90%, ¿cuál es el estado de la alerta?",
        "choices": [
            "La alerta se envía porque se cumple la condición de temperatura, haciendo verdadera la disyunción inclusiva",
            "La alerta no se envía porque no se cumplió la condición de memoria RAM",
            "La alerta no se envía porque ambas condiciones deben cumplirse a la vez para que se dispare la alarma",
            "La alerta se envía porque la suma de porcentajes supera el 100% de tolerancia del sistema"
        ],
        "correct_answer": "La alerta se envía porque se cumple la condición de temperatura, haciendo verdadera la disyunción inclusiva",
        "solution_steps": "El sistema se rige por una disyunción inclusiva $p \\lor q$. Se evalúan los componentes: la temperatura es 82 °C, que supera 80 °C ($p$ es verdadera). La memoria RAM es 90%, que no supera 95% ($q$ es falsa). La expresión resultante es $V \\lor F \\equiv V$, por lo que la alerta se activa.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-3", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Si $p$ es una proposición falsa y $q$ es una proposición verdadera, ¿cuál es el valor de verdad de la expresión lógica compuesta $(\\neg p \\lor q) \\land (p \\lor \\neg q)$?",
        "choices": ["Falso", "Verdadero", "Contingente", "Indeterminado"],
        "correct_answer": "Falso",
        "solution_steps": "Sustituyendo los valores de verdad:\n- Primer paréntesis: $\\neg p \\lor q \\equiv \\neg F \\lor V \\equiv V \\lor V \\equiv V$.\n- Segundo paréntesis: $p \\lor \\neg q \\equiv F \\lor \\neg V \\equiv F \\lor F \\equiv F$.\n- Conjunción final: $V \\land F \\equiv F$.",
        "status": "ready", "source_kind": "manual"
    })

    # 4. TABLA_DISYUNCION_EXCLUSIVA (TDEXC)
    sem_id = "MAT.FUND.TABLAS_VERDAD.TABLA_DISYUNCION_EXCLUSIVA"
    abbr = "TDEXC"

    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-1", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿Bajo qué condiciones es verdadera la disyunción exclusiva $p \\oplus q$?",
        "choices": [
            "Cuando una proposición es verdadera y la otra es falsa",
            "Cuando ambas proposiciones son verdaderas",
            "Cuando ambas proposiciones son falsas",
            "Cuando la primera proposición es falsa y la segunda es opcional"
        ],
        "correct_answer": "Cuando una proposición es verdadera y la otra es falsa",
        "solution_steps": "La disyunción exclusiva (operador $\\oplus$ o 'o exclusivo') es verdadera únicamente cuando sus componentes tienen valores de verdad contrarios ($V \\oplus F \\equiv V$ y $F \\oplus V \\equiv V$). Si tienen el mismo valor de verdad, resulta falsa.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-2", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿Cuál es la diferencia principal entre la disyunción inclusiva ($\\lor$) y la disyunción exclusiva ($\\oplus$)?",
        "choices": [
            "La disyunción exclusiva es falsa cuando ambas proposiciones son verdaderas",
            "La disyunción exclusiva es verdadera cuando ambas proposiciones son falsas",
            "La disyunción inclusiva es falsa si una proposición es verdadera",
            "No hay diferencias en sus tablas de verdad, solo en el símbolo"
        ],
        "correct_answer": "La disyunción exclusiva es falsa cuando ambas proposiciones son verdaderas",
        "solution_steps": "En la fila donde ambas variables son verdaderas, la disyunción inclusiva resulta verdadera ($V \\lor V \\equiv V$), mientras que la disyunción exclusiva resulta falsa ($V \\oplus V \\equiv F$) porque excluye la opción de que ambas ocurran a la vez.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-3", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿Cuál es el valor de verdad resultante de la expresión $p \\oplus p$ para cualquier proposición $p$?",
        "choices": [
            "Falso en todos los casos",
            "Verdadero en todos los casos",
            "Verdadero si $p$ es verdadera, y falso si $p$ es falsa",
            "Depende del dominio de discurso de la variable $p$"
        ],
        "correct_answer": "Falso en todos los casos",
        "solution_steps": "El operador $\\oplus$ requiere valores de verdad opuestos para dar verdadero. Dado que evaluamos la misma proposición consigo misma ($p \\oplus p$), los valores siempre coincidirán ($V \\oplus V \\equiv F$ y $F \\oplus F \\equiv F$), por lo que resulta siempre falsa.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-REC-1", "semantic_id": sem_id, "item_group": "reconocimiento",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "Identifica el valor de verdad resultante de la disyunción exclusiva $p \\oplus q$ en la fila donde $p$ es Verdadera y $q$ es Verdadera.",
        "choices": ["Falso", "Verdadero", "Contingente", "Indefinido"],
        "correct_answer": "Falso",
        "solution_steps": "Por la regla excluyente, si ambos componentes son verdaderos ($V \\oplus V$), el resultado de la disyunción exclusiva es Falso ($F$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-1", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que si $p$ es Falso y $q$ es Verdadero, entonces $p \\oplus q$ es Verdadero?",
        "correct_answer": "Verdadero",
        "solution_steps": "Sí. Las variables tienen valores de verdad distintos ($F$ y $V$), por lo que la regla de la disyunción exclusiva se cumple y el resultado es Verdadero.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-2", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que la expresión $p \\oplus \\neg p$ es siempre verdadera?",
        "correct_answer": "Verdadero",
        "solution_steps": "Dado que $p$ y su negación $\\neg p$ obligatoriamente poseen valores de verdad contrarios, al evaluarlos con la disyunción exclusiva siempre obtendremos Verdadero ($V \\oplus F \\equiv V$ o $F \\oplus V \\equiv V$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-3", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que la disyunción exclusiva es lógicamente equivalente a la conjunción de las proposiciones?",
        "correct_answer": "Falso",
        "solution_steps": "La conjunción $p \\land q$ solo es verdadera cuando ambas son verdaderas, mientras que la disyunción exclusiva $p \\oplus q$ es falsa en ese caso y verdadera cuando sus valores difieren. Sus tablas son completamente distintas.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-1", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Un restaurante ofrece un menú de almuerzo donde el cliente puede elegir como postre: helado ($p$) o flan ($q$), pero no ambos. Si un cliente solicita flan y el mesero le trae por error helado y flan a la vez, ¿cuál es el valor de verdad de la regla de elección del menú y cómo se describe la situación?",
        "choices": [
            "Falsa, porque el cliente recibió ambos postres y la disyunción exclusiva prohíbe la ocurrencia simultánea",
            "Verdadera, porque al final obtuvo flan, lo cual cumple con su solicitud",
            "Verdadera, porque recibir más comida siempre satisface cualquier condición lógica inclusiva",
            "Falsa, porque el cliente debió haber pagado el doble por el helado adicional"
        ],
        "correct_answer": "Falsa, porque el cliente recibió ambos postres y la disyunción exclusiva prohíbe la ocurrencia simultánea",
        "solution_steps": "La regla del menú indica 'helado o flan, pero no ambos', lo que formalmente representa la disyunción exclusiva $p \\oplus q$. Al recibir helado ($V$) y flan ($V$), la situación real corresponde a la fila $V \\oplus V$, que resulta en Falso ($F$). La regla fue violada.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-2", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Un dispositivo electrónico controla una compuerta que se abre únicamente si una de dos palancas está activada: palanca A ($p$) o palanca B ($q$), pero no las dos. Si ambas palancas son activadas simultáneamente por error, ¿qué ocurrirá con la compuerta y cuál es la justificación lógica?",
        "choices": [
            "Permanecerá cerrada porque al estar ambas activas el resultado de la disyunción exclusiva es falso",
            "Se abrirá porque la activación de ambas palancas incrementa la corriente necesaria para abrirla",
            "Se abrirá a la mitad debido al equilibrio de fuerzas entre las dos palancas lógicas",
            "Permanecerá cerrada porque el sistema eléctrico se cortocircuita debido a una conjunción"
        ],
        "correct_answer": "Permanecerá cerrada porque al estar ambas activas el resultado de la disyunción exclusiva es falso",
        "solution_steps": "La regla del dispositivo se rige por la disyunción exclusiva $p \\oplus q$. Si ambas palancas son activadas, tenemos $p = V$ y $q = V$. En la tabla de verdad de la disyunción exclusiva, $V \\oplus V \\equiv F$, lo que significa que la condición para abrir la compuerta es falsa, por lo que esta permanece cerrada.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-3", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Si la proposición $p \\oplus q$ es verdadera, ¿cuál de las siguientes expresiones lógicas debe ser obligatoriamente falsa?",
        "choices": ["$p \\leftrightarrow q$", "$p \\lor q$", "$\\neg p \\land q$", "$p \\rightarrow q$"],
        "correct_answer": "$p \\leftrightarrow q$",
        "solution_steps": "La proposición $p \\oplus q$ es verdadera si y solo si $p$ y $q$ tienen valores de verdad contrarios. Por otro lado, la bicondicional $p \\leftrightarrow q$ es verdadera si y solo si $p$ y $q$ tienen valores de verdad iguales. Por tanto, si una es verdadera, la otra es obligatoriamente falsa, siendo negaciones mutuas.",
        "status": "ready", "source_kind": "manual"
    })

    # 5. TABLA_CONDICIONAL (TCOND)
    sem_id = "MAT.FUND.TABLAS_VERDAD.TABLA_CONDICIONAL"
    abbr = "TCOND"

    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-1", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿En qué único caso es falsa la proposición condicional $p \\rightarrow q$?",
        "choices": [
            "Cuando el antecedente $p$ es verdadero y el consecuente $q$ es falso",
            "Cuando el antecedente $p$ es falso y el consecuente $q$ es verdadero",
            "Cuando tanto el antecedente como el consecuente son falsos",
            "Cuando tanto el antecedente como el consecuente son verdaderos"
        ],
        "correct_answer": "Cuando el antecedente $p$ es verdadero y el consecuente $q$ es falso",
        "solution_steps": "La implicación o condicional $p \\rightarrow q$ establece que la verdad del antecedente garantiza la verdad del consecuente. El único caso que contradice esta regla es que ocurra el antecedente ($p = V$) pero no ocurra el consecuente ($q = F$), resultando en Falso ($F$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-2", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "En la proposición condicional $p \\rightarrow q$, ¿qué nombres específicos reciben las proposiciones $p$ y $q$?",
        "choices": [
            "$p$ es el antecedente y $q$ es el consecuente",
            "$p$ es la hipótesis y $q$ es la contradicción",
            "$p$ es el consecuente y $q$ es el antecedente",
            "$p$ es la premisa y $q$ es la equivalencia"
        ],
        "correct_answer": "$p$ es el antecedente y $q$ es el consecuente",
        "solution_steps": "Por convención en lógica proposicional, en la estructura condicional $p \\rightarrow q$, el término a la izquierda de la flecha ($p$) es el antecedente y el término a la derecha ($q$) es el consecuente.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-3", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿Qué ocurre con el valor de verdad de la condicional $p \\rightarrow q$ si se sabe que el antecedente $p$ es falso?",
        "choices": [
            "Es verdadera de forma vacía (vacuidad)",
            "Es falsa en todos los casos",
            "El resultado queda indeterminado",
            "Depende del valor de verdad de $q$"
        ],
        "correct_answer": "Es verdadera de forma vacía (vacuidad)",
        "solution_steps": "Si el antecedente $p$ es falso ($F$), la condición de partida no se cumple, lo que hace que la implicación completa $p \\rightarrow q$ sea verdadera de forma vacía, independientemente de si $q$ es verdadero o falso.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-REC-1", "semantic_id": sem_id, "item_group": "reconocimiento",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "Selecciona el valor de verdad de la condicional $p \\rightarrow q$ cuando las variables de entrada son $p = F$ y $q = F$.",
        "choices": ["Verdadero", "Falso", "Contingente", "Inexistente"],
        "correct_answer": "Verdadero",
        "solution_steps": "Evaluando $p \\rightarrow q$ con $p = F$ y $q = F$, tenemos $F \\rightarrow F$. Como el antecedente es falso, el condicional es Verdadero ($V$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-1", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que si $p$ es Falso y $q$ es Verdadero, el condicional $p \\rightarrow q$ es Falso?",
        "correct_answer": "Falso",
        "solution_steps": "La implicación $F \\rightarrow V$ da como resultado Verdadero ($V$). El condicional solo es falso en el caso $V \\rightarrow F$.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-2", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que la expresión $p \\rightarrow q$ es lógicamente equivalente a $\\neg p \\lor q$?",
        "correct_answer": "Verdadero",
        "solution_steps": "Sí, construyendo las tablas de verdad de ambas expresiones se puede verificar que producen la misma columna de salida ($V, F, V, V$), por lo que son equivalentes.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-3", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que el condicional no es conmutativo, es decir, $p \\rightarrow q$ no equivale a $q \\rightarrow p$?",
        "correct_answer": "Verdadero",
        "solution_steps": "El condicional es asimétrico. La tabla de verdad de $p \\rightarrow q$ da ($V, F, V, V$) mientras que la de $q \\rightarrow p$ da ($V, V, F, V$). Sus valores difieren en las filas intermedias.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-1", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Un contrato de trabajo establece la siguiente regla: 'Si trabajas horas extras los fines de semana ($p$), entonces recibirás un bono en tu sueldo ($q$)'. Si un mes un empleado no trabajó horas extras pero de todas formas recibió el bono, ¿cuál de las siguientes opciones describe si el empleador rompió el contrato y su justificación lógica?",
        "choices": [
            "No se rompió el contrato, porque el antecedente fue falso, haciendo que la implicación sea verdadera",
            "Se rompió el contrato, porque para recibir un bono era obligatorio haber trabajado horas extras",
            "No se rompió el contrato, porque en lógica un consecuente verdadero siempre exige un antecedente verdadero",
            "Se rompió el contrato, porque la situación corresponde a la fila verdadera-falsa del condicional"
        ],
        "correct_answer": "No se rompió el contrato, because el antecedente fue falso, haciendo que la implicación sea verdadera",
        "solution_steps": "La regla contractual es una implicación $p \\rightarrow q$. Como el empleado no trabajó horas extras, el antecedente $p$ es falso ($F$). El contrato prometía pagar el bono si trabajaba, pero no prohibía pagarlo por otras razones. Por lo tanto, evaluar $F \\rightarrow V$ da como resultado Verdadero ($V$). No hubo incumplimiento.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-2", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Considera la afirmación lógica: 'Si un número entero es múltiplo de 4, entonces es múltiplo de 2'. Si elegimos el número 6 para evaluar esta regla, ¿cuál es el estado de verdad de la implicación para este caso particular?",
        "choices": [
            "Es verdadera, porque el antecedente es falso y el consecuente es verdadero",
            "Es falsa, porque el número 6 no es múltiplo de 4",
            "Es falsa, porque un antecedente falso invalida todo el análisis matemático de la divisibilidad",
            "Es verdadera, porque tanto el antecedente como el consecuente son verdaderos para el número 6"
        ],
        "correct_answer": "Es verdadera, porque el antecedente es falso y el consecuente es verdadero",
        "solution_steps": "Sea $p$: '6 es múltiplo de 4' (Falso) y $q$: '6 es múltiplo de 2' (Verdadero). Evaluando el condicional $p \\rightarrow q$, tenemos $F \\rightarrow V \\equiv V$. Por tanto, la implicación es verdadera para el número 6.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-3", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Si se sabe que la proposición condicional $p \\rightarrow q$ es falsa, ¿cuál de las siguientes afirmaciones sobre las variables $p$ y $q$ es correcta?",
        "choices": [
            "$p$ es verdadera y $q$ es falsa",
            "$p$ es falsa y $q$ es verdadera",
            "Tanto $p$ como $q$ son falsas",
            "Tanto $p$ como $q$ son verdaderas"
        ],
        "correct_answer": "$p$ es verdadera y $q$ es falsa",
        "solution_steps": "En la tabla de verdad del condicional $p \\rightarrow q$, existe una única fila donde el resultado es Falso ($F$), la cual corresponde al caso en que el antecedente $p$ es Verdadero ($V$) y el consecuente $q$ es Falso ($F$).",
        "status": "ready", "source_kind": "manual"
    })

    # 6. TABLA_BICONDICIONAL (TBICO)
    sem_id = "MAT.FUND.TABLAS_VERDAD.TABLA_BICONDICIONAL"
    abbr = "TBICO"

    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-1", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿Cuándo es verdadera la proposición bicondicional $p \\leftrightarrow q$?",
        "choices": [
            "Cuando tanto $p$ como $q$ tienen el mismo valor de verdad",
            "Cuando $p$ es verdadera y $q$ es falsa",
            "Cuando al menos una de las dos es verdadera",
            "Únicamente cuando tanto $p$ como $q$ son verdaderas"
        ],
        "correct_answer": "Cuando tanto $p$ como $q$ tienen el mismo valor de verdad",
        "solution_steps": "La bicondicional $p \\leftrightarrow q$ es una relación de equivalencia que resulta verdadera si ambos lados tienen el mismo valor lógico, es decir, ambos verdaderos ($V \\leftrightarrow V \\equiv V$) o ambos falsos ($F \\leftrightarrow F \\equiv V$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-2", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿Cómo se lee comúnmente en matemáticas y lógica el conectivo lógico del bicondicional $\\leftrightarrow$?",
        "choices": [
            "'si y solo si'",
            "'si..., entonces...'",
            "'o bien... o bien...'",
            "'no es cierto que'"
        ],
        "correct_answer": "'si y solo si'",
        "solution_steps": "El símbolo $\\leftrightarrow$ representa la doble implicación, expresada en lenguaje ordinario mediante la frase de exclusividad 'si y solo si'.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-3", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿Cuál es el valor de verdad resultante de la expresión $p \\leftrightarrow \\neg p$ para cualquier proposición $p$?",
        "choices": [
            "Falso en todos los casos",
            "Verdadero en todos los casos",
            "Depende del valor de verdad inicial de $p$",
            "Es una tautología"
        ],
        "correct_answer": "Falso en todos los casos",
        "solution_steps": "Una proposición $p$ y su negación $\\neg p$ siempre tienen valores lógicos opuestos. Como la bicondicional requiere valores idénticos para dar verdadero, la expresión $p \\leftrightarrow \\neg p$ será siempre falsa ($V \\leftrightarrow F \\equiv F$ y $F \\leftrightarrow V \\equiv F$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-REC-1", "semantic_id": sem_id, "item_group": "reconocimiento",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "Selecciona el valor de verdad correcto de la bicondicional $p \\leftrightarrow q$ para la fila donde $p$ es Falsa y $q$ es Falsa.",
        "choices": ["Verdadero", "Falso", "Contingente", "Nulo"],
        "correct_answer": "Verdadero",
        "solution_steps": "Evaluando $p \\leftrightarrow q$ con $p = F$ y $q = F$, tenemos $F \\leftrightarrow F$. Dado que ambas variables tienen el mismo valor de verdad (Falso), el resultado del bicondicional es Verdadero ($V$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-1", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que si $p$ es Verdadero y $q$ es Falso, el bicondicional $p \\leftrightarrow q$ es Falso?",
        "correct_answer": "Verdadero",
        "solution_steps": "Sí. Al tener valores de verdad contrarios ($V$ y $F$), la condición de equivalencia del bicondicional no se cumple, resultando en Falso ($V \\leftrightarrow F \\equiv F$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-2", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que el bicondicional $p \\leftrightarrow q$ es equivalente a $(p \\rightarrow q) \\land (q \\rightarrow p)$?",
        "correct_answer": "Verdadero",
        "solution_steps": "Sí, el bicondicional representa una doble implicación, lo que significa que $p$ implica a $q$ y al mismo tiempo $q$ implica a $p$. Sus tablas de verdad coinciden en todas las filas.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-3", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que si $p \\leftrightarrow q$ es verdadero, entonces obligatoriamente tanto $p$ como $q$ deben ser verdaderas?",
        "correct_answer": "Falso",
        "solution_steps": "El bicondicional también es verdadero en la fila donde ambas variables son falsas ($F \\leftrightarrow F \\equiv V$). No exige que obligatoriamente sean ambas verdaderas.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-1", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Una tienda en línea ofrece la promoción de envío gratis ($p$) si y solo si la compra supera los 50.000 pesos ($q$). Si un cliente realiza una compra por un monto de 30.000 pesos y el sistema le cobra el envío correspondiente, ¿se cumplió la regla bicondicional establecida por la tienda?",
        "choices": [
            "Sí, porque al no superarse el monto no se dio el envío gratis, coincidiendo ambos en falso, lo que hace verdadera la regla",
            "No, porque la regla del bicondicional exige que el envío gratis se aplique a todas las compras sin excepción",
            "No, porque cobrar el envío es una acción que contradice la posibilidad de envío gratis en compras menores",
            "Sí, porque el cliente pagó por el envío y el bicondicional es verdadero si al menos una parte es verdadera"
        ],
        "correct_answer": "Sí, porque al no superarse el monto no se dio el envío gratis, coincidiendo ambos en falso, lo que hace verdadera la regla",
        "solution_steps": "La regla es una equivalencia bicondicional $p \\leftrightarrow q$. Evaluamos la compra de Juan: la compra es de 30.000 pesos, por lo que no supera los 50.000 ($q$ es falsa). Como no superó el monto, no obtuvo el envío gratis ($p$ es falsa). La evaluación resulta en $F \\leftrightarrow F \\equiv V$. El sistema cumplió correctamente con la regla de la tienda.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-2", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Considera la proposición matemática: 'Un triángulo es equilátero ($p$) si y solo si tiene sus tres ángulos internos iguales ($q$)'. Si analizamos un triángulo cuyos ángulos internos miden 60° cada uno, ¿cuál de las siguientes opciones describe el análisis de verdad de esta proposición?",
        "choices": [
            "Es verdadera, porque se cumplen ambas condiciones, dando un bicondicional verdadero ($V \\leftrightarrow V \\equiv V$)",
            "Es falsa, porque tener ángulos de 60° no garantiza que el triángulo sea equilátero en geometría espacial",
            "Es verdadera, porque el antecedente es falso y el consecuente es verdadero para este triángulo",
            "Es falsa, porque la palabra 'si y solo si' prohíbe que ambas condiciones se den al mismo tiempo"
        ],
        "correct_answer": "Es verdadera, porque se cumplen ambas condiciones, dando un bicondicional verdadero ($V \\leftrightarrow V \\equiv V$)",
        "solution_steps": "El triángulo tiene sus tres ángulos iguales (60°), por lo que $q$ es verdadera. Como consecuencia geométrica, el triángulo también es equilátero ($p$ es verdadera). Al evaluar la bicondicional $p \\leftrightarrow q$ tenemos $V \\leftrightarrow V \\equiv V$. La proposición es verdadera para este caso.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-3", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Si la proposición bicondicional $p \\leftrightarrow q$ es falsa, ¿cuál de las siguientes proposiciones debe ser obligatoriamente verdadera?",
        "choices": ["$p \\oplus q$", "$p \\land q$", "$p \\rightarrow q$", "$\\neg p \\land \\neg q$"],
        "correct_answer": "$p \\oplus q$",
        "solution_steps": "El bicondicional $p \\leftrightarrow q$ es falso cuando $p$ y $q$ tienen valores de verdad distintos. Esta condición de tener valores distintos es precisamente la definición para que la disyunción exclusiva $p \\oplus q$ sea verdadera. Por lo tanto, si una es falsa, la otra es verdadera.",
        "status": "ready", "source_kind": "manual"
    })

    # 7. FILAS_DOS_VARIABLES (F2VAR)
    sem_id = "MAT.FUND.TABLAS_VERDAD.FILAS_DOS_VARIABLES"
    abbr = "F2VAR"

    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-1", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿Cuántas filas se requieren en una tabla de verdad para evaluar una expresión lógica con exactamente dos variables proposicionales distintas?",
        "choices": ["4 filas", "2 filas", "8 filas", "16 filas"],
        "correct_answer": "4 filas",
        "solution_steps": "El número de combinaciones de verdad posibles para $n$ variables proposicionales independientes es $2^n$. Para dos variables ($n=2$), se calculan $2^2 = 4$ filas.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-2", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "¿Cuál es la fórmula matemática general para calcular el número de filas en una tabla de verdad con $n$ variables proposicionales independientes?",
        "choices": ["$2^n$", "$n^2$", "$2 \\cdot n$", "$2^{n-1}$"],
        "correct_answer": "$2^n$",
        "solution_steps": "Dado que cada variable proposicional independiente tiene exactamente 2 valores lógicos posibles (Verdadero o Falso), por el principio multiplicativo, el total de combinaciones únicas para $n$ variables es $2 \\cdot 2 \\cdot \\ldots \\cdot 2 = 2^n$ filas.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-CONC-3", "semantic_id": sem_id, "item_group": "conceptuales",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "En la distribución estándar para dos variables $p$ y $q$, ¿cómo se llenan ordenadamente los valores de la primera columna correspondiente a $p$?",
        "choices": [
            "Dos verdaderos seguidos de dos falsos ($V, V, F, F$)",
            "Alternando de uno en uno ($V, F, V, F$)",
            "Cuatro verdaderos seguidos de cuatro falsos ($V, V, V, V, F, F, F, F$)",
            "Todos verdaderos en las cuatro filas"
        ],
        "correct_answer": "Dos verdaderos seguidos de dos falsos ($V, V, F, F$)",
        "solution_steps": "Para una tabla de 4 filas, la distribución estándar de valores divide el total a la mitad para la primera columna: 2 Verdaderos ($V, V$) y 2 Falsos ($F, F$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-REC-1", "semantic_id": sem_id, "item_group": "reconocimiento",
        "format": "multiple_choice", "difficulty": "basica", "competencia": "U",
        "prompt": "Si una expresión lógica compleja contiene las variables $p$, $q$, $\\neg p$ y $q$, ¿cuántas variables proposicionales independientes distintas se deben considerar para calcular el tamaño de la tabla?",
        "choices": ["2 variables distintas", "3 variables distintas", "4 variables distintas", "1 variable distinta"],
        "correct_answer": "2 variables distintas",
        "solution_steps": "Las variables proposicionales simples e independientes presentes en la fórmula son únicamente $p$ y $q$. Las negaciones ($\\neg p$) o las repeticiones ($q$) no aumentan la cantidad de variables base, por lo que son 2 variables.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-1", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que para dos variables proposicionales distintas, el número total de filas en su tabla de verdad es $2^2 = 4$?",
        "correct_answer": "Verdadero",
        "solution_steps": "Sí. Aplicando la fórmula de combinaciones posibles $2^n$ con $n=2$ variables, obtenemos exactamente 4 filas.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-2", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que las negaciones de las variables de entrada cuentan como variables adicionales independientes al calcular el número de filas de la tabla?",
        "correct_answer": "Falso",
        "solution_steps": "Las negaciones como $\\neg p$ son operaciones unarias sobre variables ya existentes, no representan nuevas variables proposicionales independientes, por lo que no afectan el valor de $n$ en la fórmula $2^n$.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PROC-3", "semantic_id": sem_id, "item_group": "procedimiento_basico",
        "format": "true_false", "difficulty": "basica",
        "prompt": "¿Es verdadero que la alternancia estándar de los valores para la segunda variable $q$ en una tabla de dos variables consiste en alternar de dos en dos ($V, V, F, F$)?",
        "correct_answer": "Falso",
        "solution_steps": "En la distribución estándar de dos variables, la primera columna ($p$) alterna de dos en dos ($V, V, F, F$), y la segunda columna ($q$) es la que alterna de uno en uno ($V, F, V, F$).",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-1", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Un estudiante está analizando las propiedades de la expresión lógica compuesta: $[(p \\land q) \\lor \\neg p] \\rightarrow (p \\lor \\neg q)$. Para comprobar la validez de esta expresión, decide construir su tabla de verdad. ¿Cuántas filas de datos tendrá la tabla de verdad construida por el estudiante?",
        "choices": [
            "4 filas, porque solo aparecen dos variables distintas, $p$ y $q$, y las negaciones no añaden variables independientes",
            "8 filas, porque hay cuatro conectivos lógicos en la expresión",
            "16 filas, porque hay cuatro variables en la expresión considerando las negaciones",
            "2 filas, porque es una implicación simple que vincula dos bloques"
        ],
        "correct_answer": "4 filas, porque solo aparecen dos variables distintas, $p$ y $q$, y las negaciones no añaden variables independientes",
        "solution_steps": "Identificamos las variables lógicas básicas de la expresión. Las únicas letras proposicionales diferentes son $p$ y $q$. Las negaciones y repeticiones no aumentan la cantidad de variables. Con $n = 2$, el número de filas de la tabla de verdad es $2^2 = 4$.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-2", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "En una prueba de lógica se pide a los alumnos estructurar las columnas de entrada de una tabla de verdad para las variables $p$ y $q$. Si un alumno escribe para la columna de $p$: $(V, F, V, F)$ y para la columna de $q$: $(V, V, F, F)$, ¿cuál de las siguientes afirmaciones describe de forma lógicamente correcta su trabajo?",
        "choices": [
            "Los valores están intercambiados respecto al orden estándar de alternancia, pero cubren todas las combinaciones posibles",
            "La tabla es incorrecta porque la columna $p$ siempre debe iniciar con dos valores falsos",
            "La tabla es incompleta porque al cambiar el orden estándar se reduce el número de filas necesarias a 2",
            "La tabla es correcta y corresponde exactamente a la distribución estándar canónica de la lógica proposicional"
        ],
        "correct_answer": "Los valores están intercambiados respecto al orden estándar de alternancia, pero cubren todas las combinaciones posibles",
        "solution_steps": "En el orden canónico estándar, la columna $p$ alterna de dos en dos ($V, V, F, F$) y la columna $q$ de uno en uno ($V, F, V, F$). El alumno intercambió el orden de alternancia entre las columnas, pero dado que las 4 filas resultantes siguen representando las 4 combinaciones posibles sin repetir ninguna, la tabla sigue siendo válida lógicamente.",
        "status": "ready", "source_kind": "manual"
    })
    tanda_1.append({
        "stable_id": f"{abbr}-GEN-PAES-3", "semantic_id": sem_id, "item_group": "tipo_paes",
        "format": "multiple_choice", "difficulty": "media", "competencia": "U", "paes_style": True,
        "prompt": "Si deseamos evaluar mediante una tabla de verdad todas las combinaciones posibles para dos condiciones climáticas independientes: $p$: 'lloverá mañana' y $q$: 'habrá viento fuerte', ¿cuántas filas debemos incluir en nuestra tabla de análisis conceptual para garantizar que no se omita ningún escenario posible?",
        "choices": [
            "4 filas, ya que cada condición tiene 2 valores lógicos posibles y son independientes",
            "2 filas, porque solo nos interesa saber si llueve o hay viento",
            "8 filas, porque hay dos estados posibles para cada uno de los cuatro cuadrantes del día",
            "6 filas, ya que debemos incluir los casos intermedios de lluvia suave"
        ],
        "correct_answer": "4 filas, ya que cada condición tiene 2 valores lógicos posibles y son independientes",
        "solution_steps": "Cada condición climática se modela como una proposición lógica simple con 2 estados posibles: ocurre ($V$) o no ocurre ($F$). Al ser dos variables independientes ($n=2$), el total de combinaciones es $2^2 = 4$ filas, lo que cubre todos los escenarios lógicos posibles.",
        "status": "ready", "source_kind": "manual"
    })

    # Save Tanda B01-3
    os.makedirs("docs/conocimiento/ejercicios", exist_ok=True)
    with open("docs/conocimiento/ejercicios/mat-fund-tablas-verdad-banco-gen-1.jsonl", "w", encoding="utf-8") as f:
        for ex in tanda_1:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print("Created Tanda B01-3 exercises successfully.")

generate()
