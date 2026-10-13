import sys
import asyncio

from infra.database.connection import DatabaseConnection
from infra.http.http_server import start_http_server
from infra.grpc.grpc_server import start_grpc_server
from app.factories.make_billing_use_case import make_billing_use_case

async def start() -> None:
    try:
        await DatabaseConnection.connect()

        billing_use_case = make_billing_use_case()

        await asyncio.gather(
            start_http_server(billing_use_case),
            start_grpc_server(billing_use_case)
        )

    except Exception as error:
        print(f"Error on trying to start server: {error}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        pass