# TCP Testing with Pure Stdlib

This example shows how to test TCP connections using only the Rust standard library, without any external dependencies.

## Pure Stdlib TCP Testing

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

## HTTP Testing with Minimal Dependencies

If your project doesn't have HTTP types, you can use a minimal test dependency:

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

## Why Stdlib First

**Principle: Project Building Blocks → Stdlib → External Dependencies (in that order)**

This ensures:
- ✅ No external dependencies when possible
- ✅ Tests are simple and fast
- ✅ Less maintenance burden
- ✅ More portable code
