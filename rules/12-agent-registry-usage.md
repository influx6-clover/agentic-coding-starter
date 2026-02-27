# Agent Registry Usage (For Sub-Agents)

## Purpose

Concise guide for sub-agents using agent registry.

## Rule

**Read this skill**: `.agents/skills/agent-documentation/skill.md`

## Summary

**Sub-Agent Startup:**
1. Receive documentation path from Main Agent
2. Read `.agents/agents/[name].md` FIRST
3. Load Rules 01-04 (mandatory)
4. Load Rule 11 (if using skills)
5. Begin work following documented workflow

**Key Principles:**
- Documentation path required
- Read documentation before starting
- Stay within boundaries
- Report completion to Main Agent
- Never spawn verification agents
- Never commit directly

---

_Version: 2.0 - Last Updated: 2026-02-27_
