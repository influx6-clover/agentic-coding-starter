---
# Identification
spec_name: "[NN-spec-name]"  # e.g., "02-build-http-client" - MUST match directory name
spec_number: NN  # Two-digit number (e.g., 02, 15)
description: Brief one-sentence description

# Location Context
# How to find: Run `bash pwd` to get CWD, this file is at CWD/specifications/[NN-spec-name]/requirements.md
# Workspace root is CWD and contains: .agents/, specifications/, documentation/, backends/
workspace_name: "ewe_platform"
spec_directory: "specifications/[NN-spec-name]"
this_file: "specifications/[NN-spec-name]/requirements.md"

# Status
status: in-progress
priority: medium
created: YYYY-MM-DD
author: Main Agent

# Context Optimization
machine_optimized: true
machine_prompt_file: ./machine_prompt.md
context_optimization: true
compact_context_file: ./COMPACT_CONTEXT.md
context_reload_required: true

# Metadata
metadata:
  version: "1.0"
  last_updated: YYYY-MM-DD
  estimated_effort: "medium"
  tags:
    - tag1
    - tag2
  stack_files:
    - .agents/stacks/[language].md
  skills: []
  tools:
    - [Tool names]

# Dependencies
builds_on: []
related_specs: []

# Structure
has_features: true  # DEFAULT: true unless spec is very simple (1-3 trivial tasks)
has_fundamentals: true  # DEFAULT: true unless user explicitly says no

# Progress Tracking (choose ONE based on has_features)
features:  # If has_features: true
  completed: 0
  uncompleted: [N]
  total: [N]
  completion_percentage: 0
tasks:  # If has_features: false
  completed: 0
  uncompleted: [N]
  total: [N]
  completion_percentage: 0

# Files Required by Agents
files_required:
  main_agent:
    rules:
      - .agents/rules/01-rule-naming-and-structure.md
      - .agents/rules/02-rules-directory-policy.md
      - .agents/rules/03-dangerous-operations-safety.md
      - .agents/rules/04-work-commit-and-push-rules.md
      - .agents/rules/05-coding-practice-agent-orchestration.md
      - .agents/rules/06-specifications-and-requirements.md
    files:
      - ./requirements.md
      - ./LEARNINGS.md (if exists)
      - ./PROGRESS.md (if exists)

  verification_agent:
    rules:
      - .agents/rules/01-rule-naming-and-structure.md
      - .agents/rules/02-rules-directory-policy.md
      - .agents/rules/03-dangerous-operations-safety.md
      - .agents/rules/04-work-commit-and-push-rules.md
      - .agents/rules/08-verification-workflow-complete-guide.md
      - [stack_file from metadata.stack_files]
    files:
      - ./requirements.md

  # STRUCTURE DIFFERS BASED ON has_features:
  # - If has_features: false → include implementation_agent section (agents read requirements.md)
  # - If has_features: true → NO implementation_agent section (agents read feature.md files)
  #
  # Example for has_features: false only:
  # implementation_agent:
  #   rules:
  #     - .agents/rules/01-rule-naming-and-structure.md
  #     - .agents/rules/02-rules-directory-policy.md
  #     - .agents/rules/03-dangerous-operations-safety.md
  #     - .agents/rules/04-work-commit-and-push-rules.md
  #     - .agents/rules/13-implementation-agent-guide.md
  #     - .agents/rules/11-skills-usage.md
  #     - [stack_file from metadata.stack_files]
  #   files:
  #     - ./requirements.md
  #     - ./fundamentals/* (if has_fundamentals: true)
---

# [Specification Name] - Requirements

## 📍 Location Reference

**How to find your location**:
1. Run `bash pwd` to get current working directory (CWD)
2. This file is at: `CWD/specifications/[NN-spec-name]/requirements.md`
3. Workspace root is CWD (contains `.agents/`, `specifications/`, `documentation/`, `backends/`)

**Quick paths** (all relative to workspace root = CWD):
- This specification: `specifications/[NN-spec-name]/`
- This file: `specifications/[NN-spec-name]/requirements.md`
- Features: `specifications/[NN-spec-name]/features/*/feature.md`
- Machine prompt: `specifications/[NN-spec-name]/machine_prompt.md`
- Progress: `specifications/[NN-spec-name]/PROGRESS.md`
- Learnings: `specifications/[NN-spec-name]/LEARNINGS.md`
- Agent rules: `.agents/rules/`
- Stack files: `.agents/stacks/`
- Documentation: `documentation/*/doc.md`

**Verification**: If you can read `.agents/AGENTS.md` from CWD, you're in the right place!

**Quick Navigation Commands**:
```bash
# Verify you're in workspace root
test -f .agents/AGENTS.md && echo "✓ In workspace root" || echo "✗ Wrong location"

# List all specifications
ls -d specifications/*/

# Check this spec's features (if has_features: true)
ls -d specifications/[NN-spec-name]/features/*/

# View specification structure
tree -L 2 specifications/[NN-spec-name]/

# Find related code (adjust pattern to your spec)
find backends/ -name "*[relevant-pattern]*" -type f
```

---

> **Specification Structure**:
> - **has_features: false** → This file contains COMPLETE requirements with detailed tasks
> - **has_features: true** → This file is HIGH-LEVEL OVERVIEW ONLY. Detailed requirements are in `features/*/feature.md`

---

## 🔍 CRITICAL: Retrieval-Led Reasoning Required

**ALL agents implementing this specification MUST use retrieval-led reasoning.**

### Before Starting Implementation

**YOU MUST** (in this order):
1. ✅ **Search the codebase** for similar implementations using Grep/Glob
2. ✅ **Read existing code** to understand project patterns and conventions
3. ✅ **Check stack files** (`.agents/stacks/[language].md`) for language-specific patterns
4. ✅ **Read module documentation** for modules you'll modify
5. ✅ **Follow discovered patterns** - do NOT invent new patterns without justification
6. ✅ **Verify all assumptions** by reading actual code

### FORBIDDEN Approaches

**YOU MUST NOT**:
- ❌ Assume typical patterns without checking the codebase
- ❌ Implement without searching for similar code first
- ❌ Apply generic best practices without verifying project conventions
- ❌ Guess file structures, naming conventions, or API patterns
- ❌ Use pretraining knowledge without verification against project code

### Retrieval Examples

**Good Retrieval Approach** ✅:
```
"Let me search for existing API endpoints to understand the pattern..."
→ Uses Grep to find similar endpoints
→ Reads actual implementation files
→ Follows discovered patterns (e.g., Axum with custom middleware)
→ Implements consistently with existing code
```

**Bad Pretraining Approach** ❌:
```
"I'll create an API endpoint using Express middleware (standard approach)"
→ Assumes Express without checking project
→ Doesn't verify actual framework used
→ Creates inconsistent code
```

### Enforcement

- Agents will be asked to demonstrate retrieval steps
- Implementation that doesn't match project patterns will be rejected
- "I assumed..." is NOT acceptable - only "I found..." backed by code references

---

## 🚀 CRITICAL: Token and Context Optimization

**ALL agents implementing this specification MUST follow token and context optimization protocols.**

### Machine-Optimized Prompts (Rule 14)

**Main Agent MUST**:
1. Generate `machine_prompt.md` from this file (requirements.md) when specification finalized
2. Use pipe-delimited compression (58% token reduction)
3. Commit machine_prompt.md alongside requirements.md
4. Regenerate when requirements.md updates
5. Provide machine_prompt.md path to sub-agents (NOT requirements.md)

**Sub-Agents MUST**:
- Read `machine_prompt.md` (NOT this verbose requirements.md file)
- 58% token savings: 2000→900 tokens typical
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
- Regenerate COMPACT_CONTEXT.md
- Clear and reload
- Maintain minimal context throughout work

**See**:
- Rule 14: Machine-Optimized Prompts (.agents/rules/14-machine-optimized-prompts.md)
- Rule 15: Instruction Compaction (.agents/rules/15-instruction-compaction.md)
- Templates: COMPACT_CONTEXT-template.md for format

---

## IF has_features: false (SIMPLE SPECS - Rare)

**Use this structure ONLY for trivial specs (1-3 simple tasks)**

### Overview

[Brief summary - 1-2 paragraphs]

### Requirements Conversation Summary

#### User's Initial Request
[What user asked for]

#### Clarifying Questions Asked
1. Question → Answer
2. Question → Answer

#### Final Requirements Agreement
[What was agreed]

### Detailed Requirements

#### Functional Requirements
1. Requirement 1
2. Requirement 2

#### Technical Specifications
- **Stack**: [Technologies]
- **Dependencies**: [Libraries]
- **Location**: [Code location]

### Tasks

> Update tasks after completion + verification. Commit after each task completion (Rule 04).

#### Implementation Tasks
- [ ] Task 1: Description
- [ ] Task 2: Description

#### Testing Tasks
- [ ] Unit tests for [component]
- [ ] Integration tests

#### Verification Tasks
- [ ] All tests pass
- [ ] Linter: 0 warnings
- [ ] Formatter: clean

### Success Criteria
- [ ] All tasks complete
- [ ] All tests passing
- [ ] Code quality checks pass
- [ ] Automated verification scripts pass (`make verify`)

### Automated Verification (MANDATORY IF APPLICABLE)

**Main Agent: Ask user during spec creation:**
> "Can any requirements be verified programmatically (file existence, function signatures, API endpoints)? Should I create automated verification scripts?"

If YES or requirements are clearly automatable:

Create `scripts/` directory with:
- `verify_requirements.py` - Checks requirements met
- `verify_completion.py` - Verifies code completion
- `validate_features.py` - Validates features

Create `Makefile` with targets:
```makefile
verify: verify-requirements verify-completion verify-features
verify-requirements:
	python3 scripts/verify_requirements.py
# ... more targets
```

**Benefits**: Executable validation > text-based checking. Reduces agent cognitive load.

See Rule 06: Automated Verification Scripts for complete guidelines.

### Module Documentation References
- **Module**: `documentation/[module]/doc.md`

---

## IF has_features: true (FEATURE-BASED SPECS - DEFAULT)

**Use this structure for all non-trivial work**

### Overview

[Brief summary of specification purpose - 2-3 paragraphs maximum]

**Key Approach**: [High-level technical approach]

### Known Issues/Limitations (if any)

#### [Issue Name] (OUT OF SCOPE / IN SCOPE)
- **Issue**: [Description]
- **Root Cause**: [Cause]
- **Impact**: [What this affects]
- **Scope**: [OUT OF SCOPE / IN SCOPE]
- **Decision**: [How handled]

### Requirements Conversation Summary

#### User's Initial Request
[What user asked for]

#### Clarifying Questions Asked
1. Question → Answer
2. Question → Answer
3. Question → Answer

#### Final Requirements Agreement
[Clear statement of agreed requirements]

### Feature Index

**Purpose**: Directory of features with dependencies. Load specific feature.md as needed.

| # | Feature | Description | Dependencies | Status |
|---|---------|-------------|--------------|--------|
| 0 | [name](./features/00-name/feature.md) | [Brief description] | None | ⬜ Pending |
| 1 | [name](./features/01-name/feature.md) | [Brief description] | 0 | ⬜ Pending |
| 2 | [name](./features/02-name/feature.md) | [Brief description] | 1 | ⬜ Pending |

**Status Key**: ⬜ Pending | 🔄 In Progress | ✅ Complete

**Notes**:
- Features implemented in dependency order
- Each feature.md contains detailed requirements, tasks, verification
- Update status in this table as features complete

### Success Criteria (Spec-Wide)

**All Features Complete**:
- [ ] All features in index marked complete (✅)
- [ ] Inter-feature integration tests passing
- [ ] Cross-feature functionality verified

**Spec-Wide Quality**:
- [ ] All features pass linter (zero warnings)
- [ ] All features pass tests
- [ ] Consistent code quality across features

**Documentation**:
- [ ] LEARNINGS.md created
- [ ] REPORT.md created at completion
- [ ] VERIFICATION.md created with signoff
- [ ] fundamentals/ directory created (if has_fundamentals: true)
- [ ] fundamentals/00-overview.md covers usage, patterns, examples

**Automated Verification**:
- [ ] scripts/ directory created with verification scripts (if applicable)
- [ ] Makefile created with `make verify` target
- [ ] All automated verification scripts pass

### Automated Verification (MANDATORY IF APPLICABLE)

**Main Agent: Ask user during spec creation:**
> "Can any requirements be verified programmatically (file existence, function signatures, API endpoints, feature integration)? Should I create automated verification scripts?"

If YES or requirements are clearly automatable:

Create `scripts/` directory with:
- `verify_requirements.py` - Checks spec-wide requirements met
- `verify_features.py` - Verifies all features complete
- `validate_integration.py` - Validates feature integration

Create `Makefile` with targets:
```makefile
verify: verify-requirements verify-features validate-integration
verify-requirements:
	python3 scripts/verify_requirements.py
verify-features:
	python3 scripts/verify_features.py
validate-integration:
	python3 scripts/validate_integration.py
```

**Benefits**: Executable validation > text-based checking. Reduces agent cognitive load. Enables regression testing.

See Rule 06: Automated Verification Scripts for complete guidelines.

### Module Documentation References

Implementation agents MUST read before changes:
- **Module**: `documentation/[module]/doc.md`

---

## Pre-Work Review (MANDATORY)

**CRITICAL**: Main Agent MUST spawn Review Agent before ANY feature work begins.

### When Review Required

Review Agent MUST be spawned:
- ✅ Before starting ANY feature (even if documentation says previous features complete)
- ✅ When resuming work after pause/break
- ✅ When switching between features
- ✅ At start of each work session

### Review Agent Responsibilities

Review Agent MUST:
1. ✅ Read specification thoroughly (requirements.md, features/*/feature.md)
2. ✅ Analyze current codebase state (actual code, not just documentation)
3. ✅ Compare reality vs documentation:
   - Verify completed features are ACTUALLY complete (code exists, tests pass)
   - Check if claimed tasks are really done
   - Validate dependency chains
4. ✅ Verify accuracy of:
   - PROGRESS.md status claims
   - Feature.md task checkboxes
   - requirements.md feature completion counts
5. ✅ Assess readiness for next work:
   - Dependencies truly complete?
   - Code quality acceptable?
   - Tests actually passing?
   - Any blockers or issues?

### Review Agent Assessment

Review Agent returns one of:
- **GO**: Ready to proceed with [specific feature] - all dependencies verified complete
- **STOP**: Issues found - list specific problems that must be fixed first
- **CLARIFY**: Need user input - specify what needs clarification

### Main Agent Response to Review

Based on Review Agent assessment:
- **GO**: Proceed with implementation of specified feature
- **STOP**: Fix issues before proceeding, may need to re-verify previous work
- **CLARIFY**: Ask user for needed clarifications

**Why This Matters**:
- Documentation can be inaccurate (tasks marked done but not actually complete)
- Previous agents may have made mistakes
- Code may not match claimed completion status
- Dependencies might not actually work
- Prevents wasted implementation effort on wrong assumptions
- **USER EXPECTS thorough review before starting work**

---

> **INSTRUCTION FOR SPECIFICATION AGENT**:
>
> Copy the content from ONE of these files below based on `has_features` value:
> - **If has_features: true** → Copy content from `.agents/templates/examples/agent-instructions-with-features.md`
> - **If has_features: false** → Copy content from `.agents/templates/examples/agent-instructions-without-features.md`
>
> Paste the content here, then delete this instruction block.

---

_Created: YYYY-MM-DD_
_Last Updated: YYYY-MM-DD_
