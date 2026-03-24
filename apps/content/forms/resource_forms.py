from django import forms
from apps.content.models import Resource


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["title", "description", "is_published"]