from django import forms
from apps.core.forms import apply_form_classes
from apps.content.models import Module


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = [
            "title",
            "subject",
            "objective",
            "description",
            "order",
            "is_published",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)
