from typing import Any
import json

from fastapi.requests import Request
from starlette.types import Scope, Message
from peewee import DatabaseProxy

db = DatabaseProxy()

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
