---
name: "Python Testing Excellence"
description: "Write proper, clear tests that validate both valid and invalid inputs with explicit assertions"
approved: Yes
created: 2026-02-02
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.2"
  last_updated: "2026-02-02"
tags:
  - python
  - testing
  - validation
  - pytest
  - pytest-plugins
  - docker
  - testcontainers
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

## Docker/Docker-Compose for Real Infrastructure Testing 🐳

**CRITICAL PRINCIPLE**: Always prefer Docker/docker-compose/podman to spawn real infrastructure for tests.

### The Infrastructure Testing Hierarchy

```
1. Docker/docker-compose (FIRST - spawn real infrastructure locally)
   ↓ Not possible locally?
2. Test instance credentials (SECOND - use provided test environment)
   ↓ No test environment available?
3. Mock (LAST RESORT - only when infrastructure cannot run locally)
```

### When to Use Docker for Tests

**✅ USE Docker/docker-compose for**:
- PostgreSQL, MySQL, MongoDB, Redis (databases)
- RabbitMQ, Kafka (message queues)
- Elasticsearch, S3-compatible storage (MinIO)
- Any service with official Docker image

**❌ DON'T USE Docker when**:
- Service is proprietary SaaS without local version (Snowflake, Salesforce)
- Service requires special hardware/licenses
- **ACTION**: Ask dev team for test instance credentials first!

### Docker-Compose for Test Infrastructure

#### Example: PostgreSQL + Redis

```yaml
# docker-compose.test.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: testdb
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  mongodb:
    image: mongo:7
    environment:
      MONGO_INITDB_ROOT_USERNAME: test
      MONGO_INITDB_ROOT_PASSWORD: test
    ports:
      - "27017:27017"
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 5s
      timeout: 5s
      retries: 5
```

#### Running Tests with Docker-Compose

```bash
# Start infrastructure
docker-compose -f docker-compose.test.yml up -d

# Wait for health checks
docker-compose -f docker-compose.test.yml ps

# Run tests
pytest

# Cleanup
docker-compose -f docker-compose.test.yml down -v
```

#### Automated Test Script

```bash
#!/bin/bash
# scripts/run-tests.sh

set -e

echo "Starting test infrastructure..."
docker-compose -f docker-compose.test.yml up -d

echo "Waiting for services to be healthy..."
timeout 30 bash -c 'until docker-compose -f docker-compose.test.yml ps | grep -q "(healthy)"; do sleep 1; done'

echo "Running tests..."
pytest "$@"

echo "Cleaning up..."
docker-compose -f docker-compose.test.yml down -v
```

### Testcontainers (Alternative to docker-compose)

**testcontainers-python**: Programmatic Docker container management for tests

```bash
pip install testcontainers
```

#### PostgreSQL with Testcontainers

```python
from testcontainers.postgres import PostgresContainer
import psycopg2
import pytest

@pytest.fixture(scope="session")
def postgres():
    """Start PostgreSQL container for test session."""
    with PostgresContainer("postgres:15-alpine") as postgres:
        yield postgres

@pytest.fixture
def db_connection(postgres):
    """Create database connection."""
    conn = psycopg2.connect(postgres.get_connection_url())
    yield conn
    conn.close()

def test_user_repository(db_connection):
    """Test with real PostgreSQL container."""
    cursor = db_connection.cursor()
    cursor.execute("CREATE TABLE users (id serial, name varchar);")
    cursor.execute("INSERT INTO users (name) VALUES ('Alice');")

    cursor.execute("SELECT name FROM users;")
    result = cursor.fetchone()
    assert result[0] == "Alice"
```

#### MongoDB with Testcontainers

```python
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
import pytest

@pytest.fixture(scope="session")
def mongodb():
    """Start MongoDB container for test session."""
    with MongoDbContainer("mongo:7") as mongodb:
        yield mongodb

@pytest.fixture
def mongo_client(mongodb):
    """Create MongoDB client."""
    client = MongoClient(mongodb.get_connection_url())
    yield client
    client.close()

def test_user_collection(mongo_client):
    """Test with real MongoDB container."""
    db = mongo_client.test_db
    users = db.users

    users.insert_one({"name": "Alice", "age": 30})

    user = users.find_one({"name": "Alice"})
    assert user["age"] == 30
```

#### Redis with Testcontainers

```python
from testcontainers.redis import RedisContainer
import redis
import pytest

@pytest.fixture(scope="session")
def redis_container():
    """Start Redis container for test session."""
    with RedisContainer("redis:7-alpine") as redis_container:
        yield redis_container

@pytest.fixture
def redis_client(redis_container):
    """Create Redis client."""
    client = redis.from_url(redis_container.get_connection_url())
    yield client
    client.close()

def test_cache_operations(redis_client):
    """Test with real Redis container."""
    redis_client.set("key", "value")
    result = redis_client.get("key")
    assert result == b"value"
```

### Conftest.py for Shared Docker Fixtures

```python
# tests/conftest.py
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
import psycopg2
import redis

@pytest.fixture(scope="session")
def postgres_container():
    """Shared PostgreSQL container for all tests."""
    with PostgresContainer("postgres:15-alpine") as container:
        yield container

@pytest.fixture(scope="session")
def redis_container():
    """Shared Redis container for all tests."""
    with RedisContainer("redis:7-alpine") as container:
        yield container

@pytest.fixture
def db_connection(postgres_container):
    """Fresh database connection per test."""
    conn = psycopg2.connect(postgres_container.get_connection_url())
    # Run migrations
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id serial, name varchar);")
    conn.commit()

    yield conn

    # Cleanup
    cursor.execute("DROP TABLE IF EXISTS users;")
    conn.commit()
    conn.close()

@pytest.fixture
def cache_client(redis_container):
    """Fresh Redis client per test."""
    client = redis.from_url(redis_container.get_connection_url())
    yield client
    client.flushdb()  # Clear data between tests
    client.close()
```

### Decision Tree for Database Testing

```
Need to test database code?
├─ Can database run in Docker? (PostgreSQL, MySQL, MongoDB, etc.)
│  ├─ YES → Use docker-compose.test.yml or testcontainers ✅ BEST
│  └─ NO → Continue to next step
├─ Is there a test instance available? (Snowflake test account, etc.)
│  ├─ YES → Ask dev team for credentials, use test instance ✅ GOOD
│  └─ NO → Continue to next step
├─ Can we use SQLite as substitute? (For SQL databases only)
│  ├─ YES → Use in-memory SQLite for fast tests ✅ ACCEPTABLE
│  └─ NO → Continue to next step
└─ Must mock (proprietary SaaS, no local/test options)
   └─ Use pytest-mock for external database client only ⚠️ LAST RESORT
```

### Example: Complete Test Setup with Docker

```python
# pyproject.toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
testcontainers = "^3.7"
psycopg2-binary = "^2.9"
redis = "^5.0"

# tests/conftest.py
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
from myapp.database import Database
from myapp.cache import Cache

@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:15-alpine") as pg:
        yield pg

@pytest.fixture(scope="session")
def redis():
    with RedisContainer("redis:7-alpine") as r:
        yield r

@pytest.fixture
def database(postgres):
    """Database with fresh schema per test."""
    db = Database(postgres.get_connection_url())
    db.migrate()
    yield db
    db.cleanup()

@pytest.fixture
def cache(redis):
    """Cache with fresh instance per test."""
    cache = Cache(redis.get_connection_url())
    yield cache
    cache.flush()

# tests/test_user_service.py
import pytest

def test_create_user(database, cache):
    """Test user creation with real database and cache."""
    from myapp.services import UserService

    service = UserService(database, cache)
    user = service.create_user("Alice", "alice@example.com")

    # Verify in database
    assert database.get_user(user.id) is not None

    # Verify in cache
    cached_user = cache.get(f"user:{user.id}")
    assert cached_user["name"] == "Alice"

def test_user_not_found(database):
    """Test error handling with real database."""
    from myapp.services import UserService
    from myapp.exceptions import UserNotFoundError

    service = UserService(database, None)

    with pytest.raises(UserNotFoundError):
        service.get_user(99999)
```

### GitHub Actions CI Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install

      - name: Run tests
        run: poetry run pytest
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379
```

### Benefits of Docker-Based Testing

**Why this matters**:
1. **Real behavior** - Tests validate actual database/service behavior
2. **Production parity** - Same services as production
3. **Isolation** - Each test run gets fresh infrastructure
4. **CI/CD friendly** - Easy to replicate in GitHub Actions/GitLab CI
5. **No mocks** - Test actual integration, not mock configuration

### When Mocking is Acceptable

**ONLY mock when**:
- ✅ Service is proprietary SaaS without Docker image (Snowflake, Salesforce API)
- ✅ Service requires hardware/licensing unavailable in test (special GPU, enterprise license)
- ✅ Service costs money per request (payment gateways in CI - but use test mode if available)

**Before mocking, ask**:
1. "Can I run this in Docker?"
2. "Does the dev team have test instance credentials?"
3. "Is there a free tier or test mode?"
4. "Can I use a compatible open-source alternative?" (MinIO for S3, LocalStack for AWS)

---

## Essential Pytest Plugins

**MANDATORY**: Use pytest plugins instead of manual mocking. Pytest has a rich ecosystem of plugins for common testing scenarios.

### Core Pytest Plugins

#### pytest-mock (Wrapper for unittest.mock)
**Use when**: You absolutely must mock (external dependencies only)

```bash
pip install pytest-mock
```

```python
def test_external_api_with_mock(mocker):
    """Use pytest-mock instead of unittest.mock directly."""
    # pytest-mock provides 'mocker' fixture
    mock_api = mocker.Mock()
    mock_api.get_data.return_value = {"status": "ok"}

    service = ExternalService(api_client=mock_api)
    result = service.fetch_data()

    assert result["status"] == "ok"
    mock_api.get_data.assert_called_once()
```

#### pytest-asyncio (Async Testing)
**Use when**: Testing async code

```bash
pip install pytest-asyncio
```

```python
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"

# Test file
@pytest.mark.asyncio
async def test_async_function():
    """Test async code naturally."""
    result = await fetch_data()
    assert result is not None
```

#### pytest-cov (Coverage Reporting)
**Use when**: Measuring test coverage

```bash
pip install pytest-cov
```

```bash
# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = [
    "--cov=src",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=80",
]
```

### HTTP Testing Plugins

#### pytest-httpserver (Lightweight HTTP Server)
**Use when**: Testing HTTP clients with simple request/response patterns

```bash
pip install pytest-httpserver
```

```python
from pytest_httpserver import HTTPServer

def test_http_client(httpserver: HTTPServer):
    """Test HTTP client with real local server."""
    httpserver.expect_request("/api/users").respond_with_json(
        {"users": [{"id": 1, "name": "Alice"}]}
    )

    client = HTTPClient()
    response = client.get(httpserver.url_for("/api/users"))

    assert response.json()["users"][0]["name"] == "Alice"
```

#### pytest-flask (Flask Test Client)
**Use when**: Testing Flask applications

```bash
pip install pytest-flask
```

```python
import pytest
from myapp import create_app

@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = create_app({"TESTING": True})
    yield app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

def test_api_endpoint(client):
    """Test Flask API endpoint."""
    response = client.get("/api/users")
    assert response.status_code == 200
```

#### pytest-aiohttp (aiohttp Test Client)
**Use when**: Testing aiohttp applications

```bash
pip install pytest-aiohttp
```

```python
from aiohttp import web
import pytest

async def hello(request):
    return web.Response(text="Hello")

@pytest.fixture
def app():
    app = web.Application()
    app.router.add_get('/', hello)
    return app

async def test_hello(aiohttp_client, app):
    """Test aiohttp endpoint."""
    client = await aiohttp_client(app)
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello' in text
```

### Database Testing Plugins

#### pytest-postgresql (Real PostgreSQL)
**Use when**: Testing with real PostgreSQL database

```bash
pip install pytest-postgresql
```

```python
from pytest_postgresql import factories

# Create database fixture
postgresql_proc = factories.postgresql_proc(port=None)
postgresql = factories.postgresql('postgresql_proc')

def test_user_repository(postgresql):
    """Test with real PostgreSQL database."""
    cursor = postgresql.cursor()
    cursor.execute("CREATE TABLE users (id serial PRIMARY KEY, name varchar);")
    cursor.execute("INSERT INTO users (name) VALUES ('Alice');")

    cursor.execute("SELECT name FROM users;")
    result = cursor.fetchone()
    assert result[0] == "Alice"
```

#### pytest-mysql (Real MySQL)
**Use when**: Testing with real MySQL database

```bash
pip install pytest-mysql
```

```python
from pytest_mysql import factories

mysql_proc = factories.mysql_proc(port=None)
mysql = factories.mysql('mysql_proc')

def test_with_mysql(mysql):
    """Test with real MySQL database."""
    cursor = mysql.cursor()
    cursor.execute("CREATE TABLE users (id INT, name VARCHAR(50));")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice');")

    cursor.execute("SELECT name FROM users WHERE id = 1;")
    result = cursor.fetchone()
    assert result[0] == "Alice"
```

#### pytest-mongodb (Real MongoDB)
**Use when**: Testing with real MongoDB

```bash
pip install pytest-mongodb
```

```python
from pytest_mongodb import factories

mongodb_proc = factories.mongodb_proc(port=None)
mongodb = factories.mongodb('mongodb_proc')

def test_with_mongodb(mongodb):
    """Test with real MongoDB."""
    db = mongodb.test_db
    collection = db.users

    collection.insert_one({"name": "Alice", "age": 30})

    user = collection.find_one({"name": "Alice"})
    assert user["age"] == 30
```

### File and System Testing Plugins

#### pytest-tmpdir (Temporary Directories)
**Built-in**: No installation needed

```python
def test_file_operations(tmp_path):
    """Test with real temporary directory."""
    # tmp_path is a pathlib.Path object
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")

    content = test_file.read_text()
    assert content == "Hello, World!"

def test_with_tmpdir(tmpdir):
    """Alternative temporary directory fixture."""
    # tmpdir is py.path.local object (legacy)
    file_path = tmpdir.join("test.txt")
    file_path.write("Hello, World!")

    assert file_path.read() == "Hello, World!"
```

### Parametrization and Data Plugins

#### pytest-parametrize-cases (Organized Test Cases)
**Use when**: Managing many parametrized test cases

```bash
pip install pytest-parametrize-cases
```

```python
import pytest
from pytest_parametrize_cases import parametrize_cases

@parametrize_cases(
    "email, expected_valid",
    [
        ("alice@example.com", True),
        ("bob@test.co.uk", True),
        ("invalid-email", False),
        ("@example.com", False),
    ],
    ids=["valid_simple", "valid_uk", "no_at_sign", "no_local_part"]
)
def test_email_validation(email, expected_valid):
    """Test email validation with clear case names."""
    assert validate_email(email) == expected_valid
```

#### pytest-datadir (Test Data Files)
**Use when**: Tests need data files

```bash
pip install pytest-datadir
```

```python
def test_load_config(datadir):
    """Test loading config from data directory.

    Looks for test_module/test_load_config/ directory with test data.
    """
    config_file = datadir / "config.json"
    config = load_config(config_file)
    assert config["setting"] == "value"
```

### Mocking and Fixtures Plugins

#### pytest-freezegun (Time Mocking)
**Use when**: Testing time-dependent code

```bash
pip install pytest-freezegun
```

```python
from freezegun import freeze_time
import datetime

@freeze_time("2024-01-01 12:00:00")
def test_time_dependent_function():
    """Test with frozen time."""
    now = datetime.datetime.now()
    assert now.year == 2024
    assert now.month == 1
    assert now.day == 1
```

#### pytest-env (Environment Variables)
**Use when**: Testing with environment variables

```bash
pip install pytest-env
```

```toml
# pyproject.toml
[tool.pytest_env]
DATABASE_URL = "postgresql://test:test@localhost/testdb"
API_KEY = "test-key"
```

```python
import os

def test_with_env_vars():
    """Environment variables set automatically."""
    assert os.environ["DATABASE_URL"].startswith("postgresql://")
```

### Performance and Benchmarking Plugins

#### pytest-benchmark (Performance Testing)
**Use when**: Benchmarking code performance

```bash
pip install pytest-benchmark
```

```python
def test_performance(benchmark):
    """Benchmark function performance."""
    result = benchmark(expensive_function, input_data)
    assert result is not None

def test_compare_implementations(benchmark):
    """Compare two implementations."""
    benchmark.group = "sorting"
    benchmark(quicksort, large_list)
```

### Test Organization Plugins

#### pytest-xdist (Parallel Testing)
**Use when**: Running tests in parallel

```bash
pip install pytest-xdist
```

```bash
# Run tests on 4 CPUs
pytest -n 4

# Run tests with auto-detection
pytest -n auto
```

#### pytest-repeat (Repeat Tests)
**Use when**: Testing for flaky behavior

```bash
pip install pytest-repeat
```

```python
@pytest.mark.repeat(100)
def test_potentially_flaky():
    """Run test 100 times to catch race conditions."""
    result = concurrent_operation()
    assert result.is_valid()
```

### Recommended Plugin Stack

**Minimal Essential Stack**:
```bash
pip install pytest pytest-asyncio pytest-cov pytest-mock
```

**Web Application Stack**:
```bash
pip install pytest pytest-asyncio pytest-cov pytest-httpserver pytest-flask
```

**Database Application Stack**:
```bash
pip install pytest pytest-asyncio pytest-cov pytest-postgresql pytest-mongodb
```

**Complete Testing Stack**:
```bash
pip install \
    pytest pytest-asyncio pytest-cov pytest-mock \
    pytest-httpserver pytest-flask pytest-aiohttp \
    pytest-postgresql pytest-mysql pytest-mongodb \
    pytest-xdist pytest-benchmark pytest-freezegun \
    pytest-env pytest-datadir
```

**pyproject.toml Configuration**:
```toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
pytest-asyncio = "^0.23"
pytest-cov = "^4.1"
pytest-mock = "^3.12"
pytest-httpserver = "^1.0"
pytest-xdist = "^3.5"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
]
asyncio_mode = "auto"
```

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
1. **HTTP clients** → Use pytest plugins: `pytest-httpserver`, `pytest-flask`, `pytest-aiohttp`
2. **Databases** → Use pytest plugins: `pytest-postgresql`, `pytest-mysql`, `pytest-mongodb`
3. **File I/O** → Use pytest fixture with `tempfile` module
4. **DNS** → Use localhost or real DNS (with retry logic)
5. **Internal services** → If you wrote it, test the real thing

**Prefer pytest plugins over unittest.mock**:
- Use `pytest-mock` (pytest wrapper) instead of `unittest.mock` directly
- Use specialized pytest plugins for common scenarios
- Mocks should be last resort, not first choice

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
def test_http_client(mocker):
    """DON'T DO THIS - mocking our own internal components!"""
    mock_dns = mocker.Mock()
    mock_tcp = mocker.Mock()
    client = HTTPClient(dns_resolver=mock_dns, tcp_conn=mock_tcp)

    # This only tests that mocks work!
    assert client.get("http://example.com") is not None

# ❌ BAD - Mock-only testing
def test_database_save(mocker):
    """DON'T DO THIS - never tests real database!"""
    mock_db = mocker.Mock()
    mock_db.save.return_value = True

    # Never tests real database!
    repo = UserRepository(mock_db)
    result = repo.save(user)
    assert result is True

# ✅ GOOD - Use pytest plugins for real testing
def test_http_client_real(httpserver):
    """Test with real HTTP server using pytest-httpserver."""
    httpserver.expect_request("/test").respond_with_data("OK")

    client = HTTPClient()
    response = client.get(httpserver.url_for("/test"))

    assert response.status_code == 200
    assert response.text == "OK"

def test_database_save_real(postgresql):
    """Test with real PostgreSQL using pytest-postgresql."""
    cursor = postgresql.cursor()
    cursor.execute("CREATE TABLE users (id serial, name varchar);")

    repo = UserRepository(postgresql)
    user = repo.save(User(name="Alice"))

    cursor.execute("SELECT name FROM users WHERE id = %s;", (user.id,))
    assert cursor.fetchone()[0] == "Alice"
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

    def test_payment_gateway_timeout(self, mocker):
        """Valid: External service, testing specific error scenario.

        Use pytest-mock (mocker fixture) instead of unittest.mock directly.
        """
        # Mock external payment gateway (not our code!)
        mock_gateway = mocker.Mock(spec=PaymentGateway)
        mock_gateway.charge.side_effect = TimeoutError()

        processor = PaymentProcessor(gateway=mock_gateway)
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

### 2026-02-02: Docker/Docker-Compose for Real Infrastructure

**Issue:** Need to emphasize Docker/docker-compose for spawning real infrastructure over mocking.

**Learning:** Added comprehensive "Docker/Docker-Compose for Real Infrastructure Testing" section:

**The Infrastructure Testing Hierarchy:**
1. **Docker/docker-compose** (FIRST) - Spawn real infrastructure locally
2. **Test instance credentials** (SECOND) - Use provided test environments
3. **Mock** (LAST RESORT) - Only when infrastructure cannot run locally

**Complete coverage of:**
- docker-compose.test.yml examples (PostgreSQL, Redis, MongoDB)
- testcontainers-python for programmatic container management
- Automated test scripts with Docker cleanup
- conftest.py patterns for shared Docker fixtures
- GitHub Actions CI integration with service containers
- Decision tree for database testing

**Examples added:**
- PostgreSQL with testcontainers
- MongoDB with testcontainers
- Redis with testcontainers
- Multi-service test setups
- Complete test infrastructure patterns

**When mocking is acceptable:**
- Proprietary SaaS without Docker (Snowflake, Salesforce)
- Services requiring special hardware/licenses
- **Always ask**: "Can I run this in Docker? Do we have test instance credentials?"

**New Standard:** Prefer Docker/docker-compose for all infrastructure testing. Only mock when truly impossible to run locally.

### 2026-02-02: Pytest Plugins Emphasis

**Issue:** Need to emphasize pytest plugins over manual mocking and unittest.mock.

**Learning:** Updated skill to strongly prefer pytest plugins:
- Added comprehensive "Essential Pytest Plugins" section
- **pytest-mock**: Use instead of unittest.mock directly
- **pytest-httpserver**: For HTTP client testing (no mocks!)
- **pytest-postgresql/mysql/mongodb**: Real database testing
- **pytest-flask/aiohttp**: Framework-specific test clients
- **pytest-xdist**: Parallel test execution
- **pytest-benchmark**: Performance testing
- **pytest-freezegun**: Time-dependent testing

Organized plugins by category:
1. Core plugins (pytest-mock, pytest-asyncio, pytest-cov)
2. HTTP testing (pytest-httpserver, pytest-flask, pytest-aiohttp)
3. Database testing (pytest-postgresql, pytest-mysql, pytest-mongodb)
4. File/system testing (tmp_path, tmpdir built-in fixtures)
5. Performance (pytest-benchmark, pytest-xdist)

Updated all mock examples to use pytest-mock's `mocker` fixture instead of unittest.mock.

**New Standard:** Always check pytest plugin ecosystem before writing manual mocks or test infrastructure.

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

*Last Updated: 2026-02-02 - Added Docker/docker-compose emphasis*
*Version: 1.2*
