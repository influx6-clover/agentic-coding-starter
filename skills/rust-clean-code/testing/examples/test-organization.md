# Test Organization Examples

This document provides complete examples of organizing tests in the `tests/` directory structure.

## Unit Tests in tests/units/

File naming convention: `{crate_name}_{what_is_being_tested}.rs`

### Example: Parser Tests

```rust
// tests/units/myapp_parser_tests.rs
//! Unit tests for parser module in myapp crate.
//!
//! Tests individual parser functions for correctness.

use myapp::parser::{parse_input, validate_syntax};

#[test]
fn test_parse_input_valid_data() {
    let result = parse_input("valid input");
    assert!(result.is_ok());
    assert_eq!(result.unwrap().len(), 2);
}

#[test]
fn test_parse_input_empty_string() {
    let result = parse_input("");
    assert!(result.is_err());
}

#[test]
fn test_validate_syntax_correct() {
    assert!(validate_syntax("{ valid: true }").is_ok());
}
```

### Example: Validation Tests

```rust
// tests/units/myapp_validation_tests.rs
//! Unit tests for validation module in myapp crate.
//!
//! Tests email validation, input sanitization, etc.

use myapp::validation::{validate_email, sanitize_input};

#[test]
fn test_validate_email_valid_formats() {
    assert!(validate_email("test@example.com").is_ok());
    assert!(validate_email("user+tag@domain.co.uk").is_ok());
}

#[test]
fn test_validate_email_invalid_formats() {
    assert!(validate_email("invalid").is_err());
    assert!(validate_email("@example.com").is_err());
}

#[test]
fn test_sanitize_input_removes_scripts() {
    let input = "<script>alert('xss')</script>Hello";
    let sanitized = sanitize_input(input);
    assert!(!sanitized.contains("script"));
    assert!(sanitized.contains("Hello"));
}
```

## Integration Tests in tests/integration/

File naming convention: `{crate_name}_{workflow_description}.rs`

### Example: API Workflow Tests

```rust
// tests/integration/myapp_api_workflow.rs
//! Integration tests for myapp public API workflows.
//!
//! Tests complete user workflows using only public API.

use myapp::{App, Config};

#[test]
fn test_full_user_registration_workflow() {
    // Setup
    let config = Config::default();
    let app = App::new(config).expect("should create app");

    // Execute workflow
    let user = app.register_user("alice", "alice@example.com").unwrap();
    assert_eq!(user.name, "alice");

    let logged_in = app.login("alice", "password").unwrap();
    assert_eq!(logged_in.id, user.id);
}
```

### Example: Authentication Flow Tests

```rust
// tests/integration/myapp_authentication_flow.rs
//! Integration tests for authentication flows in myapp.
//!
//! Tests login, logout, session management workflows.

use myapp::{AuthService, SessionStore};

#[test]
fn test_login_logout_flow() {
    let session_store = SessionStore::new();
    let auth = AuthService::new(session_store);

    let session = auth.login("user", "pass").unwrap();
    assert!(auth.is_authenticated(&session.token));

    auth.logout(&session.token).unwrap();
    assert!(!auth.is_authenticated(&session.token));
}
```

## Migration from Old Style

### Old Pattern (Tests in Source Files) - Don't Do This

```rust
// OLD ❌ - Tests in source files
// src/parser.rs
pub fn parse(input: &str) -> Result<Data> { /* ... */ }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse() { /* ... */ }
}
```

### New Pattern (Tests in Dedicated Files) - Do This

```rust
// NEW ✅ - Tests in dedicated files
// src/parser.rs
pub fn parse(input: &str) -> Result<Data> { /* ... */ }
// NO tests here!

// tests/units/myapp_parser_tests.rs
use myapp::parser::parse;

#[test]
fn test_parse_valid_input() { /* ... */ }

#[test]
fn test_parse_empty_input() { /* ... */ }
```

## Complete Project Structure

```
project_root/
├── Cargo.toml
├── src/
│   ├── lib.rs              # NO #[cfg(test)] modules here
│   └── module.rs           # NO #[cfg(test)] modules here
├── tests/                   # ALL tests go here
│   ├── units/              # Unit tests (test individual functions/modules)
│   │   ├── crate_name_module_name.rs
│   │   ├── crate_name_parser_tests.rs
│   │   └── crate_name_validation_tests.rs
│   ├── integration/        # Integration tests (test public API workflows)
│   │   ├── crate_name_api_workflow.rs
│   │   ├── crate_name_authentication_flow.rs
│   │   └── crate_name_error_handling.rs
│   └── common/             # Shared test utilities
│       └── mod.rs
└── benches/                # Benchmarks at project root
    └── crate_name/
        ├── parsing.rs
        └── serialization.rs
```

## Benefits of This Structure

- ✅ **Clear separation** - Tests are separate from production code
- ✅ **Better organization** - Easy to find unit vs integration tests
- ✅ **Parallel compilation** - Tests compile separately from main crate
- ✅ **No pollution** - Source files stay clean without test code
- ✅ **Consistent naming** - Easy to understand what each test file covers
- ✅ **Scalable** - Works well for both single crates and workspaces
