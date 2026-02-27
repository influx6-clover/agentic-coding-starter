---
name: "Context Compaction"
description: "Generate compacted.md with all retrieved information using compression strategies"
approved: Yes
created: 2026-02-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "2.0"
  last_updated: "2026-02-27"
  tags: [context, compaction, optimization, efficiency]
---

# Context Compaction

## Read By

1. **All Agents** - MANDATORY after reading required files

## Overview

After reading all required files, generate a `compacted.md` with compressed information to prevent context exhaustion.

**Token Savings**: ~85-97% reduction

## When to Use

**MANDATORY for ALL agents:**
- After reading requirements, learnings, progress, agent docs, and skills
- Before starting implementation work
- When context approaches limits

## Process

### Step 1: Read Everything You Need

Read in this order:
1. `requirements.md` or `feature.md`
2. `LEARNINGS.md`
3. `progress.md`
4. `.agents/AGENTS.md`
5. Your agent file (`.agents/agents/[agent-name].md`)
6. Skills specified in your agent documentation

### Step 2: Generate compacted.md

Create a temporary `compacted.md` file using pipe-delimited compression:

```markdown
# Compacted Context: [Task Name]

⚠️TEMP_FILE|DELETE_WHEN_DONE|GENERATED:[timestamp]

## LOCATION
workspace:[name]|spec:[NN-spec]|file:[current file path]

## OBJECTIVE
[Single sentence: what you're doing right now - max 15 words]

## REQUIREMENTS
req1:[requirement]|constraints:[...]|success:[...]
req2:[requirement]|constraints:[...]|success:[...]

## TASKS
[ ]task1:[description]|files:[list]|tests:[list]
[x]task2:[description]|status:done|commit:[hash]

## LEARNINGS
past1:[key learning from LEARNINGS.md]
past2:[another key learning]

## CURRENT_STATE
progress:[what's done]|next:[what's next]|blockers:[any blockers or NONE]

## FILES_TO_MODIFY
read:[file1,file2]|update:[file3]|create:[file4]

## NEXT_ACTIONS
1. [Immediate next step]
2. [Following step]
3. [Third step]

---

⚠️ **AFTER READING**: Clear context, reload from this file only, start work
```

### Step 3: Clear Context and Reload

1. Save `compacted.md`
2. Clear your entire context
3. Reload ONLY from `compacted.md`
4. Start implementation with fresh, minimal context

### Step 4: Delete When Done

When task complete:
- Delete `compacted.md`
- Report to Main Agent

For next task:
- Regenerate fresh `compacted.md`
- Repeat process

## Compression Strategies

### Use Pipe Delimiters
❌ Bad: "The requirement is to implement HTTP client with GET and POST methods"
✅ Good: `req:http client|methods:[GET,POST]`

### Abbreviate Common Words
- requirement → req
- implementation → impl
- configuration → cfg
- documentation → doc
- specification → spec

### Use Brackets for Lists
❌ Bad: "Files to update: file1.rs, file2.rs, file3.rs"
✅ Good: `files:[file1.rs,file2.rs,file3.rs]`

### Remove Verbosity
❌ Bad: "The system should be able to handle errors gracefully with proper error messages"
✅ Good: `error:graceful|messages:clear`

### Embed Key Info Only
- Don't copy entire files
- Extract only what's needed for current task
- Reference original files if details needed

## Example: Before and After

### Before (Reading Multiple Files - ~2000 tokens):
- requirements.md (800 tokens)
- LEARNINGS.md (400 tokens)
- progress.md (300 tokens)
- agent doc (300 tokens)
- skills (200 tokens)

### After (compacted.md - ~200 tokens):
```markdown
# Compacted Context: Add HTTP Compression

## OBJECTIVE
Implement gzip compression for HTTP client responses

## REQUIREMENTS
req:compression|formats:[gzip,deflate]|auto_detect:yes|threshold:1KB

## LEARNINGS
past1:compression must happen after parsing|past2:buffer size 8KB optimal

## CURRENT_STATE
progress:connection done,methods done|next:add compression|blockers:NONE

## FILES_TO_MODIFY
update:[src/http_client.rs,src/compression.rs]|tests:[tests/compression_tests.rs]

## NEXT_ACTIONS
1. Write test for gzip compression
2. Implement compression module
3. Integrate with http client
```

**Result**: 2000 tokens → 200 tokens (90% reduction)

## Critical Rules

✅ **ALWAYS generate compacted.md** after reading files
✅ **ALWAYS clear context** and reload from compacted.md
✅ **ALWAYS delete compacted.md** when task complete
✅ **CREATE FRESH** compacted.md for each new task

❌ **NEVER skip** compaction step
❌ **NEVER keep** old compacted.md files
❌ **NEVER commit** compacted.md to git

## Benefits

✅ **Massive token savings**: 85-97% reduction
✅ **Prevents context exhaustion**: Stay under limits
✅ **Faster processing**: Less to read and process
✅ **Clearer focus**: Only current task information
✅ **Fresh context**: No stale information

## Summary

**Workflow:**
```
Read all files → Generate compacted.md → Clear context →
Reload compacted.md → Work → Delete compacted.md → Next task
```

**Key Principle**: Compress everything into pipe-delimited format, clear context, work with minimal information.

---

_Version: 2.0 - Last Updated: 2026-02-27_
