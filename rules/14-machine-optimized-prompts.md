# Machine-Optimized Prompts and Context Optimization

## Purpose

Establishes machine-optimized prompts and instruction compaction to prevent context exhaustion.

## Rule

**Read this skill**: `.agents/skills/context-optimization/skill.md`

## Summary

**Token Savings**: 40-60% (machine prompts) + 97% (compaction) = Massive efficiency

**For Main Agent:**
1. Read `.agents/skills/context-optimization/skill.md`
2. Generate machine_prompt.md from requirements.md (58% reduction)
3. Generate COMPACT_CONTEXT.md for sub-agents (97% total reduction)
4. Provide COMPACT_CONTEXT path when spawning

**For Sub-Agents:**
1. Read `.agents/skills/context-optimization/skill.md`
2. Read COMPACT_CONTEXT.md (NOT requirements.md)
3. Regenerate COMPACT_CONTEXT.md after PROGRESS.md updates
4. Clear and reload context after regeneration

**Key Principles:**
- Dual file maintenance (human + machine)
- COMPACT_CONTEXT.md is ephemeral (one task only)
- 500-800 token limit for compact file
- Clear and reload after compaction

---

_Version: 2.0 - Last Updated: 2026-02-27_
