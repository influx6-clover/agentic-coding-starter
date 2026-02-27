# Agent Documentation and Registry (Main Agent Only)

## Purpose

For Main Agent only when creating or documenting agents. Sub-agents should load Rule 12 (Agent Registry Usage) instead.

**Context Optimization**: This full rule only needed when creating/documenting agents. Sub-agents only need Rule 12 (~150 lines).

## Overview

Establishes mandatory agent documentation system ensuring ALL agents are properly documented before use. Creates centralized registry enabling Main Agent to make informed spawning decisions.

## Core Principle

```
Need Agent → Check Registry → Found? Use Documentation : Create Documentation First
                                        ↓
                            Spawn Agent WITH Documentation File Path
                                        ↓
                            Sub-Agent Reads Own Documentation
```

**NO EXCEPTIONS:**
- ❌ NEVER spawn undocumented agent
- ❌ NEVER create agent without documentation
- ❌ NEVER skip registry check
- ❌ NEVER spawn without providing documentation path
- ❌ NEVER allow duplicate agent documentation
- ✅ ALWAYS document before using
- ✅ ALWAYS provide documentation path when spawning
- ✅ ALWAYS check for duplicates before creating

## Agent Registry Structure

### Directory Location

```
.agents/agents/
├── rust-verification.md          # Rust verification agent
├── javascript-verification.md    # JavaScript/TypeScript verification
├── python-verification.md        # Python verification
├── specification-update.md       # Specification update agent
├── implementation.md              # General implementation agent
├── review.md                      # Pre-work review agent
└── [name-of-agent].md            # Custom agent documentation
```

### Naming Convention

- **Format**: `[name-of-agent].md`
- **Style**: kebab-case (lowercase with hyphens)
- **Descriptive**: Name clearly indicates purpose
- **Specific**: Include language/domain if specialized

**Examples:**
- ✅ `rust-verification.md`, `database-migration.md`, `api-integration-test.md`
- ❌ `agent1.md` (not descriptive), `RustAgent.md` (wrong case), `rust_agent.md` (wrong separator)

### Duplicate Prevention

**Before creating new agent documentation:**
1. Scan all existing `.agents/agents/*.md` frontmatter
2. Check if similar agent exists
3. If duplicate: merge into single comprehensive file
4. If similar but different: ensure clear differentiation

**Duplicate Detection:**
```
1. Read all .agents/agents/*.md frontmatter
2. Compare: name, type, purpose, language
3. If match:
   ├─ SAME purpose + type + language → DUPLICATE (merge)
   ├─ SIMILAR purpose but DIFFERENT specialization → OK (clarify)
   └─ DIFFERENT purpose → OK (proceed)
4. If duplicate: merge both, delete redundant, commit
```

## Agent Documentation Format

### Frontmatter Importance (CRITICAL)

**Main Agent makes spawning decisions based ONLY on:**
1. **Filename**: Descriptive name
2. **Frontmatter**: Quick summary

**Main Agent DOES NOT read full documentation when scanning.**

**Frontmatter Writing Guidelines:**
- **name**: Clear, descriptive (e.g., "Rust Verification Agent")
- **type**: Exact type from allowed list
- **language**: Specific language or "language-agnostic"
- **purpose**: ONE clear sentence (10-15 words max)
  - ✅ GOOD: "Verify Rust code quality, run tests, check clippy and formatting"
  - ❌ BAD: "Handles Rust stuff" (too vague)
- **tools_required**: Complete list
- **skills_required**: Complete list

**Why This Matters**: Frontmatter enables fast filtering and selection. Clear frontmatter = correct agent. Vague frontmatter = wrong agent spawned = wasted work.

### Required Structure

Every agent documentation MUST have:
1. **Frontmatter** (YAML) - Quick summary
2. **Overview** - High-level description
3. **Capabilities** - What agent can do
4. **Requirements** - Tools, skills, dependencies
5. **Responsibilities** - Specific duties
6. **Workflow** - Step-by-step process
7. **Boundaries** - What agent CANNOT do
8. **Integration** - How it works with other agents
9. **Examples** - Real usage scenarios

### Template Reference

**Full template**: `.agents/templates/agent-documentation-template.md`

**Quick frontmatter structure:**
```yaml
---
name: [Agent Name]
type: [verification|implementation|review|utility|specialized]
language: [rust|javascript|python|language-agnostic|multiple]
purpose: Brief one-sentence description (10-15 words)
created: YYYY-MM-DD
author: "Main Agent" or "Team Name"
license: "MIT"
metadata:
  version: "1.0"
  last_updated: YYYY-MM-DD
  complexity: "simple | moderate | complex"
  tags: [tag1, tag2]  # min 2 tags
tools_required: [Tool 1, Tool 2]
skills_required: [Skill 1, Skill 2]  # optional
spawned_by: [main-agent|sub-agent-name|both]
spawns: [list of spawnable agents]  # optional
related_rules: [Rule NN]
status: [active|deprecated|experimental]
---
```

### Frontmatter Fields

**Required:**
- `name`, `type`, `language`, `purpose`
- `created`, `author`, `license`
- `metadata`: `version`, `last_updated`, `complexity`, `tags` (min 2)
- `tools_required`, `spawned_by`, `related_rules`, `status`

**Optional:**
- `skills_required`, `spawns`

**Critical**: Main Agent uses `purpose` field for selection - must be immediately understandable and specific.

## Main Agent Validation (CRITICAL)

### Before Creating Agent Documentation

Main Agent MUST validate:
1. **Frontmatter completeness**: All required fields present
2. **Field values**: Type/status are valid enums, dates correct format
3. **Purpose clarity**: Immediately understandable, specific (10-15 words)
4. **No duplicates**: Check for existing similar agents

### When Updating Agent Documentation

Main Agent MUST:
- ✅ Update `metadata.last_updated`
- ✅ Increment `metadata.version` if significant changes
- ✅ Update `status` if agent deprecated
- ✅ Add new tags if functionality expands
- ✅ Update `tools_required` if requirements change

### Enforcement Consequences

**If incomplete frontmatter:**
- ❌ Agent documentation invalid
- ❌ Agent cannot be discovered/selected
- ❌ Must be corrected before use

**If vague purpose:**
- ❌ Main Agent cannot make proper selection
- ❌ Wrong agent may be spawned
- ❌ Purpose must be rewritten to be specific

## Workflow for Agent Usage

### Documentation File Path (MANDATORY)

When spawning sub-agent, Main Agent MUST provide:
1. Path to agent's documentation (`.agents/agents/[name].md`)
2. Task-specific context
3. Related specification path (if applicable)
4. Any other required resources

**Spawn prompt format:**
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

### Main Agent Spawning Process

1. **Identify Need**: Determine what type of agent needed
2. **Check Registry**: Scan `.agents/agents/` frontmatter
3. **Select Agent**: Find best match based on purpose/type/language
4. **Verify Documentation**: Confirm complete and current
5. **Spawn with Path**: Provide documentation path in spawn prompt
6. **Monitor**: Ensure sub-agent reads documentation

### Sub-Agent Startup Process

1. **Receive Path**: Main Agent provides documentation path
2. **Read Documentation**: Load complete agent documentation
3. **Load Rules**: Load rules listed in documentation
4. **Load Skills**: Load skills if required
5. **Understand Boundaries**: Know what you can/cannot do
6. **Begin Work**: Follow documented workflow

## Creating New Agent Documentation

### When to Create

Create new agent documentation when:
1. **New Agent Type**: Capability not covered by existing agents
2. **Language-Specific**: Existing agent is language-agnostic but need specialized
3. **Domain-Specific**: Need specialized agent for specific domain (DB, API, etc.)

### Creation Process

1. **Check for Duplicates**: Scan existing agents
2. **Use Template**: Start from `.agents/templates/agent-documentation-template.md`
3. **Complete Frontmatter**: All required fields, clear purpose
4. **Write Documentation**: All required sections
5. **Validate**: Ensure frontmatter complete and purpose clear
6. **Commit**: Save to `.agents/agents/[name].md`
7. **Test**: Spawn agent with documentation to verify usability

## Updating Agent Documentation

### When to Update

Update when:
1. Agent capabilities expand
2. New tools/skills required
3. Workflow changes
4. Boundaries change
5. Integration with other agents changes

### Update Process

1. **Read Current**: Load existing documentation
2. **Update Content**: Make necessary changes
3. **Update Frontmatter**: Increment version, update last_updated, add tags if needed
4. **Validate**: Ensure still complete and clear
5. **Commit**: Save changes with clear commit message

## Enforcement

### Must Do
1. Document all agents before use
2. Provide documentation path when spawning
3. Complete frontmatter with clear purpose
4. Check for duplicates before creating
5. Validate frontmatter completeness
6. Update last_updated when modifying
7. Sub-agent reads documentation first

### Must Not Do
1. Spawn undocumented agents
2. Create duplicate agent documentation
3. Use vague purpose in frontmatter
4. Skip validation when creating
5. Leave frontmatter incomplete
6. Spawn without providing path

### Critical Violations
1. Spawning agent without documentation
2. Creating agent without complete frontmatter
3. Not providing documentation path to sub-agent
4. Allowing duplicate agent documentation
5. Using vague purpose that prevents proper selection

## Summary

**Golden Rules:**
1. **Document before use** - ALL agents must be documented
2. **Complete frontmatter** - Clear purpose (10-15 words), all required fields
3. **Provide path when spawning** - Sub-agent needs documentation location
4. **No duplicates** - Check registry before creating
5. **Sub-agent reads first** - Documentation guides all work
6. **Main Agent validates** - Enforce frontmatter completeness
7. **Purpose is critical** - Main Agent uses it for selection

**Workflow:**
```
Need Agent → Check Registry → Found? Select : Create First →
Validate Frontmatter → Spawn with Path → Sub-Agent Reads Doc → Begin Work
```

---

_Version: 1.0 - Last Updated: 2026-02-27_
