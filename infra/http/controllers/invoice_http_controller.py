import logging
from aiohttp import web

from app.errors import InvalidRequestError
from app.use_cases.calculate_invoices_use_case import CalculateInvoicesUseCase
from infra.http.responses import json_response

logger = logging.getLogger(__name__)


class InvoiceHttpController:
    def __init__(self, calculate_invoices_use_case: CalculateInvoicesUseCase) -> None:
        self.calculate_invoices_use_case = calculate_invoices_use_case

    async def calculate(self, request: web.Request) -> web.Response:
        try:
            payload = await request.json()
        except ValueError:
            return json_response({"error": "Malformed JSON body"}, status=400)

        try:
            is_object = type(payload) is dict
            result: dict = self.calculate_invoices_use_case.execute(
                payload.get("invoices") if is_object else None,
                payload.get("rounds", 1) if is_object else 1,
            )
            return json_response(result, status=200)
        except InvalidRequestError as error:
            return json_response({"error": str(error)}, status=400)
        except Exception as error:
            logger.error(error, exc_info=True)
            return json_response({"error": "Internal server error"}, status=500)


__all__ = ["InvoiceHttpController"]

