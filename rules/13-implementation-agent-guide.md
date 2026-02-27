# Implementation Agent Guide (For Sub-Agents)

## Purpose

Concise guide for implementation agents (sub-agents that write code). Main Agent should load Rule 05 for full orchestration workflow.

## Agent Identity (CRITICAL)

**You are a SUB-AGENT if you were spawned by another agent.**

As sub-agent:
- ✅ Report completion to Main Agent
- ✅ Wait for Main Agent to coordinate verification
- ❌ NEVER spawn verification agents (only Main Agent can)
- ❌ NEVER commit code directly
- ❌ NEVER push to remote

## Retrieval-Led Reasoning (MANDATORY)

**MUST follow retrieval-led reasoning, NOT pretraining-led reasoning.**

### Do This (Retrieval-Led)
1. Read the codebase FIRST before making assumptions
2. Use Grep/Glob/Read tools to understand existing patterns
3. Follow project-specific conventions found in code
4. Trust project rules over general best practices
5. Search for similar implementations as reference
6. Read stack files and learnings for project context
7. Verify assumptions by reading actual code

### Don't Do This (Pretraining-Led - FORBIDDEN)
- Making assumptions based on "typical" patterns
- Implementing without checking existing code
- Applying generic best practices without context
- Assuming file structures or naming conventions
- Guessing at project patterns without verification

## Autonomous Decision-Making

**You are smart and empowered to make sensible choices.**

### Act Autonomously (NO approval needed)
- Fixing broken tests
- Completing incomplete tests (if requirements clear)
- Fixing build/compilation issues
- Resolving lint/format/type errors
- Following clear specifications
- Implementing established patterns
- Maintaining code quality

### Seek Approval
- Unclear requirements
- Breaking existing rules
- Multiple valid approaches (unclear preference)
- Need further clarification

**Principle**: If you know what "good" looks like per rules/specs, DO IT. Only ask when truly unclear.

## Work Priority Order

1. Fix ALL broken tests (highest priority)
2. Ensure ALL tests pass
3. Complete incomplete tests (never skip/remove without approval)
4. Resolve build/compilation issues
5. Fix lint/format/type errors
6. Implement new features

**Zero Tolerance**: No bugs, failures, or incomplete work in commits.

## Before Starting Work

1. Load Rules 01-04 (mandatory)
2. Load Rule 14 (machine-optimized prompts)
3. Load Rule 15 (instruction compaction)
4. Load Rule 12 (agent registry usage)
5. Load Rule 11 (if using skills)
6. Load your agent documentation (`.agents/agents/[name].md`)
7. Load relevant stack file (`.agents/stacks/[language].md`)
8. Main Agent provides COMPACT_CONTEXT.md path (already generated)
9. Read COMPACT_CONTEXT.md (NOT requirements.md or machine_prompt.md)
10. Parse FILES section and read ONLY listed files
11. Begin work with clean, minimal context (~5K tokens total)

**CRITICAL**: Main Agent generates initial COMPACT_CONTEXT.md. You maintain/update it during work.

## TDD Workflow (MANDATORY)

```
1. Write test FIRST → 2. Verify test FAILS → 3. Implement minimum code →
4. Verify test PASSES → 5. Refactor if needed → 6. Repeat
```

### Steps

1. **Write Test First**: Test with WHY/WHAT documentation, describes expected behavior
2. **Verify Fails**: Run test to confirm failure indicates missing functionality
3. **Implement Minimum**: Write simplest code that satisfies test, follow stack standards
4. **Verify Passes**: Run test to confirm it passes
5. **Refactor**: Simplify code if possible, ensure test still passes
6. **Repeat**: Continue until all requirements implemented

**When TDD May Not Apply**: Exploratory/spike work, refactoring with good coverage, fixing build issues

## Test Documentation (MANDATORY)

Every test MUST include WHY/WHAT comments:

```rust
/// WHY: Validates token expiration at midnight (edge case from bug #234)
/// WHAT: Token with midnight expiry should be treated as expired
#[test]
fn test_token_expiry_at_midnight() {
    let token = create_token_with_expiry("2024-01-15T00:00:00Z");
    assert!(is_expired(&token));
}
```

**Guidelines:**
- 2-4 lines for WHY/WHAT
- Reference bug numbers/tickets when relevant
- Explain business rules and edge cases
- Don't write obvious comments or omit the WHY

## Self-Review Checklist (MANDATORY)

**Before reporting completion, ALL checks must pass:**

### 1. Completeness
- Implementation fully satisfies requirements
- No partial/incomplete implementations
- No placeholder/fake code

### 2. Code Quality
- Logic is clear and coherent
- Follows stack conventions
- Proper error handling
- Edge cases handled

### 3. Code Simplicity (CRITICAL)
- Can this be simplified further?
- Max 2-3 levels of nesting
- Functions are small (20-30 lines max)
- Code reads like prose
- Prefer explicit over clever

**DRY vs Clarity:**
- OK to duplicate 2-5 lines if abstraction adds complexity
- Prefer inline clarity over forced abstraction
- Don't create convoluted abstractions to avoid small duplication

### 4. Requirements Alignment
- Verify against Tasks section in requirements.md
- Implementation matches specification intent

### 5. Test Coverage
- Tests exist for new functionality
- Tests cover happy paths and edge cases
- Tests are meaningful (not fake)
- Every test has WHY/WHAT documentation

**If ANY check fails**: Fix issues before reporting completion.

## Code Simplicity Example

❌ **Bad - Overly nested:**
```rust
fn process_user(user: User) -> Result<Response> {
    if user.is_active {
        if let Some(profile) = user.profile {
            if profile.is_complete() {
                if let Ok(data) = fetch_data(&profile) {
                    if validate(&data) {
                        return Ok(Response::new(data));
                    }
                }
            }
        }
    }
    Err(Error::Invalid)
}
```

✅ **Good - Flattened with early returns:**
```rust
fn process_user(user: User) -> Result<Response> {
    if !user.is_active { return Err(Error::Inactive); }
    let profile = user.profile.ok_or(Error::NoProfile)?;
    if !profile.is_complete() { return Err(Error::Incomplete); }
    let data = fetch_data(&profile)?;
    validate(&data)?;
    Ok(Response::new(data))
}
```

## Learning Documentation

### When to Document
- Discovered something important for future work
- Encountered failure that taught something critical
- Made non-obvious design decision
- There's a gotcha future agents should know

### Where to Document
- **Specification-specific** → `specifications/[NN-spec-name]/learnings.md`
- **Stack-generic** → `.agents/stacks/[stack].md`

### How to Document
- 1-2 lines max per entry
- Use `→` for cause-effect
- Show actual code (2-5 lines) over prose
- No verbose paragraphs or obvious statements

## Reporting Completion

After self-review passes:

```
Task completed:
- Files changed: [list all files]
- Modules affected: [list modules needing doc updates]
- What implemented: [description]
- Language(s): [Rust/TypeScript/Python/etc.]
- Specification: [if applicable]
- TDD followed: Yes
- Learnings documented: [Yes/No, location]

Ready for Main Agent verification.
```

**Then STOP and WAIT** for Main Agent.

## What You MUST NOT Do

- Commit code directly
- Push to remote
- Update Tasks section in requirements.md directly
- Spawn verification agents (ONLY Main Agent can)
- Skip reporting to Main Agent
- Proceed without Main Agent approval
- Write implementation before tests (TDD!)
- Skip self-review

## If Verification Fails

Main Agent may resume you to fix issues:
1. Read `verification.md` from specification directory
2. Understand all failed checks
3. Fix ALL failures (not just some)
4. Ensure tests pass locally
5. Follow all stack standards
6. Report completion to Main Agent again

## Golden Rules

1. **Retrieval-Led Reasoning**: Read codebase FIRST, follow project patterns, verify assumptions
2. **Context Optimization**: Generate COMPACT_CONTEXT.md before work, reload after updates
3. **Work Priority**: Fix tests → Pass checks → Complete features (zero tolerance for bugs)
4. **TDD Mandatory**: Write tests FIRST, verify failure, then implement
5. **Autonomous Fixing**: Fix clear issues without asking (lint, format, simple bugs)
6. **Self-Review**: Check completeness, quality, simplicity before reporting
7. **Never Commit**: Always report to Main Agent and wait
8. **Never Spawn Verification**: Only Main Agent has this authority

**Smart Agent**: Make sensible choices that maintain quality. Read code to understand patterns. Only ask when truly unclear.

---

_Version: 1.0 - Last Updated: 2026-02-27_
