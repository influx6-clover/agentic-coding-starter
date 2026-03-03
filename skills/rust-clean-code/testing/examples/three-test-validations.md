# Three Test Validations

This document explains the three critical validations every test must perform.

## The Three Validations ✅

Every test must validate three things:

1. **Valid input produces expected output**
2. **Invalid input is properly rejected**
3. **Edge cases are handled correctly**

## Example: User Registration

```rust
use myapp::{register_user, UserError};

// ✅ Validation 1: Valid input success
#[test]
fn test_valid_user_registration() {
    let result = register_user("alice", "alice@example.com", "password123");

    assert!(result.is_ok(), "Valid registration should succeed");
    let user = result.unwrap();
    assert_eq!(user.username, "alice");
    assert_eq!(user.email, "alice@example.com");
    assert!(user.id > 0, "User should have valid ID");
}

// ✅ Validation 2: Invalid input rejection
#[test]
fn test_invalid_email_rejected() {
    let result = register_user("bob", "not-an-email", "password123");

    assert!(result.is_err(), "Invalid email should be rejected");
    match result.unwrap_err() {
        UserError::InvalidEmail(msg) => {
            assert_eq!(msg, "not-an-email is not a valid email address");
        }
        other => panic!("Expected InvalidEmail error, got {:?}", other),
    }
}

#[test]
fn test_short_password_rejected() {
    let result = register_user("charlie", "charlie@example.com", "123");

    assert!(result.is_err(), "Short password should be rejected");
    match result.unwrap_err() {
        UserError::WeakPassword(msg) => {
            assert!(msg.contains("at least 8 characters"));
        }
        other => panic!("Expected WeakPassword error, got {:?}", other),
    }
}

// ✅ Validation 3: Edge cases
#[test]
fn test_empty_username_rejected() {
    let result = register_user("", "test@example.com", "password123");
    assert!(result.is_err(), "Empty username should be rejected");
}

#[test]
fn test_whitespace_only_username_rejected() {
    let result = register_user("   ", "test@example.com", "password123");
    assert!(result.is_err(), "Whitespace-only username should be rejected");
}

#[test]
fn test_very_long_username_rejected() {
    let long_username = "a".repeat(256);
    let result = register_user(&long_username, "test@example.com", "password123");
    assert!(result.is_err(), "Username over limit should be rejected");
}

#[test]
fn test_duplicate_username_rejected() {
    // Setup: Register first user
    register_user("alice", "alice1@example.com", "password123").unwrap();

    // Test: Duplicate username should fail
    let result = register_user("alice", "alice2@example.com", "password123");
    assert!(result.is_err(), "Duplicate username should be rejected");
    match result.unwrap_err() {
        UserError::DuplicateUsername => {},
        other => panic!("Expected DuplicateUsername error, got {:?}", other),
    }
}

#[test]
fn test_duplicate_email_rejected() {
    // Setup: Register first user
    register_user("alice", "alice@example.com", "password123").unwrap();

    // Test: Duplicate email should fail
    let result = register_user("bob", "alice@example.com", "password123");
    assert!(result.is_err(), "Duplicate email should be rejected");
}
```

## Why All Three Validations Matter

**Missing Validation 1 (Valid Input):**
- Function might be completely broken
- Regression from refactoring
- Documentation doesn't match behavior

**Missing Validation 2 (Invalid Input):**
- Security vulnerabilities (injection attacks, XSS)
- Crashes instead of graceful errors
- Poor user experience (unhelpful error messages)

**Missing Validation 3 (Edge Cases):**
- Production bugs from unexpected input
- Race conditions
- Boundary errors (off-by-one, overflow)

## Common Edge Cases to Test

```rust
// Strings
#[test] fn test_empty_string() { }
#[test] fn test_whitespace_only() { }
#[test] fn test_very_long_string() { }
#[test] fn test_unicode_characters() { }
#[test] fn test_special_characters() { }

// Numbers
#[test] fn test_zero() { }
#[test] fn test_negative() { }
#[test] fn test_max_value() { }
#[test] fn test_overflow() { }

// Collections
#[test] fn test_empty_collection() { }
#[test] fn test_single_item() { }
#[test] fn test_many_items() { }
#[test] fn test_duplicates() { }

// Options/Results
#[test] fn test_none_value() { }
#[test] fn test_some_value() { }
#[test] fn test_error_variants() { }

// State
#[test] fn test_uninitialized() { }
#[test] fn test_already_closed() { }
#[test] fn test_concurrent_access() { }
```

## Test Coverage Checklist

For every public function, ensure you have tests for:

- [ ] At least one valid input case that succeeds
- [ ] At least one invalid input case that fails with correct error
- [ ] At least one edge case (empty, max, boundary)
- [ ] Error messages are clear and actionable
- [ ] Return values match expected types and ranges
- [ ] Side effects happen (or don't happen) as expected

## Anti-Pattern: Incomplete Testing

```rust
// ❌ BAD - Only tests happy path
#[test]
fn test_user_registration() {
    let user = register_user("alice", "alice@example.com", "password123").unwrap();
    assert_eq!(user.username, "alice");
    // Missing: Invalid inputs, edge cases, error handling
}

// ✅ GOOD - Comprehensive coverage
#[test]
fn test_user_registration_valid() { /* ... */ }

#[test]
fn test_user_registration_invalid_email() { /* ... */ }

#[test]
fn test_user_registration_weak_password() { /* ... */ }

#[test]
fn test_user_registration_duplicate_username() { /* ... */ }

#[test]
fn test_user_registration_empty_username() { /* ... */ }
```

Remember: **A test suite that only tests success cases is testing less than 50% of your code.**
