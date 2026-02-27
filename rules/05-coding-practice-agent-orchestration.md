# Coding Practice and Agent Orchestration

## Purpose

Establishes mandatory coding practices and agent orchestration workflow.

## For Main Agent

**Read these skills:**
1. `.agents/skills/main-agent-orchestration/skill.md` - How to coordinate agents and verification
2. `.agents/skills/code-verification/skill.md` - How to verify code before commit

## For Implementation Agents

**Read these skills:**
1. `.agents/skills/test-driven-development/skill.md` - TDD workflow (test first)
2. `.agents/skills/learning-documentation/skill.md` - How to document learnings

## Core Principles

1. **Retrieval-Led Reasoning**: Read codebase FIRST before assumptions
2. **Main Agent Orchestrates**: Never codes directly, spawns specialized agents
3. **TDD Mandatory**: Write test FIRST, verify fails, implement, verify passes
4. **Verification Required**: NO code committed without verification (ZERO TOLERANCE)
5. **Document Learnings**: Specification-specific vs stack-generic

## Workflow Summary

```
Main Agent → Spawn Implementation → TDD → Report →
Spawn Verification → All Pass? → Commit : Fix → Loop
```

## Agent Identity

**Main Agent:**
- Directly interacting with user
- ONLY agent that spawns verification agents
- Commits after verification passes

**Sub-Agents:**
- Spawned by Main Agent
- Report completion to Main Agent
- NEVER spawn verification agents
- NEVER commit directly

## Work Priority

1. Fix broken tests (highest priority)
2. Ensure all tests pass
3. Complete incomplete tests
4. Resolve build/compilation issues
5. Fix lint/format/type errors
6. Implement new features

**Zero Tolerance**: No bugs, failures, or incomplete work in commits.

## Critical Violations

1. Committing without verification
2. Sub-agent spawning verification agents
3. Writing implementation before tests
4. Using pretraining-led reasoning (assumptions)
5. Committing with failed checks

---

_Version: 3.0 - Last Updated: 2026-02-27_
_Simplified to skill references only_
