from pathlib import Path
import yaml


ROOT = Path("docs/conocimiento/contenido")

SOURCE_FILES = [
    "mat-alg-inecuaciones_lineales-definicion.yaml",
    "mat-alg-inecuaciones_lineales-resolucion_despeje.yaml",
    "mat-alg-inecuaciones_lineales-conjunto_solucion.yaml",
    "mat-alg-inecuaciones_lineales-multiplicacion_negativa_despeje.yaml",
    "mat-alg-inecuaciones_lineales-coeficientes_fraccionarios.yaml",
    "mat-alg-inecuaciones_lineales-signos_agrupacion.yaml",
    "mat-alg-inecuaciones_lineales-incognita_ambos_lados.yaml",
    "mat-alg-inecuaciones_lineales-expresion_intervalo.yaml",
    "mat-alg-inecuaciones_lineales-expresion_recta.yaml",
    "mat-alg-inecuaciones_lineales-verificacion_solucion.yaml",
    "mat-alg-inecuaciones_lineales-inecuacion_sin_solucion.yaml",
    "mat-alg-inecuaciones_lineales-inecuacion_todo_real.yaml",
    "mat-alg-sistemas_inecuaciones-definicion.yaml",
    "mat-alg-sistemas_inecuaciones-resolucion_individual.yaml",
    "mat-alg-sistemas_inecuaciones-interseccion_soluciones.yaml",
    "mat-alg-sistemas_inecuaciones-representacion_recta.yaml",
    "mat-alg-sistemas_inecuaciones-sistema_sin_solucion.yaml",
    "mat-alg-sistemas_inecuaciones-traduccion_intervalo.yaml",
    "mat-alg-inecuaciones_valor_absoluto-definicion.yaml",
    "mat-alg-inecuaciones_valor_absoluto-menor_que_positivo.yaml",
    "mat-alg-inecuaciones_valor_absoluto-mayor_que_positivo.yaml",
    "mat-alg-inecuaciones_valor_absoluto-menor_igual_positivo.yaml",
    "mat-alg-inecuaciones_valor_absoluto-mayor_igual_positivo.yaml",
    "mat-alg-inecuaciones_valor_absoluto-constante_negativa.yaml",
    "mat-alg-inecuaciones_valor_absoluto-interpretacion_intervalo.yaml",
    "mat-alg-modelamiento_desigualdades-planteamiento_inecuacion.yaml",
]


def clean_text(value):
    if value is None:
        return ""
    text = str(value).replace("\r\n", "\n").strip()
    return text


def clean_list(values):
    if not values:
        return []
    result = []
    for item in values:
        text = clean_text(item)
        if text:
            result.append(text)
    return result


def split_explanation(value):
    text = clean_text(value)
    if not text:
        return []
    parts = [part.strip() for part in text.split("\n") if part.strip()]
    return parts or [text]


def normalize_response(value):
    if isinstance(value, bool):
        return "Verdadero" if value else "Falso"
    text = clean_text(value).lower()
    if text in {"true", "verdadero"}:
        return "Verdadero"
    if text in {"false", "falso"}:
        return "Falso"
    return clean_text(value)


def transform_old_schema(data):
    content = data.get("content") or {}
    ejemplos = []
    for example in content.get("ejemplos_resueltos") or []:
        tipo = clean_text(example.get("tipo"))
        if tipo == "abierto":
            ejemplos.append(
                {
                    "titulo": clean_text(example.get("titulo")),
                    "enunciado": clean_text(example.get("enunciado")),
                    "solucion_pasos": clean_list(example.get("pasos")),
                }
            )
        elif tipo == "verdadero_falso":
            ejemplos.append(
                {
                    "titulo": clean_text(example.get("afirmacion") or example.get("titulo")),
                    "respuesta": normalize_response(example.get("respuesta")),
                    "solucion_pasos": split_explanation(example.get("explicacion")),
                }
            )

    errores = []
    for error in content.get("errores_frecuentes") or []:
        if isinstance(error, dict):
            text = clean_text(error.get("descripcion"))
        else:
            text = clean_text(error)
        if text:
            errores.append(text)

    return {
        "semantic_id": clean_text(data.get("semantic_id")),
        "titulo": clean_text(data.get("title")),
        "objetivo": clean_text(data.get("description")),
        "introduccion": clean_text(content.get("introduccion")),
        "resumen": clean_text(content.get("resumen")),
        "explicacion": clean_text(content.get("explicacion")),
        "procedimiento": clean_list(content.get("pasos")),
        "ejemplos": ejemplos,
        "errores_frecuentes": errores,
        "fuente": "Currículum Nacional MINEDUC y elaboración pedagógica ProfeOnline.",
        "estado": "publicado",
    }


for filename in SOURCE_FILES:
    path = ROOT / filename
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if "content" in data:
        data = transform_old_schema(data)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000),
        encoding="utf-8",
    )
    print(f"converted {filename}")
