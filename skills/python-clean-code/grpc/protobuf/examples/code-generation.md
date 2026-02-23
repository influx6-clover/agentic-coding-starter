# Code Generation

Generating protobuf code with protoc.

---

## Run After Modifying Proto Files

```bash
# Using Makefile
make protoc

# Or manually
python -m grpc_tools.protoc \
    -I=. -I../ca-messaging -I../ca-lib \
    --python_out=. \
    --grpc_python_out=. \
    --mypy_out=. \
    --mypy_grpc_out=. \
    myservice_protocols/*.proto
```

## Generated Files

- `*_pb2.py` - Message definitions
- `*_pb2_grpc.py` - Service stubs
- `*_pb2.pyi` - Type stubs

## Commit Generated Files

```bash
git add myservice_protocols/*_pb2.py
git add myservice_protocols/*_pb2_grpc.py
git add myservice_protocols/*_pb2.pyi
git commit -m "feat: regenerate protobuf code"
```

---

*Related: See skill.md for complete patterns*
