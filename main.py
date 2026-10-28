import sys
import asyncio

from infra.config.configuration import env
from infra.database.connection import DatabaseConnection
from infra.database.repositories.customer_repository import CustomerRepository
from infra.http.http_server import start_http_server
from infra.grpc.grpc_server import start_grpc_server
from app.use_cases.billing_use_case import BillingUseCase
from app.use_cases.calculate_invoices_use_case import CalculateInvoicesUseCase

async def main() -> None:
    try:
        pool = await DatabaseConnection.connect()

        billing_use_case = BillingUseCase(CustomerRepository(pool))
        calculate_invoices_use_case = CalculateInvoicesUseCase(max_invoices=100000)
        protocol = env.PROTOCOL

        if protocol == "HTTP":
            await start_http_server(billing_use_case, calculate_invoices_use_case)
        elif protocol == "GRPC":
            await start_grpc_server(billing_use_case, calculate_invoices_use_case)
        else:
            raise ValueError("PROTOCOL must be HTTP or GRPC")

        await asyncio.Event().wait()

    except Exception as error:
        print(f"Error on trying to start server: {error}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass