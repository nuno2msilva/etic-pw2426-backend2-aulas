## Session 12: Developing gRPC Services in Python

**Goal:**
Learn to build and consume gRPC services for efficient inter-service communication.

**Definition:**
gRPC is a high-performance RPC framework that uses Protocol Buffers for data serialization. It facilitates fast communication between microservices. Use cases include real-time data streaming, cross-language services, and distributed systems.

**Documentation Reference:**

- https://grpc.io/docs/languages/python/quickstart/
- https://docs.python.org/3/library/concurrent.futures.html
- https://realpython.com/python-grpc/

**Setup:**
```bash
uv sync
```

**Tutorial:**
- Step-by-Step Example:
    - Define a simple .proto file.
    ```proto
    syntax = "proto3";
    package service;

    service Greeter {
        rpc SayHello (HelloRequest) returns (HelloReply) {}
    }
    message HelloRequest {
        string name = 1;
    }
    message HelloReply {
        string message = 1;
    }
    ```
    - Generate Python stubs from service.proto (grpcio-tools is included in `uv sync`):
    ```bash
    uv run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
    ```
    - Implement a server and client.
    ```py
    from concurrent import futures
    import grpc
    import service_pb2
    import service_pb2_grpc

    class Greeter(service_pb2_grpc.GreeterServicer):
        def SayHello(self, request, context):
            return service_pb2.HelloReply(message=f"Hello, {request.name}!")

    def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        service_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()

    if __name__ == "__main__":
        serve()
    ```
- Run the standalone simulation (no gRPC install needed):
```bash
uv run python main.py
```

### Exercise:

- Problem: Build a basic gRPC service that returns the cube of a number.
    - Steps to Solve:
        -  Define the .proto file, generate code, and implement the server and client.

### Challenge:

- Problem:
    - Create a gRPC service that supports server-side streaming to send multiple messages for a single request.
        - Hint: Modify the .proto definition to use a stream for the response.
