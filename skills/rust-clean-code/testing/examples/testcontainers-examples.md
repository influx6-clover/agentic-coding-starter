# Testcontainers Examples

This document provides complete examples of using testcontainers-rs for database and service testing with Docker.

## PostgreSQL with Testcontainers

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

## Redis with Testcontainers

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

## MongoDB with Testcontainers

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

## Shared Test Fixtures with once_cell

For expensive setup operations that can be shared across tests:

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

## Dependencies

Add to your `Cargo.toml`:

```toml
[dev-dependencies]
testcontainers = "0.15"
postgres = "0.19"  # For PostgreSQL examples
redis = "0.23"     # For Redis examples
mongodb = "2.3"    # For MongoDB examples
once_cell = "1.19" # For shared fixtures
```

## Benefits

- ✅ **Real behavior** - Tests validate actual database/service behavior
- ✅ **Production parity** - Same services as production
- ✅ **Isolation** - Each test run gets fresh infrastructure
- ✅ **CI/CD friendly** - Easy to replicate in GitHub Actions/GitLab CI
- ✅ **No mocks** - Test actual integration, not mock configuration
