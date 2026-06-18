"""Resiliencia y seguridad de las llamadas a la IA.

Cubre: reintento con backoff ante 429, que la API key NO quede en la URL ni en
los mensajes de error (se filtraba antes en los logs), y que vaya en el header.
"""

import json
from unittest.mock import MagicMock, patch

from django.test import TestCase
from requests import HTTPError

from apps.content.services import ai_generation_service as svc

KEY = "SECRET-KEY-123"

GEMINI_OK = {
    "candidates": [{"content": {"parts": [{"text": json.dumps([
        {
            "text": "Pregunta",
            "explanation": "Explicación",
            "choices": [
                {"text": "a", "is_correct": True},
                {"text": "b", "is_correct": False},
                {"text": "c", "is_correct": False},
                {"text": "d", "is_correct": False},
            ],
        }
    ])}]}}]
}


def _resp(status, json_data=None, error_msg=None):
    r = MagicMock()
    r.status_code = status
    r.headers = {}
    if error_msg is not None:
        r.raise_for_status.side_effect = HTTPError(error_msg)
    else:
        r.raise_for_status.return_value = None
        r.json.return_value = json_data
    return r


class GeminiResilienceTests(TestCase):

    @patch("time.sleep")
    @patch("requests.post")
    def test_retries_on_429_then_succeeds(self, mock_post, mock_sleep):
        """Ante un 429 espera y reintenta; al segundo intento (200) tiene éxito."""
        mock_post.side_effect = [_resp(429), _resp(200, GEMINI_OK)]

        result = svc._call_gemini_api("prompt", KEY)

        self.assertEqual(len(result), 1)
        self.assertEqual(mock_post.call_count, 2)
        mock_sleep.assert_called_once_with(svc._BACKOFF_BASE)

    @patch("time.sleep")
    @patch("requests.post")
    def test_honors_longer_retry_after(self, mock_post, mock_sleep):
        limited = _resp(429)
        limited.headers = {"Retry-After": "12"}
        mock_post.side_effect = [limited, _resp(200, GEMINI_OK)]

        svc._call_gemini_api("prompt", KEY)

        mock_sleep.assert_called_once_with(12.0)

    @patch("time.sleep")
    @patch("requests.post")
    def test_key_not_leaked_in_error(self, mock_post, mock_sleep):
        """Aunque el error contenga la key, el mensaje propagado la sanea."""
        mock_post.return_value = _resp(429, error_msg=f"429 for url ...?key={KEY}")

        with self.assertRaises(RuntimeError) as ctx:
            svc._call_gemini_api("prompt", KEY)

        self.assertNotIn(KEY, str(ctx.exception))
        self.assertIn("***", str(ctx.exception))

    @patch("requests.post")
    def test_key_goes_in_header_not_url(self, mock_post):
        """La key viaja en el header x-goog-api-key y nunca en la URL."""
        mock_post.return_value = _resp(200, GEMINI_OK)

        svc._call_gemini_api("prompt", KEY)

        args, kwargs = mock_post.call_args
        self.assertNotIn(KEY, args[0])
        self.assertEqual(kwargs["headers"].get("x-goog-api-key"), KEY)
