# Agent Orchestration and Verification (Main Agent Only)

## Purpose

For Main Agent only - covers agent orchestration, verification coordination, and mandatory verification workflow. Implementation agents should load Rule 13 (Implementation Agent Guide).

**Context Optimization**: Implementation agents only need Rule 13 instead of this full rule.

## Overview

Establishes mandatory practice for code development, requiring specialized agent orchestration with **MANDATORY CODE VERIFICATION** before any commit. **ZERO TOLERANCE** for violations.

## Core Principles

### 1. Retrieval-Led Reasoning (MANDATORY)

**ALL agents MUST follow retrieval-led reasoning, NOT pretraining-led reasoning.**

**Do This (Retrieval-Led):**
1. Read codebase FIRST before making assumptions
2. Use Grep/Glob/Read tools to understand existing patterns
3. Follow project-specific conventions found in code
4. Trust project rules over general best practices
5. Search for similar implementations as reference
6. Read stack files and learnings for context
7. Verify assumptions by reading actual code

**Don't Do This (Pretraining-Led - FORBIDDEN):**
- Making assumptions based on "typical" patterns
- Implementing without checking existing code
- Applying generic best practices without context
- Assuming file structures or naming conventions
- Guessing at project patterns without verification

### 2. Main Agent as Orchestrator

Main Agent MUST:
- Act as controller and orchestrator ONLY
- NEVER perform coding tasks directly
- Launch specialized agents for all code work
- Delegate to verification agents after implementation
- Coordinate specification updates
- Commit code ONLY after verification passes

**See**: `.agents/skills/main-agent-orchestration/skill.md` for complete orchestration workflow.

### 3. Test-Driven Development (MANDATORY)

Implementation agents MUST follow TDD:
1. Write test FIRST (before implementation)
2. Verify test FAILS for right reason
3. Implement minimum code to pass test
4. Verify test PASSES
5. Refactor if needed (keep test green)
6. Repeat cycle

**See**: `.agents/skills/test-driven-development/skill.md` for complete TDD workflow and test documentation requirements.

### 4. Autonomous Decision-Making

**Act Autonomously (NO user approval):**
- Fixing broken tests
- Completing incomplete tests (if requirements clear)
- Fixing build/compilation issues
- Resolving lint/format/type errors
- Fixing verification failures
- Implementing against clear specifications
- Following established patterns

**Seek User Approval:**
- Unclear requirements
- Breaking existing rules
- Dangerous operations (Rule 03)
- Multiple valid approaches
- Specification writing (user must review)

**Principle**: If you know what "good" looks like, DO IT. Only ask when truly unclear.

### 5. Work Priority Order (MANDATORY)

1. Fix ALL broken tests (highest priority)
2. Ensure ALL tests pass
3. Complete incomplete tests
4. Resolve build/compilation issues
5. Fix lint/format/type errors
6. Implement new features

**Zero Tolerance**: No bugs, failures, or incomplete work in commits.

### 6. Agent Identity and Authority

**Main Agent** (Only agent with verification authority):
- Directly interacting with user
- Spawns implementation, specification, verification agents
- Can commit code after verification passes

**Sub-Agents** (No verification authority):
- Spawned by Main Agent
- Report completion to Main Agent
- NEVER spawn verification agents
- NEVER commit directly

**Quick Check:**
```
Directly interacting with user? → MAIN AGENT
Spawned by another agent? → SUB-AGENT
```

### 7. Verification-First Workflow

**CRITICAL**: NO code is EVER committed without verification.

```
Implement → Report → Verification → Update Spec → Commit
```

**See**: Rule 08 (Verification Workflow) for complete verification requirements.

### 8. Specification Versioning

**MANDATORY**: Completed specifications are IMMUTABLE.

**Before updating specification:**
1. Check status in requirements.md frontmatter
2. If "completed": Create NEW specification (use `builds_on`)
3. If "in-progress": Can update as normal

**See**: Rule 06 (Specifications and Requirements) for complete versioning rules.

## Skills for Detailed Workflows

This rule references three comprehensive skills containing detailed workflows extracted from the original rule:

### 1. Main Agent Orchestration Skill
**Location**: `.agents/skills/main-agent-orchestration/skill.md`

**Contains:**
- Complete orchestration workflow (Phases 1-5)
- Sub-agent spawning patterns
- Verification coordination
- Commit workflow with verification
- Concurrent multi-task patterns
- Feature completion workflow
- Specification update coordination

**Use when**: Main Agent needs to coordinate implementation work and verification.

### 2. Test-Driven Development (TDD) Skill
**Location**: `.agents/skills/test-driven-development/skill.md`

**Contains:**
- Complete TDD cycle (6 steps)
- Test documentation requirements (WHY/WHAT)
- Test quality validation (real vs mock)
- Test-first examples (Rust, TypeScript, Python)
- Valid/invalid test patterns
- TDD benefits and enforcement

**Use when**: Implementation agents need TDD workflow guidance.

### 3. Learning Documentation Skill
**Location**: `.agents/skills/learning-documentation/skill.md`

**Contains:**
- Specification-specific vs stack-generic learnings
- Documentation format and guidelines
- Decision tree for where to document
- Examples of both learning types
- When to document vs when not to

**Use when**: Agents need to document learnings discovered during work.

## Mandatory Workflow Summary

### Phase 1: Implementation
1. Main Agent breaks down work
2. Generates machine_prompt.md (Rule 14)
3. Generates COMPACT_CONTEXT.md (Rule 15)
4. Spawns implementation agents with context
5. Waits for completion reports

### Phase 2: Verification (MANDATORY)
1. Main Agent analyzes changed files
2. Spawns verification agents (one per language)
3. Waits for verification results
4. All checks must pass before commit

### Phase 3: Commit
1. If PASS: `git add` → `git commit` → `git push`
2. If FAIL: Create fix task, regenerate COMPACT_CONTEXT, fix, re-verify
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
4. Pretraining-led reasoning instead of retrieval
5. Committing with failed checks

## Summary

**Main Agent**: Orchestrates work, spawns agents, coordinates verification, commits after verification passes.

**Implementation Agents**: Follow TDD, report completion, NEVER commit or verify.

**Key Skills:**
1. **Main Agent Orchestration** - Complete coordination workflow
2. **Test-Driven Development** - TDD cycle and test documentation
3. **Learning Documentation** - Where and how to document learnings

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

**For Complete Details**: Read the three extracted skills for comprehensive workflows.

---

_Version: 2.0 - Last Updated: 2026-02-27_
_Major Update: Extracted detailed workflows into three focused skills_
