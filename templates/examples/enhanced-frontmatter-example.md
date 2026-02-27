# Enhanced Frontmatter for requirements.md

This example shows the mandatory frontmatter fields added in skills migration guideline v6.0 for self-contained specifications.

## Purpose

Moving stack_files and skills from body to frontmatter makes specifications machine-readable and self-documenting, allowing automated tooling to understand dependencies and requirements.

## Complete Frontmatter Example

```yaml
---
description: Build a high-performance HTTP client with async/await support
status: in-progress
priority: high
created: 2026-01-15
author: Main Agent
metadata:
  version: "1.0"
  last_updated: 2026-01-22
  estimated_effort: large
  tags:
    - http
    - networking
    - async
  stack_files:
    - .agents/skills/rust-clean-code/skill.md
  skills: []
has_features: false
has_fundamentals: true
builds_on: []
related_specs:
  - 03-dns-resolution
---
```

## New Fields Explained

### `metadata.stack_files` (REQUIRED)
- **Type**: Array of strings
- **Purpose**: Specifies which language language skills agents should load
- **Format**: Relative path from project root
- **Example**: `.agents/skills/rust-clean-code/skill.md`
- **If multiple languages**: List all (e.g., `[".agents/skills/rust-clean-code/skill.md", "language skill"]`)
- **If no code**: Empty array `[]`

### `metadata.skills` (REQUIRED)
- **Type**: Array of strings
- **Purpose**: Lists skill names from `.agents/skills/` that agents should use
- **Format**: Skill name only (e.g., `skill-name`)
- **Example**: `["git-workflow", "docker-deploy"]`
- **If no skills**: Empty array `[]`

### `has_features` (REQUIRED)
- **Type**: Boolean
- **Purpose**: Indicates if specification uses feature-based structure
- **Values**:
  - `true`: Specification has `features/` directory with multiple feature.md files
  - `false`: Simple specification with single requirements.md
- **When true**: Main requirements.md and tasks.md are concise overviews
- **When false**: Full details in main requirements.md and tasks.md

### `has_fundamentals` (REQUIRED)
- **Type**: Boolean
- **Purpose**: Indicates if user-facing fundamentals documentation is required
- **Values**:
  - `true`: Must create `fundamentals/` directory with user guides BEFORE implementation
  - `false`: Internal implementation only, no user-facing docs needed
- **When true**: Implementation agent MUST write fundamentals docs FIRST
- **Criteria**: User-facing libraries, APIs, reusable components, complex patterns

## Migration from Old Format

**BEFORE (body text)**:
```markdown
## Agent Skills Reference

**Language**: Rust → .agents/skills/rust-clean-code/skill.md

**Skills**: None
```

**AFTER (frontmatter)**:
```yaml
metadata:
  stack_files:
    - .agents/skills/rust-clean-code/skill.md
  skills: []
```

## Validation Checklist

Before committing requirements.md, verify:
- ✅ `metadata.stack_files` present (array, not null)
- ✅ `metadata.skills` present (array, not null)
- ✅ `has_features` present (true/false)
- ✅ `has_fundamentals` present (true/false)
- ✅ Language skills paths are correct and files exist
- ✅ Skill names match actual skill files
- ✅ All language skills from `.agents/stacks/`
- ✅ All skills from `.agents/skills/`

## Why This Matters

**Machine-Readable Benefits**:
- Automated tools can parse dependencies
- Scripts can validate stack file references
- Tooling can check if skills exist
- Dashboard can show language distribution
- Analytics can track skill usage

**Self-Containment Benefits**:
- Agents know exactly what to load
- No need to search body for language skills
- Clear declaration of all dependencies
- Frontmatter is single source of truth

---

*Created: 2026-01-22*
*Referenced in: Skills-based self-containment guideline*
