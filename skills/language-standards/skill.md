---
name: "Language Standards"
description: "How to read and follow language-specific standards from language skills with learning log management"
approved: Yes
created: 2026-02-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "2.0"
  last_updated: "2026-02-27"
  tags: [language, standards, conventions, learning-log, skills]
tools: []
files: []
---

# Language Standards

## Overview

Complete guide for reading and following language-specific coding standards from language skills, including how to document learnings when mistakes occur or patterns discovered.

**Usage Type**: EDUCATIONAL - Learn how to use language skills and maintain standards.

## When to Use

- Before writing ANY code in a language
- When discovering language-specific patterns
- When making mistakes that should be documented
- When updating coding standards

## Language-Specific Skills Location

```
.agents/skills/
├── rust-clean-code/              # Rust standards and conventions
│   ├── skill.md                  # Main Rust standards
│   ├── implementation/           # Implementation patterns
│   ├── testing/                  # Testing practices
│   └── async/                    # Async patterns
├── python-clean-code/            # Python standards and conventions
│   ├── skill.md                  # Main Python standards
│   ├── implementation/           # Implementation patterns
│   ├── testing/                  # Testing practices
│   └── django/                   # Django-specific
├── python-testing-excellence/    # Python testing best practices
├── python-with-async-code/       # Python async patterns
└── dst-tokio-rust/               # Tokio/async Rust patterns
```

## Language Skill Contents

Each language skill contains:

1. **Language Overview**: Version requirements, use cases
2. **Coding Standards**: Formatting, naming, organization, documentation
3. **Best Practices**: Idiomatic patterns, error handling, testing, performance, security
4. **Valid Code Requirements**: Quality checks, coverage, documentation
5. **Common Pitfalls**: Mistakes to avoid, anti-patterns
6. **Tools and Configuration**: Required tools, configs, build system
7. **Examples**: Good/bad code examples, common patterns

## For Implementation Agents

### Before Writing ANY Code

**MANDATORY:**
1. Read `.agents/skills/[language]-clean-code/skill.md` for each language being used
2. Understand ALL coding standards and requirements
3. Internalize best practices and anti-patterns
4. Note tools and configurations required

**Language-Specific Skills:**
- **Rust**: `.agents/skills/rust-clean-code/skill.md`
- **Python**: `.agents/skills/python-clean-code/skill.md`
- **JavaScript/TypeScript**: (refer to general standards)

### Follow Standards Strictly

**ZERO TOLERANCE for deviations:**
- Code MUST conform to all requirements in language skills
- If unsure about standard, stop and ask for clarification
- Never "improvise" or "use own judgment" against documented standards

### Verify Compliance

Before reporting completion:
- Run all required linters and formatters
- Ensure all tests pass
- Verify documentation is complete
- Check naming conventions

## For Specification Agents

### Add Language Stack Section

When creating requirements.md:

```markdown
## Language Stack

This specification will be implemented using:

- **Rust**: Backend API implementation
  - Version: 1.75+
  - Purpose: High-performance, type-safe backend
  - See: `.agents/skills/rust-clean-code/skill.md`

- **Python**: Backend services
  - Version: 3.11+
  - Purpose: Data processing and APIs
  - See: `.agents/skills/python-clean-code/skill.md`
```

### Reference Stack Standards

- Include clear references to language skills
- Mention agents MUST read before implementation
- Note deviations not allowed

## Learning Log Management

### When to Update

Update Learning Log section when:

1. **Mistakes Are Made**
   - Document what mistake was
   - Explain why it was wrong
   - Show correct approach
   - Add date and context

2. **New Patterns Discovered**
   - Document new pattern
   - Explain when to use it
   - Provide examples
   - Note benefits

3. **Standards Evolve**
   - Document changes to standards
   - Explain reasoning
   - Update examples
   - Mark outdated patterns deprecated

4. **Tool Configuration Changes**
   - Document tool updates
   - Explain why needed
   - Update setup instructions
   - Note compatibility

### Learning Log Format

```markdown
## Learning Log

### 2026-01-11: Error Handling Pattern Update
**Issue**: Previously used `unwrap()` extensively in Rust, causing panics
**Learning**: Always use proper error handling with `Result<T, E>` and `?` operator
**Corrective Action**: Updated all unwrap() calls. Added linter rule.
**New Standard**: Never use `unwrap()` or `expect()` in production code

### 2026-01-10: TypeScript Type Safety Improvement
**Issue**: Found several `any` types, reducing type safety
**Learning**: TypeScript's value comes from strong typing. Using `any` defeats purpose
**Corrective Action**: Replaced all `any` with proper types. Enabled strict mode
**New Standard**: `any` type is forbidden. Use `unknown` when type truly unknown
```

### Update Process

1. Implementation agent discovers learning
2. Reports to Main Agent with insight
3. Main Agent updates language skill Learning Log (if applicable)
4. Commit with clear message
5. All future implementations benefit from learning

## Stack File Self-Improvement

Language skills evolve over time:

1. **Initial State**: Basic standards and common patterns
2. **After Mistakes**: Learning Log updated with corrections
3. **After Discovery**: New patterns added to examples
4. **After Tool Updates**: Configuration updated
5. **After Standards Change**: Best practices refined

**Result**: Language skills become comprehensive guides refined by actual project experience.

## Language-Specific Examples

### Rust Standards

**Common Requirements:**
- Use `Result<T, E>` for error handling (never `unwrap()` in production)
- Run `cargo fmt -- --check` before commit
- Run `cargo clippy -- -D warnings` (zero warnings)
- All public items must have documentation
- Use `#[test]` for unit tests
- Prefer explicit types over inference for public APIs

### JavaScript/TypeScript Standards

**Common Requirements:**
- Run `prettier --check .` before commit
- Run `eslint . --max-warnings 0` (zero warnings)
- TypeScript strict mode enabled
- No `any` types (use `unknown` and narrow)
- All exports must have JSDoc comments
- Use `test()` or `describe/it` for tests

### Python Standards

**Common Requirements:**
- Run `black --check .` before commit
- Run `ruff check .` (zero errors)
- Run `mypy .` in strict mode
- No mutable default arguments
- All public functions have docstrings
- Use `pytest` for tests with descriptive names

## Enforcement

### Zero Tolerance Policy

**FORBIDDEN:**
- Writing code without reading language skills
- Deviating from documented standards without approval
- Ignoring coding conventions
- Not updating Learning Log when mistakes made
- Creating specs without documenting language stack
- Using languages not documented in requirements

### Violation Consequences

Any agent violating:
1. Code rejected immediately
2. Required to read stack standards
3. Rewrite code to comply
4. Document violation in Learning Log
5. Report violation to user

### Mandatory Checks (Before ANY Commit)

1. **Standards Read**: Agent confirms reading language skills
2. **Code Format**: Pass formatter (rustfmt, prettier, black)
3. **Linter**: Pass linter with zero warnings
4. **Type Check**: Pass type checker if supported
5. **Tests**: All tests pass
6. **Documentation**: Required docs present
7. **Standards Compliance**: Check against stack standards

**If any check fails, code CANNOT be committed.**

## Common Patterns

### Pattern: Starting Rust Implementation

```
1. Read requirements.md → See "Language Stack: Rust"
2. IMMEDIATELY read .agents/skills/rust-clean-code/skill.md (MANDATORY)
3. Study coding standards:
   - Use Result<T, E> for errors
   - Run rustfmt, clippy
   - No unwrap() in production
   - Write unit tests for all functions
4. Implement code following ALL standards
5. Run: cargo fmt, cargo clippy, cargo test
6. All checks pass
7. Commit code
8. Discover better error pattern → Report to Main Agent
9. Main Agent updates rust.md Learning Log
```

### Pattern: Updating Stack File

```
1. Implementation agent makes mistake (e.g., used unwrap())
2. Verification catches issue
3. Agent fixes issue
4. Agent reports to Main Agent: "Discovered: unwrap() causes panics, use Result<T,E>"
5. Main Agent updates .agents/skills/rust-clean-code/skill.md (if needed)
   - Date: 2026-02-27
   - Issue: Used unwrap()
   - Learning: Always use Result
   - New Standard: Never unwrap() in production
6. Commit skill file update (if applicable)
7. All future implementations benefit
```

## Summary

**Before Coding:**
1. Identify languages from requirements.md
2. Read `.agents/skills/[language]-clean-code/skill.md` for EACH language
3. Understand ALL standards
4. Note tools required

**During Coding:**
1. Follow standards strictly (ZERO TOLERANCE for deviations)
2. Run all required checks
3. Document learnings discovered

**After Coding:**
1. Verify compliance with ALL checks
2. Report learnings to Main Agent
3. Main Agent updates Learning Log

**Key Principles:**
- Read stack files BEFORE writing code (MANDATORY)
- ZERO TOLERANCE for standard deviations
- Update Learning Log when learning occurs
- All checks must pass before commit
- Stack files are living documents (improve them)
- Language stack documented in requirements.md

---

_Version: 1.0 - Last Updated: 2026-02-27_
