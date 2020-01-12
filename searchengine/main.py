from aiohttp import web
import asyncio

from searchengine.views import SiteHandler


def setup_routes(app, handler):
    router = app.router
    h = handler
    router.add_get('', h.search, name='search')


async def init():
    app = web.Application()
    handler = SiteHandler()

    setup_routes(app, handler)
    host, port = '127.0.0.1', '9002'
    return app, host, port


def main():
    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init())
    web.run_app(app, host=host, port=port)
