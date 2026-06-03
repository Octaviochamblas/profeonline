import json
import logging
from datetime import timedelta
from urllib.parse import urlsplit
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db.models.functions import TruncWeek
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from apps.core.models import AnalyticsEvent
from apps.core.ratelimit import increment_rate_limit
from apps.content.models.completion import ResourceView, ResourceCompletion
from apps.content.models.evaluation import QuizAttempt, TopicEvaluationAttempt

logger = logging.getLogger(__name__)

User = get_user_model()

# Allowlist de eventos permitidos para cliente
ANALYTICS_ALLOWLIST = {
    "signup",
    "login_google",
    "whatsapp_click",
    "phone_click",
    "video_play",
    "attachment_download",
    "resource_comprendido",
    "page_view",
}


ANALYTICS_METADATA_ALLOWLIST = {
    "whatsapp_click": set(),
    "phone_click": set(),
    "attachment_download": set(),
    "video_play": {"video_id"},
    "resource_comprendido": set(),
    "page_view": set(),
}


def sanitize_path(path):
    """Guarda solo pathnames locales; nunca querystrings ni URLs absolutas."""
    if not isinstance(path, str):
        return ""
    parsed_path = urlsplit(path.strip()).path
    if not parsed_path.startswith("/"):
        return ""
    return parsed_path[:255]


def sanitize_event_metadata(event_name, metadata):
    """Sanitiza metadata con allowlist por evento para evitar PII accidental."""
    if not isinstance(metadata, dict):
        return {}

    allowed_keys = ANALYTICS_METADATA_ALLOWLIST.get(event_name, set())
    if not allowed_keys:
        return {}

    sanitized = {}
    for key in allowed_keys:
        value = metadata.get(key)
        if not isinstance(value, str):
            continue
        value = value.strip()
        if key == "video_id":
            if not (1 <= len(value) <= 32):
                continue
            if not all(char.isalnum() or char in "_-" for char in value):
                continue
            sanitized[key] = value

    return sanitized


class AnalyticsEventPostView(View):
    """
    Endpoint POST para guardar eventos de analítica.
    No utiliza csrf_exempt; confía en la validación CSRF estándar de Django.
    """

    def post(self, request, *args, **kwargs):
        # 1. Throttling al inicio
        attempts_limit = getattr(settings, "ANALYTICS_RATE_LIMIT_ATTEMPTS", 60)
        window = getattr(settings, "ANALYTICS_RATE_LIMIT_WINDOW", 60)

        attempts = increment_rate_limit(request, "analytics_throttle", attempts_limit, window)
        if attempts > attempts_limit:
            logger.warning(
                f"Throttle de analítica excedido para cliente: {attempts} peticiones"
            )
            return HttpResponse("Demasiados intentos de analítica.", status=429)

        # 2. Parseo de datos (soporta JSON y FormData para sendBeacon)
        name = None
        path = None
        metadata = {}

        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                name = data.get("name")
                path = data.get("path")
                metadata = data.get("metadata", {})
            except json.JSONDecodeError:
                return HttpResponseBadRequest("Payload JSON inválido.")
        else:
            name = request.POST.get("name")
            path = request.POST.get("path")
            metadata_str = request.POST.get("metadata", "{}")
            try:
                metadata = json.loads(metadata_str)
            except json.JSONDecodeError:
                metadata = {}

        # 3. Validación de allowlist y parámetros obligatorios
        if not name or name not in ANALYTICS_ALLOWLIST:
            return HttpResponseBadRequest("Nombre de evento no válido o no permitido.")
        path = sanitize_path(path)
        if not path:
            return HttpResponseBadRequest("El parámetro path es obligatorio.")

        if not isinstance(metadata, dict):
            metadata = {}

        # 3.5. Sanitizar y limitar metadata
        metadata = sanitize_event_metadata(name, metadata)

        # 4. Creación del evento
        AnalyticsEvent.objects.create(
            name=name,
            path=path,
            user=request.user if request.user.is_authenticated else None,
            metadata=metadata,
        )

        return HttpResponse(status=204)


@method_decorator(staff_member_required, name="dispatch")
class AnalyticsDashboardView(TemplateView):
    """
    Dashboard de analítica interna visible sólo para usuarios del staff.
    """

    template_name = "core/panel_analitica.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Registros por semana de las últimas 12 semanas
        twelve_weeks_ago = timezone.now() - timedelta(weeks=12)
        weekly_stats = (
            User.objects.filter(date_joined__gte=twelve_weeks_ago)
            .annotate(week=TruncWeek("date_joined"))
            .values("week")
            .annotate(count=Count("id"))
            .order_by("week")
        )

        # Formatear la respuesta de semanas
        formatted_weekly_stats = []
        for stat in weekly_stats:
            week_date = stat["week"]
            if week_date:
                # Mostrar formato 'Semana del DD/MM'
                formatted_weekly_stats.append(
                    {
                        "label": f"Semana {week_date.strftime('%d/%m')}",
                        "count": stat["count"],
                    }
                )
        context["weekly_registrations"] = formatted_weekly_stats

        # 2. Clics WhatsApp y Teléfono
        context["whatsapp_clicks"] = AnalyticsEvent.objects.filter(name="whatsapp_click").count()
        context["phone_clicks"] = AnalyticsEvent.objects.filter(name="phone_click").count()
        context["video_plays"] = AnalyticsEvent.objects.filter(name="video_play").count()
        context["attachment_downloads"] = AnalyticsEvent.objects.filter(
            name="attachment_download"
        ).count()

        # 3. Recursos más vistos de ResourceView (ledger existente)
        top_resources = (
            ResourceView.objects.values(
                "resource_id", "resource__title", "resource__slug", "resource__subject__name"
            )
            .annotate(views_count=Count("id"))
            .order_by("-views_count")[:10]
        )
        context["top_resources"] = top_resources

        # 4. Embudo de Conversión (Funnel)
        total_pageviews = AnalyticsEvent.objects.filter(name="page_view").count()
        total_users = User.objects.count()
        users_with_views = ResourceView.objects.values("user").distinct().count()
        users_with_completions = ResourceCompletion.objects.values("user").distinct().count()

        # Evaluaciones intentadas (QuizAttempt y TopicEvaluationAttempt únicos por user)
        quiz_users = set(QuizAttempt.objects.values_list("user_id", flat=True))
        eval_users = set(TopicEvaluationAttempt.objects.values_list("user_id", flat=True))
        users_with_attempts = len(quiz_users.union(eval_users))

        whatsapp_clicks = context["whatsapp_clicks"]

        # Construcción del Funnel con porcentajes
        steps = [
            {"name": "Visitas Home (Pageviews)", "value": total_pageviews},
            {"name": "Registros Totales", "value": total_users},
            {"name": "Recursos Vistos", "value": users_with_views},
            {"name": "Recursos Comprendidos", "value": users_with_completions},
            {"name": "Ejercitación/Evaluación", "value": users_with_attempts},
            {"name": "Clics WhatsApp", "value": whatsapp_clicks},
        ]

        # Calcular porcentajes relativos al paso anterior y al paso inicial
        funnel_data = []
        initial_val = steps[0]["value"]
        prev_val = initial_val

        for i, step in enumerate(steps):
            val = step["value"]
            pct_initial = (val / initial_val * 100) if initial_val > 0 else 0
            pct_prev = (val / prev_val * 100) if prev_val > 0 else 0

            funnel_data.append(
                {
                    "name": step["name"],
                    "value": val,
                    "pct_initial": round(pct_initial, 1),
                    "pct_prev": round(pct_prev, 1),
                }
            )
            prev_val = val

        context["funnel"] = funnel_data

        return context
