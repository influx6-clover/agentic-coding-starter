---
name: "Context Optimization"
description: "Complete guide for machine-optimized prompts and instruction compaction to prevent context exhaustion"
approved: Yes
created: 2026-02-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-27"
  tags: [context, optimization, compaction, machine-prompts, efficiency]
tools: []
files: []
---

# Context Optimization

## Overview

Complete guide for generating machine-optimized prompts and ultra-compact instruction summaries to prevent context limit exhaustion and optimize token usage.

**Usage Type**: EDUCATIONAL - Learn context optimization patterns.

**Token Savings**: 40-60% (machine prompts) + 97% (compaction) = Massive efficiency

## When to Use

**For Main Agent:**
- Creating/updating specifications
- Generating machine_prompt.md from requirements.md
- Generating COMPACT_CONTEXT.md for sub-agents
- Before spawning sub-agents

**For Sub-Agents:**
- Reading machine_prompt.md instead of requirements.md
- Generating/updating COMPACT_CONTEXT.md during work
- Context approaching limits (proactive compaction)

## Prerequisites

- Understanding of specification structure
- Access to requirements.md/feature.md files
- Familiarity with PROGRESS.md lifecycle

## Two-Level Optimization

### Level 1: Machine-Optimized Prompts (40-60% savings)

```
requirements.md (human, 2000 tokens)
    ↓ Generate
machine_prompt.md (machine, 900 tokens, 58% reduction)
```

### Level 2: Instruction Compaction (97% total savings)

```
requirements.md (2000 tokens)
    ↓ Generate machine_prompt.md
machine_prompt.md (900 tokens)
    ↓ Extract current task + embed
COMPACT_CONTEXT.md (500 tokens, 97% reduction from original)
```

## Machine-Optimized Prompts

### When to Generate

Main Agent MUST generate `machine_prompt.md` when:
1. Specification created (after requirements.md finalized/approved)
2. Feature created (after feature.md written)
3. Specification updated (requirements.md/feature.md changes)
4. Before implementation starts
5. Before spawning sub-agents

### Location

```
specifications/01-spec/
├── requirements.md          # Human-readable (DO NOT DELETE)
├── machine_prompt.md        # Machine-optimized (GENERATED)
├── features/00-feature/
│   ├── feature.md          # Human-readable (DO NOT DELETE)
│   └── machine_prompt.md   # Machine-optimized (GENERATED)
```

**CRITICAL:**
- NEVER delete human-readable files
- ALWAYS regenerate machine_prompt.md when human files change
- machine_prompt.md is GENERATED, not hand-edited

### Format

```markdown
# Machine-Optimized Prompt: [Name]

⚠️GENERATED|DO_NOT_EDIT|REGENERATE_FROM:[source]|GENERATED:[timestamp]

## META
spec:[name]|num:[NN]|status:[status]|priority:[priority]

## LOCATION
workspace:[ewe_platform]|spec_dir:[path]|this_file:[file]

## DOCS_TO_READ
requirements.md|feature.md|.agents/stacks/rust.md

## REQUIREMENTS
req1:[description]|constraints:[...]|success:[...]
req2:[description]|constraints:[...]|success:[...]

## TASKS
[x]task1:[description]|files:[file1,file2]|tests:[test1]
[ ]task2:[description]|depends:[task1]|files:[file3]

## TECHNICAL
stack:[rust,tokio]|location:[src/http/]|dependencies:[dep1,dep2]

## VERIFICATION
scripts:[verify.py]|tests:[unit,integration]|coverage:[90%]

## SUCCESS_CRITERIA
criteria1:[description]|measurable:[metric]
```

### Compression Rules

1. **Remove whitespace**: "This is a description" → "description"
2. **Pipe-delimited**: Sections separated by `|`
3. **Abbreviate**: "specification" → "spec", "requirement" → "req"
4. **Compress tasks**: All info on one line with `|` separators
5. **Inline multi-line**: Flatten nested content

### Generation Process

1. Read requirements.md or feature.md completely
2. Extract all critical information
3. Apply compression rules
4. Generate machine_prompt.md with pipe-delimited format
5. Save to same directory as source
6. Commit BOTH files together
7. Clear context and reload from machine_prompt.md

### Dual File Maintenance

**Human Files (requirements.md, feature.md):**
- Always updated as normal
- Source of truth for humans
- Never deleted
- Edited directly when changed
- Committed with changes
- Verbose and formatted

**Machine Files (machine_prompt.md):**
- Generated automatically from human files
- Regenerated when human files change
- Used by all agents for instructions
- Committed alongside human files
- Compressed and pipe-delimited
- Never hand-edited
- Never becomes sole source

**Synchronization:**
```
Edit requirements.md → Regenerate machine_prompt.md →
Clear context → Reload from machine_prompt.md →
Commit BOTH → Agents use machine → Humans read requirements
```

## Instruction Compaction

### COMPACT_CONTEXT.md Lifecycle

**Ephemeral and Task-Specific:**
1. Generated fresh for each new task
2. Contains ONLY current task (no history, no future)
3. Regenerated every time PROGRESS.md updates
4. Cleared and rewritten when task completes
5. Never accumulates (always reflects "now" only)
6. Deleted when task fully complete

**Size Limit**: NEVER exceed 500-800 tokens

### Contents

**Contains:**
- Current task name and status
- Current objective (what doing RIGHT NOW)
- Files relevant to current task only
- Key constraints affecting current work
- Current blockers (if any)
- Immediate next actions (1-3 steps)
- **Embedded machine_prompt.md content** for current task
- References to other files (not their content)

**Must NOT Contain:**
- Historical context (completed tasks)
- Future tasks or plans
- Full file contents (use references)
- Verbose explanations
- Accumulated progress from multiple tasks

### Format

```markdown
# Compact Context: [Task Name]

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:[timestamp]

## CURRENT_TASK
task:[name]|status:[status]|started:[timestamp]

## MACHINE_PROMPT_CONTENT
[EMBEDDED CONTENT FROM machine_prompt.md FOR THIS TASK]
spec:[name]|priority:[high]
req:[description]|constraints:[...]
task:[name]|files:[file1,file2]|tests:[test1]

## OBJECTIVE
[1-line description of current objective]

## FILES
read:[file1,file2]|update:[file3]|create:[file4]

## CONSTRAINTS
[Key constraints affecting current work]

## BLOCKERS
[Current blockers or "none"]

## NEXT_ACTIONS
1. [Action 1]
2. [Action 2]
3. [Action 3]

## REFERENCES
machine_prompt:[path#section]|requirements:[path]|stack:[path]
```

### Why Embed machine_prompt Content

COMPACT_CONTEXT.md is ONLY file loaded after context clear. Must be self-contained with all critical task information. Embedding ensures:
- No need to re-read machine_prompt.md after reload
- Single source after compaction
- All context in one place

### Lifecycle Pattern

```
Task 1 starts → Generate COMPACT_CONTEXT.md (task 1 only) →
Task 1 updates → Regenerate COMPACT_CONTEXT.md (task 1 only) →
Task 1 completes → DELETE COMPACT_CONTEXT.md →
Task 2 starts → Generate NEW COMPACT_CONTEXT.md (task 2 only)
```

### When to Compact

Sub-agents MUST generate COMPACT_CONTEXT.md when:
1. Starting new task (initial compaction)
2. After updating PROGRESS.md
3. Context approaching limits (proactive compaction)
4. Before complex operations requiring clean context

### Compaction Process

1. **Read Sources**: machine_prompt.md + PROGRESS.md
2. **Extract Current Task**: Only information for RIGHT NOW
3. **Embed machine_prompt**: Include relevant content
4. **Add Files Section**: List files for current task
5. **Add Constraints**: Key constraints only
6. **Add Next Actions**: 1-3 immediate steps
7. **Generate File**: Create COMPACT_CONTEXT.md
8. **Verify Size**: MUST be 500-800 tokens max
9. **Clear Context**: Clear entire conversation context
10. **Reload**: Read ONLY COMPACT_CONTEXT.md + FILES section

## PROGRESS.md Lifecycle

**Ephemeral and Task-Specific:**
1. Rewritten from scratch when starting new task
2. Contains ONLY current task (no cumulative history)
3. Updated as current task progresses
4. Cleared completely when task completes
5. Rewritten fresh for next task
6. Deleted when specification 100% complete

**Contents:**
- Current task/feature RIGHT NOW
- Current status and progress on THIS task
- Blockers for THIS task
- Next steps for THIS task
- Recent work on THIS task only

**Must NOT Contain:**
- Historical progress from previous tasks
- Completed task summaries (goes to REPORT.md)
- Accumulated updates from multiple tasks

**When Task Completes:**
1. Extract learnings → Add to LEARNINGS.md (permanent)
2. Extract completion summary → Add to REPORT.md (permanent)
3. CLEAR PROGRESS.md completely
4. DELETE COMPACT_CONTEXT.md
5. Ready for next task

## Agent Reading Flow

### Initial Load (Before Compaction)

```
1. Read machine_prompt.md (58% compressed from requirements.md)
2. Read PROGRESS.md
3. Understand full context
```

### Generate COMPACT_CONTEXT.md

```
1. Extract current task from machine_prompt.md
2. Extract current status from PROGRESS.md
3. EMBED machine_prompt.md content for current task
4. Add files, constraints, next actions
5. Create ultra-compact self-contained file
```

### After Compaction (Clean Slate)

```
1. CLEAR entire context
2. Read ONLY COMPACT_CONTEXT.md (contains embedded machine_prompt)
3. Read ONLY files listed in FILES section
4. Work with minimal focused context
```

## File Relationship

```
requirements.md (human, permanent, 2000 tokens)
    ↓ [Generate]
machine_prompt.md (machine, permanent, 900 tokens, 58% reduction)
    ↓ [Extract current task + embed]
COMPACT_CONTEXT.md (ultra-compact, ephemeral, 500 tokens, 97% reduction)
    ↓ [Self-contained with embedded machine content]
Agent reads ONLY this after context clear
```

## Main Agent Responsibilities

### Generate machine_prompt.md

1. After requirements.md/feature.md finalized
2. Extract all critical information
3. Apply compression rules
4. Save to same directory
5. Commit both human and machine files
6. Clear context, reload from machine file

### Generate Initial COMPACT_CONTEXT.md

1. Before spawning sub-agent
2. Extract first task from machine_prompt.md
3. Embed machine_prompt content
4. Create compact file (500-800 tokens)
5. Provide path to sub-agent

### Verify Compaction

1. Verify COMPACT_CONTEXT.md exists
2. Check size (500-800 tokens max)
3. Ensure machine_prompt content embedded
4. Confirm FILES section lists only current task files
5. Validate no historical content

## Sub-Agent Responsibilities

### Use COMPACT_CONTEXT.md

1. Read COMPACT_CONTEXT.md (NOT requirements.md or full machine_prompt.md)
2. Read ONLY files in FILES section
3. Work within constraints
4. Update PROGRESS.md as progressing
5. Regenerate COMPACT_CONTEXT.md after PROGRESS.md updates
6. Clear and reload context after regeneration

### Regeneration Trigger

Regenerate when:
1. PROGRESS.md updated
2. Context growing large
3. Task status changes
4. New blockers discovered
5. Files list changes

## Benefits

1. **40-60% Token Reduction**: machine_prompt.md vs requirements.md
2. **97% Total Reduction**: COMPACT_CONTEXT.md vs requirements.md
3. **Prevents Context Exhaustion**: Regular compaction keeps context small
4. **Improved Focus**: Only current task present
5. **Faster Processing**: Less content to read

## Common Patterns

### Pattern: Specification Creation

```
1. Create requirements.md (human file)
2. Get user approval
3. Generate machine_prompt.md (compress)
4. Clear context
5. Reload from machine_prompt.md
6. Commit both files
```

### Pattern: Starting Task

```
1. machine_prompt.md exists
2. Generate COMPACT_CONTEXT.md for task 1:
   - Embed machine_prompt content for task 1
   - Add task 1 files
   - Add task 1 constraints
3. Spawn sub-agent with COMPACT_CONTEXT path
4. Sub-agent clears context
5. Sub-agent reads only COMPACT_CONTEXT.md + listed files
```

### Pattern: During Task Execution

```
1. Sub-agent working on task
2. Updates PROGRESS.md
3. Regenerates COMPACT_CONTEXT.md:
   - Still only task 1
   - Updated status from PROGRESS.md
   - Same embedded machine_prompt
4. Clears context
5. Reloads from regenerated COMPACT_CONTEXT.md
```

### Pattern: Task Completion

```
1. Task complete
2. Extract learnings → LEARNINGS.md
3. Extract summary → REPORT.md
4. CLEAR PROGRESS.md
5. DELETE COMPACT_CONTEXT.md
6. Generate NEW COMPACT_CONTEXT.md for task 2
```

## Pitfalls to Avoid

**❌ Don't:**
- Delete human-readable files
- Hand-edit machine_prompt.md
- Let COMPACT_CONTEXT.md accumulate history
- Include full file contents in compact file
- Use COMPACT_CONTEXT.md across multiple tasks
- Skip context clear after compaction
- Read verbose files after compaction
- Exceed 800 token limit

**✅ Do:**
- Maintain both human and machine files
- Regenerate machine_prompt when human changes
- Keep compact file ephemeral (one task only)
- Use references instead of content
- Generate fresh compact for each task
- Clear and reload after compaction
- Read only compact file after clear
- Ruthlessly compress (500-800 tokens max)

## Summary

**Two-Level Optimization:**
1. **Machine Prompts**: requirements.md (2000) → machine_prompt.md (900) = 58% reduction
2. **Compaction**: machine_prompt.md (900) → COMPACT_CONTEXT.md (500) = 97% total reduction

**Workflow:**
```
Create requirements.md → Generate machine_prompt.md → Clear & Reload →
Generate COMPACT_CONTEXT.md → Clear & Reload → Work with minimal context
```

**Key Principles:**
1. Dual file maintenance (human + machine)
2. COMPACT_CONTEXT.md is ephemeral (one task only)
3. Embed machine_prompt content in compact file
4. Clear and reload after compaction
5. 500-800 token limit for compact file
6. Regenerate when PROGRESS.md updates

---

_Version: 1.0 - Last Updated: 2026-02-27_
