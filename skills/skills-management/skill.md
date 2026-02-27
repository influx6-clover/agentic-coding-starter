---
name: "Skills Management"
description: "Complete guide for creating, reviewing, and using skills in the .agents/skills/ directory"
approved: Yes
created: 2026-02-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-27"
  tags: [skills, creation, usage, documentation, management]
tools: []
files: []
---

# Skills Management

## Overview

Complete guide for creating, reviewing, documenting, and using skills. Covers both Main Agent (creating skills) and Sub-Agents (using skills).

**Usage Type**: EDUCATIONAL - Learn skill management patterns.

## When to Use

**For Main Agent (Creating Skills):**
- Need to document complex technical task
- Tool/library usage needs documentation
- Pattern implementation should be captured
- Problem solution should be reusable

**For Sub-Agents (Using Skills):**
- Task requires specific skill
- Need to understand how to use skill
- Implementing pattern from skill

## Prerequisites

- Understanding of skill directory structure
- Access to `.agents/skills/` directory
- Familiarity with skill templates

## Skill Types (Usage Types)

### 1. TEMPLATE (Copy and Customize)
- Files in `templates/` copied to project
- Agent customizes copied files
- Import from project location (NOT `.agents/skills/`)

### 2. EXECUTABLE (Run as Tools)
- Scripts in `scripts/` run as external commands
- Consume output in project
- Never modify scripts

### 3. EDUCATIONAL (Learn and Implement)
- Examples in `examples/` teach patterns
- Install external dependencies
- Write fresh implementation
- Never import from `.agents/skills/`

**Golden Rule**: `.agents/skills/` is knowledge base, NOT code library.

## Creating Skills (Main Agent)

### When to Create

Create skill ONLY when:
- Fundamental understanding is missing
- No existing skill covers the need
- No alternative approach possible
- NOT for trivial tasks
- NOT for basic programming

### Creation Workflow

**Phase 1: Identification (Sub-Agent)**
```
Do I understand how to do this?
├─ YES → Proceed
└─ NO → Existing skill?
          ├─ YES → Use if approved
          └─ NO → Quick research works?
                    ├─ YES → Learn and proceed
                    └─ NO → Create skill
```

**Phase 2: Creation (Sub-Agent)**
1. Research thoroughly (official docs, multiple sources)
2. Create skill directory: `mkdir -p .agents/skills/[skill-name]`
3. Create supporting files:
   - `templates/` for TEMPLATE skills
   - `scripts/` for EXECUTABLE skills
   - `examples/` for EDUCATIONAL skills
   - `docs/` for extended documentation
   - `assets/` for diagrams, configs
4. Write `skill.md`:
   - Complete frontmatter (`approved: No`)
   - Clear Usage Type
   - Reference all files in `files` field
   - Unambiguous instructions
5. Report to Main Agent

**Phase 3: Review (Main Agent)**
1. Read skill.md - verify frontmatter, content
2. Review all attached files for safety
3. Validate accuracy (use search)
4. Assess necessity
5. Report to user for approval

**Phase 4: User Approval**
- **Approved**: Update `approved: Yes`, proceed
- **Rejected**: Use user's alternative
- **Needs Revision**: Update skill, return to Phase 3

### Skill Directory Structure

```
.agents/skills/[skill-name]/
├── skill.md           # REQUIRED - Main documentation
├── learnings.md       # OPTIONAL - Practical insights
├── assets/            # OPTIONAL - Diagrams, configs, data
├── docs/              # OPTIONAL - Extended documentation
├── templates/         # OPTIONAL - Code templates (TEMPLATE)
├── scripts/           # OPTIONAL - Executable scripts (EXECUTABLE)
└── examples/          # OPTIONAL - Reference implementations (EDUCATIONAL)
```

### Naming Convention

- Use kebab-case: `playwright-web-interaction`
- NO numeric prefixes
- Name clearly describes purpose

### Frontmatter Requirements

```yaml
---
name: "Skill Name"
description: "1-2 sentence summary"
approved: No  # Change to Yes after user approval
created: YYYY-MM-DD
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "YYYY-MM-DD"
  tags: [tag1, tag2]
tools: [Tool1, Tool2]
files:
  - templates/client.ts: "API client template"
  - scripts/run.sh: "Execution script"
assets:
  - docs/deep-dive.md: "Extended explanation"
---
```

**Required**: `name`, `description`, `approved`, `created`, `license`, `metadata`, `tools`

### Content Structure

**Template**: `.agents/templates/skill-template.md`

**Key Sections:**
1. Overview (2-3 paragraphs)
2. When to Use (scope and limitations)
3. Prerequisites (knowledge, dependencies)
4. Usage Type declaration (TEMPLATE/EXECUTABLE/EDUCATIONAL)
5. Attached Files (with clear instructions)
6. Core Concepts
7. Step-by-Step Guide
8. Common Patterns
9. Pitfalls to Avoid
10. Examples
11. References

### Duplicate Prevention

**Before creating:**
1. Scan existing `.agents/skills/*/skill.md` frontmatter
2. Check if similar skill exists
3. If duplicate: Merge into single file
4. If similar but different: Ensure clear differentiation

## Using Skills (Sub-Agents)

### Finding Skills

1. Scan `.agents/skills/` directory
2. Read frontmatter only (first 20 lines)
3. Check `approved: Yes` before using
4. Match by name/description to task

```bash
# Efficient scan
for skill in .agents/skills/*/skill.md; do
  head -n 20 "$skill"
done
```

### Before Using

1. Verify `approved: Yes` in frontmatter
2. Read complete `skill.md`
3. Read `learnings.md` if exists
4. Check Usage Type (TEMPLATE/EXECUTABLE/EDUCATIONAL)
5. Read relevant files from subdirectories
6. Perform clarity check - understand all instructions?

### Using TEMPLATE Skills

```bash
# 1. Copy ALL files from templates/ to project
cp .agents/skills/[skill-name]/templates/*.ts ./src/[destination]/

# 2. Customize the COPIED files
# 3. Import from PROJECT location, NOT .agents/skills/
```

**Rules:**
- Copy ALL files from `templates/`
- Customize copied files in project
- Import from project location
- NEVER import from `.agents/skills/`

### Using EXECUTABLE Skills

```bash
# 1. Run script from scripts/ directory
node .agents/skills/[skill-name]/scripts/run.js --arg value

# 2. Capture and use output
```

**Rules:**
- Execute scripts from `scripts/` location
- Capture and use output
- Never copy or modify scripts
- Never import from `.agents/skills/`

### Using EDUCATIONAL Skills

```bash
# 1. Install external dependencies
npm install [package-name]

# 2. Study examples in examples/
# 3. Write fresh implementation in project
```

**Rules:**
- Install external libraries (NPM, PyPI, Cargo)
- Study examples to learn patterns
- Write fresh code in project
- NEVER import from `.agents/skills/`

### When Skill is Unclear

If instructions unclear:
1. STOP immediately
2. Report to Main Agent with specific problem
3. Wait for clarification

### When Skill is Unapproved

If `approved: No`:
```
Cannot proceed. Required skill not approved.
Awaiting user approval to continue.
```

**NEVER use unapproved skills.**

## Modular Skills

For complex related skills:

```
skills/[parent-skill-name]/
├── skill.md              # Main entry point
├── [topic-1]/skill.md   # Sub-skill
├── [topic-2]/skill.md   # Sub-skill
└── [topic-3]/skill.md   # Sub-skill
```

**Main skill.md:**
- Overview of scope
- Navigation to sub-skills in `files:` field
- Table of sub-skills with descriptions

**Sub-skill.md:**
- Complete standalone documentation
- Can be used independently
- All standard sections

## Learning Documentation

### When Created

After skill first used, create `learnings.md`:
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

1. Implementation agent notes insight
2. Reports to Main Agent with insight
3. Main Agent creates task for specification-update agent
4. Agent updates learnings.md
5. User reviews and approves

## Quality Standards

### skill.md Must Be

- **Self-contained**: Essential info without needing other files
- **Unambiguous**: Clear instructions, no interpretation
- **Complete**: All prerequisites, steps, examples
- **Referenced**: Lists all files in frontmatter

### Attached Files Must Be

- **Safe**: No security risks, no malicious code
- **Tested**: Scripts run successfully
- **Documented**: Comments explain non-obvious parts
- **Referenced**: Listed in skill.md frontmatter

## Quick Reference Table

| Usage Type | Source | Action | Import From |
|-----------|---------|--------|-------------|
| TEMPLATE | `templates/` | Copy ALL files, customize | Project location |
| EXECUTABLE | `scripts/` | Run script, use output | N/A (external tool) |
| EDUCATIONAL | `examples/` | Install lib, write fresh | External package |

## Common Patterns

### Pattern: Creating TEMPLATE Skill

```
1. Identify reusable code pattern
2. Create skill directory
3. Extract code to templates/
4. Write skill.md with usage instructions
5. Test: Copy templates to test project, verify works
6. Submit for review
```

### Pattern: Creating EDUCATIONAL Skill

```
1. Research library/pattern thoroughly
2. Create examples/ directory
3. Write multiple examples (basic, intermediate, advanced)
4. Document gotchas and best practices
5. List external dependencies
6. Submit for review
```

### Pattern: Using Skill in Project

```
1. Find skill in registry
2. Read skill.md completely
3. Read learnings.md if exists
4. Follow Usage Type instructions:
   - TEMPLATE: Copy files
   - EXECUTABLE: Run scripts
   - EDUCATIONAL: Install libs, implement
5. Report completion to Main Agent
```

## Pitfalls to Avoid

**❌ Don't:**
- Create skills for trivial tasks
- Import from `.agents/skills/` in project code
- Use unapproved skills
- Skip reading complete skill.md
- Embed complete templates in rule files
- Create duplicate skills

**✅ Do:**
- Create skills for complex/reusable tasks
- Copy templates to project, import from there
- Verify approval before using
- Read all documentation before using
- Reference templates from skills or current configuration
- Check for duplicates before creating

## Summary

**Creating Skills:**
1. Last resort only (fundamental understanding missing)
2. Research thoroughly
3. Create directory with supporting files
4. Write complete skill.md
5. Get user approval

**Using Skills:**
1. Find skill (scan frontmatter)
2. Verify approved
3. Read complete documentation
4. Follow Usage Type rules:
   - TEMPLATE: Copy and customize
   - EXECUTABLE: Run and consume
   - EDUCATIONAL: Install and implement
5. Never import from `.agents/skills/`

**Key Principles:**
- Skills are knowledge base, not code library
- Always get user approval for new skills
- Clear Usage Type for each skill
- Self-contained documentation
- Never import from skills directory in project

---

_Version: 1.0 - Last Updated: 2026-02-27_
