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
spec:[name]|status:[status]|priority:[priority]|has_features:[bool]|has_fundamentals:[bool]

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

### Pseudo-Code

```python
def generate_machine_prompt(source_file: Path) -> str:
    """
    Generate machine-optimized prompt from human-readable source.

    Returns compressed, pipe-delimited, LLM-optimized content.
    """
    content = read_file(source_file)

    # Extract frontmatter
    frontmatter = parse_frontmatter(content)

    # Extract sections
    requirements = extract_section(content, "Requirements")
    tasks = extract_section(content, "Tasks")
    technical = extract_section(content, "Technical")
    verification = extract_section(content, "Verification")
    success = extract_section(content, "Success Criteria")

    # Compress each section
    meta = compress_frontmatter(frontmatter)
    docs = extract_file_references(content)  # Find all file paths mentioned
    reqs = compress_requirements(requirements)
    tasks_compressed = compress_tasks(tasks)
    tech = compress_technical(technical)
    verify = compress_verification(verification)
    success_compressed = compress_success_criteria(success)
    retrieval = extract_retrieval_checklist(content)

    # Build machine prompt
    machine_prompt = f"""# Machine-Optimized Prompt: {frontmatter['title']}

⚠️GENERATED|DO_NOT_EDIT|REGENERATE_FROM:{source_file.name}|GENERATED:{timestamp()}

## META
{meta}

## DOCS_TO_READ
{docs}

## REQUIREMENTS
{reqs}

## TASKS
{tasks_compressed}

## TECHNICAL
{tech}

## VERIFICATION
{verify}

## SUCCESS_CRITERIA
{success_compressed}

## RETRIEVAL_CHECKLIST
{retrieval}
"""

    return machine_prompt

def compress_requirements(requirements: list) -> str:
    """Convert verbose requirements to pipe-delimited format."""
    compressed = []
    for i, req in enumerate(requirements, 1):
        desc = req['description'].strip()
        constraints = ','.join(req.get('constraints', []))
        success = req.get('success_criteria', '')
        compressed.append(f"req{i}:{desc}|constraints:[{constraints}]|success:[{success}]")
    return '\n'.join(compressed)

def compress_tasks(tasks: list) -> str:
    """Convert task list to ultra-compact format."""
    compressed = []
    for task in tasks:
        status = '[x]' if task['completed'] else '[ ]'
        desc = task['description'].strip()
        files = ','.join(task.get('files', []))
        tests = ','.join(task.get('tests', []))
        deps = ','.join(task.get('depends_on', []))

        parts = [f"{status}task:{desc}"]
        if files:
            parts.append(f"files:[{files}]")
        if tests:
            parts.append(f"tests:[{tests}]")
        if deps:
            parts.append(f"depends:[{deps}]")

        compressed.append('|'.join(parts))
    return '\n'.join(compressed)

def extract_file_references(content: str) -> str:
    """Extract all file/document references from content."""
    # Find patterns like:
    # - documentation/module/doc.md
    # - .agents/stacks/rust.md
    # - src/file.rs
    # - ../requirements.md

    file_refs = set()
    # Regex patterns for file paths
    patterns = [
        r'`([^`]+\.md)`',           # Markdown files in backticks
        r'`([^`]+\.rs)`',           # Rust files
        r'documentation/[^\s]+',     # Documentation paths
        r'\.agents/[^\s]+',         # Agent files
        r'\.\./[^\s]+\.md',         # Parent directory references
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content)
        file_refs.update(matches)

    return '|'.join(sorted(file_refs))
```

---

## Example Transformation

### Before (requirements.md) - 450 tokens

```markdown
## Requirements

### Functional Requirements

1. **HTTP Client Core Structure**
   - Must implement a basic HTTP/1.1 client
   - Should support GET, POST, PUT, DELETE methods
   - Must handle request/response lifecycle
   - Connection management with keep-alive support

2. **Error Handling**
   - Comprehensive error types for all failure modes
   - Clear error messages for debugging
   - Proper error propagation

### Technical Specifications

- **Stack**: Rust, Tokio async runtime, Hyper for HTTP
- **Location**: src/http_client.rs
- **Dependencies**: tokio, hyper, serde

### Tasks

- [ ] Task 1: Implement core HTTP client structure
  - Create HttpClient struct
  - Implement connection pooling
  - Add keep-alive support
  - Files to modify: src/http_client.rs, src/lib.rs
  - Tests: tests/http_client_tests.rs

- [ ] Task 2: Add method implementations
  - GET, POST, PUT, DELETE methods
  - Request builder pattern
  - Files: src/http_client.rs
  - Tests: tests/methods_tests.rs
```

### After (machine_prompt.md) - 180 tokens (60% reduction)

```markdown
# Machine-Optimized Prompt: HTTP Client

⚠️GENERATED|DO_NOT_EDIT|REGENERATE_FROM:requirements.md|GENERATED:2026-02-01T12:00:00Z

## META
spec:http-client|status:in-progress|priority:high|has_features:true

## DOCS_TO_READ
requirements.md|documentation/http_client/doc.md|.agents/stacks/rust.md

## REQUIREMENTS
req1:impl basic HTTP/1.1 client|methods:[GET,POST,PUT,DELETE]|lifecycle:req/resp|conn:keep-alive
req2:error handling|types:comprehensive|messages:clear debug|propagation:proper

## TASKS
[ ]task1:impl core http client struct|files:[src/http_client.rs,src/lib.rs]|impl:[HttpClient,pool,keep-alive]|tests:[tests/http_client_tests.rs]
[ ]task2:add methods|methods:[GET,POST,PUT,DELETE]|pattern:builder|files:[src/http_client.rs]|tests:[tests/methods_tests.rs]

## TECHNICAL
stack:[rust,tokio,hyper]|loc:[src/http_client.rs]|deps:[tokio,hyper,serde]

## RETRIEVAL_CHECKLIST
search:http client impls|read:existing http code|check:async patterns|verify:error handling
```

**Token Savings**: 450 → 180 tokens (60% reduction, 270 tokens saved)

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

### Makefile Target

Add to specification Makefile:
```makefile
.PHONY: generate-machine-prompt

generate-machine-prompt:
	@echo "Generating machine-optimized prompts..."
	@python3 ../../scripts/generate_machine_prompt.py requirements.md
	@if [ -d features ]; then \
		for feature in features/*/feature.md; do \
			dir=$$(dirname $$feature); \
			python3 ../../scripts/generate_machine_prompt.py $$feature; \
		done \
	fi
	@echo "✓ Machine prompts generated"
```

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
