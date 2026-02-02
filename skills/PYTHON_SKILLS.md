# Python Skills - Adapted from Rust

This directory contains Python skills that have been adapted from the Rust skills, maintaining the same structure and philosophy while embracing Python idioms.

## Available Skills

### 1. Python Clean Implementation
**Path**: `python-clean-implementation/skill.md`

Covers:
- Dependency hierarchy (project → stdlib → pip packages)
- Documentation with Google/NumPy docstrings
- Custom exception handling
- Type hints and mypy compliance
- Pythonic idioms (context managers, comprehensions, dataclasses)
- Security patterns
- Performance optimization

**Adapted from**: `rust-clean-implementation/skill.md`

### 2. Python Testing Excellence
**Path**: `python-testing-excellence/skill.md`

Covers:
- **CRITICAL**: Real code over mocks philosophy
- pytest patterns and fixtures
- Test organization strategies
- Property-based testing with Hypothesis
- Mock usage guidelines (external dependencies ONLY)
- Test markers and parametrization

**Adapted from**: `rust-testing-excellence/skill.md`

### 3. Python with Async Code
**Path**: `python-with-async-code/skill.md`

Covers:
- asyncio patterns and best practices
- Event loop protection
- Non-blocking I/O patterns
- Task management (asyncio.gather, asyncio.wait)
- Queue patterns for producer-consumer
- Async testing with pytest-asyncio
- Common pitfalls and solutions

**Adapted from**: `rust-with-async-code/skill.md`

### 4. Python Directory and Configuration
**Path**: `python-directory-and-configuration/skill.md`

Covers:
- Python installation with pyenv
- Virtual environment setup (venv, Poetry, uv)
- Project structure and organization
- pyproject.toml configuration
- Development workflow
- Pre-commit hooks

**Adapted from**: `rust-directory-and-configuration/skill.md`

## Key Adaptations from Rust

### Documentation
- Rust: `///` doc comments with WHY/WHAT/HOW
- Python: Google/NumPy docstrings with Args/Returns/Raises

### Error Handling
- Rust: `derive_more::From` for error types
- Python: Custom exception classes with inheritance

### Testing
- Rust: `cargo test` with proptest
- Python: pytest with Hypothesis

### Async Runtime
- Rust: tokio with `spawn_blocking`
- Python: asyncio with `asyncio.to_thread`

### Code Quality Tools
- Rust: rustfmt + clippy
- Python: black + ruff + mypy

### Project Configuration
- Rust: Cargo.toml
- Python: pyproject.toml

## Common Principles (Unchanged)

### 1. Dependency Hierarchy
**BOTH**: Project → Stdlib → External packages (last resort)

### 2. Real Code Over Mocks
**BOTH**: Only mock external dependencies, never your own code

### 3. Type Safety
- Rust: Compile-time type checking
- Python: Runtime with mypy static analysis

### 4. Documentation Quality
- Rust: Mandatory panics documentation
- Python: Mandatory raises documentation

### 5. Security Focus
- Input validation
- No dangerous operations (eval/exec in Python, unsafe in Rust)
- Parameterized queries
- Secrets management

## Usage

Reference the appropriate skill before starting work:

```bash
# Before implementing new features
Read: python-clean-implementation/skill.md

# Before writing tests
Read: python-testing-excellence/skill.md

# Before async work
Read: python-with-async-code/skill.md

# Before project setup
Read: python-directory-and-configuration/skill.md
```

## Examples Directory Structure

Each skill includes an `examples/` directory with detailed guides:

```
python-clean-implementation/
├── skill.md
├── examples/
│   ├── documentation-patterns.md
│   ├── error-handling-guide.md
│   ├── security-guide.md
│   ├── pythonic-patterns.md
│   └── basic-template.md
└── templates/
    └── basic-example.py

python-testing-excellence/
├── skill.md
└── examples/
    └── intro-to-property-based-testing.md

python-with-async-code/
├── skill.md
└── examples/
    └── async-best-practices.py

python-directory-and-configuration/
├── skill.md
└── examples/
    ├── python-installation.md
    ├── python-project-setup.md
    └── pyproject-config.md
```

## Philosophy

These skills maintain the same core philosophy as the Rust skills:

1. **Build libraries, not frameworks** - Everything public by design
2. **Composition over inheritance** - Favor small, composable pieces
3. **Explicit over implicit** - Clear, documented behavior
4. **Security by design** - Validate inputs, protect secrets
5. **Real testing** - Test actual behavior, not mocks

---

*Created: 2026-02-02*
*Adapted from Rust skills by Main Agent*
