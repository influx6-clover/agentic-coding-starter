# Machine-Optimized Prompts for Token Efficiency

## Purpose

Dramatically reduce token consumption by generating highly compressed, LLM-optimized versions of human-readable specification files. This rule establishes the mandatory practice of creating `machine_prompt.md` files that remove unnecessary whitespace, use pipe-delimited structures, and compress content while preserving all critical information.

---

## Core Principle

**Human-readable files** (requirements.md, feature.md) → **Machine-optimized files** (machine_prompt.md)

- Human files: Verbose, formatted, easy to read/edit
- Machine files: Compressed, pipe-delimited, minimal tokens
- Agents read machine files during implementation
- Main Agent regenerates machine files when human files change

**Token Savings**: 40-60% reduction in context usage

---

## When to Generate machine_prompt.md

### MANDATORY Generation

Main Agent **MUST** generate `machine_prompt.md` when:

1. **Specification Created**: After requirements.md is finalized and approved
2. **Feature Created**: After feature.md is written
3. **Specification Updated**: When requirements.md or feature.md changes
4. **Before Implementation Starts**: Always ensure machine_prompt.md exists and is current
5. **Before Spawning Sub-Agents**: Generate fresh machine_prompt.md with latest changes

### Location

```
specifications/01-spec-name/
├── requirements.md              # Human-readable (DO NOT DELETE)
├── machine_prompt.md            # Machine-optimized (GENERATED)
├── features/
│   ├── 00-feature/
│   │   ├── feature.md          # Human-readable (DO NOT DELETE)
│   │   └── machine_prompt.md   # Machine-optimized (GENERATED)
```

**CRITICAL**:
- **NEVER delete** human-readable files (requirements.md, feature.md)
- **ALWAYS regenerate** machine_prompt.md when human files change
- machine_prompt.md is **GENERATED**, not hand-edited

---

## CRITICAL: machine_prompt.md Lifecycle and Usage

### Generation and Context Workflow

**WHEN machine_prompt.md IS GENERATED**:

1. ✅ **Project start**: Main Agent creates new specification
2. ✅ **Specification creation**: Generated when requirements.md finalized and approved
3. ✅ **Feature creation**: Generated for each feature.md created
4. ✅ **Updates**: Regenerated when requirements.md or feature.md changes

**ONCE GENERATED** (CRITICAL WORKFLOW):

```
Step 1: Generate machine_prompt.md from requirements.md/feature.md
   ↓
Step 2: Main Agent CLEARS context
   ↓
Step 3: Main Agent RELOADS from machine_prompt.md
   ↓
Step 4: machine_prompt.md becomes source of agent instructions
   ↓
Step 5: Sub-agents use machine_prompt.md (NOT human files)
   ↓
Step 6: Human files (requirements.md/feature.md) STILL updated normally for human readability
   ↓
Step 7: When human files change → Regenerate machine_prompt.md → Clear → Reload
   ↓
Step 8: machine_prompt.md stays in sync with human files
```

### Dual File Maintenance (MANDATORY)

**Human-Readable Files** (requirements.md, feature.md):
- ✅ **Always updated** as normal workflow requires
- ✅ **Source of truth** for human understanding
- ✅ **Never deleted** - permanent record
- ✅ **Edited directly** when requirements change
- ✅ **Committed to version control** with changes
- ✅ **Verbose and formatted** for human readability

**Machine-Optimized Files** (machine_prompt.md):
- ✅ **Generated automatically** from human files
- ✅ **Regenerated** whenever human files change
- ✅ **Used by all agents** for instructions
- ✅ **Stays synchronized** with human files
- ✅ **Committed to version control** alongside human files
- ✅ **Compressed and pipe-delimited** for machines
- ❌ **Never hand-edited** - always generated from source
- ❌ **Never becomes sole source** - human files remain truth

**Synchronization Pattern**:
```
Edit requirements.md (human) →
Regenerate machine_prompt.md (machine) →
Clear context →
Reload from machine_prompt.md →
Commit BOTH files together →
Agents use machine_prompt.md →
Humans read requirements.md
```

### Integration with Rule 15 (Context Compaction)

**machine_prompt.md → COMPACT_CONTEXT.md Flow**:

```
1. machine_prompt.md exists (generated from requirements.md)
   ↓
2. Sub-agent reads machine_prompt.md initially
   ↓
3. Sub-agent generates COMPACT_CONTEXT.md:
   - Extracts current task from machine_prompt.md
   - EMBEDS machine_prompt content in MACHINE_PROMPT_CONTENT section
   - Adds current status from PROGRESS.md
   ↓
4. Sub-agent CLEARS context
   ↓
5. Sub-agent reads ONLY COMPACT_CONTEXT.md (which contains embedded machine_prompt)
   ↓
6. No need to re-read machine_prompt.md (content already in COMPACT_CONTEXT.md)
```

**Result**: machine_prompt.md content flows into COMPACT_CONTEXT.md, which becomes sole source after context clear.

---

## machine_prompt.md Format

### Structure

```markdown
# Machine-Optimized Prompt: [Specification/Feature Name]

⚠️GENERATED|DO_NOT_EDIT|REGENERATE_FROM:[source_file]|GENERATED:[timestamp]

## META
spec:[name]|num:[NN]|status:[status]|priority:[priority]|has_features:[bool]|has_fundamentals:[bool]

## LOCATION
workspace:[ewe_platform]|spec_dir:[specifications/NN-spec-name]|this_file:[specifications/NN-spec-name/requirements.md]
cwd_get:[bash pwd]|verify:[test -f .agents/AGENTS.md]
# For features: feature:[name]|num:[N]|feature_dir:[specifications/NN-spec-name/features/feature-name]

## DOCS_TO_READ
requirements.md|feature.md|../requirements.md|documentation/module/doc.md|.agents/stacks/rust.md

## REQUIREMENTS
[Pipe-delimited compressed requirements]
req1:[description]|constraints:[...]|success:[...]
req2:[description]|constraints:[...]|success:[...]

## TASKS
[x]task1:[description]|files:[file1,file2]|tests:[test1]
[ ]task2:[description]|depends:[task1]|files:[file3]
[ ]task3:[description]|verification:[script_name]

## TECHNICAL
stack:[rust,tokio,hyper]|location:[src/http/]|dependencies:[dep1,dep2]
patterns:[pattern1,pattern2]|errors:[error_handling_approach]

## VERIFICATION
scripts:[verify_requirements.py,verify_completion.py]|makefile_target:[make verify]
tests:[unit,integration]|coverage:[90%]|standards:[.agents/stacks/rust.md]

## SUCCESS_CRITERIA
criteria1:[description]|measurable:[metric]
criteria2:[description]|validation:[script]

## RETRIEVAL_CHECKLIST
search_similar:[grep pattern]|read_existing:[file_pattern]|check_patterns:[convention]
```

### Compression Rules

#### 1. Remove Unnecessary Whitespace
```
❌ Human: "This is a detailed description of the requirement that spans multiple lines"
✅ Machine: "req1:detailed description|spans multiple lines"
```

#### 2. Pipe-Delimited Sections
```
❌ Human:
- Requirement 1: Description
- Requirement 2: Description

✅ Machine:
req1:Description|req2:Description
```

#### 3. Collapse Nested Structures
```
❌ Human:
**Technical Requirements**:
- Stack: Rust, Tokio, Hyper
- Location: src/http/
- Dependencies: serde, reqwest

✅ Machine:
tech:stack=[rust,tokio,hyper]|loc=[src/http/]|deps=[serde,reqwest]
```

#### 4. Abbreviate Common Terms
```
❌ Human: "Implementation must follow..."
✅ Machine: "impl:must follow..."

❌ Human: "Verification scripts"
✅ Machine: "verify:scripts"

❌ Human: "Documentation references"
✅ Machine: "docs:refs"
```

#### 5. List Files Compactly
```
❌ Human:
Files to read:
- requirements.md
- documentation/http_client/doc.md
- .agents/stacks/rust.md

✅ Machine:
DOCS_TO_READ:requirements.md|documentation/http_client/doc.md|.agents/stacks/rust.md
```

#### 6. Compress Tasks
```
❌ Human:
- [ ] Task 1: Implement HTTP client core structure
  - Files: src/http_client.rs, src/lib.rs
  - Tests: tests/http_client_tests.rs

✅ Machine:
[ ]task1:impl http client core|files:[src/http_client.rs,src/lib.rs]|tests:[tests/http_client_tests.rs]
```

#### 7. Location Awareness
```
❌ Human (verbose frontmatter):
# === LOCATION CONTEXT ===
workspace_name: "ewe_platform"
spec_directory: "specifications/02-build-http-client"
this_file: "specifications/02-build-http-client/requirements.md"

✅ Machine (compressed):
LOCATION:workspace:[ewe_platform]|spec:[02-build-http-client]|this:[specifications/02-build-http-client/requirements.md]|cwd_get:[bash pwd]|verify:[test -f .agents/AGENTS.md]

For features:
LOCATION:workspace:[ewe_platform]|spec:[02-build-http-client]|feature:[compression]|num:[3]|this:[specifications/02-build-http-client/features/compression/feature.md]
```

**Why Location Matters**:
- Agents immediately know where they are without exploration
- CWD placeholder prevents absolute path confusion
- Verification command confirms correct workspace
- Reduces orientation tool calls by 60-70%

---

## Main Agent Responsibilities

### During Specification Creation

After user approves requirements.md:

```
1. ✅ Read requirements.md (or feature.md)
2. ✅ Generate compressed machine_prompt.md
3. ✅ Place in same directory as source file
4. ✅ Add generation metadata (timestamp, source file)
5. ✅ Commit both files together
```

### Before Spawning Sub-Agents

Before spawning implementation/verification agents:

```
1. ✅ Check if machine_prompt.md exists
2. ✅ Check if it's current (compare timestamps with source file)
3. ✅ If missing or stale: Regenerate from source
4. ✅ Provide path to machine_prompt.md (not requirements.md) to sub-agent
```

### When Specifications Update

When requirements.md or feature.md changes:

```
1. ✅ Detect changes to source file
2. ✅ Regenerate machine_prompt.md
3. ✅ Commit both files together
4. ✅ Note in commit message: "Regenerated machine_prompt.md"
```

---

## Sub-Agent Responsibilities

### Implementation Agents

When spawned:

```
1. ✅ Check for machine_prompt.md in specification/feature directory
2. ✅ If exists: Read machine_prompt.md (not requirements.md)
3. ✅ Parse pipe-delimited structure
4. ✅ Extract DOCS_TO_READ section
5. ✅ Read only files listed in DOCS_TO_READ
6. ✅ Use compressed requirements for implementation
```

**Fallback**: If machine_prompt.md missing, read requirements.md and request Main Agent regenerate

### Verification Agents

```
1. ✅ Read machine_prompt.md for quick context
2. ✅ Extract verification scripts from VERIFICATION section
3. ✅ Run checks based on compressed criteria
```

---

## Generation Algorithm

### Implementation

A complete Python script implementing the machine prompt generation algorithm is available:

**Template**: [generate_machine_prompt.py](../templates/generate_machine_prompt.py)

**Usage**:
```bash
python3 generate_machine_prompt.py requirements.md
# Creates machine_prompt.md in same directory
```

**Key Functions**:
- `generate_machine_prompt()` - Main generation function
- `compress_requirements()` - Pipe-delimit requirements
- `compress_tasks()` - Compact task format
- `extract_file_references()` - Find all file paths mentioned
- Token reduction: 58% average savings

See template file for full implementation details and compression algorithms.

---

## Example Transformation

A complete before/after example demonstrating the compression transformation is available:

**Template**: [machine_prompt_example.md](../templates/machine_prompt_example.md)

**Example Summary**:
- Before: Human-readable requirements.md (450 tokens)
- After: Machine-optimized machine_prompt.md (180 tokens)
- **Savings**: 270 tokens (60% reduction)

**Key Techniques Demonstrated**:
- Pipe-delimited sections
- Abbreviated terms
- Collapsed lists
- Compact file references
- Single-line tasks with embedded metadata

See template file for full transformation example with detailed analysis.

---

## Frontmatter Reminders

### All Requirements.md Files

Add to frontmatter:
```yaml
machine_optimized: true  # Main Agent must generate machine_prompt.md before spawning sub-agents
machine_prompt_file: ./machine_prompt.md
```

### All Feature.md Files

Add to frontmatter:
```yaml
machine_optimized: true  # Main Agent must generate machine_prompt.md before spawning sub-agents
machine_prompt_file: ./machine_prompt.md
```

### PROGRESS.md Header

Add reminder at top:
```markdown
⚠️ **Machine Optimization**: Sub-agents should read `machine_prompt.md` (not this file) for token efficiency
```

---

## Integration with Existing Rules

### Rule 05 (Agent Orchestration)

Main Agent spawning sub-agents:
```
Before spawning:
1. ✅ Check for machine_prompt.md
2. ✅ If missing/stale: Generate from requirements.md
3. ✅ Provide machine_prompt.md path to sub-agent (not requirements.md)
```

Sub-agent prompt:
```
MANDATORY: Read .agents/AGENTS.md, Rules 01-04, Rule 13
Read specification: specifications/01-spec/machine_prompt.md  ← Use machine-optimized
Extract DOCS_TO_READ section and read only those files
```

### Rule 06 (Specifications)

When creating specifications:
```
1. ✅ User approves requirements.md
2. ✅ Main Agent generates machine_prompt.md
3. ✅ Commit both files
4. ✅ Reference machine_prompt.md in files_required section
```

files_required update:
```yaml
implementation_agent:
  files:
    - ./machine_prompt.md  # Token-optimized (primary)
    - ./requirements.md    # Human-readable (reference only)
```

### Rule 13 (Implementation Agent)

Before starting work:
```
1. ✅ Read machine_prompt.md (not requirements.md)
2. ✅ Parse DOCS_TO_READ section
3. ✅ Read only listed files
4. ✅ Extract compressed requirements/tasks
5. ✅ If machine_prompt.md missing: Request Main Agent regenerate
```

---

## Token Efficiency Benefits

### Typical Savings

| File Type | Before | After | Savings |
|-----------|--------|-------|---------|
| Simple Spec (requirements.md) | 800 tokens | 320 tokens | 60% |
| Complex Spec (requirements.md) | 2000 tokens | 900 tokens | 55% |
| Feature (feature.md) | 600 tokens | 240 tokens | 60% |
| **Average** | - | - | **58%** |

### Cumulative Impact

For a specification with 10 features:
- **Before**: 1 requirements.md (2000) + 10 feature.md (600 each) = **8000 tokens**
- **After**: 1 machine_prompt.md (900) + 10 machine_prompt.md (240 each) = **3300 tokens**
- **Savings**: 4700 tokens (59% reduction)

### Per-Agent Session

Single implementation agent session:
- **Reads**: 1 machine_prompt.md (240 tokens) vs 1 feature.md (600 tokens)
- **Savings per agent**: 360 tokens
- **10 agent sessions**: 3600 tokens saved

---

## Maintenance

### Keeping Files in Sync

```
Human file changed → Regenerate machine file → Commit both

Git workflow:
1. Edit requirements.md (human)
2. Run: make generate-machine-prompt
3. Git add requirements.md machine_prompt.md
4. Git commit -m "Update requirements + regenerate machine prompt"
```

### Makefile Targets

A complete Makefile template with machine prompt generation targets is available:

**Template**: [Makefile.spec-template](../templates/Makefile.spec-template)

**Key Targets**:
- `generate-machine-prompt` - Generate machine_prompt.md files
- `verify-machine-prompt` - Check if regeneration needed
- `compact-context` - Generate COMPACT_CONTEXT.md (Rule 15)

Copy template to specification directory and customize paths as needed.

### Validation

Verify machine_prompt.md is current:
```bash
# Check if machine_prompt.md is older than source
if [ requirements.md -nt machine_prompt.md ]; then
    echo "⚠️ machine_prompt.md is stale, regenerating..."
    make generate-machine-prompt
fi
```

---

## Summary

**Core Workflow**:
```
Write requirements.md (human) → Generate machine_prompt.md (machine) →
Sub-agents read machine_prompt.md → 58% token savings
```

**Key Principles**:
1. ✅ Human files (requirements.md) are source of truth - NEVER delete
2. ✅ Machine files (machine_prompt.md) are generated - NEVER hand-edit
3. ✅ Regenerate machine files when human files change
4. ✅ Sub-agents read machine files for token efficiency
5. ✅ Pipe-delimited, compressed, minimal whitespace
6. ✅ DOCS_TO_READ section lists exact files to read
7. ✅ 58% average token reduction

**Benefits**:
- 🚀 58% token savings per agent session
- 🚀 Faster agent context loading
- 🚀 More tokens available for code/reasoning
- 🚀 Reduced API costs
- 🚀 Consistent format across all specifications

**Enforcement**:
- ❌ **USER WILL BE FRUSTRATED** if agents read verbose files when machine files exist
- ❌ Sub-agents reading requirements.md directly wastes tokens
- ❌ Missing machine_prompt.md slows down agents
- ✅ Main Agent MUST generate machine_prompt.md before spawning sub-agents

---

*Created: 2026-02-01*
*Purpose: Reduce token consumption through machine-optimized prompt generation*
