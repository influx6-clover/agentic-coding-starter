# Trait Implementation Patterns

This document covers best practices for implementing traits in Rust.

## Core Principles

1. **Implement for references** - More flexible for callers
2. **Provide blanket implementations** - Reduce boilerplate
3. **Use marker traits** - For compile-time guarantees
4. **Document trait contracts** - Explain requirements and invariants

## Common Patterns

### Pattern 1: Implement for &T and T

```rust
pub trait Validator {
    fn validate(&self) -> Result<(), Error>;
}

// Implement for owned type
impl Validator for MyType {
    fn validate(&self) -> Result<(), Error> {
        // Implementation
        Ok(())
    }
}

// Automatic implementation for references
// (already works because validate takes &self)
```

### Pattern 2: Blanket Implementations

```rust
// Implement for all types that implement Display
impl<T: std::fmt::Display> MyTrait for T {
    fn my_method(&self) -> String {
        format!("{}", self)
    }
}
```

### Pattern 3: From/Into Pattern

```rust
// Always implement From, get Into for free
impl From<String> for MyType {
    fn from(s: String) -> Self {
        MyType { data: s }
    }
}

// Now works automatically:
let my_type: MyType = "hello".to_string().into();
```

### Pattern 4: AsRef/Borrow Pattern

```rust
use std::borrow::Borrow;

// Implement AsRef for common conversions
impl AsRef<str> for MyType {
    fn as_ref(&self) -> &str {
        &self.data
    }
}

// Now works with functions accepting AsRef<str>
fn process<S: AsRef<str>>(s: S) {
    let text = s.as_ref();
}

process(my_type); // Works!
process("string"); // Also works!
```

### Pattern 5: Default Implementation

```rust
#[derive(Default)]
pub struct Config {
    timeout: u64,
    retries: u32,
}

// Or manual implementation
impl Default for Config {
    fn default() -> Self {
        Self {
            timeout: 30,
            retries: 3,
        }
    }
}
```

## Iterator Implementation

```rust
pub struct MyIter<T> {
    items: Vec<T>,
    index: usize,
}

impl<T> Iterator for MyIter<T> {
    type Item = T;

    fn next(&mut self) -> Option<Self::Item> {
        if self.index < self.items.len() {
            let item = self.items.swap_remove(self.index);
            self.index += 1;
            Some(item)
        } else {
            None
        }
    }

    // Optional: Provide size_hint for better performance
    fn size_hint(&self) -> (usize, Option<usize>) {
        let remaining = self.items.len() - self.index;
        (remaining, Some(remaining))
    }
}

// Implement IntoIterator for convenience
impl<T> IntoIterator for MyCollection<T> {
    type Item = T;
    type IntoIter = MyIter<T>;

    fn into_iter(self) -> Self::IntoIter {
        MyIter {
            items: self.items,
            index: 0,
        }
    }
}
```

## Display and Debug

```rust
use std::fmt;

impl fmt::Display for MyType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "MyType({})", self.data)
    }
}

impl fmt::Debug for MyType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("MyType")
            .field("data", &self.data)
            .field("count", &self.count)
            .finish()
    }
}
```

## Error Trait

```rust
use std::fmt;

#[derive(Debug)]
pub enum MyError {
    InvalidInput(String),
    NotFound,
}

impl fmt::Display for MyError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            MyError::InvalidInput(msg) => write!(f, "invalid input: {}", msg),
            MyError::NotFound => write!(f, "not found"),
        }
    }
}

#[cfg(feature = "std")]
impl std::error::Error for MyError {}
```

## Deref Pattern

```rust
use std::ops::Deref;

pub struct Wrapper<T>(T);

impl<T> Deref for Wrapper<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

// Now Wrapper<String> can use String methods directly
let wrapped = Wrapper("hello".to_string());
println!("{}", wrapped.len()); // Works due to Deref
```

## Builder Pattern with Traits

```rust
pub trait Builder {
    type Output;

    fn build(self) -> Result<Self::Output, Error>;
}

pub struct ConfigBuilder {
    timeout: Option<u64>,
    retries: Option<u32>,
}

impl Builder for ConfigBuilder {
    type Output = Config;

    fn build(self) -> Result<Self::Output, Error> {
        Ok(Config {
            timeout: self.timeout.unwrap_or(30),
            retries: self.retries.unwrap_or(3),
        })
    }
}

impl ConfigBuilder {
    pub fn timeout(mut self, timeout: u64) -> Self {
        self.timeout = Some(timeout);
        self
    }

    pub fn retries(mut self, retries: u32) -> Self {
        self.retries = Some(retries);
        self
    }
}
```

## Sealed Trait Pattern

```rust
// Prevent external implementations
mod sealed {
    pub trait Sealed {}
}

pub trait MyTrait: sealed::Sealed {
    fn method(&self);
}

// Only we can implement it
impl sealed::Sealed for MyType {}
impl MyTrait for MyType {
    fn method(&self) { }
}
```

## Common Derive Macros

```rust
// Most common combination
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MyType {
    data: String,
}

// For types that can be compared and ordered
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct Ordered {
    priority: u32,
}

// For types that can be copied (no heap allocations)
#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub struct Point {
    x: i32,
    y: i32,
}

// For types with default values
#[derive(Debug, Default)]
pub struct Config {
    timeout: u64,
}
```

## Trait Bounds

```rust
// Multiple bounds
fn process<T: Display + Debug>(item: T) { }

// Where clause for complex bounds
fn process<T>(item: T)
where
    T: Display + Debug + Clone,
    T: Send + Sync,
{
}

// Lifetime bounds
fn process<'a, T: 'a>(item: &'a T)
where
    T: Display,
{
}
```

## Best Practices

✅ **Do:**
- Implement Display for user-facing types
- Implement Debug for all types
- Use derive macros when possible
- Provide Default for configuration types
- Document trait requirements
- Implement From instead of Into
- Use AsRef/Borrow for flexible APIs

❌ **Don't:**
- Implement Clone for large types (use Arc instead)
- Implement PartialEq without Eq (if possible)
- Forget to implement Error for error types
- Make trait objects when static dispatch works
- Implement Into (implement From instead)

## Checklist

- [ ] Implemented Debug for all public types
- [ ] Implemented Display for user-facing types
- [ ] Used derive macros where applicable
- [ ] Provided Default for configuration types
- [ ] Documented trait contracts and invariants
- [ ] Implemented From instead of Into
- [ ] Used AsRef/Borrow for flexible parameters
- [ ] Considered trait objects vs static dispatch
