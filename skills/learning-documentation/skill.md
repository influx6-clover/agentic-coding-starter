---
name: "Learning Documentation"
description: "How to document learnings in specification-specific locations with proper format"
approved: Yes
created: 2026-02-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "2.0"
  last_updated: "2026-02-27"
  tags: [learning, documentation, knowledge, insights, patterns]
tools: []
files: []
---

# Learning Documentation

## Overview

This skill defines how to document learnings discovered during implementation, focusing on specification-specific insights.

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

## Specification-Specific Learnings

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

## Examples

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

### Example 2: Payment Processing

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
- ❌ It's already documented in language skills
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
- Forget to document important discoveries
- Skip code examples when they clarify

**✅ Do:**
- Keep entries 1-2 lines max
- Focus on non-obvious insights
- Document as you discover (don't wait until end)
- Include 2-5 line code examples

## Summary

**Learnings Location:**
- **Specification-Specific** → `specifications/[spec]/LEARNINGS.md`
  - Critical implementation details for THIS feature
  - Specific to this spec, not generally applicable

**Format:**
- Concise (1-2 lines)
- Use `→` for cause-effect
- Show code (2-5 lines) over prose

**Key Principles:**
1. Document non-obvious discoveries
2. Keep it concise
3. Include code examples
4. Document as you discover
5. Help future agents avoid your mistakes

---

_Version: 2.0 - Last Updated: 2026-02-27_
