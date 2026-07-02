from django import forms

from apps.content.models import NodeContent


class NodeContentEditorForm(forms.Form):
    objetivo = forms.CharField(required=False)
    introduccion = forms.CharField(required=False)
    resumen = forms.CharField(required=False)
    explicacion = forms.CharField(required=False)
    procedimiento = forms.JSONField(required=False)
    ejemplos = forms.JSONField(required=False)
    errores_frecuentes = forms.JSONField(required=False)
    fuente = forms.CharField(required=False)
    estado = forms.ChoiceField(choices=NodeContent.ESTADO_CHOICES)
    updated_at = forms.CharField(required=False)

    def clean_procedimiento(self):
        return self._clean_string_list(
            self.cleaned_data.get("procedimiento"), "procedimiento"
        )

    def clean_errores_frecuentes(self):
        return self._clean_string_list(
            self.cleaned_data.get("errores_frecuentes"), "errores_frecuentes"
        )

    def clean_ejemplos(self):
        value = self.cleaned_data.get("ejemplos") or []
        if not isinstance(value, list):
            raise forms.ValidationError("Debe ser una lista de ejemplos.")

        cleaned = []
        allowed_answers = {"", "Sí", "No", "Verdadero", "Falso"}
        for index, example in enumerate(value, start=1):
            if not isinstance(example, dict):
                raise forms.ValidationError(f"El ejemplo {index} no es válido.")

            title = self._clean_text(example.get("titulo"))
            statement = self._clean_text(example.get("enunciado"))
            answer = self._clean_text(example.get("respuesta"))
            if answer not in allowed_answers:
                raise forms.ValidationError(
                    f"La respuesta del ejemplo {index} no es válida."
                )
            steps = self._clean_string_list(
                example.get("solucion_pasos"), f"solucion_pasos del ejemplo {index}"
            )
            if not title and not statement:
                raise forms.ValidationError(
                    f"El ejemplo {index} necesita título o enunciado."
                )

            item = {
                "titulo": title,
                "enunciado": statement,
                "solucion_pasos": steps,
            }
            if answer:
                item["respuesta"] = answer
            cleaned.append(item)
        return cleaned

    @staticmethod
    def _clean_text(value):
        if value is None:
            return ""
        if not isinstance(value, str):
            raise forms.ValidationError("Todos los textos deben ser cadenas.")
        return value.strip()

    @classmethod
    def _clean_string_list(cls, value, field_name):
        value = value or []
        if not isinstance(value, list):
            raise forms.ValidationError(f"{field_name} debe ser una lista.")
        cleaned = []
        for item in value:
            text = cls._clean_text(item)
            if text:
                cleaned.append(text)
        return cleaned
