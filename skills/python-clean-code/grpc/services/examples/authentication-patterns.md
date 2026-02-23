# Authentication Patterns

Authentication decorator patterns for gRPC services.

---

## Standard Authentication

```python
from ca_lib.grpc.decorators import ca_user_service_authenticated

@ca_user_service_authenticated
def CreatePost(self, request, context):
    user_id = context.auth_user_id
    # Implementation
```

## Unauthenticated Endpoints

```python
from ca_lib.grpc.decorators import DANGEROUS_unauthorized

@DANGEROUS_unauthorized
def HealthCheck(self, request, context):
    # Public endpoint
    pass
```

---

*Related: See skill.md for complete patterns*
