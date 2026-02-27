# Agent Rules

## Purpose

Single consolidated rule file directing each agent type to their specific documentation.

## Core Principle

**Every agent MUST read their documentation file which specifies which skills and rules to load.**

## Agent Registry

### Main Agent
**Read**: `.agents/agents/main-agent.md`

Main orchestrator that coordinates all work, spawns specialized agents, manages verification, and commits code.

### Implementation Agents
**Read**: `.agents/agents/implementation.md`

Writes code following TDD, implements features per specifications, reports completion to Main Agent.

### Verification Agents

**Rust Verification**
**Read**: `.agents/agents/rust-verification.md`

Verifies Rust code quality, runs cargo checks, reports pass/fail to Main Agent.

**JavaScript/TypeScript Verification**
**Read**: `.agents/agents/javascript-verification.md`

Verifies JavaScript/TypeScript code quality, runs npm checks, reports pass/fail to Main Agent.

**Python Verification**
**Read**: `.agents/agents/python-verification.md`

Verifies Python code quality, runs pytest checks, reports pass/fail to Main Agent.

**Generic Verification**
**Read**: `.agents/agents/verification.md`

Language-agnostic verification agent for general quality checks.

### Specification Agents

**Specification Update Agent**
**Read**: `.agents/agents/specification-update.md`

Updates specification files, manages task status, maintains requirements.md.

**Review Agent**
**Read**: `.agents/agents/review.md`

Reviews specifications and requirements before implementation begins.

### Utility Agents

**Documentation Agent**
**Read**: `.agents/agents/documentation.md`

Updates documentation when module interfaces change.

**Rust Cleanup Agent**
**Read**: `.agents/agents/rust-cleanup.md`

Specialized cleanup for Rust code formatting and organization.

## Agent Selection

**Main Agent**: When you need to:
- Coordinate implementation work
- Spawn specialized agents
- Manage verification workflow
- Commit code after verification passes

**Implementation Agent**: When you need to:
- Write code following TDD
- Implement features from specifications
- Create tests

**Verification Agent**: When you need to:
- Verify code quality before commit
- Run language-specific checks
- Validate tests pass

**Specification Update Agent**: When you need to:
- Update requirements.md task status
- Maintain specification files
- Update frontmatter

**Documentation Agent**: When you need to:
- Update module documentation
- Sync docs with code changes

**Review Agent**: When you need to:
- Review specifications before work begins
- Validate requirements clarity

## Quick Reference

| Agent Type | File | Purpose |
|-----------|------|---------|
| Main | `main-agent.md` | Orchestrate all work |
| Implementation | `implementation.md` | Write code, TDD |
| Rust Verification | `rust-verification.md` | Verify Rust code |
| JS Verification | `javascript-verification.md` | Verify JS/TS code |
| Python Verification | `python-verification.md` | Verify Python code |
| Generic Verification | `verification.md` | Generic quality checks |
| Spec Update | `specification-update.md` | Update specifications |
| Review | `review.md` | Review requirements |
| Documentation | `documentation.md` | Update docs |
| Rust Cleanup | `rust-cleanup.md` | Rust code cleanup |

## For Sub-Agents

When you are spawned, Main Agent will provide your documentation path:

```
You are a [Agent Name].

CRITICAL: Read your agent documentation FIRST:
- File: .agents/agents/[agent-name].md

After reading your documentation, load required skills and begin work.
```

If documentation path not provided, STOP and request it from Main Agent.

---

_Version: 1.0 - Last Updated: 2026-02-27_
_Consolidated from 15 individual rule files_
