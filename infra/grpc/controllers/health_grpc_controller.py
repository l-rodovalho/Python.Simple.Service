import grpc

from infra.grpc.pb import health_pb2, health_pb2_grpc


class HealthGrpcController(health_pb2_grpc.HealthServiceServicer):
    async def Check(
        self,
        request: health_pb2.HealthRequest,
        context: grpc.aio.ServicerContext,
    ) -> health_pb2.HealthResponse:
        return health_pb2.HealthResponse(message="OK")


__all__ = ["HealthGrpcController"]
