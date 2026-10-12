import logging
from aiohttp import web

from app.use_cases.billing_use_case import BillingUseCase

logger = logging.getLogger(__name__)


class CustomerHttpController:
    def __init__(self, billing_use_case: BillingUseCase) -> None:
        self.billing_use_case = billing_use_case

    async def process_billing(self, request: web.Request) -> web.Response:
        customer_id = request.match_info.get("customer_id")
        if not customer_id:
            return web.json_response({"error": "Missing customer_id parameter"}, status=400)

        try:
            result: dict = await self.billing_use_case.execute(customer_id)
            return web.json_response(result, status=200)
        except Exception as error:
            if str(error) == "Customer not found":
                return web.json_response({"error": "Customer not found"}, status=404)

            logger.error(error, exc_info=True)
            return web.json_response({"error": "Internal server error"}, status=500)


__all__ = ["CustomerHttpController"]
