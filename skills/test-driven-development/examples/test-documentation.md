# Test Documentation Standards

This document covers the mandatory WHY/WHAT documentation format for tests.

## Format (MANDATORY)

Every test MUST have:
```
WHY: <reason for this test>
WHAT: <what behavior is being tested>
```

## Why This Matters

**Without WHY/WHAT:**
- Future developers don't know why test exists
- Tests become "mystery code"
- Hard to maintain or update
- Unclear if test is still relevant

**With WHY/WHAT:**
- Clear purpose and context
- Easy to understand intent
- Guides implementation
- Documents requirements

## Guidelines

### WHY Section
- Explains business reason, requirement, or bug being prevented
- Links to specs, tickets, or security concerns
- Provides context for future maintainers

### WHAT Section
- Describes the exact behavior being validated
- One sentence, specific and clear
- No implementation details

## Examples

### Good Documentation

**Rust:**
```rust
/// WHY: CVE-2024-1234 requires token validation before API access
/// WHAT: Expired tokens should be rejected with 401 status
#[test]
fn test_expired_token_returns_401() {
    let token = create_expired_token();
    let response = api_call_with_token(token);
    assert_eq!(response.status(), 401);
}
```

**TypeScript:**
```typescript
/**
 * WHY: GDPR requires user data deletion within 30 days
 * WHAT: Delete operation should remove all user records from database
 */
test('delete user removes all associated data', async () => {
  const userId = await createTestUser();
  await deleteUser(userId);

  const user = await findUser(userId);
  expect(user).toBeNull();
});
```

**Python:**
```python
def test_email_validation_rejects_invalid_format():
    """
    WHY: Spam prevention requires valid email addresses
    WHAT: Registration with invalid email should fail immediately
    """
    validator = EmailValidator()
    result = validator.validate("not@an@email")
    assert result.is_valid is False
```

**Go:**
```go
// WHY: Rate limiting prevents API abuse (security requirement)
// WHAT: 101st request within 1 minute should return 429 error
func TestRateLimiterRejects101stRequest(t *testing.T) {
    limiter := NewRateLimiter(100, time.Minute)

    // Make 100 requests
    for i := 0; i < 100; i++ {
        assert.NoError(t, limiter.Check("user123"))
    }

    // 101st should fail
    err := limiter.Check("user123")
    assert.Error(t, err)
    assert.Equal(t, ErrRateLimitExceeded, err)
}
```

### Bad Documentation (Don't Do This)

**❌ No documentation:**
```rust
#[test]
fn test_token_validation() {
    // What is being tested? Why?
    let result = validate_token("abc123");
    assert!(result);
}
```

**❌ Only implementation details:**
```typescript
/**
 * Tests the validateEmail method with invalid input
 */
test('validateEmail returns false', () => {
    // Doesn't explain WHY this test exists
    expect(validateEmail("bad")).toBe(false);
});
```

**❌ Vague or generic:**
```python
def test_user_service():
    """Tests user service functionality"""
    # Too vague - what specific behavior?
    service = UserService()
    assert service is not None
```

**❌ Only WHAT, no WHY:**
```go
// WHAT: Returns error for negative numbers
func TestNegativeInput(t *testing.T) {
    // Missing WHY - is this a requirement or bug fix?
    result := Calculate(-5)
    assert.Error(t, result)
}
```

## Template for Different Languages

### Rust
```rust
/// WHY: <business reason, requirement, or bug>
/// WHAT: <specific behavior being tested>
#[test]
fn test_descriptive_name() {
    // Arrange
    // Act
    // Assert
}
```

### TypeScript/JavaScript
```typescript
/**
 * WHY: <business reason, requirement, or bug>
 * WHAT: <specific behavior being tested>
 */
test('descriptive test name', () => {
    // Arrange
    // Act
    // Assert
});
```

### Python
```python
def test_descriptive_name():
    """
    WHY: <business reason, requirement, or bug>
    WHAT: <specific behavior being tested>
    """
    # Arrange
    # Act
    # Assert
```

### Go
```go
// WHY: <business reason, requirement, or bug>
// WHAT: <specific behavior being tested>
func TestDescriptiveName(t *testing.T) {
    // Arrange
    // Act
    // Assert
}
```

## Examples by Category

### Security Requirements
```rust
/// WHY: PCI-DSS requires credit card masking in logs
/// WHAT: Credit card numbers in logs should be masked except last 4 digits
#[test]
fn test_credit_card_masking_in_logs() {
    let log_entry = create_log_with_credit_card("1234567890123456");
    assert_eq!(log_entry.message, "Card: ************3456");
}
```

### Bug Fixes
```typescript
/**
 * WHY: Bug #1234 - Users could bypass payment step
 * WHAT: Checkout should require payment before order confirmation
 */
test('checkout requires payment before confirmation', async () => {
    const checkout = new Checkout();
    await expect(checkout.confirm()).rejects.toThrow('Payment required');
});
```

### Business Rules
```python
def test_discount_applies_to_items_over_100():
    """
    WHY: Marketing campaign offers 10% off purchases over $100
    WHAT: Cart total over $100 should receive 10% discount automatically
    """
    cart = ShoppingCart()
    cart.add_item("laptop", 150.00)

    assert cart.total() == 135.00  # 150 * 0.9
```

### Compliance Requirements
```go
// WHY: HIPAA requires audit trail for all patient data access
// WHAT: Reading patient record should create audit log entry
func TestPatientAccessCreatesAuditLog(t *testing.T) {
    db := setupTestDB()
    patientID := createTestPatient(db)

    _ = readPatientRecord(db, patientID)

    logs := getAuditLogs(db)
    assert.Equal(t, 1, len(logs))
    assert.Equal(t, patientID, logs[0].PatientID)
}
```

## Checklist

Every test should have:
- [ ] WHY comment explaining business reason
- [ ] WHAT comment describing exact behavior
- [ ] Descriptive test function name
- [ ] Clear arrange/act/assert structure
- [ ] Specific assertions (not just "is not null")

## Anti-Patterns

❌ **Don't:**
- Skip documentation ("it's obvious")
- Document implementation instead of behavior
- Use vague language ("tests functionality")
- Only document WHAT without WHY
- Copy-paste documentation between tests

✅ **Do:**
- Always document WHY and WHAT
- Be specific about behavior
- Link to tickets/specs when relevant
- Update docs when test changes
- Make each test's purpose crystal clear
