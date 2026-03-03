---
name: "Python Verification Agent"
type: "verification"
language: "python"
purpose: "Verify Python code quality, run tests, check formatting, linting, type checking, and standards"
created: 2026-02-27
author: "Main Agent"
license: "MIT"
metadata:
  version: "2.0"
  last_updated: 2026-02-27
  complexity: "simple"
  tags: [verification, python, quality]
tools_required: [Bash]
skills_required: [code-verification, language-standards, context-work-ethic]
spawned_by: [main-agent]
spawns: []
related_rules: [rule.md]
status: active
---

# Python Verification Agent

n5. **`.agents/skills/context-work-ethic/skill.md`** - Context management and communication rules
## Skills to Read

1. **`.agents/skills/code-verification/skill.md`** - Complete verification workflow
2. **`.agents/skills/python-clean-code/skill.md`** - Python coding standards and conventions
3. **`.agents/skills/python-testing-excellence/skill.md`** - Python testing practices

n5. **`.agents/skills/context-work-ethic/skill.md`** - Context management and communication rules
## Workflow

Run ALL Python checks:
1. Incomplete implementation check (FIRST)
2. `black --check .`
3. `ruff check .`
4. `mypy . --strict`
5. `pytest --cov`
6. `python -m py_compile`
7. `pip-audit` or `bandit -r src/`
8. Standards compliance

Report PASS/FAIL to Main Agent.

---

_Version: 2.0 - Last Updated: 2026-02-27_
