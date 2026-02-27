---
name: "Specifications Management"
description: "Complete guide for creating, managing, and structuring specifications with requirements and features"
approved: Yes
created: 2026-02-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-27"
  tags: [specifications, requirements, features, management, workflow]
tools: []
files: []
---

# Specifications Management

## Overview

Complete guide for creating and managing specifications including requirements-first development, feature-based structure, and specification lifecycle.

**Usage Type**: EDUCATIONAL - Learn specification management patterns.

## When to Use

- Creating new specifications
- Managing specification lifecycle
- Structuring requirements and features
- Understanding specification versioning

## Core Principles

### Requirements-First Development

Before ANY work:
1. Engage in conversation with user (Socratic method)
2. Document requirements in specification directory
3. Create integrated task list
4. Get explicit user approval
5. Agents read specifications before starting

**No exceptions**: No coding without documented requirements.

### Socratic Requirements Conversation

**Deep Thinking Approach:**
- Ask clarifying questions (expose assumptions)
- Probe edge cases
- Challenge vague requirements
- Help define "success" concretely
- Explore unknowns and dependencies

**Minimum questions**: 3-5 (small), 5-10 (medium), 10+ (large/complex)

**Critical areas**: Scope, technical approach, constraints, success criteria, edge cases, integration, priority, timeline, failure scenarios

**Encode Everything**: All decisions → requirements.md, edge cases → test scenarios, success criteria → measurable statements

## Directory Structure

### Simple Specification (has_features: false)

**Use ONLY for trivial specs (1-3 simple tasks)**

```
specifications/01-simple-spec/
├── requirements.md          # Complete requirements + tasks
├── machine_prompt.md        # Machine-optimized (Rule 14)
├── COMPACT_CONTEXT.md       # Ultra-compact (Rule 15)
├── scripts/                 # Verification scripts
├── Makefile                 # Verification commands
├── LEARNINGS.md            # Permanent learnings
├── REPORT.md               # Permanent reports
├── VERIFICATION.md         # Verification signoff
├── PROGRESS.md             # Current status (ephemeral)
└── templates/              # Code templates (optional)
```

### Feature-Based Specification (has_features: true - DEFAULT)

**Use for all non-trivial work**

```
specifications/02-feature-spec/
├── requirements.md          # High-level overview + feature index ONLY
├── machine_prompt.md        # Machine-optimized
├── COMPACT_CONTEXT.md       # Ultra-compact current work
├── scripts/                 # Spec verification scripts
├── Makefile                 # Verification commands
├── features/
│   ├── 00-foundation/
│   │   ├── feature.md       # Detailed requirements + tasks
│   │   ├── IMPLEMENTATION_PLAN.md  # Technical plan (complex features)
│   │   ├── machine_prompt.md
│   │   ├── COMPACT_CONTEXT.md
│   │   └── scripts/        # Feature-specific scripts
│   ├── 01-core-api/feature.md
│   └── 02-integrations/feature.md
├── LEARNINGS.md            # Spec-wide learnings (permanent)
├── REPORT.md               # Spec-wide report (permanent)
├── VERIFICATION.md         # Spec signoff (permanent)
└── PROGRESS.md             # Current status (ephemeral)
```

### When to Use Features

**DEFAULT: Use features** unless very simple.

**Use `has_features: true` when:**
- Multiple components or logical groupings
- Work split into phases with dependencies
- Requirements exceed ~5 tasks
- Context optimization needed

**Use `has_features: false` ONLY when:**
- Trivial (1-3 simple tasks)
- No logical component boundaries
- User explicitly requests simple structure

**Decision Rule**: When in doubt, default to `has_features: true`.

## Requirements.md Content

### For Simple Specs (has_features: false)

**Contains COMPLETE details:**
- Full functional requirements
- Full technical specifications
- Complete task breakdown
- Detailed implementation guidance
- All success criteria
- All verification commands

### For Feature-Based Specs (has_features: true - DEFAULT)

**Contains HIGH-LEVEL OVERVIEW ONLY:**

**Include:**
- Overview: Brief summary
- Known Issues/Limitations
- Feature Index: Table with descriptions
- Requirements Conversation Summary
- High-Level Architecture
- Success Criteria: Spec-wide only
- Module References

**Do NOT Include:**
- Detailed functional requirements (→ feature.md)
- Detailed technical specs (→ feature.md)
- Individual task breakdowns (→ feature.md)
- Implementation details (→ feature.md)

**Benefit**: Context optimization - agents read overview + specific feature, not all features.

## Frontmatter Requirements

### requirements.md

```yaml
---
description: "Brief description"
status: "in-progress" | "completed"
priority: "high" | "medium" | "low"
created: YYYY-MM-DD
author: "Main Agent"
metadata:
  version: "1.0"
  last_updated: YYYY-MM-DD
  estimated_effort: "small | medium | large"
  tags: [tag1, tag2]
  stack_files: [rust.md, javascript.md]
  skills: [skill1, skill2]
  tools: [Tool1, Tool2]
has_features: true | false
has_fundamentals: true | false
builds_on: "specifications/NN-previous-spec"  # optional
related_specs: ["spec1", "spec2"]  # optional
files_required:
  implementation_agent: [file1, file2]
  verification_agent: [file1, file2]
tasks:  # or features:
  completed: N
  uncompleted: N
  total: N
  completion_percentage: N%
---
```

### feature.md (if has_features: true)

```yaml
---
feature: "Feature Name"
description: "Brief description"
status: "pending" | "in-progress" | "completed"
priority: "high" | "medium" | "low"
depends_on: ["feature-name"]  # optional
estimated_effort: "small | medium | large"
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
author: "Main Agent"
tasks:
  completed: N
  uncompleted: N
  total: N
  completion_percentage: N%
files_required:
  implementation_agent: [file1, file2]
  verification_agent: [file1, file2]
---
```

## Specification Lifecycle

### Creation Phase

1. User requests feature
2. Main Agent conversation with user (Socratic questions)
3. Create specification directory
4. Write requirements.md
5. Get explicit user approval ("Start implementation", "Go ahead", "Proceed")
6. Generate machine_prompt.md (context optimization)

### Implementation Phase

1. Generate COMPACT_CONTEXT.md
2. Spawn implementation agents
3. Agents implement following specifications
4. Update PROGRESS.md as work progresses
5. Verification before commits

### Completion Phase

1. All tasks/features completed
2. Generate REPORT.md (permanent)
3. Generate VERIFICATION.md (permanent)
4. Update status to "completed"
5. Delete PROGRESS.md
6. Specification now IMMUTABLE

## Specification Versioning (CRITICAL)

**Completed specifications are IMMUTABLE.**

**Before updating:**
1. Check status in requirements.md frontmatter
2. If "completed": Create NEW specification (use `builds_on` field)
3. If "in-progress": Can update

**Example:**
```
User: "Add retry logic to HTTP client"
Main Agent checks: specifications/01-build-http-client/requirements.md
Status: completed ✅
Action: Create specifications/04-add-http-client-retry-logic/
Reference: builds_on: "specifications/01-build-http-client"
```

**Why**: Preserves historical record, creates clear lineage, enables audit trail.

## Implementation Plans

**Location**: `specifications/[spec]/features/[feature]/IMPLEMENTATION_PLAN.md`

**When to create:**
- Non-trivial feature requiring design decisions
- Complex feature affecting multiple files
- Multiple valid approaches exist
- User requests "create a plan"

**Contents:**
- Technical approach and architecture
- Key framework patterns
- Step-by-step implementation tasks
- Success criteria
- Trade-offs considered

**Lifecycle:**
- Created in plan mode (BEFORE implementation)
- Updated if approach changes
- Kept permanently (never delete)
- Referenced in feature.md

**Don't:**
- Create in `~/.claude/plans/` (temporary)
- Put in requirements.md (too high-level)
- Delete after implementation

## Naming Convention

**Format**: `NN-descriptive-name/` (two-digit prefix, dashes, lowercase)

**Good**: `01-build-http-client/`, `features/dns-resolution/`
**Bad**: `http-client/` (no number), `1-client/` (single digit), `features/DnsResolution/` (wrong case)

## File Lifecycle

### Permanent Files (Never Delete)
- requirements.md
- feature.md
- LEARNINGS.md
- REPORT.md
- VERIFICATION.md
- IMPLEMENTATION_PLAN.md
- scripts/
- Makefile

### Ephemeral Files (Delete When Done)
- PROGRESS.md (delete when spec 100% complete)
- COMPACT_CONTEXT.md (delete when task complete)
- machine_prompt.md (generated, can regenerate)

## User Approval Requirements

**MANDATORY user review:**
- Specification writing (user must approve specs)
- Requirements clarification
- Defining success criteria
- Major architectural decisions

**NO user approval needed:**
- Implementation details (follow spec)
- Fixing broken tests
- Completing incomplete tests (if clear)
- Standard quality improvements
- Following established patterns

**Principle**: User deeply involved in **what** to build. Agents autonomously execute **how** per approved spec.

## Common Patterns

### Pattern: Simple Specification

```
1. User requests simple task
2. Socratic conversation (3-5 questions)
3. Create specifications/NN-task/requirements.md
4. Include all details in requirements.md
5. Set has_features: false
6. Get user approval
7. Generate machine_prompt.md
8. Implement
```

### Pattern: Feature-Based Specification

```
1. User requests complex feature
2. Socratic conversation (10+ questions)
3. Create specifications/NN-feature/requirements.md (overview only)
4. Create features/00-foundation/feature.md (detailed)
5. Create features/01-core/feature.md
6. Set has_features: true
7. Get user approval
8. Generate machine_prompt.md per feature
9. Implement feature-by-feature
```

### Pattern: Building on Completed Spec

```
1. User requests enhancement to completed spec
2. Check specifications/01-original/requirements.md status
3. Status: completed ✅
4. Create NEW spec: specifications/04-enhancement/
5. Set builds_on: "specifications/01-original"
6. Continue normal workflow
```

## Summary

**Requirements-First:**
1. Socratic conversation (3-5+ questions)
2. Document requirements
3. Get explicit user approval
4. No coding without requirements

**Structure:**
- Simple specs: has_features: false (1-3 tasks only)
- Feature-based: has_features: true (DEFAULT)
- High-level overview in requirements.md
- Detailed requirements in feature.md

**Versioning:**
- Completed specs are IMMUTABLE
- Build on completed specs with new spec
- Use builds_on field to reference

**Lifecycle:**
- Creation → Implementation → Completion
- PROGRESS.md ephemeral (delete at 100%)
- REPORT.md + VERIFICATION.md permanent

**Key Principles:**
1. Requirements-first (no coding without specs)
2. User approval required (explicit confirmation)
3. Features by default (unless trivial)
4. Immutable when complete (create new for changes)
5. Context optimization (machine prompts + compaction)

---

_Version: 1.0 - Last Updated: 2026-02-27_
