# Instruction Compaction and Context Optimization

## Purpose

Establish mandatory practice of creating ultra-compact instruction summaries preserving only critical information for current work. Prevents context limit exhaustion and ensures clean, focused context.

**Key Insight**: Most context is historical; only 10-20% matters for current task. Compact ruthlessly.

## Core Principle

**Verbose Context → Compacted Instructions → Context Reload → Clean Workspace**

- Long files exhaust context windows
- Compacted files preserve only current-work essentials
- References replace content duplication
- Regular reloading prevents context bloat

## COMPACT_CONTEXT.md Lifecycle (MANDATORY)

### Ephemeral and Task-Specific

**COMPACT_CONTEXT.md is:**
1. Generated fresh for each new task
2. Contains ONLY current task - no history, no future
3. Regenerated every time PROGRESS.md updates
4. Cleared and rewritten from scratch when task completes
5. Never accumulates - always reflects "now" only
6. Deleted when task fully complete

### Contents

**Contains:**
- Current task name and status
- Current objective (what you're doing RIGHT NOW)
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
- Content from previous task iterations

**Size Limit**: NEVER exceed 500-800 tokens. If larger, compress more aggressively.

### Lifecycle Pattern

```
Task 1 starts → Generate COMPACT_CONTEXT.md (task 1 only) →
Task 1 updates → Regenerate COMPACT_CONTEXT.md (task 1 only) →
Task 1 completes → DELETE COMPACT_CONTEXT.md →
Task 2 starts → Generate NEW COMPACT_CONTEXT.md (task 2 only) →
[Repeat for each task]
```

## machine_prompt.md Integration

### Embedding in COMPACT_CONTEXT.md

COMPACT_CONTEXT.md MUST include machine_prompt.md content for current task:

```markdown
# Compact Context: Implement DNS Resolver

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:[timestamp]

## CURRENT_TASK
task:impl_dns_resolver|status:in_progress|started:[timestamp]

## MACHINE_PROMPT_CONTENT
[EMBEDDED CONTENT FROM machine_prompt.md FOR THIS TASK]
spec:http-client|priority:high
req:impl DnsResolver trait|cache:LRU,ttl=300s|async:tokio
task:impl_dns_resolver|files:[src/dns.rs]|tests:[tests/dns_tests.rs]

## OBJECTIVE
Impl DnsResolver trait with LRU caching per machine_prompt.md#TASK_1

## FILES
read:[src/http_client.rs]|update:[src/dns_resolver.rs]|create:[tests/dns_tests.rs]

## NEXT_ACTIONS
1. Read existing DNS code patterns
2. Impl trait skeleton
3. Add LRU cache
```

**Why Embed**: COMPACT_CONTEXT.md is the ONLY file loaded after context clear. Must be self-contained with all critical task information.

### Agent Reading Flow

```
INITIAL LOAD (Before Compaction):
1. Read machine_prompt.md (58% compressed from requirements.md)
2. Read PROGRESS.md
3. Understand full context

GENERATE COMPACT_CONTEXT.md:
1. Extract current task from machine_prompt.md
2. Extract current status from PROGRESS.md
3. EMBED machine_prompt.md content for current task
4. Add files, constraints, next actions
5. Create ultra-compact self-contained file

AFTER COMPACTION (Clean Slate):
1. CLEAR entire context
2. Read ONLY COMPACT_CONTEXT.md (contains embedded machine_prompt)
3. Read ONLY files listed in FILES section
4. Work with minimal focused context
```

## File Relationship

```
requirements.md (human, permanent, 2000 tokens)
    ↓ [Generate via Rule 14]
machine_prompt.md (machine, permanent, 900 tokens, 58% reduction)
    ↓ [Extract current task + embed]
COMPACT_CONTEXT.md (ultra-compact, ephemeral, 500 tokens, 97% reduction)
    ↓ [Contains embedded machine_prompt for current task]
Agent reads ONLY this after context clear (self-contained)
```

**Token Flow**:
- Human file: 2000 tokens (never loaded by sub-agents)
- Machine file: 900 tokens (loaded once, content embedded in compact)
- Compact file: 500 tokens (loaded after clear, includes embedded machine content)
- **Final context**: 500 tokens + FILES section (~3-5K total)

## PROGRESS.md Lifecycle

### Ephemeral and Task-Specific

**PROGRESS.md is:**
1. Rewritten from scratch when starting new task
2. Contains ONLY current task - no cumulative history
3. Updated as current task progresses
4. Cleared completely when task completes
5. Rewritten fresh for next task
6. Deleted when specification 100% complete

### Contents

**Contains:**
- Current task/feature RIGHT NOW
- Current status and progress on THIS task
- Blockers for THIS task
- Next steps for THIS task
- Recent work on THIS task only

**Must NOT Contain:**
- Historical progress from previous tasks
- Completed task summaries (goes to REPORT.md)
- Accumulated updates from multiple tasks
- Future task plans

### Lifecycle Pattern

```
Task 1 starts → Create PROGRESS.md (task 1 only) →
Task 1 updates → Update PROGRESS.md (task 1 only) →
Task 1 completes → CLEAR PROGRESS.md completely →
Task 2 starts → REWRITE PROGRESS.md (task 2 only) →
[Repeat]
```

**When Task Completes:**
1. Extract learnings → Add to LEARNINGS.md (permanent)
2. Extract completion summary → Add to REPORT.md (permanent)
3. CLEAR PROGRESS.md completely
4. DELETE COMPACT_CONTEXT.md
5. Ready for next task with clean slate

## Compaction Process

### When to Compact

Sub-agents MUST generate COMPACT_CONTEXT.md when:
1. Starting new task (initial compaction)
2. After updating PROGRESS.md
3. Context approaching limits (proactive compaction)
4. Before complex operations requiring clean context

### How to Compact

1. **Read Sources**: machine_prompt.md + PROGRESS.md
2. **Extract Current Task**: Only information for RIGHT NOW
3. **Embed machine_prompt**: Include relevant machine_prompt content
4. **Add Files Section**: List files for current task
5. **Add Constraints**: Key constraints only
6. **Add Next Actions**: 1-3 immediate steps
7. **Generate File**: Create COMPACT_CONTEXT.md
8. **Verify Size**: MUST be 500-800 tokens max
9. **Clear Context**: Clear entire conversation context
10. **Reload**: Read ONLY COMPACT_CONTEXT.md + FILES section

### Compaction Format

```markdown
# Compact Context: [Task Name]

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:[timestamp]

## CURRENT_TASK
task:[name]|status:[status]|started:[timestamp]

## MACHINE_PROMPT_CONTENT
[Embedded content from machine_prompt.md for THIS task]

## OBJECTIVE
[1-line description of current objective]

## FILES
read:[file1,file2]|update:[file3]|create:[file4]

## CONSTRAINTS
[Key constraints affecting current work]

## BLOCKERS
[Current blockers if any, or "none"]

## NEXT_ACTIONS
1. [Action 1]
2. [Action 2]
3. [Action 3]

## REFERENCES
machine_prompt:[path#section]|requirements:[path]|stack:[path]
```

## Main Agent Responsibilities

### Generate COMPACT_CONTEXT.md

Main Agent MUST:
1. Generate initial COMPACT_CONTEXT.md when spawning sub-agent
2. Include embedded machine_prompt.md content
3. Provide COMPACT_CONTEXT.md path to sub-agent
4. Monitor sub-agent context usage
5. Regenerate if sub-agent context grows too large

### Verify Compaction

Main Agent MUST:
1. Verify COMPACT_CONTEXT.md exists before spawning sub-agents
2. Check file size is 500-800 tokens max
3. Ensure machine_prompt content embedded
4. Confirm FILES section lists only current task files
5. Validate no historical content included

## Sub-Agent Responsibilities

### Use COMPACT_CONTEXT.md

Sub-agents MUST:
1. Read COMPACT_CONTEXT.md (NOT requirements.md or full machine_prompt.md)
2. Read ONLY files listed in FILES section
3. Work within constraints listed
4. Update PROGRESS.md as work progresses
5. Regenerate COMPACT_CONTEXT.md after PROGRESS.md updates
6. Clear and reload context after regeneration

### Regeneration Trigger

Regenerate COMPACT_CONTEXT.md when:
1. PROGRESS.md updated
2. Context growing large
3. Task status changes
4. New blockers discovered
5. Files list changes

## Enforcement

### Must Do
1. Generate COMPACT_CONTEXT.md for every task
2. Embed machine_prompt.md content in compact file
3. Keep compact file under 500-800 tokens
4. Clear PROGRESS.md when task completes
5. Delete COMPACT_CONTEXT.md when task completes
6. Regenerate compact file after PROGRESS.md updates
7. Clear and reload context after compaction

### Must Not Do
1. Let COMPACT_CONTEXT.md accumulate history
2. Include full file contents in compact file
3. Use COMPACT_CONTEXT.md across multiple tasks
4. Skip context clear after compaction
5. Read verbose files after compaction
6. Exceed 800 token limit for compact file

### Critical Violations
1. Sub-agent reading requirements.md instead of COMPACT_CONTEXT.md
2. COMPACT_CONTEXT.md exceeding 800 tokens
3. COMPACT_CONTEXT.md containing multiple tasks
4. Not clearing context after compaction
5. PROGRESS.md accumulating across multiple tasks

## Benefits

1. **97% Token Reduction**: requirements.md (2000) → machine_prompt.md (900) → COMPACT_CONTEXT.md (500)
2. **Prevents Context Exhaustion**: Regular compaction keeps context small
3. **Improved Focus**: Only current task information present
4. **Faster Processing**: Less content to read and parse
5. **Clean Slate**: Context reload ensures no accumulated cruft

## Summary

**Golden Rules:**
1. **COMPACT_CONTEXT.md is ephemeral** - one task only, deleted after
2. **Embed machine_prompt content** - self-contained instructions
3. **500-800 token limit** - ruthlessly compact
4. **Clear and reload** - fresh context after compaction
5. **PROGRESS.md is ephemeral** - rewritten per task
6. **References over content** - link to files, don't include them
7. **Current task only** - no history, no future

---

_Version: 1.0 - Last Updated: 2026-02-27_
