---
name: "Git Workflow"
description: "Git commit and push workflow with verification, safety rules, and best practices"
approved: Yes
created: 2026-02-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.1"
  last_updated: "2026-02-27"
  tags: [git, version-control, workflow, commit, push, safety]
tools: [Bash]
files: []
---

# Git Workflow

## Overview

Complete git workflow covering commit requirements, push automation, safety rules, commit message formatting, and verification integration.

## Core Principles

1. Commit after each completed task/feature (following verification)
2. Push to remote immediately after every commit
3. Only non-destructive git operations allowed
4. All code commits require verification first
5. Never add Claude or agent attribution to commits

## Branch Management

When starting new work:
1. Check current branch: `git branch --show-current`
2. If on main/master: Create new branch from spec name (e.g., `04-add-auth-middleware`)
3. Otherwise: Use current branch as-is

## Workflows

### Code Changes (with Verification)

1. Implementation agent completes task/feature and reports to Main Agent
2. Main Agent spawns Verification Agent
3. Verification Agent runs all checks
4. If all pass: `git add [files]` → `git commit` → `git status` → `git push` → verify
5. If any fail: Create urgent task, do NOT commit

### Non-Code Changes

1. Make changes
2. `git add [files]` → `git commit` → `git status` → `git push` → verify

## Commit Message Format

```
Brief summary (50 chars max)

Detailed explanation of what and why.

Changes made:
- Change 1
- Change 2

[Verification status for code changes]

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Code example:**
```bash
git commit -m "$(cat <<'EOF'
Add authentication middleware

Implemented JWT-based authentication middleware to secure API
endpoints. Validates tokens and attaches user info to requests.

Changes made:
- Created auth.js middleware with token validation
- Added JWT verification using jsonwebtoken
- Implemented error handling for invalid/expired tokens

Verified by JavaScript Verification Agent: All checks passed
- Format: PASS (prettier)
- Lint: PASS (eslint, 0 warnings)
- Tests: 12/12 PASS
- Build: PASS

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Non-code example:**
```bash
git commit -m "$(cat <<'EOF'
Update installation instructions

Added Docker setup steps and clarified dependency requirements.

Changes made:
- Added Docker installation section
- Updated prerequisites list
- Fixed typos in quick start guide

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Safety Rules

### Forbidden Operations
- `git push --force` / `-f` (except commit correction with `--force-with-lease`)
- `git reset --hard`
- `git reset --soft HEAD~N` (except commit correction)
- `git rebase -i`
- `git commit --amend` (except specific cases)
- Any history-rewriting operations

### Allowed Operations
- `git add`, `git commit`, `git status`, `git push` (standard)
- `git pull`, `git fetch`, `git log`, `git diff`
- `git branch`, `git checkout`, `git stash`, `git merge` (non-force)

## Commit Correction Pattern

For just-committed features needing immediate fix:

1. `git reset --soft HEAD~1` (keeps changes staged)
2. Make the fix
3. `git add [files]` (re-stage all)
4. `git commit -m "..."` (recommit complete feature)
5. `git push` or `git push --force-with-lease` (if already pushed)

**Use only when:**
- Just committed (1-2 commits ago)
- No other commits after
- On feature branch (not main)

## Special Cases

### Merge Conflicts
1. `git pull` to fetch remote changes
2. Resolve conflicts
3. `git add [files]` → `git commit` → `git push`

### First Push to New Branch
Use `git push -u origin branch-name` for first push to set upstream

### Network/Protection Issues
Report to user if push fails due to network issues or branch protection. Do not retry indefinitely or use `--force`.

## Main Agent Responsibilities

When receiving completion reports from sub-agents:
1. Check if sub-agent pushed
2. If not confirmed: Run `git status` to check for unpushed commits
3. If unpushed: Remind sub-agent and wait for push confirmation
4. Then continue workflow

**Detection:** `git status` shows "ahead of origin" or `git log origin/main..HEAD` shows unpushed commits

## Version History Management

1. All version history goes in `.agents/CHANGELOG.md`
2. Individual files show only current version and link to changelog
3. When updating files: Update file + add CHANGELOG entry + commit both together

## Enforcement

### Must Do
1. Commit after task/feature completion (with verification for code)
2. Push automatically after every commit
3. Use detailed commit messages with bullet points
4. Include verification status for code changes
5. Verify commit and push succeeded

### Must Not Do
1. Ask for approval before commit/push
2. Commit incomplete tasks/features
3. Batch multiple tasks into one commit
4. Use forbidden git operations
5. Commit code without verification
6. Skip push after commit
7. Add agent attribution (no "Claude" in commit messages)

### Critical Violations
1. Committing code without verification
2. Committing code with failed verification
3. Missing verification status in code commits
4. Force push or destructive operations

### Corrective Action
Stop immediately → Revert if needed → Run proper verification → Re-commit correctly → Document in Learning Log

---

_Version: 1.1 - Last Updated: 2026-02-27_
