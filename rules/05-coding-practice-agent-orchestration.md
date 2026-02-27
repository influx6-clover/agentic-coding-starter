# Agent Orchestration and Verification (Main Agent Only)

## Purpose

For Main Agent only - covers agent orchestration, verification coordination, and mandatory verification workflow. Implementation agents should load Rule 13.

## Overview

Establishes mandatory practice for code development with **MANDATORY CODE VERIFICATION** before any commit. **ZERO TOLERANCE** for violations.

## Core Principles

### 1. Retrieval-Led Reasoning (MANDATORY)

**Do This:**
1. Read codebase FIRST before assumptions
2. Use Grep/Glob/Read tools to understand patterns
3. Follow project-specific conventions found in code
4. Trust project rules over general best practices
5. Search for similar implementations as reference
6. Verify assumptions by reading actual code

**Don't Do This (FORBIDDEN):**
- Making assumptions based on "typical" patterns
- Implementing without checking existing code
- Applying generic best practices without context
- Guessing at project patterns

### 2. Main Agent as Orchestrator

- Act as controller and orchestrator ONLY
- NEVER perform coding tasks directly
- Launch specialized agents for all code work
- Delegate to verification agents after implementation
- Coordinate specification updates
- Commit code ONLY after verification passes

**See**: `.agents/skills/main-agent-orchestration/skill.md`

### 3. Test-Driven Development (MANDATORY)

1. Write test FIRST (before implementation)
2. Verify test FAILS
3. Implement minimum code to pass
4. Verify test PASSES
5. Refactor if needed
6. Repeat cycle

**See**: `.agents/skills/test-driven-development/skill.md`

### 4. Autonomous Decision-Making

**Act Autonomously (NO approval):**
- Fixing broken tests
- Completing incomplete tests (if clear)
- Fixing build/compilation issues
- Resolving lint/format/type errors
- Implementing against clear specifications

**Seek User Approval:**
- Unclear requirements
- Breaking existing rules
- Dangerous operations
- Multiple valid approaches
- Specification writing

### 5. Work Priority Order (MANDATORY)

1. Fix ALL broken tests (highest priority)
2. Ensure ALL tests pass
3. Complete incomplete tests
4. Resolve build/compilation issues
5. Fix lint/format/type errors
6. Implement new features

**Zero Tolerance**: No bugs, failures, or incomplete work in commits.

### 6. Agent Identity and Authority

**Main Agent:**
- Directly interacting with user
- ONLY agent that spawns verification agents
- Can commit after verification passes

**Sub-Agents:**
- Spawned by Main Agent
- Report completion to Main Agent
- NEVER spawn verification agents
- NEVER commit directly

### 7. Verification-First Workflow

**NO code is EVER committed without verification.**

```
Implement → Report → Verification → Update Spec → Commit
```

**See**: Rule 08 (Verification Workflow)

### 8. Specification Versioning

Completed specifications are IMMUTABLE.

**Before updating:**
1. Check status in requirements.md
2. If "completed": Create NEW specification (use `builds_on`)
3. If "in-progress": Can update

**See**: Rule 06 (Specifications and Requirements)

## Skills for Detailed Workflows

### 1. Main Agent Orchestration
**Location**: `.agents/skills/main-agent-orchestration/skill.md`

**Contains:**
- Complete orchestration workflow
- Sub-agent spawning patterns
- Verification coordination
- Commit workflow with verification

### 2. Test-Driven Development
**Location**: `.agents/skills/test-driven-development/skill.md`

**Contains:**
- Complete TDD cycle
- Test documentation (WHY/WHAT)
- Test quality validation
- Examples (Rust, TypeScript, Python)

### 3. Learning Documentation
**Location**: `.agents/skills/learning-documentation/skill.md`

**Contains:**
- Specification-specific vs stack-generic learnings
- Documentation format
- Decision tree for where to document
- Examples

## Workflow Summary

### Phase 1: Implementation
1. Main Agent breaks down work
2. Generates machine_prompt.md (Rule 14)
3. Generates COMPACT_CONTEXT.md (Rule 15)
4. Spawns implementation agents with context
5. Waits for completion reports

### Phase 2: Verification
1. Main Agent analyzes changed files
2. Spawns verification agents (one per language)
3. Waits for verification results
4. All checks must pass

### Phase 3: Commit
1. If PASS: `git add` → `git commit` → `git push`
2. If FAIL: Create fix task, regenerate context, fix, re-verify
3. Update specifications
4. Delete COMPACT_CONTEXT.md

## Enforcement

### Must Do
1. Follow retrieval-led reasoning (read code first)
2. Use TDD workflow (test first)
3. Document learnings (spec vs stack)
4. Main Agent orchestrates, never codes
5. Verify before every commit
6. Fix all failures before new work

### Must Not Do
1. Use pretraining-led reasoning (assumptions)
2. Write implementation before tests
3. Skip learning documentation
4. Main Agent code directly
5. Commit without verification
6. Leave failures for later

### Critical Violations
1. Committing code without verification
2. Sub-agent spawning verification agents
3. Writing implementation before tests
4. Pretraining-led reasoning
5. Committing with failed checks

## Summary

**Main Agent**: Orchestrates, spawns agents, coordinates verification, commits after pass.

**Implementation Agents**: Follow TDD, report completion, NEVER commit or verify.

**Workflow:**
```
Main Agent → Spawn Implementation → TDD → Report →
Spawn Verification → All Pass? → Commit : Fix → Loop
```

**Key Principles:**
1. Retrieval-led reasoning (read code first)
2. Main Agent orchestrates, never codes
3. TDD mandatory (test first)
4. Verification required (no exceptions)
5. Document learnings (spec vs stack)

**For Complete Details**: Read the three extracted skills.

---

_Version: 2.0 - Last Updated: 2026-02-27_
