# Compact Context: [Task Name]

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:[YYYY-MM-DDTHH:MM:SSZ]|FROM:[progress.md,machine_prompt.md]

## CURRENT_TASK
task:[task_name]|status:[in_progress/blocked/testing]|started:[YYYY-MM-DDTHH:MM:SSZ]

## OBJECTIVE
[Single sentence describing what you're doing RIGHT NOW - max 15 words]

## FILES
read:[file1.rs,file2.rs]|update:[file3.rs]|create:[file4.rs]|review:[doc.md]

## REQUIREMENTS_REF
machine_prompt:[./machine_prompt.md#TASK_N]|spec:[./requirements.md#L45-67]

## KEY_CONSTRAINTS
1. [Critical constraint affecting current work]
2. [Another critical constraint]
3. [Third constraint if applicable]

## BLOCKERS
[Current blockers if any - or "NONE"]

## NEXT_ACTIONS
1. [Immediate next step]
2. [Following step]
3. [Third step if needed]

## CONTEXT_REFS
progress:[./PROGRESS.md#current-section]|learnings:[./LEARNINGS.md#relevant-section]|docs:[documentation/module/doc.md#section]

---

⚠️ **AFTER READING THIS FILE**: Clear entire context, reload from this file only, proceed with fresh minimal context

---

## Instructions for Agent

**Context Reload Protocol**:
1. Read this file completely
2. Clear ALL previous context (conversation history, file reads, everything)
3. Reload ONLY from this compact file
4. Read ONLY files listed in FILES section
5. Follow references in REQUIREMENTS_REF and CONTEXT_REFS as needed
6. Proceed with current task using minimal, focused context

**Context Size**: This file should be ~300-500 tokens. Full context after reload: ~5K-10K tokens (vs 150K+ before compaction)

**When to Regenerate**:
- After updating PROGRESS.md
- Every 50-100 agent turns
- When context approaches 150K tokens (85% of limit)
- Before switching tasks

**See**: Rule 15 (Instruction Compaction) for complete protocol
