---
name: "Learning Documentation"
description: "How to document learnings in specification-specific vs stack-generic locations with proper format"
approved: Yes
created: 2026-02-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-27"
  tags: [learning, documentation, knowledge, insights, patterns]
tools: []
files: []
---

# Learning Documentation

## Overview

This skill defines how to document learnings discovered during implementation, distinguishing between specification-specific insights and stack-generic patterns.

**Usage Type**: EDUCATIONAL - Learn when and how to document learnings effectively.

## When to Use

Document learnings when:
- You discovered something important for future work
- You encountered a failure that taught something critical
- You made a non-obvious design decision
- There's a gotcha future agents should know
- You found a pattern that works well
- You discovered a pitfall to avoid

## Prerequisites

- Understanding of specification structure
- Access to specification directory
- Access to stack files (`.agents/stacks/[language].md`)

## Two Types of Learnings

### 1. Specification-Specific Learnings

**Location**: `specifications/[NN-spec-name]/LEARNINGS.md`

**What to Document:**
- Critical implementation details for THIS feature
- Common failures and fixes specific to this spec
- Testing insights specific to this implementation
- Integration gotchas unique to this feature
- Dependencies and interactions for this spec
- Future considerations for this feature

**Examples:**
```markdown
## Critical Implementation Details
- Auth token validates BEFORE rate limiter (prevents token leakage)
- DB pool: exactly 20 connections (downstream service limit)
- Cache TTL: 5 minutes for user data, 1 hour for static content

## Common Failures and Fixes
- DNS resolution timeout → Retry with exponential backoff (3 attempts)
- Empty response body → Check for 204 status before parsing JSON
- Connection pool exhausted → Added connection timeout of 10s

## Testing Insights
- Integration tests require test HTTP server on localhost:8080
- Mock Stripe API for payment tests (use test keys)
- DNS tests need real network access (skip in offline mode)
```

### 2. Stack-Generic Learnings

**Location**: `.agents/stacks/[language].md` (Learning Log section)

**What to Document:**
- Generic patterns that work across projects
- Common pitfalls for the language
- Testing best practices language-wide
- Tooling tips and configurations
- Language-specific gotchas
- Framework patterns that apply broadly

**Examples:**
```markdown
## Learning Log

### 2026-02-27: Async Error Handling in Rust
**Issue**: Using `?` operator in async functions without proper error propagation
**Learning**: Always define custom error types that implement std::error::Error
**Pattern**:
```rust
#[derive(Debug)]
pub enum ApiError {
    Network(reqwest::Error),
    Parse(serde_json::Error),
}

impl std::error::Error for ApiError {}
```
**New Standard**: All async functions return Result<T, CustomError>

### 2026-02-27: TypeScript Strict Mode Benefits
**Issue**: Found bugs due to implicit any types
**Learning**: Enable strict mode in tsconfig.json catches type errors early
**Corrective Action**: Added "strict": true, fixed all type violations
**New Standard**: All projects use strict mode, no any types allowed
```

## Documentation Format

### Keep It Concise

**✅ Good Format:**
- 1-2 lines max per entry
- Use `→` for cause-effect
- Show actual code (2-5 lines) over prose
- No verbose paragraphs
- No obvious statements

**❌ Bad Format:**
- Long paragraphs explaining obvious things
- No code examples
- Vague descriptions
- Obvious statements like "tests are important"

### Use Clear Sections

**Specification-Specific (`LEARNINGS.md`):**
```markdown
# Learnings: [Specification Name]

## Critical Implementation Details
- [Detail 1]
- [Detail 2]

## Common Failures and Fixes
- [Issue] → [Solution]
- [Issue] → [Solution]

## Testing Insights
- [Insight 1]
- [Insight 2]

## Dependencies and Interactions
- [Component A] depends on [Component B]
- [Integration point with System X]

## Future Considerations
- [Improvement idea]
- [Technical debt to address]
```

**Stack-Generic (`[language].md` Learning Log):**
```markdown
## Learning Log

### [YYYY-MM-DD]: [Title of Learning]
**Issue**: [What went wrong or what was discovered]
**Learning**: [Key insight or lesson]
**Corrective Action**: [What was done to fix/improve]
**New Standard**: [Updated guideline or best practice]
**Pattern** (if applicable):
```language
[2-5 lines of code showing pattern]
```
```

## Decision Tree: Where to Document

```
Ask: Is this learning specific to THIS specification?
├─ YES → specifications/[spec]/LEARNINGS.md
│   Examples:
│   - "Auth token validates before rate limiter" (specific design choice)
│   - "DB pool size is 20 due to downstream limit" (specific constraint)
│   - "Cache TTL: 5min for users, 1hr for static" (specific config)
│
└─ NO → .agents/stacks/[language].md (Learning Log)
    Examples:
    - "Async error handling pattern in Rust" (applies to all Rust code)
    - "TypeScript strict mode catches type errors" (applies to all TS projects)
    - "Test localhost services instead of mocks" (testing philosophy)
```

## Examples

### Example 1: Specification-Specific

**Scenario**: Building HTTP client, discovered DNS caching improves performance

**Document in**: `specifications/02-http-client/LEARNINGS.md`

```markdown
## Critical Implementation Details
- DNS resolver uses LRU cache with 300s TTL → reduces resolution time by 80%
- Cache size: 100 entries (sufficient for typical usage patterns)
- Cache invalidation on network error → prevents stale DNS entries

## Testing Insights
- DNS cache tests require mocking system time (use tokio::time::pause)
- Integration tests validate cache hit/miss with real DNS queries
- Performance tests show 5ms cache hit vs 150ms cache miss
```

**Why Specification-Specific**: This DNS caching is specific to this HTTP client implementation. Other projects may not need DNS caching.

### Example 2: Stack-Generic

**Scenario**: Discovered Tokio task spawning pattern that works well

**Document in**: `.agents/stacks/rust.md` (Learning Log)

```markdown
### 2026-02-27: Tokio Task Spawning Pattern
**Issue**: Tasks were blocking runtime when using blocking I/O
**Learning**: Use tokio::task::spawn_blocking for CPU-heavy or blocking operations
**Pattern**:
```rust
// For async operations
tokio::spawn(async move {
    // async work
});

// For blocking operations
tokio::task::spawn_blocking(move || {
    // blocking work
});
```
**New Standard**: Always use spawn_blocking for blocking I/O, never block async runtime
```

**Why Stack-Generic**: This Tokio pattern applies to all Rust async projects, not just this HTTP client.

### Example 3: Specification-Specific vs Generic

**Scenario**: Implementing payment processing with Stripe API

**Specification-Specific** (`specifications/03-payment/LEARNINGS.md`):
```markdown
## Critical Implementation Details
- Stripe webhook signature verification required (prevents replay attacks)
- Idempotency keys: use transaction_id + timestamp → prevents duplicate charges
- Refund window: 180 days per Stripe policy → validate before refund attempts

## Dependencies and Interactions
- Payment service depends on user-service for account validation
- Webhook endpoint must be publicly accessible (configured in Stripe dashboard)
- Database must support transactions for payment + order update atomicity
```

**Stack-Generic** (`.agents/stacks/typescript.md` Learning Log):
```markdown
### 2026-02-27: Webhook Signature Verification Pattern
**Issue**: Need to verify webhook signatures from external services
**Learning**: Use timing-safe comparison to prevent timing attacks
**Pattern**:
```typescript
import crypto from 'crypto';

function verifyWebhookSignature(payload: string, signature: string, secret: string): boolean {
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  );
}
```
**New Standard**: Always use timing-safe comparison for signature verification
```

## When to Document

### Document Immediately When:
- ✅ You discover a non-obvious solution
- ✅ You fix a bug that was hard to track down
- ✅ You make an important design decision
- ✅ You find a gotcha that wasted time
- ✅ You discover a performance optimization
- ✅ You learn something that would help future agents

### Don't Document When:
- ❌ It's obvious from code comments
- ❌ It's already documented in stack file
- ❌ It's standard practice for the language
- ❌ It's explained in external documentation
- ❌ It's trivial implementation detail

## Reporting to Main Agent

When you document a learning during implementation:

```
Task completed:
- Files changed: [list]
- What implemented: [description]
- Language(s): [Rust/TypeScript/Python]
- Learnings documented: Yes, in specifications/02-http-client/LEARNINGS.md

Key learnings:
- DNS caching with LRU improves performance by 80%
- Cache size 100 entries, 300s TTL optimal for our use case
- Cache invalidation on network error prevents stale entries

Ready for Main Agent verification.
```

## Pitfalls to Avoid

**❌ Don't:**
- Write verbose paragraphs instead of concise points
- Document obvious things everyone knows
- Mix specification-specific with stack-generic learnings
- Forget to document important discoveries
- Skip code examples when they clarify
- Write learnings without date stamps (in Learning Log)

**✅ Do:**
- Keep entries 1-2 lines max
- Focus on non-obvious insights
- Put learnings in correct location (spec vs stack)
- Document as you discover (don't wait until end)
- Include 2-5 line code examples
- Date stamp Learning Log entries

## Summary

**Two Types of Learnings:**
1. **Specification-Specific** → `specifications/[spec]/LEARNINGS.md`
   - Critical implementation details for THIS feature
   - Specific to this spec, not generally applicable

2. **Stack-Generic** → `.agents/stacks/[language].md` (Learning Log)
   - Patterns that work across all projects
   - Language-specific best practices

**Format:**
- Concise (1-2 lines)
- Use `→` for cause-effect
- Show code (2-5 lines) over prose
- Date stamp Learning Log entries

**Decision Rule:**
```
Specific to THIS spec? → specifications/[spec]/LEARNINGS.md
Applies to ALL projects in language? → .agents/stacks/[language].md
```

**Key Principles:**
1. Document non-obvious discoveries
2. Keep it concise
3. Put it in the right location
4. Include code examples
5. Document as you discover
6. Help future agents avoid your mistakes

---

_Version: 1.0 - Last Updated: 2026-02-27_
