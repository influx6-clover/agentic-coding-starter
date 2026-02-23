---
name: "Python Directory and Configuration"
description: "Set up Python projects with proper structure, virtual environments, and tool configuration"
approved: Yes
created: 2026-02-02
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-02"
tags:
  - python
  - installation
  - configuration
  - project-setup
  - virtual-environments
files:
  - examples/python-installation.md: "Complete Python installation guide"
  - examples/python-project-setup.md: "Step-by-step project setup and structure"
  - examples/pyproject-config.md: "pyproject.toml configuration examples"
---

# Python Directory and Configuration

## When to Use This Skill

Read this when:
- Setting up a new Python project
- Installing Python on a new machine
- Configuring project structure
- Setting up development environment

---

## Installation

### 1. Install Python

```bash
# Using pyenv (recommended for managing multiple versions)
curl https://pyenv.run | bash

# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Install Python 3.11 or 3.12
pyenv install 3.12.0
pyenv global 3.12.0

# Verify installation
python --version
python3 --version
```

### 2. Install Development Tools

```bash
# Using pip
pip install black ruff mypy pytest pytest-cov

# Or using pipx (recommended for tools)
pipx install black
pipx install ruff
pipx install mypy
pipx install poetry  # Or use pip install poetry

# Verify installations
black --version
ruff --version
mypy --version
pytest --version
```

---

## Project Setup

### Using Poetry (Recommended)

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Create new project
poetry new my-python-project
cd my-python-project

# Or initialize in existing directory
mkdir my-python-project
cd my-python-project
poetry init

# Project structure created:
# my-python-project/
# ├── pyproject.toml
# ├── README.md
# ├── my_python_project/
# │   └── __init__.py
# └── tests/
#     └── __init__.py
```

### Using uv (Modern Alternative)

```bash
# Install uv (fastest Python package installer)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create new project
uv init my-python-project
cd my-python-project

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Unix/macOS
# .venv\Scripts\activate   # Windows
```

### Manual Setup with venv

```bash
# Create project directory
mkdir my-python-project
cd my-python-project

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Unix/macOS
# .venv\Scripts\activate   # Windows

# Create project structure
mkdir -p src/myapp tests
touch src/myapp/__init__.py tests/__init__.py
touch pyproject.toml README.md
```

---

## Recommended Project Structure

```
my-python-project/
├── .venv/                  # Virtual environment (don't commit)
├── src/                    # Source code (src layout recommended)
│   └── myapp/
│       ├── __init__.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── auth_service.py
│       └── utils/
│           ├── __init__.py
│           └── validators.py
├── tests/                  # Test directory
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── integration/
│       ├── __init__.py
│       └── test_api.py
├── docs/                   # Documentation
├── .gitignore             # Git ignore file
├── pyproject.toml         # Project metadata and dependencies
├── README.md              # Project documentation
└── .python-version        # Python version (for pyenv)
```

---

## pyproject.toml Configuration

### Complete Example

```toml
[project]
name = "my-python-project"
version = "0.1.0"
description = "My awesome Python project"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    # Add runtime dependencies here
]

[project.optional-dependencies]
dev = [
    "black>=24.0",
    "ruff>=0.1",
    "mypy>=1.8",
    "pytest>=7.4",
    "pytest-cov>=4.1",
    "pytest-asyncio>=0.23",
]

[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

# Black configuration
[tool.black]
line-length = 100
target-version = ['py310', 'py311', 'py312']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''

# Ruff configuration
[tool.ruff]
line-length = 100
target-version = "py310"
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
    "TCH", # flake8-type-checking
]
ignore = []

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__.py
"tests/**/*.py" = ["S101"]  # Allow assert in tests

# Mypy configuration
[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

# Pytest configuration
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "--cov=src/myapp",
    "--cov-report=term-missing",
    "--cov-report=html",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]
asyncio_mode = "auto"

# Coverage configuration
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/.venv/*",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
```

### Poetry-Specific Configuration

```toml
[tool.poetry]
name = "my-python-project"
version = "0.1.0"
description = "My awesome Python project"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "myapp", from = "src"}]

[tool.poetry.dependencies]
python = "^3.10"
# Add runtime dependencies here

[tool.poetry.group.dev.dependencies]
black = "^24.0"
ruff = "^0.1"
mypy = "^1.8"
pytest = "^7.4"
pytest-cov = "^4.1"
pytest-asyncio = "^0.23"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

## .gitignore for Python

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/
*.egg

# Virtual environments
.venv/
venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Ruff
.ruff_cache/

# OS
.DS_Store
Thumbs.db
```

---

## Development Workflow

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd my-python-project

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Unix/macOS

# Install dependencies
pip install -e ".[dev]"

# Or with Poetry
poetry install

# Or with uv
uv pip install -e ".[dev]"
```

### Daily Development

```bash
# Activate virtual environment
source .venv/bin/activate

# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_models.py::test_user_creation
```

### Pre-commit Hooks (Recommended)

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.15
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
EOF

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

---

## Module Organization

### Package __init__.py

```python
# src/myapp/__init__.py
"""My App - A Python application.

This package provides functionality for X, Y, and Z.
"""

__version__ = "0.1.0"

# Re-export commonly used items
from .models import User, Post
from .services import UserService, AuthService
from .exceptions import AppError, ValidationError

__all__ = [
    "User",
    "Post",
    "UserService",
    "AuthService",
    "AppError",
    "ValidationError",
]
```

---

## Environment Variables

### Using python-dotenv

```bash
# Install python-dotenv
pip install python-dotenv
```

```python
# Load environment variables
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env file

DATABASE_URL = os.getenv("DATABASE_URL", "")
API_KEY = os.getenv("API_KEY", "")
```

### .env File (DON'T COMMIT!)

```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost/dbname
API_KEY=sk-1234567890abcdef
DEBUG=true
```

### .env.example (DO COMMIT)

```bash
# .env.example
DATABASE_URL=postgresql://user:pass@localhost/dbname
API_KEY=your-api-key-here
DEBUG=false
```

---

## Common Commands Reference

```bash
# Virtual Environment
python -m venv .venv              # Create venv
source .venv/bin/activate         # Activate (Unix)
deactivate                        # Deactivate

# Dependencies
pip install package               # Install package
pip install -e .                  # Install project in editable mode
pip install -e ".[dev]"          # Install with dev dependencies
pip freeze > requirements.txt     # Export dependencies
pip install -r requirements.txt   # Install from requirements

# Poetry
poetry add package                # Add dependency
poetry add --group dev package    # Add dev dependency
poetry install                    # Install dependencies
poetry update                     # Update dependencies
poetry shell                      # Activate virtual environment

# Code Quality
black src/ tests/                 # Format code
ruff check src/ tests/            # Lint code
ruff check --fix src/ tests/      # Lint and fix
mypy src/                         # Type check
pytest                            # Run tests
pytest --cov=src                  # Run tests with coverage

# Build and Distribution
python -m build                   # Build package
twine upload dist/*               # Upload to PyPI
```

---

## Learning Log

### 2026-02-02: Python Directory and Configuration Skill Created

**Issue:** Creating Python equivalent of Rust directory and configuration skill.

**Learning:** Adapted Rust cargo/rustup patterns to Python:
- Virtual environments instead of cargo workspaces
- pyproject.toml instead of Cargo.toml
- black/ruff/mypy instead of rustfmt/clippy
- pytest instead of cargo test
- Poetry/uv as modern alternatives to pip

**New Standard:** All Python projects must follow these setup patterns.

---

## Examples

See `examples/` directory for detailed guides:

- `python-installation.md` - Complete Python installation guide
- `python-project-setup.md` - Step-by-step project setup
- `pyproject-config.md` - pyproject.toml configuration examples

## Related Skills

- [Python Clean Implementation](../implementation/skill.md) - For implementation patterns
- [Python Testing Excellence](../testing/skill.md) - For testing setup
- [Python with Async Code](../async/skill.md) - For async project setup

---

*Last Updated: 2026-02-02*
*Version: 1.0*
