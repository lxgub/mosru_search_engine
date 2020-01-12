from aiohttp import web
from searchengine.engine import SearchEngine


class SiteHandler:
    def __init__(self):
        self.engine = SearchEngine()

    async def search(self, request):
        query_string = request.query.get('req')
        if query_string:
            categories = await self.engine.get_categories(query_string)
            return web.json_response(categories)
        else:
            raise web.HTTPBadRequest(text='400: BadRequest. You must send GET request type of:'
                                          ' http://{host}/?req=<your search phrase>'.format(host=request.host))
