---
name: "Python Clean Implementation"
description: "Write clean, well-documented Python code with proper error handling and type safety"
approved: Yes
created: 2026-02-02
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-02"
tags:
  - python
  - clean-code
  - documentation
  - error-handling
  - type-hints
  - abstraction
files:
  - examples/documentation-patterns.md: Docstring patterns with Google/NumPy style
  - examples/error-handling-guide.md: Custom exception patterns
  - examples/security-guide.md: Security best practices for Python
  - examples/pythonic-patterns.md: Idiomatic Python code patterns
  - examples/basic-template.md: Basic implementation template
  - templates/basic-example.py: Starter template for new Python modules
---

# Python Clean Implementation

## When to Use This Skill

Read this skill when **implementing new Python code** (not tests or async). This covers:

- Writing new modules and functions
- Documenting code with Google/NumPy docstring style
- Error handling with custom exceptions
- Type hints and mypy compliance
- Security best practices
- Pythonic idioms and patterns

**Do NOT read this for:**
- Testing → See [python-testing-excellence](../python-testing-excellence/skill.md)
- Async code → See [python-with-async-code](../python-with-async-code/skill.md)

---

## Core Principles

### 0. Dependency Hierarchy: Project First, Stdlib Second, Pip Packages Last

**CRITICAL PROJECT PRINCIPLE:** Before adding external dependencies, check what the project already provides.

#### The Dependency Hierarchy

```
1. Project modules/packages (FIRST)
   ↓ Can't fulfill need?
2. Python stdlib (SECOND)
   ↓ Can't fulfill need?
3. Pip packages (LAST RESORT)
```

#### Process: Building Blocks Before Dependencies

**MANDATORY steps before adding external dependency:**

1. **Search project codebase** - Does a module already provide this?
2. **Check building blocks** - Can we compose existing project types?
3. **Try stdlib** - Does standard library provide primitives?
4. **Create project module** - Build on existing foundation if possible
5. **External dependency** - Only when truly necessary

#### Example: HTTP Test Server

**❌ BAD - Immediate external dependency:**
```toml
[dev-dependencies]
httpx = "*"  # External HTTP library
aiohttp = "*"  # External async HTTP
```

**✅ GOOD - Use project building blocks:**
```python
# Project already has:
# - http_client module with request/response handling
# - Simple HTTP parser for testing
# - Built on stdlib's http.server

# So we create: src/testing/http_server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from typing import Callable, Optional

class TestHTTPServer:
    """Test HTTP server using stdlib components.

    Built on project's existing HTTP types and stdlib's http.server.
    No external dependencies needed.
    """

    def __init__(self, handler: Optional[Callable] = None):
        """Initialize test server.

        Args:
            handler: Optional custom request handler.
        """
        self.handler = handler or self._default_handler
        self.server: Optional[HTTPServer] = None
        self.thread: Optional[threading.Thread] = None

    def start(self, port: int = 0) -> str:
        """Start server on random available port.

        Returns:
            URL of started server (e.g., "http://localhost:12345")
        """
        self.server = HTTPServer(("127.0.0.1", port), self._create_handler())
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return f"http://127.0.0.1:{self.server.server_port}"

    def stop(self):
        """Stop the server."""
        if self.server:
            self.server.shutdown()
```

#### When Project Building Blocks Exist

**If project has HTTP types:**
- ❌ Don't add `httpx`, `aiohttp`, `requests` for tests
- ✅ Create `testing/http_server.py` module using project's HTTP types

**If project has JSON utilities:**
- ❌ Don't add `ujson` for performance (unless proven bottleneck)
- ✅ Use stdlib `json` or project's JSON implementation

**If project has async primitives:**
- ❌ Don't add `trio` or `curio` just for different async style
- ✅ Use project's asyncio patterns

#### When to Create Project Modules/Packages

**Create dedicated testing package when:**
1. **Testing utilities** - Test helpers, mock servers, test fixtures
2. **Cross-module test support** - Multiple modules need same test infrastructure
3. **Significant test code** - More than just a few helper functions

**Create module in existing package when:**
1. **Small utilities** - Few helper functions specific to one package
2. **Internal abstractions** - Not used by other packages

**Example structure (BEST - Separate testing package):**
```
src/
├── myapp/               # Production code
│   ├── __init__.py
│   └── http/            # HTTP building blocks
│       ├── __init__.py
│       ├── client.py
│       └── parser.py
├── myapp_testing/       # NEW: Dedicated testing package
│   ├── __init__.py
│   └── http_server.py   # Built on myapp.http types
tests/
└── test_http_integration.py  # Uses myapp_testing.http_server
```

**Benefits of separate testing package:**
- ✅ Clean separation: production vs test code
- ✅ Reusable: Other packages can import it
- ✅ Clear dependency tree: `myapp_testing` depends on `myapp`
- ✅ No test code in production distribution
- ✅ Type-checkable test utilities

#### Benefits of Project-First Approach

**Why this matters:**
1. **Consistency** - Test code uses same types as production
2. **No duplication** - Don't reimplement what exists
3. **Smaller dependencies** - Fewer pip packages to manage
4. **Better integration** - Tests exercise real code paths
5. **Maintainability** - Changes update both prod and test code

#### Red Flags

**Warning signs you're adding unnecessary dependencies:**
- Project already has similar functionality
- Dependency only used in tests
- "Convenience" dependency for something project can do
- Adding framework when project has primitives

**Ask yourself:**
1. "Does the project already provide these building blocks?"
2. "Can I compose existing project types to achieve this?"
3. "Would creating a project module be better long-term?"
4. "Is this dependency truly necessary or just convenient?"

### 1. Documentation: Google/NumPy Docstring Style

**MANDATORY:** Every public function must document:
- **Summary** - One-line description
- **Args** - Parameter descriptions with types
- **Returns** - What the function returns
- **Raises** - What exceptions can be raised
- **Examples** - Usage examples (optional but recommended)

```python
def register_user(username: str, email: str) -> int:
    """Register a new user in the system.

    Validates user input before database insertion to prevent invalid state
    from entering persistent storage.

    Args:
        username: Unique username, must be 3+ characters per USERNAME_POLICY.
        email: User email for notifications, must be valid RFC 5322 format.

    Returns:
        User ID of the newly created user.

    Raises:
        ValidationError: If username is too short or email format is invalid.
        DatabaseError: If database connection fails.

    Examples:
        >>> user_id = register_user("alice", "alice@example.com")
        >>> print(user_id)
        123
    """
    # Implementation...
```

**Documentation Checklist for Every Public Function:**

- [ ] Summary - One-line description
- [ ] Args section - Document each parameter with type
- [ ] Returns section - What the function returns
- [ ] Raises section - What exceptions can occur
- [ ] Examples section - Code examples showing usage (optional)

**NumPy Style Alternative:**
```python
def register_user(username: str, email: str) -> int:
    """
    Register a new user in the system.

    Validates user input before database insertion to prevent invalid state
    from entering persistent storage.

    Parameters
    ----------
    username : str
        Unique username, must be 3+ characters per USERNAME_POLICY.
    email : str
        User email for notifications, must be valid RFC 5322 format.

    Returns
    -------
    int
        User ID of the newly created user.

    Raises
    ------
    ValidationError
        If username is too short or email format is invalid.
    DatabaseError
        If database connection fails.

    Examples
    --------
    >>> user_id = register_user("alice", "alice@example.com")
    >>> print(user_id)
    123
    """
    # Implementation...
```

### 2. Error Handling: Custom Exceptions

**MANDATORY:** Use custom exception classes for domain errors. Never use generic `Exception`.

```python
class AppError(Exception):
    """Base exception for application errors."""
    pass

class ConfigNotFoundError(AppError):
    """Raised when configuration file is not found."""

    def __init__(self, path: str):
        self.path = path
        super().__init__(f"Configuration not found at: {path}")

class InvalidConfigError(AppError):
    """Raised when configuration format is invalid."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Invalid configuration: {message}")

# Usage with exception chaining
def load_config(path: str) -> dict:
    """Load configuration from file.

    Args:
        path: Path to configuration file.

    Returns:
        Parsed configuration dictionary.

    Raises:
        ConfigNotFoundError: If file doesn't exist.
        InvalidConfigError: If file format is invalid.
    """
    try:
        with open(path) as f:
            content = f.read()
    except FileNotFoundError as e:
        raise ConfigNotFoundError(path) from e

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise InvalidConfigError(str(e)) from e
```

### 3. No Bare Excepts

**FORBIDDEN:** Never use bare `except:` or catch generic `Exception` without re-raising.

```python
# BAD ❌
try:
    result = risky_operation()
except:  # Catches EVERYTHING, even KeyboardInterrupt!
    result = None

# BAD ❌
try:
    result = risky_operation()
except Exception:  # Too broad
    result = None

# GOOD ✅
try:
    result = risky_operation()
except (NetworkError, TimeoutError) as e:
    logger.error(f"Operation failed: {e}")
    result = None

# GOOD ✅ - Re-raising after logging
try:
    result = risky_operation()
except Exception as e:
    logger.exception("Unexpected error")
    raise  # Re-raise to propagate
```

### 4. Avoid Unnecessary Abstraction

**CRITICAL PRINCIPLE:** Only create abstraction layers when they solve real problems. Unnecessary abstraction adds complexity, reduces maintainability, and obscures intent.

#### When Abstraction ADDS Value

✅ **Reusable patterns** - Multiple call sites benefit from shared code
✅ **Complex logic** - Encapsulation aids understanding and testing
✅ **Required by framework** - API demands specific interfaces
✅ **Cross-cutting concerns** - Logging, error handling, retry logic

#### When Abstraction REMOVES Value

❌ **Single-use wrappers** - Only one caller, no reuse benefit
❌ **Pass-through layers** - Just forwarding to another function
❌ **Premature generalization** - "Might need it someday"
❌ **Framework over-compliance** - Using complex patterns when simple solutions work

#### Example: HTTP Client Testing

**❌ BAD - Unnecessary wrapper for single use:**

```python
# DON'T create custom wrapper just to make one HTTP call!
class HTTPRequestWrapper:
    def __init__(self, url: str, method: str):
        self.url = url
        self.method = method

    def execute(self) -> dict:
        # Just wrapping urllib for one call
        req = urllib.request.Request(self.url, method=self.method)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())

# Then pass wrapper through layers...
# Way too complex for simple HTTP call!
```

**✅ GOOD - Direct call when appropriate:**

```python
# Simple, direct, clear
def fetch_user_data(user_id: int) -> dict:
    """Fetch user data from API.

    Args:
        user_id: ID of user to fetch.

    Returns:
        User data dictionary.

    Raises:
        HTTPError: On request failure.
    """
    url = f"https://api.example.com/users/{user_id}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())
```

**When wrapper IS needed:**
- ✅ Multiple HTTP calls with shared configuration
- ✅ Complex error handling, retries, authentication
- ✅ Reusable patterns used across multiple modules

#### Data Flow Principle

**If data flows A → B, pass directly:**

```python
# ✅ GOOD
data = compute_data()
consumer = Consumer(data)

# ❌ BAD - unnecessary queue
from queue import Queue
q = Queue()
q.put(compute_data())
consumer = Consumer(q.get())
```

**Use queues ONLY for:**
- ✅ Cross-thread communication
- ✅ Producer-consumer patterns with timing mismatch
- ✅ Multiple producers/consumers
- ❌ NOT for passing data between sequential function calls

#### Type Design Anti-Patterns

**❌ BAD - Over-generic types:**

```python
from typing import Generic, TypeVar

T = TypeVar('T')
U = TypeVar('U')

class DataProcessor(Generic[T, U]):
    """Why generic if we always use str and dict?"""
    def process(self, data: T) -> U:
        ...
```

**✅ GOOD - Specific where possible:**

```python
class UserDataProcessor:
    """Clear intent, known types."""
    def process(self, username: str) -> dict:
        ...
```

#### Review Checklist

Before adding abstraction, ask:

- [ ] Can I pass this data directly instead of through queues/wrappers?
- [ ] Do I really need this abstraction layer, or is it wrapping a single call?
- [ ] Am I creating a class for one use case, or will it be reused?
- [ ] Can I make this type more specific instead of generic?
- [ ] Does this code reflect the actual problem domain?

#### Decision Rule

**Ask:** "If I removed this abstraction, would the code be simpler to understand?"

- **If yes** → remove it
- **If no** → keep it, but document WHY it exists

---

## Type Hints and Mypy Compliance

### Mandatory Type Hints

**MANDATORY:** All function signatures must have type hints.

```python
from __future__ import annotations  # Enable forward references

from typing import Optional, Union, Protocol
from collections.abc import Sequence, Mapping

# GOOD ✅ - Complete type hints
def process_users(
    users: Sequence[User],
    filter_fn: Optional[Callable[[User], bool]] = None
) -> dict[str, list[User]]:
    """Process users and group by status."""
    ...

# BAD ❌ - No type hints
def process_users(users, filter_fn=None):
    """Process users and group by status."""
    ...
```

### Modern Type Hint Syntax (Python 3.10+)

```python
# Use | for Union (Python 3.10+)
def get_user(user_id: int) -> User | None:
    ...

# Use built-in generics (Python 3.9+)
def get_users() -> list[User]:
    ...

# Use dict directly (Python 3.9+)
def get_user_map() -> dict[int, User]:
    ...
```

### Protocol for Structural Typing

```python
from typing import Protocol

class Validator(Protocol):
    """Protocol for validators (structural typing)."""
    def validate(self, value: str) -> bool:
        ...

def validate_input(value: str, validator: Validator) -> bool:
    """Validate using any object with validate method."""
    return validator.validate(value)
```

---

## Pythonic Idioms

### Context Managers for Resources

**MANDATORY:** Always use context managers for resources (files, connections, locks).

```python
# GOOD ✅
with open('file.txt') as f:
    content = f.read()

# GOOD ✅ - Custom context manager
from contextlib import contextmanager

@contextmanager
def database_transaction(db):
    """Context manager for database transactions."""
    db.begin()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise

# Usage
with database_transaction(db):
    db.execute("INSERT INTO users ...")
```

### List Comprehensions and Generator Expressions

```python
# GOOD ✅ - List comprehension
doubled = [x * 2 for x in numbers]

# GOOD ✅ - Generator expression (memory efficient)
sum_doubled = sum(x * 2 for x in numbers)

# GOOD ✅ - With condition
evens = [x for x in numbers if x % 2 == 0]

# BAD ❌ - Unnecessary loop
doubled = []
for x in numbers:
    doubled.append(x * 2)
```

### Avoid Mutable Default Arguments

**CRITICAL:** Never use mutable objects as default arguments.

```python
# BAD ❌ - Mutable default argument
def add_item(item: str, items=[]):  # WRONG! Shared across calls
    items.append(item)
    return items

# GOOD ✅ - Use None and create new list
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

### Dataclasses for Data Containers

```python
from dataclasses import dataclass, field

@dataclass
class User:
    """User model with automatic __init__, __repr__, etc."""
    id: int
    name: str
    email: str
    roles: list[str] = field(default_factory=list)

    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return 'admin' in self.roles
```

### Enums for Constants

```python
from enum import Enum, auto

class UserStatus(Enum):
    """User status enumeration."""
    ACTIVE = auto()
    INACTIVE = auto()
    BANNED = auto()

# Usage
user.status = UserStatus.ACTIVE
if user.status == UserStatus.BANNED:
    raise PermissionError("User is banned")
```

---

## Security Best Practices

### Input Validation

Always validate untrusted input:

```python
import re

MAX_INPUT_LENGTH = 1024
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def process_user_input(email: str) -> str:
    """Process and validate user email.

    Args:
        email: User-provided email address.

    Returns:
        Validated email address.

    Raises:
        ValidationError: If email is invalid.
    """
    # Length check (DoS prevention)
    if len(email) > MAX_INPUT_LENGTH:
        raise ValidationError("Input too long")

    # Format validation (whitelist approach)
    if not EMAIL_PATTERN.match(email):
        raise ValidationError("Invalid email format")

    return email.strip().lower()
```

### Secrets Management

Use environment variables and `secrets` module:

```python
import os
import secrets

# GOOD ✅ - Environment variables for secrets
DATABASE_URL = os.environ["DATABASE_URL"]
API_KEY = os.environ.get("API_KEY", "")

# GOOD ✅ - Secure random tokens
def generate_token() -> str:
    """Generate a secure random token."""
    return secrets.token_urlsafe(32)

# BAD ❌ - Secrets in code
API_KEY = "sk-1234567890abcdef"  # NEVER DO THIS!
```

### SQL Injection Prevention

Always use parameterized queries:

```python
# GOOD ✅ - Parameterized query
def get_user_safe(db, user_id: int) -> User | None:
    """Fetch user by ID using safe parameterized query."""
    query = "SELECT * FROM users WHERE id = ?"
    return db.execute(query, (user_id,)).fetchone()

# BAD ❌ - String interpolation
def get_user_unsafe(db, user_id: int) -> User | None:
    """DON'T DO THIS - SQL injection vulnerable!"""
    query = f"SELECT * FROM users WHERE id = {user_id}"  # DANGEROUS!
    return db.execute(query).fetchone()
```

### Command Injection Prevention

```python
import subprocess

# GOOD ✅ - Safe command execution
def run_safe(file_path: str) -> bytes:
    """Run command safely with argument list."""
    result = subprocess.run(
        ["process", file_path],  # Argument list, not shell
        capture_output=True,
        check=True
    )
    return result.stdout

# BAD ❌ - Shell injection
def run_unsafe(cmd: str, arg: str) -> bytes:
    """DON'T DO THIS - Command injection vulnerable!"""
    result = subprocess.run(
        f"{cmd} {arg}",  # VULNERABLE!
        shell=True,
        capture_output=True
    )
    return result.stdout
```

---

## Performance Tips

### Use Generators for Large Datasets

```python
# GOOD ✅ - Generator (memory efficient)
def read_large_file(path: str):
    """Read file line by line (memory efficient)."""
    with open(path) as f:
        for line in f:
            yield line.strip()

# BAD ❌ - Loads entire file into memory
def read_large_file_bad(path: str) -> list[str]:
    """Loads entire file into memory."""
    with open(path) as f:
        return [line.strip() for line in f]
```

### Use `functools.lru_cache` for Expensive Pure Functions

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    """Cached expensive computation."""
    # Expensive operation here
    return result
```

### Use `__slots__` for Memory Efficiency

```python
class Point:
    """Memory-efficient point class."""
    __slots__ = ('x', 'y')

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
```

---

## Common Pitfalls

### Pitfall 1: Mutable Default Arguments

**Problem**: Mutable default arguments are shared across function calls.
**Solution**: Use `None` and create new mutable object inside function.

```python
# BAD ❌
def add_item(item, items=[]):  # Shared across calls!
    items.append(item)
    return items

# GOOD ✅
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

### Pitfall 2: Not Using Type Hints

**Problem**: No static type checking, harder to maintain.
**Solution**: Always add type hints to function signatures.

### Pitfall 3: Catching Too Broad Exceptions

**Problem**: `except Exception:` catches everything, hiding real errors.
**Solution**: Catch specific exception types.

```python
# BAD ❌
try:
    result = risky_operation()
except Exception:  # Too broad!
    result = None

# GOOD ✅
try:
    result = risky_operation()
except (NetworkError, TimeoutError) as e:
    logger.error(f"Operation failed: {e}")
    result = None
```

### Pitfall 4: Not Closing Resources

**Problem**: File handles, network connections left open.
**Solution**: Always use context managers.

```python
# BAD ❌
f = open('file.txt')
content = f.read()
f.close()  # Might not be called if exception occurs!

# GOOD ✅
with open('file.txt') as f:
    content = f.read()  # Automatically closed
```

### Pitfall 5: Using `import *`

**Problem**: Pollutes namespace, unclear where names come from.
**Solution**: Import specific names or use qualified imports.

```python
# BAD ❌
from module import *  # What did we import?

# GOOD ✅
from module import specific_function, SpecificClass

# GOOD ✅ - Qualified import
import module
module.specific_function()
```

---

## Learning Log

### 2026-02-02: Python Clean Implementation Skill Created

**Issue:** Creating Python equivalent of Rust clean implementation skill.

**Learning:** Adapted Rust patterns to Python idioms:
- Dependency hierarchy (project → stdlib → pip)
- Docstrings instead of doc comments
- Custom exceptions instead of derive_more
- Context managers instead of RAII
- Type hints with mypy instead of Rust's type system

**New Standard:** All Python implementation must follow these patterns.

---

## Examples

See `examples/` directory for detailed guides:

- `documentation-patterns.md` - Docstring patterns with examples
- `error-handling-guide.md` - Custom exception patterns
- `security-guide.md` - Security best practices
- `pythonic-patterns.md` - Idiomatic Python code
- `basic-template.md` - Starting template for new code

See `templates/` directory for starter code:

- `basic-example.py` - Starter template for new Python modules

## Related Skills

- [Python Testing Excellence](../python-testing-excellence/skill.md) - For writing tests
- [Python with Async Code](../python-with-async-code/skill.md) - For async/await patterns
- [Python Directory Setup](../python-directory-and-configuration/skill.md) - For project setup

---

*Last Updated: 2026-02-02*
*Version: 1.0*
