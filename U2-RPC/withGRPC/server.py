from concurrent import futures

import grpc

import calculator_pb2
import calculator_pb2_grpc


class Calculator(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        print(f"Received: {request.a} + {request.b}")
        return calculator_pb2.AddResponse(result=request.a + request.b)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        Calculator(), server
    )

    server.add_insecure_port("127.0.0.1:50051")
    server.start()
    print("Calculator server listening on 127.0.0.1:50051")
    server.wait_for_termination()


if __name__ == "__main__":
    main()