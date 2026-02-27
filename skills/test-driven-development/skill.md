---
name: "Test-Driven Development (TDD)"
description: "Complete TDD workflow including test-first development, test documentation, and test quality validation"
approved: Yes
created: 2026-02-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-27"
  tags: [tdd, testing, test-first, quality, workflow]
tools: []
files: []
---

# Test-Driven Development (TDD)

## Overview

This skill defines the mandatory Test-Driven Development workflow that all implementation agents must follow when writing code. TDD ensures tests are written before implementation, validating behavior before code exists.

**Usage Type**: EDUCATIONAL - Learn TDD patterns and implement in your workflow.

## When to Use

Use this skill when:
- Implementing new functionality
- Adding features to existing code
- Writing any code that has testable behavior
- Ensuring code quality through tests

**When TDD May Not Apply:**
- Exploratory/spike work with unclear requirements
- Refactoring code with good existing test coverage
- Fixing build/infrastructure issues
- UI/visual work requiring manual testing

## Prerequisites

- Understanding of testing frameworks for your language
- Access to language stack file (`.agents/stacks/[language].md`)
- Clear requirements for what to implement

## The TDD Cycle

```
1. Write Test FIRST → 2. Verify FAILS → 3. Implement Code →
4. Verify PASSES → 5. Refactor → 6. Repeat
```

### Step 1: Write the Test FIRST

**Before any implementation code:**

1. Write test with WHY/WHAT documentation
2. Test describes expected behavior
3. Test should be specific to one requirement/behavior
4. Use meaningful test names

**Example (Rust):**
```rust
/// WHY: Token must expire at midnight (edge case from security review)
/// WHAT: Token with midnight expiry should be treated as expired
#[test]
fn test_token_expires_at_midnight() {
    let token = create_token_with_expiry("2024-01-15T00:00:00Z");
    assert!(is_expired(&token));
}
```

**Example (TypeScript):**
```typescript
/**
 * WHY: Rate limiter must track per-IP (security requirement)
 * WHAT: Same IP with different users should hit rate limit
 */
test('rate limiter tracks by IP address', async () => {
  const limiter = new RateLimiter({ maxRequests: 3, windowMs: 1000 });

  // Same IP, different users
  await limiter.check('192.168.1.1', 'user1');
  await limiter.check('192.168.1.1', 'user2');
  await limiter.check('192.168.1.1', 'user3');

  // Fourth request from same IP should be rate limited
  await expect(limiter.check('192.168.1.1', 'user4'))
    .rejects.toThrow('Rate limit exceeded');
});
```

**Example (Python):**
```python
def test_password_strength_validation():
    """
    WHY: Password requirements from security policy
    WHAT: Passwords must have 8+ chars, uppercase, lowercase, number, special
    """
    validator = PasswordValidator()

    # Valid password
    assert validator.validate("Str0ng!Pass") == True

    # Too short
    assert validator.validate("Sh0rt!") == False

    # Missing special char
    assert validator.validate("Str0ngPass") == False
```

### Step 2: Verify Test FAILS

**Run the test to confirm it fails:**

1. Execute test command for your language
2. Ensure failure indicates **missing functionality** (not syntax errors)
3. Verify error message is meaningful

**Why This Matters:**
- Confirms test is actually testing something
- If test passes before implementation, test is wrong or feature exists
- Validates test would catch a real bug

**Example Failure Messages:**
```
Rust: thread 'test_token_expires_at_midnight' panicked at 'called `Option::unwrap()` on a `None` value'
TypeScript: Error: Function 'check' not implemented
Python: AttributeError: 'PasswordValidator' object has no attribute 'validate'
```

### Step 3: Implement Minimum Code

**Write simplest code that satisfies the test:**

1. Focus on making the test pass
2. Follow stack standards
3. Don't over-engineer
4. Don't add functionality not tested

**Example (Rust):**
```rust
pub fn is_expired(token: &Token) -> bool {
    let now = Utc::now();
    token.expiry_time <= now
}
```

**Example (TypeScript):**
```typescript
export class RateLimiter {
  private requests: Map<string, number[]> = new Map();

  constructor(private config: { maxRequests: number; windowMs: number }) {}

  async check(ip: string, userId: string): Promise<void> {
    const now = Date.now();
    const requests = this.requests.get(ip) || [];

    // Remove expired requests
    const validRequests = requests.filter(
      time => now - time < this.config.windowMs
    );

    if (validRequests.length >= this.config.maxRequests) {
      throw new Error('Rate limit exceeded');
    }

    validRequests.push(now);
    this.requests.set(ip, validRequests);
  }
}
```

### Step 4: Verify Test PASSES

**Run the test to confirm it now passes:**

1. Execute test command
2. Ensure test passes (green)
3. Verify implementation actually fixed the failure

**Success Output:**
```
Rust: test test_token_expires_at_midnight ... ok
TypeScript: ✓ rate limiter tracks by IP address (15ms)
Python: test_password_strength_validation PASSED
```

### Step 5: Refactor If Needed

**Improve code while keeping test green:**

1. Simplify code if possible
2. Apply DRY where it improves clarity
3. Improve naming
4. Ensure test still passes after changes

**Refactoring Example:**
```rust
// Before refactoring
pub fn is_expired(token: &Token) -> bool {
    let now = Utc::now();
    token.expiry_time <= now
}

// After refactoring (clearer intent)
pub fn is_expired(token: &Token) -> bool {
    token.expiry_time <= Utc::now()
}
```

### Step 6: Repeat Cycle

Continue until all requirements implemented:
1. Write next test
2. Verify it fails
3. Implement code
4. Verify it passes
5. Refactor
6. Repeat

## Test Documentation (MANDATORY)

Every test MUST include WHY/WHAT comments:

### Format

```
WHY: [Explains business reason, edge case, or requirement]
WHAT: [Describes specific behavior being tested]
```

### Guidelines

**✅ Good Documentation:**
- 2-4 lines for WHY/WHAT
- Reference bug numbers/tickets when relevant
- Explain business rules and edge cases
- Connect test to real-world scenarios

**❌ Bad Documentation:**
- No documentation
- Obvious comments ("tests addition")
- Missing the WHY
- Vague WHAT

### Examples

**Good (Rust):**
```rust
/// WHY: DNS resolution can fail due to network issues (bug #234)
/// WHAT: Client should retry 3 times with exponential backoff before failing
#[test]
fn test_dns_retry_on_failure() {
    // Test implementation
}
```

**Good (TypeScript):**
```typescript
/**
 * WHY: Cart total must include tax and shipping (accounting requirement)
 * WHAT: Total calculation should be: subtotal + tax + shipping
 */
test('calculates correct cart total with tax and shipping', () => {
  // Test implementation
});
```

**Bad:**
```rust
/// Test token expiration
#[test]
fn test_token_expiry() { }  // ❌ No WHY, vague WHAT
```

## Test Quality Validation

### Valid Test Usage

**✅ Tests must validate real code behavior:**
- Unit tests with real components (localhost, temp files)
- Integration tests with real local services (test servers, test DBs)
- End-to-end tests with full workflows
- Limited mocks only for external services (payment gateways, third-party APIs)

### Invalid Test Usage

**❌ Tests must NOT be integration theater:**
- Mocking our own code (HTTP clients, databases we wrote)
- Integration tests without integration (all external calls mocked)
- Mock-only testing (no real component validation)
- Untested integration points

### Examples

**❌ Bad - Integration Theater:**
```rust
#[test]
fn test_http_client() {
    let mock_dns = MockDnsResolver::new();
    let mock_tcp = MockTcpConnection::new();
    let client = HttpClient::new(mock_dns, mock_tcp);

    assert!(client.get("http://example.com").is_ok());
}
// ❌ Mocking our own DNS and TCP - not testing real integration
```

**✅ Good - Real Integration:**
```rust
#[tokio::test]
async fn test_http_client_real_integration() {
    // Start real test HTTP server on localhost
    let server = TestHttpServer::new("127.0.0.1:8080");
    server.respond_with(200, "OK");

    // Test with real client using real DNS and TCP
    let client = HttpClient::new();
    let response = client.get("http://127.0.0.1:8080").await.unwrap();

    assert_eq!(response.status(), 200);
    assert_eq!(response.body(), "OK");
}
// ✅ Tests real HTTP client with real server
```

**✅ Good - Valid Mock (External Service):**
```typescript
test('payment processing with Stripe', async () => {
  // Mock external Stripe API (we don't control this)
  const stripeMock = createStripeMock();
  stripeMock.charges.create.mockResolvedValue({ id: 'ch_123', status: 'succeeded' });

  // Test our payment processor with real logic
  const processor = new PaymentProcessor(stripeMock);
  const result = await processor.charge({ amount: 1000, currency: 'usd' });

  expect(result.success).toBe(true);
  expect(result.chargeId).toBe('ch_123');
});
// ✅ Mocking external service (Stripe), testing our logic
```

## TDD Benefits

1. **Tests prove code works** before implementation
2. **Tests document requirements** as executable specifications
3. **Prevents over-engineering** (only write what's tested)
4. **Catches regressions** immediately
5. **Makes refactoring safer** (tests catch breakage)
6. **Improves design** (testable code is better designed)

## TDD Enforcement

### User Will Shout If:

**❌ VIOLATION:**
- Writing implementation before tests
- Not verifying tests fail first
- Skipping test documentation
- Using integration theater (mocking own code)
- Incomplete test coverage

**✅ CORRECT:**
- Writing test first
- Verifying red → green cycle
- Documenting WHY/WHAT
- Testing real behavior
- Complete coverage of requirements

## Common Patterns

### Pattern: Feature with Multiple Requirements

```
Requirement 1: User login
  1. Write test for valid credentials → RED
  2. Implement login logic → GREEN
  3. Refactor if needed → GREEN

Requirement 2: User login with invalid credentials
  1. Write test for invalid credentials → RED
  2. Add error handling → GREEN
  3. Refactor if needed → GREEN

Requirement 3: User login rate limiting
  1. Write test for rate limit → RED
  2. Add rate limiting → GREEN
  3. Refactor if needed → GREEN
```

### Pattern: Edge Case Testing

```
1. Write test for happy path → RED → Implement → GREEN
2. Write test for edge case 1 → RED → Handle case → GREEN
3. Write test for edge case 2 → RED → Handle case → GREEN
4. Write test for error case → RED → Handle error → GREEN
5. Refactor all handling → GREEN
```

### Pattern: Refactoring with TDD Safety

```
1. Existing tests all pass → GREEN
2. Refactor code (improve design, simplify)
3. Run tests again → GREEN
4. If RED: Revert and fix
5. If GREEN: Commit refactoring
```

## Pitfalls to Avoid

**❌ Don't:**
- Write implementation before tests
- Skip verifying test failure
- Write tests without documentation
- Mock your own code
- Skip edge case testing
- Write obvious/trivial tests
- Ignore failed tests

**✅ Do:**
- Always write test first
- Always verify red → green cycle
- Document WHY/WHAT for every test
- Test real behavior
- Cover edge cases and errors
- Test meaningful behavior
- Fix all failing tests immediately

## Summary

**TDD Workflow:**
```
Write Test → Verify Fails → Implement → Verify Passes → Refactor → Repeat
```

**Test Documentation:**
```
WHY: [Business reason, edge case, requirement]
WHAT: [Specific behavior being tested]
```

**Test Quality:**
- Real tests over mocks
- Integration tests with real components
- Mock only external services
- Complete coverage of requirements

**Key Principles:**
1. Test first, code second
2. Red → Green → Refactor
3. Document every test
4. Test real behavior
5. One test per requirement
6. Fix failures immediately

---

_Version: 1.0 - Last Updated: 2026-02-27_
