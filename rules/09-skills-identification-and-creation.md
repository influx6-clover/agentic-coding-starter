# Skills Creation and Usage

## Purpose

Establishes how to create, review, and use skills.

## Rule

**Read this skill**: `.agents/skills/skills-management/skill.md`

## Summary

**For Main Agent (Creating Skills):**
1. Read `.agents/skills/skills-management/skill.md`
2. Create skill ONLY as last resort (fundamental understanding missing)
3. Get user approval before use

**For Sub-Agents (Using Skills):**
1. Read `.agents/skills/skills-management/skill.md`
2. Find skill in registry (scan frontmatter)
3. Verify `approved: Yes`
4. Follow Usage Type rules:
   - TEMPLATE: Copy and customize
   - EXECUTABLE: Run and consume output
   - EDUCATIONAL: Install and implement
5. Never import from `.agents/skills/` in project code

**Key Principles:**
- Skills are knowledge base, not code library
- User approval required for new skills
- Clear Usage Type for each skill
- Never import from skills directory

---

_Version: 2.0 - Last Updated: 2026-02-27_
