---
purpose: Central entry point for AI agent configuration
description: Minimal configuration directing agents to load rules selectively
version: 5.4.0
last_updated: 2026-02-01
---

# Agent Configuration

## Core Principle

Agents load rules **selectively** based on role and task to optimize context window usage.

**CRITICAL**: `.agents/rules/*` takes precedence over this file if conflicts arise.

### Retrieval-Led Reasoning (MANDATORY)

**ALL agents MUST follow retrieval-led reasoning, NOT pretraining-led reasoning.**

**Retrieval-Led Reasoning**:
- ✅ **Read the codebase FIRST** before making assumptions
- ✅ **Use Grep/Glob/Read tools** to understand existing patterns
- ✅ **Follow project-specific conventions** found in code
- ✅ **Trust project rules** over general best practices
- ✅ **Search for similar implementations** as reference
- ✅ **Read stack files and learnings** for project context
- ✅ **Verify assumptions** by reading actual code

**Pretraining-Led Reasoning** (FORBIDDEN):
- ❌ Making assumptions based on "typical" patterns
- ❌ Implementing without checking existing code
- ❌ Applying generic best practices without context
- ❌ Assuming file structures or naming conventions
- ❌ Guessing at project patterns without verification

**Why This Matters**:
- Every codebase has unique patterns and conventions
- Pretraining knowledge may not match project specifics
- Reading actual code reveals true project structure
- Project rules and learnings encode critical context
- Assumptions lead to inconsistent implementations

**Example**:
```
❌ BAD (Pretraining-Led):
"I'll create the API endpoint using Express middleware because that's standard"

✅ GOOD (Retrieval-Led):
"Let me search for existing API endpoints to see how this project structures them"
[Uses Grep to find route patterns]
[Reads actual endpoint files]
"I see this project uses Axum with custom middleware. I'll follow that pattern."
```

**Enforcement**: Before any implementation, agents MUST demonstrate retrieval by:
1. Searching for similar implementations
2. Reading relevant existing code
3. Checking project conventions
4. Following discovered patterns

---

## Rule Loading

### Mandatory (ALL Agents)

| Rule | Topic |
|------|-------|
| [01](./rules/01-rule-naming-and-structure.md) | File naming conventions |
| [02](./rules/02-rules-directory-policy.md) | Directory policies |
| [03](./rules/03-dangerous-operations-safety.md) | Dangerous operations safety |
| [04](./rules/04-work-commit-and-push-rules.md) | Work commit and push rules |
| [14](./rules/14-machine-optimized-prompts.md) | Machine-optimized prompts (token efficiency) |
| [15](./rules/15-instruction-compaction.md) | Instruction compaction (context optimization) |

### By Role

| Agent Type | Load These Rules |
|------------|------------------|
| **Main Agent** | 01-04, 14-15, [05](./rules/05-coding-practice-agent-orchestration.md), [06](./rules/06-specifications-and-requirements.md) (+ [09](./rules/09-skills-identification-and-creation.md), [10](./rules/10-agent-documentation-and-registry.md) when creating skills/agents) |
| **Implementation Agent** | 01-04, 14-15, [13](./rules/13-implementation-agent-guide.md), [11](./rules/11-skills-usage.md) (if skills), stack file (includes [07](./rules/07-language-conventions-and-standards.md)), machine_prompt.md (from spec) |
| **Verification Agent** | 01-04, 14-15, [08](./rules/08-verification-workflow-complete-guide.md), stack file (includes [07](./rules/07-language-conventions-and-standards.md)) |
| **Specification Agent** | 01-04, 14-15, [06](./rules/06-specifications-and-requirements.md) |
| **Any Sub-Agent** | 01-04, 14-15, [12](./rules/12-agent-registry-usage.md), own agent doc, relevant stack (includes [07](./rules/07-language-conventions-and-standards.md) if applicable) |

---

## Rules Reference

| Rule | For | Purpose |
|------|-----|---------|
| 01-04 | All | Core mandatory rules |
| 05 | Main Agent | Agent orchestration and verification coordination |
| 06 | Main Agent, Spec agents | Specifications and requirements |
| 07 | Code writers (via stack files) | Language conventions (embedded in stack files) |
| 08 | Verification agents | Verification workflow |
| 09 | Main Agent | Skills creation and review |
| 10 | Main Agent | Agent documentation and creation |
| 11 | Sub-agents | Skills usage (concise) |
| 12 | Sub-agents | Agent registry usage (concise) |
| 13 | Implementation agents | Coding practice guide (concise) |
| 14 | All | Machine-optimized prompts (token efficiency) |
| 15 | All Sub-Agents | Instruction compaction (context optimization) |

---

## Directory Structure

```
.agents/
├── AGENTS.md           # This file
├── rules/              # Load selectively
├── stacks/             # Load for your language only
├── skills/             # Scan frontmatter, read when using
├── agents/             # Scan frontmatter, read own doc
└── templates/          # Reference when creating files

specifications/         # Read when working on features
documentation/          # Read for modules you're changing
```

---

## Spawning Sub-Agents

Include in spawn prompt:
```
MANDATORY: Load Rules 01-04, Rule 14 (machine prompts), Rule 15 (context compaction), Rule 12, your doc at .agents/agents/[name].md
OPTIONAL: Rule 11 (skills), Rule 13 (implementation), stack file, machine_prompt.md (from spec)
READ: specifications/[NN-spec]/machine_prompt.md (NOT requirements.md - use token-optimized version)
THEN: Generate COMPACT_CONTEXT.md, clear context, reload from compact file
```

---

## Critical Reminders

1. **Retrieval-Led Reasoning**: Read codebase FIRST, follow discovered patterns, verify assumptions (NOT pretraining guessing)
2. **Machine-Optimized Prompts**: Sub-agents read machine_prompt.md (NOT requirements.md) for 58% token savings
3. **Context Compaction**: Generate COMPACT_CONTEXT.md before work, reload after updates for 97% context reduction
4. **Main Agent**: Orchestrator only - delegates ALL work, generates machine_prompt.md before spawning
5. **Verification Required**: NO commits without verification passing
6. **Documentation After Implementation**: Update docs AFTER successful implementation and verification
7. **Context Optimization**: Load ONLY what you need, compact regularly
8. **Sub-agents**: Never commit directly, never spawn verification agents, MUST compact context

---

_Version: 5.4.0 - Last Updated: 2026-02-01_

_For complete version history, see [CHANGELOG.md](./CHANGELOG.md)_
