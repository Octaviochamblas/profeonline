import json
import urllib.request
from email.utils import parseaddr

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class BrevoApiEmailBackend(BaseEmailBackend):
    """Envía correos usando la API HTTP de Brevo (HTTPS, puerto 443).

    Evita el bloqueo de puertos SMTP salientes (25/465/587/2525) que aplican
    algunos hosts como Railway, que provoca timeouts al intentar conectar por
    SMTP y termina en errores 500.
    """

    api_url = "https://api.brevo.com/v3/smtp/email"

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.api_key = getattr(settings, "BREVO_API_KEY", "") or ""
        self.timeout = getattr(settings, "EMAIL_TIMEOUT", 10) or 10

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        if not self.api_key:
            if not self.fail_silently:
                raise ValueError("BREVO_API_KEY no está configurado.")
            return 0

        sent = 0
        for message in email_messages:
            if self._send(message):
                sent += 1
        return sent

    def _send(self, message):
        data = json.dumps(self._build_payload(message)).encode("utf-8")
        request = urllib.request.Request(
            self.api_url,
            data=data,
            headers={
                "api-key": self.api_key,
                "content-type": "application/json",
                "accept": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return 200 <= response.status < 300
        except Exception:
            if not self.fail_silently:
                raise
            return False

    def _build_payload(self, message):
        from_name, from_email = parseaddr(
            message.from_email or settings.DEFAULT_FROM_EMAIL
        )

        payload = {
            "sender": {"email": from_email},
            "to": [{"email": addr} for addr in message.to],
            "subject": message.subject,
            "textContent": message.body,
        }
        if from_name:
            payload["sender"]["name"] = from_name

        if getattr(message, "cc", None):
            payload["cc"] = [{"email": addr} for addr in message.cc]
        if getattr(message, "bcc", None):
            payload["bcc"] = [{"email": addr} for addr in message.bcc]
        if getattr(message, "reply_to", None):
            reply_name, reply_email = parseaddr(message.reply_to[0])
            payload["replyTo"] = {"email": reply_email}
            if reply_name:
                payload["replyTo"]["name"] = reply_name

        for content, mimetype in getattr(message, "alternatives", []) or []:
            if mimetype == "text/html":
                payload["htmlContent"] = content
                break

        return payload
