---
this_file: ".agents/templates/examples/README.md"
purpose: "Reference examples for specifications, features, and workflows"
created: 2026-01-22
last_updated: 2026-02-27
---

# Specification Examples

This directory contains reference examples for specifications, features, git workflows, and agent orchestration patterns.

## Available Examples

### 1. Feature-Based Specifications

#### [feature-based-tasks-example.md](./feature-based-tasks-example.md)
Example of how to structure the main `tasks.md` file when using feature-based specifications.
- Shows feature priority order
- Demonstrates task counts and dependencies

#### [feature-frontmatter-examples.md](./feature-frontmatter-examples.md)
Complete frontmatter examples for feature files:
- `feature.md` frontmatter with status, dependencies, effort
- `tasks.md` frontmatter with completion tracking

### 2. Specification Versioning

#### [builds-on-example.md](./builds-on-example.md)
Example showing how to create new specifications that build upon completed specifications.
- When to use `builds_on` field
- Proper frontmatter structure
- Specification versioning principles

### 3. Documentation Requirements

#### [fundamentals-section-example.md](./fundamentals-section-example.md)
Example of "User-Facing Documentation Requirements" section for specifications that need fundamentals documentation.
- When to set `has_fundamentals: true`
- Structure for requirements.md section
- Corresponding tasks.md entries
- Documentation principles

### 4. Git Workflow

#### [git-workflow-examples.md](./git-workflow-examples.md)
Complete examples of proper git commit and push practices:
- Atomic commits during implementation
- Final commit after completion
- Commit message formats
- Safety rules and best practices

### 5. Self-Containment Requirements

#### [cross-reference-links-example.md](./cross-reference-links-example.md)
Example of mandatory cross-reference links for requirements.md:
- Top link after frontmatter (to tasks.md and learnings.md)
- Bottom link at end (to verification.md)
- Why these links matter
- Validation checklist

#### [enhanced-frontmatter-example.md](./enhanced-frontmatter-example.md)
Example of enhanced frontmatter for requirements.md:
- Simplified metadata structure
- `has_features` boolean
- `has_fundamentals` boolean
- Migration from old format
- Validation checklist

### 6. Completion and Verification

#### [completion-verification-section-example.md](./completion-verification-section-example.md)
Complete "MANDATORY Completion and Verification Requirements" section:
- Task completion verification (100% required)
- Code/implementation verification
- Documentation verification
- Quality verification (zero tolerance)
- Specification tracking verification
- Verification issue resolution
- Validation script example

#### [validation-commands-example.md](./validation-commands-example.md)
Exact bash commands for specification completion validation:
- Task validation commands
- File existence checks
- Quality validation (build, test, lint)
- Frontmatter validation
- Documentation quality checks
- Complete validation script
- Common validation failures

### 7. Agent Orchestration

#### [agent-identity-reference.md](./agent-identity-reference.md)
Complete reference for MAIN AGENT vs SUB-AGENT distinction:
- Quick identity check flowchart
- Authority hierarchy and verification spawning rules
- Self-awareness requirements
- Common violations and corrections

#### [workflow-success-example.md](./workflow-success-example.md)
Complete successful workflow from user request to commit:
- Step-by-step breakdown of ideal path
- Agent interactions and authority respect
- Quality gates and success factors
- Time savings from first-attempt pass

#### [workflow-failure-example.md](./workflow-failure-example.md)
Failed verification with fix cycle and recovery:
- Complete workflow with failures and fixes
- Verification failure handling
- Fix cycle process
- Re-verification and commit
- Comparison of with vs without verification

#### [test-documentation-examples.md](./test-documentation-examples.md)
Comprehensive test documentation guide (WHY/WHAT/IMPORTANCE):
- Language-specific examples (Rust, TypeScript, Python, Go, Java, C#)
- Format requirements and validation checklist
- DO and DON'T guidelines
- Quick reference card

### 8. Agent Documentation

#### [agent-frontmatter-reference.md](./agent-frontmatter-reference.md)
Complete frontmatter field reference for agent documentation:
- All required and optional fields with descriptions
- Validation rules and format requirements
- Field-by-field explanations
- Update guidelines and versioning
- Common mistakes and corrections

### 9. Commit Messages

#### [commit-message-templates.md](./commit-message-templates.md)
Comprehensive commit message guide with templates and examples:
- Mandatory format requirements
- Two standard templates (code and non-code)
- 8+ real-world examples (feature, bug fix, refactor, docs, config)
- Language-specific examples (Rust, TypeScript, JavaScript)
- Common mistakes and corrections
- HEREDOC usage guide

## Usage

These examples are referenced throughout agent skills and documentation to:
- ✅ Reduce documentation size
- ✅ Make examples reusable across documentation
- ✅ Allow independent updates to examples
- ✅ Improve searchability and organization
- ✅ Follow DRY (Don't Repeat Yourself) principle
- ✅ Provide copy-paste templates for common needs
- ✅ Consolidate related concepts in single files

## Summary Statistics

**Total Templates/Examples**: 19 files
**Total Lines**: 5,000+ lines
**Coverage**: Specifications, features, git workflows, agent patterns, commit messages

## Maintenance

When updating these examples:
1. Update the specific example file
2. Verify references in related documentation are still accurate
3. Check if related template files need updates
4. Commit with clear message explaining changes

---

*Created: 2026-01-22*
*Updated: 2026-02-27*
*Purpose: Reference examples for specifications and agent workflows*
