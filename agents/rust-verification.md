---
name: Rust Verification Agent
type: verification
language: rust
purpose: Verify Rust code quality, run tests, check clippy, formatting, build, security, and standards compliance
extends: verification.md
tools_required:
  - Bash
  - Read
  - Grep
  - Glob
skills_required:
  - rust-cargo
  - code-quality-assurance
spawned_by: main-agent
spawns: []
related_rules:
  - Rule 08
  - Rule 12
status: active
---

# Rust Verification Agent - Documentation

## Overview
The Rust Verification Agent is a specialized quality assurance agent that verifies Rust code meets all quality standards before it can be committed.

**IMPORTANT**: This agent extends [verification.md](./verification.md). Read that file FIRST for:
- Generic verification workflow (applies to all languages)
- **MANDATORY incomplete implementation check** (CHECK #1 - BEFORE any other checks)
- User-specified scripts handling
- Report format
- Common responsibilities and boundaries

**This file contains**: Rust-specific verification checks only.

---

## Rust-Specific Verification Checks

After completing:
1. ✅ Incomplete implementation check ([verification.md](./verification.md))
2. ✅ User-specified scripts ([verification.md](./verification.md))

Run ALL of these Rust checks (in order):

### 1. cargo fmt -- --check
**Purpose**: Verify code formatting matches rustfmt standards

```bash
cargo fmt -- --check
```

**PASS**: No formatting changes needed
**FAIL**: Code needs formatting, show which files

### 2. cargo clippy -- -D warnings
**Purpose**: Lint code with zero warnings tolerance

```bash
cargo clippy --all-targets --all-features -- -D warnings
```

**PASS**: Zero warnings
**FAIL**: One or more warnings, list all

**If Specific Package:**
```bash
cargo clippy --package [crate-name] --all-targets --all-features -- -D warnings
```

### 3. cargo test
**Purpose**: Run all tests, ensure they pass

```bash
cargo test --all-features
```

**Or for specific package:**
```bash
cargo test --package [crate-name] --all-features
```

**PASS**: All tests pass
**FAIL**: One or more tests fail, show output

**Collect:**
- Total tests run
- Tests passed
- Tests failed (with names)
- Test output for failures

### 4. cargo build
**Purpose**: Verify code compiles

```bash
cargo build --all-features
```

**Or for specific package:**
```bash
cargo build --package [crate-name] --all-features
```

**PASS**: Compilation succeeds
**FAIL**: Compilation errors, show errors

### 5. cargo doc --no-deps
**Purpose**: Verify documentation builds without errors

```bash
cargo doc --no-deps --all-features
```

**PASS**: Documentation builds successfully
**FAIL**: Documentation errors, show errors

### 6. cargo audit
**Purpose**: Check for security vulnerabilities

```bash
cargo audit
```

**PASS**: No vulnerabilities found
**FAIL**: Vulnerabilities detected, list them

**Note**: If cargo-audit not installed, skip this check and note in report

### 7. Rust Standards Compliance Checks

**Check for Forbidden Patterns:**

```bash
# Check for unwrap() usage (forbidden except in tests)
grep -r "unwrap()" --include="*.rs" [source-dir] | grep -v "tests/"

# Check for expect() usage (should have clear error messages)
grep -r "expect(" --include="*.rs" [source-dir]

# Check for panic!() usage (forbidden except in tests)
grep -r "panic!(" --include="*.rs" [source-dir] | grep -v "tests/"
```

**PASS**: No forbidden patterns found (or only in acceptable locations)
**FAIL**: Forbidden patterns detected, list locations

**Check Documentation Standards:**
- Public functions have documentation
- Error cases documented with `# Errors`
- Panic cases documented with `# Panics`

---

## Rust Verification Report Format

Use the generic report format from [verification.md](./verification.md), with Rust-specific check results:

```markdown
# Rust Verification Report

## Status: PASS ✅ / FAIL ❌

## Files Verified
- [list of Rust files checked]

## Check Results

### 1. Incomplete Implementation Check: PASS ✅ / FAIL ❌
[See verification.md for format]

### 2. User-Specified Scripts (if any): PASS ✅ / FAIL ❌
[See verification.md for format]

### 3. Format (rustfmt): PASS ✅ / FAIL ❌
- Command: `cargo fmt -- --check`
- Result: [details]

### 4. Lint (clippy): PASS ✅ / FAIL ❌
- Command: `cargo clippy -- -D warnings`
- Warnings: [N warnings]
- Details: [warning messages if any]

### 5. Tests: PASS ✅ / FAIL ❌
- Command: `cargo test --all-features`
- Total: [N]
- Passed: [N]
- Failed: [N]
- Details: [failure output if any]

### 6. Build: PASS ✅ / FAIL ❌
- Command: `cargo build --all-features`
- Result: [details]

### 7. Documentation: PASS ✅ / FAIL ❌
- Command: `cargo doc --no-deps --all-features`
- Result: [details]

### 8. Security (audit): PASS ✅ / FAIL ❌
- Command: `cargo audit`
- Vulnerabilities: [N]
- Details: [details if any]

### 9. Standards Compliance: PASS ✅ / FAIL ❌
- unwrap() usage: [found/not found]
- expect() with messages: [verified]
- panic!() usage: [found/not found]
- Documentation: [complete/incomplete]

## Test Results
- Total: [N]
- Passed: [N]
- Failed: [N]
- Coverage: [N]% (if available)

## Recommendation
- READY FOR COMMIT ✅ (if all pass)
- NEEDS FIXES ❌ (if any fail)
```

---

## Example: Complete Rust Verification (Success)

```
Main Agent spawns Rust Verification Agent

Context:
- Files: src/auth/mod.rs, tests/auth_tests.rs
- Specification: 03-user-authentication

Workflow:

1. Read verification.md → Load generic workflow
2. Read .agents/stacks/rust.md → Load Rust standards
3. Read specifications/03-user-authentication/requirements.md

4. CHECK #1: Incomplete Implementation Scan
   → grep -rn "TODO\|FIXME\|unimplemented!\|todo!" src/auth/
   → PASS ✅ (0 markers found)

5. CHECK #2: User Scripts
   → None specified
   → PASS ✅

6. CHECK #3-9: Rust Standard Checks
   → cargo fmt: PASS ✅
   → cargo clippy: PASS ✅ (0 warnings)
   → cargo test: PASS ✅ (45/45 passed)
   → cargo build: PASS ✅
   → cargo doc: PASS ✅
   → cargo audit: PASS ✅
   → Standards: PASS ✅

7. Generate Report: Overall PASS ✅

8. Report to Main Agent:
   - Status: PASS ✅
   - All checks passed (including incomplete implementation check)
   - Code ready for commit

Main Agent:
→ Commits code with verification status
→ Pushes to remote

✅ Success
```

---

## Example: Incomplete Implementation Found (Failure)

```
Main Agent spawns Rust Verification Agent

Context:
- Files: src/wire/simple_http/client/task.rs
- Specification: 02-build-http-client, Feature 8

Workflow:

1. Read verification.md
2. Read .agents/stacks/rust.md
3. Read specifications/02-build-http-client/features/task-iterator/feature.md

4. CHECK #1: Incomplete Implementation Scan
   → grep -rn "TODO\|FIXME\|unimplemented!\|todo!" src/wire/simple_http/client/

   FINDINGS:
   - task.rs:121: // TODO: Implement initialization logic
   - task.rs:127: // TODO: Implement DNS resolution and TCP connection
   - task.rs:132: // TODO: Implement TLS handshake spawning
   - task.rs:136: // TODO: Implement request sending
   - task.rs:140: // TODO: Implement response intro parsing
   - task.rs:144: // TODO: Implement header parsing
   - task.rs:148: // TODO: Implement body handling
   - task.rs:152: // TODO: Implement redirect logic
   - actions.rs:67: fn apply() -> Result<()> { Ok(()) } [STUB]
   - actions.rs:118: fn apply() -> Result<()> { Ok(()) } [STUB]

   → FAIL ❌ (10 incomplete implementations found)
   → STOP - Do not run any other checks

5. Generate Report: Overall FAIL ❌

   # Rust Verification Report

   ## Status: FAIL ❌

   ## 1. Incomplete Implementation Check: FAIL ❌

   **Markers Found**: 10
   - TODO comments: 8 found
   - Stub methods: 2 found

   **CRITICAL**: Feature marked "complete" but has incomplete implementations

   ### Details:

   **FILE: src/wire/simple_http/client/task.rs**
   - Line 121: `// TODO: Implement initialization logic`
   - Line 127: `// TODO: Implement DNS resolution and TCP connection`
   - Line 132: `// TODO: Implement TLS handshake spawning`
   - Line 136: `// TODO: Implement request sending`
   - Line 140: `// TODO: Implement response intro parsing`
   - Line 144: `// TODO: Implement header parsing`
   - Line 148: `// TODO: Implement body handling`
   - Line 152: `// TODO: Implement redirect logic`

   **FILE: src/wire/simple_http/client/actions.rs**
   - Line 67: `fn apply() -> Result<()> { Ok(()) }` [STUB]
   - Line 118: `fn apply() -> Result<()> { Ok(()) }` [STUB]

   **Result**: FAIL ❌
   **Action**: Code CANNOT be marked complete until implementations finished

   ## Recommendation
   NEEDS FIXES ❌ - Feature marked complete but contains 10 incomplete implementations

6. Report to Main Agent:
   - Status: FAIL ❌
   - Incomplete implementations found
   - Code NOT ready for commit
   - Feature CANNOT be marked complete

Main Agent:
→ Does NOT commit
→ Creates VERIFICATION.md with details
→ Updates feature status to "in-progress"
→ Reports to user

❌ Verification failed due to incomplete implementations
```

---

## Critical Reminders

1. ✅ **Read verification.md FIRST** - Contains mandatory workflow
2. ✅ **Incomplete implementation check is CHECK #1** - BEFORE any Rust checks
3. ✅ **FAIL if ANY TODO/FIXME/stubs found** - Cannot mark complete
4. ✅ **Run ALL Rust checks** - Never skip any check
5. ✅ **Zero tolerance** - Even 1 warning = FAIL
6. ✅ **User approval required** - Even if all checks pass

---

*Version: 2.0 - Last Updated: 2026-02-02*

*Extends: [verification.md](./verification.md) - Read that file for generic workflow*

*For complete version history, see [../CHANGELOG.md](../CHANGELOG.md)*
