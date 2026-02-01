# Instruction Compaction and Context Optimization

## Purpose

Establish mandatory practice of creating ultra-compact instruction summaries that preserve only critical information for current work. This rule prevents context limit exhaustion, optimizes token usage, and ensures agents work with clean, focused context by regularly compacting and reloading.

**Inspiration**: Modeled after principles of concise system prompt design - every word earns its place, references replace verbosity, structure enables rapid parsing.

---

## Core Principle

**Verbose Context → Compacted Instructions → Context Reload → Clean Workspace**

- Long files exhaust context windows
- Compacted files preserve only current-work essentials
- References replace content duplication
- Regular reloading prevents context bloat

**Key Insight**: Most context is historical; only 10-20% matters for current task. Compact ruthlessly.

---

## When to Compact (MANDATORY)

### ALWAYS Compact When:

1. **Starting New Work**: Before beginning any task/feature
2. **Updating PROGRESS.md**: Every time progress file changes
3. **Context Approaching Limit**: When nearing 150K-180K tokens (85-90% of 200K limit)
4. **Switching Tasks**: Moving between tasks or features
5. **After Long Sessions**: Every 50-100 agent turns
6. **Before Major Operations**: Commits, verification, documentation generation

### The Compaction File

**Name**: `COMPACT_CONTEXT.md`

**Location**: Same directory as PROGRESS.md
```
specifications/01-spec-name/
├── PROGRESS.md              # Full detailed progress (can be verbose)
├── COMPACT_CONTEXT.md       # Ultra-compressed current work context
├── machine_prompt.md        # Machine-optimized requirements
```

**Purpose**: Minimal, focused context for current task only

---

## COMPACT_CONTEXT.md Format

### Structure

```markdown
# Compact Context: [Current Task Name]

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:[timestamp]|FROM:[progress.md,machine_prompt.md]

## CURRENT_TASK
task:[task_name]|status:[in_progress/blocked/testing]|started:[timestamp]

## OBJECTIVE
[Single sentence describing what you're doing RIGHT NOW]

## FILES
read:[file1.rs,file2.rs]|update:[file3.rs]|create:[file4.rs]|review:[doc.md]

## REQUIREMENTS_REF
machine_prompt:[./machine_prompt.md#TASK_3]|spec:[./requirements.md#L45-67]

## KEY_CONSTRAINTS
1. [Critical constraint affecting current work]
2. [Another critical constraint]

## BLOCKERS
[Current blockers if any - or "NONE"]

## NEXT_ACTIONS
1. [Immediate next step]
2. [Following step]

## CONTEXT_REFS
progress:[./PROGRESS.md]|learnings:[./LEARNINGS.md#critical-impl]|docs:[documentation/module/doc.md]

---
⚠️ AFTER READING THIS FILE: Clear context, reload from this file, proceed with fresh context
```

### Compaction Rules

#### 1. Radical Brevity
```
❌ Verbose: "We are currently implementing the HTTP client core structure which involves creating the HttpClient struct with connection pooling support and implementing keep-alive functionality"

✅ Compact: "task:impl HttpClient struct|features:[conn_pool,keep-alive]"
```

#### 2. References Over Content
```
❌ Duplicating: Include full requirements, full progress, full learnings

✅ Referencing:
machine_prompt:[./machine_prompt.md#TASK_3]
progress:[./PROGRESS.md#current-task]
learnings:[./LEARNINGS.md#conn-pool-insights]
```

#### 3. Current Work Only
```
❌ Including: Completed tasks, future tasks, historical context

✅ Including: Current task, immediate next step, active blockers
```

#### 4. File Lists Not Content
```
❌ Listing: Full file paths with explanations

✅ Listing: read:[http.rs,dns.rs]|update:[lib.rs]|create:[tests.rs]
```

#### 5. Single Sentence Objective
```
❌ Verbose: "The objective of the current work is to implement the core HTTP client structure following the requirements specified in the machine_prompt.md file, which includes..."

✅ Compact: "Impl HttpClient struct with conn pooling per machine_prompt.md#TASK_3"
```

#### 6. Constraints Not Explanations
```
❌ Explaining: "We must ensure that the implementation follows the async pattern because..."

✅ Constraining: "async_only|no_blocking_calls|tokio_runtime"
```

---

## Generation Workflow

### Main Agent Responsibility

**Never generates COMPACT_CONTEXT.md** - only sub-agents generate for their own work

### Sub-Agent Responsibility (MANDATORY)

#### Before Starting Work

```
1. ✅ Load machine_prompt.md (not requirements.md)
2. ✅ Load PROGRESS.md to understand context
3. ✅ Generate COMPACT_CONTEXT.md from:
   - machine_prompt.md (extract current task)
   - PROGRESS.md (current status)
   - Own understanding of immediate work
4. ✅ Save COMPACT_CONTEXT.md
5. ✅ CLEAR ENTIRE CONTEXT
6. ✅ RELOAD: Read ONLY COMPACT_CONTEXT.md
7. ✅ Follow references to read specific files/sections
8. ✅ Proceed with fresh, compact context
```

#### After Updating PROGRESS.md

```
1. ✅ Update PROGRESS.md with progress
2. ✅ Regenerate COMPACT_CONTEXT.md (reflect new status)
3. ✅ CLEAR ENTIRE CONTEXT
4. ✅ RELOAD: Read ONLY COMPACT_CONTEXT.md
5. ✅ Continue work with fresh context
```

#### When Approaching Context Limit

If context reaches 85-90% (150K-180K tokens):

```
⚠️ EMERGENCY COMPACTION
1. ✅ Immediately generate COMPACT_CONTEXT.md
2. ✅ CLEAR ENTIRE CONTEXT (drop everything)
3. ✅ RELOAD: Read ONLY COMPACT_CONTEXT.md
4. ✅ Read only files listed in FILES section
5. ✅ Continue work with minimal context
```

---

## Generation Algorithm

### Pseudo-Code

```python
def generate_compact_context(progress_md: str, machine_prompt_md: str, current_files: list) -> str:
    """
    Generate ultra-compact context from verbose sources.

    Preserve ONLY what's needed for immediate work.
    Everything else becomes a reference.
    """

    # Extract current task (not past, not future)
    current_task = extract_current_task(progress_md)

    # Single sentence objective
    objective = summarize_objective(current_task, max_words=15)

    # File lists (no content)
    files_to_read = [f for f in current_files if needs_reading(f)]
    files_to_update = [f for f in current_files if needs_updating(f)]
    files_to_create = [f for f in current_files if needs_creation(f)]

    # Extract only critical constraints
    constraints = extract_critical_constraints(machine_prompt_md, max_items=3)

    # Current blockers (or NONE)
    blockers = extract_active_blockers(progress_md) or "NONE"

    # Next 1-3 immediate actions
    next_actions = extract_next_actions(progress_md, max_items=3)

    # References (not content)
    refs = {
        'machine_prompt': find_relevant_section(machine_prompt_md, current_task),
        'progress': './PROGRESS.md',
        'learnings': find_relevant_learnings(current_task),
    }

    compact = f"""# Compact Context: {current_task['name']}

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:{timestamp()}|FROM:[progress.md,machine_prompt.md]

## CURRENT_TASK
task:{current_task['name']}|status:{current_task['status']}|started:{current_task['started']}

## OBJECTIVE
{objective}

## FILES
read:[{','.join(files_to_read)}]|update:[{','.join(files_to_update)}]|create:[{','.join(files_to_create)}]

## REQUIREMENTS_REF
machine_prompt:[{refs['machine_prompt']}]|progress:[{refs['progress']}]

## KEY_CONSTRAINTS
{format_constraints(constraints)}

## BLOCKERS
{blockers}

## NEXT_ACTIONS
{format_actions(next_actions)}

## CONTEXT_REFS
progress:[{refs['progress']}]|learnings:[{refs['learnings']}]

---
⚠️ AFTER READING THIS FILE: Clear context, reload from this file, proceed with fresh context
"""

    return compact

def extract_current_task(progress_md: str) -> dict:
    """Extract ONLY current task, ignore completed/future."""
    # Parse PROGRESS.md
    # Find section marked "Current Task" or "In Progress"
    # Return task details
    pass

def summarize_objective(task: dict, max_words: int) -> str:
    """Single sentence, max_words limit."""
    # Take task description
    # Compress to essential action + target
    # Return concise sentence
    pass

def extract_critical_constraints(machine_prompt: str, max_items: int) -> list:
    """Only constraints affecting current task."""
    # Parse machine_prompt
    # Filter to current task constraints
    # Return top max_items most critical
    pass
```

---

## Context Reload Protocol

### The Reload Cycle

```
[Working with accumulated context] →
[Generate COMPACT_CONTEXT.md] →
[Clear entire context] →
[Read ONLY COMPACT_CONTEXT.md] →
[Follow references to specific files/sections] →
[Continue work with fresh, minimal context] →
[Repeat when context grows again]
```

### How to Clear Context

Agent performs mental reset:
```
1. Save COMPACT_CONTEXT.md
2. Acknowledge: "Context cleared. Reloading from compact context."
3. Read COMPACT_CONTEXT.md
4. Read only referenced files (FILES section)
5. Proceed as if starting fresh session
```

**Effect**: Context window resets to ~10-20% of previous usage

---

## Example Transformation

### Before Compaction (Context: 180K tokens, approaching limit)

Agent has in context:
- Full requirements.md (2000 tokens)
- Full PROGRESS.md with all historical progress (5000 tokens)
- Full LEARNINGS.md with all insights (3000 tokens)
- Multiple full file reads (20,000 tokens)
- Conversation history (150,000 tokens)
- **Total: ~180,000 tokens (90% of limit)**

### After Compaction (Context: 5K tokens, fresh start)

Agent has in context:
- COMPACT_CONTEXT.md (500 tokens)
- Only current task files (3000 tokens)
- Current conversation (1500 tokens)
- **Total: ~5,000 tokens (2.5% of limit)**

**Savings**: 175,000 tokens (97.2% reduction)

### COMPACT_CONTEXT.md Example

```markdown
# Compact Context: Implement DNS Resolver

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:2026-02-01T14:30:00Z|FROM:[progress.md,machine_prompt.md]

## CURRENT_TASK
task:impl_dns_resolver|status:in_progress|started:2026-02-01T14:00:00Z

## OBJECTIVE
Impl DnsResolver trait with caching per machine_prompt.md#TASK_1

## FILES
read:[src/http_client.rs,src/lib.rs]|update:[src/dns_resolver.rs]|create:[tests/dns_tests.rs]

## REQUIREMENTS_REF
machine_prompt:[./machine_prompt.md#TASK_1]|spec:[./requirements.md#L45-67]

## KEY_CONSTRAINTS
1. async_only|tokio_runtime
2. cache_ttl:300s|max_entries:1000
3. ipv4_ipv6_support

## BLOCKERS
NONE

## NEXT_ACTIONS
1. Impl DnsResolver trait|methods:[resolve_host,cache_lookup]
2. Add LRU cache|dep:[lru_cache]
3. Write unit tests|coverage:>80%

## CONTEXT_REFS
progress:[./PROGRESS.md#dns-resolver-work]|learnings:[./LEARNINGS.md#dns-caching]|docs:[documentation/http_client/doc.md#dns]

---
⚠️ AFTER READING THIS FILE: Clear context, reload from this file, proceed with fresh context
```

**Size**: 500 tokens (vs 10,000+ for full context)

---

## Frontmatter Reminders

### All Specification Files

Add to frontmatter:
```yaml
context_optimization: true  # Agent MUST generate COMPACT_CONTEXT.md before work, reload after updates
compact_context_file: ./COMPACT_CONTEXT.md  # Ultra-compact current task context
context_reload_required: true  # Clear and reload from compact context regularly
```

### PROGRESS.md Header

Update header:
```markdown
> **⚠️ Context Optimization**:
> - Generate `COMPACT_CONTEXT.md` before starting work
> - Regenerate after updating this file
> - Clear context and reload from `COMPACT_CONTEXT.md`
> - See Rule 15 for compaction protocol
```

---

## Integration with Existing Rules

### Rule 14 (Machine-Optimized Prompts)

**Relationship**: Complementary optimization layers
- Rule 14: Compress specifications (requirements.md → machine_prompt.md)
- Rule 15: Compress runtime context (PROGRESS.md → COMPACT_CONTEXT.md)

**Combined Effect**:
- Machine prompts: 58% reduction in specification tokens
- Context compaction: 97% reduction in runtime context tokens

### Rule 05 (Agent Orchestration)

Sub-agent workflow update:
```
1. Load machine_prompt.md (Rule 14)
2. Load PROGRESS.md
3. Generate COMPACT_CONTEXT.md (Rule 15)
4. Clear context
5. Reload from COMPACT_CONTEXT.md
6. Begin work with minimal context
```

### Rule 13 (Implementation Agent)

Add to "Before Starting Work":
```
8. ✅ Generate COMPACT_CONTEXT.md (Rule 15)
9. ✅ Clear entire context
10. ✅ Reload from COMPACT_CONTEXT.md only
11. ✅ Read only files listed in FILES section
```

---

## Benefits

### 1. Prevents Context Limit Errors
- Regular compaction keeps context well below limits
- Emergency compaction when approaching limit
- Never hit 200K token ceiling

### 2. Improves Agent Performance
- Clean context = faster processing
- Focused context = better decisions
- Less noise = clearer reasoning

### 3. Reduces Token Costs
- Smaller context = fewer input tokens
- Reload cycle = minimal cumulative usage
- References instead of duplication

### 4. Maintains Focus
- Only current task in context
- Historical info via references
- Prevents context drift

### 5. Enables Long Sessions
- Can work indefinitely with reload cycles
- Each reload resets context usage
- No gradual context exhaustion

---

## Monitoring and Enforcement

### Context Usage Monitoring

Agent should track approximate context usage:
```
If estimated_context_tokens > 150K:
    ⚠️ WARNING: Approaching context limit (85%)
    → IMMEDIATE COMPACTION REQUIRED

If estimated_context_tokens > 180K:
    🚨 CRITICAL: Context limit imminent (90%)
    → EMERGENCY COMPACTION + RELOAD NOW
```

### Enforcement Rules

**MANDATORY compaction triggers**:
- ✅ Before starting any new task
- ✅ After updating PROGRESS.md
- ✅ Every 50-100 agent turns
- ✅ When context exceeds 150K tokens

**FORBIDDEN behaviors**:
- ❌ Continuing work when context >150K without compaction
- ❌ Including full file contents in COMPACT_CONTEXT.md
- ❌ Skipping context reload after compaction
- ❌ Duplicating content that should be referenced

---

## Templates

### COMPACT_CONTEXT-template.md

```markdown
# Compact Context: [Task Name]

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:[timestamp]|FROM:[source_files]

## CURRENT_TASK
task:[task_name]|status:[status]|started:[timestamp]

## OBJECTIVE
[Single sentence: what you're doing right now]

## FILES
read:[files_to_read]|update:[files_to_update]|create:[files_to_create]

## REQUIREMENTS_REF
machine_prompt:[path#section]|spec:[path#lines]

## KEY_CONSTRAINTS
1. [Constraint 1]
2. [Constraint 2]
3. [Constraint 3]

## BLOCKERS
[Current blockers or "NONE"]

## NEXT_ACTIONS
1. [Immediate next step]
2. [Following step]
3. [Third step if needed]

## CONTEXT_REFS
progress:[path]|learnings:[path#section]|docs:[path]

---
⚠️ AFTER READING THIS FILE: Clear context, reload from this file, proceed with fresh context
```

---

## Makefile Integration

Add to specification Makefile:
```makefile
.PHONY: compact-context

compact-context:
	@echo "Generating compact context from progress..."
	@python3 ../../scripts/generate_compact_context.py \
		PROGRESS.md machine_prompt.md
	@echo "✓ COMPACT_CONTEXT.md generated"
	@echo "⚠️  Clear context and reload from COMPACT_CONTEXT.md"
```

---

## Summary

**Core Workflow**:
```
Load machine_prompt.md + PROGRESS.md →
Generate COMPACT_CONTEXT.md (ultra-minimal) →
Clear context (drop everything) →
Reload from COMPACT_CONTEXT.md only →
Read referenced files (not all files) →
Work with 97% less context →
Repeat cycle when context grows
```

**Key Principles**:
1. ✅ Compact before every new task
2. ✅ References replace content duplication
3. ✅ Current work only (no historical)
4. ✅ Clear and reload regularly
5. ✅ Monitor context usage
6. ✅ Emergency compact at 85%+
7. ✅ Single sentence objectives
8. ✅ File lists not file contents

**Benefits**:
- 🚀 97% context reduction
- 🚀 Prevents context limit errors
- 🚀 Improves agent performance
- 🚀 Enables indefinite work sessions
- 🚀 Reduces token costs
- 🚀 Maintains laser focus

**Combined with Rule 14**:
- Rule 14: 58% specification token reduction
- Rule 15: 97% runtime context reduction
- **Total**: >98% token optimization

**Enforcement**:
- ❌ **USER WILL BE FRUSTRATED** if agent hits context limits
- ❌ Continuing without compaction when context >150K is FORBIDDEN
- ❌ Including full content instead of references wastes tokens
- ✅ Regular compaction and reload cycles are MANDATORY

---

*Created: 2026-02-01*
*Purpose: Prevent context exhaustion through radical compaction and reload cycles*
*Inspiration: Concise system prompt principles - every word earns its place*
