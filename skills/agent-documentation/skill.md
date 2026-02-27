---
name: "Agent Documentation"
description: "Complete guide for documenting agents and using agent registry for Main Agent and Sub-Agents"
approved: Yes
created: 2026-02-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-27"
  tags: [agents, documentation, registry, spawning, coordination]
tools: []
files: []
---

# Agent Documentation

## Overview

Complete guide for documenting agents in the registry and using agent documentation. Covers Main Agent (creating/documenting agents) and Sub-Agents (reading own documentation).

**Usage Type**: EDUCATIONAL - Learn agent documentation patterns.

## When to Use

**For Main Agent:**
- Creating new agent type
- Documenting existing agent
- Spawning sub-agents
- Need to select appropriate agent

**For Sub-Agents:**
- Starting work after being spawned
- Understanding capabilities and boundaries
- Loading required rules and skills

## Prerequisites

- Understanding of agent types (Main, Sub-Agent, Verification, Implementation, etc.)
- Access to `.agents/agents/` directory
- Familiarity with agent documentation template

## Agent Registry Location

```
.agents/agents/
├── rust-verification.md
├── javascript-verification.md
├── python-verification.md
├── specification-update.md
├── implementation.md
├── review.md
└── [name-of-agent].md
```

## Creating Agent Documentation (Main Agent)

### When to Create

Create documentation when:
1. New agent type with capability not covered by existing
2. Language-specific need (existing is agnostic)
3. Domain-specific need (DB, API, etc.)

### Naming Convention

- **Format**: `[name-of-agent].md`
- **Style**: kebab-case (lowercase with hyphens)
- **Descriptive**: Name clearly indicates purpose
- **Specific**: Include language/domain if specialized

**Examples:**
- ✅ `rust-verification.md`, `database-migration.md`
- ❌ `agent1.md` (not descriptive), `RustAgent.md` (wrong case)

### Duplicate Prevention

**Before creating:**
1. Scan all `.agents/agents/*.md` frontmatter
2. Compare: name, type, purpose, language
3. If match:
   - SAME purpose + type + language → DUPLICATE (merge)
   - SIMILAR but DIFFERENT specialization → OK (clarify)
   - DIFFERENT purpose → OK (proceed)
4. If duplicate: Merge, delete redundant, commit

### Frontmatter (CRITICAL)

**Main Agent makes spawning decisions based ONLY on:**
1. Filename
2. Frontmatter (NOT full documentation)

**Why**: Scanning 10-20 agents quickly. Frontmatter enables fast selection.

```yaml
---
name: "Agent Name"
type: [verification|implementation|review|utility|specialized]
language: [rust|javascript|python|language-agnostic|multiple]
purpose: Brief one-sentence description (10-15 words max)
created: YYYY-MM-DD
author: "Main Agent"
license: "MIT"
metadata:
  version: "1.0"
  last_updated: YYYY-MM-DD
  complexity: "simple | moderate | complex"
  tags: [tag1, tag2]  # min 2 tags
tools_required: [Tool1, Tool2]
skills_required: [Skill1, Skill2]  # optional
spawned_by: [main-agent|sub-agent-name|both]
spawns: [list]  # optional
related_rules: [Rule NN]
status: [active|deprecated|experimental]
---
```

**Required:**
- `name`, `type`, `language`, `purpose` (10-15 words, crystal clear)
- `created`, `author`, `license`
- `metadata`: `version`, `last_updated`, `complexity`, `tags` (min 2)
- `tools_required`, `spawned_by`, `related_rules`, `status`

**Purpose Writing:**
- ✅ GOOD: "Verify Rust code quality, run tests, check clippy and formatting"
- ❌ BAD: "Handles Rust stuff" (too vague)

### Required Documentation Structure

**Template**: `.agents/templates/agent-documentation-template.md`

**Sections:**
1. **Frontmatter** (YAML) - Quick summary
2. **Overview** - High-level description
3. **Capabilities** - What agent can do
4. **Requirements** - Tools, skills, dependencies
5. **Responsibilities** - Specific duties
6. **Workflow** - Step-by-step process
7. **Boundaries** - What agent CANNOT do
8. **Integration** - How it works with other agents
9. **Examples** - Real usage scenarios

### Validation (Main Agent)

**Before creating:**
1. Check frontmatter completeness (all required fields)
2. Validate field values (type/status are valid enums, dates correct)
3. Validate purpose clarity (immediately understandable, 10-15 words)
4. Check for duplicates

**When updating:**
- Update `metadata.last_updated`
- Increment `metadata.version` if significant changes
- Update `status` if deprecated
- Add new tags if functionality expands

## Spawning Sub-Agents (Main Agent)

### Spawning Process

1. **Identify Need**: Determine agent type needed
2. **Check Registry**: Scan `.agents/agents/` frontmatter
3. **Select Agent**: Find best match by purpose/type/language
4. **Verify Documentation**: Confirm complete and current
5. **Spawn with Path**: Provide documentation path
6. **Monitor**: Ensure sub-agent reads documentation

### Spawn Message Format

```
You are a [Agent Name].

CRITICAL: Read your agent documentation FIRST:
- File: .agents/agents/[name-of-agent].md

After reading your documentation:
1. Understand your capabilities and boundaries
2. Load required rules (listed in documentation)
3. Load required skills (if any)
4. Begin work following documented workflow

[Task-specific instructions...]
```

### MANDATORY: Provide Documentation Path

When spawning, Main Agent MUST provide:
1. Path to agent documentation (`.agents/agents/[name].md`)
2. Task-specific context
3. Related specification path (if applicable)
4. Required resources

## Using Agent Documentation (Sub-Agents)

### Startup Protocol

**Step 1: Check for Documentation Path**

Main Agent MUST provide documentation path.

**If provided:**
```
Your documentation: .agents/agents/[name].md
```
→ Proceed to Step 2

**If missing:**
```
STOP: No agent documentation provided!

Request from Main Agent:
"I am [Agent Type] for [purpose].
 I need my documentation path: .agents/agents/[expected-name].md
 Cannot proceed without understanding responsibilities, tools, workflow, boundaries."
```

**Step 2: Read Your Documentation**

1. Read documentation file FIRST
2. Understand: capabilities, requirements, responsibilities, boundaries
3. Note required skills (check `.agents/skills/`)
4. Note required tools

**Step 3: Load Required Rules**

1. Rules 01-04 (mandatory for all agents)
2. skills-management skill (if using skills)
3. Relevant language skill (`language-specific skill files`)
4. Specification files (if provided)

**Step 4: Execute Your Work**

Follow workflow documented in your documentation.

### What Documentation Contains

| Section | What It Tells You |
|---------|-------------------|
| Frontmatter | Name, type, purpose, tools, skills |
| Overview | High-level description |
| Capabilities | What you can do |
| Requirements | Tools, skills, dependencies |
| Responsibilities | Your specific duties |
| Workflow | Step-by-step process |
| Boundaries | What you CANNOT do |
| Integration | How you work with other agents |

### Sub-Agent Boundaries

**Can Do:**
- Read and follow own documentation
- Execute documented workflow
- Use approved skills (per skills-management skill)
- Report completion to Main Agent
- Request help when stuck

**Cannot Do:**
- Spawn verification agents (only Main Agent can)
- Spawn other agents directly (report need to Main Agent)
- Commit code directly (report to Main Agent)
- Exceed documented boundaries
- Proceed without documentation path

### Requesting Additional Agents

If you need another agent:
1. DO NOT spawn directly
2. Report to Main Agent: "I need [type] agent for [purpose]. Reason: [why]. Blocker: [what you can't do]."
3. Wait for Main Agent to spawn and coordinate

### Reporting Completion

When work complete:
```
Task completed:
- Files changed: [list]
- What implemented: [description]
- Specification: [if applicable]
- Learnings documented: [Yes/No]

Ready for Main Agent verification.
```

**CRITICAL**: Never commit directly. Always report to Main Agent.

## Common Patterns

### Pattern: Main Agent Selects Agent

```
1. Task requires Rust verification
2. Scan .agents/agents/*.md frontmatter
3. Find rust-verification.md:
   - Type: verification
   - Language: rust
   - Purpose: "Verify Rust code quality, run tests, check clippy"
4. Select rust-verification.md
5. Spawn with documentation path
```

### Pattern: Sub-Agent Startup

```
1. Spawned by Main Agent
2. Receive documentation path: .agents/agents/implementation.md
3. Read complete documentation
4. Load Rules 01-04 (mandatory)
5. Read implementation-practices skill
6. Load language skill (.agents/skills/rust-clean-code/skill.md)
7. Begin work following documented workflow
```

### Pattern: Creating New Agent

```
1. Main Agent identifies need for new agent type
2. Check registry for duplicates (scan frontmatter)
3. Create .agents/agents/[name].md
4. Write complete frontmatter (all required fields)
5. Write documentation sections
6. Validate frontmatter completeness
7. Test spawn agent with documentation
8. Commit to registry
```

## Common Agent Types

### Verification Agents
- **Purpose**: Verify code quality before commit
- **Type**: `verification`
- **Language**: Specific (rust, javascript, python)
- **Spawned by**: Main Agent only

### Implementation Agents
- **Purpose**: Write code following specifications
- **Type**: `implementation`
- **Language**: Specific or agnostic
- **Spawned by**: Main Agent

### Review Agents
- **Purpose**: Review specifications/requirements
- **Type**: `review`
- **Language**: Language-agnostic
- **Spawned by**: Main Agent

### Utility Agents
- **Purpose**: Specific utility tasks
- **Type**: `utility`
- **Language**: Language-agnostic or specific
- **Spawned by**: Main Agent or Sub-Agent

## Pitfalls to Avoid

**❌ Don't:**
- Spawn agents without documentation path
- Create duplicate agent documentation
- Use vague purpose in frontmatter
- Skip validation when creating
- Leave frontmatter incomplete
- Sub-agent proceed without reading documentation
- Spawn agents that don't exist in registry

**✅ Do:**
- Always provide documentation path when spawning
- Check for duplicates before creating
- Write clear, specific purpose (10-15 words)
- Validate frontmatter completeness
- Update metadata when modifying
- Sub-agent read documentation first
- Only spawn documented agents

## Summary

**Main Agent (Creating/Spawning):**
1. Create documentation with complete frontmatter
2. Write clear purpose (10-15 words)
3. Check for duplicates
4. Validate completeness
5. Provide documentation path when spawning

**Sub-Agents (Using):**
1. Receive documentation path from Main Agent
2. Read complete documentation FIRST
3. Load required rules and skills
4. Follow documented workflow
5. Stay within boundaries
6. Report completion to Main Agent

**Key Principles:**
- Documentation path MANDATORY when spawning
- Frontmatter enables fast agent selection
- Purpose must be crystal clear (10-15 words)
- Sub-agents read documentation before starting
- Never spawn undocumented agents
- Check for duplicates before creating

---

_Version: 1.0 - Last Updated: 2026-02-27_
