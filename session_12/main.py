import threading
from concurrent import futures

import grpc
import service_pb2
import service_pb2_grpc

# ---------------------------------------------------------------------------
# Tutorial: CubeService — unary RPC
# ---------------------------------------------------------------------------

class CubeServicer(service_pb2_grpc.CubeServiceServicer):
    # Problem: returns the cube of the requested number
    def GetCube(self, request, context):
        return service_pb2.NumberReply(result=request.value ** 3)


# ---------------------------------------------------------------------------
# Challenge: StreamService — server-side streaming RPC
# ---------------------------------------------------------------------------

class StreamServicer(service_pb2_grpc.StreamServiceServicer):
    def CountUp(self, request, context):
        for i in range(request.value):
            yield service_pb2.NumberReply(result=i)


def serve(port: int = 50051) -> grpc.Server:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_CubeServiceServicer_to_server(CubeServicer(), server)
    service_pb2_grpc.add_StreamServiceServicer_to_server(StreamServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    return server


def run_client(port: int = 50051) -> None:
    with grpc.insecure_channel(f"localhost:{port}") as channel:
        # Problem: cube client
        cube_stub = service_pb2_grpc.CubeServiceStub(channel)
        reply = cube_stub.GetCube(service_pb2.NumberRequest(value=4))
        print(f"  GetCube(4)  = {reply.result}")

        # Challenge: streaming client
        stream_stub = service_pb2_grpc.StreamServiceStub(channel)
        results = [r.result for r in stream_stub.CountUp(service_pb2.NumberRequest(value=5))]
        print(f"  CountUp(5)  = {results}")


def main():
    port = 50051
    print(f"Starting gRPC server on :{port} ...")
    server = serve(port)

    print("Running client demo:")
    run_client(port)

    server.stop(0)
    print("\nTo keep the server running: call serve() and server.wait_for_termination()")


if __name__ == "__main__":
    main()
