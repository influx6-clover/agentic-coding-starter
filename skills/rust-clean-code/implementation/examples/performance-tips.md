# Performance Tips

This document provides practical performance optimization patterns for Rust code.

## Core Principles

1. **Measure first** - Use `criterion` for benchmarks
2. **Profile** - Use `cargo flamegraph` or `perf`
3. **Optimize hot paths** - Focus on code that runs frequently
4. **Avoid premature optimization** - Clarity first, speed second

## Common Performance Patterns

### 1. Use References to Avoid Clones

```rust
// ❌ BAD - Unnecessary clone
fn process(data: Vec<u8>) -> usize {
    data.len()
}
let len = process(my_data.clone()); // Clone just to get length!

// ✅ GOOD - Borrow instead
fn process(data: &[u8]) -> usize {
    data.len()
}
let len = process(&my_data); // No clone needed
```

### 2. Preallocate Collections

```rust
// ❌ BAD - Grows as needed
let mut result = Vec::new();
for i in 0..1000 {
    result.push(i);
}

// ✅ GOOD - Preallocate
let mut result = Vec::with_capacity(1000);
for i in 0..1000 {
    result.push(i);
}
```

### 3. Use Iterators Instead of Loops

```rust
// ❌ SLOWER - Index-based loop
let mut sum = 0;
for i in 0..numbers.len() {
    sum += numbers[i];
}

// ✅ FASTER - Iterator (no bounds checks)
let sum: i32 = numbers.iter().sum();
```

### 4. Avoid String Allocations

```rust
// ❌ BAD - Creates new String each time
fn get_prefix() -> String {
    "prefix".to_string()
}

// ✅ GOOD - Return &str
fn get_prefix() -> &'static str {
    "prefix"
}

// Or use Cow for conditional ownership
use std::borrow::Cow;

fn get_name(custom: Option<&str>) -> Cow<'static, str> {
    match custom {
        Some(s) => Cow::Owned(s.to_string()),
        None => Cow::Borrowed("default"),
    }
}
```

### 5. Use `&str` Instead of `String` for Parameters

```rust
// ❌ BAD - Forces caller to own String
fn process(s: String) { }

// ✅ GOOD - Accepts any string type
fn process(s: &str) { }

// Caller can pass:
process("literal");
process(&my_string);
process(&my_string[..]);
```

### 6. Small Copy Types > References

```rust
// ❌ SLOWER - Reference has indirection
fn add(a: &i32, b: &i32) -> i32 {
    a + b
}

// ✅ FASTER - Copy is cheaper than indirection
fn add(a: i32, b: i32) -> i32 {
    a + b
}

// Rule: If type is ≤16 bytes and Copy, pass by value
```

### 7. Avoid Vec<String> When Possible

```rust
// ❌ SLOW - Many heap allocations
let names: Vec<String> = vec![
    "alice".to_string(),
    "bob".to_string(),
];

// ✅ FASTER - Single allocation for Vec
let names: Vec<&str> = vec!["alice", "bob"];

// ✅ EVEN BETTER - No allocation at all
const NAMES: &[&str] = &["alice", "bob"];
```

### 8. Use SmallVec for Small Collections

```rust
use smallvec::SmallVec;

// Stores up to 4 items on stack, heap for more
type SmallBuffer = SmallVec<[u8; 4]>;

fn process() -> SmallBuffer {
    let mut buf = SmallBuffer::new();
    buf.push(1);
    buf.push(2);
    buf // No heap allocation if ≤4 items
}
```

## Advanced Patterns

### Pattern 1: Reuse Allocations

```rust
// Keep buffer between iterations
let mut buffer = Vec::with_capacity(1024);
for item in items {
    buffer.clear(); // Reuse capacity
    process_into(&item, &mut buffer);
}
```

### Pattern 2: Use Bytes for Binary Data

```rust
use bytes::Bytes;

// ❌ BAD - Vec allocates and copies
fn process(data: Vec<u8>) { }

// ✅ GOOD - Bytes is cheap to clone (refcount)
fn process(data: Bytes) { }
```

### Pattern 3: Inline Hot Functions

```rust
// For small, frequently-called functions
#[inline]
fn is_valid(x: u8) -> bool {
    x > 0 && x < 128
}

// For critical hot paths
#[inline(always)]
fn fast_path(x: u32) -> u32 {
    x * 2
}
```

### Pattern 4: Use `Cow` for Conditional Cloning

```rust
use std::borrow::Cow;

fn process<'a>(data: &'a str, uppercase: bool) -> Cow<'a, str> {
    if uppercase {
        Cow::Owned(data.to_uppercase())
    } else {
        Cow::Borrowed(data)
    }
}
```

## Benchmarking

```rust
// Cargo.toml
[dev-dependencies]
criterion = "0.5"

[[bench]]
name = "my_bench"
harness = false

// benches/my_bench.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn fibonacci_bench(c: &mut Criterion) {
    c.bench_function("fib 20", |b| {
        b.iter(|| fibonacci(black_box(20)))
    });
}

criterion_group!(benches, fibonacci_bench);
criterion_main!(benches);
```

Run benchmarks:
```bash
cargo bench
```

## Profiling

```bash
# Install flamegraph
cargo install flamegraph

# Generate flamegraph
cargo flamegraph --bin myapp

# Opens SVG showing hot paths
```

## When to Optimize

**✅ Optimize when:**
- Profiler shows hot spots
- Benchmarks show measurable impact
- User-facing performance matters
- Code is stable and correct

**❌ Don't optimize when:**
- Code isn't finished
- No measurements taken
- Premature (before profiling)
- Trades clarity for tiny gains

## Checklist

- [ ] Benchmarked with criterion before optimizing
- [ ] Profiled to find actual hot paths
- [ ] Used references instead of clones where possible
- [ ] Preallocated collections with known sizes
- [ ] Chose appropriate string types (&str vs String)
- [ ] Passed small Copy types by value
- [ ] Avoided unnecessary allocations
- [ ] Measured after optimization to verify improvement
