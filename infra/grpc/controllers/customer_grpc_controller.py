import logging
from typing import Any, Mapping

import grpc

from app.errors import CustomerNotFoundError, InvalidCustomerIdError, InvalidRequestError
from app.use_cases.billing_use_case import BillingUseCase
from app.use_cases.calculate_invoices_use_case import CalculateInvoicesUseCase
from infra.grpc.pb import billing_pb2, billing_pb2_grpc

logger = logging.getLogger(__name__)


class CustomerGrpcController(billing_pb2_grpc.BillingServiceServicer):
    def __init__(
        self,
        billing_use_case: BillingUseCase,
        calculate_invoices_use_case: CalculateInvoicesUseCase,
    ) -> None:
        self.billing_use_case = billing_use_case
        self.calculate_invoices_use_case = calculate_invoices_use_case

    async def ProcessBilling(
        self,
        request: billing_pb2.BillingRequest,
        context: grpc.aio.ServicerContext,
    ) -> billing_pb2.BillingResponse:
        try:
            result: Mapping[str, Any] = await self.billing_use_case.execute(request.customer_id)
        except InvalidCustomerIdError as error:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(error))
        except CustomerNotFoundError as error:
            await context.abort(grpc.StatusCode.NOT_FOUND, str(error))
        except Exception as error:
            logger.error(error, exc_info=True)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

        metrics_data = result.get("metrics", {})

        return billing_pb2.BillingResponse(
            customer_id=str(result.get("customer_id", "")),
            name=str(result.get("name", "")),
            metrics=billing_pb2.Metrics(
                invoices_processed=int(metrics_data.get("invoices_processed", 0)),
                total_paid=str(metrics_data.get("total_paid", "0.00")),
                total_due_with_interest=str(metrics_data.get("total_due_with_interest", "0.00")),
            ),
        )

    async def CalculateInvoices(
        self,
        request: billing_pb2.CalculateInvoicesRequest,
        context: grpc.aio.ServicerContext,
    ) -> billing_pb2.CalculateInvoicesResponse:
        invoices = [
            {"amount": i.amount, "days_overdue": i.days_overdue, "paid": i.paid, "tier": i.tier}
            for i in request.invoices
        ]

        try:
            result: Mapping[str, Any] = self.calculate_invoices_use_case.execute(invoices, request.rounds or 1)
        except InvalidRequestError as error:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(error))
        except Exception as error:
            logger.error(error, exc_info=True)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

        return billing_pb2.CalculateInvoicesResponse(**result)


__all__ = ["CustomerGrpcController"]
