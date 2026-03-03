# TDD Workflow Examples

This document provides complete examples of the TDD cycle across different languages.

## The TDD Cycle

```
ONE TEST:
Write Test → Verify FAILS → Implement Code → Verify PASSES → Refactor

THEN NEXT TEST:
Write Test → Verify FAILS → Implement Code → Verify PASSES → Refactor

THEN NEXT TEST:
...
```

## Complete Example: Token Validation (Rust)

### Step 1: Write Test FIRST

```rust
/// WHY: Token must expire at midnight (edge case from security review)
/// WHAT: Token with midnight expiry should be treated as expired
#[test]
fn test_token_expires_at_midnight() {
    let token = create_token_with_expiry("2024-01-15T00:00:00Z");
    assert!(is_expired(&token));
}
```

### Step 2: Verify FAILS

```bash
cargo test test_token_expires_at_midnight
# Should fail: is_expired function doesn't exist yet
```

### Step 3: Implement Minimum Code

```rust
pub fn is_expired(token: &Token) -> bool {
    let now = Utc::now();
    token.expires_at <= now
}
```

### Step 4: Verify PASSES

```bash
cargo test test_token_expires_at_midnight
# Should pass: is_expired now handles midnight correctly
```

### Step 5: Refactor (if needed)

```rust
// Add helper for clarity
pub fn is_expired(token: &Token) -> bool {
    is_past_expiry(token.expires_at)
}

fn is_past_expiry(expiry: DateTime<Utc>) -> bool {
    Utc::now() >= expiry
}
```

### Step 6: Move to NEXT Test

```rust
/// WHY: Tokens with null expiry should never expire (spec requirement)
/// WHAT: Token without expiry field should be treated as valid
#[test]
fn test_token_without_expiry_never_expires() {
    let token = create_token_without_expiry();
    assert!(!is_expired(&token));
}
```

## Complete Example: Rate Limiter (TypeScript)

### Step 1: Write Test FIRST

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

  // Fourth request from same IP should fail
  await expect(limiter.check('192.168.1.1', 'user4'))
    .rejects.toThrow('Rate limit exceeded');
});
```

### Step 2: Verify FAILS

```bash
npm test
# Should fail: RateLimiter doesn't exist yet
```

### Step 3: Implement Minimum Code

```typescript
export class RateLimiter {
  private requests: Map<string, number[]> = new Map();

  constructor(private config: { maxRequests: number; windowMs: number }) {}

  async check(ip: string, userId: string): Promise<void> {
    const now = Date.now();
    const requests = this.requests.get(ip) || [];

    // Filter requests within window
    const recentRequests = requests.filter(
      time => now - time < this.config.windowMs
    );

    if (recentRequests.length >= this.config.maxRequests) {
      throw new Error('Rate limit exceeded');
    }

    recentRequests.push(now);
    this.requests.set(ip, recentRequests);
  }
}
```

### Step 4: Verify PASSES

```bash
npm test
# Should pass: Rate limiter now tracks by IP
```

### Step 5: Refactor (if needed)

```typescript
export class RateLimiter {
  private requests: Map<string, number[]> = new Map();

  constructor(private config: { maxRequests: number; windowMs: number }) {}

  async check(ip: string, userId: string): Promise<void> {
    const recentRequests = this.getRecentRequests(ip);

    if (this.isRateLimited(recentRequests)) {
      throw new Error('Rate limit exceeded');
    }

    this.recordRequest(ip, recentRequests);
  }

  private getRecentRequests(ip: string): number[] {
    const now = Date.now();
    const requests = this.requests.get(ip) || [];
    return requests.filter(time => now - time < this.config.windowMs);
  }

  private isRateLimited(recentRequests: number[]): boolean {
    return recentRequests.length >= this.config.maxRequests;
  }

  private recordRequest(ip: string, recentRequests: number[]): void {
    recentRequests.push(Date.now());
    this.requests.set(ip, recentRequests);
  }
}
```

### Step 6: Move to NEXT Test

```typescript
/**
 * WHY: Different IPs should have independent limits
 * WHAT: Two different IPs should each have their own rate limit
 */
test('different IPs have independent rate limits', async () => {
  const limiter = new RateLimiter({ maxRequests: 2, windowMs: 1000 });

  // IP 1 uses its limit
  await limiter.check('192.168.1.1', 'user1');
  await limiter.check('192.168.1.1', 'user2');

  // IP 2 should still work (independent limit)
  await expect(limiter.check('192.168.1.2', 'user3'))
    .resolves.not.toThrow();
});
```

## Complete Example: User Registration (Python)

### Step 1: Write Test FIRST

```python
def test_register_user_with_valid_email():
    """
    WHY: Email validation prevents spam accounts
    WHAT: Valid email format should create user successfully
    """
    user_service = UserService()
    result = user_service.register("alice@example.com", "password123")

    assert result.success is True
    assert result.user.email == "alice@example.com"
```

### Step 2: Verify FAILS

```bash
pytest test_user_service.py::test_register_user_with_valid_email
# Should fail: UserService doesn't exist yet
```

### Step 3: Implement Minimum Code

```python
from dataclasses import dataclass
import re

@dataclass
class User:
    email: str

@dataclass
class Result:
    success: bool
    user: User | None = None

class UserService:
    def register(self, email: str, password: str) -> Result:
        if not self._is_valid_email(email):
            return Result(success=False)

        user = User(email=email)
        return Result(success=True, user=user)

    def _is_valid_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
```

### Step 4: Verify PASSES

```bash
pytest test_user_service.py::test_register_user_with_valid_email
# Should pass: User registration now validates email
```

### Step 5: Refactor (if needed)

```python
# Extract email validator
class EmailValidator:
    @staticmethod
    def is_valid(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

class UserService:
    def __init__(self):
        self.validator = EmailValidator()

    def register(self, email: str, password: str) -> Result:
        if not self.validator.is_valid(email):
            return Result(success=False)

        user = User(email=email)
        return Result(success=True, user=user)
```

### Step 6: Move to NEXT Test

```python
def test_register_user_with_invalid_email():
    """
    WHY: Invalid emails should be rejected immediately
    WHAT: Registration with invalid email should fail gracefully
    """
    user_service = UserService()
    result = user_service.register("not-an-email", "password123")

    assert result.success is False
    assert result.user is None
```

## Key Principles Demonstrated

1. **One test at a time** - Each example shows completing one test before moving to next
2. **Test first** - Test is written before implementation exists
3. **Verify fails** - Run test to see it fail (confirms test is valid)
4. **Minimum code** - Implement just enough to pass the current test
5. **Verify passes** - Run test to see it pass
6. **Refactor** - Improve code structure while tests keep passing
7. **Next test** - Move to next requirement/behavior

## Why This Works

✅ **Focus** - One behavior at a time prevents overwhelm
✅ **Validation** - Seeing failure confirms test is valid
✅ **Progress** - Each passing test is concrete progress
✅ **Safety** - Tests catch regressions immediately
✅ **Design** - Writing tests first improves API design
