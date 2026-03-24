from django import forms
from apps.content.models import Resource, Topic


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            "title",
            "subject",
            "topic",
            "description",
            "content_body",
            "resource_type",
            "external_url",
            "is_published",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["topic"].queryset = Topic.objects.none()

        if "subject" in self.data:
            try:
                subject_id = int(self.data.get("subject"))
                self.fields["topic"].queryset = Topic.objects.filter(
                    subject_id=subject_id,
                    is_active=True,
                ).order_by("name")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.subject:
            self.fields["topic"].queryset = Topic.objects.filter(
                subject=self.instance.subject,
                is_active=True,
            ).order_by("name")