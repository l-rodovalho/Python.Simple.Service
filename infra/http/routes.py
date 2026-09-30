from aiohttp import web

from infra.http.controllers.health_http_controller import HealthHttpController


def setup_http_routes(app: web.Application) -> None:
    health_http_controller = HealthHttpController()
    
    app.router.add_get("/health", health_http_controller.get_health)


__all__ = ["setup_http_routes"]