---
name: "Python gRPC Services"
description: "gRPC service implementation patterns with authentication, error handling, and service registration"
approved: Yes
created: 2026-02-02
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-02"
tags:
  - python
  - grpc
  - services
  - authentication
  - error-handling
files:
  - examples/service-implementation.md: "Complete service implementation guide"
  - examples/authentication-patterns.md: "Authentication decorators and patterns"
  - examples/error-handling.md: "gRPC exception handling patterns"
  - examples/testing-grpc-services.md: "Testing gRPC services"
---

# Python gRPC Services

## When to Use This Skill

Read this when:
- Implementing gRPC service methods
- Adding authentication to service endpoints
- Handling errors in gRPC services
- Registering services with gRPC server
- Testing gRPC service implementations

---

## Critical Principles

### 1. Service Registration (MANDATORY)

**ALWAYS** register services in `SERVICES_TO_REGISTER` list:

```python
# myservice/services.py
from myservice_protocols import auth_service_pb2_grpc
from myservice_protocols import user_service_pb2_grpc
from auth import services as auth_services
from users import services as user_services

SERVICES_TO_REGISTER = [
    (
        auth_service_pb2_grpc.add_AuthServiceServicer_to_server,
        auth_services.AuthService,
    ),
    (
        user_service_pb2_grpc.add_UserManagementServiceServicer_to_server,
        user_services.UserManagementService,
    ),
]
```

### 2. Method Signature Pattern (MANDATORY)

**ALWAYS** use this exact signature for gRPC methods:

```python
from grpc import ServicerContext
from myservice_protocols import user_service_pb2 as usr_pb2

def CreateUser(
    self,
    request: usr_pb2.CreateUserRequest,
    context: ServicerContext,
) -> usr_pb2.CreateUserResponse:
    """Create new user.

    Args:
        request: Create user request with user data
        context: gRPC context with metadata and auth

    Returns:
        CreateUserResponse with created user

    Raises:
        InvalidRequestArgumentsException: If request data is invalid
        PermissionDeniedException: If user lacks permission
    """
    # Implementation
    return usr_pb2.CreateUserResponse()
```

### 3. Authentication Required (CRITICAL)

**ALWAYS** use authentication decorators unless explicitly public:

```python
from ca_lib.grpc.decorators import ca_user_service_authenticated

# GOOD ✅ - Authenticated endpoint
@ca_user_service_authenticated
def CreateUser(self, request, context):
    # User is authenticated, can access context.auth_user_id
    pass


# BAD ❌ - No authentication (security risk!)
def CreateUser(self, request, context):
    # Vulnerable!
    pass


# ACCEPTABLE ✅ - Explicitly unauthenticated (health checks, public APIs)
from ca_lib.grpc.decorators import DANGEROUS_unauthorized

@DANGEROUS_unauthorized
def HealthCheck(self, request, context):
    # Public endpoint
    pass
```

---

## Service Implementation

### Basic Service Class

```python
from grpc import ServicerContext
from ca_lib.grpc.decorators import ca_user_service_authenticated, DANGEROUS_unauthorized
from ca_lib.grpc.exceptions import (
    InvalidRequestArgumentsException,
    ResourceNotFoundException,
)

from myservice_protocols import user_service_pb2 as usr_pb2
from myservice_protocols import user_service_pb2_grpc as usr_pb2_grpc


class UserManagementService(usr_pb2_grpc.UserManagementServiceServicer):
    """User management gRPC service."""

    @ca_user_service_authenticated
    def CreateUser(
        self,
        request: usr_pb2.CreateUserRequest,
        context: ServicerContext,
    ) -> usr_pb2.CreateUserResponse:
        """Create new user.

        Args:
            request: User creation data
            context: gRPC context with auth_user_id

        Returns:
            CreateUserResponse with created user

        Raises:
            InvalidRequestArgumentsException: If email invalid
        """
        # Validate request
        if not request.email:
            raise InvalidRequestArgumentsException("email is required")

        # Create user
        from myapp.models import User
        user = User.objects.create(
            email=request.email,
            name=request.name,
        )

        # Build response
        return usr_pb2.CreateUserResponse(
            user=self._user_to_proto(user)
        )

    @ca_user_service_authenticated
    def GetUser(
        self,
        request: usr_pb2.GetUserRequest,
        context: ServicerContext,
    ) -> usr_pb2.GetUserResponse:
        """Get user by ID.

        Args:
            request: User ID to fetch
            context: gRPC context with auth_user_id

        Returns:
            GetUserResponse with user data

        Raises:
            InvalidRequestArgumentsException: If user_id missing
            ResourceNotFoundException: If user not found
        """
        # Validate
        if not request.user_id:
            raise InvalidRequestArgumentsException("user_id is required")

        # Fetch user
        from myapp.models import User
        try:
            user = User.objects.get(pk=request.user_id)
        except User.DoesNotExist:
            raise ResourceNotFoundException(f"User {request.user_id} not found")

        # Build response
        return usr_pb2.GetUserResponse(
            user=self._user_to_proto(user)
        )

    def _user_to_proto(self, user) -> usr_pb2.User:
        """Convert Django model to protobuf message.

        Args:
            user: Django User model instance

        Returns:
            User protobuf message
        """
        return usr_pb2.User(
            user_id=str(user.id),
            email=user.email,
            name=user.name,
            is_active=user.is_active,
        )
```

---

## Service Registration

### Registration Pattern

```python
# myservice/services.py
"""Service registration for gRPC server."""

from myservice_protocols import auth_service_pb2_grpc
from myservice_protocols import user_service_pb2_grpc
from myservice_protocols import health_check_pb2_grpc

from auth import services as auth_services
from users import services as user_services
from health import services as health_services

SERVICES_TO_REGISTER = [
    # (add_servicer_function, service_class)
    (
        auth_service_pb2_grpc.add_AuthServiceServicer_to_server,
        auth_services.AuthService,
    ),
    (
        user_service_pb2_grpc.add_UserManagementServiceServicer_to_server,
        user_services.UserManagementService,
    ),
    (
        health_check_pb2_grpc.add_HealthCheckServiceServicer_to_server,
        health_services.HealthCheckService,
    ),
]
```

### Server Startup

```python
# management/commands/run_grpc_server.py
import grpc
from concurrent import futures
from myservice.services import SERVICES_TO_REGISTER

def serve():
    """Start gRPC server with all registered services."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register all services
    for add_servicer_to_server, service_class in SERVICES_TO_REGISTER:
        add_servicer_to_server(service_class(), server)

    # Start server
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
```

---

## Authentication Decorators

### Standard Authentication

```python
from ca_lib.grpc.decorators import ca_user_service_authenticated

@ca_user_service_authenticated
def CreatePost(
    self,
    request: blog_pb2.CreatePostRequest,
    context: ServicerContext,
) -> blog_pb2.CreatePostResponse:
    """Create post (requires authentication).

    Authentication is verified by decorator.
    Access authenticated user ID via context.auth_user_id
    """
    # Get authenticated user ID
    user_id = context.auth_user_id

    # Create post for authenticated user
    post = Post.objects.create(
        author_id=user_id,
        title=request.title,
        content=request.content,
    )

    return blog_pb2.CreatePostResponse(post=post_to_proto(post))
```

### Unauthenticated Endpoints

```python
from ca_lib.grpc.decorators import DANGEROUS_unauthorized

@DANGEROUS_unauthorized
def HealthCheck(
    self,
    request: health_pb2.HealthCheckRequest,
    context: ServicerContext,
) -> health_pb2.HealthCheckResponse:
    """Health check (no authentication required).

    DANGEROUS_unauthorized prefix is intentional - forces you to think
    about whether endpoint should be public.

    Use ONLY for:
    - Health checks
    - Public APIs
    - Registration/signup endpoints
    """
    return health_pb2.HealthCheckResponse(
        status='healthy',
        version='1.0.0',
    )
```

### Permission-Based Authentication

```python
from ca_lib.grpc.decorators import ca_user_service_authenticated
from ca_lib.permissions import require_permission, Permission

@ca_user_service_authenticated
@require_permission(Permission.ADMIN)
def DeleteUser(
    self,
    request: usr_pb2.DeleteUserRequest,
    context: ServicerContext,
) -> usr_pb2.DeleteUserResponse:
    """Delete user (requires admin permission).

    Both authentication AND admin permission are checked.
    """
    user = User.objects.get(pk=request.user_id)
    user.delete()

    return usr_pb2.DeleteUserResponse(success=True)
```

---

## Error Handling

### Standard Exceptions

```python
from ca_lib.grpc.exceptions import (
    InvalidRequestArgumentsException,  # 400 - Invalid input
    UnauthenticatedException,          # 401 - Not authenticated
    PermissionDeniedException,         # 403 - Insufficient permissions
    ResourceNotFoundException,         # 404 - Not found
    InternalServerException,           # 500 - Unexpected error
)

def UpdateUser(
    self,
    request: usr_pb2.UpdateUserRequest,
    context: ServicerContext,
) -> usr_pb2.UpdateUserResponse:
    """Update user with proper error handling."""

    # Validate request
    if not request.user_id:
        raise InvalidRequestArgumentsException("user_id is required")

    if not request.email and not request.name:
        raise InvalidRequestArgumentsException(
            "At least one field (email or name) must be provided"
        )

    # Fetch user
    try:
        user = User.objects.get(pk=request.user_id)
    except User.DoesNotExist:
        raise ResourceNotFoundException(f"User {request.user_id} not found")

    # Check permissions
    if context.auth_user_id != str(user.id):
        # User can only update their own profile (unless admin)
        if not has_admin_permission(context.auth_user_id):
            raise PermissionDeniedException("Cannot update other users")

    # Update user
    if request.email:
        user.email = request.email
    if request.name:
        user.name = request.name
    user.save()

    return usr_pb2.UpdateUserResponse(user=user_to_proto(user))
```

### Exception Best Practices

```python
# GOOD ✅ - Specific exception with helpful message
if not user.is_active:
    raise InvalidRequestArgumentsException(
        f"User {user.id} is inactive and cannot perform this action"
    )

# BAD ❌ - Generic exception
if not user.is_active:
    raise Exception("User not active")


# GOOD ✅ - Catch specific exceptions
try:
    value = int(request.age)
except ValueError:
    raise InvalidRequestArgumentsException(
        f"Invalid age: '{request.age}' is not a valid integer"
    ) from None

# BAD ❌ - Catch all exceptions
try:
    value = int(request.age)
except Exception as e:  # Too broad
    raise InternalServerException(str(e))
```

---

## Model to Proto Conversion

### Conversion Helper Methods

```python
class UserManagementService(usr_pb2_grpc.UserManagementServiceServicer):
    """User service with conversion helpers."""

    def _user_to_proto(self, user) -> usr_pb2.User:
        """Convert Django User to protobuf User.

        Args:
            user: Django User model instance

        Returns:
            User protobuf message
        """
        return usr_pb2.User(
            user_id=str(user.id),
            email=user.email,
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at.isoformat(),
        )

    def _proto_to_user_data(self, proto: usr_pb2.User) -> dict:
        """Convert protobuf User to Django model data.

        Args:
            proto: User protobuf message

        Returns:
            Dict suitable for User.objects.create()
        """
        return {
            'email': proto.email,
            'name': proto.name,
            'is_active': proto.is_active,
        }
```

### Enum Conversion

```python
from myservice_protocols import constants_pb2

class UserService(usr_pb2_grpc.UserManagementServiceServicer):
    """Service with enum conversion."""

    def _status_to_proto(self, status: str) -> int:
        """Convert Django status to protobuf enum.

        Args:
            status: Django User status ('active', 'inactive', etc.)

        Returns:
            Protobuf UserStatus enum value
        """
        status_map = {
            'active': constants_pb2.USER_STATUS_ACTIVE,
            'inactive': constants_pb2.USER_STATUS_INACTIVE,
            'suspended': constants_pb2.USER_STATUS_SUSPENDED,
        }
        return status_map.get(status, constants_pb2.USER_STATUS_UNKNOWN)

    def _proto_to_status(self, proto_status: int) -> str:
        """Convert protobuf enum to Django status.

        Args:
            proto_status: Protobuf UserStatus enum value

        Returns:
            Django status string
        """
        status_map = {
            constants_pb2.USER_STATUS_ACTIVE: 'active',
            constants_pb2.USER_STATUS_INACTIVE: 'inactive',
            constants_pb2.USER_STATUS_SUSPENDED: 'suspended',
        }
        return status_map.get(proto_status, 'unknown')
```

---

## Integration with Django

### Using Django ORM

```python
@ca_user_service_authenticated
def ListUsers(
    self,
    request: usr_pb2.ListUsersRequest,
    context: ServicerContext,
) -> usr_pb2.ListUsersResponse:
    """List users with pagination.

    Uses Django ORM with query optimization.
    """
    from myapp.models import User

    # Build query
    queryset = User.objects.filter(is_active=True)

    # Pagination
    offset = request.page * request.page_size
    limit = request.page_size or 20

    users = queryset[offset:offset + limit]

    # Convert to proto
    user_protos = [self._user_to_proto(user) for user in users]

    return usr_pb2.ListUsersResponse(
        users=user_protos,
        total_count=queryset.count(),
        page=request.page,
    )
```

### Transaction Support

```python
from django.db import transaction

@ca_user_service_authenticated
def CreateUserWithProfile(
    self,
    request: usr_pb2.CreateUserWithProfileRequest,
    context: ServicerContext,
) -> usr_pb2.CreateUserWithProfileResponse:
    """Create user and profile in single transaction."""

    with transaction.atomic():
        # Create user
        user = User.objects.create(
            email=request.email,
            name=request.name,
        )

        # Create profile
        profile = Profile.objects.create(
            user=user,
            bio=request.bio,
            website=request.website,
        )

    return usr_pb2.CreateUserWithProfileResponse(
        user=self._user_to_proto(user),
        profile=self._profile_to_proto(profile),
    )
```

---

## Common Pitfalls

### Pitfall 1: Missing Authentication

```python
# BAD ❌ - No authentication decorator
def DeleteUser(self, request, context):
    # Anyone can delete users!
    pass

# GOOD ✅ - Authenticated
@ca_user_service_authenticated
def DeleteUser(self, request, context):
    pass
```

### Pitfall 2: Missing Type Hints

```python
# BAD ❌ - No type hints
def CreateUser(self, request, context):
    pass

# GOOD ✅ - Full type hints
def CreateUser(
    self,
    request: usr_pb2.CreateUserRequest,
    context: ServicerContext,
) -> usr_pb2.CreateUserResponse:
    pass
```

### Pitfall 3: Generic Exceptions

```python
# BAD ❌ - Generic exception
if not user:
    raise Exception("Not found")

# GOOD ✅ - Specific gRPC exception
if not user:
    raise ResourceNotFoundException(f"User {user_id} not found")
```

### Pitfall 4: Not Registering Service

```python
# BAD ❌ - Service not in SERVICES_TO_REGISTER
# Service won't be available!

# GOOD ✅ - Add to registration list
SERVICES_TO_REGISTER = [
    (
        user_pb2_grpc.add_UserServiceServicer_to_server,
        UserService,
    ),
]
```

---

## Best Practices

1. **Always authenticate** - Use decorators on all methods
2. **Type hints required** - Full type annotations
3. **Specific exceptions** - Use ca_lib.grpc.exceptions
4. **Register services** - Add to SERVICES_TO_REGISTER
5. **Conversion helpers** - Separate model_to_proto methods
6. **Validate input** - Check required fields
7. **Transaction support** - Use Django transactions when needed
8. **Docstrings** - Document all RPC methods
9. **Error messages** - Include helpful context
10. **Permission checks** - Verify authorization

---

## Learning Log

### 2026-02-02: Python gRPC Services Skill Created

**Issue:** Need comprehensive gRPC service implementation patterns.

**Learning:** Created gRPC services skill covering:
- Service registration pattern
- Method signature requirements
- Authentication decorators (mandatory)
- Error handling with specific exceptions
- Model to proto conversion
- Django ORM integration
- Transaction support

**Adaptation:** Integrated with existing Python skills:
- Type hints from python-clean-implementation
- Django patterns from python-django-models
- Testing patterns from python-testing-excellence

**New Standard:** All gRPC services must follow these patterns.

---

## Examples

See `examples/` directory for detailed guides:

- `service-implementation.md` - Complete service implementation guide
- `authentication-patterns.md` - Authentication decorators and patterns
- `error-handling.md` - gRPC exception handling patterns
- `testing-grpc-services.md` - Testing gRPC services

## Related Skills

- [Python gRPC Protobuf](../protobuf/skill.md) - For protobuf patterns
- [Python Django Models](../../django/models/skill.md) - For Django integration
- [Python Testing Excellence](../../testing/skill.md) - For testing patterns

---

*Created: 2026-02-02*
*Version: 1.0*
