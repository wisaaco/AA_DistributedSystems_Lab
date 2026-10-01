# Setup & Run

## add dependencies
uv add "grpcio>=1.65.5" "grpcio-tools==1.65.5" "protobuf>=5.26.1,<6"

## proto package generation
uv run python -m grpc_tools.protoc \
  -I. \
  --python_out=. \
  --grpc_python_out=. \
  calculator.proto

# Terminal 1
uv run server.py

# T2 
uv run client.py

## Note Isaac: on your server linux