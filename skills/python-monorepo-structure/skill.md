---
name: "Python Monorepo Structure"
description: "Monorepo organization with workspace configuration, shared utilities, and cross-service dependencies"
approved: Yes
created: 2026-02-02
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-02"
tags:
  - python
  - monorepo
  - workspace
  - uv
  - dependencies
  - ca-lib
files:
  - examples/workspace-configuration.md: "UV workspace setup and configuration"
  - examples/ca-lib-utilities.md: "Shared ca-lib utilities reference"
  - examples/cross-service-dependencies.md: "Managing cross-service dependencies"
  - examples/monorepo-workflows.md: "Development workflows in monorepo"
---

# Python Monorepo Structure

## When to Use This Skill

Read this when:
- Setting up Python monorepo with uv workspace
- Using shared ca-lib utilities
- Managing cross-service dependencies
- Working with protocol buffer definitions across services
- Understanding monorepo structure and organization

---

## Critical Principles

### 1. Services Import from ca-lib, NOT from Each Other (MANDATORY)

**CRITICAL:** Services must NEVER import directly from other services:

```python
# GOOD ✅ - Import shared utilities from ca-lib
from ca_lib.grpc.decorators import ca_user_service_authenticated
from ca_lib.djangolib.models import base
from ca_lib import clover_datetime

# BAD ❌ - Direct import from another service
from ca_user_service.user_management import models  # WRONG!
from ca_task_service import services  # WRONG!
```

### 2. Cross-Service Communication via gRPC ONLY (MANDATORY)

**ALWAYS** use gRPC clients for cross-service calls:

```python
# GOOD ✅ - Use gRPC client
from ca_user_service_protocols import user_management_service_pb2_grpc

channel = grpc.insecure_channel('user-service:50051')
client = user_management_service_pb2_grpc.UserManagementServiceStub(channel)
response = client.GetUser(request)

# BAD ❌ - Direct Python import
from ca_user_service.user_management.services import get_user  # WRONG!
```

### 3. Virtual Workspace Root (MANDATORY)

**Root pyproject.toml is virtual** - doesn't install a package:

```toml
# Root pyproject.toml
[project]
name = "ca-workspace"
version = "0.0.0"

[tool.uv]
package = false  # Virtual root - don't install this

[tool.uv.workspace]
members = [
    "ca-lib",
    "ca-messaging",
    "ca-user-service",
    "ca-task-service",
    # ... other services
]
```

---

## Monorepo Structure

### Directory Layout

```
/workspace-root/
├── pyproject.toml          # Virtual workspace root
├── uv.lock                 # Unified dependency lock
├── ca-lib/                 # Shared utilities (foundation)
│   ├── pyproject.toml
│   └── ca_lib/
│       ├── grpc/           # gRPC utilities
│       ├── djangolib/      # Django utilities
│       ├── clover_datetime/# Datetime utilities
│       └── ca_lib_protocols/  # Shared protobufs
├── ca-messaging/           # Messaging infrastructure
│   ├── pyproject.toml
│   └── ca_messaging/
├── ca-user-service/        # User management service
│   ├── pyproject.toml
│   ├── ca_user_service/
│   └── ca_user_service_protocols/
├── ca-task-service/        # Task service
│   ├── pyproject.toml
│   ├── ca_task_service/
│   └── ca_task_service_protocols/
└── docs/                   # Shared documentation
    ├── TESTING.md
    ├── PYTHON.md
    ├── DJANGO.md
    └── GRPC.md
```

### Workspace Root Configuration

```toml
# Root pyproject.toml
[project]
name = "ca-workspace"
version = "0.0.0"
description = "CA monorepo workspace"
requires-python = ">=3.11"

[tool.uv]
package = false  # Virtual root

[tool.uv.workspace]
members = [
    # Core libraries
    "ca-lib",
    "ca-messaging",
    "ca-analytics-platform",

    # Microservices
    "ca-user-service",
    "ca-patient-data-service",
    "ca-clinical-data-service",
    "ca-task-service",
    "ca-chart-service",
]

exclude = [
    # Legacy services not yet migrated
    "ca-dev",
    "ca-pipeline-lib",
]

[tool.uv.sources]
# Workspace members reference each other
ca-lib = { workspace = true }
ca-messaging = { workspace = true }

[dependency-groups]
# Monorepo-wide dev tools
dev = [
    "ruff>=0.1",
    "pytest>=7.4",
    "mypy>=1.8",
]
```

---

## ca-lib: Shared Utilities

**ca-lib is the foundation** - all services depend on it.

### Core Utilities

#### gRPC and Authentication

```python
# Location: ca_lib.grpc/
from ca_lib.grpc.decorators import (
    ca_user_service_authenticated,
    DANGEROUS_unauthorized,
)
from ca_lib.grpc.exceptions import (
    InvalidRequestArgumentsException,
    ResourceNotFoundException,
    PermissionDeniedException,
)

# Use in service
@ca_user_service_authenticated
def CreateUser(self, request, context):
    user_id = context.auth_user_id  # Access authenticated user
    # Implementation
```

#### Django Integration

```python
# Location: ca_lib.djangolib/
from ca_lib.djangolib.models import base
from ca_lib.djangolib.fields import ProtobufEnumField

class User(base.UUIDPrimaryKeyModelBase, base.TimestampedModelBase):
    """User with ca-lib base classes."""
    name = models.CharField(max_length=255)
    status = ProtobufEnumField(
        enum_class=constants_pb2.UserStatus,
        default=constants_pb2.USER_STATUS_ACTIVE,
    )
```

#### Datetime Handling

```python
# Location: ca_lib.clover_datetime
from ca_lib import clover_datetime

# All methods return UTC timezone-aware datetimes
now = clover_datetime.CloverDatetime.now()
today = clover_datetime.CloverDatetime.today()
dt = clover_datetime.CloverDatetime.at(2022, 1, 15, 14, 30)
days_ago = clover_datetime.CloverDatetime.days_ago(7)
```

### Protocol Buffers

```python
# Location: ca_lib.ca_lib_protocols/
from ca_lib.ca_lib_protocols import constants_pb2
from ca_lib.ca_lib_protocols import roles_pb2

# Shared enums and constants
status = constants_pb2.STATUS_ACTIVE
role = roles_pb2.ROLE_ADMIN
```

### Healthcare Domain Logic

```python
# Line of Business
from ca_lib.line_of_business_utils import lob_constants
lob = lob_constants.LineOfBusiness.MA

# FHIR utilities
from ca_lib.fhir_utils import parsers

# Quality measures
from ca_lib.hedis_hero import calculators

# Care gaps
from ca_lib.gaps_in_care import identifiers
```

### Infrastructure

```python
# Redis caching
from ca_lib.redis import client, lock_manager

# Performance metrics
from ca_lib.performance import metrics, timing

# Sentry error tracking
from ca_lib.sentry import bootstrap

# Structured logging
from ca_lib.logs.formatter import StackdriverFormatter
```

### Testing Utilities

```python
# Fake data generation
from ca_lib.fake_data import factories, generators

# Synthetic healthcare data
from ca_lib.synthetic_data import patients

# Demo utilities
from ca_lib.demo_utils import seeders
```

---

## Service Configuration

### Service pyproject.toml

```toml
# ca-user-service/pyproject.toml
[project]
name = "ca-user-service"
version = "1.0.0"
description = "User management and authentication service"
requires-python = ">=3.11"

dependencies = [
    "django>=4.2",
    "grpcio>=1.60",
    "ca-lib",  # Workspace dependency
]

[tool.uv.sources]
ca-lib = { workspace = true }

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Cross-Service Protocol Dependencies

```toml
# ca-task-service depends on user service protocols
[project]
name = "ca-task-service"
dependencies = [
    "ca-lib",
    "ca-user-service-protocols",  # Reference protocols only
]

[tool.uv.sources]
ca-lib = { workspace = true }
ca-user-service-protocols = { workspace = true }
```

---

## Cross-Service Dependencies

### Dependency Graph

```
ca-lib (foundation)
├── All services depend on ca-lib
│
ca-messaging (event bus)
├── Services use for async communication
│
ca-user-service
├── Provides: Authentication, user data
├── Used by: All services needing auth
│
ca-patient-data-service
├── Provides: Patient demographics
├── Used by: Clinical services
│
ca-clinical-data-service
├── Provides: Labs, vitals, observations
├── Used by: Care quality, charts
```

### Import Patterns

```python
# GOOD ✅ - Import from ca-lib
from ca_lib.grpc.decorators import ca_user_service_authenticated
from ca_lib.djangolib.models import base
from ca_lib import clover_datetime

# GOOD ✅ - Import protocols for gRPC
from ca_user_service_protocols import user_management_service_pb2
from ca_user_service_protocols import user_management_service_pb2_grpc

# GOOD ✅ - Use gRPC client for cross-service calls
channel = grpc.insecure_channel('user-service:50051')
client = user_management_service_pb2_grpc.UserManagementServiceStub(channel)
response = client.GetUser(request)

# BAD ❌ - Direct service import
from ca_user_service.user_management import services  # WRONG!
```

---

## Protobuf Cross-References

### Proto Include Paths

```makefile
# In ca-task-service/Makefile
PROTO_INCLUDES=-I../ca-messaging -I../ca-lib -I../ca-user-service

protoc:
	python -m grpc_tools.protoc \
		-I=. $(PROTO_INCLUDES) \
		--python_out=. \
		--grpc_python_out=. \
		--mypy_out=. \
		ca_task_service_protocols/*.proto
```

### Importing Shared Protos

```protobuf
// ca-task-service/ca_task_service_protocols/task_service.proto
syntax = "proto3";

// Import from ca-lib
import "ca_lib/ca_lib_protocols/constants.proto";

// Import from ca-user-service
import "ca_user_service_protocols/user_management_service.proto";

service TaskService {
  rpc CreateTask(CreateTaskRequest) returns (CreateTaskResponse);
}
```

---

## Dependency Management

### Installing Dependencies

```bash
# From workspace root
cd /workspace-root

# Install all workspace dependencies
uv sync

# Install specific service
uv sync --package ca-user-service

# Install with all extras
uv sync --all-extras

# Install dev dependencies
uv sync --group dev
```

### Adding Dependencies

```bash
# Add to specific service
cd ca-user-service
uv add django

# Add dev dependency
uv add --dev pytest

# Add workspace dependency
uv add ca-lib --workspace
```

### Updating Dependencies

```bash
# Update all dependencies
uv lock --upgrade

# Update specific package
uv lock --upgrade-package django

# Update workspace member
cd ca-lib
# Make changes
cd ../ca-user-service
uv sync  # Gets updated ca-lib
```

---

## Development Workflows

### Working Across Services

```bash
# 1. Make changes to ca-lib
cd ca-lib
# Edit files
make protoc  # Regenerate if proto changed

# 2. Test ca-lib changes
make test

# 3. Update dependent service
cd ../ca-user-service
uv sync  # Gets updated ca-lib
make test  # Verify compatibility

# 4. Commit both changes
cd ..
git add ca-lib ca-user-service
git commit -m "feat: update ca-lib and dependent services"
```

### Adding New Shared Utility

```bash
# 1. Add to ca-lib
cd ca-lib
# Create ca_lib/new_utility/module.py

# 2. Update ca-lib tests
# Create tests/test_new_utility.py
make test

# 3. Use in service
cd ../ca-user-service
from ca_lib.new_utility import module

# 4. Document in ca-lib
# Update ca-lib/README.md
```

### Publishing Development Builds

```bash
# For cross-service feature development
cd ca-lib
make development_build
# Version: 1.2.3.dev42+abc123 (copied to clipboard)

# Use in another service
cd ../ca-task-service
# Update pyproject.toml with dev version
uv sync
```

---

## Service Categories

### Core Infrastructure

- **ca-lib** - Shared utilities (foundation for all services)
- **ca-messaging** - Pub/sub messaging infrastructure
- **ca-analytics-platform** - Metrics and analytics

### User and Authentication

- **ca-user-service** - User management, authentication, cohorts
- **clover-services-authentication** - Authentication framework

### Clinical Data

- **ca-patient-data-service** - Patient demographics
- **ca-clinical-data-service** - Clinical observations
- **ca-diagnosis-suspecting-service** - Diagnosis prediction
- **ca-care-quality-service** - Quality measures, HEDIS

### Workflow and Operations

- **ca-task-service** - Task workflow orchestration
- **ca-chart-service** - Medical chart management
- **ca-recommender-framework** - Healthcare recommendations

### Data Standards

- **clover-fhir** - FHIR protocol definitions

---

## Monorepo Commands

### Root-Level Commands

```bash
# From workspace root

# Sync all workspace dependencies
uv sync

# Lint all workspace members
ruff check .

# Format all workspace members
ruff format .

# Type check all workspace members
mypy .
```

### Per-Service Commands

**ALWAYS use service-specific Makefiles:**

```bash
cd ca-user-service

# Setup environment
make setup

# Run tests
make test

# Run service
make run

# Generate protobuf code
make protoc

# Clean generated files
make clean
```

---

## Common Pitfalls

### Pitfall 1: Direct Service Imports

```python
# BAD ❌ - Importing from another service
from ca_user_service.user_management import models

# GOOD ✅ - Use gRPC client
from ca_user_service_protocols import user_management_service_pb2_grpc
client = user_management_service_pb2_grpc.UserManagementServiceStub(channel)
```

### Pitfall 2: Not Using Virtual Root

```toml
# BAD ❌ - Root is a real package
[tool.uv]
# Missing package = false

# GOOD ✅ - Virtual root
[tool.uv]
package = false
```

### Pitfall 3: Forgetting Workspace Sources

```toml
# BAD ❌ - Missing workspace source
[project]
dependencies = ["ca-lib"]
# No [tool.uv.sources] section!

# GOOD ✅ - Declare workspace source
[project]
dependencies = ["ca-lib"]

[tool.uv.sources]
ca-lib = { workspace = true }
```

### Pitfall 4: Not Regenerating Protos

```bash
# BAD ❌ - Forget to regenerate after proto changes
# Edit .proto file
make test  # Uses old generated code!

# GOOD ✅ - Always regenerate
# Edit .proto file
make protoc  # Regenerate
make test
```

---

## Best Practices

1. **Virtual workspace root** - Don't install root package
2. **Services import from ca-lib** - Never from each other
3. **gRPC for communication** - Cross-service calls via gRPC only
4. **Workspace sources** - Declare all workspace dependencies
5. **Single uv.lock** - Unified dependency resolution
6. **Per-service Makefiles** - Standard commands per service
7. **Proto includes** - Reference shared protos correctly
8. **Development builds** - For cross-service features
9. **Test dependencies** - Verify after ca-lib changes
10. **Documentation** - Keep workspace structure documented

---

## Learning Log

### 2026-02-02: Python Monorepo Structure Skill Created

**Issue:** Need comprehensive monorepo organization patterns.

**Learning:** Created monorepo skill covering:
- Virtual workspace root with uv
- ca-lib as foundation library
- Cross-service dependency patterns (gRPC only, no direct imports)
- Protobuf cross-references
- Workspace configuration
- Development workflows
- Service categories and organization

**Adaptation:** Integrated with existing Python skills:
- gRPC patterns from python-grpc-services
- Protobuf patterns from python-grpc-protobuf
- Django patterns from python-django-models

**New Standard:** All monorepo services must follow these patterns.

---

## Examples

See `examples/` directory for detailed guides:

- `workspace-configuration.md` - UV workspace setup
- `ca-lib-utilities.md` - Shared utilities reference
- `cross-service-dependencies.md` - Managing dependencies
- `monorepo-workflows.md` - Development workflows

## Related Skills

- [Python gRPC Services](../python-grpc-services/skill.md) - For service implementation
- [Python gRPC Protobuf](../python-grpc-protobuf/skill.md) - For protobuf patterns
- [Python Django Models](../python-django-models/skill.md) - For Django patterns

---

*Created: 2026-02-02*
*Version: 1.0*
