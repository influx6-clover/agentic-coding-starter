# Specifications and Requirements Management

## Purpose

Establishes mandatory requirements-gathering and specification-tracking system. All work begins with documented conversation between Main Agent and user.

## Core Workflow

### Requirements-First Development

Before any work, Main Agent MUST:
1. Engage in conversation with user about requirements
2. Document requirements in specification directory
3. Create integrated task list for tracking
4. Have agents read specifications before starting
5. Verify and update status as work progresses

**No exceptions**: No coding without documented requirements. No implementation until user explicitly approves.

### User Approval Required

After creating specification:
1. Present specification to user
2. Wait for explicit approval: "Start implementation", "Go ahead", "Proceed"
3. Never assume "ok" or "thanks" means approval
4. When in doubt, ask: "Would you like me to begin implementation now?"

### Requirements Conversation (CRITICAL)

Main Agent MUST actively probe requirements using **Socratic method**.

**Deep Thinking Approach:**
- Ask clarifying questions to expose assumptions
- Probe edge cases user hasn't considered
- Challenge vague requirements with specific scenarios
- Help define "success" concretely
- Explore unknowns and dependencies
- Make user think harder about implications

**Minimum questions**: 3-5 (small), 5-10 (medium), 10+ (large/complex)

**Critical areas**: Scope, technical approach, constraints, success criteria, edge cases, integration, priority, timeline, failure scenarios

**Bad Example:**
```
User: "Add authentication"
Agent: "Ok, I'll create spec"
```

**Good Example:**
```
User: "Add authentication"
Agent: "Let's think through this:
  1. Auth method? (JWT, sessions, OAuth?)
  2. Storage? (DB, Redis, memory?)
  3. Token expiry? What happens on expiry?
  4. Password reset? Email verification?
  5. Rate limiting? Account lockout?
  6. Multiple devices edge case?
  7. Success criteria: What does 'working' mean?
  8. Security: HTTPS only? Password strength?
  9. Integration: Affect existing endpoints?
  10. What shouldn't we build? (YAGNI)

[After discussion]
Agent: "Let me summarize what success looks like..."
```

**Encode Everything in Spec**: All decisions → requirements.md, edge cases → test scenarios, success criteria → measurable statements

### When User Review Required

**MANDATORY user review:**
- ✅ Specification writing (user must approve specs)
- ✅ Requirements clarification
- ✅ Defining success criteria
- ✅ Major architectural decisions

**NO user approval needed:**
- ❌ Implementation details (follow spec)
- ❌ Fixing broken tests (fix immediately)
- ❌ Completing incomplete tests (if requirements clear)
- ❌ Standard quality improvements
- ❌ Following established patterns

**Principle**: User deeply involved in **what** to build. Agents autonomously execute **how** per approved spec.

### Frontmatter Requirements

**requirements.md MUST include** (see `.agents/templates/requirements-template.md`):
- `description`, `status`, `priority`, `created`, `author`
- `metadata`: version, last_updated, estimated_effort, tags, stack_files, skills, tools
- `has_features`, `has_fundamentals`, `builds_on`, `related_specs`
- **`files_required`**: Complete object for each agent type (MANDATORY)
- `tasks` or `features`: completed, uncompleted, total, completion_percentage

**feature.md MUST include** (if has_features: true):
- `feature`, `description`, `status`, `priority`, `depends_on`, `estimated_effort`, `created`, `last_updated`, `author`
- **`tasks`**: completed, uncompleted, total, completion_percentage (MANDATORY)
- **`files_required`**: implementation_agent and verification_agent entries (MANDATORY)

## Directory Structure

### Simple Specification (has_features: false)

**Use ONLY for trivial specs (1-3 simple tasks)**

```
specifications/01-simple-spec/
├── requirements.md          # Complete requirements with tasks
├── machine_prompt.md        # Machine-optimized (Rule 14)
├── COMPACT_CONTEXT.md       # Ultra-compact current task (Rule 15)
├── scripts/                 # Verification scripts (if applicable)
├── Makefile                 # Verification commands (if scripts exist)
├── LEARNINGS.md            # All learnings (permanent)
├── REPORT.md               # All reports (permanent)
├── VERIFICATION.md         # Verification signoff (permanent)
├── PROGRESS.md             # Current status (ephemeral - delete at 100%)
├── fundamentals/           # User docs (if has_fundamentals: true)
└── templates/              # Code templates (optional)
```

### Feature-Based Specification (has_features: true - DEFAULT)

**Use for all non-trivial work**

```
specifications/02-feature-spec/
├── requirements.md          # High-level overview + feature index ONLY
├── machine_prompt.md        # Machine-optimized (Rule 14)
├── COMPACT_CONTEXT.md       # Ultra-compact current work (Rule 15)
├── scripts/                 # Verification scripts (if applicable)
├── Makefile                 # Verification commands (if scripts exist)
├── features/
│   ├── 00-foundation/
│   │   ├── feature.md       # Detailed requirements + tasks
│   │   ├── IMPLEMENTATION_PLAN.md  # Technical plan (for complex features)
│   │   ├── machine_prompt.md    # Machine-optimized
│   │   ├── COMPACT_CONTEXT.md   # Ultra-compact
│   │   ├── scripts/        # Feature verification scripts (optional)
│   │   └── templates/      # Feature templates (optional)
│   ├── 01-core-api/feature.md
│   └── 02-integrations/feature.md
├── LEARNINGS.md            # Spec-wide learnings
├── REPORT.md               # Spec-wide completion report
├── VERIFICATION.md         # Spec-wide verification signoff
├── PROGRESS.md             # Current work status (ephemeral)
└── fundamentals/           # User docs (if has_fundamentals: true)
```

### When to Use Features

**DEFAULT: Use features** unless very simple.

**Use `has_features: true` when:**
- Multiple components or logical groupings
- Work split into phases with clear dependencies
- Requirements exceed ~5 tasks
- Context optimization needed

**Use `has_features: false` ONLY when:**
- Trivial (1-3 simple tasks)
- No logical component boundaries
- Breaking into features adds complexity
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
- Known Issues/Limitations: Pre-existing blockers
- Feature Index: Table with descriptions and dependencies
- Requirements Conversation Summary: What user asked
- High-Level Architecture: Overall approach
- Success Criteria: Spec-wide completion criteria
- Module References: Links to docs

**Do NOT Include:**
- ❌ Detailed functional requirements (→ feature.md)
- ❌ Detailed technical specs (→ feature.md)
- ❌ Individual task breakdowns (→ feature.md)
- ❌ Implementation details (→ feature.md)
- ❌ Feature-specific verification (→ feature.md)
- ❌ Code examples/templates (→ feature.md/templates/)

**Benefit**: Context optimization - agents read overview + specific feature, not all features.

### Naming Convention

Format: `NN-descriptive-name/` (two-digit prefix, dashes, lowercase)

**Good**: `01-build-http-client/`, `features/dns-resolution/`
**Bad**: `http-client/` (no number), `1-client/` (single digit), `features/DnsResolution/` (wrong case)

### Implementation Plans

**Location**: `specifications/[spec]/features/[feature]/IMPLEMENTATION_PLAN.md`

**When to create:**
- Non-trivial feature requiring design decisions
- Complex feature affecting multiple files
- Multiple valid approaches exist
- User requests "create a plan"

**Contents:**
- Technical approach and architecture
- Key framework patterns to use
- Step-by-step implementation tasks
- Success criteria and outcomes
- Trade-offs considered
- Links to relevant docs

**Lifecycle:**
- Created in plan mode (BEFORE implementation)
- Updated if approach changes
- Kept permanently (never delete)
- Referenced in feature.md

**Do NOT:**
- ❌ Create plans in `~/.claude/plans/` (temporary working files)
- ❌ Put implementation details in requirements.md (too high-level)
- ❌ Put plans in feature.md itself (link instead)
- ❌ Delete plans after implementation
- ❌ Create for trivial features

## Specification Immutability

**Completed specifications are IMMUTABLE.**

**Before updating specification:**
1. Read `specifications/NN-spec/requirements.md` frontmatter
2. Check status: is it "completed"?
3. Check for REPORT.md and VERIFICATION.md

**If COMPLETED:**
- ❌ DO NOT update
- ✅ CREATE new specification (use `builds_on` field)

**If IN-PROGRESS:**
- ✅ Can update as normal

## File Lifecycle

### Permanent Files (Never Delete)
- `requirements.md` - Source of truth
- `feature.md` - Feature requirements
- `LEARNINGS.md` - All learnings
- `REPORT.md` - All completion reports
- `VERIFICATION.md` - Verification signoff
- `IMPLEMENTATION_PLAN.md` - Technical plans
- `scripts/` - Verification scripts
- `Makefile` - Verification commands

### Ephemeral Files (Delete When Done)
- `PROGRESS.md` - Delete when spec 100% complete
- `COMPACT_CONTEXT.md` - Delete when task complete (Rule 15)
- `machine_prompt.md` - Generated, can be regenerated

## Enforcement

### Must Do
1. Document requirements before coding
2. Get explicit user approval to start
3. Ask minimum required questions (3-5+ depending on complexity)
4. Use features for non-trivial specs (default)
5. Keep requirements.md high-level if using features
6. Create implementation plans for complex features
7. Never update completed specifications

### Must Not Do
1. Code without documented requirements
2. Assume approval without explicit confirmation
3. Skip Socratic questioning
4. Put detailed requirements in requirements.md when using features
5. Delete permanent files
6. Update completed specifications
7. Create plans in ~/.claude/plans/

### Critical Violations
1. Starting implementation without user approval
2. No requirements conversation
3. Insufficient probing of requirements
4. Detailed requirements in requirements.md with has_features: true
5. Updating completed specifications
6. Deleting permanent documentation

## Summary

**Golden Rules:**
1. **Requirements first** - No coding without documented requirements
2. **User approval required** - Explicit confirmation to start
3. **Socratic method** - Deep requirements probing (3-5+ questions)
4. **Features by default** - Use has_features: true unless trivial
5. **High-level overview** - When using features, requirements.md is index only
6. **Implementation plans** - For complex features, create technical plan
7. **Immutable when complete** - Never update completed specifications

**Workflow:**
```
User Request → Socratic Questions → Requirements.md → User Approval →
Implementation → Verification → Complete
```

---

_Version: 1.0 - Last Updated: 2026-02-27_
