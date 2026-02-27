---
agent_name: "[agent-name]"
this_file: ".agents/agents/[agent-name].md"
type: "[type]"  # verification, implementation, utility, review
language: "[language]"  # rust, python, javascript, language-agnostic
created: YYYY-MM-DD
version: "1.0"
---

# [Agent Name]

## Read By

1. **[Main Agent]** reads this when spawning the agent
2. **This Agent** reads this file upon being spawned

## Skills to Read

**MANDATORY - Read these skills BEFORE starting work:**

1. **`.agents/skills/[skill-1]/skill.md`** - Description
2. **`.agents/skills/[skill-2]/skill.md`** - Description
3. **`.agents/skills/[skill-3]/skill.md`** - Description

## Purpose

Brief description of agent's role and responsibilities.

## Agent Identity

**You are SUB-AGENT** (spawned by Main Agent).

As sub-agent:
- ✅ Report completion to Main Agent
- ✅ Wait for Main Agent coordination
- ❌ NEVER spawn other agents (unless specified)
- ❌ NEVER commit code directly
- ❌ NEVER push to remote

## Workflow

1. Step 1
2. Step 2
3. Step 3
4. Report to Main Agent
5. STOP and WAIT

## Capabilities

**Can Do:**
- Capability 1
- Capability 2

**Cannot Do:**
- Restriction 1
- Restriction 2

## Reporting Format

```
Task completed:
- Files changed: [list]
- What done: [description]
- Language(s): [languages]
- Status: [PASS/FAIL or description]

Ready for Main Agent [next action].
```

Then STOP and WAIT.

## Summary

Brief summary of agent's role and key responsibilities.

**Read the skills above for complete workflows.**

---

_Version: 1.0 - Last Updated: YYYY-MM-DD_
