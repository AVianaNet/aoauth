from aiohttp import web
from core.router import routes
from core.conf import *
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_cache import cache, setup_cache


async def factory():
    app = web.Application(middlewares=[session_middleware(EncryptedCookieStorage(SESSION_SECRET))])
    setup_cache(app)
    routes(app)
    return app

