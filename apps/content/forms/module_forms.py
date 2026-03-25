from django import forms
from apps.content.models import Level, Module, Topic


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = [
            "title",
            "subject",
            "topic",
            "levels",
            "objective",
            "description",
            "order",
            "is_published",
        ]
        widgets = {
            "levels": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["topic"].queryset = Topic.objects.none()
        self.fields["levels"].queryset = Level.objects.filter(
            is_active=True
        ).order_by("order", "name")

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