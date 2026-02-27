# Skills Creation and Review (Main Agent Only)

## Purpose

For Main Agent only when creating/reviewing skills. Sub-agents should load Rule 11 (Skills Usage) instead.

## Overview

Skills are documented know-how for complex technical tasks capturing tool/library usage, pattern implementations, operations, and problem solutions.

## Core Principles

1. **User Approval Required**: No skill can be used until user approves
2. **Last Resort Only**: Create ONLY when fundamental understanding is missing, no existing skill covers the need, and no alternative approach possible

## Directory Structure

```
.agents/skills/[skill-name]/
├── skill.md           # REQUIRED - Main documentation
├── learnings.md       # OPTIONAL - Practical insights from usage
├── assets/            # OPTIONAL - Diagrams, configs, sample data
├── docs/              # OPTIONAL - Extended documentation
├── templates/         # OPTIONAL - Code templates (TEMPLATE skills)
├── scripts/           # OPTIONAL - Executable scripts (EXECUTABLE skills)
└── examples/          # OPTIONAL - Reference implementations (EDUCATIONAL)
```

### Directory Contents

| Directory | Purpose | When to Include |
|-----------|---------|----------------|
| `skill.md` | Main documentation (REQUIRED) | Always |
| `learnings.md` | Practical insights from usage | After skill is used |
| `assets/` | Diagrams, configs, sample data | When visual/config aids helpful |
| `docs/` | Extended documentation, FAQ | For complex skills |
| `templates/` | Code templates (TEMPLATE) | When copying files to project |
| `scripts/` | Executable tools (EXECUTABLE) | When running as external tools |
| `examples/` | Reference implementations (EDUCATIONAL) | For learning patterns |

### Naming
- Use kebab-case: `playwright-web-interaction`, `kubernetes-deployment`
- NO numeric prefixes
- Name clearly describes purpose

### Modular Skills

For complex or related skills under a common theme:

```
skills/[parent-skill-name]/
├── skill.md                    # Main entry point - references all sub-skills
├── [topic-1]/skill.md         # Sub-skill documentation
├── [topic-2]/skill.md
└── [topic-3]/skill.md
```

**Main skill.md Requirements:**
- Brief overview of scope
- Navigation to sub-skills in frontmatter `files:` field
- Table/list of sub-skills with descriptions

**Sub-skill Requirements:**
- Complete standalone documentation
- Can be used independently
- All standard sections

## Three Usage Types

### 1. TEMPLATE (Copy and Customize)
- Files in `templates/` copied to project
- Agent customizes copied files
- ❌ NEVER import from `.agents/skills/` in project code

### 2. EXECUTABLE (Run as Tools)
- Scripts in `scripts/` run as external commands
- Consume output in project
- Never modify scripts

### 3. EDUCATIONAL (Learn and Implement)
- Examples in `examples/` teach patterns
- Install external dependencies listed
- Write fresh implementation
- ❌ NEVER import from `.agents/skills/` in project code

## Skill File Format

### Frontmatter (Required)

```yaml
---
name: "Skill Name"
description: "1-2 sentence summary"
approved: No
created: YYYY-MM-DD
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "YYYY-MM-DD"
  tags: [tag-1, tag-2]
tools: [Tool1, Tool2]
files:
  - templates/client.ts: "API client template"
  - scripts/run.sh: "Execution script"
assets:
  - docs/deep-dive.md: "Extended explanation"
  - assets/diagrams/flow.png: "Architecture diagram"
---
```

**Required**: `name`, `description`, `approved`, `created`, `license`, `metadata`, `tools`
**Optional**: `files` (agent-facing), `assets` (user/informational)

### Content Structure

**Template Location**: `.agents/templates/skill-template.md`

Key sections:
- Overview (2-3 paragraphs)
- When to Use (scope and limitations)
- Prerequisites (knowledge, dependencies)
- **Usage Type declaration** (TEMPLATE/EXECUTABLE/EDUCATIONAL)
- Attached Files (with clear instructions)
- Core Concepts
- Step-by-Step Guide
- Common Patterns
- Pitfalls to Avoid
- Examples
- References

### skill.md vs learnings.md

| File | Purpose | When Read |
|------|---------|-----------|
| `skill.md` | Canonical truth - BEFORE using | During discovery + usage |
| `learnings.md` | Practical insights - AFTER using | Only when actively using |

**Template**: `.agents/templates/learnings-template.md`

## Workflow: Skill Creation

### Phase 1: Identification (Sub-Agent)

```
Do I understand how to accomplish this?
├─ YES → Proceed
└─ NO → Existing skill covers this?
          ├─ YES → Use if approved
          └─ NO → Quick research works?
                    ├─ YES → Learn and proceed
                    └─ NO → Create skill
```

### Phase 2: Creation (Sub-Agent)

1. Research thoroughly (official docs, multiple sources)
2. Create skill directory: `mkdir -p .agents/skills/[skill-name]`
3. Create supporting files as needed (templates/, scripts/, examples/, docs/, assets/)
4. Write skill.md with complete frontmatter (`approved: No`), clear Usage Type, and unambiguous instructions
5. Report to Main Agent

### Phase 3: Review (Main Agent)

1. Read skill.md - verify frontmatter, content
2. Review all attached files for safety
3. Validate accuracy (use search)
4. Assess necessity
5. Report to user for approval

### Phase 4: User Approval

- **Approved**: Update `approved: Yes`, proceed
- **Rejected**: Use user's alternative
- **Needs Revision**: Update skill, return to Phase 3

## Skill Clarity Verification (Two Checkpoints)

### Checkpoint 1: During Requirements (Main Agent)

**When**: After requirements.md created with skills listed

1. Review each skill's `skill.md` completely
2. Verify Usage Type is clear
3. Confirm instructions are unambiguous
4. Document in requirements.md

### Checkpoint 2: Before Starting Work (Sub-Agent)

**When**: Before using skill for first time

1. Read complete skill.md
2. Read learnings.md if exists
3. Read relevant files (templates/, scripts/, examples/)
4. If unclear: STOP and report to Main Agent

## Learnings Documentation

### When Created

After skill first used, create `learnings.md` with:
- Critical implementation details
- Common failures and fixes
- Real code snippets (2-5 lines)
- Testing insights
- Integration gotchas

### Format

**Template**: `.agents/templates/learnings-template.md`

- 1-2 lines per entry
- Use `→` for cause-effect
- Show code over prose
- No verbose paragraphs

### Update Process

1. Implementation agent notes insight during work
2. Reports to Main Agent with insight
3. Main Agent creates task for specification-update agent
4. Specification-update agent updates learnings.md
5. User reviews and approves changes

## Quality Standards

### skill.md Must Be

- **Self-contained**: Essential info without needing other files
- **Unambiguous**: Clear instructions with no interpretation needed
- **Complete**: All prerequisites, steps, examples documented
- **Referenced**: Lists all files in frontmatter with descriptions

### Attached Files Must Be

- **Safe**: No security risks, no malicious code
- **Tested**: Scripts run successfully
- **Documented**: Comments explain non-obvious parts
- **Referenced**: Listed in skill.md frontmatter

## Reporting to User (Main Agent)

```
New skill created: [skill-name]

Location: .agents/skills/[skill-name]/skill.md
Type: [TEMPLATE/EXECUTABLE/EDUCATIONAL]
Purpose: [1-2 sentence summary]

Attached files:
- [file]: [purpose]

Necessity: [Why this skill is needed]
Alternatives considered: [What was tried first]

Requesting approval to use this skill.
```

## Summary

**Golden Rules:**
1. **Last resort only** - Create skills when fundamental understanding missing
2. **User approval required** - No skill used until approved
3. **Clear usage type** - TEMPLATE/EXECUTABLE/EDUCATIONAL must be explicit
4. **Self-contained** - skill.md has all essential information
5. **Never import from .agents/skills/** - Templates copied, executables run, educational patterns reimplemented
6. **Two checkpoints** - Main Agent verifies during requirements, sub-agent verifies before use

---

_Version: 1.0 - Last Updated: 2026-02-27_
