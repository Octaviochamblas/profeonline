from django import forms


def apply_form_classes(form):
    for field in form.fields.values():
        widget = field.widget
        existing = widget.attrs.get("class", "").split()

        if isinstance(widget, forms.CheckboxSelectMultiple):
            extra = ["checkbox-list"]
        elif isinstance(widget, forms.CheckboxInput):
            extra = ["form-check-input"]
        else:
            extra = ["form-control"]

        classes = []
        for value in existing + extra:
            if value and value not in classes:
                classes.append(value)

        widget.attrs["class"] = " ".join(classes)
