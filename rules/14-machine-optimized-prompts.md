# Machine-Optimized Prompts for Token Efficiency

## Purpose

Dramatically reduce token consumption by generating highly compressed, LLM-optimized versions of human-readable specification files.

**Token Savings**: 40-60% reduction in context usage

## Core Principle

**Human-readable files** (requirements.md, feature.md) → **Machine-optimized files** (machine_prompt.md)

- Human files: Verbose, formatted, easy to read/edit
- Machine files: Compressed, pipe-delimited, minimal tokens
- Agents read machine files during implementation
- Main Agent regenerates machine files when human files change

## When to Generate machine_prompt.md

Main Agent MUST generate when:
1. Specification created (after requirements.md finalized/approved)
2. Feature created (after feature.md written)
3. Specification updated (requirements.md or feature.md changes)
4. Before implementation starts
5. Before spawning sub-agents

## Location

```
specifications/01-spec-name/
├── requirements.md              # Human-readable (DO NOT DELETE)
├── machine_prompt.md            # Machine-optimized (GENERATED)
├── features/00-feature/
│   ├── feature.md               # Human-readable (DO NOT DELETE)
│   └── machine_prompt.md        # Machine-optimized (GENERATED)
```

**CRITICAL:**
- NEVER delete human-readable files
- ALWAYS regenerate machine_prompt.md when human files change
- machine_prompt.md is GENERATED, not hand-edited

## Lifecycle and Usage

### Generation and Context Workflow

```
1. Generate machine_prompt.md from requirements.md/feature.md
   ↓
2. Main Agent CLEARS context
   ↓
3. Main Agent RELOADS from machine_prompt.md
   ↓
4. machine_prompt.md becomes source of agent instructions
   ↓
5. Sub-agents use machine_prompt.md (NOT human files)
   ↓
6. Human files STILL updated for human readability
   ↓
7. When human files change → Regenerate → Clear → Reload
```

### Dual File Maintenance (MANDATORY)

**Human-Readable Files** (requirements.md, feature.md):
- Always updated as normal workflow requires
- Source of truth for human understanding
- Never deleted - permanent record
- Edited directly when requirements change
- Committed to version control
- Verbose and formatted for readability

**Machine-Optimized Files** (machine_prompt.md):
- Generated automatically from human files
- Regenerated whenever human files change
- Used by all agents for instructions
- Committed to version control alongside human files
- Compressed and pipe-delimited for machines
- Never hand-edited - always generated
- Never becomes sole source - human files remain truth

**Synchronization Pattern:**
```
Edit requirements.md → Regenerate machine_prompt.md → Clear context →
Reload from machine_prompt.md → Commit BOTH files → Agents use machine →
Humans read requirements
```

### Integration with Rule 15 (Context Compaction)

```
1. machine_prompt.md exists (from requirements.md)
   ↓
2. Sub-agent reads machine_prompt.md initially
   ↓
3. Sub-agent generates COMPACT_CONTEXT.md:
   - Extracts current task
   - EMBEDS machine_prompt content
   - Adds current status from PROGRESS.md
   ↓
4. Sub-agent CLEARS context
   ↓
5. Sub-agent reads ONLY COMPACT_CONTEXT.md (contains embedded machine_prompt)
```

## machine_prompt.md Format

### Structure

```markdown
# Machine-Optimized Prompt: [Name]

⚠️GENERATED|DO_NOT_EDIT|REGENERATE_FROM:[source]|GENERATED:[timestamp]

## META
spec:[name]|num:[NN]|status:[status]|priority:[priority]

## LOCATION
workspace:[ewe_platform]|spec_dir:[path]|this_file:[file]
cwd_get:[bash pwd]|verify:[test -f .agents/AGENTS.md]

## DOCS_TO_READ
requirements.md|feature.md|.agents/stacks/rust.md

## REQUIREMENTS
req1:[description]|constraints:[...]|success:[...]
req2:[description]|constraints:[...]|success:[...]

## TASKS
[x]task1:[description]|files:[file1,file2]|tests:[test1]
[ ]task2:[description]|depends:[task1]|files:[file3]

## TECHNICAL
stack:[rust,tokio,hyper]|location:[src/http/]|dependencies:[dep1,dep2]
patterns:[pattern1,pattern2]|errors:[error_handling]

## VERIFICATION
scripts:[verify.py]|makefile:[make verify]
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
req1:[description]|constraints:[...]
req2:[description]|constraints:[...]
```

#### 3. Abbreviate Common Terms
```
❌ Human: "specification", "requirement", "description"
✅ Machine: "spec", "req", "desc"
```

#### 4. Compress Task Format
```
❌ Human:
- [ ] Task 1: Implement feature X
  - Files: src/main.rs, src/lib.rs
  - Tests: tests/main_test.rs

✅ Machine:
[ ]task1:implement feature X|files:[src/main.rs,src/lib.rs]|tests:[tests/main_test.rs]
```

#### 5. Inline Multi-Line Content
```
❌ Human:
Requirement 1:
  Description: This is a long description
  Constraints: Must be fast
  Success: Passes tests

✅ Machine:
req1:long description|constraints:fast|success:passes tests
```

## Generation Process

### Main Agent Responsibility

1. Read requirements.md or feature.md completely
2. Extract all critical information
3. Apply compression rules
4. Generate machine_prompt.md with pipe-delimited format
5. Save to same directory as source file
6. Commit BOTH files together
7. Clear context and reload from machine_prompt.md

### Template

**Template Location**: `.agents/templates/machine-prompt-template.md`

Contains structure and examples for generating machine_prompt.md files.

## Usage by Sub-Agents

Sub-agents MUST:
1. Read machine_prompt.md (NOT requirements.md) for current task
2. Parse pipe-delimited format
3. Extract relevant sections
4. Follow compressed instructions
5. If unclear: Request Main Agent regenerate with more detail

## Maintenance

### When Human Files Change

1. Edit requirements.md or feature.md as needed
2. Regenerate machine_prompt.md from updated source
3. Clear context and reload from new machine_prompt.md
4. Commit BOTH files together
5. Sub-agents automatically use updated machine file

### Versioning

- Both human and machine files committed together
- Git history shows both versions side-by-side
- Can always regenerate machine file from human file
- Human file is canonical source of truth

## Benefits

1. **40-60% Token Reduction**: Compressed format uses fewer tokens
2. **Faster Processing**: Less content to read and parse
3. **Same Information**: All critical details preserved
4. **Human Readable Backup**: requirements.md always available
5. **Automated**: Main Agent handles generation
6. **Synchronized**: Both files stay in sync

## Enforcement

### Must Do
1. Generate machine_prompt.md for all specifications and features
2. Regenerate when human files change
3. Sub-agents read machine files, not human files
4. Commit both human and machine files together
5. Never hand-edit machine files

### Must Not Do
1. Delete human-readable files
2. Use human files as source for sub-agents
3. Hand-edit machine_prompt.md
4. Commit machine file without corresponding human file update
5. Let machine and human files get out of sync

### Critical Violations
1. Sub-agent reading requirements.md instead of machine_prompt.md
2. Machine file not regenerated after human file changes
3. Human file deleted
4. Machine file hand-edited instead of regenerated

## Summary

**Golden Rules:**
1. **Human files for humans** - verbose, formatted, source of truth
2. **Machine files for machines** - compressed, pipe-delimited, generated
3. **Always maintain both** - never delete human files
4. **Regenerate on change** - keep machine files synchronized
5. **40-60% token savings** - significant efficiency gain
6. **Main Agent generates** - sub-agents consume

---

_Version: 1.0 - Last Updated: 2026-02-27_
