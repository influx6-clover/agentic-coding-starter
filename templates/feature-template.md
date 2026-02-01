---
# === IDENTIFICATION ===
spec_name: "[NN-spec-name]"  # Parent spec (e.g., "02-build-http-client")
spec_number: NN  # Parent spec number (e.g., 02)
feature_name: "feature-name"  # This feature's name (e.g., "compression")
feature_number: N  # Feature number within spec (e.g., 3 for compression)
description: Brief one-sentence description of what this feature implements

# === LOCATION CONTEXT ===
# To find this file's location:
# 1. Run: bash pwd  (gets current working directory = CWD)
# 2. This file is at: CWD/specifications/[NN-spec-name]/features/[feature-name]/feature.md
# 3. Workspace root: CWD (contains .agents/, specifications/, documentation/, backends/)
workspace_name: "ewe_platform"  # Project workspace name
spec_directory: "specifications/[NN-spec-name]"  # Parent spec directory (relative to CWD)
feature_directory: "specifications/[NN-spec-name]/features/[feature-name]"  # This feature's directory
this_file: "specifications/[NN-spec-name]/features/[feature-name]/feature.md"  # This file's path

# === STATUS ===
status: pending
priority: medium
depends_on: []  # Other features this depends on (e.g., ["foundation", "connection"])
estimated_effort: medium
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
author: Main Agent

# === CONTEXT OPTIMIZATION ===
machine_optimized: true  # Main Agent MUST generate machine_prompt.md before spawning sub-agents
machine_prompt_file: ./machine_prompt.md  # Sub-agents read this (NOT feature.md) for 58% token savings
context_optimization: true  # Sub-agents MUST generate COMPACT_CONTEXT.md before work, reload after updates
compact_context_file: ./COMPACT_CONTEXT.md  # Ultra-compact current task context (97% reduction)
context_reload_required: true  # Clear and reload from compact context regularly to prevent context limit errors

# === TASKS ===
tasks:
  completed: 0
  uncompleted: 0
  total: 0
  completion_percentage: 0
files_required:
  implementation_agent:
    rules:
      - .agents/rules/01-rule-naming-and-structure.md
      - .agents/rules/02-rules-directory-policy.md
      - .agents/rules/03-dangerous-operations-safety.md
      - .agents/rules/04-work-commit-and-push-rules.md
      - .agents/rules/13-implementation-agent-guide.md
      - .agents/rules/11-skills-usage.md
      - .agents/stacks/[language].md
    files:
      - ../requirements.md
      - ./feature.md
      - ./templates/ # If feature has templates
      - ../fundamentals/* # If parent spec has_fundamentals: true
  verification_agent:
    rules:
      - .agents/rules/01-rule-naming-and-structure.md
      - .agents/rules/02-rules-directory-policy.md
      - .agents/rules/03-dangerous-operations-safety.md
      - .agents/rules/04-work-commit-and-push-rules.md
      - .agents/rules/08-verification-workflow-complete-guide.md
      - .agents/stacks/[language].md
    files:
      - ../requirements.md
      - ./feature.md
---

# [Feature Name]

## 📍 Location Reference

**How to find your location**:
1. Run `bash pwd` to get current working directory (CWD)
2. This file is at: `CWD/specifications/[NN-spec-name]/features/[feature-name]/feature.md`
3. Workspace root is CWD (contains `.agents/`, `specifications/`, `documentation/`, `backends/`)

**Quick paths** (all relative to workspace root = CWD):
- Parent spec: `specifications/[NN-spec-name]/requirements.md`
- This feature: `specifications/[NN-spec-name]/features/[feature-name]/`
- This file: `specifications/[NN-spec-name]/features/[feature-name]/feature.md`
- Machine prompt: `specifications/[NN-spec-name]/features/[feature-name]/machine_prompt.md`
- Templates: `specifications/[NN-spec-name]/features/[feature-name]/templates/` (if exists)
- Parent progress: `specifications/[NN-spec-name]/PROGRESS.md`
- Parent learnings: `specifications/[NN-spec-name]/LEARNINGS.md`
- Agent rules: `.agents/rules/`
- Stack files: `.agents/stacks/`

**Verification**: If you can read `.agents/AGENTS.md` from CWD, you're in the right place!

**Quick Navigation Commands**:
```bash
# Verify you're in workspace root
test -f .agents/AGENTS.md && echo "✓ In workspace root" || echo "✗ Wrong location"

# View parent spec
cat specifications/[NN-spec-name]/requirements.md

# List all features in parent spec
ls -d specifications/[NN-spec-name]/features/*/

# Check feature dependencies (other features listed in depends_on)
cat specifications/[NN-spec-name]/features/[dependency-name]/feature.md

# View this feature's structure
tree specifications/[NN-spec-name]/features/[feature-name]/

# Find related code (adjust pattern to your feature)
find backends/ -name "*[relevant-pattern]*" -type f
```

---

## 🔍 CRITICAL: Retrieval-Led Reasoning Required

**ALL agents implementing this feature MUST use retrieval-led reasoning.**

### Before Starting Implementation

**YOU MUST** (in this order):
1. ✅ **Search the codebase** for similar implementations using Grep/Glob
2. ✅ **Read existing code** in related modules to understand patterns
3. ✅ **Check stack files** (`.agents/stacks/[language].md`) for language-specific conventions
4. ✅ **Read parent specification** (`../requirements.md`) for high-level context
5. ✅ **Read module documentation** for modules this feature touches
6. ✅ **Check dependencies** by reading other feature files referenced in `depends_on`
7. ✅ **Follow discovered patterns** consistently with existing codebase

### FORBIDDEN Approaches

**YOU MUST NOT**:
- ❌ Assume patterns based on typical practices without checking this codebase
- ❌ Implement without searching for similar features first
- ❌ Apply generic solutions without verifying project conventions
- ❌ Guess at naming conventions, file structures, or patterns
- ❌ Use pretraining knowledge without validating against actual project code

### Retrieval Checklist

Before implementing, answer these questions by reading code:
- [ ] What similar features exist in this project? (use Grep to find)
- [ ] What patterns do they follow? (read their implementations)
- [ ] What naming conventions are used? (observed from existing code)
- [ ] How are errors handled in similar code? (check error patterns)
- [ ] What testing patterns exist? (read existing test files)
- [ ] Are there existing helper functions I can reuse? (search thoroughly)

### Enforcement

- Show your retrieval steps in your work report
- Reference specific files/patterns you discovered
- Explain how your implementation matches existing patterns
- "I assumed..." responses will be rejected - only "I found in [file]..." accepted

---

## 🚀 CRITICAL: Token and Context Optimization

**ALL agents implementing this feature MUST follow token and context optimization protocols.**

### Machine-Optimized Prompts (Rule 14)

**Main Agent MUST**:
1. Generate `machine_prompt.md` from this file (feature.md) when feature created
2. Use pipe-delimited compression (58% token reduction)
3. Commit machine_prompt.md alongside feature.md
4. Regenerate when feature.md updates
5. Provide machine_prompt.md path to sub-agents (NOT feature.md)

**Sub-Agents MUST**:
- Read `machine_prompt.md` (NOT this verbose feature.md file)
- 58% token savings: 600→240 tokens typical
- Parse DOCS_TO_READ section for files to load

### Context Compaction (Rule 15)

**Sub-Agents MUST** (before starting work):
1. Read machine_prompt.md and PROGRESS.md
2. Generate `COMPACT_CONTEXT.md`:
   - Embed machine_prompt.md content for current task
   - Extract current status from PROGRESS.md
   - List files for current task only
   - Ultra-compact: 500-800 tokens
3. CLEAR entire context (drop everything)
4. RELOAD from COMPACT_CONTEXT.md only
5. Proceed with 97% less context (180K→5K tokens)

**After PROGRESS.md Updates**:
- Regenerate COMPACT_CONTEXT.md (embed fresh machine_prompt content)
- Clear and reload
- Maintain minimal context throughout work

**COMPACT_CONTEXT.md Lifecycle**:
- Generated fresh per task
- Contains ONLY current task (no history)
- Deleted when task completes
- Rewritten from scratch for next task

**See**:
- Rule 14: Machine-Optimized Prompts (.agents/rules/14-machine-optimized-prompts.md)
- Rule 15: Instruction Compaction (.agents/rules/15-instruction-compaction.md)
- Templates: COMPACT_CONTEXT-template.md for format

---

## Overview

Brief summary of what this feature implements and its purpose within the larger specification.

## Dependencies

This feature depends on:
- `[other-feature]` - Why this dependency exists

This feature is required by:
- `[dependent-feature]` - Why this feature is needed

## Requirements

### Functional Requirements

1. **Requirement 1**
   - Detail about the requirement
   - Expected behavior

2. **Requirement 2**
   - Detail about the requirement
   - Expected behavior

### Technical Requirements

- **Pattern to follow**: Description of required patterns
- **Types to create**: List of types/structs to implement
- **Integrations**: What this connects to

## Implementation Details

### Key Structures

```rust
// Example structure - or reference templates/
pub struct ExampleStruct {
    // fields
}
```

### Key Functions

| Function | Purpose | Location |
|----------|---------|----------|
| `function_name()` | What it does | `file.rs` |

## Templates

See `templates/` directory for:
- `example-struct.rs` - Base structure template
- `example-impl.rs` - Implementation template

---

## Tasks

> **Task Tracking**: Mark tasks as `[x]` after completing AND verifying each task. Update frontmatter counts (completed/uncompleted/total/completion_percentage) immediately. Commit after task completion + verification pass (Rule 04).
>
> **Important**: Each feature manages its own task tracking. Update this file's frontmatter as tasks complete.

### Implementation Tasks
- [ ] Task 1: Implement core structure
- [ ] Task 2: Add key functions
- [ ] Task 3: Integrate with dependencies

### Testing Tasks
- [ ] Write unit tests for [component]
- [ ] Write integration tests
- [ ] Run verification commands

### Documentation Tasks
- [ ] Document public APIs
- [ ] Add usage examples

---

## Success Criteria

- [ ] Criterion 1 - specific and verifiable
- [ ] Criterion 2 - specific and verifiable
- [ ] All unit tests pass
- [ ] Code passes `cargo fmt` and `cargo clippy`

## Verification Commands

```bash
cargo fmt -- --check
cargo clippy -- -D warnings
cargo test --package [package] -- [test_filter]
cargo build --package [package]
```

## Agent Instructions

### Before Starting (MANDATORY)

**CRITICAL**: Main Agent MUST spawn Review Agent before starting this feature.

**Review Agent Responsibilities**:
1. ✅ Read parent specification's requirements.md
2. ✅ Read this feature.md file completely
3. ✅ **VERIFY in code** that dependent features are ACTUALLY complete:
   - Check that code exists (not just documentation claims)
   - Verify tests pass for dependencies
   - Validate types/functions this feature needs are present
4. ✅ Read any templates referenced in templates/ directory
5. ✅ Analyze current codebase state vs claimed completion status
6. ✅ Assess readiness: GO / STOP / CLARIFY

**Why This Matters**:
- Documentation may claim features complete when they're not
- Previous work may have gaps or issues
- Prevents building on broken foundations
- **USER EXPECTS verification before implementation starts**

### For Main Agent

**CRITICAL REMINDERS**:

1. **Load Relevant Rules**: Before starting work, ensure you have loaded all rules specified in parent `requirements.md` file's `files_required.main_agent.rules`.

2. **Autonomous Agent Behavior**: Follow `.agents/rules/05-coding-practice-agent-orchestration.md` - Work autonomously without unnecessary back-and-forth. Make informed decisions based on loaded context and rules.

3. **Implementation Review First**:
   - **ALWAYS** start by reviewing current implementation status for this feature
   - Verify if reported issues are still pending or already resolved
   - Check git history and actual code state for feature-related files
   - Do NOT assume issues are unresolved without verification

4. **No Unnecessary Questions**:
   - If this feature is already approved, it tells you what to do
   - Do NOT ask for clarification on items already clearly defined
   - Do NOT seek permission for implementation details covered in approved feature
   - Only ask questions when genuinely ambiguous or blocking

### For Sub-Agents (Implementation/Verification)

**CRITICAL REMINDERS**:

1. **Load Your Role-Specific Rules**:
   - **Implementation agents**: Load rules from `files_required.implementation_agent.rules` in frontmatter above
   - **Verification agents**: Load rules from `files_required.verification_agent.rules` in frontmatter above
   - Load appropriate stack files specified in files_required

2. **Read Required Context**:
   - **MUST READ** parent specification's `../requirements.md`
   - **MUST READ** this `feature.md` file for complete feature context
   - **MUST VERIFY** dependent features (in depends_on) are complete
   - **MUST READ** any templates in `./templates/` directory
   - **MUST READ** `../fundamentals/*` documentation if parent spec has_fundamentals: true

3. **Autonomous Execution**:
   - Execute your assigned tasks without seeking unnecessary approval
   - This feature is pre-approved - implement as specified
   - Make technical decisions within scope of your role and expertise
   - Follow existing patterns in codebase and use types from dependent features

4. **Status Verification**:
   - Before starting, verify current state of assigned tasks in this feature
   - Check if work is partially complete or already done
   - Review recent commits and code changes related to your tasks
   - Check dependency status before beginning work

5. **Complete Your Scope**:
   - Focus ONLY on tasks assigned to you in this feature
   - Do NOT expand scope without explicit instruction
   - Update Tasks section and frontmatter counts (completed/uncompleted/total/completion_percentage) as you progress
   - Mark tasks complete only when fully implemented and verified
   - Commit after task completion + verification pass (Rule 04)

### Implementation Guidelines
- Follow existing patterns in codebase
- Use types from dependent features
- Update Tasks section and frontmatter counts as work progresses
- Follow TDD: Write tests FIRST, verify they fail, then implement
- Self-review before reporting completion
- Document learnings in ../LEARNINGS.md

---

*Created: YYYY-MM-DD*
*Last Updated: YYYY-MM-DD*
