# No_std / Std Support

This document explains how to write Rust code that works in both no_std and std environments.

## Core Pattern

```rust
// Always use #![cfg_attr] for no_std
#![cfg_attr(not(feature = "std"), no_std)]

// Import from core/alloc, re-export as stdlib names
#[cfg(not(feature = "std"))]
use core::{fmt, result};

#[cfg(feature = "std")]
use std::{fmt, result};
```

## Cargo.toml Configuration

```toml
[package]
name = "mylib"
version = "0.1.0"
edition = "2021"

[features]
default = ["std"]
std = []

[dependencies]
# For no_std allocations
[dependencies.alloc]
package = "alloc"
version = "1.0"
optional = true
default-features = false
```

## Type Imports Pattern

```rust
// String and Vec
#[cfg(not(feature = "std"))]
extern crate alloc;

#[cfg(not(feature = "std"))]
use alloc::{string::String, vec::Vec, format};

#[cfg(feature = "std")]
use std::{string::String, vec::Vec, format};

// HashMap/BTreeMap
#[cfg(not(feature = "std"))]
use alloc::collections::BTreeMap as Map;

#[cfg(feature = "std")]
use std::collections::HashMap as Map;
```

## Error Handling

```rust
use core::fmt;

#[derive(Debug)]
pub enum Error {
    InvalidInput,
    ParseError,
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::InvalidInput => write!(f, "invalid input"),
            Error::ParseError => write!(f, "parse error"),
        }
    }
}

// Only implement std::error::Error in std mode
#[cfg(feature = "std")]
impl std::error::Error for Error {}
```

## I/O Operations

```rust
// No I/O in no_std - use traits instead
pub trait Write {
    fn write(&mut self, buf: &[u8]) -> Result<usize, Error>;
}

// Implement for std types when available
#[cfg(feature = "std")]
impl Write for std::fs::File {
    fn write(&mut self, buf: &[u8]) -> Result<usize, Error> {
        use std::io::Write as _;
        std::io::Write::write(self, buf)
            .map_err(|_| Error::IoError)
    }
}
```

## Testing Both Modes

```bash
# Test with std (default)
cargo test

# Test without std
cargo test --no-default-features

# Test with specific features
cargo test --no-default-features --features "alloc"
```

## Common Patterns

### Pattern 1: Conditional Compilation Blocks

```rust
#[cfg(feature = "std")]
mod std_only {
    pub fn read_file(path: &str) -> Result<String, Error> {
        std::fs::read_to_string(path)
            .map_err(|_| Error::IoError)
    }
}

#[cfg(not(feature = "std"))]
mod std_only {
    pub fn read_file(_path: &str) -> Result<String, Error> {
        Err(Error::NotSupported)
    }
}
```

### Pattern 2: Re-export Common Types

```rust
// lib.rs
mod prelude {
    #[cfg(not(feature = "std"))]
    pub use alloc::{string::String, vec::Vec, format};

    #[cfg(feature = "std")]
    pub use std::{string::String, vec::Vec, format};
}

// Other modules
use crate::prelude::*;
```

### Pattern 3: Feature-Gated Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_core_functionality() {
        // Works in both std and no_std
        let result = parse("input");
        assert!(result.is_ok());
    }

    #[test]
    #[cfg(feature = "std")]
    fn test_std_only_feature() {
        // Only runs with std feature
        let result = read_file("test.txt");
        assert!(result.is_ok());
    }
}
```

## What to Avoid

❌ **Don't use these in no_std libraries:**
- `std::io::*` - Use traits instead
- `std::fs::*` - No filesystem in no_std
- `std::net::*` - No networking in no_std
- `std::process::*` - No process management
- `println!` / `eprintln!` - Use `core::fmt` instead
- `std::sync::Mutex` - Use `spin::Mutex` or similar
- `std::thread` - No threading in no_std

✅ **Safe to use (available in core):**
- `core::fmt` - Formatting
- `core::ops` - Operators
- `core::convert` - Conversions
- `core::option` - Option type
- `core::result` - Result type
- `core::iter` - Iterators
- `core::mem` - Memory utilities

## Checklist for no_std Support

- [ ] Added `#![cfg_attr(not(feature = "std"), no_std)]`
- [ ] Created `std` feature in Cargo.toml
- [ ] Imported types from `core`/`alloc` when std disabled
- [ ] Used conditional compilation for std-only features
- [ ] Implemented `Display` for errors (not just std::error::Error)
- [ ] Tested with `--no-default-features`
- [ ] Documented which features require std
- [ ] Avoided std-only types (io, fs, net, thread)
