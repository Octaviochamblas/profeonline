from django.db.models import Case, IntegerField, Value, When


def order_resources_by_manual_order(queryset):
    """Order resources by manual order, keeping unordered resources at the end."""
    return queryset.annotate(
        missing_manual_order=Case(
            When(order=0, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by("missing_manual_order", "order", "title")
