---
name: "Python Testing Excellence"
description: "Write proper, clear tests that validate both valid and invalid inputs with explicit assertions"
approved: Yes
created: 2026-02-02
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-02"
tags:
  - python
  - testing
  - validation
  - pytest
files:
  - examples/intro-to-property-based-testing.md: "Complete beginner to advanced guide on property-based testing with Hypothesis"
---

# Python Testing Excellence

## When to Use This Skill

Read this when **writing or reviewing tests** (not implementation or async code). This covers:

- Unit tests, integration tests, test organization
- Validating both valid AND invalid inputs
- pytest patterns and fixtures
- Property-based testing with Hypothesis
- Avoiding false-positive tests
- Real code over mocks

**Do NOT read this for:**
- Implementation → See [python-clean-implementation](../python-clean-implementation/skill.md)
- Async code → See [python-with-async-code](../python-with-async-code/skill.md)

---

## Core Testing Principles

### CRITICAL: Real Code Over Mocks 🚨

**The Fundamental Rule**: Tests must validate actual code behavior, not mock behavior.

#### When to Use Mocks (VERY SPARINGLY)

**✅ VALID Mock Usage - External Dependencies Only:**
1. **Third-party services** - Payment gateways, external APIs, cloud services
2. **System resources** - Hardware devices, OS calls you don't control
3. **Error injection** - Rare failure scenarios (disk full, network partition)

**❌ INVALID Mock Usage - Our Own Code:**
1. **HTTP clients** → Use real test HTTP servers (Flask, FastAPI test client)
2. **Databases** → Use test databases, SQLite in-memory, or testcontainers
3. **File I/O** → Use `tempfile` module with real filesystem
4. **DNS** → Use localhost or real DNS (with retry logic)
5. **Internal services** → If you wrote it, test the real thing

#### The Three Questions (Ask Before Every Mock)

```python
# Before writing: mock = Mock()
# Ask yourself:

1. "Is this really external (third-party/OS)?"
   ❌ My HTTP client? → NO MOCK
   ✅ Stripe payment API? → Mock OK

2. "Am I testing real logic or mock setup?"
   ❌ Testing mock returns what I configured? → INVALID
   ✅ Testing my error handling of mock failure? → VALID

3. "Are integration points tested separately?"
   ❌ Only mock tests exist? → INVALID
   ✅ Have separate real integration tests? → VALID
```

#### Real Testing Tools for Python

**Principle: Project Building Blocks → Stdlib → External Dependencies (in that order)**

**STEP 1: Check Project Building Blocks**

Before adding test dependencies, search what the project already provides:

```python
# Example: HTTP Client Testing
# Project ALREADY has:
# - http_client module with request/response handling
# - Simple HTTP parser for testing
# - Built on stdlib's http.server

# ✅ BEST - Create dedicated testing module
# File: src/myapp_testing/http_server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from typing import Callable

class TestHTTPServer:
    """Test HTTP server built on project's HTTP types.

    Uses project's existing HTTP implementation and stdlib's http.server.
    No external dependencies needed.
    """

    def __init__(self):
        """Initialize test server."""
        self.server = None
        self.thread = None

    def start(self, port: int = 0) -> str:
        """Start server on random available port.

        Returns:
            URL of started server (e.g., "http://localhost:12345")
        """
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'OK')

        self.server = HTTPServer(('127.0.0.1', port), Handler)
        actual_port = self.server.server_port
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return f"http://127.0.0.1:{actual_port}"

    def stop(self):
        """Stop the server."""
        if self.server:
            self.server.shutdown()

# Now tests use it:
# File: tests/test_http_integration.py
from myapp_testing import TestHTTPServer
from myapp import HTTPClient

def test_http_client():
    """Test HTTP client with real server."""
    server = TestHTTPServer()
    url = server.start()

    client = HTTPClient()
    response = client.get(url)

    assert response.status_code == 200
    assert response.text == 'OK'

    server.stop()
```

**Why separate testing module is better:**
- ✅ Clean separation: production vs test infrastructure
- ✅ Reusable: Multiple test files can import it
- ✅ No test code in production distribution
- ✅ Type-checkable test utilities
- ✅ Clear dependency: `myapp_testing` → `myapp`

**Test Organization Strategy:**

```python
# File: tests/test_http_internal.py
# Fast tests using our own TestHTTPServer
from myapp_testing import TestHTTPServer
from myapp import HTTPClient

def test_http_get():
    """Test GET request with internal test server."""
    server = TestHTTPServer()
    url = server.start()

    client = HTTPClient()
    response = client.get(url)

    assert response.status_code == 200
    server.stop()

def test_http_redirects():
    """Test redirect handling."""
    server = TestHTTPServer()
    url = server.start()

    client = HTTPClient()
    response = client.get(f"{url}/redirect")

    assert response.status_code == 200
    server.stop()

# File: tests/test_http_external.py
# Slower validation tests against real HTTP servers
import pytest
from myapp import HTTPClient

@pytest.mark.integration
@pytest.mark.slow
def test_external_httpbin_get():
    """Validate against real httpbin.org."""
    client = HTTPClient()
    response = client.get("http://httpbin.org/get")
    assert response.status_code == 200

@pytest.mark.integration
@pytest.mark.slow
def test_external_https():
    """Validate HTTPS handling."""
    client = HTTPClient()
    response = client.get("https://httpbin.org/get")
    assert response.status_code == 200
```

**Test Pyramid:**
1. **Many tests (90%)**: Unit tests using project's testing module - Fast, controlled
2. **Some tests (9%)**: Integration tests using project's testing module - Medium speed
3. **Few tests (1%)**: External validation with `@pytest.mark.slow` - Slow, real-world

**Run Strategy:**
```bash
# Fast tests only (no external network calls)
pytest

# Include slow integration tests
pytest -m slow

# Run specific external test
pytest tests/test_http_external.py::test_external_httpbin_get

# Run all tests (internal + external)
pytest -m "slow or not slow"
```

**STEP 2: Try Stdlib (if project doesn't have it)**

**HTTP Testing (Pure Stdlib - NO dependencies):**
```python
# ✅ BEST - Pure stdlib HTTP testing
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.request

def test_http_request():
    """Test HTTP with stdlib only."""
    # Real HTTP server (no dependencies)
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'test data')

    server = HTTPServer(('127.0.0.1', 0), Handler)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    # Test actual HTTP request
    with urllib.request.urlopen(f'http://127.0.0.1:{port}/') as response:
        data = response.read()

    assert data == b'test data'
    server.shutdown()
```

**STEP 3: External Dependencies (ONLY when necessary)**

**HTTP Testing (If project lacks HTTP types):**
```python
# ✅ ACCEPTABLE - Use minimal test dependency if project has NO HTTP
# requirements-dev.txt: pytest-httpserver

from pytest_httpserver import HTTPServer

def test_http_client(httpserver: HTTPServer):
    """Test HTTP client with lightweight test server."""
    httpserver.expect_request("/test").respond_with_data("OK")

    client = HTTPClient()
    response = client.get(httpserver.url_for("/test"))

    assert response.status_code == 200
    assert response.text == "OK"
```

**Decision Tree:**

```
Need to test HTTP?
├─ Does project have HTTP types?
│  ├─ YES → Create myapp_testing module with TestHTTPServer ✅ BEST
│  └─ NO → Continue to stdlib
├─ Can stdlib do it? (http.server + urllib)
│  ├─ YES → Use stdlib HTTP server ✅ GOOD
│  └─ NO → Use minimal external dep (pytest-httpserver) ✅ ACCEPTABLE

Need to test JSON?
├─ Does project have JSON utilities?
│  ├─ YES → Create myapp_testing with helpers ✅ BEST
│  └─ NO → Use stdlib json ✅ ACCEPTABLE

Need test utilities?
├─ Multiple modules need it?
│  ├─ YES → Create dedicated testing module (myapp_testing) ✅ BEST
│  └─ NO → Small helper in test file ✅ ACCEPTABLE
```

**When to Use Test-Only External Dependencies:**
- ✅ Protocol stdlib doesn't provide AND project doesn't have
- ✅ Complex test fixtures that would be extremely verbose to write manually
- ✅ Specialized testing tools (Hypothesis, pytest plugins)

**When NOT to Use External Test Dependencies:**
- ❌ Project already has the building blocks (compose them instead)
- ❌ HTTP requests → Use stdlib `urllib` or `http.client`
- ❌ File I/O → Use stdlib `tempfile`
- ❌ Threads → Use stdlib `threading`

**Database Testing:**
```python
# ✅ GOOD - Real database testing
import pytest
from sqlalchemy import create_engine

@pytest.fixture
def db():
    """Create in-memory SQLite database for testing."""
    engine = create_engine('sqlite:///:memory:')
    # Run migrations
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

def test_user_repository(db):
    """Test with real database."""
    repo = UserRepository(db)
    user = repo.create("alice")
    assert user.name == "alice"
```

**File I/O Testing:**
```python
# ✅ GOOD - Real file testing
import tempfile
from pathlib import Path

def test_config_loader():
    """Test with real temporary file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"
        config_path.write_text('{"key": "value"}')

        config = ConfigLoader.load(config_path)
        assert config["key"] == "value"
```

#### Red Flags: Integration Theater

⚠️ **These are WARNING SIGNS of invalid mock usage:**

```python
# ❌ BAD - Mocking our own code
from unittest.mock import Mock

def test_http_client():
    mock_dns = Mock()
    mock_tcp = Mock()
    client = HTTPClient(dns_resolver=mock_dns, tcp_conn=mock_tcp)

    # This only tests that mocks work!
    assert client.get("http://example.com") is not None

# ❌ BAD - Mock-only testing
def test_database_save():
    mock_db = Mock()
    mock_db.save.return_value = True

    # Never tests real database!
    repo = UserRepository(mock_db)
    result = repo.save(user)
    assert result is True
```

#### Required Test Coverage

**MANDATORY for all features:**
1. **Unit tests** - Individual components with real dependencies
2. **Integration tests** - Complete flows with real local services
3. **End-to-end tests** - Full workflows (may use mocks for external services only)

**Example Test Structure:**
```python
# tests/test_my_feature.py

class TestUnitLevel:
    """Unit tests with real components."""

    def test_parser(self):
        """Test individual parsing logic."""
        result = parse_input("test")
        assert result.valid

class TestIntegration:
    """Integration tests with real services."""

    def test_api_endpoint(self, test_client):
        """Test complete API flow."""
        response = test_client.get("/api/users")
        assert response.status_code == 200

class TestExternalMocks:
    """ONLY for external services."""

    def test_payment_gateway_timeout(self):
        """Valid: External service, testing specific error scenario."""
        mock = Mock(spec=PaymentGateway)
        mock.charge.side_effect = TimeoutError()

        processor = PaymentProcessor(gateway=mock)
        result = processor.charge(100)

        assert isinstance(result, PaymentError)
```

### The Three Test Validations ✅

Every meaningful test MUST validate:

1. **Input Validation** - Verify inputs are handled correctly
2. **Output Verification** - Confirm result matches expectations
3. **Error Path Testing** - Ensure error conditions produce appropriate errors

```python
# BAD ❌ - Creates variable with no assertions
def test_process():
    result = process("valid_input")  # Assumes success!

# GOOD ✅ - Validates both success and error paths
def test_process_valid_input():
    """Test processing with valid input."""
    result = process("valid_input")
    assert result is not None
    assert len(result) == 11

def test_process_invalid_input():
    """Test processing with invalid input."""
    with pytest.raises(ValueError, match="Empty input"):
        process("")
```

### Anti-Pattern: Unused Variables Without Assertions

**CRITICAL:** Tests that create variables but never validate their content are **FORBIDDEN**.

```python
# BAD ❌ - False confidence, no validation
def test_user_creation():
    user = User.create("Alice", "alice@example.com")
    # Variable created but NEVER checked!

# GOOD ✅ - Explicit validation
def test_user_creation():
    """Test creating a user with valid data."""
    user = User.create("Alice", "alice@example.com")

    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.id > 0
```

---

## Test Organization

### Test Location Conventions

**CRITICAL:** Python has specific conventions for where to place tests:

#### 1. Test Directory Structure

```
myproject/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── models.py
│       └── services.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── integration/
│       ├── __init__.py
│       └── test_api.py
└── pyproject.toml
```

#### 2. Test File Naming

```python
# File: tests/test_user_service.py
"""Tests for user service module."""

def test_create_user_success():
    """Test creating a user succeeds with valid data."""
    service = UserService()
    user = service.create_user("John", "john@example.com")
    assert user.name == "John"

def test_create_user_invalid_email():
    """Test creating a user fails with invalid email."""
    service = UserService()
    with pytest.raises(ValidationError):
        service.create_user("John", "invalid-email")
```

#### 3. Test Class Organization

```python
class TestUserService:
    """Tests for UserService class."""

    @pytest.fixture
    def service(self):
        """Create UserService instance for testing."""
        return UserService(db=MockDatabase())

    def test_create_user(self, service):
        """Test user creation."""
        user = service.create_user("John", "john@example.com")
        assert user.name == "John"

    def test_delete_user(self, service):
        """Test user deletion."""
        user = service.create_user("John", "john@example.com")
        result = service.delete_user(user.id)
        assert result is True
```

---

## Pytest Patterns

### Fixtures for Setup/Teardown

```python
import pytest

@pytest.fixture
def db_connection():
    """Create database connection for testing."""
    conn = create_connection(':memory:')
    setup_schema(conn)
    yield conn
    conn.close()

@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(id=1, name="John", email="john@example.com")

def test_user_repository(db_connection, sample_user):
    """Test user repository with fixtures."""
    repo = UserRepository(db_connection)
    saved = repo.save(sample_user)
    assert saved.id == sample_user.id
```

### Parametrize for Multiple Test Cases

```python
@pytest.mark.parametrize("email", [
    "test@example.com",
    "user.name@domain.co.uk",
    "user+tag@example.com",
])
def test_valid_emails(email):
    """Test that various valid email formats are accepted."""
    service = UserService()
    user = service.create_user("Test", email)
    assert user.email == email

@pytest.mark.parametrize("email,expected_error", [
    ("invalid-email", "Invalid email format"),
    ("@example.com", "Invalid email format"),
    ("user@", "Invalid email format"),
])
def test_invalid_emails(email, expected_error):
    """Test that invalid emails are rejected."""
    service = UserService()
    with pytest.raises(ValidationError, match=expected_error):
        service.create_user("Test", email)
```

### Markers for Test Organization

```python
@pytest.mark.slow
def test_external_api():
    """Slow test that calls external API."""
    response = call_external_api()
    assert response.status_code == 200

@pytest.mark.integration
def test_database_integration():
    """Integration test with real database."""
    db = create_test_db()
    # Test with real database

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    """Test for feature under development."""
    pass
```

---

## Property-Based Testing with Hypothesis

**Use `hypothesis` to test invariants across hundreds of generated inputs automatically.**

### Why Property-Based Testing?

Property-based testing is **highly recommended** for:
- ✅ Testing invariants (properties that should always hold)
- ✅ Finding edge cases you didn't think of
- ✅ Serialization/deserialization roundtrips
- ✅ Parsers and data transformations
- ✅ Mathematical operations (commutativity, associativity, etc.)
- ✅ State machines and protocols

### Basic Usage

```python
from hypothesis import given, strategies as st

@given(st.text(), st.integers(min_value=0, max_value=100))
def test_valid_inputs_produce_valid_outputs(name, value):
    """Test with generated inputs."""
    user = User(name=name, age=value)
    assert user.age >= 0
    assert user.age <= 100

@given(st.text(min_size=1))
def test_idempotency(input_str):
    """Hash computation should be deterministic."""
    first = compute_hash(input_str)
    second = compute_hash(input_str)
    assert first == second
```

### Common Property Testing Patterns

**Roundtrip Properties** (serialization):
```python
from hypothesis import given
from hypothesis.strategies import builds

@given(builds(User))
def test_json_roundtrip(user):
    """Test JSON serialization roundtrip."""
    json_str = user.to_json()
    decoded = User.from_json(json_str)
    assert decoded == user
```

**Invariant Properties** (never raise exception):
```python
@given(st.text())
def test_parser_never_raises(input_str):
    """Parser should never raise, regardless of input."""
    try:
        parse_input(input_str)
    except ValueError:
        pass  # Expected error type
    # No other exceptions should occur
```

**Relationship Properties** (commutativity):
```python
@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """Addition should be commutative."""
    assert add(a, b) == add(b, a)
```

### Dependencies

```toml
# pyproject.toml
[tool.poetry.group.dev.dependencies]
hypothesis = "^6.0"
```

---

## Common Pitfalls

### Pitfall 1: Testing Implementation Details

```python
# BAD ❌ - Tests internal state
def test_internal_state():
    obj = MyClass()
    obj.process("input")
    assert obj._internal_cache["key"] == "value"  # Testing private attribute!

# GOOD ✅ - Tests observable behavior
def test_observable_behavior():
    obj = MyClass()
    result = obj.process("input")
    assert "output" in result
```

### Pitfall 2: No Error Path Testing

```python
# BAD ❌ - Only tests success path
def test_valid_input():
    assert process("valid_data") is not None

# GOOD ✅ - Tests both paths
def test_valid_input():
    """Test processing with valid input."""
    result = process("valid_data")
    assert result is not None

def test_invalid_input():
    """Test processing with invalid input."""
    with pytest.raises(ValueError):
        process("")

    with pytest.raises(ValueError):
        process("x" * 10000)  # Too long
```

### Pitfall 3: Missing Fixture Setup

```python
# BAD ❌ - No proper setup
def test_database_operation():
    repo = UserRepository()
    # Missing: Database initialization!
    user = repo.get(1)
    assert user is not None

# GOOD ✅ - Proper fixture setup
@pytest.fixture
def repo():
    """Create repository with initialized database."""
    db = create_test_db()
    initialize_schema(db)
    return UserRepository(db)

def test_database_operation(repo):
    """Test database operation with initialized repo."""
    user = repo.get(1)
    assert user is not None
```

---

## Test Helper Functions

Create reusable helpers for common test setup:

```python
# tests/conftest.py (shared fixtures)
import pytest

@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(
        id=1,
        name="Alice",
        email="alice@example.com"
    )

def assert_valid_user(user: User):
    """Assert user object is valid."""
    assert user.id > 0
    assert len(user.name) > 0
    assert "@" in user.email

# tests/test_users.py
def test_create_user(sample_user):
    """Test user creation with helper."""
    assert_valid_user(sample_user)
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_user_service.py

# Run specific test
pytest tests/test_user_service.py::test_create_user

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run with markers
pytest -m "not slow"  # Skip slow tests
pytest -m "integration"  # Only integration tests

# Run with verbosity
pytest -v

# Run with output capture disabled (see print statements)
pytest -s
```

---

## Valid Test Requirements

Tests are considered valid when they:

- ✅ Pass with `pytest`
- ✅ Have explicit assertions on outputs
- ✅ Test both valid and invalid inputs
- ✅ Test error paths, not just success
- ✅ Don't test implementation details
- ✅ Are properly isolated with fixtures
- ✅ Have clear, descriptive names
- ✅ Include docstrings for complex tests
- ✅ Use real code over mocks (mocks only for external services)

---

## Learning Log

### 2026-02-02: Python Testing Excellence Skill Created

**Issue:** Creating Python equivalent of Rust testing excellence skill.

**Learning:** Adapted Rust testing patterns to Python:
- pytest fixtures instead of setup functions
- Hypothesis instead of proptest
- pytest.raises for exception testing
- @pytest.mark for test organization
- Real code over mocks (same philosophy)

**New Standard:** All Python tests must follow these patterns.

---

## Examples

See `examples/` directory for comprehensive guides:

- `intro-to-property-based-testing.md` - **Complete beginner to advanced guide** on property-based testing with Hypothesis

## Related Skills

- [Python Clean Implementation](../python-clean-implementation/skill.md) - For implementation patterns
- [Python with Async Code](../python-with-async-code/skill.md) - For async testing patterns

---

*Last Updated: 2026-02-02*
*Version: 1.0*
