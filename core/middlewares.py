import json
import time
import traceback

from fastapi import status, Request
from fastapi.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp, Scope, Receive, Send
from core.extensions import RequestWithBody



class CatchExceptionsMiddleware(BaseHTTPMiddleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            await super().__call__(scope, receive, send)
        except RuntimeError as exc_msg:
            request = Request(scope, receive, send)
            if not await request.is_disconnected():
                raise exc_msg

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        request_body_bytes = await request.body()
        request_with_body = RequestWithBody(request.scope, request_body_bytes)

        try:
            response = await call_next(request_with_body)

        except Exception as exc_msg:
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal Server Error"},
            )
            headers = {
                "Authorization": request.headers.get("Authorization"),
                "Host": request.headers.get("Host"),
                "X-Real-Ip": request.headers.get("X-Real-Ip"),
                "X-Forwarded-For": request.headers.get("X-Forwarded-For"),
                "X-Forwarded-Host": request.headers.get("X-Forwarded-Host"),
                "X-Forwarded-Port": request.headers.get("X-Forwarded-Port"),
            }
            error_data = [
                f"status: {response.status_code}\n",
                f"params: {request.query_params}\n",
                f"path_params: {request.url.path}\n",
                f"time: {time.time() - start_time}\n",
                f"headers: {json.dumps(headers)}\n",
                f"body: {request_with_body.json_body}\n",
                f"message: {exc_msg}\n",
                f"traceback: {traceback.format_exc()[-1000:]}",
            ]
            error_msg = "".join(error_data)
            print(f"Error occurred: {str(error_data)}")

            

        return response


