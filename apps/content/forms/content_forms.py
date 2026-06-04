from django import forms

from apps.core.forms import apply_form_classes
from apps.content.models import Area, Level, Subject, Topic


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["name", "description", "order", "is_active"]
        labels = {
            "description": "Descripción",
            "is_active": "Activa",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "description", "is_active"]
        labels = {
            "description": "Descripción",
            "is_active": "Activa",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["subject", "name", "description", "resource_ordering_method", "is_active"]
        labels = {
            "description": "Descripción",
            "resource_ordering_method": "Método de ordenación de recursos",
            "is_active": "Activo",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].queryset = Subject.objects.filter(is_active=True).order_by("name")
        apply_form_classes(self)


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ["name", "description", "order", "is_active"]
        labels = {
            "description": "Descripción",
            "is_active": "Activo",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)
