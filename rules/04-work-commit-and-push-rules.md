# Work Commit and Push Rules

## Purpose

Establishes mandatory git workflow practices for version control. All agents must commit after verified changes and push automatically.

## Core Requirements

**Read Complete Workflow**: See `.agents/skills/git-workflow/skill.md` for comprehensive git workflow details.

### Must Do

1. Commit code after every completed task/feature + verification passes
2. Commit non-code changes (docs, config) immediately after completion
3. Push automatically after every commit (no approval needed)
4. Run verification before committing any code changes
5. Include verification status in code commit messages
6. Use detailed commit messages with bullet points
7. Verify commit and push succeeded before proceeding
8. Use only safe, non-destructive git operations

### Must Not Do

1. Add Claude or any other agent attribution in commits
2. Commit non-working code or code with failed tests
3. Commit before verification completes (for code changes)
4. Ask for permission to commit or push
5. Use forbidden git operations (force push, hard reset, etc.)

## Quick Workflow

### Code Changes
```
Complete → Verify → ALL PASS → git add → git commit → git push → verify → proceed
```

### Non-Code Changes
```
Complete → git add → git commit → git push → verify → proceed
```

## Commit Message Format

```
Brief summary (50 chars max)

Detailed explanation of what and why.

Changes made:
- Change 1
- Change 2

[Verification status for code]

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Safety

### ❌ Forbidden Operations
- `git push --force` or `-f`
- `git reset --hard`
- `git rebase -i`
- `git commit --amend` (except specific cases)
- Any history-rewriting operations

### ✅ Allowed Operations
- `git add`, `git commit`, `git push` (standard)
- `git pull`, `git fetch`, `git status`
- `git branch`, `git checkout`, `git merge`

See `.agents/skills/git-workflow/skill.md` for complete safety rules and special cases.

## Enforcement

### Critical Violations (Zero Tolerance)
1. Committing code without verification
2. Committing code with failed verification
3. Using forbidden git operations
4. Forgetting to commit or push

### Corrective Action
1. Stop immediately
2. Revert if needed
3. Run proper verification
4. Re-commit correctly
5. Document in Learning Log

---

_Version: 2.0 - Last Updated: 2026-02-27_
_For complete version history, see [../CHANGELOG.md](../CHANGELOG.md)_
