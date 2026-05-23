from django.views.generic import ListView
from apps.content.models import Area

class AreaListView(ListView):
    model = Area
    template_name = "pages/area_list.html"
    context_object_name = "areas"

    def get_queryset(self):
        return Area.objects.filter(is_active=True).order_by("order", "name")
