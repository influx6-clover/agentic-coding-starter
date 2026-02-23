---
name: "Python gRPC Protobuf"
description: "Protocol buffer patterns with imports, code generation, and protobuf organization"
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
  - protobuf
  - code-generation
files:
  - examples/protobuf-imports.md: "Protobuf import patterns and naming"
  - examples/code-generation.md: "Generating protobuf code with protoc"
  - examples/proto-organization.md: "Organizing proto files and packages"
---

# Python gRPC Protobuf

## When to Use This Skill

Read this when:
- Importing protobuf modules in Python
- Generating protobuf code from .proto files
- Organizing proto files and packages
- Working with generated protobuf code

---

## Critical Principles

### 1. Always Import with _pb2 Suffix (MANDATORY)

**CRITICAL:** Always import protobuf modules with `_pb2` suffix to distinguish generated code:

```python
# GOOD ✅ - Clear that these are generated protobuf files
from ca_lib_protocols import constants_pb2
from ca_user_service_protocols import user_management_service_pb2 as usr_mgmt_pb2

# Usage
status = constants_pb2.STATUS_ACTIVE
user_type = usr_mgmt_pb2.USER_STATUS_ACTIVE

# BAD ❌ - Unclear if generated or application code
from ca_lib_protocols.constants_pb2 import STATUS_ACTIVE
```

### 2. Keep _pb2 Suffix in Aliases (MANDATORY)

**When aliasing long names, ALWAYS keep the `_pb2` suffix:**

```python
# GOOD ✅ - Alias keeps _pb2 suffix
from ca_user_service_protocols import user_management_service_pb2 as usr_mgmt_pb2

user = usr_mgmt_pb2.User()

# BAD ❌ - Lost _pb2 suffix (looks like app code)
from ca_user_service_protocols import user_management_service_pb2 as usr_mgmt

user = usr_mgmt.User()  # Is this generated or app code?
```

### 3. Import Both _pb2 and _pb2_grpc (MANDATORY)

**For gRPC services, import BOTH message definitions and service stubs:**

```python
# Message definitions (_pb2)
from ca_user_service_protocols import auth_service_pb2

# Service stubs (_pb2_grpc)
from ca_user_service_protocols import auth_service_pb2_grpc

# _pb2 contains message definitions
request = auth_service_pb2.CreateTokenRequest()

# _pb2_grpc contains service stubs for registration
auth_service_pb2_grpc.add_AuthServiceServicer_to_server(...)
```

---

## Protobuf Import Patterns

### Module Import Pattern

```python
# Import full module with _pb2 suffix
from myservice_protocols import user_service_pb2
from myservice_protocols import constants_pb2
from myservice_protocols import common_pb2

# Use with module prefix
user = user_service_pb2.User()
status = constants_pb2.STATUS_ACTIVE
error = common_pb2.Error(message='Failed')
```

### Aliased Import Pattern

```python
# For long names, alias but keep _pb2 suffix
from ca_user_service_protocols import user_management_service_pb2 as usr_mgmt_pb2
from ca_user_service_protocols import authentication_service_pb2 as auth_pb2

# Usage
user = usr_mgmt_pb2.User()
token = auth_pb2.Token()
```

### Service Import Pattern

```python
# Import BOTH message definitions and service stubs
from myservice_protocols import health_check_service_pb2 as hc_pb2
from myservice_protocols import health_check_service_pb2_grpc as hc_pb2_grpc

# _pb2 for messages
request = hc_pb2.HealthCheckRequest()
response = hc_pb2.HealthCheckResponse(healthy=True)

# _pb2_grpc for service registration
class HealthCheckService(hc_pb2_grpc.HealthCheckServiceServicer):
    pass

# Register service
hc_pb2_grpc.add_HealthCheckServiceServicer_to_server(service, server)
```

---

## Code Generation Workflow

### Generating Protobuf Code

**ALWAYS run after modifying `.proto` files:**

```bash
# From service directory
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

**Generated files:**
- `*_pb2.py` - Message definitions and serialization
- `*_pb2_grpc.py` - Service stubs and client/server interfaces
- `*_pb2.pyi` - Type stubs for mypy

### Makefile Pattern

```makefile
# Makefile
.PHONY: protoc clean

protoc:
	uv run python -m grpc_tools.protoc \
		-I=. -I../ca-messaging -I../ca-lib \
		--python_out=. \
		--grpc_python_out=. \
		--mypy_out=relax_strict_optional_primitives:. \
		--mypy_grpc_out=. \
		myservice_protocols/*.proto

clean:
	find . -name '*_pb2.py' -delete
	find . -name '*_pb2_grpc.py' -delete
	find . -name '*_pb2.pyi' -delete
```

### Protoc Flags Explained

```bash
python -m grpc_tools.protoc \
    -I=.                    # Include current directory
    -I../ca-messaging       # Include shared messaging protos
    -I../ca-lib             # Include shared library protos
    --python_out=.          # Generate Python message code
    --grpc_python_out=.     # Generate gRPC service code
    --mypy_out=...          # Generate mypy type stubs
    --mypy_grpc_out=.       # Generate mypy stubs for gRPC
    myservice_protocols/*.proto  # Proto files to compile
```

---

## Generated Files Policy

### Commit Generated Files (MANDATORY)

**Generated files ARE committed to version control** in monorepo:

```bash
# After running make protoc, commit generated files
git add myservice_protocols/*_pb2.py
git add myservice_protocols/*_pb2_grpc.py
git add myservice_protocols/*_pb2.pyi
git commit -m "feat: regenerate protobuf code after service changes"
```

**Why commit generated files?**
- Ensures all developers use identical generated code
- CI/CD doesn't need protoc installation
- Easier to review proto changes via diffs
- Version control for generated code

### Clean Generated Files

```bash
# Before regenerating
make clean

# Or manually
find . -name '*_pb2.py' -delete
find . -name '*_pb2_grpc.py' -delete
find . -name '*_pb2.pyi' -delete
```

---

## Proto File Organization

### Directory Structure

```
myservice/
├── myservice_protocols/
│   ├── __init__.py
│   ├── user_service.proto
│   ├── auth_service.proto
│   ├── common.proto
│   ├── user_service_pb2.py       (generated)
│   ├── user_service_pb2_grpc.py  (generated)
│   └── user_service_pb2.pyi      (generated)
├── myservice/
│   ├── users/
│   │   └── services.py           (implements gRPC services)
│   └── auth/
│       └── services.py
└── Makefile
```

### Proto File Naming

```
# Service definitions
*_service.proto

# Message definitions
*_messages.proto
*_common.proto

# Generated files
*_pb2.py          # Message definitions
*_pb2_grpc.py     # Service stubs
*_pb2.pyi         # Type stubs
```

---

## Working with Protobuf Messages

### Creating Messages

```python
from myservice_protocols import user_service_pb2 as usr_pb2

# Create message
user = usr_pb2.User(
    user_id='123',
    email='alice@example.com',
    name='Alice',
    is_active=True,
)

# Set fields after creation
user.created_at = '2024-01-15T10:00:00Z'

# Nested messages
address = usr_pb2.Address(
    street='123 Main St',
    city='New York',
    zip_code='10001',
)
user.address.CopyFrom(address)
```

### Reading Messages

```python
# Access fields
print(user.user_id)      # '123'
print(user.email)        # 'alice@example.com'
print(user.is_active)    # True

# Check if field is set
if user.HasField('address'):
    print(user.address.city)

# Repeated fields
for phone in user.phone_numbers:
    print(phone)
```

### Enums

```python
from myservice_protocols import constants_pb2

# Use enum values
status = constants_pb2.USER_STATUS_ACTIVE

# Check enum value
if user.status == constants_pb2.USER_STATUS_ACTIVE:
    print('User is active')

# Enum name
print(constants_pb2.UserStatus.Name(user.status))  # 'USER_STATUS_ACTIVE'
```

---

## Integration with Django

### ProtobufEnumField

```python
# Django model with protobuf enum
from django.db import models
from ca_lib.djangolib.fields import ProtobufEnumField
from myservice_protocols import constants_pb2

class User(models.Model):
    """User with protobuf enum status."""

    name = models.CharField(max_length=255)
    status = ProtobufEnumField(
        enum_class=constants_pb2.UserStatus,
        default=constants_pb2.USER_STATUS_ACTIVE,
    )

# Usage
user = User.objects.create(
    name='Alice',
    status=constants_pb2.USER_STATUS_ACTIVE,
)

# Query with enum
active_users = User.objects.filter(status=constants_pb2.USER_STATUS_ACTIVE)
```

---

## Common Pitfalls

### Pitfall 1: Missing _pb2 Suffix

```python
# BAD ❌ - Lost _pb2 suffix
from myservice_protocols import user_service_pb2 as user_service

# Unclear if generated or app code
user = user_service.User()

# GOOD ✅ - Keep _pb2 suffix
from myservice_protocols import user_service_pb2 as usr_pb2

user = usr_pb2.User()
```

### Pitfall 2: Not Importing _pb2_grpc

```python
# BAD ❌ - Missing service stub import
from myservice_protocols import user_service_pb2

# Error: user_service_pb2 doesn't have add_*_to_server
user_service_pb2.add_UserServiceServicer_to_server(...)

# GOOD ✅ - Import both
from myservice_protocols import user_service_pb2
from myservice_protocols import user_service_pb2_grpc

user_service_pb2_grpc.add_UserServiceServicer_to_server(...)
```

### Pitfall 3: Not Committing Generated Files

```bash
# BAD ❌ - Forgetting to commit generated files
make protoc
git add myservice_protocols/*.proto
git commit -m "Update proto"
# Generated files not committed!

# GOOD ✅ - Commit generated files
make protoc
git add myservice_protocols/*_pb2.py
git add myservice_protocols/*_pb2_grpc.py
git add myservice_protocols/*_pb2.pyi
git commit -m "feat: update proto and regenerate code"
```

### Pitfall 4: Not Cleaning Before Regenerating

```bash
# BAD ❌ - Old generated files remain
make protoc  # May have stale files

# GOOD ✅ - Clean first
make clean
make protoc
```

---

## Best Practices

1. **Always _pb2 suffix** - Never drop _pb2 from imports or aliases
2. **Import both _pb2 and _pb2_grpc** - For service implementations
3. **Commit generated files** - Ensure consistent code across team
4. **Clean before regenerate** - Avoid stale generated code
5. **Type hints** - Use generated .pyi stubs for mypy
6. **Module imports** - Import modules, not individual classes
7. **Makefile** - Standardize protoc commands
8. **Version control** - Track proto changes with generated code
9. **Documentation** - Comment proto files thoroughly
10. **Shared protos** - Reuse common message definitions

---

## Learning Log

### 2026-02-02: Python gRPC Protobuf Skill Created

**Issue:** Need comprehensive protobuf import and generation patterns.

**Learning:** Created gRPC protobuf skill covering:
- _pb2 suffix import pattern (mandatory)
- Import both _pb2 and _pb2_grpc for services
- Code generation workflow with protoc
- Generated files committed to version control
- Proto file organization
- Integration with Django (ProtobufEnumField)

**Adaptation:** Integrated with existing Python skills:
- Type hints from python-clean-implementation
- Django patterns from python-django-models

**New Standard:** All protobuf imports must follow these patterns.

---

## Examples

See `examples/` directory for detailed guides:

- `protobuf-imports.md` - Protobuf import patterns and naming
- `code-generation.md` - Generating protobuf code with protoc
- `proto-organization.md` - Organizing proto files and packages

## Related Skills

- [Python gRPC Services](../services/skill.md) - For service implementation
- [Python Django Models](../python-django-models/skill.md) - For ProtobufEnumField

---

*Created: 2026-02-02*
*Version: 1.0*
