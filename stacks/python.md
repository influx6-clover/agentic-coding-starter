# Python Coding Standards

## Overview
- **Language**: Python 3.10+ (prefer 3.11 or 3.12)
- **Use Cases**: Data processing, scripting, automation, backend services, machine learning
- **Official Docs**: https://docs.python.org/3/

## Skill References (MANDATORY)

**ALL Python skills MUST be consulted based on task type. Load skills selectively to optimize context.**

### Project Setup & Configuration ⚙️

**Read BEFORE setting up new Python projects or configuring environment:**

- [`python-directory-and-configuration`](../skills/python-directory-and-configuration/skill.md)
  - Python installation with pyenv
  - Virtual environment setup (venv, Poetry, uv)
  - Project structure and module organization
  - pyproject.toml configuration (black, ruff, mypy, pytest)
  - Development workflow and pre-commit hooks
  - Environment variables with python-dotenv

### Implementation Work 🔨

**Read BEFORE implementing any new features:**

- [`python-clean-implementation`](../skills/python-clean-implementation/skill.md)
  - Dependency hierarchy (project → stdlib → pip packages)
  - Google/NumPy docstring patterns
  - Custom exception handling patterns
  - Type hints and mypy compliance
  - Pythonic idioms (context managers, comprehensions, dataclasses)
  - Security best practices (input validation, secrets management, SQL/command injection)
  - Performance patterns (generators, lru_cache, __slots__)
  - Common pitfalls (mutable defaults, broad exceptions)

### Testing Work 🧪

**Read BEFORE writing or reviewing tests:**

- [`python-testing-excellence`](../skills/python-testing-excellence/skill.md)
  - **CRITICAL**: Docker/docker-compose for real infrastructure (FIRST)
  - **CRITICAL**: Real code over mocks philosophy
  - pytest patterns and fixtures
  - Essential pytest plugins (pytest-httpserver, pytest-postgresql, testcontainers)
  - Test organization (unit vs integration)
  - Property-based testing with Hypothesis
  - Test coverage with pytest-cov

### Async/Await Work ⚡

**Read BEFORE implementing async code:**

- [`python-with-async-code`](../skills/python-with-async-code/skill.md)
  - Core principle: Never block the event loop
  - Non-blocking I/O with asyncio
  - asyncio.to_thread for CPU-intensive work
  - Task management with asyncio.gather
  - Queue patterns for producer-consumer
  - Timeout and cancellation patterns
  - Async testing with pytest-asyncio

### Django Work 🌐

**Read BEFORE working with Django:**

- [`python-django-models`](../skills/python-django-models/skill.md)
  - Base model classes (UUID, timestamps, soft delete, temporal)
  - Query optimization (select_related, prefetch_related)
  - N+1 query prevention
  - Transaction patterns with performance optimization
  - Real database testing with Docker/testcontainers
  - Factory-Boy for test data generation

- [`python-django-configuration`](../skills/python-django-configuration/skill.md)
  - django-configurations framework (MANDATORY)
  - Environment variable management (Required, Optional, Default-allowed)
  - Multi-tenancy with BRAND pattern
  - Feature flags
  - Caching configuration (Redis, Database, Memcached)

- [`python-django-testing`](../skills/python-django-testing/skill.md)
  - **CRITICAL**: 100% coverage requirement (MANDATORY)
  - **CRITICAL**: Function-based tests only (never classes)
  - Test naming: test_<function>__<scenario>__<assertion>
  - Fixtures in file (away from bloated conftest.py)
  - Factory-Boy patterns
  - Given/When/Then structure
  - Django-specific patterns (@override_settings, N+1 testing)

### gRPC Work 📡

**Read BEFORE implementing gRPC services:**

- [`python-grpc-services`](../skills/python-grpc-services/skill.md)
  - Service registration pattern (SERVICES_TO_REGISTER)
  - **CRITICAL**: Authentication decorators (MANDATORY for all endpoints)
  - Method signature requirements
  - Error handling with specific exceptions
  - Model to proto conversion
  - Django ORM integration

- [`python-grpc-protobuf`](../skills/python-grpc-protobuf/skill.md)
  - **CRITICAL**: _pb2 suffix import pattern (MANDATORY)
  - Import both _pb2 and _pb2_grpc for services
  - Code generation workflow with protoc
  - Generated files committed to version control
  - Proto file organization

### Monorepo Work 🏗️

**Read BEFORE working in monorepo:**

- [`python-monorepo-structure`](../skills/python-monorepo-structure/skill.md)
  - **CRITICAL**: Services import from ca-lib ONLY (never from each other)
  - **CRITICAL**: Cross-service communication via gRPC ONLY
  - Virtual workspace root configuration
  - ca-lib utilities reference (foundation library)
  - Protobuf cross-references
  - Development workflows

---

## Quick Reference

### Essential Tools
```bash
# Install core tools
pip install black ruff mypy pytest

# Or with Poetry
poetry add --group dev black ruff mypy pytest
```

### Naming Conventions (PEP 8)
- **Variables/Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

### Type Hints (Mandatory)
```python
def process_data(items: list[str], limit: int = 10) -> dict[str, int]:
    """All function signatures must have type hints."""
    ...
```

### Testing Hierarchy (CRITICAL)
```
1. Docker/docker-compose (FIRST) - Real infrastructure
2. Test instance credentials (SECOND) - Provided environments
3. pytest plugins (THIRD) - pytest-httpserver, pytest-postgresql
4. Mock (LAST RESORT) - External dependencies only
```

---

## Code Verification Workflow

**MANDATORY**: Every Python code change MUST be verified by a dedicated verification agent before commit.

### Verification Agent Responsibility

The Main Agent MUST:
1. **Delegate** to Python Verification Agent after implementation
2. **Wait** for verification results
3. **Not commit** until verification passes
4. **Report** results to user

### Verification Checks (All Must Pass)

```bash
# 1. Format check
black --check .

# 2. Lint check
ruff check .

# 3. Type check
mypy .

# 4. Test execution
pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# 5. Import check
python -m py_compile src/**/*.py

# 6. Security check (optional)
pip-audit
# or
bandit -r src/
```

### Standards Compliance Checks

- [ ] Type hints present for all function signatures
- [ ] Docstrings for all public functions and classes
- [ ] No use of dangerous functions (eval, exec, os.system)
- [ ] Naming conventions followed
- [ ] No broad exception catching
- [ ] No mutable default arguments
- [ ] Context managers used for resources
- [ ] No `import *`

### Verification Report Format

```markdown
# Python Verification Report

## Summary
- **Status**: PASS ✅ / FAIL ❌
- **Files Changed**: [list]
- **Verification Time**: [timestamp]

## Check Results
1. Format Check: PASS ✅ / FAIL ❌
2. Linting Check: PASS ✅ / FAIL ❌
3. Type Check: PASS ✅ / FAIL ❌
4. Tests: PASS ✅ / FAIL ❌ (X tests, Y% coverage)
5. Import Check: PASS ✅ / FAIL ❌
6. Security Check: PASS ✅ / FAIL ❌
7. Standards Compliance: PASS ✅ / FAIL ❌

## Overall Assessment
[Detailed explanation]

## Blockers
[Any issues preventing commit]
```

### Integration with Other Rules

- **Works With Rule 03 (Work Commit Rules)**: Verification before commit
- **Works With Rule 04 (Agent Orchestration)**: Main Agent orchestrates verification
- **Works With Rule 06 (Specifications)**: Verification confirms requirements met
- **Works With Rule 07 (Language Conventions)**: Enforces stack standards

### Zero Tolerance Policy

**VIOLATIONS** are treated with **ZERO TOLERANCE**:
- ❌ **FORBIDDEN**: Committing Python code without verification
- ❌ **FORBIDDEN**: Skipping verification checks
- ❌ **FORBIDDEN**: Ignoring verification failures
- ❌ **FORBIDDEN**: Running verification after commit

**Violation Consequences**:
1. Changes **REVERTED**
2. Required to run verification properly
3. Fix ALL issues before re-attempting
4. Document violation in Learning Log

---

## Valid Code Requirements

Code is considered valid when:
- [x] Passes `black --check .`
- [x] Passes `ruff check .`
- [x] Passes `mypy .`
- [x] Passes `pytest` with 80%+ coverage
- [x] Has type hints for all function signatures
- [x] Has docstrings for all public functions/classes
- [x] Follows all naming conventions
- [x] No use of eval/exec/os.system
- [x] No broad exception catching
- [x] Context managers for resources

---

## Common Pitfalls (Quick Reference)

**For detailed guidance, see skills above**

### Pitfall 1: Mutable Default Arguments
```python
# BAD ❌
def add_item(item, items=[]):
    items.append(item)
    return items

# GOOD ✅
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

### Pitfall 2: Not Using Type Hints
```python
# BAD ❌
def process(data):
    return data.upper()

# GOOD ✅
def process(data: str) -> str:
    return data.upper()
```

### Pitfall 3: Catching Too Broad Exceptions
```python
# BAD ❌
try:
    result = risky_operation()
except Exception:
    result = None

# GOOD ✅
try:
    result = risky_operation()
except (NetworkError, TimeoutError) as e:
    logger.error(f"Operation failed: {e}")
    result = None
```

### Pitfall 4: Not Closing Resources
```python
# BAD ❌
f = open('file.txt')
content = f.read()
f.close()

# GOOD ✅
with open('file.txt') as f:
    content = f.read()
```

### Pitfall 5: Mocking Our Own Code
```python
# BAD ❌ - Mocking internal database
def test_user_repo(mocker):
    mock_db = mocker.Mock()
    repo = UserRepository(mock_db)
    # Only tests mock, not real code!

# GOOD ✅ - Docker with real database
def test_user_repo(postgresql):  # testcontainers fixture
    repo = UserRepository(postgresql)
    # Tests real database operations!
```

---

## Learning Log

### 2026-02-02: Added Django, gRPC, and Monorepo Skills

**Issue:** Need comprehensive skills for Django, gRPC, and monorepo development.

**Action:** Created 6 additional Python skills (11,771 lines total):

**Django Skills (3 skills - 9,410 lines):**
- **python-django-models**: Base model classes, query optimization, N+1 prevention, real database testing
- **python-django-configuration**: django-configurations, environment management, multi-tenancy, caching
- **python-django-testing**: 100% coverage (MANDATORY), function-based tests, Factory-Boy, Given/When/Then

**gRPC Skills (2 skills - 1,480 lines):**
- **python-grpc-services**: Service registration, authentication decorators (MANDATORY), error handling
- **python-grpc-protobuf**: _pb2 suffix pattern (MANDATORY), code generation, proto organization

**Monorepo Skill (1 skill - 881 lines):**
- **python-monorepo-structure**: Workspace configuration, ca-lib utilities, cross-service dependencies (gRPC only)

**Key Principles Established:**
- Services import from ca-lib ONLY (never from each other)
- Cross-service communication via gRPC ONLY (no direct imports)
- Authentication MANDATORY for all gRPC endpoints
- 100% test coverage MANDATORY for Django
- _pb2 suffix MANDATORY for protobuf imports
- Real databases over mocks (Docker/testcontainers FIRST)

**Adapted from:** DJANGO.md, TESTING.md, GRPC.md, MONOREPO.md counterpart prompts

**New Standard:** All Django, gRPC, and monorepo work must reference appropriate skills.

### 2026-02-02: Streamlined Stack File - Skills References

**Issue:** Python stack file had 1200+ lines with content now covered by dedicated skills.

**Action:** Streamlined stack file to ~400 lines:
- **Kept**: Skill references, verification workflow, quick reference
- **Removed**: Detailed content now in skills (setup, patterns, examples)
- **Focused on**: Project-specific rules and verification requirements

**Rationale:**
- Skills provide comprehensive detail
- Stack file becomes navigation hub
- Reduces duplication
- Easier to maintain
- Agents read skills for detailed guidance, stack for project rules

**New Standard:** Stack files should be concise navigation hubs that reference skills for details.

### 2026-02-02: Python Skills Created - Rust Patterns Adapted

**Issue**: Need comprehensive Python skills equivalent to Rust skills.

**Learning**: Created four Python skills adapted from Rust patterns:
- **python-clean-implementation**: Dependency hierarchy (project → stdlib → pip), type hints, docstrings, custom exceptions
- **python-testing-excellence**: Docker/docker-compose FIRST, real code over mocks, pytest plugins, Hypothesis
- **python-with-async-code**: asyncio patterns, event loop protection, async testing
- **python-directory-and-configuration**: Virtual environments, pyproject.toml, development workflow

Key adaptations from Rust:
- `derive_more` → custom exception classes with inheritance
- rustfmt/clippy → black/ruff
- Cargo.toml → pyproject.toml
- tokio → asyncio
- proptest → Hypothesis
- cargo test → pytest

**New Standard**: All Python development must reference appropriate skill before starting work.

### 2026-01-11: Initial Python Standards

**Issue**: Creating initial standards document.
**Learning**: Established baseline standards for Python development in this project.
**New Standard**: All Python code must follow these standards starting from this date.

---

*Created: 2026-01-11*
*Last Updated: 2026-02-02 - Added Django, gRPC, and Monorepo skills; updated skill references*
