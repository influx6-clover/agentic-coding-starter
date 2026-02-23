# gRPC Service Implementation - Complete Guide

Complete guide to implementing gRPC services with authentication and error handling.

---

## Basic Service Structure

```python
from grpc import ServicerContext
from ca_lib.grpc.decorators import ca_user_service_authenticated
from ca_lib.grpc.exceptions import (
    InvalidRequestArgumentsException,
    ResourceNotFoundException,
)

from myservice_protocols import user_service_pb2 as usr_pb2
from myservice_protocols import user_service_pb2_grpc as usr_pb2_grpc


class UserManagementService(usr_pb2_grpc.UserManagementServiceServicer):
    """User management gRPC service implementation."""

    @ca_user_service_authenticated
    def CreateUser(
        self,
        request: usr_pb2.CreateUserRequest,
        context: ServicerContext,
    ) -> usr_pb2.CreateUserResponse:
        """Create new user."""
        if not request.email:
            raise InvalidRequestArgumentsException("email required")

        user = User.objects.create(
            email=request.email,
            name=request.name,
        )

        return usr_pb2.CreateUserResponse(user=self._user_to_proto(user))

    def _user_to_proto(self, user) -> usr_pb2.User:
        """Convert Django model to protobuf."""
        return usr_pb2.User(
            user_id=str(user.id),
            email=user.email,
            name=user.name,
        )
```

---

## Service Registration

```python
# myservice/services.py
from myservice_protocols import user_service_pb2_grpc
from users import services as user_services

SERVICES_TO_REGISTER = [
    (
        user_service_pb2_grpc.add_UserManagementServiceServicer_to_server,
        user_services.UserManagementService,
    ),
]
```

---

*Related: See skill.md for complete patterns*
