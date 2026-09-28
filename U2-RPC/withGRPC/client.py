import grpc

import calculator_pb2
import calculator_pb2_grpc


def main():
    with grpc.insecure_channel("127.0.0.1:50051") as channel:
        calculator = calculator_pb2_grpc.CalculatorStub(channel)

        request = calculator_pb2.AddRequest(a=7, b=5)
        response = calculator.Add(request, timeout=5)

        print(f"7 + 5 = {response.result}")


if __name__ == "__main__":
    main()