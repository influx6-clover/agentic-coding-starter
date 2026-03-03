# Common Test Pitfalls and Solutions

This document shows examples of common testing mistakes and how to fix them.

## Pitfall 1: Testing Implementation Details

**Problem:** Testing internal state instead of behavior.

### Bad - Testing Implementation

```rust
// BAD ❌ - Testing internal cache state
#[test]
fn test_cache_internal_state() {
    let cache = Cache::new();
    cache.insert("key", "value");
    assert_eq!(cache.internal_map.len(), 1); // Testing internals!
}
```

### Good - Testing Behavior

```rust
// GOOD ✅ - Testing observable behavior
#[test]
fn test_cache_stores_and_retrieves_values() {
    let cache = Cache::new();
    cache.insert("key", "value");
    assert_eq!(cache.get("key"), Some("value")); // Testing behavior!
}
```

## Pitfall 2: No Error Path Testing

**Problem:** Only testing success cases, ignoring error handling.

### Bad - Only Success Cases

```rust
// BAD ❌ - Only happy path
#[test]
fn test_parse_valid_json() {
    let result = parse_json(r#"{"key": "value"}"#);
    assert!(result.is_ok());
}
```

### Good - Test Both Success and Failure

```rust
// GOOD ✅ - Test both paths
#[test]
fn test_parse_valid_json() {
    let result = parse_json(r#"{"key": "value"}"#);
    assert!(result.is_ok());
}

#[test]
fn test_parse_invalid_json() {
    let result = parse_json(r#"{"key": invalid}"#);
    assert!(result.is_err());
    assert_eq!(
        result.unwrap_err().to_string(),
        "invalid JSON: expected string value"
    );
}

#[test]
fn test_parse_empty_string() {
    let result = parse_json("");
    assert!(result.is_err());
}
```

## Pitfall 3: Missing Initialization in Tests

**Problem:** Tests pass incorrectly because setup is missing.

### Bad - Missing Setup

```rust
// BAD ❌ - No setup, false positive
#[test]
fn test_user_can_login() {
    let result = login("alice", "password");
    // This fails, but for the wrong reason - user doesn't exist!
    assert!(result.is_err());
}
```

### Good - Proper Setup

```rust
// GOOD ✅ - Proper test setup
#[test]
fn test_user_can_login() {
    // Setup: Create user first
    let db = setup_test_db();
    create_user(&db, "alice", "password");

    // Test: Verify login works
    let result = login("alice", "password");
    assert!(result.is_ok());
    assert_eq!(result.unwrap().username, "alice");
}

#[test]
fn test_invalid_credentials_rejected() {
    // Setup: Create user
    let db = setup_test_db();
    create_user(&db, "alice", "password");

    // Test: Verify wrong password fails
    let result = login("alice", "wrong_password");
    assert!(result.is_err());
    assert_eq!(
        result.unwrap_err().to_string(),
        "invalid credentials"
    );
}
```

## Pitfall 4: Muted Variables Without Assertions

**Problem:** Variables are calculated but never asserted, making tests useless.

### Bad - No Assertions

```rust
// BAD ❌ - Calculates but doesn't verify
#[test]
fn test_process_data() {
    let input = vec![1, 2, 3];
    let _result = process_data(input); // No assertion!
}
```

### Good - Explicit Assertions

```rust
// GOOD ✅ - Verifies results
#[test]
fn test_process_data() {
    let input = vec![1, 2, 3];
    let result = process_data(input);

    assert_eq!(result.len(), 3);
    assert_eq!(result[0], 2); // 1 * 2
    assert_eq!(result[1], 4); // 2 * 2
    assert_eq!(result[2], 6); // 3 * 2
}
```

## Test Helper Functions (Good Pattern)

Proper test helpers reduce duplication without hiding logic:

```rust
/// Helper: Create test database with schema
fn setup_test_db() -> Database {
    let db = Database::new_in_memory();
    db.execute_sql(include_str!("schema.sql")).unwrap();
    db
}

/// Helper: Create user with default test settings
fn create_test_user(db: &Database, username: &str) -> User {
    create_user(db, username, "default_password")
}

/// Helper: Assert user has expected permissions
fn assert_has_permissions(user: &User, expected: &[Permission]) {
    let actual: Vec<_> = user.permissions().collect();
    assert_eq!(actual.len(), expected.len());
    for perm in expected {
        assert!(actual.contains(perm), "Missing permission: {:?}", perm);
    }
}

// Usage in tests
#[test]
fn test_admin_user_has_all_permissions() {
    let db = setup_test_db();
    let admin = create_test_user(&db, "admin");

    grant_admin_role(&db, admin.id);

    assert_has_permissions(&admin, &[
        Permission::Read,
        Permission::Write,
        Permission::Delete,
    ]);
}
```

## Key Takeaways

1. **Test behavior, not implementation** - Tests should care about what code does, not how
2. **Test error paths** - Most bugs are in error handling
3. **Proper setup** - Every test should create the state it needs
4. **Explicit assertions** - Every test must verify results
5. **Good helpers** - Extract common setup, but keep assertions visible
