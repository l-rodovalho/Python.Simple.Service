from aiohttp import web

class HealthHttpController:
    async def get_health(self, request: web.Request) -> web.Response:
        response = {"message": "OK"}
        return web.json_response(response, status=200)

__all__ = ["HealthHttpController"]