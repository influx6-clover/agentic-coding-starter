# Error Handling

gRPC exception handling patterns.

---

## Standard Exceptions

```python
from ca_lib.grpc.exceptions import (
    InvalidRequestArgumentsException,
    ResourceNotFoundException,
    PermissionDeniedException,
)

def UpdateUser(self, request, context):
    if not request.user_id:
        raise InvalidRequestArgumentsException("user_id required")

    try:
        user = User.objects.get(pk=request.user_id)
    except User.DoesNotExist:
        raise ResourceNotFoundException(f"User {request.user_id} not found")
```

---

*Related: See skill.md for complete patterns*
