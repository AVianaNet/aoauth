from aiohttp import web
from json import dumps


async def json(data, status, headers=None):
    response = web.json_response(data, status=status, headers=headers, content_type='application/json')
    return response
