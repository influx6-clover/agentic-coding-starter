# Feature-Gated Tests

This document shows how to properly organize tests that depend on Cargo features using module-level gates.

## Use Module-Level Gates, Not Individual Attributes

**MANDATORY:** Group feature-specific tests into modules with `#[cfg(...)]` at module level.

### Bad Pattern (Individual Attributes)

```rust
// BAD ❌ - Individual test attributes scattered
#[cfg(test)]
mod tests {
    #[test]
    #[cfg(not(feature = "std"))]
    fn test_spinlock_basic() { }

    #[test]
    #[cfg(not(feature = "std"))]
    fn test_spinlock_contention() { }

    #[test]
    #[cfg(feature = "std")]
    fn test_std_mutex() { }
}
```

### Good Pattern (Module-Level Gates)

```rust
// GOOD ✅ - Feature-gated test modules
#[cfg(test)]
mod tests {
    // Tests for no_std builds (spinlock)
    #[cfg(not(feature = "std"))]
    mod no_std_tests {
        use super::super::*;

        #[test]
        fn test_spinlock_basic() {
            let lock = SpinLock::new(0);
            *lock.lock() = 42;
            assert_eq!(*lock.lock(), 42);
        }

        #[test]
        fn test_spinlock_contention() {
            let lock = Arc::new(SpinLock::new(0));
            let handles: Vec<_> = (0..10).map(|_| {
                let lock = Arc::clone(&lock);
                thread::spawn(move || {
                    *lock.lock() += 1;
                })
            }).collect();

            for h in handles {
                h.join().unwrap();
            }

            assert_eq!(*lock.lock(), 10);
        }
    }

    // Tests for std builds (using std::sync::Mutex)
    #[cfg(feature = "std")]
    mod std_tests {
        use super::super::*;

        #[test]
        fn test_std_mutex() {
            let lock = std::sync::Mutex::new(0);
            *lock.lock().unwrap() = 42;
            assert_eq!(*lock.lock().unwrap(), 42);
        }

        #[test]
        fn test_std_rwlock() {
            let lock = std::sync::RwLock::new(0);
            *lock.write().unwrap() = 42;
            assert_eq!(*lock.read().unwrap(), 42);
        }
    }
}
```

## Why Module-Level Gates?

**Benefits:**
- ✅ **Clear organization** - All no_std tests in one place, all std tests in another
- ✅ **Easier maintenance** - Add new tests to the right module without #[cfg] attributes
- ✅ **Better readability** - Immediately see which tests run under which conditions
- ✅ **Less repetition** - Write `#[cfg(...)]` once per module, not per test
- ✅ **IDE support** - Better syntax highlighting and code completion

**Running tests with different features:**
```bash
# Test with default features
cargo test

# Test without std (no_std)
cargo test --no-default-features

# Test with specific feature
cargo test --features "async"

# Test all feature combinations
cargo test --all-features
```
