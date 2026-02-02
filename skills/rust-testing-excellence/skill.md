---
name: "Rust Testing Excellence"
description: "Write proper, clear tests that validate both valid and invalid inputs with explicit assertions"
approved: Yes
created: 2026-01-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "3.2-approved"
  last_updated: "2026-02-02"
tags:
  - rust
  - testing
  - validation
  - docker
  - testcontainers
files:
  - examples/intro-to-property-based-testing.md: "Complete beginner to advanced guide on property-based testing with proptest"
---

# Rust Testing Excellence

## When to Use This Skill

Read this when **writing or reviewing tests** (not implementation or async code). This covers:

- Unit tests, integration tests, benchmarks
- Validating both valid AND invalid inputs
- Feature-gated test modules
- Property-based testing
- Avoiding false-positive tests

**Do NOT read this for:**
- Implementation → See [rust-clean-implementation](../rust-clean-implementation/skill.md)
- Async code → See [rust-with-async-code](../rust-with-async-code/skill.md)

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
1. **HTTP clients** → Use real test HTTP servers (axum, hyper, wiremock)
2. **Databases** → Use testcontainers, in-memory SQLite, or test databases
3. **File I/O** → Use `tempfile` crate with real filesystem
4. **DNS** → Use localhost or real DNS (with retry logic)
5. **Internal services** → If you wrote it, test the real thing

#### The Three Questions (Ask Before Every Mock)

```rust
// Before writing: let mock = Mock...::new()
// Ask yourself:

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

#### Real Testing Tools for Rust

**Principle: Project Building Blocks → Stdlib → External Dependencies (in that order)**

**STEP 1: Check Project Building Blocks**

Before adding test dependencies, search what the project already provides:

```rust
// Example: HTTP Client Testing (02-build-http-client spec)
// Project ALREADY has:
// - wire::simple_http::HttpRequestReader
// - wire::simple_http::SimpleOutgoingResponse
// - wire::simple_http::RenderHttp trait + Http11
// - wire::simple_http::SimpleIncomingRequest

// ✅ BEST - Create dedicated testing crate
// File: backends/foundation_testing/Cargo.toml
// [dependencies]
// foundation_core = { path = "../foundation_core" }

// File: backends/foundation_testing/src/http_server.rs
use foundation_core::wire::simple_http::{
    HttpRequestReader, SimpleOutgoingResponse, Http11,
    SimpleIncomingRequest, RenderHttp
};
use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};
use std::thread;

/// Test HTTP server built on project's simple_http types.
///
/// WHY: Provides real HTTP server for testing without external dependencies.
/// Uses foundation_core's existing HTTP implementation.
pub struct TestHttpServer {
    listener: TcpListener,
    addr: String,
    handle: Option<thread::JoinHandle<()>>,
}

impl TestHttpServer {
    /// Start a new test HTTP server on random port.
    pub fn start() -> Self {
        let listener = TcpListener::bind("127.0.0.1:0").unwrap();
        let addr = format!("http://{}", listener.local_addr().unwrap());

        let listener_clone = listener.try_clone().unwrap();
        let handle = thread::spawn(move || {
            for stream in listener_clone.incoming() {
                if let Ok(mut stream) = stream {
                    // Use project's HttpRequestReader
                    let reader = HttpRequestReader::new(stream.try_clone().unwrap());
                    let _request = reader.read().unwrap();

                    // Use project's SimpleOutgoingResponse + Http11
                    let response = SimpleOutgoingResponse::new()
                        .status(200)
                        .body(b"OK");
                    let rendered = Http11.render(&response).unwrap();
                    stream.write_all(&rendered).unwrap();
                }
            }
        });

        Self {
            listener,
            addr,
            handle: Some(handle)
        }
    }

    /// Get URL for path on this test server.
    pub fn url(&self, path: &str) -> String {
        format!("{}{}", self.addr, path)
    }
}

// File: backends/foundation_testing/src/lib.rs
pub mod http_server;
pub use http_server::TestHttpServer;

// Now tests use it:
// File: backends/foundation_core/tests/http_integration.rs
use foundation_testing::TestHttpServer;

#[test]
fn test_http_client() {
    let server = TestHttpServer::start();
    let client = HttpClient::new();
    let response = client.get(&server.url("/")).unwrap();
    assert_eq!(response.status(), 200);
}
```

**Why separate testing crate is better:**
- ✅ Clean separation: production vs test infrastructure
- ✅ Parallel compilation: builds alongside main crates
- ✅ Reusable: Multiple crates can depend on `foundation_testing`
- ✅ No test code in production binaries
- ✅ Clear dependency: `foundation_testing` → `foundation_core`

**Integration tests go in `./tests` directory:**
```
backends/foundation_core/
├── src/                        # Production code
├── tests/                      # Integration tests (separate crate)
│   ├── http_internal.rs        # Tests using foundation_testing
│   └── http_external.rs        # Tests against real servers
└── Cargo.toml

# Integration tests are a separate crate that depends on foundation_core
# This prevents cyclical dependencies and keeps organization clean
```

**Test Organization Strategy:**

```rust
// File: backends/foundation_core/tests/http_internal.rs
// Fast tests using our own TestHttpServer
use foundation_testing::TestHttpServer;
use foundation_core::wire::simple_http::client::HttpClient;

#[test]
fn test_http_get() {
    let server = TestHttpServer::start();
    let client = HttpClient::new();
    let response = client.get(&server.url("/")).unwrap();
    assert_eq!(response.status(), 200);
}

#[test]
fn test_http_redirects() {
    let server = TestHttpServer::with_redirect();
    let client = HttpClient::new();
    let response = client.get(&server.url("/redirect")).unwrap();
    assert_eq!(response.status(), 200);
}

// File: backends/foundation_core/tests/http_external.rs
// Slower validation tests against real HTTP servers
use foundation_core::wire::simple_http::client::HttpClient;

#[test]
#[ignore] // Ignored by default (requires network)
fn test_external_httpbin_get() {
    let client = HttpClient::new();
    let response = client.get("http://httpbin.org/get").unwrap();
    assert_eq!(response.status(), 200);
}

#[test]
#[ignore] // Requires network
fn test_external_httpbin_redirects() {
    let client = HttpClient::new();
    let response = client.get("http://httpbin.org/redirect/1").unwrap();
    assert_eq!(response.status(), 200); // After following redirect
}

#[test]
#[ignore]
fn test_external_https() {
    let client = HttpClient::new();
    let response = client.get("https://httpbin.org/get").unwrap();
    assert_eq!(response.status(), 200);
}

#[test]
#[ignore]
fn test_external_error_codes() {
    let client = HttpClient::new();
    let response = client.get("http://httpbin.org/status/404").unwrap();
    assert_eq!(response.status(), 404);
}

#[test]
#[ignore]
fn test_external_headers() {
    let client = HttpClient::new();
    let response = client.get("http://httpbin.org/headers").unwrap();
    assert_eq!(response.status(), 200);
    // Verify headers were sent/received correctly
}
```

**Test Pyramid:**
1. **Many tests (90%)**: Unit tests in `src/` using foundation_testing - Fast, controlled
2. **Some tests (9%)**: Integration tests in `./tests` using foundation_testing - Medium speed
3. **Few tests (1%)**: External validation in `./tests` with `#[ignore]` - Slow, real-world

**Run Strategy:**
```bash
# Fast tests only (no external network calls)
cargo test

# Include external validation tests
cargo test -- --ignored

# Run specific external test
cargo test test_external_httpbin_get -- --ignored

# Run all tests (internal + external)
cargo test -- --include-ignored
```

**Benefits of `./tests` directory for integration tests:**
- ✅ **No cyclical dependencies** - Integration tests are separate crate
- ✅ **Clean organization** - Clear separation of unit vs integration tests
- ✅ **Realistic testing** - Tests use public API like real consumers
- ✅ **Multiple sources** - Can test against foundation_testing AND external servers
- ✅ **Conditional compilation** - Easy to exclude expensive tests from CI

**STEP 2: Try Stdlib (if project doesn't have it)**

**TCP Testing (Pure Stdlib - NO dependencies):**
```rust
// ✅ BEST - Pure stdlib TCP testing
use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};
use std::thread;

#[test]
fn test_tcp_connection() {
    // Real TCP server (no dependencies)
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let addr = listener.local_addr().unwrap();

    // Spawn server thread
    thread::spawn(move || {
        let (mut stream, _) = listener.accept().unwrap();
        let mut buf = [0u8; 1024];
        let n = stream.read(&mut buf).unwrap();
        // Echo back
        stream.write_all(&buf[..n]).unwrap();
    });

    // Test actual TCP connection
    let mut client = TcpStream::connect(addr).unwrap();
    client.write_all(b"test data").unwrap();

    let mut buf = [0u8; 1024];
    let n = client.read(&mut buf).unwrap();
    assert_eq!(&buf[..n], b"test data");
}
```

**STEP 3: External Dependencies (ONLY when necessary)**

**HTTP Testing (If project lacks HTTP types):**
```rust
// ✅ ACCEPTABLE - Use minimal test dependency if project has NO HTTP
// Cargo.toml: [dev-dependencies] tiny_http = "0.12"

#[test]
fn test_http_client() {
    use tiny_http::{Server, Response};
    use std::thread;

    // Real HTTP server (test-only dependency)
    let server = Server::http("127.0.0.1:0").unwrap();
    let addr = format!("http://{}", server.server_addr());

    thread::spawn(move || {
        let request = server.recv().unwrap();
        request.respond(Response::from_string("OK")).unwrap();
    });

    // Test our real HTTP client
    let client = HttpClient::new();
    let response = client.get(&addr).unwrap();
    assert_eq!(response.status(), 200);
}
```

**Decision Tree:**

```
Need to test HTTP?
├─ Does project have HTTP types? (wire::simple_http)
│  ├─ YES → Create foundation_testing crate with TestHttpServer ✅ BEST
│  └─ NO → Continue to stdlib
├─ Can stdlib do it? (std::net::TcpListener + raw bytes)
│  ├─ YES → Use stdlib with raw HTTP bytes ✅ GOOD
│  └─ NO → Use minimal external dep (tiny_http) ✅ ACCEPTABLE

Need to test JSON?
├─ Does project have JSON types?
│  ├─ YES → Create foundation_testing with helpers ✅ BEST
│  └─ NO → Use serde_json ✅ ACCEPTABLE

Need test utilities?
├─ Multiple crates need it?
│  ├─ YES → Create dedicated testing crate (e.g., foundation_testing) ✅ BEST
│  └─ NO → Small helper module in single crate ✅ ACCEPTABLE
```

**When to Use Test-Only External Dependencies:**
- ✅ Protocol stdlib doesn't provide (HTTP, WebSocket) AND project doesn't have
- ✅ Complex test fixtures that would be extremely verbose to write manually
- ✅ Specialized testing tools (proptest, criterion)

**When NOT to Use External Test Dependencies:**
- ❌ Project already has the building blocks (compose them instead)
- ❌ TCP/UDP → Use `std::net` (stdlib)
- ❌ File I/O → Use `std::fs` + `tempfile` (stdlib)
- ❌ Threads/channels → Use `std::thread`, `std::sync::mpsc` (stdlib)

**Database Testing:**
```rust
// ✅ GOOD - Real database testing
use sqlx::SqlitePool;

#[tokio::test]
async fn test_user_repository() {
    // Real in-memory SQLite database
    let pool = SqlitePool::connect(":memory:").await.unwrap();
    sqlx::migrate!().run(&pool).await.unwrap();

    let repo = UserRepository::new(pool);
    let user = repo.create("alice").await.unwrap();

    assert_eq!(user.name, "alice");
}
```

**File I/O Testing:**
```rust
// ✅ GOOD - Real file testing
use tempfile::TempDir;
use std::fs;

#[test]
fn test_config_loader() {
    // Real temporary directory
    let dir = TempDir::new().unwrap();
    let config_path = dir.path().join("config.json");

    // Real file write
    fs::write(&config_path, r#"{"key": "value"}"#).unwrap();

    // Real file read
    let config = ConfigLoader::load(&config_path).unwrap();
    assert_eq!(config.key, "value");
}
```

**DNS Testing:**
```rust
// ✅ GOOD - Real DNS with localhost
#[test]
fn test_dns_resolver() {
    let resolver = SystemDnsResolver::new();

    // localhost always resolves - valid real test
    let addrs = resolver.resolve("localhost", 80).unwrap();
    assert!(!addrs.is_empty());
}
```

#### Red Flags: Integration Theater

⚠️ **These are WARNING SIGNS of invalid mock usage:**

```rust
// ❌ BAD - Mocking our own code
#[test]
fn test_http_client() {
    let mock_dns = MockDnsResolver::new();
    let mock_tcp = MockTcpConnection::new();
    let client = HttpClient::new(mock_dns, mock_tcp);

    // This only tests that mocks work!
    assert!(client.get("http://example.com").is_ok());
}

// ❌ BAD - Mock-only testing
#[test]
fn test_database_save() {
    let mock_db = MockDatabase::new();
    mock_db.expect_save().return_ok();

    // Never tests real database!
    repo.save(mock_db).unwrap();
}
```

#### Required Test Coverage

**MANDATORY for all features:**
1. **Unit tests** - Individual components with real dependencies
2. **Integration tests** - Complete flows with real local services
3. **End-to-end tests** - Full workflows (may use mocks for external services only)

**Example Test Structure:**
```rust
// tests/my_feature_test.rs
mod unit {
    // Test individual functions with real components
    #[test]
    fn test_parser() { /* real parsing logic */ }
}

mod integration {
    // Test complete flows with real services
    #[tokio::test]
    async fn test_api_endpoint() {
        let server = start_test_server(); // Real HTTP
        let response = real_client.get(server.url()).await.unwrap();
        // ...
    }
}

mod external_mocks {
    // ONLY for external services
    #[test]
    fn test_payment_gateway_timeout() {
        let mock = MockStripeAPI::timeout(); // Valid: external
        // ...
    }
}
```

### The Three Test Validations ✅

Every meaningful test MUST validate:

1. **Input Validation** - Verify inputs are handled correctly
2. **Output Verification** - Confirm result matches expectations
3. **Error Path Testing** - Ensure error conditions produce appropriate errors

```rust
// BAD ❌ - Creates variable with no assertions
#[test]
fn test_process() {
    let result = process("valid_input").unwrap(); // Assumes success!
}

// GOOD ✅ - Validates both success and error paths
#[test]
fn test_process_valid_input() {
    let result = process("valid_input");
    assert!(result.is_ok(), "valid input should succeed");
    assert_eq!(result.unwrap().len(), 11);
}

#[test]
fn test_process_invalid_input() {
    let result = process("");
    assert_eq!(result, Err(Error::EmptyInput));
}
```

### Anti-Pattern: Muted Variables Without Assertions

**CRITICAL:** Tests that create variables but never validate their content are **FORBIDDEN**.

```rust
// BAD ❌ - False confidence, no validation
#[test]
fn test_user_creation() {
    let user = User::new("Alice", "alice@example.com");
    // Variable created but NEVER checked!
}

// GOOD ✅ - Explicit validation
#[test]
fn test_user_creation() {
    let user = User::new("Alice", "alice@example.com")
        .expect("should create user");

    assert_eq!(user.name, "Alice");
    assert_eq!(user.email(), "alice@example.com");
    assert!(user.id() > 0);
}
```

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
```

#### Running Tests with Docker-Compose

```bash
# Start infrastructure
docker-compose -f docker-compose.test.yml up -d

# Wait for health checks
docker-compose -f docker-compose.test.yml ps

# Run tests
cargo test

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
cargo test "$@"

echo "Cleaning up..."
docker-compose -f docker-compose.test.yml down -v
```

### Testcontainers-rs (Programmatic Docker Management)

**testcontainers**: Rust library for managing Docker containers in tests

```toml
# Cargo.toml
[dev-dependencies]
testcontainers = "0.15"
postgres = "0.19"  # Or your database client
```

#### PostgreSQL with Testcontainers

```rust
#[cfg(test)]
mod tests {
    use testcontainers::{clients, images};
    use postgres::{Client, NoTls};

    #[test]
    fn test_user_repository() {
        // Start PostgreSQL container
        let docker = clients::Cli::default();
        let postgres = docker.run(images::postgres::Postgres::default());

        // Get connection details
        let host_port = postgres.get_host_port_ipv4(5432);
        let connection_string = format!(
            "postgresql://postgres:postgres@127.0.0.1:{}/postgres",
            host_port
        );

        // Connect to real PostgreSQL
        let mut client = Client::connect(&connection_string, NoTls).unwrap();

        // Run actual database operations
        client.execute(
            "CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR NOT NULL)",
            &[],
        ).unwrap();

        client.execute(
            "INSERT INTO users (name) VALUES ($1)",
            &[&"Alice"],
        ).unwrap();

        let rows = client.query("SELECT name FROM users", &[]).unwrap();
        assert_eq!(rows[0].get::<_, String>(0), "Alice");

        // Container automatically cleaned up when dropped
    }
}
```

#### Redis with Testcontainers

```rust
#[cfg(test)]
mod tests {
    use testcontainers::{clients, images};
    use redis::Commands;

    #[test]
    fn test_cache_operations() {
        let docker = clients::Cli::default();
        let redis = docker.run(images::redis::Redis::default());

        let host_port = redis.get_host_port_ipv4(6379);
        let connection_string = format!("redis://127.0.0.1:{}", host_port);

        let client = redis::Client::open(connection_string).unwrap();
        let mut con = client.get_connection().unwrap();

        // Test actual Redis operations
        con.set::<_, _, ()>("key", "value").unwrap();
        let result: String = con.get("key").unwrap();

        assert_eq!(result, "value");
    }
}
```

#### MongoDB with Testcontainers

```rust
#[cfg(test)]
mod tests {
    use testcontainers::{clients, images};
    use mongodb::{Client, options::ClientOptions};

    #[tokio::test]
    async fn test_user_collection() {
        let docker = clients::Cli::default();
        let mongo = docker.run(images::mongo::Mongo::default());

        let host_port = mongo.get_host_port_ipv4(27017);
        let connection_string = format!("mongodb://127.0.0.1:{}", host_port);

        // Connect to real MongoDB
        let client_options = ClientOptions::parse(&connection_string).await.unwrap();
        let client = Client::with_options(client_options).unwrap();

        let db = client.database("test_db");
        let collection = db.collection("users");

        // Test actual MongoDB operations
        collection.insert_one(
            doc! { "name": "Alice", "age": 30 },
            None,
        ).await.unwrap();

        let user = collection.find_one(
            doc! { "name": "Alice" },
            None,
        ).await.unwrap().unwrap();

        assert_eq!(user.get_str("name").unwrap(), "Alice");
    }
}
```

### Shared Test Fixtures with once_cell

```rust
use once_cell::sync::Lazy;
use testcontainers::{clients, images, Container};
use std::sync::Mutex;

// Shared PostgreSQL container for all tests
static POSTGRES: Lazy<Mutex<Container<'static, images::postgres::Postgres>>> = Lazy::new(|| {
    let docker = Box::leak(Box::new(clients::Cli::default()));
    let container = docker.run(images::postgres::Postgres::default());
    Mutex::new(container)
});

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_user_creation() {
        let postgres = POSTGRES.lock().unwrap();
        let host_port = postgres.get_host_port_ipv4(5432);
        // Use shared container
    }

    #[test]
    fn test_user_deletion() {
        let postgres = POSTGRES.lock().unwrap();
        let host_port = postgres.get_host_port_ipv4(5432);
        // Use same shared container
    }
}
```

### Decision Tree for Database Testing

```
Need to test database code?
├─ Can database run in Docker? (PostgreSQL, MySQL, MongoDB, etc.)
│  ├─ YES → Use docker-compose or testcontainers-rs ✅ BEST
│  └─ NO → Continue to next step
├─ Is there a test instance available? (Snowflake test account, etc.)
│  ├─ YES → Ask dev team for credentials, use test instance ✅ GOOD
│  └─ NO → Continue to next step
├─ Can we use SQLite as substitute? (For SQL databases only)
│  ├─ YES → Use SQLite :memory: for fast tests ✅ ACCEPTABLE
│  └─ NO → Continue to next step
└─ Must mock (proprietary SaaS, no local/test options)
   └─ Use trait mock for external database client only ⚠️ LAST RESORT
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
      - uses: actions-rs/toolchain@v1
        with:
          toolchain: stable

      - name: Run tests
        run: cargo test
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

## Test Organization

### Test Location Conventions

**CRITICAL:** Rust has specific conventions for where to place tests:

#### 1. Unit Tests - Inside Source Files

```rust
// src/lib.rs or src/module.rs
pub fn public_function() -> Result<()> {
    private_helper()
}

fn private_helper() -> Result<()> {
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_private_helper() {
        // Unit tests can access private functions
        assert!(private_helper().is_ok());
    }

    #[test]
    fn test_public_function() {
        assert!(public_function().is_ok());
    }
}
```

#### 2. Integration Tests - At Project Root

```
project_root/
├── Cargo.toml
├── src/
│   └── lib.rs
└── tests/                      # Integration tests at project root
    ├── crate_name/             # Organize by crate name
    │   ├── api_tests.rs
    │   ├── authentication.rs
    │   └── error_handling.rs
    └── common/                 # Shared test utilities
        └── mod.rs
```

```rust
// tests/crate_name/api_tests.rs
use my_crate::prelude::*; // Only public API

#[test]
fn test_full_workflow() {
    let service = Service::new();
    let result = service.process("input");
    assert!(result.is_ok());
}
```

#### 3. Benchmarks - At Project Root

```
project_root/
├── Cargo.toml
└── benches/                    # Benchmarks at project root
    └── crate_name/             # Organize by crate name
        ├── parsing.rs
        └── serialization.rs
```

```toml
# Cargo.toml
[[bench]]
name = "crate_name_parsing"
harness = false
path = "benches/crate_name/parsing.rs"

[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }
```

---

## Feature-Gated Tests

### Use Module-Level Gates, Not Individual Attributes

**MANDATORY:** Group feature-specific tests into modules with `#[cfg(...)]` at module level.

```rust
// BAD ❌ - Individual test attributes scattered
#[cfg(test)]
mod tests {
    #[test]
    #[cfg(not(feature = "std"))]
    fn test_spinlock_basic() { }

    #[test]
    #[cfg(not(feature = "std"))]
    fn test_spinlock_contention() { }

    #[test]
    #[cfg(feature = "std")]
    fn test_std_mutex() { }
}

// GOOD ✅ - Feature-gated test modules
#[cfg(test)]
mod tests {
    use super::*;

    // Common tests for all configurations
    #[test]
    fn test_basic_functionality() {
        // Works with both std and no_std
    }

    // No-std specific tests grouped together
    #[cfg(not(feature = "std"))]
    mod nostd_tests {
        use super::*;

        #[test]
        fn test_spinlock_basic() {
            // SpinLock only available in no_std
        }

        #[test]
        fn test_spinlock_contention() { }
    }

    // Std-specific tests grouped together
    #[cfg(feature = "std")]
    mod std_tests {
        use super::*;

        #[test]
        fn test_std_mutex_threading() {
            // Test with real OS threads
        }
    }
}
```

**Benefits:**
- ✅ Clear organization - see which tests run in which configuration
- ✅ Single location for feature changes
- ✅ Better test output and maintainability
- ✅ Feature-specific imports scoped to relevant module

---

## Async Test Isolation

**MANDATORY:** See [Async Test Isolation](../rust-with-async-code/skill.md#3-async-test-isolation---mandatory) in rust-with-async-code for complete patterns.

**Quick reference:** Always use `flavor = "current_thread"` for async tests to prevent test isolation issues with global state.

---

## Property-Based Testing (Recommended)

**Use `proptest` to test invariants across hundreds of generated inputs automatically.**

### Why Property-Based Testing?

Property-based testing is **highly recommended** for:
- ✅ Testing invariants (properties that should always hold)
- ✅ Finding edge cases you didn't think of
- ✅ Serialization/deserialization roundtrips
- ✅ Parsers and data transformations
- ✅ Mathematical operations (commutativity, associativity, etc.)
- ✅ State machines and protocols

### Basic Usage

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_valid_inputs_produce_valid_outputs(
        name in "[a-zA-Z]+",
        value in 0i32..100,
    ) {
        let user = User::new(&name);
        prop_assert!(user.is_ok());

        let result = process_value(user.unwrap(), value);
        prop_assert!(result.is_ok());
        prop_assert!(result.unwrap() >= 0);
    }

    #[test]
    fn test_idempotency(input in "[a-zA-Z]+") {
        let first = compute_hash(&input);
        let second = compute_hash(&input);
        prop_assert_eq!(first, second,
            "Hash computation should be deterministic");
    }
}
```

### Common Property Testing Patterns

**Roundtrip Properties** (serialization):
```rust
proptest! {
    #[test]
    fn test_json_roundtrip(user in any::<User>()) {
        let json = serde_json::to_string(&user)?;
        let decoded: User = serde_json::from_str(&json)?;
        prop_assert_eq!(user, decoded);
    }
}
```

**Invariant Properties** (never panic):
```rust
proptest! {
    #[test]
    fn test_parser_never_panics(input in ".*") {
        // Should never panic, regardless of input
        let _ = parse_input(&input);
    }
}
```

**Relationship Properties** (commutativity):
```rust
proptest! {
    #[test]
    fn test_addition_commutative(a in 0i32..1000, b in 0i32..1000) {
        prop_assert_eq!(add(a, b), add(b, a));
    }
}
```

### When to Use Property-Based Testing

| Use Case | Example Property |
|----------|------------------|
| Serialization | `deserialize(serialize(x)) == x` |
| Parsing | `parse` never panics on any input |
| Encoding | `decode(encode(x)) == x` |
| Sorting | Output is sorted and contains same elements |
| Hashing | `hash(x) == hash(x)` (deterministic) |
| Reversible operations | `reverse(reverse(x)) == x` |

### Dependencies

Add to `Cargo.toml`:
```toml
[dev-dependencies]
proptest = "1.4"
```

---

## Common Pitfalls

### Pitfall 1: Testing Implementation Details

```rust
// BAD ❌ - Tests internal state
let internal_state = obj.get_internal_map();
assert_eq!(*internal_state.last_key(), "expected");

// GOOD ✅ - Tests observable behavior
obj.process("input");
assert!(obj.result().contains("output"));
```

### Pitfall 2: No Error Path Testing

```rust
// BAD ❌ - Only tests success path
#[test]
fn test_valid_input() {
    assert!(process(valid_data).is_ok());
}

// GOOD ✅ - Tests both paths
#[test]
fn test_valid_input() {
    assert!(process(valid_data).is_ok());
}

#[test]
fn test_invalid_input() {
    assert_eq!(process(""), Err(Error::EmptyInput));
    assert_eq!(process(too_long), Err(Error::InputTooLong));
}
```

### Pitfall 3: Missing Initialization in Tests

```rust
// BAD ❌ - Pool never initialized
#[test]
fn test_threaded_operation() {
    let mut executor = ThreadPool::new(4);
    // MISSING: No initialization call!
    assert!(executor.is_ready());
}

// GOOD ✅ - Properly initializes and validates
#[test]
fn test_threaded_operation() {
    let mut thread_pool = ExecutorPool::with_capacity(4);

    // MANDATORY: Initialize before testing
    assert!(thread_pool.initialize().is_ok(),
        "Pool must initialize successfully");

    // Now validate actual behavior
    assert!(thread_pool.is_ready());
}
```

---

## Test Helper Functions

Create reusable helpers for common test setup:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    fn create_test_user(name: &str) -> User {
        User::new(name, format!("{}@test.com", name))
            .expect("should create test user")
    }

    fn assert_valid_result(result: &Result<Data>) {
        assert!(result.is_ok(), "result should be Ok");
        let data = result.as_ref().unwrap();
        assert!(!data.is_empty(), "data should not be empty");
    }

    #[test]
    fn test_multiple_users() {
        let alice = create_test_user("alice");
        let bob = create_test_user("bob");

        assert_ne!(alice.id(), bob.id());
    }
}
```

---

## Running Tests

```bash
# Run all tests (unit + integration + doc tests)
cargo test

# Run only unit tests
cargo test --lib

# Run only integration tests
cargo test --test '*'

# Run specific integration test file
cargo test --test api_tests

# Run only doc tests
cargo test --doc

# Run with specific feature flags
cargo test --features "std"
cargo test --no-default-features

# Run benchmarks
cargo bench
cargo bench --bench crate_name_parsing
```

---

## Valid Test Requirements

Tests are considered valid when they:

- ✅ Compile with `cargo test`
- ✅ Have explicit assertions on outputs
- ✅ Test both valid and invalid inputs
- ✅ Test error paths, not just success
- ✅ Don't test implementation details
- ✅ Are properly isolated (use `current_thread` for async)
- ✅ Have clear, descriptive names
- ✅ Include documentation comments for complex tests

---

## Learning Log

### 2026-02-02: Docker/Docker-Compose for Real Infrastructure

**Issue:** Need to emphasize Docker/docker-compose for spawning real infrastructure over mocking.

**Learning:** Added comprehensive "Docker/Docker-Compose for Real Infrastructure Testing" section:

**The Infrastructure Testing Hierarchy:**
1. **Docker/docker-compose** (FIRST) - Spawn real infrastructure locally
2. **Test instance credentials** (SECOND) - Use provided test environments
3. **Mock** (LAST RESORT) - Only when infrastructure cannot run locally

**Complete coverage of:**
- docker-compose.test.yml examples (PostgreSQL, Redis)
- testcontainers-rs for programmatic container management
- Automated test scripts with Docker cleanup
- Shared test fixtures with once_cell
- GitHub Actions CI integration with service containers
- Decision tree for database testing

**Examples added:**
- PostgreSQL with testcontainers-rs
- Redis with testcontainers-rs
- MongoDB with testcontainers-rs (async)
- Shared container fixtures
- Complete test infrastructure patterns

**When mocking is acceptable:**
- Proprietary SaaS without Docker (Snowflake, Salesforce)
- Services requiring special hardware/licenses
- **Always ask**: "Can I run this in Docker? Do we have test instance credentials?"

**New Standard:** Prefer Docker/docker-compose for all infrastructure testing. Only mock when truly impossible to run locally.

### 2026-01-28: Skill Restructuring

**Issue:** Original skill.md was 1059 lines with extensive duplication.

**Learning:** Consolidated feature-gating patterns, removed duplicated test organization examples, streamlined into focused sections.

**New Standard:** Test skill reduced to ~450 lines focusing on core patterns and anti-patterns.

### 2026-01-27: False Positive Test Prevention

**Issue:** Tests creating variables without validation were passing CI but catching no bugs.

**Learning:** Every test must have at least one explicit assertion validating behavior.

**Standard:** All tests must validate actual outputs, not just execute code paths.

---

## Examples

See `examples/` directory for comprehensive guides:

- `intro-to-property-based-testing.md` - **Complete beginner to advanced guide** on property-based testing with proptest, including exercises and real-world examples

## Related Skills

- [Rust Clean Implementation](../rust-clean-implementation/skill.md) - For implementation patterns
- [Rust with Async Code](../rust-with-async-code/skill.md) - For async testing patterns

---

*Last Updated: 2026-01-28*
*Version: 3.1-approved*
