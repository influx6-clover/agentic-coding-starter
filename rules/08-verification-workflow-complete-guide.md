# Verification Workflow - Complete Integration Guide

## Purpose

Comprehensive guide to iron-clad verification workflow ensuring **NO code is EVER committed without passing ALL quality checks**. **ZERO TOLERANCE** for violations.

Integrates verification workflow from Rules 03, 04, 05, 07 and all stack files.

## Core Principle

```
Task Complete → Report → Verify → Pass? → Commit → Push
                             ↓
                           Fail → Fix → Loop
```

**CRITICAL:**
- Code commits ONLY after task complete + verification passes
- Implementation agents NEVER commit directly
- ONLY Main Agent can spawn verification agents

## Agent Hierarchy

**Main Agent** (Top of hierarchy):
- ✅ Directly interacting with user
- ✅ **ONLY agent with authority to spawn verification agents**
- ✅ Spawns: Implementation, Specification, Verification agents

**Sub-Agents**:
- ❌ **NEVER spawn verification agents**
- ✅ Report completion to Main Agent
- ✅ Wait for Main Agent to orchestrate verification

**Identity Rule**: If you were spawned by another agent → You are a SUB-AGENT (no verification authority)

## The Four-Phase Workflow

### Phase 1: Implementation

Implementation agent:
1. Implements code following all documented standards
2. Writes tests for new functionality
3. Tracks changes made
4. **REPORTS to Main Agent** (changed files, description, language(s))
5. **STOPS and WAITS**
6. ❌ DOES NOT commit, push, update tasks.md, or spawn verification

### Phase 2: Mandatory Verification

Main Agent:
1. Analyzes changed files to identify language(s)
2. Spawns **ONE verification agent per language stack**
3. Verification agent runs **ALL checks** from stack file

**Incomplete Implementation Check** (MANDATORY FIRST):
1. Search for: `TODO`, `FIXME`, `unimplemented!()`, `todo!()`, `panic!("not implemented")`
2. Check for stub methods (functions returning default/Ok(()) only)
3. Verify all public methods have real implementations
4. If ANY incomplete → **FAIL IMMEDIATELY**

**Per Language Checks:**

**Rust** (from `.agents/stacks/rust.md`):
1. Incomplete implementation check (MANDATORY)
2. `cargo fmt -- --check`
3. `cargo clippy -- -D warnings`
4. `cargo test`
5. `cargo build --all-features`
6. `cargo doc --no-deps`
7. `cargo audit`
8. Standards compliance (no unwrap(), proper docs)

**JavaScript/TypeScript** (from `.agents/stacks/javascript.md`):
1. Incomplete implementation check (MANDATORY)
2. `npx prettier --check .`
3. `npx tsc --noEmit`
4. `npx eslint . --max-warnings 0`
5. `npm test` (with coverage)
6. `npm run build`
7. `npm audit`
8. Standards compliance (no `any` type)

**Python** (from `.agents/stacks/python.md`):
1. Incomplete implementation check (MANDATORY)
2. `black --check .`
3. `ruff check .`
4. `mypy .` (strict mode)
5. `pytest --cov`
6. `python -m py_compile src/**/*.py`
7. `pip-audit` or `bandit`
8. Standards compliance (no mutable defaults)

**Test Quality Check (MANDATORY):**

Tests must validate real code behavior, not mock behavior.

**Valid Test Usage:**
- ✅ Unit tests with real components (localhost, temp files)
- ✅ Integration tests with real local services (test servers, test DBs)
- ✅ End-to-end tests with full workflows
- ✅ Limited mocks only for external services (payment gateways, third-party APIs)

**Invalid Test Usage (FAIL):**
- ❌ Mocking our own code (HTTP clients, databases we wrote)
- ❌ Integration tests without integration (all external calls mocked)
- ❌ Mock-only testing (no real component validation)
- ❌ Untested integration points

**Verification Report Format:**
```markdown
# [Language] Verification Report

## Status: PASS ✅ / FAIL ❌

## Files Verified
- [list]

## Check Results
1. Incomplete Implementation: PASS/FAIL
2. Format: PASS/FAIL
3. Lint: PASS/FAIL
4. Type Check: PASS/FAIL
5. Tests: PASS/FAIL ([N] passed, [N] failed)
6. Build: PASS/FAIL
7. Security: PASS/FAIL
8. Standards: PASS/FAIL

## Test Results
- Total: [N] | Passed: [N] | Failed: [N] | Coverage: [N]%

## Failures (if any)
[Details for each failed check]
```

### Phase 3: Main Agent Decision

**If ALL Checks PASS ✅:**
1. Main Agent: `git add [files]`
2. Main Agent: `git commit -m "[message with verification status]"`
3. Main Agent: `git push`
4. Update tasks.md (mark task complete)
5. Proceed to next task

**If ANY Check FAILS ❌:**
1. Main Agent creates urgent fix task
2. Main Agent spawns/resumes implementation agent with fix instructions
3. Implementation agent fixes ALL failures
4. Implementation agent reports completion
5. Return to Phase 2 (verify again)
6. Loop until all checks pass

### Phase 4: Documentation Updates (Optional)

If modules changed, Main Agent may:
1. Spawn documentation agent
2. Documentation agent updates affected module docs
3. Verification runs on doc changes
4. Commit doc updates

## Commit Message Format (with Verification)

```bash
git commit -m "$(cat <<'EOF'
Add authentication middleware

Implemented JWT-based authentication middleware to secure API endpoints.

Changes made:
- Created auth.js middleware with token validation
- Added JWT verification using jsonwebtoken
- Implemented error handling for invalid tokens
- Wrote comprehensive test suite

Verified by JavaScript Verification Agent: All checks passed
- Format: PASS (prettier)
- Lint: PASS (eslint, 0 warnings)
- Type Check: PASS (tsc)
- Tests: 12/12 PASS, coverage 95%
- Build: PASS
- Security: PASS (audit, 0 vulnerabilities)
- Standards: PASS

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Specification Versioning

**From Rule 06:** Completed specifications are **IMMUTABLE**.

**Before updating any specification:**
1. Read `specifications/NN-spec-name/requirements.md` frontmatter
2. Check status: is it "completed"?
3. Check for REPORT.md and VERIFICATION.md existence

**If COMPLETED:**
- ❌ DO NOT update
- ✅ CREATE new specification (use `builds_on` field)

**If IN-PROGRESS:**
- ✅ Can update tasks.md as normal

## Enforcement

### Zero Tolerance Violations

**CRITICAL VIOLATIONS:**
1. Committing code without verification
2. Sub-agent spawning verification agents
3. Committing with failed verification
4. Skipping any required checks
5. Using mock-only testing
6. Committing incomplete implementations (TODO, FIXME, stubs)

**Consequences:**
1. Code rejected immediately
2. Must fix all issues
3. Re-run complete verification
4. Document violation in Learning Log
5. Report violation to user

### Mandatory Requirements

**Must Do:**
1. Run ALL checks from stack file
2. Check for incomplete implementations FIRST
3. Validate test quality (real vs mock)
4. Main Agent spawns verification agents
5. Include verification status in commits
6. Fix ALL failures before commit
7. Push after successful commit

**Must Not Do:**
1. Skip any verification checks
2. Commit with incomplete implementations
3. Use mock-only testing
4. Sub-agents spawn verification
5. Commit before verification passes
6. Ignore failed checks

## Integration with Other Rules

- **Rule 03 (Dangerous Operations)**: Git checkpoint required before dangerous operations
- **Rule 04 (Commit and Push)**: Verification required before all code commits
- **Rule 05 (Agent Orchestration)**: Main Agent orchestrates verification workflow
- **Rule 07 (Language Standards)**: Stack files define verification requirements
- **Rule 06 (Specifications)**: Completed specs are immutable

## Summary

**Golden Rules:**
1. **NO code committed without verification** (ZERO TOLERANCE)
2. **ONLY Main Agent spawns verification agents**
3. **ALL checks must pass** (format, lint, type, tests, build, security, standards)
4. **Check incomplete implementations FIRST** (TODO, FIXME, stubs)
5. **Real tests over mocks** (test actual behavior, not mock setup)
6. **Fix ALL failures** (loop until pass)
7. **Include verification status in commits**

**Workflow:**
```
Implement → Report → Main Agent → Spawn Verification →
Run ALL Checks → PASS? → Commit + Push : Fix → Loop
```

---

_Version: 1.0 - Last Updated: 2026-02-27_
