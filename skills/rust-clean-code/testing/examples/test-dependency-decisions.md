# Test Dependency Decision Tree

This document provides decision trees and guidelines for choosing between project types, stdlib, and external dependencies for testing.

## Core Principle

**Project Building Blocks → Stdlib → External Dependencies (in that order)**

Always check what you have before adding dependencies.

## Decision Tree: HTTP Testing

```
Need to test HTTP?
├─ Does project have HTTP types? (e.g., wire::simple_http)
│  ├─ YES → Create foundation_testing crate with TestHttpServer ✅ BEST
│  │       See: http-testing-with-project-types.md
│  └─ NO → Continue to stdlib
├─ Can stdlib do it? (std::net::TcpListener + raw bytes)
│  ├─ YES → Use stdlib with raw HTTP bytes ✅ GOOD
│  │       See: tcp-testing-stdlib.md
│  └─ NO → Use minimal external dep (tiny_http) ✅ ACCEPTABLE
```

## Decision Tree: Database Testing

```
Need to test database code?
├─ Can database run in Docker? (PostgreSQL, MySQL, MongoDB, etc.)
│  ├─ YES → Use docker-compose or testcontainers-rs ✅ BEST
│  │       See: docker-for-testing.md or testcontainers-examples.md
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

## Decision Tree: JSON Testing

```
Need to test JSON?
├─ Does project have JSON types?
│  ├─ YES → Create foundation_testing with helpers ✅ BEST
│  └─ NO → Use serde_json ✅ ACCEPTABLE
```

## Decision Tree: Test Utilities

```
Need test utilities?
├─ Multiple crates need it?
│  ├─ YES → Create dedicated testing crate (e.g., foundation_testing) ✅ BEST
│  │       Benefit: Reusable, parallel compilation, clean separation
│  └─ NO → Small helper module in single crate ✅ ACCEPTABLE
```

## When to Use Test-Only External Dependencies

**✅ ACCEPTABLE External Dependencies:**

- `testcontainers` - Real Docker containers for databases/services
- `tempfile` - Safe temporary files/directories
- `proptest` - Property-based testing framework
- `criterion` - Benchmarking (performance regression detection)
- `wiremock` - HTTP mocking for **external** APIs only (not your own code)
- `tiny_http` - Minimal HTTP server (if project has no HTTP types)

**❌ AVOID Adding Dependencies For:**

- Mock your own types → Use real implementations
- "Test helpers" that duplicate stdlib → Use stdlib
- Complex test frameworks when simple assertions work
- Things your project already provides

## The Three Questions Before Adding a Test Dependency

1. **"Does the project already have this?"**
   - Check existing crates, especially `foundation_*` or `*_core`
   - Grep for similar functionality: `rg "TcpListener|HttpServer"`

2. **"Can stdlib do this?"**
   - `std::net` for TCP/UDP
   - `std::fs` with `tempfile` for files
   - `std::thread` for concurrency testing

3. **"Is this dependency truly minimal?"**
   - Check crate size: `cargo tree -e normal,build`
   - Check dependencies: Large trees indicate complexity
   - Prefer well-maintained, focused crates

## Project Structure for Testing Crate

If creating a dedicated testing crate (e.g., `foundation_testing`):

```
backends/
├── foundation_core/          # Production code
│   └── src/
│       └── wire/
│           └── simple_http/  # HTTP types live here
├── foundation_testing/        # Testing infrastructure
│   ├── Cargo.toml
│   │   [dependencies]
│   │   foundation_core = { path = "../foundation_core" }
│   └── src/
│       ├── lib.rs
│       └── http_server.rs    # TestHttpServer using foundation_core types
└── foundation_app/            # Uses both
    ├── tests/
    │   ├── units/
    │   │   └── app_logic_tests.rs
    │   └── integration/
    │       └── http_integration.rs
    └── Cargo.toml
        [dev-dependencies]
        foundation_testing = { path = "../foundation_testing" }
```

**Benefits:**
- ✅ Clean separation: production vs test infrastructure
- ✅ Parallel compilation: builds alongside main crates
- ✅ Reusable: Multiple crates can depend on `foundation_testing`
- ✅ No test code in production binaries
- ✅ Clear dependency: `foundation_testing` → `foundation_core`

## Integration Tests Directory

Integration tests ALWAYS go in `./tests` directory:

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

**Why `./tests` directory:**
- ✅ **No cyclical dependencies** - Integration tests are separate crate
- ✅ **Clean organization** - Clear separation of unit vs integration tests
- ✅ **Realistic testing** - Tests use public API like real consumers
- ✅ **Multiple sources** - Can test against foundation_testing AND external servers
- ✅ **Conditional compilation** - Easy to exclude expensive tests from CI

## Test Pyramid Strategy

1. **Many tests (90%)**: Fast unit tests using project's testing utilities
2. **Some tests (9%)**: Integration tests in `./tests` using testing utilities
3. **Few tests (1%)**: External validation tests with `#[ignore]` attribute

**Run Strategy:**
```bash
# Fast tests only (no external network calls)
cargo test

# Include external validation tests
cargo test -- --ignored

# Run all tests (internal + external)
cargo test -- --include-ignored
```

## Summary Checklist

Before adding a test dependency:

- [ ] Checked if project already has needed types/utilities
- [ ] Considered if stdlib can do it
- [ ] Evaluated dependency size and maintenance
- [ ] Decided if creating testing crate is better (for reusability)
- [ ] Understood the test pyramid strategy
- [ ] Placed integration tests in `./tests` directory
