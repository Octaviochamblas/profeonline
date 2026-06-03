import logging
from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from apps.core.models import AnalyticsEvent

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def track_google_login(request, user, **kwargs):
    """
    Registra el evento de analítica 'login_google' si el usuario se ha
    autenticado mediante Google OAuth (detectado a través de request.sociallogin).
    """
    if hasattr(request, "sociallogin"):
        provider = request.sociallogin.account.provider
        AnalyticsEvent.objects.create(
            name="login_google",
            path=request.path,
            user=user,
            metadata={"provider": provider}
        )
        logger.info(
            f"Registrado evento login_google para el usuario {user.username} "
            f"(proveedor: {provider})"
        )
