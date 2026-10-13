import grpc

from app.use_cases.billing_use_case import BillingUseCase
from infra.config.configuration import env
from infra.grpc.controllers.customer_grpc_controller import CustomerGrpcController
from infra.grpc.controllers.health_grpc_controller import HealthGrpcController
from infra.grpc.pb import billing_pb2_grpc, health_pb2_grpc


async def start_grpc_server(billing_use_case: BillingUseCase) -> None:
    server: grpc.aio.Server = grpc.aio.server()

    health_controller = HealthGrpcController()
    health_pb2_grpc.add_HealthServiceServicer_to_server(health_controller, server)

    customer_controller = CustomerGrpcController(billing_use_case)
    billing_pb2_grpc.add_BillingServiceServicer_to_server(customer_controller, server)

    port = int(env.GRPC_PORT)
    server.add_insecure_port(f"0.0.0.0:{port}")

    await server.start()
    print(f"gRPC server listening on port {port}", flush=True)

    await server.wait_for_termination()


__all__ = ["start_grpc_server"]
