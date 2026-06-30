import json
import os

def create_tanda_b01_5():
    tanda = []
    
    # 1. EQUIVALENCIA_LOGICA (EQUIV)
    equiv_exercises = [
        {
            "stable_id": "EQUIV-GEN-CONC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.EQUIVALENCIA_LOGICA",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Qué significa que dos proposiciones compuestas $P$ y $Q$ sean lógicamente equivalentes?",
            "choices": [
                "Tienen los mismos valores de verdad para cada combinación en su tabla de verdad",
                "Tienen la misma cantidad de conectivos lógicos en sus fórmulas",
                "Ambas son verdaderas en al menos una fila de la tabla",
                "Comparten exactamente las mismas variables proposicionales simples"
            ],
            "correct_answer": "Tienen los mismos valores de verdad para cada combinación en su tabla de verdad",
            "solution_steps": "Por definición de equivalencia lógica, $P \\equiv Q$ si y solo si sus columnas de verdad coinciden en todas las filas de la tabla de verdad.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "EQUIV-GEN-CONC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.EQUIVALENCIA_LOGICA",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "Si $P \\equiv Q$, ¿cuál de las siguientes proposiciones compuestas es una tautología?",
            "choices": [
                "$P \\leftrightarrow Q$",
                "$P \\to Q$",
                "$P \\land Q$",
                "$P \\lor Q$"
            ],
            "correct_answer": "$P \\leftrightarrow Q$",
            "solution_steps": "Dos proposiciones son equivalentes si y solo si su bicondicional $P \\leftrightarrow Q$ es siempre verdadera (tautología).",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "EQUIV-GEN-CONC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.EQUIVALENCIA_LOGICA",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cuál de las siguientes denotaciones se utiliza comúnmente para indicar que $P$ es lógicamente equivalente a $Q$?",
            "choices": [
                "$P \\equiv Q$",
                "$P \\to Q$",
                "$P \\land Q$",
                "$P \\vdash Q$"
            ],
            "correct_answer": "$P \\equiv Q$",
            "solution_steps": "La equivalencia lógica se representa mediante el símbolo $\\equiv$ o $\\Leftrightarrow$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "EQUIV-GEN-REC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.EQUIVALENCIA_LOGICA",
            "item_group": "reconocimiento",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cuál de las siguientes parejas de proposiciones es una equivalencia lógica conocida como la conmutatividad de la disyunción?",
            "choices": [
                "$p \\lor q \\equiv q \\lor p$",
                "$p \\land q \\equiv q \\land p$",
                "$p \\to q \\equiv q \\to p$",
                "$\\neg(\\neg p) \\equiv p$"
            ],
            "correct_answer": "$p \\lor q \\equiv q \\lor p$",
            "solution_steps": "La conmutatividad de la disyunción establece que el orden de los sumandos lógicos no altera su valor: $p \\lor q \\equiv q \\lor p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "EQUIV-GEN-PROC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.EQUIVALENCIA_LOGICA",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Son lógicamente equivalentes las proposiciones $p \\to q$ y $\\neg p \\lor q$?",
            "correct_answer": "Verdadero",
            "solution_steps": "Su equivalencia se demuestra mediante la tabla de verdad, donde ambas dan la columna (V, F, V, V) para las filas (VV, VF, FV, FF). Por lo tanto, $p \\to q \\equiv \\neg p \\lor q$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "EQUIV-GEN-PROC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.EQUIVALENCIA_LOGICA",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Son lógicamente equivalentes las proposiciones $p \\land q$ y $p \\lor q$?",
            "correct_answer": "Falso",
            "solution_steps": "$p \\land q$ solo es verdadera si ambas variables son verdaderas, mientras que $p \\lor q$ es verdadera si al menos una lo es. Sus tablas no coinciden: $p \\land q \\not\\equiv p \\lor q$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "EQUIV-GEN-PROC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.EQUIVALENCIA_LOGICA",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es lógicamente equivalente $\\neg(p \\to q)$ a $p \\land \\neg q$?",
            "correct_answer": "Verdadero",
            "solution_steps": "Dado que $p \\to q \\equiv \\neg p \\lor q$, al negar ambos lados obtenemos $\\neg(p \\to q) \\equiv \\neg(\\neg p \\lor q) \\equiv p \\land \\neg q$ por la Ley de De Morgan.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "EQUIV-GEN-PAES-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.EQUIVALENCIA_LOGICA",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Un profesor desafía a sus estudiantes a simplificar la expresión lógica $\\neg(p \\to q) \\lor (p \\land \\neg q)$. Utilizando las equivalencias lógicas conocidas, ¿a qué expresión simplificada equivale esta fórmula?",
            "choices": [
                "$p \\land \\neg q$",
                "$\\neg p \\lor q$",
                "$p \\lor q$",
                "$p \\land q$"
            ],
            "correct_answer": "$p \\land \\neg q$",
            "solution_steps": "Sabemos que la negación del condicional equivale a: $\\neg(p \\to q) \\equiv p \\land \\neg q$. Por lo tanto, la expresión queda como $(p \\land \\neg q) \\lor (p \\land \\neg q)$, que por idempotencia equivale a $p \\land \\neg q$.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "EQUIV-GEN-PAES-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.EQUIVALENCIA_LOGICA",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "En un circuito de control automático, se diseñaron dos interruptores lógicos programados como $A = \\neg(p \\land q)$ y $B = \\neg p \\lor \\neg q$. ¿Qué relación lógica existe entre los interruptores $A$ y $B$?",
            "choices": [
                "Son lógicamente equivalentes por Ley de De Morgan",
                "Son contradictorios en cualquier estado",
                "$A$ es verdadero solo si $B$ es falso",
                "No tienen ninguna relación lógica"
            ],
            "correct_answer": "Son lógicamente equivalentes por Ley de De Morgan",
            "solution_steps": "Por la Ley de De Morgan, la negación de una conjunción es equivalente a la disyunción de las negaciones: $\\neg(p \\land q) \\equiv \\neg p \\lor \\neg q$. Por ende, los interruptores $A$ y $B$ son equivalentes.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "EQUIV-GEN-PAES-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.EQUIVALENCIA_LOGICA",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Si se sabe que la proposición $p$ es verdadera y $q$ es falsa, ¿cuál de las siguientes proposiciones lógicamente equivalentes a la disyunción exclusiva $(p \\lor q) \\land \\neg(p \\land q)$ tendrá un valor de verdad FALSO?",
            "choices": [
                "$p \\leftrightarrow q$",
                "$\\neg(p \\leftrightarrow q)$",
                "$p \\leftrightarrow \\neg q$",
                "$(p \\land \\neg q) \\lor (\\neg p \\land q)$"
            ],
            "correct_answer": "$p \\leftrightarrow q$",
            "solution_steps": "Dado que $p$ es V y $q$ es F, difieren en su valor de verdad. La disyunción exclusiva es Verdadera. El bicondicional $p \\leftrightarrow q$ es Falso cuando las variables difieren, por lo que es la opción correcta.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        }
    ]
    tanda.extend(equiv_exercises)

    # 2. DOBLE_NEGACION (DNEG)
    dneg_exercises = [
        {
            "stable_id": "DNEG-GEN-CONC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DOBLE_NEGACION",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Qué establece formalmente la Ley de Doble Negación?",
            "choices": [
                "$\\neg(\\neg p) \\equiv p$",
                "$\\neg(\\neg p) \\equiv \\neg p$",
                "$\\neg p \\equiv p$",
                "$\\neg(\\neg p) \\equiv \\text{Falso}$"
            ],
            "correct_answer": "$\\neg(\\neg p) \\equiv p$",
            "solution_steps": "La Ley de Doble Negación establece que la negación de una proposición ya negada equivale a la proposición original: $\\neg(\\neg p) \\equiv p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "DNEG-GEN-CONC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DOBLE_NEGACION",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "Si negamos dos veces una proposición falsa, el valor de verdad final es:",
            "choices": [
                "Falso",
                "Verdadero",
                "Indeterminado",
                "Tautológico"
            ],
            "correct_answer": "Falso",
            "solution_steps": "La doble negación preserva el valor de verdad original de la proposición. Si la proposición era falsa, el resultado sigue siendo falso: $\\neg(\\neg F) \\equiv F$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "DNEG-GEN-CONC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DOBLE_NEGACION",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cuál de las siguientes afirmaciones en lenguaje natural representa la estructura de una doble negación?",
            "choices": [
                "Es mentira que no estudié",
                "No iré a la playa hoy",
                "Fui al parque o a la plaza",
                "Si no llueve, saldré a correr"
            ],
            "correct_answer": "Es mentira que no estudié",
            "solution_steps": "'Es mentira que' representa una negación, y 'no estudié' otra negación, lo que equivale a la afirmación 'estudié' por la ley de doble negación.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "DNEG-GEN-REC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DOBLE_NEGACION",
            "item_group": "reconocimiento",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "Al evaluar la proposición $\\neg(\\neg(\\neg p))$, esta se reduce por doble negación a:",
            "choices": [
                "$\\neg p$",
                "$p$",
                "$p \\land \\neg p$",
                "$\\neg(\\neg p)$"
            ],
            "correct_answer": "$\\neg p$",
            "solution_steps": "Dos de las negaciones consecutivas se anulan mutuamente, por lo que queda una sola negación: $\\neg(\\neg(\\neg p)) \\equiv \\neg p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "DNEG-GEN-PROC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DOBLE_NEGACION",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es la proposición $\\neg(\\neg(p \\lor q))$ equivalente a $p \\lor q$?",
            "correct_answer": "Verdadero",
            "solution_steps": "Por la Ley de Doble Negación, aplicando $\\neg(\\neg P) \\equiv P$ donde $P = p \\lor q$, la doble negación exterior se cancela, resultando en $p \\lor q$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "DNEG-GEN-PROC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DOBLE_NEGACION",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es la proposición $\\neg(\\neg(\\neg(\\neg p)))$ equivalente a $\\neg p$?",
            "correct_answer": "Falso",
            "solution_steps": "Cuatro negaciones consecutivas se cancelan de a pares: $\\neg\\neg\\neg\\neg p \\equiv \\neg\\neg p \\equiv p$. Por lo tanto, no es equivalente a $\\neg p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "DNEG-GEN-PROC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DOBLE_NEGACION",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es la frase 'No es cierto que no soy estudiante' equivalente a 'Soy estudiante'?",
            "correct_answer": "Verdadero",
            "solution_steps": "Formalizando la frase: $\\neg(\\neg e) \\equiv e$, donde $e$ es 'Soy estudiante'. Por doble negación, la frase equivale a la afirmación original.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "DNEG-GEN-PAES-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DOBLE_NEGACION",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "En una investigación científica se concluye que: 'No es cierto que no exista relación entre el clima y la migración de las aves'. Si la variable $p$ representa 'Existe relación entre el clima y la migración', ¿cómo se simplifica lógicamente la conclusión del estudio?",
            "choices": [
                "$p$ (Existe relación)",
                "$\\neg p$ (No existe relación)",
                "$p \\land \\neg p$",
                "$\\neg(\\neg(\\neg p))$"
            ],
            "correct_answer": "$p$ (Existe relación)",
            "solution_steps": "La frase se formaliza como la negación de 'no existe relación', es decir, $\\neg(\\neg p)$. Aplicando la Ley de Doble Negación: $\\neg(\\neg p) \\equiv p$. La conclusión es que existe relación.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "DNEG-GEN-PAES-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DOBLE_NEGACION",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Un programador tiene la línea de código `if (!(!condicion1 && condicion2))`. Si desea simplificar esta condición usando doble negación y De Morgan, ¿a cuál de las siguientes expresiones equivale?",
            "choices": [
                "`condicion1 || !condicion2`",
                "`!condicion1 || condicion2`",
                "`condicion1 && condicion2`",
                "`!condicion1 && !condicion2`"
            ],
            "correct_answer": "`condicion1 || !condicion2`",
            "solution_steps": "La expresión es $\\neg(\\neg c_1 \\land c_2)$. Aplicando la Ley de De Morgan: $\\neg(\\neg c_1) \\lor \\neg c_2$. Por la ley de doble negación, $\\neg(\\neg c_1) \\equiv c_1$. Obtenemos $c_1 \\lor \\neg c_2$.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "DNEG-GEN-PAES-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DOBLE_NEGACION",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Considere la proposición compleja $A = \\neg(\\neg p \\lor \\neg(\\neg q))$. Si aplicamos la ley de doble negación a la variable $q$ y luego reescribimos el condicional equivalente, ¿a qué expresión resulta equivalente?",
            "choices": [
                "$\\neg(p \\to q)$",
                "$p \\to q$",
                "$q \\to p$",
                "$\\neg p \\lor q$"
            ],
            "correct_answer": "$\\neg(p \\to q)$",
            "solution_steps": "Primero, por doble negación, $\\neg(\\neg q) \\equiv q$. Esto simplifica la expresión interna a $\\neg(\\neg p \\lor q)$. Dado que $\\neg p \\lor q$ es equivalente a $p \\to q$, la expresión completa equivale a $\\neg(p \\to q)$.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        }
    ]
    tanda.extend(dneg_exercises)

    # 3. DE_MORGAN_CONJUNCION (MORGC)
    morgc_exercises = [
        {
            "stable_id": "MORGC-GEN-CONC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_CONJUNCION",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Qué conectivo lógico reemplaza a la conjunción al aplicar la Ley de De Morgan para la conjunción?",
            "choices": [
                "Disyunción inclusiva ($\\lor$)",
                "Conjunción ($\\land$)",
                "Condicional ($\\to$)",
                "Disyunción exclusiva"
            ],
            "correct_answer": "Disyunción inclusiva ($\\lor$)",
            "solution_steps": "Al negar una conjunción, el conectivo 'y' ($\\land$) se transforma en 'o' ($\\lor$), que es la disyunción inclusiva.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGC-GEN-CONC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_CONJUNCION",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "La expresión $\\neg(p \\land q)$ es lógicamente equivalente a:",
            "choices": [
                "$\\neg p \\lor \\neg q$",
                "$\\neg p \\land \\neg q$",
                "$p \\lor q$",
                "$\\neg p \\lor q$"
            ],
            "correct_answer": "$\\neg p \\lor \\neg q$",
            "solution_steps": "La Ley de De Morgan para la conjunción establece que la negación de una conjunción es la disyunción de las negaciones: $\\neg(p \\land q) \\equiv \\neg p \\lor \\neg q$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGC-GEN-CONC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_CONJUNCION",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "Negar que ocurran simultáneamente dos proposiciones equivale a decir que:",
            "choices": [
                "Al menos una de las dos proposiciones es falsa",
                "Ambas proposiciones son verdaderas",
                "Ninguna de las dos proposiciones ocurre",
                "La primera proposición es falsa y la segunda es verdadera"
            ],
            "correct_answer": "Al menos una de las dos proposiciones es falsa",
            "solution_steps": "Decir que no ocurre la conjunción ($\\neg(p \\land q)$) significa que al menos uno de los términos es falso ($\\neg p \\lor \\neg q$).",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGC-GEN-REC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_CONJUNCION",
            "item_group": "reconocimiento",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cuál de las siguientes opciones muestra una aplicación directa y correcta de la Ley de De Morgan para la conjunción?",
            "choices": [
                "$\\neg(p \\land \\neg q) \\equiv \\neg p \\lor q$",
                "$\\neg(p \\land q) \\equiv \\neg p \\land \\neg q$",
                "$\\neg(p \\lor q) \\equiv \\neg p \\land \\neg q$",
                "$\\neg(p \\to q) \\equiv p \\land \\neg q$"
            ],
            "correct_answer": "$\\neg(p \\land \\neg q) \\equiv \\neg p \\lor q$",
            "solution_steps": "Aplicando De Morgan a $\\neg(p \\land \\neg q)$ obtenemos $\\neg p \\lor \\neg(\\neg q)$, lo cual se reduce a $\\neg p \\lor q$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGC-GEN-PROC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_CONJUNCION",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es la proposición $\\neg(p \\land q)$ equivalente a $\\neg p \\land \\neg q$?",
            "correct_answer": "Falso",
            "solution_steps": "Incorrecto. La Ley de De Morgan transforma la conjunción en disyunción. La equivalencia correcta es $\\neg(p \\land q) \\equiv \\neg p \\lor \\neg q$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGC-GEN-PROC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_CONJUNCION",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es la proposición $\\neg(\\neg p \\land \\neg q)$ equivalente a $p \\lor q$?",
            "correct_answer": "Verdadero",
            "solution_steps": "Aplicando De Morgan a la conjunción interna: $\\neg(\\neg p) \\lor \\neg(\\neg q) \\equiv p \\lor q$, lo cual es verdadero.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGC-GEN-PROC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_CONJUNCION",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es la proposición $\\neg(p \\land q)$ falsa cuando ambas variables $p$ y $q$ son verdaderas?",
            "correct_answer": "Verdadero",
            "solution_steps": "Si $p$ y $q$ son verdaderas, la conjunción $p \\land q$ es verdadera. Por ende, su negación $\\neg(p \\land q)$ es falsa.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGC-GEN-PAES-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_CONJUNCION",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Un detective declara en un juicio: 'No es cierto que el sospechoso tuviera el arma y estuviera en la escena del crimen'. Si $a$ representa 'el sospechoso tenía el arma' y $e$ representa 'el sospechoso estaba en la escena', ¿cuál es la declaración equivalente del detective según las leyes de la lógica?",
            "choices": [
                "El sospechoso no tenía el arma o no estaba en la escena",
                "El sospechoso no tenía el arma y no estaba en la escena",
                "Si el sospechoso tenía el arma, no estaba en la escena",
                "El sospechoso tenía el arma pero no estaba en la escena"
            ],
            "correct_answer": "El sospechoso no tenía el arma o no estaba en la escena",
            "solution_steps": "La declaración original es $\\neg(a \\land e)$. Por De Morgan para la conjunción, esto equivale a $\\neg a \\lor \\neg e$, que significa 'El sospechoso no tenía el arma o no estaba en la escena'.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGC-GEN-PAES-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_CONJUNCION",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Un estudiante debe simplificar el circuito lógico representado por la proposición $\\neg(p \\land (q \\land r))$. Aplicando las leyes de De Morgan para la conjunción de manera sucesiva, ¿cuál de las siguientes opciones es equivalente?",
            "choices": [
                "$\\neg p \\lor (\\neg q \\lor \\neg r)$",
                "$\\neg p \\land (\\neg q \\land \\neg r)$",
                "$\\neg p \\lor (\\neg q \\land \\neg r)$",
                "$p \\lor (q \\lor r)$"
            ],
            "correct_answer": "$\\neg p \\lor (\\neg q \\lor \\neg r)$",
            "solution_steps": "Aplicando De Morgan a la conjunción exterior: $\\neg p \\lor \\neg(q \\land r)$. Luego, aplicando De Morgan al segundo término: $\\neg p \\lor (\\neg q \\lor \\neg r)$.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGC-GEN-PAES-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_CONJUNCION",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "En un sistema de seguridad, una alarma se activa si no se cumple que las dos puertas estén cerradas al mismo tiempo, lo que se modela como $\\neg(p \\land q)$, donde $p$ y $q$ representan que las puertas 1 y 2 están cerradas. ¿En cuál de las siguientes situaciones la alarma NO se activará?",
            "choices": [
                "La puerta 1 está cerrada y la puerta 2 está cerrada",
                "La puerta 1 está abierta y la puerta 2 está abierta",
                "La puerta 1 está cerrada y la puerta 2 está abierta",
                "La puerta 1 está abierta y la puerta 2 está cerrada"
            ],
            "correct_answer": "La puerta 1 está cerrada y la puerta 2 está cerrada",
            "solution_steps": "La alarma se modela como $\\neg(p \\land q)$. Para que la alarma NO se active, esta proposición debe ser falsa, lo que requiere que $p \\land q$ sea verdadera. Esto solo ocurre cuando ambas puertas están cerradas.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        }
    ]
    tanda.extend(morgc_exercises)

    # 4. DE_MORGAN_DISYUNCION (MORGD)
    morgd_exercises = [
        {
            "stable_id": "MORGD-GEN-CONC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_DISYUNCION",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Qué establece la Ley de De Morgan para la disyunción?",
            "choices": [
                "$\\neg(p \\lor q) \\equiv \\neg p \\land \\neg q$",
                "$\\neg(p \\lor q) \\equiv \\neg p \\lor \\neg q$",
                "$\\neg(p \\lor q) \\equiv p \\land q$",
                "$\\neg(p \\lor q) \\equiv \\neg p \\to \\neg q$"
            ],
            "correct_answer": "$\\neg(p \\lor q) \\equiv \\neg p \\land \\neg q$",
            "solution_steps": "La Ley de De Morgan para la disyunción establece que la negación de una disyunción es la conjunción de las negaciones: $\\neg(p \\lor q) \\equiv \\neg p \\land \\neg q$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGD-GEN-CONC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_DISYUNCION",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "Al negar una disyunción, el conectivo 'o' ($\\lor$) se transforma en:",
            "choices": [
                "Conjunción ($\\land$)",
                "Condicional ($\\to$)",
                "Bicondicional ($\\leftrightarrow$)",
                "Disyunción exclusiva"
            ],
            "correct_answer": "Conjunción ($\\land$)",
            "solution_steps": "Por las Leyes de De Morgan, la disyunción se transforma en conjunción al ser negada.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGD-GEN-CONC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_DISYUNCION",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "Decir que es falso que ocurra $p$ o $q$ equivale a decir que:",
            "choices": [
                "Tanto $p$ como $q$ son falsas a la vez",
                "$p$ es verdadero y $q$ es falso",
                "$p$ es falso o $q$ es falso",
                "Al menos una de las dos es verdadera"
            ],
            "correct_answer": "Tanto $p$ como $q$ son falsas a la vez",
            "solution_steps": "$\\neg(p \\lor q) \\equiv \\neg p \\land \\neg q$. Para que esta conjunción sea verdadera, ambas variables deben ser falsas simultáneamente.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGD-GEN-REC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_DISYUNCION",
            "item_group": "reconocimiento",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cuál de las siguientes expresiones es lógicamente equivalente a $\\neg(\\neg p \\lor q)$?",
            "choices": [
                "$p \\land \\neg q$",
                "$p \\lor \\neg q$",
                "$\\neg p \\land \\neg q$",
                "$p \\land q$"
            ],
            "correct_answer": "$p \\land \\neg q$",
            "solution_steps": "Por De Morgan: $\\neg(\\neg p \\lor q) \\equiv \\neg(\\neg p) \\land \\neg q \\equiv p \\land \\neg q$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGD-GEN-PROC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_DISYUNCION",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es la proposición $\\neg(p \\lor q)$ verdadera cuando $p$ es verdadera y $q$ es falsa?",
            "correct_answer": "Falso",
            "solution_steps": "Si $p$ es verdadera, la disyunción $p \\lor q$ es verdadera. Su negación $\\neg(p \\lor q)$ debe ser falsa.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGD-GEN-PROC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_DISYUNCION",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es la proposición $\\neg(\\neg p \\lor \\neg q)$ equivalente a $p \\land q$?",
            "correct_answer": "Verdadero",
            "solution_steps": "Aplicando De Morgan a la disyunción interna: $\\neg(\\neg p) \\land \\neg(\\neg q) \\equiv p \\land q$, lo cual es verdadero.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGD-GEN-PROC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_DISYUNCION",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es la frase 'No es verdad que vaya al cine o juegue videojuegos' equivalente a 'No voy al cine y no juego videojuegos'?",
            "correct_answer": "Verdadero",
            "solution_steps": "Formalizando: $\\neg(c \\lor v) \\equiv \\neg c \\land \\neg v$, lo cual coincide exactamente con la segunda frase.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGD-GEN-PAES-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_DISYUNCION",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Una aerolínea publica el siguiente reglamento de equipaje: 'No está permitido llevar líquidos inflamables o herramientas afiladas en el equipaje de mano'. Si $l$ representa 'llevar líquidos inflamables' y $h$ representa 'llevar herramientas afiladas', ¿cómo se expresa correctamente la restricción en términos lógicos equivalentes?",
            "choices": [
                "No se puede llevar líquidos inflamables y no se puede llevar herramientas afiladas",
                "No se puede llevar líquidos inflamables o no se puede llevar herramientas afiladas",
                "Si se llevan líquidos inflamables, no se pueden llevar herramientas afiladas",
                "Se pueden llevar líquidos inflamables siempre que no se lleven herramientas afiladas"
            ],
            "correct_answer": "No se puede llevar líquidos inflamables y no se puede llevar herramientas afiladas",
            "solution_steps": "La restricción se formaliza como $\\neg(l \\lor h)$. Por De Morgan, esto equivale a $\\neg l \\land \\neg h$, es decir: no llevar líquidos inflamables Y no llevar herramientas afiladas.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGD-GEN-PAES-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_DISYUNCION",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "En el diseño de un puente levadizo, el sistema de seguridad prohíbe que el puente esté abierto si se cumple que hay automóviles cruzando o hay peatones en la vía. Si esto se denota como $\\neg(a \\lor p)$, ¿cuál de las siguientes opciones lógicas es una condición de seguridad equivalente?",
            "choices": [
                "$\\neg a \\land \\neg p$",
                "$\\neg a \\lor \\neg p$",
                "$a \\land p$",
                "$\\neg(a \\land \\neg p)$"
            ],
            "correct_answer": "$\\neg a \\land \\neg p$",
            "solution_steps": "Por la Ley de De Morgan para la disyunción, negar una disyunción equivale a la conjunción de los términos negados: $\\neg(a \\lor p) \\equiv \\neg a \\land \\neg p$.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MORGD-GEN-PAES-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.DE_MORGAN_DISYUNCION",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Considere la proposición compleja $S = \\neg(\\neg p \\lor q)$. Al aplicar la Ley de De Morgan, ¿a qué expresión equivale?",
            "choices": [
                "$p \\land \\neg q$",
                "$p \\lor \\neg q$",
                "$\\neg p \\land q$",
                "$p \\land q$"
            ],
            "correct_answer": "$p \\land \\neg q$",
            "solution_steps": "Aplicando De Morgan para la disyunción: $\\neg(\\neg p) \\land \\neg q$. Por la ley de doble negación, $\\neg(\\neg p) \\equiv p$. El resultado es $p \\land \\neg q$.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        }
    ]
    tanda.extend(morgd_exercises)

    # 5. CONDICIONAL_RECIPROCO (CRECIP)
    crecip_exercises = [
        {
            "stable_id": "CRECIP-GEN-CONC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_RECIPROCO",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cómo se obtiene el recíproco de una proposición condicional $p \\to q$?",
            "choices": [
                "Intercambiando el antecedente y el consecuente: $q \\to p$",
                "Negando ambas proposiciones: $$\\neg p \\to \\neg q$$",
                "Negando e intercambiando ambas: $$\\neg q \\to \\neg p$$",
                "Negando solo el consecuente: $p \\to \\neg q$"
            ],
            "correct_answer": "Intercambiando el antecedente y el consecuente: $q \\to p$",
            "solution_steps": "El recíproco de un condicional $p \\to q$ se obtiene simplemente intercambiando las posiciones del antecedente y el consecuente, resultando en $q \\to p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CRECIP-GEN-CONC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_RECIPROCO",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "Si el condicional original es $A \\to B$, su recíproco es:",
            "choices": [
                "$B \\to A$",
                "$\\neg A \\to \\neg B$",
                "$\\neg B \\to \\neg A$",
                "$A \\land \\neg B$"
            ],
            "correct_answer": "$B \\to A$",
            "solution_steps": "El recíproco simplemente intercambia los roles de antecedente y consecuente: $B \\to A$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CRECIP-GEN-CONC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_RECIPROCO",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cuál de las siguientes relaciones de equivalencia lógica es FALSA para un condicional y sus variaciones?",
            "choices": [
                "Un condicional es lógicamente equivalente a su recíproco",
                "Un condicional es lógicamente equivalente a su contrarrecíproco",
                "El recíproco de un condicional es equivalente a su inverso",
                "El inverso de un condicional no es equivalente al condicional original"
            ],
            "correct_answer": "Un condicional es lógicamente equivalente a su recíproco",
            "solution_steps": "El condicional original $p \\to q$ y su recíproco $q \\to p$ no son lógicamente equivalentes, por lo que esta afirmación es FALSA y es la respuesta correcta.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CRECIP-GEN-REC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_RECIPROCO",
            "item_group": "reconocimiento",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cuál de las siguientes frases representa el recíproco de: 'Si soy un pez, entonces sé nadar'?",
            "choices": [
                "Si sé nadar, entonces soy un pez",
                "Si no soy un pez, entonces no sé nadar",
                "Si no sé nadar, entonces no soy un pez",
                "Soy un pez o sé nadar"
            ],
            "correct_answer": "Si sé nadar, entonces soy un pez",
            "solution_steps": "Intercambiamos el antecedente ('soy un pez') con el consecuente ('sé nadar'), lo que resulta en: 'Si sé nadar, entonces soy un pez'.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CRECIP-GEN-PROC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_RECIPROCO",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es el recíproco de $\\neg p \\to q$ la proposición $q \\to \\neg p$?",
            "correct_answer": "Verdadero",
            "solution_steps": "Intercambiando el antecedente ($\\neg p$) y el consecuente ($q$) obtenemos exactamente $q \\to \\neg p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CRECIP-GEN-PROC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_RECIPROCO",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es el recíproco del condicional $p \\to \\neg q$ la proposición $\\neg q \\to p$?",
            "correct_answer": "Verdadero",
            "solution_steps": "Al intercambiar las posiciones de $p$ y $\\neg q$, el nuevo condicional resultante es $\\neg q \\to p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CRECIP-GEN-PROC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_RECIPROCO",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "Si un condicional es verdadero, ¿su recíproco debe ser obligatoriamente verdadero?",
            "correct_answer": "Falso",
            "solution_steps": "Los valores de verdad de un condicional y su recíproco son independientes. Por ejemplo, 'Si es cuadrado, es rectángulo' es verdadero, pero 'Si es rectángulo, es cuadrado' es falso.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CRECIP-GEN-PAES-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_RECIPROCO",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "En un teorema de geometría se afirma: 'Si un cuadrilátero es un cuadrado, entonces sus diagonales son perpendiculares'. ¿Cuál es el recíproco de esta afirmación y qué valor de verdad posee?",
            "choices": [
                "'Si las diagonales de un cuadrilátero son perpendiculares, entonces es un cuadrado', y es falso",
                "'Si las diagonales de un cuadrilátero no son perpendiculares, entonces no es un cuadrado', y es verdadero",
                "'Si un cuadrilátero no es un cuadrado, entonces sus diagonales no son perpendiculares', y es falso",
                "'Si las diagonales de un cuadrilátero son perpendiculares, entonces es un cuadrado', y es verdadero"
            ],
            "correct_answer": "'Si las diagonales de un cuadrilátero son perpendiculares, entonces es un cuadrado', y es falso",
            "solution_steps": "El recíproco intercambia el antecedente y el consecuente: 'Si las diagonales son perpendiculares, entonces es un cuadrado'. Esta afirmación es falsa, porque un rombo tiene diagonales perpendiculares pero no es necesariamente un cuadrado.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CRECIP-GEN-PAES-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_RECIPROCO",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Un programador establece una regla para una base de datos: 'Si un usuario es administrador, entonces tiene acceso de escritura'. ¿Cuál de las siguientes afirmaciones describe correctamente el recíproco de esta regla y su consecuencia práctica?",
            "choices": [
                "'Si tiene acceso de escritura, entonces es administrador', lo cual permite que usuarios no administradores tengan acceso si la regla original no es un bicondicional",
                "'Si no es administrador, entonces no tiene acceso de escritura', lo cual es equivalente a la regla original",
                "'Si no tiene acceso de escritura, entonces no es administrador', lo cual es el recíproco",
                "'Si es administrador, entonces no tiene acceso de escritura', lo cual es la negación"
            ],
            "correct_answer": "'Si tiene acceso de escritura, entonces es administrador', lo cual permite que usuarios no administradores tengan acceso si la regla original no es un bicondicional",
            "solution_steps": "El recíproco es 'Si tiene acceso de escritura, entonces es administrador'. En la práctica, si el recíproco no se cumple de manera obligatoria, podría haber usuarios con acceso de escritura sin ser administradores (por ejemplo, editores).",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CRECIP-GEN-PAES-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_RECIPROCO",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Considere la proposición condicional en álgebra: 'Si $x = 2$, entonces $x^2 = 4$'. ¿Cuál de las siguientes opciones expresa correctamente su recíproco y determina su valor de verdad en el conjunto de los números reales?",
            "choices": [
                "'Si $x^2 = 4$, entonces $x = 2$', y es falso en los reales porque $x$ podría ser $-2$",
                "'Si $x \\neq 2$, entonces $x^2 \\neq 4$', y es verdadero en los reales",
                "'Si $x^2 \\neq 4$, entonces $x \\neq 2$', y es falso en los reales",
                "'Si $x^2 = 4$, entonces $x = 2$', y es siempre verdadero en los reales"
            ],
            "correct_answer": "'Si $x^2 = 4$, entonces $x = 2$', y es falso en los reales porque $x$ podría ser $-2$",
            "solution_steps": "El recíproco intercambia los lados: 'Si $x^2 = 4$, entonces $x = 2$'. Esto es falso en $\\mathbb{R}$ porque $(-2)^2 = 4$, donde $x = -2$ sirve como contraejemplo.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        }
    ]
    tanda.extend(crecip_exercises)

    return tanda

def create_tanda_b01_6():
    tanda = []
    
    # 6. CONDICIONAL_INVERSO (CINVER)
    cinver_exercises = [
        # Conceptuales (3)
        {
            "stable_id": "CINVER-GEN-CONC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_INVERSO",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cómo se define el inverso de una proposición condicional $p \\to q$?",
            "choices": [
                "$\\neg p \\to \\neg q$",
                "$q \\to p$",
                "$\\neg q \\to \\neg p$",
                "$\\neg p \\lor q$"
            ],
            "correct_answer": "$\\neg p \\to \\neg q$",
            "solution_steps": "El inverso de un condicional se construye negando tanto el antecedente como el consecuente, sin alterar el sentido de la implicación: $\\neg p \\to \\neg q$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CINVER-GEN-CONC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_INVERSO",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "Si el condicional original es $A \\to \\neg B$, ¿cuál es su condicional inverso?",
            "choices": [
                "$\\neg A \\to B$",
                "$\\neg A \\to \\neg B$",
                "$B \\to A$",
                "$\\neg B \\to A$"
            ],
            "correct_answer": "$\\neg A \\to B$",
            "solution_steps": "Negamos el antecedente $A$ para obtener $\\neg A$. Negamos el consecuente $\\neg B$ para obtener $\\neg(\\neg B) \\equiv B$. El inverso es $\\neg A \\to B$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CINVER-GEN-CONC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_INVERSO",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Qué relación de equivalencia lógica tiene un condicional $p \\to q$ con su inverso $\\neg p \\to \\neg q$?",
            "choices": [
                "No son equivalentes en general",
                "Son siempre equivalentes",
                "Son equivalentes solo si el antecedente es verdadero",
                "Son equivalentes si y solo si el consecuente es verdadero"
            ],
            "correct_answer": "No son equivalentes en general",
            "solution_steps": "Como demuestran las tablas de verdad, sus valores de verdad difieren en la segunda y tercera fila de la tabla, por lo que $p \\to q \\not\\equiv \\neg p \\to \\neg q$.",
            "status": "ready",
            "source_kind": "manual"
        },
        # Reconocimiento (1)
        {
            "stable_id": "CINVER-GEN-REC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_INVERSO",
            "item_group": "reconocimiento",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cuál de las siguientes frases representa el inverso de: 'Si soy mayor de edad, entonces puedo votar'?",
            "choices": [
                "Si no soy mayor de edad, entonces no puedo votar",
                "Si puedo votar, entonces soy mayor de edad",
                "Si no puedo votar, entonces no soy mayor de edad",
                "No soy mayor de edad o puedo votar"
            ],
            "correct_answer": "Si no soy mayor de edad, entonces no puedo votar",
            "solution_steps": "Negamos el antecedente ('no soy mayor de edad') y negamos el consecuente ('no puedo votar'), manteniendo la estructura de la implicación.",
            "status": "ready",
            "source_kind": "manual"
        },
        # Procedimiento (3)
        {
            "stable_id": "CINVER-GEN-PROC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_INVERSO",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es el inverso de $\\neg p \\to q$ la proposición $p \\to \\neg q$?",
            "correct_answer": "Verdadero",
            "solution_steps": "Negamos el antecedente $\\neg p$ obteniendo $p$, y negamos el consecuente $q$ obteniendo $\\neg q$. El inverso es $p \\to \\neg q$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CINVER-GEN-PROC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_INVERSO",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es el inverso de $p \\to q$ lógicamente equivalente a su recíproco $q \\to p$?",
            "correct_answer": "Verdadero",
            "solution_steps": "El inverso es $\\neg p \\to \\neg q$ y el recíproco es $q \\to p$. Por la ley del contrarrecíproco, $\\neg p \\to \\neg q$ es equivalente a $\\neg(\\neg q) \\to \\neg(\\neg p) \\equiv q \\to p$. Sus tablas de verdad coinciden.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CINVER-GEN-PROC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_INVERSO",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es el inverso de un condicional verdadero siempre verdadero?",
            "correct_answer": "Falso",
            "solution_steps": "El valor del condicional y de su inverso son independientes. Por ejemplo, 'Si un número es divisible por 4, es par' es verdadero, pero su inverso 'Si no es divisible por 4, no es par' es falso (ej. el número 6).",
            "status": "ready",
            "source_kind": "manual"
        },
        # Tipo PAES (3)
        {
            "stable_id": "CINVER-GEN-PAES-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_INVERSO",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Un médico afirma: 'Si el paciente tiene fiebre alta, entonces requiere reposo absoluto'. ¿Cuál de las siguientes opciones expresa correctamente el inverso de esta afirmación?",
            "choices": [
                "'Si el paciente no tiene fiebre alta, entonces no requiere reposo absoluto'",
                "'Si el paciente requiere reposo absoluto, entonces tiene fiebre alta'",
                "'Si el paciente no requiere reposo absoluto, entonces no tiene fiebre alta'",
                "'El paciente tiene fiebre alta o no requiere reposo absoluto'"
            ],
            "correct_answer": "'Si el paciente no tiene fiebre alta, entonces no requiere reposo absoluto'",
            "solution_steps": "El inverso se obtiene negando el antecedente y el consecuente sin alterar su orden: 'Si el paciente no tiene fiebre alta, entonces no requiere reposo absoluto'.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CINVER-GEN-PAES-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_INVERSO",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "¿Cuál de las siguientes expresiones lógicas representa el inverso de un condicional compuesto con variables $t$ (temperatura) y $v$ (ventilador) de la forma $t \\to v$?",
            "choices": [
                "$\\neg t \\to \\neg v$",
                "$v \\to t$",
                "$\\neg v \\to \\neg t$",
                "$t \\lor \\neg v$"
            ],
            "correct_answer": "$\\neg t \\to \\neg v$",
            "solution_steps": "Por definición, el inverso de la implicación $t \\to v$ es $\\neg t \\to \\neg v$.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CINVER-GEN-PAES-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_INVERSO",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Considere la proposición: 'Si un número real $x$ es menor que 0, entonces $x^2$ es positivo'. ¿Cuál es el inverso de esta afirmación y qué valor de verdad tiene en el conjunto de los reales?",
            "choices": [
                "'Si $x$ no es menor que 0, entonces $x^2$ no es positivo', y es falso porque para $x = 2$, $x^2 = 4$ es positivo",
                "'Si $x^2$ no es positivo, entonces $x$ no es menor que 0', y es verdadero",
                "'Si $x$ es mayor que 0, entonces $x^2$ es negativo', y es verdadero",
                "'Si $x^2$ es positivo, entonces $x$ es menor que 0', y es falso"
            ],
            "correct_answer": "'Si $x$ no es menor que 0, entonces $x^2$ no es positivo', y es falso porque para $x = 2$, $x^2 = 4$ es positivo",
            "solution_steps": "El inverso niega el antecedente ($x \\ge 0$) y el consecuente ($x^2 \\le 0$): 'Si $x \\ge 0$, entonces $x^2 \\le 0$'. Esto es falso en $\\mathbb{R}$ ya que el número 2 cumple el antecedente ($2 \\ge 0$) pero su cuadrado ($4$) es positivo (no cumple el consecuente).",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        }
    ]
    tanda.extend(cinver_exercises)

    # 7. CONDICIONAL_CONTRARRECIPROCO (CCONT)
    ccont_exercises = [
        # Conceptuales (3)
        {
            "stable_id": "CCONT-GEN-CONC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_CONTRARRECIPROCO",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cómo se define el contrarrecíproco de un condicional $p \\to q$?",
            "choices": [
                "$\\neg q \\to \\neg p$",
                "$\\neg p \\to \\neg q$",
                "$q \\to p$",
                "$\\neg p \\lor q$"
            ],
            "correct_answer": "$\\neg q \\to \\neg p$",
            "solution_steps": "El contrarrecíproco se construye negando e intercambiando tanto el antecedente como el consecuente: $\\neg q \\to \\neg p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CCONT-GEN-CONC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_CONTRARRECIPROCO",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Qué relación de equivalencia existe entre un condicional y su contrarrecíproco?",
            "choices": [
                "Son siempre lógicamente equivalentes",
                "Nunca son equivalentes",
                "Son equivalentes solo si el antecedente es falso",
                "Son equivalentes si y solo si ambas variables son verdaderas"
            ],
            "correct_answer": "Son siempre lógicamente equivalentes",
            "solution_steps": "La columna final de la tabla de verdad de $p \\to q$ y $\\neg q \\to \\neg p$ coincide fila por fila. Por lo tanto, $p \\to q \\equiv \\neg q \\to \\neg p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CCONT-GEN-CONC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_CONTRARRECIPROCO",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "Si el condicional original es $\\neg A \\to B$, su contrarrecíproco es:",
            "choices": [
                "$\\neg B \\to A$",
                "$\\neg B \\to \\neg A$",
                "$B \\to \\neg A$",
                "$A \\to \\neg B$"
            ],
            "correct_answer": "$\\neg B \\to A$",
            "solution_steps": "Negamos el consecuente: $\\neg B$. Negamos el antecedente: $\\neg(\\neg A) \\equiv A$. Intercambiamos posiciones: $\\neg B \\to A$.",
            "status": "ready",
            "source_kind": "manual"
        },
        # Reconocimiento (1)
        {
            "stable_id": "CCONT-GEN-REC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_CONTRARRECIPROCO",
            "item_group": "reconocimiento",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cuál de las siguientes frases representa el contrarrecíproco de: 'Si es un felino, entonces es un mamífero'?",
            "choices": [
                "Si no es un mamífero, entonces no es un felino",
                "Si no es un felino, entonces no es un mamífero",
                "Si es un mamífero, entonces es un felino",
                "No es un felino o es un mamífero"
            ],
            "correct_answer": "Si no es un mamífero, entonces no es un felino",
            "solution_steps": "Negamos y cambiamos el orden: 'Si no es un mamífero (consecuente negado), entonces no es un felino (antecedente negado)'.",
            "status": "ready",
            "source_kind": "manual"
        },
        # Procedimiento (3)
        {
            "stable_id": "CCONT-GEN-PROC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_CONTRARRECIPROCO",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es el contrarrecíproco de $\\neg p \\to \\neg q$ la proposición $q \\to p$?",
            "correct_answer": "Verdadero",
            "solution_steps": "Negamos el consecuente: $\\neg(\\neg q) \\equiv q$. Negamos el antecedente: $\\neg(\\neg p) \\equiv p$. Al intercambiarlos nos queda $q \\to p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CCONT-GEN-PROC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_CONTRARRECIPROCO",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "¿Es el contrarrecíproco de $p \\to \\neg q$ la proposición $q \\to \\neg p$?",
            "correct_answer": "Verdadero",
            "solution_steps": "Negamos el consecuente: $\\neg(\\neg q) \\equiv q$. Negamos el antecedente: $\\neg p$. Al intercambiarlos obtenemos $q \\to \\neg p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CCONT-GEN-PROC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_CONTRARRECIPROCO",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "Si se sabe que el contrarrecíproco de un condicional es falso, ¿el condicional original puede ser verdadero?",
            "correct_answer": "Falso",
            "solution_steps": "No. Un condicional y su contrarrecíproco son lógicamente equivalentes. Tienen el mismo valor de verdad; si uno es falso, el otro obligatoriamente es falso.",
            "status": "ready",
            "source_kind": "manual"
        },
        # Tipo PAES (3)
        {
            "stable_id": "CCONT-GEN-PAES-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_CONTRARRECIPROCO",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "En una clase de álgebra, un estudiante afirma: 'Si un número real $x$ es mayor que 5, entonces su cuadrado $x^2$ es mayor que 25'. ¿Cuál de las siguientes opciones describe correctamente la afirmación contrarrecíproca y su valor de verdad?",
            "choices": [
                "'Si $x^2 \\le 25$, entonces $x \\le 5$', la cual es lógicamente equivalente a la original y es verdadera",
                "'Si $x \\le 5$, entonces $x^2 \\le 25$', la cual es el inverso y es verdadera",
                "'Si $x^2 \\le 25$, entonces $x \\le 5$', la cual es el recíproco y es falsa",
                "'Si $x^2 > 25$, entonces $x > 5$', la cual es equivalente y es falsa"
            ],
            "correct_answer": "'Si $x^2 \\le 25$, entonces $x \\le 5$', la cual es lógicamente equivalente a la original y es verdadera",
            "solution_steps": "El contrarrecíproco de $x > 5 \\to x^2 > 25$ niega e intercambia los lados: $\\neg(x^2 > 25) \\to \\neg(x > 5)$, lo que se traduce como $x^2 \\le 25 \\to x \\le 5$. Puesto que la original es verdadera (para números mayores que 5, su cuadrado es mayor que 25), su contrarrecíproco también es verdadero.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CCONT-GEN-PAES-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_CONTRARRECIPROCO",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Un contrato de alquiler contiene la cláusula: 'Si el arrendatario no paga el alquiler antes del día 5, entonces se aplicará una multa'. Si $p$ es 'paga el alquiler antes del día 5' y $m$ es 'se aplica una multa', ¿cuál es la proposición contrarrecíproca equivalente a la cláusula?",
            "choices": [
                "$\\neg m \\to p$",
                "$\\neg m \\to \\neg p$",
                "$m \\to \\neg p$",
                "$p \\to \\neg m$"
            ],
            "correct_answer": "$\\neg m \\to p$",
            "solution_steps": "La cláusula original es $\\neg p \\to m$. Negando e intercambiando: $\\neg m  \\to \\neg(\\neg p) \\equiv \\neg m \\to p$. Esta es la expresión contrarrecíproca lógicamente equivalente.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "CCONT-GEN-PAES-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.CONDICIONAL_CONTRARRECIPROCO",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Un científico postula la teoría: 'Si el compuesto $X$ se expone a la luz, entonces se descompone'. Para demostrar de forma indirecta esta teoría usando el contrarrecíproco, ¿cuál de los siguientes experimentos debería realizar?",
            "choices": [
                "Verificar que si el compuesto $X$ no se descompone, es porque no se expuso a la luz",
                "Verificar que si el compuesto $X$ se descompone, es porque se expuso a la luz",
                "Verificar que si el compuesto $X$ no se expuso a la luz, entonces no se descompone",
                "Verificar qué ocurre cuando el compuesto se expone a la oscuridad"
            ],
            "correct_answer": "Verificar que si el compuesto $X$ no se descompone, es porque no se expuso a la luz",
            "solution_steps": "El contrarrecíproco de 'expone a la luz $\\to$ se descompone' es 'no se descompone $\\to$ no se expuso a la luz'. Demostrar esta última afirmación es lógicamente equivalente a demostrar la teoría original.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        }
    ]
    tanda.extend(ccont_exercises)

    # 8. MODUS_PONENS (MPON)
    mpon_exercises = [
        # Conceptuales (3)
        {
            "stable_id": "MPON-GEN-CONC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_PONENS",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cuál es el esquema formal de la regla de inferencia Modus Ponens?",
            "choices": [
                "$p, p \\to q \\vdash q$",
                "$\\neg q, p \\to q \\vdash \\neg p$",
                "$q, p \\to q \\vdash p$",
                "$\\neg p, p \\to q \\vdash \\neg q$"
            ],
            "correct_answer": "$p, p \\to q \\vdash q$",
            "solution_steps": "El Modus Ponens establece que si tenemos un condicional $p \\to q$ y afirmamos su antecedente $p$, podemos concluir el consecuente $q$. Esquema: $p, p \\to q \\vdash q$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MPON-GEN-CONC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_PONENS",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "La premisa fundamental del Modus Ponens consiste en un condicional. Para aplicar la regla, ¿qué se debe afirmar en la segunda premisa?",
            "choices": [
                "El antecedente del condicional",
                "El consecuente del condicional",
                "La negación del antecedente",
                "La negación del consecuente"
            ],
            "correct_answer": "El antecedente del condicional",
            "solution_steps": "Modus Ponens es la regla que 'afirma al afirmar'. Requiere la afirmación del antecedente para deducir válidamente el consecuente.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MPON-GEN-CONC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_PONENS",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Qué nombre en latín recibe formalmente la regla de inferencia Modus Ponens?",
            "choices": [
                "Modus Ponendo Ponens",
                "Modus Tollendo Tollens",
                "Modus Tollendo Ponens",
                "Modus Ponendo Tollens"
            ],
            "correct_answer": "Modus Ponendo Ponens",
            "solution_steps": "El nombre completo es Modus Ponendo Ponens, que significa 'el modo que al afirmar, afirma'.",
            "status": "ready",
            "source_kind": "manual"
        },
        # Reconocimiento (1)
        {
            "stable_id": "MPON-GEN-REC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_PONENS",
            "item_group": "reconocimiento",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "Dado el argumento: 'Si el agua hierve, entonces se evapora. El agua está hirviendo. Por lo tanto, el agua se evapora'. ¿Qué regla de inferencia se aplicó?",
            "choices": [
                "Modus Ponens",
                "Modus Tollens",
                "Silogismo Disyuntivo",
                "Doble Negación"
            ],
            "correct_answer": "Modus Ponens",
            "solution_steps": "El argumento responde al esquema: Premisa 1 ($p \\to q$), Premisa 2 ($p$), Conclusión ($q$). Esta es la regla del Modus Ponens.",
            "status": "ready",
            "source_kind": "manual"
        },
        # Procedimiento (3)
        {
            "stable_id": "MPON-GEN-PROC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_PONENS",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "Dadas las premisas $p \\to q$ y $p$, ¿es válido concluir $q$ por la regla del Modus Ponens?",
            "correct_answer": "Verdadero",
            "solution_steps": "Sí. Ese es exactamente el esquema formal y básico de la regla: $p, p \\to q \\vdash q$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MPON-GEN-PROC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_PONENS",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "Dadas las premisas $\\neg a \\to b$ y $\\neg a$, ¿es la conclusión válida $b$ por Modus Ponens?",
            "correct_answer": "Verdadero",
            "solution_steps": "Sí, porque el antecedente del condicional es $\\neg a$, y la segunda premisa afirma exactamente ese antecedente $\\neg a$. Por lo tanto, concluimos el consecuente $b$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MPON-GEN-PROC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_PONENS",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "Dadas las premisas $x \\to y$ y $y$, ¿es válido concluir $x$ por Modus Ponens?",
            "correct_answer": "Falso",
            "solution_steps": "No. Concluir el antecedente $x$ a partir de la afirmación del consecuente $y$ es una falacia lógica llamada falacia de afirmación del consecuente.",
            "status": "ready",
            "source_kind": "manual"
        },
        # Tipo PAES (3)
        {
            "stable_id": "MPON-GEN-PAES-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_PONENS",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "En una campaña de seguridad vial se establece la premisa: 'Si conduces bajo los efectos del alcohol, entonces se te suspenderá la licencia de conducir'. Si se constata que 'Juan conduce bajo los efectos del alcohol', ¿cuál es la conclusión válida que se obtiene y qué regla lógica la respalda?",
            "choices": [
                "Se le suspenderá la licencia de conducir, respaldado por Modus Ponens",
                "No se le suspenderá la licencia de conducir, respaldado por Modus Tollens",
                "Si no se le suspende la licencia, entonces no consumió alcohol, por recíproco",
                "No se puede obtener ninguna conclusión válida en este caso"
            ],
            "correct_answer": "Se le suspenderá la licencia de conducir, respaldado por Modus Ponens",
            "solution_steps": "Tenemos el condicional 'alcohol $\\to$ suspensión' y la afirmación del antecedente 'conduce bajo efectos del alcohol'. Por Modus Ponens ($p, p \\to q \\vdash q$), concluimos que se le suspenderá la licencia.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MPON-GEN-PAES-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_PONENS",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Un sistema informático de acceso tiene las siguientes reglas: Premisa 1: 'Si el usuario ingresa la contraseña correcta, entonces el sistema le concede acceso'. Premisa 2: 'El usuario ingresó la contraseña correcta'. ¿Cuál es el estado de acceso del usuario según las reglas lógicas?",
            "choices": [
                "El sistema le concede acceso por Modus Ponens",
                "El sistema no le concede acceso por Modus Tollens",
                "El acceso se concede por falacia de afirmación del consecuente",
                "El sistema no puede determinar el acceso"
            ],
            "correct_answer": "El sistema le concede acceso por Modus Ponens",
            "solution_steps": "Se cumplen las condiciones de Modus Ponens: se tiene la regla condicional y se afirma su antecedente. Por ende, la deducción lógica válida es que el sistema le concede acceso.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MPON-GEN-PAES-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_PONENS",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Considere las premisas: Premisa 1: $\\neg p \\to (q \\lor r)$, Premisa 2: $\\neg p$. ¿Cuál es la conclusión que se obtiene aplicando la regla del Modus Ponens?",
            "choices": [
                "$q \\lor r$",
                "$p$",
                "$\\neg(q \\lor r)$",
                "$q \\land r$"
            ],
            "correct_answer": "$q \\lor r$",
            "solution_steps": "La Premisa 2 afirma el antecedente completo $\\neg p$ del condicional de la Premisa 1. Por lo tanto, Modus Ponens nos permite concluir directamente el consecuente: $q \\lor r$.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        }
    ]
    tanda.extend(mpon_exercises)

    # 9. MODUS_TOLLENS (MTOL)
    mtol_exercises = [
        # Conceptuales (3)
        {
            "stable_id": "MTOL-GEN-CONC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_TOLLENS",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Cuál es el esquema formal de la regla de inferencia Modus Tollens?",
            "choices": [
                "$\\neg q, p \\to q \\vdash \\neg p$",
                "$p, p \\to q \\vdash q$",
                "$q, p \\to q \\vdash p$",
                "$\\neg p, p \\to q \\vdash \\neg q$"
            ],
            "correct_answer": "$\\neg q, p \\to q \\vdash \\neg p$",
            "solution_steps": "El Modus Tollens establece que si tenemos un condicional $p \\to q$ y la negación de su consecuente $\\neg q$, podemos concluir válidamente la negación de su antecedente $\\neg p$. Esquema: $\\neg q, p \\to q \\vdash \\neg p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MTOL-GEN-CONC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_TOLLENS",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "En la regla de inferencia Modus Tollens, si se tiene como premisa un condicional, ¿qué condición debe cumplir la segunda premisa?",
            "choices": [
                "Debe negar el consecuente del condicional",
                "Debe afirmar el antecedente del condicional",
                "Debe negar el antecedente del condicional",
                "Debe afirmar el consecuente del condicional"
            ],
            "correct_answer": "Debe negar el consecuente del condicional",
            "solution_steps": "Modus Tollens es la regla que 'niega al negar'. Requiere la negación del consecuente en la segunda premisa para poder inferir la negación del antecedente.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MTOL-GEN-CONC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_TOLLENS",
            "item_group": "conceptuales",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "¿Qué nombre en latín recibe la regla de inferencia Modus Tollens?",
            "choices": [
                "Modus Tollendo Tollens",
                "Modus Ponendo Ponens",
                "Modus Tollendo Ponens",
                "Modus Ponendo Tollens"
            ],
            "correct_answer": "Modus Tollendo Tollens",
            "solution_steps": "El nombre completo es Modus Tollendo Tollens, que significa 'el modo que al negar, niega'.",
            "status": "ready",
            "source_kind": "manual"
        },
        # Reconocimiento (1)
        {
            "stable_id": "MTOL-GEN-REC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_TOLLENS",
            "item_group": "reconocimiento",
            "format": "multiple_choice",
            "difficulty": "basica",
            "competencia": "U",
            "prompt": "Dado el argumento: 'Si el sospechoso es culpable, entonces estaba nervioso. El sospechoso no estaba nervioso. Por lo tanto, el sospechoso no es culpable'. ¿Qué regla de inferencia se utilizó?",
            "choices": [
                "Modus Tollens",
                "Modus Ponens",
                "Silogismo Hipotético",
                "Contrarrecíproco"
            ],
            "correct_answer": "Modus Tollens",
            "solution_steps": "El argumento responde al esquema: Premisa 1 ($p \\to q$), Premisa 2 ($\\neg q$), Conclusión ($\\neg p$). Esta es la regla del Modus Tollens.",
            "status": "ready",
            "source_kind": "manual"
        },
        # Procedimiento (3)
        {
            "stable_id": "MTOL-GEN-PROC-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_TOLLENS",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "Dadas las premisas $p \\to q$ y $\\neg q$, ¿es válido concluir $\\neg p$ por Modus Tollens?",
            "correct_answer": "Verdadero",
            "solution_steps": "Sí. Ese es exactamente el esquema de la regla de inferencia Modus Tollens: $\\neg q, p \\to q \\vdash \\neg p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MTOL-GEN-PROC-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_TOLLENS",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "Dadas las premisas $p \\to \\neg q$ and $q$, ¿es válido concluir $\\neg p$ por Modus Tollens?",
            "correct_answer": "Verdadero",
            "solution_steps": "Sí. El consecuente es $\\neg q$. Su negación es $\\neg(\\neg q) \\equiv q$. Como la segunda premisa es $q$, se está negando correctamente el consecuente. Por Modus Tollens, concluimos la negación del antecedente: $\\neg p$.",
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MTOL-GEN-PROC-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_TOLLENS",
            "item_group": "procedimiento_basico",
            "format": "true_false",
            "difficulty": "basica",
            "prompt": "Dadas las premisas $p \\to q$ y $\\neg p$, ¿es válido concluir $\\neg q$ por Modus Tollens?",
            "correct_answer": "Falso",
            "solution_steps": "No. Negar el antecedente no permite deducir nada sobre el consecuente. Esto constituye la falacia de negación del antecedente.",
            "status": "ready",
            "source_kind": "manual"
        },
        # Tipo PAES (3)
        {
            "stable_id": "MTOL-GEN-PAES-1",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_TOLLENS",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Un médico forense analiza un caso basándose en la regla: 'Si la víctima falleció por envenenamiento, entonces se encontrarían rastros de la sustancia $Z$ en la sangre'. Si el informe del laboratorio indica que 'No se encontraron rastros de la sustancia $Z$ en la sangre', ¿cuál es la conclusión válida que se puede obtener?",
            "choices": [
                "La víctima no falleció por envenenamiento, obtenido por Modus Tollens",
                "La víctima falleció por envenenamiento, obtenido por Modus Ponens",
                "No se puede concluir nada sobre la causa de muerte",
                "La víctima falleció por otra causa, obtenido por la falacia de afirmación del consecuente"
            ],
            "correct_answer": "La víctima no falleció por envenenamiento, obtenido por Modus Tollens",
            "solution_steps": "Tenemos el condicional 'envenenamiento $\\to$ sustancia Z' y la negación del consecuente 'no hay sustancia Z'. Por Modus Tollens ($\\neg q, p \\to q \\vdash \\neg p$), concluimos la negación del antecedente: no falleció por envenenamiento.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MTOL-GEN-PAES-2",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_TOLLENS",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "En un control de calidad industrial se tiene la regla: 'Si el sensor de calor funciona correctamente, entonces la alarma se enciende cuando la temperatura supera los $100^\\circ\\text{C}$'. Durante una prueba a $120^\\circ\\text{C}$, la alarma no se encendió. ¿Cuál es la conclusión correcta sobre el sensor de calor?",
            "choices": [
                "El sensor de calor no funciona correctamente, concluido por Modus Tollens",
                "El sensor de calor funciona correctamente, concluido por Modus Ponens",
                "No se puede concluir nada sobre el sensor de calor",
                "La alarma está defectuosa"
            ],
            "correct_answer": "El sensor de calor no funciona correctamente, concluido por Modus Tollens",
            "solution_steps": "El condicional es: 'funciona $\\to$ alarma enciende'. Constatamos que la alarma no encendió (negación del consecuente). Por Modus Tollens, concluimos que el sensor no funciona correctamente.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        },
        {
            "stable_id": "MTOL-GEN-PAES-3",
            "semantic_id": "MAT.FUND.RAZONAMIENTO_LOGICO.MODUS_TOLLENS",
            "item_group": "tipo_paes",
            "format": "multiple_choice",
            "difficulty": "media",
            "competencia": "U",
            "prompt": "Considere las premisas: Premisa 1: $(a \\land b) \\to \\neg c$, Premisa 2: $c$. ¿Cuál es la conclusión válida que se deduce de este razonamiento aplicando Modus Tollens y leyes de equivalencia?",
            "choices": [
                "$\\neg(a \\land b)$",
                "$a \\land b$",
                "$\\neg a \\lor c$",
                "$c \\to \\neg(a \\land b)$"
            ],
            "correct_answer": "$\\neg(a \\land b)$",
            "solution_steps": "La Premisa 2 ($c$) es la negación del consecuente $\\neg c$. Por Modus Tollens, concluimos la negación del antecedente $(a \\land b)$, la cual se expresa como $\\neg(a \\land b)$.",
            "paes_style": True,
            "status": "ready",
            "source_kind": "manual"
        }
    ]
    tanda.extend(mtol_exercises)

    return tanda

def main():
    # Tanda B01-5
    tanda_b01_5 = create_tanda_b01_5()
    os.makedirs('docs/conocimiento/ejercicios', exist_ok=True)
    with open('docs/conocimiento/ejercicios/mat-fund-razonamiento-banco-gen-1.jsonl', 'w', encoding='utf-8') as f:
        for ex in tanda_b01_5:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')
    print(f"Successfully generated {len(tanda_b01_5)} exercises in mat-fund-razonamiento-banco-gen-1.jsonl")

    # Tanda B01-6
    tanda_b01_6 = create_tanda_b01_6()
    with open('docs/conocimiento/ejercicios/mat-fund-razonamiento-banco-gen-2.jsonl', 'w', encoding='utf-8') as f:
        for ex in tanda_b01_6:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')
    print(f"Successfully generated {len(tanda_b01_6)} exercises in mat-fund-razonamiento-banco-gen-2.jsonl")

if __name__ == '__main__':
    main()
