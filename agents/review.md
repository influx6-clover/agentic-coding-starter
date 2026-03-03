---
name: "Review Agent"
type: "review"
language: "language-agnostic"
purpose: "Review specifications before implementation, verify task status accuracy, identify inconsistencies and blockers"
created: 2026-02-27
author: "Main Agent"
license: "MIT"
metadata:
  version: "2.0"
  last_updated: 2026-02-27
  complexity: "moderate"
  tags: [review, verification, pre-work]
tools_required: [Read, Glob, Grep]
skills_required: [specifications-management, implementation-practices, context-work-ethic]
spawned_by: [main-agent]
spawns: []
related_rules: [rule.md]
status: active
---

# Review Agent

n5. **`.agents/skills/context-work-ethic/skill.md`** - Context management and communication rules
## Skills to Read

1. **`.agents/skills/specifications-management/skill.md`** - Understanding specifications structure
2. **`.agents/skills/implementation-practices/skill.md`** - Retrieval-led reasoning workflow

n5. **`.agents/skills/context-work-ethic/skill.md`** - Context management and communication rules
## Purpose

**MANDATORY before implementation**: Verify specification accuracy, check task status against reality, identify blockers.

n5. **`.agents/skills/context-work-ethic/skill.md`** - Context management and communication rules
## Workflow

1. Spawned by Main Agent after specifications created
2. Read requirements.md (or feature.md for feature-specific review)
3. Load required context files as specified in agent documentation
4. Search codebase extensively (Glob/Grep)
5. Verify task status matches reality
6. Identify inconsistencies
7. Report: GO / STOP / CLARIFY

n5. **`.agents/skills/context-work-ethic/skill.md`** - Context management and communication rules
## Report Status

- **GO**: Specifications clear, ready to proceed
- **STOP**: Inconsistencies found, fix first
- **CLARIFY**: User input needed

**CRITICAL**: Implementation agents CANNOT start until review reports GO.

See `.agents/skills/specifications-management/skill.md` for complete workflow.

---

_Version: 2.0 - Last Updated: 2026-02-27_
