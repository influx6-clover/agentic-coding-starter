# Specifications and Requirements Management

## Purpose

Establishes mandatory requirements-gathering and specification-tracking system. All work begins with documented conversation between Main Agent and user, creating clear record of requirements and tasks in `specifications/` directory.

## Core Workflow

### Requirements-First Development

Before any work begins, Main Agent MUST:

1. Engage in conversation with user about requirements
2. Document requirements in specification directory
3. Create integrated task list for tracking
4. Have agents read specifications before starting
5. Verify and update status as work progresses

**No exceptions**: No coding without documented requirements. No implementation until user explicitly approves.

### User Approval Required

After creating specification, Main Agent:

1. Presents specification to user
2. Waits for explicit approval: "Start implementation", "Go ahead", "Proceed with implementation"
3. Never assumes "ok" or "thanks" means approval
4. When in doubt, asks: "Would you like me to begin implementation now?"

### Requirements Conversation (CRITICAL)

Main Agent MUST actively probe requirements using **Socratic method** to help user think deeply.

**Deep Thinking Approach**:
- ✅ **Ask clarifying questions** to expose assumptions
- ✅ **Probe edge cases** user hasn't considered
- ✅ **Challenge vague requirements** with specific scenarios
- ✅ **Help define "success"** concretely
- ✅ **Explore unknowns** and dependencies
- ✅ **Make user think harder** about implications

**Minimum questions**: 3-5 (small), 5-10 (medium), 10+ (large/complex)

**Critical areas**: Scope, technical approach, constraints, success criteria, edge cases, integration, priority, timeline, failure scenarios

**Bad Example**:
```
User: "Add authentication"
Agent: "Ok, I'll create spec"
```

**Good Example**:
```
User: "Add authentication"
Agent: "Let's think through this thoroughly:
  1. What auth method? (JWT, sessions, OAuth?)
  2. Where stored? (DB, Redis, memory?)
  3. Token expiry? What happens on expiry?
  4. Password reset flow? Email verification?
  5. Rate limiting? Account lockout after failed attempts?
  6. What about edge case: user logs in from multiple devices?
  7. Success criteria: What does 'working auth' mean specifically?
  8. Security requirements: HTTPS only? Password strength rules?
  9. Integration: How does this affect existing API endpoints?
  10. What shouldn't we build? (YAGNI principle)

[After discussion, confirms understanding]
Agent: "Let me summarize what success looks like..."
[Creates comprehensive spec]
```

**Encode Everything in Spec**:
- All decisions → requirements.md
- All edge cases → test scenarios
- Success criteria → clear, measurable statements
- Unknowns resolved → documented in spec

**Principle**: Specification quality determines implementation quality. Invest time upfront in deep requirements gathering.

### When User Review/Approval Required

**MANDATORY user review during**:
- ✅ Specification writing (CRITICAL: user must approve specs)
- ✅ Requirements clarification phase
- ✅ Defining success criteria
- ✅ Major architectural decisions

**NO user approval needed for**:
- ❌ Implementation details (follow the spec)
- ❌ Fixing broken tests (fix immediately)
- ❌ Completing incomplete tests (if requirements clear)
- ❌ Standard quality improvements
- ❌ Following established patterns

**Principle**: Get user deeply involved upfront in **what** to build. Then agents autonomously execute **how** to build it per the approved spec.

### Frontmatter Requirements

**Requirements.md MUST include** (see `.agents/templates/requirements-template.md`):

- `description`, `status`, `priority`, `created`, `author`
- `metadata`: version, last_updated, estimated_effort, tags, stack_files, skills, tools
- `has_features`, `has_fundamentals`, `builds_on`, `related_specs`
- **`files_required`**: Complete object for each agent type (MANDATORY, use correct type for requirements file based on this flag)
- `tasks` or `features`: completed, uncompleted, total, completion_percentage

**Feature.md MUST include** (if has_features: true, see `.agents/templates/feature-template.md`):

- `feature`, `description`, `status`, `priority`, `depends_on`, `estimated_effort`, `created`, `last_updated`, `author`
- **`tasks`**: completed, uncompleted, total, completion_percentage (MANDATORY)
- **`files_required`**: implementation_agent and verification_agent entries (MANDATORY)

## Directory Structure

### Simple Specification (has_features: false)

**Use ONLY for trivial specs (1-3 simple tasks)**

```
specifications/01-simple-spec/
├── requirements.md          # Complete requirements with integrated tasks
├── machine_prompt.md        # Machine-optimized (Rule 14 - 58% savings)
├── COMPACT_CONTEXT.md       # Ultra-compact current task (Rule 15 - 97% reduction)
├── scripts/                 # Automated verification/validation scripts (MANDATORY if applicable)
│   ├── verify_requirements.py   # Verifies requirement expectations met
│   ├── verify_completion.py     # Verifies completed code elements
│   └── validate_features.py     # Validates feature implementation
├── Makefile                 # Encodes verification commands (MANDATORY if scripts exist)
├── LEARNINGS.md            # All learnings (permanent)
├── REPORT.md               # All reports (permanent)
├── VERIFICATION.md         # Verification signoff (permanent)
├── PROGRESS.md             # Current status only (ephemeral - delete at 100%)
├── fundamentals/           # User docs (if has_fundamentals: true)
└── templates/              # Code templates (optional)
```

### Feature-Based Specification (has_features: true - DEFAULT)

**Use for all non-trivial work**

```
specifications/02-feature-spec/
├── requirements.md          # High-level overview + feature index ONLY
├── machine_prompt.md        # Machine-optimized (Rule 14 - 58% savings)
├── COMPACT_CONTEXT.md       # Ultra-compact current work (Rule 15 - 97% reduction)
├── scripts/                 # Automated verification/validation scripts (MANDATORY if applicable)
│   ├── verify_requirements.py   # Verifies requirement expectations met
│   ├── verify_features.py       # Verifies all features complete
│   └── validate_integration.py  # Validates feature integration
├── Makefile                 # Encodes verification commands (MANDATORY if scripts exist)
├── features/
│   ├── 00-foundation/
│   │   ├── feature.md       # Detailed feature requirements + tasks
│   │   ├── machine_prompt.md    # Machine-optimized (Rule 14)
│   │   ├── COMPACT_CONTEXT.md   # Ultra-compact current task (Rule 15)
│   │   ├── scripts/        # Feature-specific verification scripts (optional)
│   │   └── templates/      # Feature-specific templates (optional)
│   ├── 01-core-api/
│   │   └── feature.md
│   └── 02-integrations/
│       └── feature.md
├── LEARNINGS.md            # Spec-wide learnings
├── REPORT.md               # Spec-wide completion report
├── VERIFICATION.md         # Spec-wide verification signoff
├── PROGRESS.md             # Current work status (ephemeral)
└── fundamentals/           # User docs (if has_fundamentals: true)
```

### When to Use Features

**DEFAULT: Use features** unless specification is very simple and cannot be broken down further.

**Use `has_features: true` when**:
- Specification involves multiple components or logical groupings
- Work can be split into phases with clear dependencies
- Requirements exceed ~5 tasks
- Context optimization needed for agent efficiency

**Use `has_features: false` ONLY when**:
- Specification is trivial (1-3 simple tasks)
- No logical component boundaries exist
- Breaking into features adds more complexity than value
- User explicitly requests simple structure

**Decision Rule**: When in doubt, default to `has_features: true`. Features provide better organization, clearer dependencies, and improved context management.

## Requirements.md Content Structure

### For Simple Specs (has_features: false)

**requirements.md contains COMPLETE details**:
- Full functional requirements
- Full technical specifications
- Complete task breakdown with all subtasks
- Detailed implementation guidance
- All success criteria
- All verification commands

**Purpose**: Single file contains everything agents need to implement.

### For Feature-Based Specs (has_features: true - DEFAULT)

**requirements.md contains HIGH-LEVEL OVERVIEW ONLY**:

#### What to Include:
- **Overview**: Brief summary of specification purpose
- **Known Issues/Limitations**: Pre-existing blockers or constraints
- **Feature Index**: Table listing all features with descriptions and dependencies
- **Requirements Conversation Summary**: What user asked for and clarifications
- **High-Level Architecture**: Overall approach (not implementation details)
- **Success Criteria**: Spec-wide completion criteria (not feature-specific)
- **Module References**: Links to documentation agents must read

#### What NOT to Include:
- ❌ Detailed functional requirements (goes in feature.md)
- ❌ Detailed technical specifications (goes in feature.md)
- ❌ Individual task breakdowns (goes in feature.md)
- ❌ Implementation details (goes in feature.md)
- ❌ Feature-specific verification commands (goes in feature.md)
- ❌ Code examples or templates (goes in feature.md or templates/)

**Purpose**: Lightweight index that directs agents to relevant features. Agents load specific features as needed, not entire spec.

**Benefit**: Context optimization - agents read overview + specific feature, not all features.

### Naming Convention

Format: `NN-descriptive-name/` (two-digit number prefix, dash separators, lowercase)

**Good**: `01-build-http-client/`, `features/dns-resolution/`
**Bad**: `http-client/` (no number), `1-client/` (single digit), `features/DnsResolution/` (wrong case)

### Specification Immutability

Once completed (status: completed, REPORT.md and VERIFICATION.md created), specification is LOCKED.

**Any new work** → Create NEW specification, reference old one in `builds_on` field

**Exception**: In-progress specifications (no REPORT.md, status not "completed") can be modified

## File Organization

### Allowed Files (Exhaustive List)

Each specification directory MUST contain ONLY these files:

| File                  | Status    | Purpose                                                                              |
| --------------------- | --------- | ------------------------------------------------------------------------------------ |
| `requirements.md`     | Permanent | Requirements with integrated tasks                                                   |
| `machine_prompt.md`   | Generated | Machine-optimized specification (Rule 14 - 58% token savings)                        |
| `COMPACT_CONTEXT.md`  | Generated | Ultra-compact current task context (Rule 15 - 97% context reduction)                 |
| `scripts/`            | Permanent | Automated verification/validation scripts (MANDATORY if applicable)                  |
| `Makefile`            | Permanent | Encodes verification commands (MANDATORY if scripts exist)                           |
| `LEARNINGS.md`        | Permanent | ALL learnings consolidated (technical + process, with efficient writing for context) |
| `REPORT.md`           | Permanent | ALL reports consolidated (work sessions, testing, completion)                        |
| `VERIFICATION.md`     | Permanent | Verification signoff                                                                 |
| `PROGRESS.md`         | Ephemeral | Current status (DELETE at 100%)                                                      |
| `fundamentals/`       | Permanent | User docs (if has_fundamentals: true)                                                |
| `features/`           | Permanent | Feature breakdown (if has_features: true)                                            |
| `templates/`          | Permanent | Code templates (optional)                                                            |

### File Consolidation Rules

**All learnings** → LEARNINGS.md (no separate process/technical learning files)
**All reports** → REPORT.md (no separate WASM/session/testing reports)
**One verification** → VERIFICATION.md (no multiple verification files)

### Forbidden Files

DO NOT create:

- `PROCESS_LEARNINGS.md`, `TECHNICAL_LEARNINGS.md` → Use LEARNINGS.md
- `WASM_TESTING_REPORT.md`, `WORK_SESSION_SUMMARY.md`, `TESTING_REPORT.md` → Add sections to REPORT.md
- `VERIFICATION_SIGNOFF.md`, `VERIFICATION_RESULTS.md` → Use VERIFICATION.md
- `NOTES.md`, `TODO.md`, `STATUS.md` → Use PROGRESS.md during work, delete at completion

### Requirements.md Reminder

Every requirements.md MUST end with:

```markdown
---

## File Organization Reminder

ONLY these files allowed:

1. requirements.md - Requirements with tasks
2. LEARNINGS.md - All learnings
3. REPORT.md - All reports
4. VERIFICATION.md - Verification
5. PROGRESS.md - Current status (delete at 100%)
6. fundamentals/, features/, templates/ (optional)

FORBIDDEN: Separate learning/report/verification files

Consolidation: All learnings → LEARNINGS.md, All reports → REPORT.md

See Rule 06 "File Organization" for complete policy.
```

## Self-Contained Specifications

### files_required Frontmatter

Every requirements.md MUST include `files_required` section listing exact rules and files for each agent type.

**CRITICAL**: Structure differs based on `has_features` value:
- **has_features: false** → Include `implementation_agent` section (agents read requirements.md)
- **has_features: true** → NO `implementation_agent` section (agents read feature.md files per feature's files_required)

**Example for has_features: false**:

```yaml
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
      - ./LEARNINGS.md
      - ./PROGRESS.md

  implementation_agent:
    rules:
      - .agents/rules/01-rule-naming-and-structure.md
      - .agents/rules/02-rules-directory-policy.md
      - .agents/rules/03-dangerous-operations-safety.md
      - .agents/rules/04-work-commit-and-push-rules.md
      - .agents/rules/13-implementation-agent-guide.md
      - [stack_file from metadata.stack_files]
    files:
      - ./requirements.md
      - [feature.md if has_features: true]
      - [fundamentals/* if has_fundamentals: true]

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
```

**Example for has_features: true**:

```yaml
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
      - ./LEARNINGS.md
      - ./PROGRESS.md

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

  # NOTE: No implementation_agent section for feature-based specs
  # Implementation agents load feature.md files directly (each feature has its own files_required)
```

**Dynamic references**:

- `[stack_file from metadata.stack_files]` - Expands to full path from metadata
- `[feature.md if has_features: true]` - Conditional file inclusion (usually complex requirements always have features)
- `[fundamentals/* if has_fundamentals: true]` - Conditional directory inclusion

**Benefits**: Agents know exactly what to load, no guessing

**See**: `.agents/templates/requirements-template.md` for complete structure

## Automated Verification Scripts (MANDATORY IF APPLICABLE)

### Purpose

Shift from text-based verification to **executable, automated validation** using scripts that encode expectations in runnable code. This reduces agent cognitive load, ensures consistency, and enables continuous verification.

### When Scripts Are MANDATORY

Create automated verification scripts when:
- ✅ Requirements can be programmatically validated (file existence, structure, patterns)
- ✅ Code completeness can be checked (functions exist, signatures match, exports present)
- ✅ Feature implementation can be verified (API endpoints work, integration points exist)
- ✅ Validation logic can be encoded (input validation, output formatting, error handling)
- ✅ Completion criteria can be tested (all modules present, all tests exist, coverage met)

Skip scripts when:
- ❌ Requirements are purely subjective (code readability, architecture elegance)
- ❌ Verification requires human judgment
- ❌ Writing script is more complex than manual check

**Default Stance**: If in doubt, CREATE THE SCRIPT. Automation > manual verification.

### Script Location and Structure

#### Specification-Level Scripts

**Location**: `specifications/[NN-spec-name]/scripts/`

**Standard Scripts**:
```
specifications/01-example-spec/
├── scripts/
│   ├── verify_requirements.py    # Verifies requirement expectations met
│   ├── verify_completion.py      # Verifies all code elements complete
│   ├── validate_features.py      # Validates feature implementation
│   ├── check_integration.py      # Checks integration points
│   └── run_all_checks.py         # Runs all verification scripts
└── Makefile                      # Encodes script execution commands
```

#### Feature-Level Scripts (Optional)

**Location**: `specifications/[NN-spec-name]/features/[feature-name]/scripts/`

For complex features that need feature-specific validation beyond spec-wide checks.

#### Project-Level Scripts (If No Specification)

**Location**: `scripts/` at project root

For ad-hoc validation or project-wide checks not tied to a specific specification.

### Script Requirements

#### 1. Python as Default Language

**Prefer Python** unless:
- User explicitly requests another language
- Language-specific validation requires native tooling (e.g., Rust validation using cargo)
- Project is polyglot and Python adds dependency burden

**Why Python**:
- Universal availability
- Easy to read and maintain
- Rich stdlib for file operations, subprocess, JSON/YAML parsing
- Excellent error messages

#### 2. Script Structure

Every verification script MUST:

```python
#!/usr/bin/env python3
"""
verify_requirements.py - Verifies all requirements are met

This script encodes requirement expectations in executable form:
- Checks file existence and structure
- Validates code patterns and signatures
- Verifies integration points
- Tests completion criteria

Exit Codes:
    0: All checks passed
    1: One or more checks failed
    2: Script error (invalid args, missing dependencies)

Usage:
    python3 verify_requirements.py [--verbose] [--fix]
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple

# ANSI colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

class VerificationResult:
    def __init__(self, passed: bool, message: str, details: str = ""):
        self.passed = passed
        self.message = message
        self.details = details

def check_requirement_1() -> VerificationResult:
    """Check that requirement 1 is satisfied."""
    # Actual verification logic
    if condition_met:
        return VerificationResult(True, "Requirement 1: PASS")
    else:
        return VerificationResult(False, "Requirement 1: FAIL", "Details about failure")

def main():
    """Run all verification checks."""
    print(f"{BLUE}Running requirement verification...{RESET}\n")

    checks = [
        ("Requirement 1", check_requirement_1),
        ("Requirement 2", check_requirement_2),
        # ... more checks
    ]

    results = []
    for name, check_fn in checks:
        result = check_fn()
        results.append(result)

        status = f"{GREEN}✓{RESET}" if result.passed else f"{RED}✗{RESET}"
        print(f"{status} {result.message}")
        if result.details:
            print(f"  {YELLOW}{result.details}{RESET}")

    # Summary
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    print(f"\n{passed}/{total} checks passed")

    return 0 if all(r.passed for r in results) else 1

if __name__ == "__main__":
    sys.exit(main())
```

#### 3. Script Capabilities

Scripts SHOULD:
- ✅ Check file existence and structure
- ✅ Verify function/class/module signatures
- ✅ Validate exports and public APIs
- ✅ Test integration points (imports work, services respond)
- ✅ Check code patterns (error handling present, logging configured)
- ✅ Verify test coverage and test existence
- ✅ Validate configuration files
- ✅ Check documentation presence
- ✅ Provide clear, actionable error messages
- ✅ Support `--verbose` flag for detailed output
- ✅ Support `--fix` flag for auto-fixable issues (optional)
- ✅ Exit with 0 on success, 1 on failure, 2 on error

#### 4. Makefile Integration (MANDATORY)

Every specification with scripts/ MUST have a Makefile:

```makefile
# Makefile for specification verification

.PHONY: help verify verify-requirements verify-completion verify-features verify-all clean

help:
	@echo "Specification Verification Commands:"
	@echo "  make verify              - Run all verification checks"
	@echo "  make verify-requirements - Verify requirements met"
	@echo "  make verify-completion   - Verify code completion"
	@echo "  make verify-features     - Verify feature implementation"
	@echo "  make clean               - Clean temporary verification files"

verify: verify-requirements verify-completion verify-features
	@echo "✓ All verification checks passed"

verify-requirements:
	@python3 scripts/verify_requirements.py

verify-completion:
	@python3 scripts/verify_completion.py

verify-features:
	@python3 scripts/validate_features.py

verify-all: verify
	@echo "✓ Comprehensive verification complete"

clean:
	@rm -rf __pycache__
	@find scripts -type d -name __pycache__ -exec rm -rf {} +
```

### Main Agent Responsibilities

When creating specification, Main Agent MUST:

1. **Ask user about automated checks**:
   ```
   "Can any of these requirements be verified programmatically?
    - File/module existence?
    - Function signatures?
    - Integration points?
    - API endpoints?
    - Configuration files?

   Would you like me to create automated verification scripts?"
   ```

2. **Create scripts/ directory** if user approves or if requirements are clearly automatable

3. **Generate verification scripts** that encode:
   - Requirement validation logic
   - Completion criteria checks
   - Feature verification tests
   - Integration point validation

4. **Create Makefile** with appropriate targets

5. **Document scripts in requirements.md**:
   ```markdown
   ## Automated Verification

   This specification includes automated verification scripts:

   - `scripts/verify_requirements.py` - Checks all requirements met
   - `scripts/verify_completion.py` - Verifies code completion
   - `scripts/validate_features.py` - Validates feature implementation

   Run all checks:
   ```bash
   make verify
   ```
   ```

6. **Update scripts as requirements evolve** throughout implementation

### Implementation Agent Responsibilities

After completing work, implementation agent MUST:

1. **Run verification scripts**:
   ```bash
   cd specifications/[NN-spec-name]
   make verify
   ```

2. **Fix failures** before reporting completion

3. **Update scripts** if new requirements discovered during implementation

4. **Report script results** to Main Agent:
   ```
   Task completed:
   - Files changed: [list]
   - Automated verification: make verify - ALL PASSED ✓
   - Script updates: [if any scripts were updated/added]
   ```

### Verification Agent Responsibilities

Verification agent MUST:

1. **Check for scripts/** directory in specification

2. **If scripts exist**:
   - Run `make verify` FIRST (before standard language checks)
   - Treat script failures as verification FAILURE
   - Include script output in verification report

3. **If scripts don't exist**:
   - Note in report: "No automated verification scripts present"
   - Recommend creating scripts if requirements seem automatable

4. **Report format**:
   ```markdown
   ## Automated Verification Scripts

   Status: FOUND / NOT FOUND

   ### Script Execution Results

   ```bash
   $ make verify
   ✓ Verify requirements - PASSED
   ✓ Verify completion - PASSED
   ✓ Verify features - PASSED
   ```

   Exit Code: 0 (success)
   ```

### Script Evolution

Scripts are **living documents** that evolve with specification:

**During Implementation**:
- Update scripts as requirements clarify
- Add new checks for discovered edge cases
- Refine validation logic based on actual code

**After Implementation**:
- Keep scripts for regression testing
- Use for future work building on specification
- Valuable reference for similar specifications

### Benefits of Automated Verification

1. **Consistency**: Same checks run every time, no human error
2. **Speed**: Instant feedback vs. manual text reading
3. **Automation**: Integrate into CI/CD pipelines
4. **Documentation**: Scripts encode expectations in executable form
5. **Regression Prevention**: Rerun scripts to catch regressions
6. **Agent Efficiency**: Less cognitive load reading text, more focus on implementation
7. **Maintenance**: Scripts are easier to update than documentation

### Examples of Scriptable Checks

**File/Module Existence**:
```python
def check_module_exists():
    required_files = [
        "src/http_client.rs",
        "src/dns_resolver.rs",
        "src/connection.rs",
    ]
    missing = [f for f in required_files if not Path(f).exists()]
    if missing:
        return VerificationResult(False, "Missing files", f"Not found: {missing}")
    return VerificationResult(True, "All required files present")
```

**Function Signature Validation**:
```python
def check_function_signatures():
    # Parse source code and check function signatures
    with open("src/http_client.rs") as f:
        content = f.read()

    required_sigs = [
        "pub fn new() -> Self",
        "pub async fn get(&self, url: &str) -> Result<Response>",
    ]

    for sig in required_sigs:
        if sig not in content:
            return VerificationResult(False, f"Missing signature: {sig}")

    return VerificationResult(True, "All function signatures present")
```

**API Endpoint Validation**:
```python
def check_api_endpoints():
    # Test that API endpoints exist and respond
    import subprocess

    # Start server (if needed)
    proc = subprocess.Popen(["cargo", "run", "--bin", "server"])
    time.sleep(2)  # Wait for startup

    try:
        response = requests.get("http://localhost:8080/health")
        if response.status_code == 200:
            return VerificationResult(True, "API endpoint reachable")
        else:
            return VerificationResult(False, f"API returned {response.status_code}")
    finally:
        proc.terminate()
```

### Integration with Existing Rules

**Rule 05 (Verification Workflow)**:
- Verification agents run automated scripts BEFORE standard checks
- Script failures block commit just like test failures

**Rule 08 (Verification Details)**:
- Verification reports include automated script results
- Scripts become part of standard verification checklist

**Rule 04 (Commit Rules)**:
- Commits must pass automated verification scripts
- Script updates committed with implementation changes

## Module Documentation

### Purpose

`documentation/` directory at project root contains detailed module documentation that **MUST be updated AFTER implementation, refactoring, or feature changes**.

### Documentation-After-Implementation Workflow (MANDATORY)

**CRITICAL CHANGE**: Documentation is created/updated **AFTER** successful implementation and verification, NOT before.

**Workflow**:
```
Implement → Verify → Update Documentation → Commit (code + docs together)
```

**Rationale**:
- Implementation reveals actual design decisions and edge cases
- Code is the source of truth; documentation reflects reality
- Prevents documentation-code divergence from speculative design
- Ensures documentation describes what was actually built

### When Documentation Updates Required

Documentation **MUST** be updated after:
- ✅ Implementing new modules or features
- ✅ Refactoring existing modules (significant changes)
- ✅ Updating module specifications or APIs
- ✅ Fixing bugs that change behavior
- ✅ Adding new dependencies or integrations
- ✅ **Performance optimizations** (MANDATORY: document reasoning, benchmarks, trade-offs)

Documentation updates **NOT** required for:
- ❌ Trivial bug fixes (typos, formatting)
- ❌ Internal implementation details (no API changes)
- ❌ Test-only changes

### Performance Optimization Documentation (MANDATORY)

**CRITICAL**: Performance optimizations **MUST** be comprehensively documented with fundamentals, reasoning, and justification.

When implementing performance optimizations, Documentation Agent **MUST** create:

1. **Fundamental Documentation** (`documentation/[module]/fundamentals/performance/[optimization-name].md`):
   - **Problem Statement**: What performance issue was observed
   - **Measurement**: Baseline benchmarks and metrics (with data)
   - **Root Cause**: Why the performance issue existed
   - **Solution Approach**: What optimization technique was applied
   - **Trade-offs**: What was sacrificed (readability, memory, maintainability, etc.)
   - **Alternative Approaches**: What other solutions were considered and why they were rejected
   - **Results**: Post-optimization benchmarks showing improvement
   - **Verification**: How to verify the optimization is still effective

2. **Module Documentation Update** (`documentation/[module]/doc.md`):
   - Add entry to "Performance Characteristics" section
   - Document optimization in "Architecture" section
   - Reference fundamental documentation for details

3. **Code Comments** (in optimized code):
   - WHY the optimization was necessary
   - WHAT trade-off was made
   - HOW to benchmark/verify the optimization
   - Reference to fundamental documentation

**Example Performance Optimization Documentation**:

```markdown
# HTTP Connection Pooling Optimization

## Problem Statement
HTTP client was creating new TCP connections for every request, causing:
- 200ms average latency per request
- TCP handshake overhead on every call
- Resource exhaustion under high load (>1000 req/s)

## Baseline Measurements
- Requests/second: 850 (before)
- Average latency: 200ms (before)
- P99 latency: 450ms (before)
- Memory usage: 120MB baseline

## Root Cause
Default HTTP client configuration created fresh connections without reuse.
TCP handshake (SYN, SYN-ACK, ACK) added ~80ms per request.

## Solution Approach
Implemented connection pooling with:
- Pool size: 50 persistent connections
- Keep-alive: 60 seconds
- Connection reuse across requests

## Trade-offs
✅ Gained: 3x throughput, 75% latency reduction
❌ Sacrificed:
  - Increased memory footprint (+15MB for connection pool)
  - More complex error handling (stale connections)
  - Additional configuration parameters

## Alternative Approaches Considered
1. HTTP/2 multiplexing - rejected (server doesn't support HTTP/2)
2. Larger pool (100 connections) - rejected (diminishing returns, 2x memory cost)
3. Adaptive pooling - rejected (complexity not justified by gains)

## Results
- Requests/second: 2,500 (after) - **3x improvement**
- Average latency: 45ms (after) - **78% reduction**
- P99 latency: 95ms (after) - **79% reduction**
- Memory usage: 135MB - **12% increase**

## Verification
Run benchmark: `cargo bench --bench http_client_pool`
Expected: >2000 req/s with <50ms avg latency
```

**Why Comprehensive Performance Documentation Matters**:
- Future agents understand WHY optimization exists (prevents accidental removal)
- Trade-offs are explicit (helps with future refactoring decisions)
- Benchmarks provide regression detection baseline
- Alternative approaches prevent re-exploring dead ends
- Reasoning captures context that code alone cannot express

**Enforcement**:
- ❌ **USER WILL REJECT** performance optimizations without comprehensive documentation
- ❌ Committing performance changes without benchmarks is FORBIDDEN
- ❌ Optimizations without trade-off analysis will be reverted

### doc.md Structure

**Required frontmatter**: module, language, status, last_updated, maintainer, related_specs

Depending on `has_features=false`:
**Required sections**: Overview, Purpose, Location, Implementation, Public API, Imports, Calls, Workflows, Architecture, Tests, Dependencies, Configuration, Issues, Improvements, Related Docs, Version History

Depending on `has_features=true`:
**Required sections**: Overview, Purpose, Location, Features, Public API, configuration, Architecture, Related Docs.

**Context optimization**: If >8-10KB, agents use Grep/Glob/Read tools instead of loading entire file

### Post-Implementation Documentation Workflow

**After verification passes**, Main Agent **MUST**:

1. ✅ Identify affected modules (which modules were changed)
2. ✅ Check if documentation update required (see criteria above)
3. ✅ If required: Spawn Documentation Agent
4. ✅ Provide Documentation Agent with:
   - Implementation summary
   - Files changed
   - Verification report (PASS status)
   - Specification reference
   - List of modules affected
5. ✅ WAIT for Documentation Agent to complete
6. ✅ Review documentation updates
7. ✅ Commit code AND documentation together
8. ✅ Push to remote

**Documentation Agent responsibilities**:
1. ✅ Read implementation code (actual behavior)
2. ✅ Read existing documentation (if exists)
3. ✅ Update doc.md to reflect new implementation
4. ✅ Update frontmatter (last_updated, version)
5. ✅ Create/update supplementary assets (OpenAPI, schemas, examples, diagrams)
6. ✅ Ensure documentation accuracy (matches code behavior)
7. ✅ Report completion to Main Agent

**Main Agent MUST NOT**:
- ❌ Commit code without updating required documentation
- ❌ Update documentation directly (delegate to Documentation Agent)
- ❌ Skip documentation updates for significant changes

## Verification and Quality

### Progress Tracking

**PROGRESS.md** (Ephemeral):

- Created at for each task you start, cleared after task completion
- Tracks current task and immediate next steps
- Cleared and rewritten after each task is done
- DELETED when specification 100% complete

**LEARNINGS.md** (Permanent):

- Created early, updated throughout
- Cumulative record of all insights
- Never cleared or deleted
- Technical + process learnings consolidated here
- Efficiently written with precision and surgical care to manage context but without loosing information

**REPORT.md** (Permanent):

- Created when nearing completion
- Comprehensive summary of work, testing, metrics
- Can be updated progressively despite name
- Consolidates ALL reports (work sessions, WASM testing, etc.)
- Efficiently written with precision and surgical care to manage context but without loosing information

### Pre-Work Review

Before any agent starts work, spawn Review Agent:

1. Reads specifications thoroughly
2. Analyzes current codebase
3. Compares reality vs documentation
4. Verifies task status accuracy
5. Assesses readiness (GO/STOP/CLARIFY)

**STOP if**: Inconsistencies found, requirements unclear, tasks need refinement, user input required, blockers exist

### Verification Agent

After implementation complete:

1. Main Agent spawns Verification Agent
2. Verification Agent runs all checks (format, lint, tests, build, docs)
3. Creates VERIFICATION.md with results
4. If ALL PASS: Main Agent marks specification complete
5. If ANY FAIL: Fix issues, re-verify

## Spec.md Master Index

Central dashboard at `specifications/Spec.md`:

- List of all specifications with status
- Status dashboard (completed, in-progress, pending counts)
- Organized by completion status
- Links to each specification

**Template**: `.agents/templates/Spec-md-template.md`

## Enforcement

### Violations

**File organization**: Creating forbidden files, not consolidating, keeping PROGRESS.md after 100%

**Task tracking**: Batching updates, not updating after each task, incorrect completion percentages

**Requirements**: Coding without documented requirements, skipping user approval, incomplete frontmatter

**Verification**: Committing without verification, skipping quality checks, missing documentation updates

**Documentation**: Committing module changes without updating documentation, performance optimizations without comprehensive documentation and benchmarks

### Corrective Action

1. Stop immediately
2. Identify violation
3. Fix issue (consolidate files, update tasks, run verification)
4. Report violation for awareness
5. Continue with correct process

## Integration with Other Rules

**Rule 04**: Commit requirements.md updates after changes, include verification status

**Rule 05**: Main Agent spawns Review Agent before work, Verification Agent after work

**Rule 08**: Verification workflow complements continuous verification checkpoints

**Rule 13**: Implementation agents update LEARNINGS.md and requirements.md tasks/features

## Summary

**Core workflow**: Deep requirements gathering (Socratic method) → Document → User approval of spec → **Create Automated Verification Scripts** → Autonomous implementation → **Run Automated Verification** → Verification → **Update Documentation** → Completion

**Requirements Excellence**:
- Use Socratic method to probe deeply
- Challenge assumptions, explore edge cases
- Help user define success concretely
- Encode all decisions, edge cases, unknowns in spec
- Invest time upfront for quality specs

**User Involvement**:
- MANDATORY approval: Specifications, requirements, success criteria
- NO approval needed: Implementation details, fixing tests, following specs

**Automated Verification** (NEW):
- Create scripts/ directory with executable verification scripts (Python default)
- Encode requirements, completion, and feature validation in runnable code
- Makefile targets for easy execution (`make verify`)
- Reduces agent cognitive load (scripts > text reading)
- Scripts evolve with specification, serve as regression tests
- Verification agents run automated scripts BEFORE standard checks

**Documentation Workflow** (NEW):
- Documentation created/updated AFTER implementation and verification
- Code is source of truth, documentation reflects reality
- **Performance optimizations REQUIRE comprehensive documentation**: fundamentals, reasoning, benchmarks, trade-offs
- Commit code and documentation together

**File structure**: requirements.md (with tasks) + scripts/ + Makefile + LEARNINGS.md + REPORT.md + VERIFICATION.md + PROGRESS.md (ephemeral)

**Consolidation**: All learnings in one file, all reports in one file, one verification file

**Quality**: Automated verification scripts, pre-work review, continuous verification, final verification signoff

**Templates**: `.agents/templates/requirements-template.md`, `LEARNINGS-template.md`, `REPORT-template.md`, `VERIFICATION-template.md`

---

_Created: 2026-01-11_
_Last Updated: 2026-02-01 (Added: Automated verification scripts, instruction compaction (COMPACT_CONTEXT.md). Changed: Documentation workflow - now AFTER implementation. Added: Performance optimization documentation requirements.)_
