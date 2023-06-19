from typing import Any
import json
from pathlib import Path

from fastapi.requests import Request
from starlette.types import Scope, Message
from peewee import DatabaseProxy
from fastapi_mail import ConnectionConfig

db = DatabaseProxy()

email_conf = ConnectionConfig(
    MAIL_USERNAME = "aaalizada37@gmail.com",
    MAIL_PASSWORD = "h e l w t x j c l q g h y a i r",
    MAIL_FROM = "aaalizada37@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Amil",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = False,
    # TEMPLATE_FOLDER = Path(__file__) / 'templates',
)

class RequestWithBody(Request):
    def __init__(self, scope: Scope, body: bytes) -> None:
        super().__init__(scope, self._receive)
        self._body = body
        self.body = body
        self._body_returned = False

    @property
    def json_body(self) -> dict:
        try:
            return json.loads(self.body)
        except Exception:  # noqa
            return {}

    async def _receive(self) -> Message:
        if self._body_returned:
            return {"type": "http.disconnect"}
        else:
            self._body_returned = True
            return {"type": "http.request", "body": self._body, "more_body": False}
