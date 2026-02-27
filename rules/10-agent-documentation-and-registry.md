# Agent Documentation and Registry

## Purpose

Establishes how to document and use agents in the registry.

## Rule

**Read this skill**: `.agents/skills/agent-documentation/skill.md`

## Summary

**For Main Agent (Creating/Spawning):**
1. Read `.agents/skills/agent-documentation/skill.md`
2. Create documentation with complete frontmatter
3. Write clear purpose (10-15 words)
4. Check for duplicates
5. Provide documentation path when spawning

**For Sub-Agents (Using):**
1. Read `.agents/skills/agent-documentation/skill.md`
2. Receive documentation path from Main Agent
3. Read complete documentation FIRST
4. Load required rules and skills
5. Follow documented workflow

**Key Principles:**
- Documentation path MANDATORY when spawning
- Frontmatter enables fast selection
- Purpose must be crystal clear
- Never spawn undocumented agents

---

_Version: 2.0 - Last Updated: 2026-02-27_
