# HTTP Testing with Project's Own Types

This example shows how to create a dedicated testing crate that uses your project's existing HTTP types, avoiding external dependencies.

## Creating a Test HTTP Server with Project Types

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

## Test Organization with Internal and External Tests

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

## Why This Approach

**Benefits of separate testing crate:**
- ✅ Clean separation: production vs test infrastructure
- ✅ Parallel compilation: builds alongside main crates
- ✅ Reusable: Multiple crates can depend on `foundation_testing`
- ✅ No test code in production binaries
- ✅ Clear dependency: `foundation_testing` → `foundation_core`

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
