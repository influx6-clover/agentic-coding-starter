# Real Testing Tools Examples

This document shows examples of integration theater (bad) vs real testing (good).

## Integration Theater - What NOT to Do

These tests look like integration tests but actually test nothing real:

```rust
// ❌ BAD - Integration Theater Examples

// Mock returns exactly what we configured
#[test]
fn test_get_user_by_id() {
    let mut mock_db = MockDatabase::new();
    mock_db.expect_get_user()
        .with(eq(1))
        .returning(|_| Ok(User { id: 1, name: "Alice".into() }));

    let service = UserService::new(mock_db);
    let user = service.get_user(1).unwrap();

    assert_eq!(user.name, "Alice");
    // ❌ This only tests that our mock works, not our code!
}

// HTTP mock that's more complex than the real client
#[test]
fn test_http_client() {
    let mock_server = MockServer::start();
    mock_server.expect_get("/api/users")
        .with_status(200)
        .with_body(r#"[{"id":1,"name":"Alice"}]"#);

    let client = HttpClient::new(&mock_server.url());
    let users = client.get_users().unwrap();

    assert_eq!(users.len(), 1);
    // ❌ Spent more time on mock than actual HTTP would take!
}
```

## Real Testing - What TO Do

Test actual code with real dependencies:

```rust
// ✅ GOOD - Real Integration Tests

// Real database with testcontainers
#[test]
fn test_user_repository_with_real_db() {
    let docker = testcontainers::clients::Cli::default();
    let postgres = docker.run(testcontainers::images::postgres::Postgres::default());

    let connection_string = format!(
        "postgresql://postgres:postgres@127.0.0.1:{}/postgres",
        postgres.get_host_port_ipv4(5432)
    );

    let db = Database::connect(&connection_string).unwrap();
    let repo = UserRepository::new(db);

    // Test real database operations
    let user = repo.create_user("Alice", "alice@example.com").unwrap();
    let found = repo.get_user(user.id).unwrap();

    assert_eq!(found.name, "Alice");
    assert_eq!(found.email, "alice@example.com");
    // ✅ Tests actual SQL, transactions, error handling!
}

// Real HTTP server with stdlib
#[test]
fn test_http_client_with_real_server() {
    use std::net::TcpListener;
    use std::thread;

    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let addr = format!("http://{}", listener.local_addr().unwrap());

    thread::spawn(move || {
        let (mut stream, _) = listener.accept().unwrap();
        let response = "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK";
        stream.write_all(response.as_bytes()).unwrap();
    });

    // Test real HTTP client
    let client = HttpClient::new();
    let response = client.get(&addr).unwrap();

    assert_eq!(response.status(), 200);
    assert_eq!(response.body(), b"OK");
    // ✅ Tests actual HTTP parsing, connection handling!
}
```

## Red Flags for Integration Theater

Watch out for these warning signs:

```rust
// 🚩 Red Flag 1: Mock setup is more complex than real thing
let mut mock = MockApi::new();
mock.expect_call_1().returning(|| Ok(1));
mock.expect_call_2().with(eq(1)).returning(|_| Ok("result"));
mock.expect_call_3().times(1).returning(|| Ok(()));
// ❌ Just use the real API!

// 🚩 Red Flag 2: Only testing mock return values
#[test]
fn test_service() {
    let mut mock = MockClient::new();
    mock.expect_get().returning(|| Ok(42));
    let service = Service::new(mock);
    assert_eq!(service.get(), Ok(42));
    // ❌ What did we actually test?
}

// 🚩 Red Flag 3: Fragile tests that break on refactoring
#[test]
fn test_service() {
    let mut mock = MockRepo::new();
    mock.expect_find().times(1).returning(|| None);
    mock.expect_create().times(1).returning(|_| Ok(()));
    // ❌ Breaks if we change call order or add caching!
}
```

## Required Test Coverage

Every significant code path needs tests for:

```rust
// ✅ Test ALL of these scenarios:

// 1. Valid input success path
#[test]
fn test_valid_user_registration() {
    let result = register_user("alice", "alice@example.com");
    assert!(result.is_ok());
}

// 2. Invalid input rejection
#[test]
fn test_invalid_email_rejected() {
    let result = register_user("bob", "not-an-email");
    assert!(result.is_err());
    assert_eq!(result.unwrap_err().to_string(), "invalid email format");
}

// 3. Duplicate handling
#[test]
fn test_duplicate_username_rejected() {
    register_user("alice", "alice@example.com").unwrap();
    let result = register_user("alice", "alice2@example.com");
    assert!(result.is_err());
    assert_eq!(result.unwrap_err().to_string(), "username already exists");
}

// 4. Edge cases
#[test]
fn test_empty_username_rejected() {
    let result = register_user("", "test@example.com");
    assert!(result.is_err());
}

#[test]
fn test_very_long_username_rejected() {
    let long_name = "a".repeat(256);
    let result = register_user(&long_name, "test@example.com");
    assert!(result.is_err());
}
```

## Key Principles

1. **Real dependencies over mocks** - Use testcontainers, real servers, real files
2. **Test behavior, not configuration** - Verify your code works, not that mocks work
3. **Comprehensive coverage** - Test success, failure, and edge cases
4. **Keep it simple** - If mocks are complex, use the real thing
5. **Integration tests matter** - They catch bugs unit tests miss
