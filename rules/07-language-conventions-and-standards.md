# Language Conventions and Standards

## Purpose

Establishes mandatory language-specific coding standards that all agents must follow, ensuring consistency and creating a self-improving system where agents learn from mistakes.

## Stack Standards Location

```
.agents/stacks/
├── javascript.md          # JavaScript/TypeScript standards
├── rust.md                # Rust standards
├── python.md              # Python standards
├── go.md                  # Go standards
└── [language].md          # Additional language standards
```

## Stack Standards File Requirements

Each language stack file MUST contain:

1. **Language Overview**: Version requirements, use cases, when to use
2. **Coding Standards**: Formatting, naming conventions, organization, documentation
3. **Best Practices**: Idiomatic patterns, error handling, testing, performance, security
4. **Valid Code Requirements**: Quality requirements, checks, coverage, documentation
5. **Common Pitfalls**: Mistakes to avoid, anti-patterns, common bugs
6. **Tools and Configuration**: Required tools, configs, build system, dependencies
7. **Examples**: Good/bad code examples, common patterns
8. **Learning Log**: Lessons learned, mistakes corrected, new patterns (date-stamped)

## For Specification Agents

When creating requirements.md, agents MUST:

1. **Add Language Stack Section**:
   ```markdown
   ## Language Stack

   - **Rust**: Backend API implementation
     - Version: 1.75+
     - Purpose: High-performance, type-safe backend logic
     - See: `.agents/stacks/rust.md`

   - **TypeScript**: Frontend UI components
     - Version: 5.0+
     - Purpose: Type-safe React components
     - See: `.agents/stacks/javascript.md`
   ```

2. **Reference Stack Standards**: Include clear references, mention agents MUST read before implementation

3. **Document Language-Specific Requirements**: Constraints, performance requirements, integration needs

## For Implementation Agents

Before writing ANY code, agents MUST:

1. **Read Relevant Stack Standards**:
   - Load `.agents/stacks/[language].md` for each language
   - Understand all coding standards and requirements
   - Internalize best practices and anti-patterns

2. **Follow Standards Strictly**:
   - ZERO TOLERANCE for deviations
   - Code MUST conform to all requirements
   - If unsure, stop and ask for clarification
   - Never improvise against documented standards

3. **Verify Compliance**:
   - Run all required linters and formatters
   - Ensure all tests pass
   - Verify documentation is complete
   - Check naming conventions

4. **Update Stack Standards When Learning**:
   - New best practice → add to stack file
   - Made a mistake → document in Learning Log
   - Found better way → update examples
   - Keep standards current and accurate

## Learning Log Updates

Agents MUST update Learning Log when:

### 1. Mistakes Are Made
- Document the mistake
- Explain why it was wrong
- Show correct approach
- Add date and context

### 2. New Patterns Discovered
- Document the new pattern
- Explain when to use it
- Provide examples
- Note benefits

### 3. Standards Evolve
- Document changes
- Explain reasoning
- Update examples
- Mark deprecated patterns

### 4. Tool Configuration Changes
- Document updates
- Explain why needed
- Update setup instructions
- Note compatibility

### Format

```markdown
## Learning Log

### 2026-01-11: Error Handling Pattern Update
**Issue**: Used `unwrap()` extensively, causing panics.
**Learning**: Always use `Result<T, E>` with `?` operator.
**Corrective Action**: Updated all unwrap() calls. Added linter rule.
**New Standard**: Never use `unwrap()` in production code.

### 2026-01-10: TypeScript Type Safety
**Issue**: Found `any` types, reducing type safety.
**Learning**: Using `any` defeats TypeScript's purpose.
**Corrective Action**: Replaced with proper types. Enabled strict mode.
**New Standard**: `any` forbidden. Use `unknown` then narrow with guards.
```

## Workflow Integration

```
1. User Requests Feature
   ↓
2. Main Agent identifies languages to use
   ↓
3. Create requirements.md with Language Stack section
   ↓
4. Add tasks with languages in frontmatter
   ↓
5. Review Agent verifies language stack documented
   ↓
6. Implementation Agents:
   - MANDATORY: Read .agents/stacks/[language].md FIRST
   - Implement following standards strictly
   - Verify compliance
   - Update Learning Log if needed
   ↓
7. Verification checks stack standards compliance
   ↓
8. Update stack standards if new learnings
```

## Enforcement

### Zero Tolerance Policy

**FORBIDDEN:**
- Writing code without reading stack standard file
- Deviating from documented standards without approval
- Ignoring coding conventions in stack files
- Not updating Learning Log when mistakes made
- Creating specs without documenting language stack
- Using languages not documented in requirements

### Violation Consequences

1. Code rejected immediately
2. Agent required to read stack standards
3. Rewrite code to comply
4. Document violation in Learning Log
5. Report violation to user

### Mandatory Checks (Before ANY Commit)

1. **Stack Standards Read**: Agent confirms reading stack files
2. **Code Format**: Pass formatter (rustfmt, prettier, black)
3. **Linter**: Pass linter with zero warnings
4. **Type Check**: Pass type checker if supported
5. **Tests**: All tests pass
6. **Documentation**: Required docs present
7. **Standards Compliance**: Check against stack standards

**If any check fails, code CANNOT be committed.**

## Examples

### Good Practice ✅

**Starting Rust Implementation:**
1. Reads requirements.md, sees "Language Stack: Rust"
2. IMMEDIATELY reads `.agents/stacks/rust.md` (MANDATORY)
3. Studies coding standards (Result<T,E>, rustfmt, clippy, no unwrap())
4. Implements code following ALL standards
5. Runs: `cargo fmt`, `cargo clippy`, `cargo test`
6. All checks pass
7. Commits code
8. Discovers better pattern → updates Learning Log

### Bad Practice ❌

**Starting Without Reading Standards:**
1. Reads requirements.md
2. Starts writing Rust code immediately (VIOLATION)
3. Uses `unwrap()` everywhere (violates standards)
4. Doesn't run clippy (violates process)
5. Code has warnings (violates quality requirements)
6. Commits anyway (SEVERE VIOLATION)

**Result**: Code rejected, agent must read standards and rewrite.

## Stack File Self-Improvement

Stack files evolve over time:

1. **Initial State**: Basic standards and common patterns
2. **After Mistakes**: Learning Log updated with corrections
3. **After Discovery**: New patterns added to examples
4. **After Tool Updates**: Configuration updated
5. **After Standards Change**: Best practices refined

**Result**: Stack files become comprehensive guides refined by actual project experience.

## Summary

**Golden Rules:**
1. **Read stack files BEFORE writing code** (MANDATORY)
2. **ZERO TOLERANCE for standard deviations**
3. **Update Learning Log when learning occurs**
4. **All checks must pass before commit**
5. **Stack files are living documents** - improve them
6. **Language stack documented in requirements.md**

---

_Version: 1.0 - Last Updated: 2026-02-27_
