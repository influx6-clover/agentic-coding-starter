# Running Tests - Commands and Strategies

This document covers all the ways to run tests in Rust with cargo.

## Basic Commands

```bash
# Run all tests
cargo test

# Run specific test by name
cargo test test_name

# Run tests matching a pattern
cargo test parse  # Runs all tests with "parse" in the name

# Run tests in specific package (workspace)
cargo test --package crate_name
cargo test -p crate_name

# Run tests in specific file
cargo test --test integration_test_file_name
```

## Feature Flags

```bash
# Run tests with default features
cargo test

# Run tests without default features (no_std testing)
cargo test --no-default-features

# Run tests with specific feature enabled
cargo test --features "feature_name"

# Run tests with multiple features
cargo test --features "feature1,feature2"

# Run tests with ALL features enabled
cargo test --all-features
```

## Test Output Control

```bash
# Show stdout/stderr from tests (nocapture)
cargo test -- --nocapture

# Show output even for passing tests
cargo test -- --show-output

# Quiet mode (less output)
cargo test --quiet
cargo test -q
```

## Parallel vs Sequential

```bash
# Run tests in parallel (default)
cargo test

# Run tests sequentially (single thread)
cargo test -- --test-threads=1

# Run with specific number of threads
cargo test -- --test-threads=4
```

## Ignored Tests

Tests marked with `#[ignore]` are skipped by default (useful for slow/network tests):

```rust
#[test]
#[ignore]
fn test_external_api() {
    // Slow test requiring network
}
```

```bash
# Run only ignored tests
cargo test -- --ignored

# Run all tests INCLUDING ignored ones
cargo test -- --include-ignored

# Run specific ignored test
cargo test test_external_api -- --ignored
```

## Test Organization Targeting

```bash
# Run only unit tests (in tests/units/)
cargo test --test 'tests/units/*'

# Run only integration tests (in tests/integration/)
cargo test --test 'tests/integration/*'

# Run specific test file
cargo test --test myapp_parser_tests
```

## Filtering and Selection

```bash
# Run tests in a specific module
cargo test module_name::

# Run tests with exact name match
cargo test --exact test_full_name

# List all tests without running them
cargo test -- --list

# List ignored tests
cargo test -- --ignored --list
```

## Benchmarks

```bash
# Run benchmarks (requires nightly or criterion)
cargo bench

# Run specific benchmark
cargo bench bench_name

# Run benchmarks with criterion
cargo bench --bench benchmark_name
```

## Documentation Tests

```bash
# Run doc tests (code in /// comments)
cargo test --doc

# Run all tests including doc tests
cargo test
```

## Workspace Testing

```bash
# Run tests for all workspace members
cargo test --workspace
cargo test --all

# Exclude specific packages
cargo test --workspace --exclude package_name

# Run tests for specific workspace member
cargo test -p workspace_member_name
```

## Environment Variables

```bash
# Set environment variable for tests
RUST_LOG=debug cargo test

# Multiple environment variables
DATABASE_URL=postgresql://... REDIS_URL=redis://... cargo test

# Run tests with backtrace on failure
RUST_BACKTRACE=1 cargo test
RUST_BACKTRACE=full cargo test
```

## Common Test Workflows

### Local Development (Fast Feedback)

```bash
# Run only fast tests (skip ignored network tests)
cargo test

# Run specific test you're working on
cargo test test_name -- --nocapture
```

### Before Commit (Comprehensive)

```bash
# Run all tests including ignored ones
cargo test -- --include-ignored

# Run with all features
cargo test --all-features
```

### CI/CD Pipeline

```bash
# Run all tests
cargo test --all-features -- --include-ignored

# Run tests with specific features for different jobs
cargo test --no-default-features  # no_std job
cargo test --features "async"      # async job
cargo test --all-features          # full feature job
```

### Debugging Failing Tests

```bash
# Show output and run single-threaded
cargo test test_name -- --nocapture --test-threads=1

# With full backtrace
RUST_BACKTRACE=full cargo test test_name -- --nocapture

# With logging
RUST_LOG=debug cargo test test_name -- --nocapture
```

### Testing with Docker Infrastructure

```bash
# Start infrastructure first
docker-compose -f docker-compose.test.yml up -d

# Wait for services to be ready
sleep 5

# Run tests
cargo test

# Cleanup
docker-compose -f docker-compose.test.yml down -v
```

Or use an automated script (see `docker-for-testing.md`).

## Test Performance

```bash
# Time test execution
time cargo test

# Run tests in parallel (faster)
cargo test

# Run tests sequentially (debugging)
cargo test -- --test-threads=1
```

## Tips and Best Practices

1. **Use `--nocapture` for debugging:**
   ```bash
   cargo test -- --nocapture
   ```

2. **Run specific test during development:**
   ```bash
   cargo test test_name
   ```

3. **Mark expensive tests with `#[ignore]`:**
   ```rust
   #[test]
   #[ignore]
   fn test_expensive_operation() { }
   ```

4. **Use environment variables in tests:**
   ```rust
   let db_url = std::env::var("DATABASE_URL")
       .unwrap_or_else(|_| "postgresql://localhost".to_string());
   ```

5. **Run CI tests locally:**
   ```bash
   # Same command as CI
   cargo test --all-features -- --include-ignored
   ```

6. **Check which tests will run:**
   ```bash
   cargo test -- --list
   ```

## Combining Options

You can combine multiple options:

```bash
# Run specific package, with feature, showing output
cargo test -p myapp --features "async" -- --nocapture

# Run all workspace tests, all features, including ignored
cargo test --workspace --all-features -- --include-ignored

# Run specific test, single-threaded, with output
cargo test test_name -- --nocapture --test-threads=1
```
