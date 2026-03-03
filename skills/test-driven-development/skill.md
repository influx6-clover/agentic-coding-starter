---
name: "Test-Driven Development (TDD)"
description: "Complete TDD workflow: ONE test at a time, test-first, finish before moving to next"
approved: Yes
created: 2026-02-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "3.0-streamlined"
  last_updated: "2026-03-03"
  tags: [tdd, testing, test-first, quality, workflow, one-at-a-time]
tools: []
files:
  - examples/tdd-workflow-examples.md: "Complete TDD cycle examples in Rust, TypeScript, Python"
  - examples/tdd-patterns.md: "Common patterns for features, edge cases, refactoring"
  - examples/test-documentation.md: "WHY/WHAT documentation standards and templates"
---

# Test-Driven Development (TDD)

## When to Use This Skill

**Read when:** Writing implementation code with tests.

**Referenced by:** Implementation Agent (`.agents/agents/implementation.md`)

---

## 🎯 Critical Rule: ONE Test at a Time 🚨

**⚠️ MANDATORY - NON-NEGOTIABLE ⚠️**

Work on **ONE** test at a time. Finish it **completely** before moving to the next test.

**This is the MOST IMPORTANT rule in TDD.**

### The Cycle (ONE at a time)

```
🔴 ONE TEST: Write → Verify FAILS → Implement → Verify PASSES → Refactor
                              ↓
🔴 NEXT TEST: Write → Verify FAILS → Implement → Verify PASSES → Refactor
                              ↓
🔴 NEXT TEST: Write → Verify FAILS → Implement → Verify PASSES → Refactor
```

### ❌ NEVER Do This (FORBIDDEN)
- ❌ Write multiple tests at once
- ❌ Generate test file with all tests
- ❌ Write implementation for multiple tests simultaneously
- ❌ Skip ahead to other tests before current one passes
- ❌ Plan out 10 tests and write them all
- ❌ Copy-paste test template with TODO comments

### ✅ ALWAYS Do This (MANDATORY)
1. ✅ Write **ONE** test (just one!)
2. ✅ Verify it **FAILS** (red)
3. ✅ Implement **minimum** code to pass **THAT** test
4. ✅ Verify it **PASSES** (green)
5. ✅ Refactor if needed (while staying green)
6. ✅ **ONLY THEN** move to **NEXT** test
7. ✅ Repeat: ONE test at a time

**Why ONE at a time:**
- ✅ **Focus**: Single behavior, no distractions
- ✅ **Validation**: Each test proves the last code works
- ✅ **Debugging**: Know exactly what broke
- ✅ **Progress**: Concrete progress with each passing test
- ✅ **Design**: Better API design from incremental feedback
- ✅ **Safety**: Tests catch regressions immediately

---

## 📖 The TDD Workflow

### Step 1: Write the Test FIRST

**Before any implementation code:**

```rust
/// WHY: Token must expire at midnight (edge case from security review)
/// WHAT: Token with midnight expiry should be treated as expired
#[test]
fn test_token_expires_at_midnight() {
    let token = create_token_with_expiry("2024-01-15T00:00:00Z");
    assert!(is_expired(&token));
}
```

### Step 2: Verify Test FAILS

Run test to confirm it fails (proves test is valid):

```bash
cargo test test_token_expires_at_midnight
# Should fail: function doesn't exist yet
```

### Step 3: Implement Minimum Code

Write just enough code to pass THIS test:

```rust
pub fn is_expired(token: &Token) -> bool {
    let now = Utc::now();
    token.expires_at <= now
}
```

### Step 4: Verify Test PASSES

```bash
cargo test test_token_expires_at_midnight
# Should pass: implementation now correct
```

### Step 5: Refactor If Needed

Improve code structure (tests stay green):

```rust
pub fn is_expired(token: &Token) -> bool {
    is_past_expiry(token.expires_at)
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

📖 **Complete examples:** [`tdd-workflow-examples.md`](examples/tdd-workflow-examples.md) - Rust, TypeScript, Python

---

## 📝 Test Documentation (MANDATORY)

**Every test MUST have WHY and WHAT:**

```rust
/// WHY: <business reason, requirement, or bug>
/// WHAT: <specific behavior being tested>
#[test]
fn test_name() { }
```

**Why this matters:**
- Future developers understand purpose
- Links to requirements/specs
- Documents business rules
- Makes tests maintainable

📖 **Complete guide:** [`test-documentation.md`](examples/test-documentation.md) - Templates and examples

---

## ✅ Valid Test Usage

**Good tests:**
1. **Descriptive name** - Explains what is being tested
2. **WHY/WHAT docs** - Business context and behavior
3. **Specific assertions** - Check exact expected values
4. **One behavior** - Tests single requirement/case
5. **Independent** - Doesn't depend on other tests

```rust
/// WHY: Security requirement from audit
/// WHAT: Admin role should have all permissions
#[test]
fn test_admin_has_all_permissions() {
    let admin = create_admin_user();
    assert!(admin.has_permission(Permission::Read));
    assert!(admin.has_permission(Permission::Write));
    assert!(admin.has_permission(Permission::Delete));
}
```

---

## ❌ Invalid Test Usage

**Bad tests:**
1. **No documentation** - No WHY/WHAT
2. **Vague assertions** - `assert!(result)` without checking what
3. **Multiple behaviors** - Tests 5 things in one test
4. **Muted variables** - `let _result = ...` without assertions
5. **Empty body** - `#[test] fn test_something() { }`

```rust
// ❌ BAD - No docs, vague assertion
#[test]
fn test_user() {
    let user = User::new();
    assert!(user.id > 0); // What are we really testing?
}
```

---

## 🔍 Common Patterns (Read When Needed)

**When you need to:**

1. **Build feature with multiple requirements** → [`tdd-patterns.md#feature-with-multiple-requirements`](examples/tdd-patterns.md)
2. **Test edge cases** → [`tdd-patterns.md#edge-case-testing`](examples/tdd-patterns.md)
3. **Refactor safely** → [`tdd-patterns.md#refactoring-with-tdd-safety`](examples/tdd-patterns.md)
4. **Build complex algorithms** → [`tdd-patterns.md#building-complex-algorithms`](examples/tdd-patterns.md)
5. **Test different data scenarios** → [`tdd-patterns.md#data-driven-development`](examples/tdd-patterns.md)
6. **Build error handling** → [`tdd-patterns.md#error-handling-development`](examples/tdd-patterns.md)

---

## ⚠️ Common Pitfalls

**Avoid these mistakes:**

1. **Writing all tests first** → Write ONE test, implement, then next
2. **Skipping failure verification** → Always verify test fails first
3. **Over-implementing** → Write minimum code to pass current test
4. **Poor test names** → Use descriptive names explaining behavior
5. **Missing WHY/WHAT** → Always document business context
6. **Testing implementation** → Test behavior, not internal details
7. **Dependent tests** → Each test should run independently

---

## 🎯 TDD Benefits

**Why TDD works:**
- ✅ **Better design** - Writing tests first improves API design
- ✅ **Safety net** - Tests catch regressions immediately
- ✅ **Documentation** - Tests document expected behavior
- ✅ **Confidence** - Know code works as expected
- ✅ **Incremental** - Small steps prevent overwhelm
- ✅ **Focus** - One test = one requirement at a time

---

## 📋 TDD Checklist

Every test should have:
- [ ] Written BEFORE implementation
- [ ] WHY/WHAT documentation
- [ ] Verified it FAILS first
- [ ] Minimum implementation to pass
- [ ] Verified it PASSES
- [ ] Refactored if needed
- [ ] One test finished before starting next

---

## 🔗 Related Skills

- [Rust Testing Excellence](../rust-clean-code/testing/skill.md) - Rust-specific testing patterns
- [Implementation Practices](../implementation-practices/skill.md) - General implementation guidelines
