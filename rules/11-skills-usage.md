# Skills Usage Guide (For Sub-Agents)

## Purpose

Concise guide for sub-agents who need to use existing skills. For skill creation and review, Main Agent should load Rule 09.

## Finding Skills

1. Scan `.agents/skills/` directory
2. Read only frontmatter (first 20 lines) of `skill.md` files
3. Check `approved: Yes` before using
4. Match by name/description to task needs

```bash
# Efficient scan - frontmatter only
for skill in .agents/skills/*/skill.md; do
  head -n 20 "$skill"
done
```

## Before Using a Skill

1. Verify `approved: Yes` in frontmatter
2. Read complete `skill.md`
3. Read `learnings.md` if exists
4. Check Usage Type (TEMPLATE/EXECUTABLE/EDUCATIONAL)
5. Read relevant files from subdirectories
6. Perform clarity check - understand all instructions?

## Skill Directory Structure

```
.agents/skills/[skill-name]/
├── skill.md        # Required - main doc (always read)
├── learnings.md    # Optional - practical insights
├── assets/         # Optional - diagrams, configs, data
├── docs/           # Optional - extended documentation
├── templates/      # Optional - for TEMPLATE skills
├── scripts/        # Optional - for EXECUTABLE skills
└── examples/       # Optional - for EDUCATIONAL skills
```

## Three Skill Usage Types

### 1. TEMPLATE (Copy and Customize)

**Identified by**: `Usage Type: TEMPLATE` in skill.md

**Actions:**
1. Copy ALL files from `templates/` to project
2. Customize the COPIED files
3. Import from project location (NOT `.agents/skills/`)

```bash
cp .agents/skills/[skill-name]/templates/*.ts ./src/[destination]/
```

### 2. EXECUTABLE (Run as Tools)

**Identified by**: `Usage Type: EXECUTABLE` in skill.md

**Actions:**
1. Run script from `scripts/` directory
2. Capture and use output
3. Never copy or modify scripts
4. Never import from `.agents/skills/`

```bash
node .agents/skills/[skill-name]/scripts/run.js --arg value
```

### 3. EDUCATIONAL (Learn and Implement)

**Identified by**: `Usage Type: EDUCATIONAL` in skill.md

**Actions:**
1. Install external dependencies listed in skill
2. Study examples in `examples/`
3. Write fresh implementation in project
4. Never import from `.agents/skills/`

```bash
npm install [package-name]
```

## CRITICAL: Skills Directory Isolation

```
❌ NEVER do this in project code:
   import { something } from '.agents/skills/...'

✅ ALWAYS do this:
   - TEMPLATE: Copy from templates/, import from project
   - EXECUTABLE: Run from scripts/, use output
   - EDUCATIONAL: Install lib, write fresh code
```

**Golden Rule**: `.agents/skills/` is a knowledge base, NOT a code library. Never import from it in project code.

## When Skill is Unclear

If instructions are unclear:
1. STOP immediately
2. Report to Main Agent with specific problem
3. Wait for clarification before proceeding

## When Skill is Unapproved

If skill has `approved: No`:
```
Cannot proceed. Required skill not approved.
Awaiting user approval to continue.
```

**NEVER use unapproved skills.**

## After Using a Skill

If you discover useful insights:
1. Note the insight
2. Report to Main Agent
3. Main Agent coordinates learnings.md update (requires user approval)

## Quick Reference Table

| Usage Type | Source | Action | Import From |
|-----------|---------|--------|-------------|
| TEMPLATE | `templates/` | Copy ALL files, customize | Project location |
| EXECUTABLE | `scripts/` | Run script, use output | N/A (external tool) |
| EDUCATIONAL | `examples/` | Install lib, write fresh | External package |

---

_Version: 1.0 - Last Updated: 2026-02-27_
