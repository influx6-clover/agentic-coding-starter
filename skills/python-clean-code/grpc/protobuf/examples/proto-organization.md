# Proto Organization

Organizing proto files and packages.

---

## Directory Structure

```
myservice/
├── myservice_protocols/
│   ├── user_service.proto
│   ├── auth_service.proto
│   ├── user_service_pb2.py       (generated)
│   ├── user_service_pb2_grpc.py  (generated)
│   └── user_service_pb2.pyi      (generated)
└── Makefile
```

## File Naming

- Service definitions: `*_service.proto`
- Message definitions: `*_messages.proto`
- Generated: `*_pb2.py`, `*_pb2_grpc.py`, `*_pb2.pyi`

---

*Related: See skill.md for complete patterns*
