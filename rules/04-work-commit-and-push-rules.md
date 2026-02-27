# Work Commit and Push Rules

## Purpose

Establishes mandatory git workflow practices for version control.

**Complete Workflow Details**: See `.agents/skills/git-workflow/skill.md`

## Must Do

1. Commit code after every completed task/feature + verification passes all checks
2. Commit non-code changes (docs, config) immediately after completion
3. Push automatically after every commit (no approval needed)
4. Run verification before committing any code changes
5. Validate all tests pass before committing

## Must Not Do

1. Add Claude or any other agent attribution in commits
2. Commit non-working code or code with failed tests
3. Commit before verification completes (for code changes)
4. Ask for permission to commit or push
5. Forget to commit and push after completing work

## Critical Violations (Zero Tolerance)

1. Committing code without verification
2. Committing code with failed verification
3. Forgetting to commit or push completed work

---

_Version: 2.0 - Last Updated: 2026-02-27_
