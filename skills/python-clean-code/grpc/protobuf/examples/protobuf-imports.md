# Protobuf Import Patterns

Complete guide to importing protobuf modules in Python.

---

## Always Use _pb2 Suffix

```python
# GOOD ✅ - Clear that these are generated files
from ca_lib_protocols import constants_pb2
from myservice_protocols import user_service_pb2 as usr_pb2

status = constants_pb2.STATUS_ACTIVE
user = usr_pb2.User()

# BAD ❌ - Unclear if generated or app code
from ca_lib_protocols.constants_pb2 import STATUS_ACTIVE
from myservice_protocols import user_service_pb2 as user_service
```

## Import Both _pb2 and _pb2_grpc

```python
# For gRPC services, import BOTH
from myservice_protocols import auth_service_pb2
from myservice_protocols import auth_service_pb2_grpc

# _pb2 for messages
request = auth_service_pb2.CreateTokenRequest()

# _pb2_grpc for service stubs
auth_service_pb2_grpc.add_AuthServiceServicer_to_server(...)
```

## Aliasing Long Names

```python
# Keep _pb2 suffix in alias
from ca_user_service_protocols import user_management_service_pb2 as usr_mgmt_pb2

user = usr_mgmt_pb2.User()
```

---

*Related: See skill.md for complete patterns*
