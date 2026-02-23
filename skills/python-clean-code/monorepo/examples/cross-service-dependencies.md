# Cross-Service Dependencies

Managing dependencies between services in monorepo.

---

## Import from ca-lib Only

```python
# GOOD ✅
from ca_lib.grpc.decorators import ca_user_service_authenticated

# BAD ❌
from ca_user_service.auth import decorators  # WRONG!
```

## Use gRPC for Cross-Service Calls

```python
# GOOD ✅
from ca_user_service_protocols import user_management_service_pb2_grpc
client = user_management_service_pb2_grpc.UserManagementServiceStub(channel)

# BAD ❌
from ca_user_service import services  # WRONG!
```

## Workspace Dependencies

```toml
[project]
dependencies = ["ca-lib"]

[tool.uv.sources]
ca-lib = { workspace = true }
```

---

*Related: See skill.md for complete patterns*
