from django import forms
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