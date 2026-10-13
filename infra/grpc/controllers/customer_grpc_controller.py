import logging
from typing import Any, Mapping

import grpc

from app.use_cases.billing_use_case import BillingUseCase
from infra.grpc.pb import billing_pb2, billing_pb2_grpc

logger = logging.getLogger(__name__)


class CustomerGrpcController(billing_pb2_grpc.BillingServiceServicer):
    def __init__(self, billing_use_case: BillingUseCase) -> None:
        self.billing_use_case = billing_use_case

    async def ProcessBilling(
        self,
        request: billing_pb2.BillingRequest,
        context: grpc.aio.ServicerContext,
    ) -> billing_pb2.BillingResponse:
        customer_id: str = request.customer_id

        try:
            result: Mapping[str, Any] = await self.billing_use_case.execute(customer_id)
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
        except Exception as error:
            if str(error) == "Customer not found":
                await context.abort(grpc.StatusCode.NOT_FOUND, "Customer not found")

            logger.error(error, exc_info=True)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")


__all__ = ["CustomerGrpcController"]
