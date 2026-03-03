# TDD Patterns

This document provides common TDD patterns for different scenarios.

## Pattern: Feature with Multiple Requirements

When building a feature with multiple requirements, tackle one requirement per test.

### Example: User Authentication

**Requirement 1: Valid credentials should succeed**
```rust
#[test]
fn test_login_with_valid_credentials() {
    let auth = AuthService::new();
    auth.create_user("alice", "password123");

    let result = auth.login("alice", "password123");
    assert!(result.is_ok());
}
```

**Requirement 2: Invalid password should fail**
```rust
#[test]
fn test_login_with_wrong_password() {
    let auth = AuthService::new();
    auth.create_user("alice", "password123");

    let result = auth.login("alice", "wrongpassword");
    assert!(result.is_err());
}
```

**Requirement 3: Non-existent user should fail**
```rust
#[test]
fn test_login_with_nonexistent_user() {
    let auth = AuthService::new();

    let result = auth.login("nobody", "password123");
    assert!(result.is_err());
}
```

## Pattern: Edge Case Testing

Test edge cases separately, one at a time.

### Example: String Validation

**Edge case 1: Empty string**
```typescript
test('validation rejects empty string', () => {
  const validator = new Validator();
  expect(validator.isValid('')).toBe(false);
});
```

**Edge case 2: Whitespace only**
```typescript
test('validation rejects whitespace-only string', () => {
  const validator = new Validator();
  expect(validator.isValid('   ')).toBe(false);
});
```

**Edge case 3: Maximum length**
```typescript
test('validation accepts string at max length', () => {
  const validator = new Validator({ maxLength: 100 });
  const input = 'a'.repeat(100);
  expect(validator.isValid(input)).toBe(true);
});
```

**Edge case 4: Over maximum length**
```typescript
test('validation rejects string over max length', () => {
  const validator = new Validator({ maxLength: 100 });
  const input = 'a'.repeat(101);
  expect(validator.isValid(input)).toBe(false);
});
```

## Pattern: Refactoring with TDD Safety

Use tests as safety net when refactoring.

### Before Refactoring: Write Comprehensive Tests

```python
def test_calculate_total_with_discount():
    """Coverage before refactoring"""
    cart = ShoppingCart()
    cart.add_item("book", 10.00)
    cart.add_item("pen", 2.00)
    cart.apply_discount(0.1)  # 10% off

    assert cart.total() == 10.80  # (10 + 2) * 0.9

def test_calculate_total_without_discount():
    cart = ShoppingCart()
    cart.add_item("book", 10.00)
    cart.add_item("pen", 2.00)

    assert cart.total() == 12.00

def test_empty_cart_total_is_zero():
    cart = ShoppingCart()
    assert cart.total() == 0.00
```

### During Refactoring: Tests Keep Passing

```python
# Refactor internal implementation
class ShoppingCart:
    def __init__(self):
        self._items = []
        self._discount = 0.0

    def total(self) -> float:
        # Refactored to use helper methods
        subtotal = self._calculate_subtotal()
        return self._apply_discount(subtotal)

    def _calculate_subtotal(self) -> float:
        return sum(item.price for item in self._items)

    def _apply_discount(self, amount: float) -> float:
        return amount * (1 - self._discount)
```

### After Refactoring: All Tests Still Pass

```bash
pytest test_shopping_cart.py
# All 3 tests pass - refactoring was safe!
```

## Pattern: Building Complex Algorithms Step-by-Step

Break down complex algorithms into incremental tests.

### Example: Fibonacci Sequence

**Step 1: Base case - fib(0)**
```rust
#[test]
fn test_fibonacci_zero_returns_zero() {
    assert_eq!(fibonacci(0), 0);
}

// Implementation
fn fibonacci(n: u32) -> u32 {
    0
}
```

**Step 2: Base case - fib(1)**
```rust
#[test]
fn test_fibonacci_one_returns_one() {
    assert_eq!(fibonacci(1), 1);
}

// Implementation
fn fibonacci(n: u32) -> u32 {
    match n {
        0 => 0,
        1 => 1,
        _ => 0,
    }
}
```

**Step 3: Recursive case - fib(2)**
```rust
#[test]
fn test_fibonacci_two_returns_one() {
    assert_eq!(fibonacci(2), 1);
}

// Implementation
fn fibonacci(n: u32) -> u32 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}
```

**Step 4: Verify larger numbers**
```rust
#[test]
fn test_fibonacci_five_returns_five() {
    assert_eq!(fibonacci(5), 5);
}

#[test]
fn test_fibonacci_ten_returns_fifty_five() {
    assert_eq!(fibonacci(10), 55);
}
```

## Pattern: Data-Driven Development

Test different data scenarios one at a time.

### Example: Tax Calculator

**Scenario 1: Low income bracket**
```typescript
test('calculates tax for low income', () => {
  const calculator = new TaxCalculator();
  const tax = calculator.calculate(30000);
  expect(tax).toBe(3000); // 10% rate
});
```

**Scenario 2: Medium income bracket**
```typescript
test('calculates tax for medium income', () => {
  const calculator = new TaxCalculator();
  const tax = calculator.calculate(75000);
  expect(tax).toBe(11250); // Progressive rates
});
```

**Scenario 3: High income bracket**
```typescript
test('calculates tax for high income', () => {
  const calculator = new TaxCalculator();
  const tax = calculator.calculate(150000);
  expect(tax).toBe(30000); // Higher progressive rates
});
```

## Pattern: Error Handling Development

Build error handling incrementally.

### Example: File Reader

**Happy path first**
```python
def test_read_existing_file():
    reader = FileReader()
    content = reader.read("test.txt")
    assert content == "test content"
```

**Error case 1: File not found**
```python
def test_read_nonexistent_file_raises_error():
    reader = FileReader()
    with pytest.raises(FileNotFoundError):
        reader.read("nonexistent.txt")
```

**Error case 2: Permission denied**
```python
def test_read_protected_file_raises_error():
    reader = FileReader()
    with pytest.raises(PermissionError):
        reader.read("/root/protected.txt")
```

**Error case 3: Empty file**
```python
def test_read_empty_file_returns_empty_string():
    reader = FileReader()
    content = reader.read("empty.txt")
    assert content == ""
```

## Key Principles

1. **One test per requirement** - Each test validates one specific behavior
2. **Small steps** - Build complex features incrementally
3. **Safety net** - Tests protect refactoring
4. **Clear progression** - Each test adds one piece of functionality
5. **Edge cases separate** - Don't mix happy path and edge cases
6. **Error cases explicit** - Test each error condition separately
