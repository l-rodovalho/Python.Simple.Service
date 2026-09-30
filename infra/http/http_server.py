from typing import Callable, Awaitable
from aiohttp import web

from infra.config.configuration import env
from infra.http.routes import setup_http_routes


@web.middleware
async def error_middleware(
    request: web.Request, 
    handler: Callable[[web.Request], Awaitable[web.StreamResponse]]
) -> web.StreamResponse:
    try:
        return await handler(request)
    except web.HTTPNotFound:
        return web.json_response({"error": "Route not found"}, status=404)
    except web.HTTPException as ex:
        return web.json_response({"error": ex.reason}, status=ex.status)
    except Exception as ex:
        return web.json_response({"error": "Internal Server Error"}, status=500)


def create_app() -> web.Application:
    app = web.Application(middlewares=[error_middleware])
    setup_http_routes(app)
    return app


async def start_http_server() -> web.AppRunner:
    http_port = int(env.HTTP_PORT)
    app = create_app()

    runner = web.AppRunner(app, access_log=None)
    await runner.setup()
    
    site = web.TCPSite(runner, "0.0.0.0", http_port)
    await site.start()

    print(f"HTTP server listening on port {http_port}", flush=True)
    return runner


__all__ = ["create_app", "start_http_server", "error_middleware"]