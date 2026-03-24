from django import forms
from apps.content.models import Resource


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            "title",
            "subject",
            "description",
            "content_body",
            "resource_type",
            "external_url",
            "is_published",
        ]