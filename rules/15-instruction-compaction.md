# Instruction Compaction and Context Optimization

## Purpose

Establishes instruction compaction to prevent context exhaustion.

## Rule

**Read this skill**: `.agents/skills/context-optimization/skill.md`

## Summary

**Token Savings**: 97% reduction (requirements.md → COMPACT_CONTEXT.md)

**COMPACT_CONTEXT.md Lifecycle:**
1. Ephemeral and task-specific (one task only)
2. Generated fresh for each task
3. Regenerated when PROGRESS.md updates
4. Deleted when task completes
5. Never accumulates history

**Key Principles:**
- Contains ONLY current task
- Embeds machine_prompt content
- 500-800 token limit (ruthlessly compact)
- Clear and reload after regeneration
- References instead of full content

---

_Version: 2.0 - Last Updated: 2026-02-27_
