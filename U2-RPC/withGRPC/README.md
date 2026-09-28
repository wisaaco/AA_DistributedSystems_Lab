# Init
uv init 
uv add grpcio grpcio-tools

# Package generation
uv run grpc_tools.protoc \
  -I. \
  --python_out=. \
  --grpc_python_out=. \
  calculator.proto

# Terminal 1
uv run server.py

# T2 
uv run client.py

## Note Isaac: on your server linux