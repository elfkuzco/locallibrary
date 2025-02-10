from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send


class AuthorizationHeaderFromCookieMiddleware:
    """Set Authorization header from cookie if missing from request.

    Because the tokens are set as httponly and thus innaccessible to client
    side JavaScript, this middleware extracts the token set by the
    registration/login route and updates the request headers.
    """

    def __init__(self, app: ASGIApp, *, cookie_name: str):
        self.app = app
        self.cookie_name = cookie_name

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        request = Request(scope)
        request_headers = MutableHeaders(scope=scope)
        # First check if the request has the Authorization header set.
        # if it does, we leave it as it is and forward the request to
        # the next handler
        authorization_header = request_headers.get("authorization", "")
        if authorization_header:
            return await self.app(scope, receive, send)

        token_cookie = request.cookies.get(self.cookie_name)
        # If token was not set, forward the request to the next handler
        if not token_cookie:
            return await self.app(scope, receive, send)
        # We proceed to set the token value as the value of
        # the Authorization Header and forward the request to the
        # next handler
        request_headers["Authorization"] = f"Bearer {token_cookie}"

        # Update the scope's headers - convert headers to list of tuples
        scope["headers"] = [
            (key.lower().encode(), value.encode())
            for key, value in request_headers.items()
        ]

        return await self.app(scope, receive, send)
