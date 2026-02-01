# [Specification Name] - Progress Report

> **⚠️ EPHEMERAL FILE - REWRITE PER TASK**: This file is CLEARED and REWRITTEN from scratch for each new task. It contains ONLY current task progress (no history, no future tasks).
>
> **Purpose**: Track current task/feature progress ONLY. All permanent insights → LEARNINGS.md. All completion summaries → REPORT.md.
>
> **Lifecycle**: Create for Task 1 → Update during Task 1 → CLEAR completely → Rewrite for Task 2 → Repeat
>
> **Commit Strategy**: Update this file during work. Commit happens AFTER task/feature verification passes (Rule 04).
>
> **⚠️ Machine Optimization** (Rule 14):
> - Main Agent generates `machine_prompt.md` from requirements.md/feature.md
> - Sub-agents read `machine_prompt.md` (NOT verbose human files)
> - 58% token savings: 2000→900 tokens typical
> - machine_prompt.md regenerated when human files change
> - Both files committed together (human + machine)
>
> **⚠️ Context Optimization** (Rule 15 - CRITICAL):
> - Generate `COMPACT_CONTEXT.md` before starting any task
> - EMBED machine_prompt.md content for current task in COMPACT_CONTEXT.md
> - Regenerate COMPACT_CONTEXT.md after updating this file (MANDATORY)
> - CLEAR entire context after generating COMPACT_CONTEXT.md
> - RELOAD from COMPACT_CONTEXT.md only (self-contained with embedded machine_prompt)
> - 97% context reduction: 180K→5K tokens
> - COMPACT_CONTEXT.md deleted when task completes
> - MANDATORY: Compact → Clear → Reload cycle prevents context limit errors
>
> **File Relationship**:
> ```
> requirements.md (human, 2000 tokens, always updated)
>     ↓ generate (Rule 14)
> machine_prompt.md (machine, 900 tokens, 58% savings)
>     ↓ embed in compact context (Rule 15)
> COMPACT_CONTEXT.md (ultra-compact, 500 tokens, 97% reduction)
>     ↓ read after context clear
> Agent works with 5K total context
> ```
>
> **See**:
> - Rule 14: .agents/rules/14-machine-optimized-prompts.md
> - Rule 15: .agents/rules/15-instruction-compaction.md
> - Template: .agents/templates/COMPACT_CONTEXT-template.md

---

## Current Task/Feature: [What you're working on RIGHT NOW]

**Status**: [In Progress / Testing / Blocked / Awaiting Verification]

**Started**: [Date/Time when you started this specific task/feature]

**Expected Completion**: [Estimated date/time]

---

## Progress This Session

**Completed**:
- ✅ [What was finished this session]
- ✅ [What was finished this session]

**In Progress**:
- 🔄 [What you're actively working on]

**Ready for Verification**:
- ⏳ [Implemented but awaiting verification]

---

## Immediate Next Steps

1. [Next immediate action for THIS task]
2. [Following action for THIS task]
3. [Third action if needed]

---

## Blockers/Issues for THIS Task

[Any problems or blockers for the CURRENT task, or "None"]

**If blocked**:
- What's blocking: [specific blocker]
- Waiting for: [user input / external dependency / etc.]
- Impact: [how this affects current task]

---

## Current Session Statistics

- Files modified in this session: [N]
- Lines changed in this session: [N]
- Tests added/modified: [N]
- Time spent: [approximate hours]

---

## What's Left for THIS Task

- [ ] [Remaining step 1]
- [ ] [Remaining step 2]
- [ ] [Remaining step 3]

---

## Quick Context (for resuming work)

**What I just finished**:
- ✅ [Most recent completion]
- ✅ [Previous completion]

**Where I am in the code**:
- Working in: [file/module path]
- Current focus: [specific function/feature]

---

## Notes for Next Session

[Any quick notes or reminders for when work resumes]

---

## When to Clear/Rewrite This File

✅ **Clear and rewrite** when:
- Completed this major task/phase
- Switching to different task/feature
- Major milestone reached
- Coming back after break (write fresh status)

✅ **Delete this file** when:
- ALL tasks complete (100%)
- Ready to create FINAL_REPORT.md
- Specification being marked as complete

✅ **Transfer to LEARNINGS.md** before clearing:
- Any insights or lessons learned from this task
- Design decisions or architectural choices
- Problems solved and how
- Patterns that worked well or poorly

---

*Progress Report Last Updated: [Date and Time]*

*⚠️ Remember: This is EPHEMERAL. Permanent insights go to LEARNINGS.md*
