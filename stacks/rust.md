# Rust Coding Standards

## Overview
- **Language**: Rust 1.75+ (stable channel, use latest stable)
- **Edition**: 2021 (latest edition with all modern features)
- **Use Cases**: Systems programming, high-performance backend services, CLI tools, embedded systems, WebAssembly, performance-critical code
- **Official Docs**: https://doc.rust-lang.org/
- **The Rust Book**: https://doc.rust-lang.org/book/

## Visibility Policy

**Project Convention**: ALL types are public by default.

- ✅ Use `pub` for all structs, enums, functions, traits, fields
- ❌ DO NOT use `pub(crate)` - everything is public
- ❌ DO NOT use `pub(super)` - everything is public
- ✅ Module-level organization for API structure
- ✅ Use `#[doc(hidden)]` if truly internal (rare)

**Rationale**:
- Simpler mental model (no visibility complexity)
- Better API discoverability
- Enables easier testing and extension
- Follows principle: "build libraries, not frameworks"
- Documentation (not visibility) indicates "internal" vs "public API"

**Example**:
```rust
// ✅ Good - all public
pub struct MyStruct {
    pub field: String,
}

pub fn helper_function() {
    // Implementation
}

// ❌ Bad - don't use pub(crate)
pub(crate) struct Internal {}  // NO! Use pub instead

// ❌ Bad - don't use pub(super)
pub(super) fn internal_fn() {}  // NO! Use pub instead
```

**Module Organization**:
- Privacy achieved through clear documentation, not visibility modifiers
- Public internal modules are acceptable
- Use clear module naming to indicate intent:
  - `internal::` prefix for truly internal modules (still public)
  - Document modules as "Internal" or "Public API"
- Consumers guided by documentation, not forced by compiler

## Skill References (MANDATORY)

**ALL Rust skills MUST be consulted based on task type. Load skills selectively to optimize context.**

### Project Setup & Configuration ⚙️

**Read BEFORE setting up new Rust projects or configuring toolchain:**

- [`rust-clean-code/directory-and-configuration`](../skills/rust-clean-code/directory-and-configuration/skill.md)
  - Rust toolchain installation and configuration
  - Project structure and module organization
  - Cargo.toml profile optimizations (release, dev, test, bench)
  - rust-toolchain.toml for version pinning
  - Professional rustfmt and clippy configurations
  - .cargo/config.toml for faster linking (lld/mold)
  - Additional development tools (cargo-audit, cargo-deny, cargo-nextest, etc.)

### Implementation Work 🔨

**Read BEFORE implementing any new features:**

- [`rust-clean-code/implementation`](../skills/rust-clean-code/implementation/skill.md)
  - WHY/WHAT/HOW documentation patterns with panic documentation
  - derive_more error handling patterns
  - no_std/std hybrid library strategies
  - Naming conventions (RFC 430) for types, generics, lifetimes
  - #[must_use] attribute patterns
  - Performance patterns (SmallVec, inline hints, allocation reduction)
  - Security best practices (input validation, secrets management)
  - Iterator patterns and trait implementations
  - Type system mastery (newtypes, builders, type states)
  - **Examples**: [`.agents/skills/rust-clean-code/implementation/examples/`](../skills/rust-clean-code/implementation/examples/)

### Testing Work 🧪

**Read BEFORE writing or reviewing tests:**

- [`rust-clean-code/testing`](../skills/rust-clean-code/testing/skill.md)
  - **CRITICAL**: ALL tests in tests/ directory (NO tests in source files)
  - Test organization: tests/units/ and tests/integration/
  - File naming: {crate_name}_{what_is_tested}.rs
  - Three test validations: input, output, error paths
  - Feature-gated test modules (NOT individual attributes)
  - Property-based testing with proptest
  - Docker/docker-compose for real infrastructure (FIRST)
  - Real code over mocks philosophy
  - Anti-pattern: muted variables without assertions
  - Async test isolation with current_thread flavor
  - **Examples**: [`.agents/skills/rust-clean-code/testing/examples/`](../skills/rust-clean-code/testing/examples/)

### Async/Tokio Work ⚡

**Read BEFORE implementing async code:**

- [`rust-clean-code/async`](../skills/rust-clean-code/async/skill.md)
  - Core principle: Never block the event loop
  - Non-blocking I/O with timeouts
  - spawn_blocking for CPU-intensive work
  - Async test isolation (MANDATORY: current_thread flavor)
  - Channel patterns (unbounded, bounded, broadcast)
  - Task management and select! patterns
  - Common pitfalls (blocking, holding locks across await)
  - Stream processing patterns
  - **Examples**: [`.agents/skills/rust-clean-code/async/examples/`](../skills/rust-clean-code/async/examples/)

## Tooling Standards (Reference Only)

### Required Tools
- **rustup**: Rust toolchain installer and version manager
- **cargo**: Build system, package manager, test runner
- **rustfmt**: Official code formatter
- **clippy**: Lint tool for catching common mistakes
- **rust-analyzer**: LSP implementation for IDE support

### Configuration Files (Reference Only)

See Rule 05 (`./rules/04-work-commit-and-push-rules.md`) and [`agent-guide`](./skills/rust-clean-code/implementation/skill.md) examples:
- `Cargo.toml` - Package manifest with profile configurations
- `.clippy.toml` - Clippy lint configuration

## Verification Workflow (Reference Only)

**MANDATORY**: Every Rust code change MUST be verified by a dedicated verification agent before commit.

See [`verification-workflow-complete-guide`](./rules/08-verification-workflow-complete-guide.md) for complete workflow including:
1. Format check (`cargo fmt --check`)
2. Clippy linting
3. Compilation (debug + release)
4. Test execution

## Testing Philosophy: Real Code Over Mocks

**CRITICAL PRINCIPLE**: Tests must validate actual code behavior, not mock behavior.

### When to Use Mocks (VERY SPARINGLY)

**✅ VALID Mock Usage - External Dependencies Only:**
1. **Third-party network services** - External APIs, cloud services, payment gateways
2. **Operating system resources** - Hardware devices, system calls you can't control
3. **Specific error injection** - Testing rare failure scenarios (disk full, network timeout)

**❌ INVALID Mock Usage - Our Own Code:**
1. **Internal services** - If you wrote it, test the real thing
2. **Database interactions** - Use test databases or in-memory implementations
3. **HTTP clients** - Spin up local test servers
4. **File I/O** - Use temp directories with real files
5. **DNS resolution** - Use localhost or controlled test domains

### The Three Questions (Ask Before Every Mock)

Before using a mock, answer these questions:

1. **Is this really external?**
   - External service I don't control? → Mock OK
   - My own code? → NO MOCK, test real code

2. **Am I testing real logic?**
   - Testing error handling of DNS failure? → Mock OK (specific error injection)
   - Testing that my HTTP client works? → NO MOCK, use real HTTP

3. **Are integration points tested?**
   - Using MockDatabase but never testing real DB? → INVALID
   - Using MockAPI but have separate real API tests? → VALID

### Real Testing Examples

**❌ BAD - Integration Theater:**
```rust
#[test]
fn test_http_client() {
    let mock_dns = MockDnsResolver::new();
    let mock_tcp = MockTcpConnection::new();
    let client = HttpClient::new(mock_dns, mock_tcp);

    // This only tests that mocks work, not that HTTP works!
    assert!(client.get("http://example.com").is_ok());
}
```

**✅ GOOD - Real Integration Testing:**
```rust
#[test]
fn test_http_client_real() {
    // Start real HTTP server on localhost
    let server = TestServer::start();
    server.expect_get("/test").respond_with(200, "OK");

    // Use real client with real DNS, real TCP, real HTTP
    let client = HttpClient::new();
    let response = client.get(&server.url("/test")).unwrap();

    assert_eq!(response.status(), 200);
    assert_eq!(response.body(), "OK");
}
```

**✅ GOOD - Mock for External Service:**
```rust
#[test]
fn test_payment_gateway_timeout() {
    // Valid: External service, testing specific error scenario
    let mock_gateway = MockPaymentGateway::timeout_after(1);
    let processor = PaymentProcessor::new(mock_gateway);

    let result = processor.charge(100);
    assert!(matches!(result, Err(PaymentError::Timeout)));
}
```

### Rust-Specific Real Testing Tools

**For HTTP Clients:**
- `axum` + `tokio` test server for real HTTP
- `hyper::server` for low-level HTTP testing
- `wiremock` for HTTP mock server (still uses real HTTP stack!)

**For Databases:**
- `sqlx::testing` for real database tests
- `testcontainers` for Docker-based real databases
- In-memory SQLite for fast real SQL tests

**For DNS:**
- `localhost` always resolves (valid for testing)
- `trust-dns` for spinning up test DNS servers
- Real DNS calls in CI (with retry logic)

**For Files:**
- `tempfile` crate for real temporary files/directories
- Test with actual filesystem, not mocks

### Integration Test Requirements

**MANDATORY for all features:**

1. **End-to-end tests** - Full user workflow with real components
2. **Real external integration** - If it talks to network/disk, test it for real
3. **Mock only externals** - Third-party services only
4. **Document mock reasoning** - Why this specific mock is valid

**Example: HTTP Client Testing Strategy:**
```rust
// Unit tests - test individual components
mod unit_tests {
    // Real DNS resolver with localhost
    #[test]
    fn test_dns_resolver_localhost() {
        let resolver = SystemDnsResolver::new();
        assert!(resolver.resolve("localhost", 80).is_ok());
    }
}

// Integration tests - test complete flows
mod integration_tests {
    // Real HTTP server + real client
    #[test]
    fn test_http_get_request() {
        let server = start_test_http_server();
        let client = HttpClient::new();
        let response = client.get(&server.url("/")).unwrap();
        assert_eq!(response.status(), 200);
    }

    // Mock external service
    #[test]
    fn test_external_api_failure() {
        // Valid: External service, testing error handling
        let mock = MockExternalAPI::with_error(500);
        let client = ApiClient::new(mock);
        assert!(client.fetch_data().is_err());
    }
}
```

### Red Flags: Signs You're Mocking Too Much

⚠️ **Warning signs:**
- Tests pass but production code fails
- High test coverage but low confidence
- "Integration tests" that never touch real I/O
- More mock code than real code
- Tests only verify mock setup, not behavior
- Can't run tests without network mocks

✅ **Healthy signs:**
- Tests catch real bugs before production
- Integration tests use real local services
- Mocks only for external dependencies
- Tests run against real databases/servers
- Can reproduce production issues in tests

## Learning Log References (from consolidated skills)

### 2026-02-02: Testing Philosophy - Real Code Over Mocks 🧪
**CRITICAL**: Mocks are for external dependencies only. Test actual implementations, not mock behavior.
- Use real HTTP servers (axum, hyper) in integration tests
- Use real databases (testcontainers, in-memory SQLite)
- Use real file I/O with tempfile
- Only mock third-party services you don't control
- Ask three questions before every mock: Is this external? Am I testing real logic? Are integration points tested?

### 2026-01-27: Testing Failures Anti-Patterns ⚠️
Tests that create variables but never validate their actual content are critical anti-patterns:
- ❌ Bad: `let result = do_work();` with no assertions about what happens after or validation of the variable's content.
- ✅ Good: Validates both valid and invalid inputs produce correct results/errors.

### 2026-01-23: no_std/std Implementation Strategy 📚
For libraries supporting both environments:
1. **no_std mode**: Always implement from scratch using `core` and atomics (see [`rust-clean-code/implementation`](../skills/rust-clean-code/implementation/skill.md))
2. **std mode**: Re-export std types when sufficient; wrap to add methods if needed

### 2026-01-24: Feature-Gated Type Architecture Pattern 📚
For managing complex feature combinations:
1. Create compatibility layers in higher-level dependencies (e.g., `foundation_nostd`)
2. Use explicit submodule paths - never wildcard re-exports for type imports
3. Move complexity up to dependency, keep consuming code simple and clear

---

*Created: 2026-01-11*
*Last Updated: 2026-01-28 - Enhanced with complete skill references and professional configuration patterns*
