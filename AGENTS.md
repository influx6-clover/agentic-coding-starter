---
purpose: Central entry point for AI agent configuration
description: Simplified agent system with skill-based architecture
version: 6.0.0
last_updated: 2026-02-27
---

# Agent Configuration

## Core Principle

**Every agent reads their documentation file which specifies skills to load.**

Agents load **only what they need** to optimize context window usage.

## Agent Registry

All agents are documented in `.agents/agents/` directory:

1. **[Main Agent]** read `.agents/agents/main-agent.md`
2. **[Implementation Agent]** read `.agents/agents/implementation.md`
3. **[Rust Verification Agent]** read `.agents/agents/rust-verification.md`
4. **[JavaScript Verification Agent]** read `.agents/agents/javascript-verification.md`
5. **[Python Verification Agent]** read `.agents/agents/python-verification.md`
6. **[Generic Verification Agent]** read `.agents/agents/verification.md`
7. **[Specification Update Agent]** read `.agents/agents/specification-update.md`
8. **[Review Agent]** read `.agents/agents/review.md`
9. **[Documentation Agent]** read `.agents/agents/documentation.md`
10. **[Rust Cleanup Agent]** read `.agents/agents/rust-cleanup.md`

## For Sub-Agents

Main Agent provides documentation path when spawning. If not provided, request it.

---

## Retrieval-Led Reasoning (MANDATORY)

**ALL agents MUST follow retrieval-led reasoning, NOT pretraining-led reasoning.**

**Retrieval-Led Reasoning** ✅:
- Read the codebase FIRST before making assumptions
- Use Grep/Glob/Read tools to understand existing patterns
- Follow project-specific conventions found in code
- Trust project rules over general best practices
- Search for similar implementations as reference
- Verify assumptions by reading actual code

**Pretraining-Led Reasoning** ❌ (FORBIDDEN):
- Making assumptions based on "typical" patterns
- Implementing without checking existing code
- Applying generic best practices without context
- Assuming file structures or naming conventions
- Guessing at project patterns without verification

**Why This Matters**:
- Every codebase has unique patterns and conventions
- Pretraining knowledge may not match project specifics
- Reading actual code reveals true project structure
- Assumptions lead to inconsistent implementations

**Enforcement**: Before any implementation, agents MUST demonstrate retrieval by:
1. Searching for similar implementations
2. Reading relevant existing code
3. Checking project conventions
4. Following discovered patterns

---

## Directory Structure

```
.agents/
├── AGENTS.md           # This file
├── agents/             # Agent documentation (read your own)
├── skills/             # Reusable skills (load as specified by agent docs)
└── templates/          # File templates

specifications/         # Read when working on features
documentation/          # Read for modules you're changing
```

**Key Directories**:
- [agents/](./agents/) - Agent documentation registry
- [skills/](./skills/) - Reusable agent skills (language skills, workflows, practices)
- [templates/](./templates/) - File templates (requirements, features, learnings, etc.)

**Project Directories**:
- [specifications/](../specifications/) - Requirements and features
- [documentation/](../documentation/) - Module documentation

---

## Language-Specific Skills

Language standards and best practices are in skill files:

- **Rust**: `.agents/skills/rust-clean-code/skill.md`
- **Python**: `.agents/skills/python-clean-code/skill.md`
- **JavaScript/TypeScript**: General standards in code-verification

---

## Spawning Sub-Agents

### For Implementation Agents

```
You are an Implementation Agent for [task description].

1. Read your agent documentation: .agents/agents/implementation.md
2. Read required skills as specified in your documentation
3. Read compacted.md (provided by Main Agent)
4. Begin implementation following TDD
5. Report completion to Main Agent (do NOT commit)
```

### For Verification Agents

```
You are a [Language] Verification Agent for [specification/feature name].

1. Read your agent documentation: .agents/agents/[language]-verification.md
2. Read required skills as specified in your documentation
3. **FIRST MANDATORY CHECK: Incomplete Implementation Scan**
   - Search ALL modified files for: TODO, FIXME, unimplemented!(), todo!()
   - Check for stub methods (functions returning Ok(()), default values)
   - **If ANY incomplete implementations found → FAIL immediately**
4. Run standard language checks (ONLY if incomplete check passes)
5. Generate report with all check results
6. Report PASS/FAIL to Main Agent

Files to verify: [list]
Specification: [path]
```

---

## Critical Reminders

1. **Retrieval-Led Reasoning**: Read codebase FIRST, follow discovered patterns, verify assumptions
2. **Agent Documentation**: Each agent reads their own documentation file which specifies skills to load
3. **Skills-Based**: Load only required skills, not everything
4. **Main Agent**: Orchestrator only - delegates ALL work
5. **Verification Required**: NO commits without verification passing
6. **Incomplete Implementation Check**: MANDATORY first check in verification
7. **Sub-agents**: Never commit directly, never spawn verification agents
8. **Context Optimization**: Load ONLY what you need

---

## Quick Reference

**I am Main Agent:**
- Read: `.agents/agents/main-agent.md`
- Skills: main-agent-orchestration, code-verification, agent-documentation, specifications-management, etc.

**I am Implementation Agent:**
- Read: `.agents/agents/implementation.md`
- Skills: implementation-practices, test-driven-development, learning-documentation, language-standards

**I am Verification Agent:**
- Read: `.agents/agents/[language]-verification.md`
- Skills: code-verification, language-standards, [language]-clean-code

**I am spawned but don't know my role:**
- Ask Main Agent for documentation path
- Read that documentation file
- Follow the skills and workflow specified there

---

_Version: 6.0.0 - Last Updated: 2026-02-27_

_Simplified architecture: rule.md → agents → skills_
