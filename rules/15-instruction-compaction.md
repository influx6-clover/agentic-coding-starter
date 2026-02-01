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

## CRITICAL: Ephemeral Nature of COMPACT_CONTEXT.md

### COMPACT_CONTEXT.md Lifecycle (MANDATORY)

**COMPACT_CONTEXT.md is EPHEMERAL and TASK-SPECIFIC**:

1. ✅ **Generated fresh** for each new task
2. ✅ **Contains ONLY current task** - no history, no future tasks
3. ✅ **Regenerated** every time PROGRESS.md updates
4. ✅ **Cleared and rewritten** from scratch when task completes
5. ✅ **Never accumulates** - always reflects "now" only
6. ✅ **Deleted** when task fully complete (before starting next task)

**What COMPACT_CONTEXT.md CONTAINS**:
- ✅ Current task name and status
- ✅ Current objective (what you're doing RIGHT NOW)
- ✅ Files relevant to current task only
- ✅ Key constraints affecting current work
- ✅ Current blockers (if any)
- ✅ Immediate next actions (1-3 steps)
- ✅ **Embedded machine_prompt.md content** for current task
- ✅ References to other files (not their content)

**What COMPACT_CONTEXT.md MUST NOT CONTAIN**:
- ❌ Historical context (completed tasks)
- ❌ Future tasks or plans
- ❌ Full file contents (use references)
- ❌ Verbose explanations
- ❌ Accumulated progress from multiple tasks
- ❌ Content from previous task iterations

**Lifecycle Pattern**:
```
Task 1 starts → Generate COMPACT_CONTEXT.md (task 1 only) →
Task 1 updates → Regenerate COMPACT_CONTEXT.md (task 1 only) →
Task 1 completes → DELETE COMPACT_CONTEXT.md →
Task 2 starts → Generate NEW COMPACT_CONTEXT.md (task 2 only) →
[Repeat for each task]
```

**Size Limit**: COMPACT_CONTEXT.md should NEVER exceed 500-800 tokens. If larger, compress more aggressively.

---

## CRITICAL: machine_prompt.md Integration

### machine_prompt.md Generation and Usage

**WHEN machine_prompt.md IS GENERATED** (Rule 14):

1. ✅ **Project start**: Main Agent generates for new specification
2. ✅ **Specification creation**: Generated when requirements.md finalized
3. ✅ **Feature creation**: Generated for each feature.md
4. ✅ **Specification updates**: Regenerated when requirements.md changes
5. ✅ **Feature updates**: Regenerated when feature.md changes

**ONCE GENERATED** (CRITICAL WORKFLOW):

```
1. machine_prompt.md is generated from requirements.md/feature.md
   ↓
2. Main Agent CLEARS context
   ↓
3. Main Agent RELOADS from machine_prompt.md
   ↓
4. machine_prompt.md becomes source of truth for agent instructions
   ↓
5. Human files (requirements.md/feature.md) still updated normally
   ↓
6. When human files change → Regenerate machine_prompt.md → Clear → Reload
   ↓
7. machine_prompt.md stays in sync with human files
```

### COMPACT_CONTEXT.md Embeds machine_prompt.md Content

**CRITICAL RELATIONSHIP**:

When generating COMPACT_CONTEXT.md, it **MUST include machine_prompt.md content** for current task:

```markdown
# Compact Context: Implement DNS Resolver

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:[timestamp]|FROM:[machine_prompt.md,progress.md]

## CURRENT_TASK
task:impl_dns_resolver|status:in_progress|started:[timestamp]

## MACHINE_PROMPT_CONTENT
[EMBEDDED CONTENT FROM machine_prompt.md FOR THIS SPECIFIC TASK]

spec:http-client|priority:high
req:impl DnsResolver trait|cache:LRU,ttl=300s|async:tokio
task:impl_dns_resolver|files:[src/dns.rs]|tests:[tests/dns_tests.rs]
constraints:async_only|no_blocking|ipv4_ipv6

## OBJECTIVE
Impl DnsResolver trait with LRU caching per machine_prompt.md#TASK_1

## FILES
read:[src/http_client.rs,src/lib.rs]|update:[src/dns_resolver.rs]|create:[tests/dns_tests.rs]

## REQUIREMENTS_REF
machine_prompt:[./machine_prompt.md#TASK_1]

[... rest of compact context ...]
```

**Why Embed**:
- COMPACT_CONTEXT.md is the ONLY file loaded after context clear
- Must be self-contained with all critical task information
- Embedding machine_prompt.md task content ensures completeness
- Agent doesn't need to read machine_prompt.md separately after reload

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
2. Read ONLY COMPACT_CONTEXT.md (contains embedded machine_prompt content)
3. Read ONLY files listed in FILES section
4. No need to re-read machine_prompt.md (content already embedded)
5. Work with minimal focused context
```

### Dual File Maintenance

**Human-Readable Files** (requirements.md, feature.md):
- ✅ **Always updated** as normal workflow
- ✅ **Source of truth** for human understanding
- ✅ **Never deleted** - permanent record
- ✅ **Edited directly** when requirements change
- ✅ **Committed with changes** to version control

**Machine-Optimized Files** (machine_prompt.md):
- ✅ **Generated** from human files (Rule 14)
- ✅ **Regenerated** when human files change
- ✅ **Used by agents** for instructions
- ✅ **Stays in sync** with human files
- ✅ **Committed** alongside human files
- ❌ **Never hand-edited** - always generated

**Ultra-Compact Files** (COMPACT_CONTEXT.md):
- ✅ **Generated** for each task from machine_prompt.md + PROGRESS.md
- ✅ **Embeds** machine_prompt.md content for current task
- ✅ **Regenerated** on every PROGRESS.md update
- ✅ **Deleted** when task completes
- ✅ **Current task only** - no history
- ❌ **Never accumulates** - always fresh per task
- ❌ **Never committed** - ephemeral working file

### File Relationship Summary

```
requirements.md (human, permanent, 2000 tokens)
    ↓ [Generate via Rule 14]
machine_prompt.md (machine, permanent, 900 tokens, 58% reduction)
    ↓ [Extract current task + embed]
COMPACT_CONTEXT.md (ultra-compact, ephemeral, 500 tokens, 97% reduction)
    ↓ [Contains embedded machine_prompt content for current task]
Agent reads ONLY this after context clear (self-contained)
```

**Token Flow**:
- Human file: 2000 tokens (never loaded by sub-agents)
- Machine file: 900 tokens (loaded once, content embedded in compact)
- Compact file: 500 tokens (loaded after clear, includes embedded machine content)
- **Final context**: 500 tokens + FILES section (~3-5K total)

---

## CRITICAL: PROGRESS.md Lifecycle

### PROGRESS.md Must Be Rewritten Per Task

**MANDATORY BEHAVIOR** (Confirming/Reinforcing):

**PROGRESS.md is EPHEMERAL and TASK-SPECIFIC** (just like COMPACT_CONTEXT.md):

1. ✅ **Rewritten from scratch** when starting new task
2. ✅ **Contains ONLY current task** - no cumulative history
3. ✅ **Updated** as current task progresses
4. ✅ **Cleared completely** when task completes
5. ✅ **Rewritten fresh** for next task
6. ✅ **Deleted** when specification 100% complete

**What PROGRESS.md CONTAINS**:
- ✅ Current task/feature being worked on RIGHT NOW
- ✅ Current status and progress on THIS task
- ✅ Blockers for THIS task
- ✅ Next steps for THIS task
- ✅ Recent work on THIS task only

**What PROGRESS.md MUST NOT CONTAIN**:
- ❌ Historical progress from previous tasks
- ❌ Completed task summaries (goes to REPORT.md)
- ❌ Accumulated updates from multiple tasks
- ❌ Future task plans

**Lifecycle Pattern** (Same as COMPACT_CONTEXT.md):
```
Task 1 starts → Create PROGRESS.md (task 1 only) →
Task 1 updates → Update PROGRESS.md (task 1 only) →
Task 1 completes → CLEAR PROGRESS.md completely →
Task 2 starts → REWRITE PROGRESS.md from scratch (task 2 only) →
[Repeat for each task]
```

**When Task Completes**:
1. ✅ Extract learnings → Add to LEARNINGS.md (permanent)
2. ✅ Extract completion summary → Add to REPORT.md (permanent)
3. ✅ CLEAR PROGRESS.md completely (delete all content)
4. ✅ DELETE COMPACT_CONTEXT.md
5. ✅ Ready for next task with clean slate

**Synchronization with COMPACT_CONTEXT.md**:
```
Update PROGRESS.md →
Regenerate COMPACT_CONTEXT.md from machine_prompt.md + PROGRESS.md →
Clear context →
Reload from COMPACT_CONTEXT.md →
Continue work
```

---

## Key Insight

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

**CRITICAL**: COMPACT_CONTEXT.md MUST embed machine_prompt.md content AND relevant rule summaries for current task.

```markdown
# Compact Context: [Current Task Name]

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:[timestamp]|FROM:[machine_prompt.md,progress.md,rules]

## RULES_SUMMARY
[EMBEDDED COMPACTED RULES FROM FRONTMATTER - ONLY RULES AGENT NEEDS]

rule:01|naming_structure|ref:[.agents/rules/01-*.md]
rule:02|dir_policy|ref:[.agents/rules/02-*.md]
rule:03|danger_ops|safe_patterns:[list]|forbidden:[list]|ref:[.agents/rules/03-*.md]
rule:04|commit|verify_first|no_force_push|ref:[.agents/rules/04-*.md]
rule:13|impl_agent|tdd|retrieval_first|test_docs|ref:[.agents/rules/13-*.md]
stack:[rust]|patterns:[discovered_patterns]|ref:[.agents/stacks/rust.md]

## CURRENT_TASK
task:[task_name]|status:[in_progress/blocked/testing]|started:[timestamp]

## MACHINE_PROMPT_CONTENT
[EMBEDDED CONTENT FROM machine_prompt.md FOR THIS SPECIFIC TASK ONLY]

spec:[name]|status:[status]|priority:[priority]
req:[current_task_requirement]|constraints:[...]|success:[...]
task:[current_task]|files:[...]|tests:[...]|verification:[...]
tech:stack=[...]|loc=[...]|deps=[...]

## OBJECTIVE
[Single sentence describing what you're doing RIGHT NOW - max 15 words]

## FILES
read:[file1.rs,file2.rs]|update:[file3.rs]|create:[file4.rs]|review:[doc.md]

## REQUIREMENTS_REF
machine_prompt:[./machine_prompt.md#TASK_N]|spec:[./requirements.md#L45-67]

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

**Why RULES_SUMMARY Section Exists**:
- Embeds compacted essential rules from specification frontmatter
- Eliminates need to load full rule files after context reload
- Only includes rules agent type needs (from files_required)
- Provides quick reference + link for deeper reading if needed
- Saves ~10-20K tokens per rule file avoided

**Why MACHINE_PROMPT_CONTENT Section Exists**:
- After context clear, COMPACT_CONTEXT.md is the ONLY file loaded
- Must be self-contained with ALL task requirements
- Embedding machine_prompt content eliminates need to re-read machine_prompt.md
- Agent has complete instructions in single compact file
- No external file dependencies after reload

**Size Target**: 500-1000 tokens total (including embedded rules + machine_prompt content)

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

### Main Agent Responsibility (CRITICAL)

**Main Agent MUST generate initial COMPACT_CONTEXT.md before spawning sub-agents**:

```
BEFORE SPAWNING SUB-AGENT:

1. ✅ Generate machine_prompt.md from requirements.md/feature.md (Rule 14)
2. ✅ Clear context and reload from machine_prompt.md
3. ✅ Read PROGRESS.md (or create fresh if starting first task)
4. ✅ Generate initial COMPACT_CONTEXT.md:
   a. Extract first/current task from machine_prompt.md
   b. EMBED machine_prompt content for current task
   c. Extract/create initial status
   d. List files for current task
   e. Create ultra-compact self-contained file (500-800 tokens)
5. ✅ Save COMPACT_CONTEXT.md
6. ✅ Spawn sub-agent with path to COMPACT_CONTEXT.md
7. ✅ Sub-agent starts with clean compact context (no need to generate initially)
```

**AFTER SUB-AGENT COMPLETES AND REPORTS BACK**:

```
1. ✅ Receive completion report from sub-agent
2. ✅ Run verification (Rule 05)
3. ✅ If verification passes:
   - Update specifications (mark tasks complete)
   - Update documentation (Rule 06)
   - DELETE COMPACT_CONTEXT.md (task complete)
   - Commit changes
4. ✅ If verification fails:
   - Update PROGRESS.md with failure details
   - Regenerate COMPACT_CONTEXT.md (embed fix requirements)
   - Resume/spawn sub-agent with updated COMPACT_CONTEXT.md
```

**Main Agent maintains COMPACT_CONTEXT.md ownership**:
- Generates initial version before spawning
- Regenerates when resuming sub-agent after verification
- Deletes when task completes
- Ensures sub-agent always starts with correct compact context

### Sub-Agent Responsibility (MANDATORY)

**Sub-Agent receives COMPACT_CONTEXT.md from Main Agent**:

```
ON STARTUP (spawned by Main Agent):

1. ✅ Main Agent provides path to COMPACT_CONTEXT.md (already generated)
2. ✅ Read COMPACT_CONTEXT.md (self-contained with embedded machine_prompt)
3. ✅ Read files from FILES section
4. ✅ Begin work with clean compact context (~5K tokens)
5. ✅ NO need to generate COMPACT_CONTEXT.md initially (Main Agent did this)
```

**DURING WORK (Sub-Agent Updates)**:

```
1. ✅ Make progress on task
2. ✅ Update PROGRESS.md with current progress
3. ✅ Regenerate COMPACT_CONTEXT.md:
   a. Re-read machine_prompt.md (extract current task)
   b. Re-embed machine_prompt content
   c. Update status from new PROGRESS.md
   d. Update FILES list if changed
   e. Update NEXT_ACTIONS based on progress
4. ✅ CLEAR ENTIRE CONTEXT (drop everything)
5. ✅ RELOAD: Read ONLY COMPACT_CONTEXT.md (freshly regenerated)
6. ✅ Continue work with refreshed minimal context
```

**Sub-Agent maintains COMPACT_CONTEXT.md during work**:
- Receives initial version from Main Agent
- Regenerates after each PROGRESS.md update
- Keeps file current throughout task work
- Reports completion (does NOT delete - Main Agent handles cleanup)

**CRITICAL**: Sub-agent regenerates COMPACT_CONTEXT.md for updates, but Main Agent generates initial version and handles final cleanup.

**DURING WORK (After PROGRESS.md Updates)**:

```
1. ✅ Update PROGRESS.md with current task progress
2. ✅ Regenerate COMPACT_CONTEXT.md:
   a. Extract current task from machine_prompt.md again
   b. Re-embed machine_prompt content for current task
   c. Update status from new PROGRESS.md
   d. Update FILES list if changed
   e. Update NEXT_ACTIONS based on new progress
3. ✅ CLEAR ENTIRE CONTEXT (drop everything)
4. ✅ RELOAD: Read ONLY COMPACT_CONTEXT.md (freshly regenerated)
5. ✅ Continue work with refreshed minimal context
```

**CRITICAL**: Regeneration pulls fresh task content from machine_prompt.md each time, ensuring COMPACT_CONTEXT.md stays current.

**WHEN APPROACHING CONTEXT LIMIT**:

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

### Implementation

A complete Python script implementing the compact context generation algorithm is available:

**Template**: [generate_compact_context.py](../templates/generate_compact_context.py)

**Usage**:
```bash
python3 generate_compact_context.py PROGRESS.md machine_prompt.md
# Creates COMPACT_CONTEXT.md in same directory
```

**Key Functions**:
- `generate_compact_context()` - Main generation function
- `compact_rules_from_frontmatter()` - Embed rule summaries (~70K tokens saved)
- `extract_task_from_machine_prompt()` - Embed current task requirements
- `extract_current_task()` - Extract only current work
- Token reduction: 97% average savings (180K → 5K tokens)

See template file for full implementation details and compression algorithms.

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

A complete before/after example demonstrating the context compaction transformation is available:

**Template**: [compact_context_example.md](../templates/compact_context_example.md)

**Example Summary**:
- Before: Full accumulated context (180,000 tokens - 90% of limit)
- After: Ultra-compact COMPACT_CONTEXT.md (500 tokens)
- Post-reload: Fresh context with only needed files (5,000 tokens total)
- **Savings**: 175,000 tokens (97.2% reduction)

**Key Techniques Demonstrated**:
- References over content duplication
- Current work only (no historical context)
- Embedded machine_prompt content
- Embedded rule summaries (~70K tokens saved)
- Single sentence objective
- Pipe-delimited constraints
- Context reload cycle

See template file for full transformation example with detailed analysis.

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

A template file for COMPACT_CONTEXT.md structure is already available:

**Template**: [COMPACT_CONTEXT-template.md](../templates/COMPACT_CONTEXT-template.md)

This template provides the basic structure for manually creating compact context files.
For automated generation, use the Python script: [generate_compact_context.py](../templates/generate_compact_context.py)

---

## Makefile Integration

A complete Makefile template with context compaction targets is available:

**Template**: [Makefile.spec-template](../templates/Makefile.spec-template)

**Key Targets**:
- `compact-context` - Generate COMPACT_CONTEXT.md
- `generate-machine-prompt` - Generate machine_prompt.md (Rule 14)
- `verify-machine-prompt` - Check if regeneration needed

Copy template to specification directory and customize paths as needed.

---

## Summary

**Core Workflow**:
```
Main Agent: Generate machine_prompt.md + initial COMPACT_CONTEXT.md (with embedded rules) →
Spawn sub-agent with COMPACT_CONTEXT.md path →
Sub-Agent: Read COMPACT_CONTEXT.md (embedded rules + machine_prompt) →
Work on task →
Update PROGRESS.md →
Regenerate COMPACT_CONTEXT.md (re-embed rules + machine_prompt) →
Clear & Reload →
Continue OR Report completion →
Main Agent: Verify → Delete COMPACT_CONTEXT.md if complete → Commit
```

**Key Principles**:
1. ✅ Main Agent generates initial COMPACT_CONTEXT.md before spawning
2. ✅ Sub-agent receives and maintains during work
3. ✅ **Embed rule summaries** from specification frontmatter (~70K tokens saved)
4. ✅ Embed machine_prompt content (self-contained)
5. ✅ References replace content duplication
6. ✅ Current work only (no historical)
7. ✅ Clear and reload after updates
8. ✅ Main Agent handles cleanup after verification
9. ✅ PROGRESS.md rewritten per task (ephemeral)
10. ✅ COMPACT_CONTEXT.md deleted per task (ephemeral)

**Benefits**:
- 🚀 97% context reduction (180K → 5K tokens)
- 🚀 **~70K tokens saved** by embedding rule summaries vs loading full rule files
- 🚀 Prevents context limit errors
- 🚀 Improves agent performance
- 🚀 Enables indefinite work sessions
- 🚀 Reduces token costs dramatically
- 🚀 Maintains laser focus

**Combined with Rule 14**:
- Rule 14: 58% specification token reduction (requirements.md → machine_prompt.md)
- Rule 15: 97% runtime context reduction (verbose context → COMPACT_CONTEXT.md with embedded rules)
- **Total**: >98% token optimization

**Enforcement**:
- ❌ **USER WILL BE FRUSTRATED** if agent hits context limits
- ❌ Continuing without compaction when context >150K is FORBIDDEN
- ❌ Including full content instead of references wastes tokens
- ✅ Regular compaction and reload cycles are MANDATORY

---

*Created: 2026-02-01*
*Last Updated: 2026-02-01 (Clarified: Main Agent generates initial COMPACT_CONTEXT.md, sub-agent maintains during work, Main Agent handles cleanup.)*
*Purpose: Prevent context exhaustion through radical compaction and reload cycles*
*Inspiration: Concise system prompt principles - every word earns its place*
