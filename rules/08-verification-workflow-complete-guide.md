# Verification Workflow

## Purpose

Establishes iron-clad verification workflow ensuring **NO code is EVER committed without passing ALL quality checks**. **ZERO TOLERANCE** for violations.

## Rule

**Read this skill**: `.agents/skills/code-verification/skill.md`

## Summary

**Verification agents must:**
1. Read `.agents/skills/code-verification/skill.md`
2. Run ALL checks from language stack file
3. Report PASS/FAIL to Main Agent

**Main Agent must:**
1. Spawn verification agents (one per language)
2. Wait for ALL checks to pass
3. Commit ONLY after verification passes
4. Include verification status in commit message

**Key Principles:**
- NO code committed without verification
- ONLY Main Agent spawns verification agents
- ALL checks must pass (no exceptions)
- Check incomplete implementations FIRST
- Fix ALL failures before commit

---

_Version: 2.0 - Last Updated: 2026-02-27_
