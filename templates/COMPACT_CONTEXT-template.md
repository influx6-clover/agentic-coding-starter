# Compact Context: [Task Name]

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:[YYYY-MM-DDTHH:MM:SSZ]|FROM:[machine_prompt.md,progress.md]

## CURRENT_TASK
task:[task_name]|status:[in_progress/blocked/testing]|started:[YYYY-MM-DDTHH:MM:SSZ]

## MACHINE_PROMPT_CONTENT
[EMBEDDED CONTENT FROM machine_prompt.md FOR THIS SPECIFIC TASK ONLY]

spec:[spec_name]|status:[status]|priority:[priority]
req:[current_task_requirement]|constraints:[...]|success:[...]
task:[current_task_name]|files:[...]|tests:[...]|deps:[...]
tech:stack=[...]|pattern:[...]|error_handling:[...]
verify:scripts=[...]|tests:[...]|coverage:[...]

## OBJECTIVE
[Single sentence describing what you're doing RIGHT NOW - max 15 words]

## FILES
read:[file1.rs,file2.rs]|update:[file3.rs]|create:[file4.rs]|review:[doc.md]

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

**CRITICAL**: This file is self-contained. After context clear, read ONLY this file.

**Machine Prompt Content**: The MACHINE_PROMPT_CONTENT section contains all requirements
for current task. You do NOT need to read machine_prompt.md separately after reload.

**Context Reload Protocol**:
1. Read this file completely
2. Clear ALL previous context (conversation history, file reads, everything)
3. Reload ONLY from this compact file
4. Read ONLY files listed in FILES section
5. Follow references in CONTEXT_REFS as needed (not full reads)
6. Proceed with current task using minimal, focused context

**Context Size**: This file should be ~500-800 tokens. Full context after reload: ~5K-10K tokens (vs 150K+ before compaction)

**Ephemeral Nature**:
- Generated fresh for each task
- Regenerated after PROGRESS.md updates
- Deleted when task completes
- Never accumulates history
- Always reflects "now" only

**When to Regenerate**:
- After updating PROGRESS.md (MANDATORY)
- Every 50-100 agent turns
- When context approaches 150K tokens (85% of limit)
- Before switching tasks
- Task status changes

**When to Delete**:
- Current task fully completes
- Moving to next task
- Specification work complete

**See**: Rule 15 (Instruction Compaction) for complete protocol
