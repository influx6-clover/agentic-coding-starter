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
| **Main Agent** | [01-04](./rules/), [14](./rules/14-machine-optimized-prompts.md), [15](./rules/15-instruction-compaction.md), [05](./rules/05-coding-practice-agent-orchestration.md), [06](./rules/06-specifications-and-requirements.md) (+ [09](./rules/09-skills-identification-and-creation.md), [10](./rules/10-agent-documentation-and-registry.md) when creating skills/agents) |
| **Implementation Agent** | [01-04](./rules/), [14](./rules/14-machine-optimized-prompts.md), [15](./rules/15-instruction-compaction.md), [13](./rules/13-implementation-agent-guide.md), [11](./rules/11-skills-usage.md) (if skills), [stack file](./stacks/) (includes [07](./rules/07-language-conventions-and-standards.md)), [machine_prompt.md](../specifications/) (from spec) |
| **Verification Agent** | [01-04](./rules/), [14](./rules/14-machine-optimized-prompts.md), [15](./rules/15-instruction-compaction.md), **[08](./rules/08-verification-workflow-complete-guide.md)** (CRITICAL: incomplete implementation check), [stack file](./stacks/) (includes [07](./rules/07-language-conventions-and-standards.md)) |
| **Specification Agent** | [01-04](./rules/), [14](./rules/14-machine-optimized-prompts.md), [15](./rules/15-instruction-compaction.md), [06](./rules/06-specifications-and-requirements.md) |
| **Any Sub-Agent** | [01-04](./rules/), [14](./rules/14-machine-optimized-prompts.md), [15](./rules/15-instruction-compaction.md), [12](./rules/12-agent-registry-usage.md), [own agent doc](./agents/), [relevant stack](./stacks/) (includes [07](./rules/07-language-conventions-and-standards.md) if applicable) |

---

## Rules Reference

| Rule | For | Purpose |
|------|-----|---------|
| [01-04](./rules/) | All | Core mandatory rules |
| [05](./rules/05-coding-practice-agent-orchestration.md) | Main Agent | Agent orchestration and verification coordination |
| [06](./rules/06-specifications-and-requirements.md) | Main Agent, Spec agents | Specifications and requirements |
| [07](./rules/07-language-conventions-and-standards.md) | Code writers (via stack files) | Language conventions (embedded in stack files) |
| [08](./rules/08-verification-workflow-complete-guide.md) | Verification agents | **Verification workflow (CRITICAL: incomplete implementation check FIRST)** |
| [09](./rules/09-skills-identification-and-creation.md) | Main Agent | Skills creation and review |
| [10](./rules/10-agent-documentation-and-registry.md) | Main Agent | Agent documentation and creation |
| [11](./rules/11-skills-usage.md) | Sub-agents | Skills usage (concise) |
| [12](./rules/12-agent-registry-usage.md) | Sub-agents | Agent registry usage (concise) |
| [13](./rules/13-implementation-agent-guide.md) | Implementation agents | Coding practice guide (concise) |
| [14](./rules/14-machine-optimized-prompts.md) | All | Machine-optimized prompts (token efficiency) |
| [15](./rules/15-instruction-compaction.md) | All Sub-Agents | Instruction compaction (context optimization) |

---

## Directory Structure

```
.agents/
├── AGENTS.md           # This file
├── rules/              # Load selectively - see Rule Loading table above
├── stacks/             # Load for your language only
├── skills/             # Scan frontmatter, read when using
├── agents/             # Scan frontmatter, read own doc
└── templates/          # Reference when creating files

specifications/         # Read when working on features
documentation/          # Read for modules you're changing
```

**Key Directories**:
- [rules/](./rules/) - Agent behavior rules ([01-04](./rules/), [05-15](./rules/))
- [stacks/](./stacks/) - Language-specific conventions
- [skills/](./skills/) - Reusable agent skills
- [agents/](./agents/) - Agent documentation registry
- [templates/](./templates/) - File templates (requirements, features, learnings, etc.)

**Project Directories**:
- [specifications/](../specifications/) - Requirements and features
- [documentation/](../documentation/) - Module documentation

---

## Spawning Sub-Agents

### General Sub-Agents
Include in spawn prompt:
```
MANDATORY: Load Rules [01-04](./rules/), Rule [14](./rules/14-machine-optimized-prompts.md) (machine prompts), Rule [15](./rules/15-instruction-compaction.md) (context compaction), Rule [12](./rules/12-agent-registry-usage.md), your doc at .agents/agents/[name].md
OPTIONAL: Rule [11](./rules/11-skills-usage.md) (skills), Rule [13](./rules/13-implementation-agent-guide.md) (implementation), [stack file](./stacks/), machine_prompt.md (from spec)
READ: specifications/[NN-spec]/machine_prompt.md (NOT requirements.md - use token-optimized version)
THEN: Generate COMPACT_CONTEXT.md, clear context, reload from compact file
```

### Verification Agents (CRITICAL)
**Main Agent MUST spawn verification agents with these EXACT instructions:**

```
You are a [Language] Verification Agent for [specification/feature name].

CRITICAL INSTRUCTIONS:

1. Load MANDATORY Rules:
   - Rules 01-04 (.agents/rules/01-04-*.md)
   - Rule 14 (.agents/rules/14-machine-optimized-prompts.md)
   - Rule 15 (.agents/rules/15-instruction-compaction.md)
   - **Rule 08 (.agents/rules/08-verification-workflow-complete-guide.md)** [CRITICAL]
   - Stack file: .agents/stacks/[language].md

2. **FIRST MANDATORY CHECK: Incomplete Implementation Scan**
   Before running ANY other checks, you MUST:
   - Search ALL modified files for: TODO, FIXME, unimplemented!(), todo!()
   - Check for stub methods (functions returning Ok(()), default values, or empty implementations)
   - Verify all public methods have real implementations (not just type signatures)
   - Check all state machine states are implemented (not just returning Pending forever)
   - **If ANY incomplete implementations found → FAIL immediately**

   Commands to run:
   ```bash
   # Search for markers
   grep -rn "TODO\|FIXME\|unimplemented!\|todo!" [modified_files_directory]

   # For Rust specifically
   rg "unimplemented!\|todo!" --type rust [directory]
   ```

   **CRITICAL**: Features/specifications claiming "complete" MUST have ZERO incomplete implementations.

3. Run Standard Language Checks (ONLY if incomplete implementation check passes):
   [Standard checks from stack file]

4. Generate Report:
   Include incomplete implementation scan results as Check #1 in report.

5. Return Status:
   - PASS ✅ only if incomplete implementation check passes AND all other checks pass
   - FAIL ❌ if ANY check fails (including incomplete implementations)

Files to verify: [list]
Specification: [path]
```

**See**:
- [Agent Documentation Template](./templates/agent-documentation-template.md)
- [Agent Registry](./agents/)
- [Stack Files](./stacks/)

---

## Critical Reminders

1. **Retrieval-Led Reasoning**: Read codebase FIRST, follow discovered patterns, verify assumptions (NOT pretraining guessing) - See [AGENTS.md Core Principle](#retrieval-led-reasoning-mandatory)
2. **Machine-Optimized Prompts**: Sub-agents read [machine_prompt.md](../specifications/) (NOT requirements.md) for 58% token savings - See [Rule 14](./rules/14-machine-optimized-prompts.md)
3. **Context Compaction**: Generate [COMPACT_CONTEXT.md](./templates/COMPACT_CONTEXT-template.md) before work, reload after updates for 97% context reduction - See [Rule 15](./rules/15-instruction-compaction.md)
4. **Main Agent**: Orchestrator only - delegates ALL work, generates machine_prompt.md before spawning - See [Rule 05](./rules/05-coding-practice-agent-orchestration.md)
5. **Verification Required**: NO commits without verification passing, **MANDATORY incomplete implementation check FIRST** (TODO/FIXME/unimplemented!/stubs) - See [Rule 08](./rules/08-verification-workflow-complete-guide.md)
6. **Documentation After Implementation**: Update docs AFTER successful implementation and verification - See [Rule 06](./rules/06-specifications-and-requirements.md)
7. **Context Optimization**: Load ONLY what you need, compact regularly - See [Rules 14](./rules/14-machine-optimized-prompts.md) & [15](./rules/15-instruction-compaction.md)
8. **Sub-agents**: Never commit directly, never spawn verification agents, MUST compact context - See [Rule 13](./rules/13-implementation-agent-guide.md)

---

_Version: 5.4.0 - Last Updated: 2026-02-01_

_For complete version history, see [CHANGELOG.md](./CHANGELOG.md)_
