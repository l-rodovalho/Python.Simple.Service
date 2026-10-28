import logging
from aiohttp import web

from app.errors import CustomerNotFoundError, InvalidCustomerIdError
from app.use_cases.billing_use_case import BillingUseCase
from infra.http.responses import json_response

logger = logging.getLogger(__name__)


class CustomerHttpController:
    def __init__(self, billing_use_case: BillingUseCase) -> None:
        self.billing_use_case = billing_use_case

    async def process_billing(self, request: web.Request) -> web.Response:
        try:
            result: dict = await self.billing_use_case.execute(request.match_info.get("customer_id"))
            return json_response(result, status=200)
        except InvalidCustomerIdError as error:
            return json_response({"error": str(error)}, status=400)
        except CustomerNotFoundError as error:
            return json_response({"error": str(error)}, status=404)
        except Exception as error:
            logger.error(error, exc_info=True)
            return json_response({"error": "Internal server error"}, status=500)


__all__ = ["CustomerHttpController"]
