---
name: "Rust Testing Excellence"
description: "Write proper, clear tests that validate both valid and invalid inputs with explicit assertions"
approved: Yes
created: 2026-01-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "3.1-approved"
  last_updated: "2026-01-28"
tags:
  - rust
  - testing
  - validation
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
