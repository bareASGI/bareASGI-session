"""Session"""

from datetime import datetime, timedelta
from typing import cast

from bareasgi import Application, HttpRequest

from .middleware import SessionMiddleware
from .storage import SessionStorage

SESSION_CONTEXT_KEY = '__bareasgi_session__'


def add_session_middleware[T](
        app: Application,
        storage: SessionStorage[T],
        *,
        context_key: str = SESSION_CONTEXT_KEY,
        cookie_name: bytes = b'bareASGI-session',
        expires: datetime | None = None,
        max_age: int | timedelta | None = None,
        path: bytes | None = None,
        domain: bytes | None = None,
        secure: bool = False,
        http_only: bool = False,
        same_site: bytes | None = None
) -> Application:
    """Add session storage middleware.

    If no storage provider is supplied the default is to store the sessions in
    memory.

    The default settings are **not secure**. In production the following settings
    are recommended.

    Setting `http_only=True` forbids JavaScript from accessing the cookie in
    the browser. With `same_site="Strict"` or `same_site="Lax"`, the browser
    prevents the cookie being sent on cross-site requests. If the server is
    delivering over https, setting `secure=True` will prevent the cookie from
    being sent from non-https requests.

    Args:
        app (Application): The ASGI application.
        storage (SessionStorage[T] | None, optional): The storage provider.
            Defaults to None.
        context_key (str, optional): The key in the applications context where session
            data can be found. Defaults to SESSION_CONTEXT_KEY.
        cookie_name (bytes, optional): The cookie name. Defaults to b'bareASGI-session'.
        expires (datetime | None, optional): The cookie expiry time. Defaults
            to None.
        max_age (int | timedelta | None, optional): The maximum age of
            the cookie. Defaults to None.
        path (bytes | None, optional): The cookie path. Defaults to None.
        domain (bytes | None, optional): The cookie domain. If unspecified
            the host header of the request will be used. Defaults to None.
        secure (bool, optional): The cookie is only sent if the request is
            using https Defaults to False.
        http_only (bool, optional): If true the cookie is not available with
            javascript in the client. Defaults to False.
        same_site (bytes | None, optional): Controls whether the cookie is
            sent cross origin. Defaults to None.

    Returns:
        Application: The ASGI application.
    """

    session_middleware = SessionMiddleware[T](
        context_key,
        storage,
        cookie_name,
        expires,
        max_age,
        path,
        domain,
        secure,
        http_only,
        same_site
    )

    app.middlewares.append(session_middleware)

    return app


def session_data[T](
        request: HttpRequest,
        _type: type[T] | None = None,
        *,
        context_key: str = SESSION_CONTEXT_KEY
) -> T:
    return cast(T, request.context[context_key])
