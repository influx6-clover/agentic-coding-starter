# Rules Directory and File Structure Policy

## Purpose
Establishes the canonical location, naming conventions, and structural requirements for all agent rules.

## Rules Directory Location

All agent rules **MUST** be placed in `.agents/rules/` directory.

### Must Do
1. Place all rules in `.agents/rules/` directory
2. Check `.agents/rules/` for all applicable rules

### Must Not Do
1. Place rules in `.claude/` directory
2. Place rules in any other directory location
3. Look for rules outside `.agents/rules/`

## File Naming Format

```
NN-rule-name-describing-the-policy.md
```

### Must Do
1. Use two-digit numerical prefix (01-99) to control load order
2. Use dash (`-`) as word separator
3. Use `.md` extension
4. Use descriptive, lowercase names
5. Place all rules in flat `.agents/rules/` directory (no subdirectories)
6. Create one rule per file

### Must Not Do
1. Use single-digit prefixes (e.g., `1-rule.md`)
2. Use underscores or spaces (e.g., `01_rule.md` or `01 rule.md`)
3. Use camelCase or PascalCase (e.g., `01-ruleNaming.md`)
4. Omit numerical prefix (e.g., `rule-naming.md`)
5. Create subdirectories within `.agents/rules/`
6. Combine multiple rules in one file

### Examples
- **Good**: `01-rules-directory-and-structure.md`, `04-work-commit-and-push-rules.md`
- **Bad**: `rule1.md`, `1-rule-naming.md`, `01_rule_naming.md`, `01 rule.md`

## Template Policy

### Must Do
1. Extract templates to `.agents/templates/` directory
2. Reference templates in rules (e.g., "See `.agents/templates/skill-template.md`")
3. Include brief description and key sections list in rules
4. Keep rules focused on policies, not full template content

### Must Not Do
1. Embed complete templates directly in rule files (>50 lines)
2. Duplicate template content across multiple rules

### Why
- Reduces rule file sizes by 40-50%
- Maintains single source of truth
- Agents load templates only when needed
- Easier to maintain and update

### Templates Directory
Store all templates in `.agents/templates/` including skill templates, requirements templates, documentation templates, etc.

## Directory Structure

```
.agents/
├── rules/
│   ├── 01-rules-directory-and-structure.md
│   ├── 02-dangerous-operations-safety.md
│   ├── 03-work-commit-and-push-rules.md
│   └── [other rules...]
└── templates/
    ├── skill-template.md
    ├── requirements-template.md
    └── [other templates...]
```

## Enforcement

### Naming Violations
1. Rename to follow convention
2. Move to flat structure
3. Split if combining multiple rules

### Directory Violations
1. Move rules to `.agents/rules/`
2. Report any rules found outside `.agents/rules/` as misplaced
3. Remove rules from `.claude/` or other locations

### Template Violations
1. Extract templates (>50 lines) to `.agents/templates/`
2. Update rule to reference template
3. Commit with clear message

---
*Created: 2026-01-11*
*Last Updated: 2026-02-27 (Combined Rule 01 and Rule 02)*
