---
name: "Git Workflow"
description: "Git commit and push workflow with verification, safety rules, and best practices"
approved: Yes
created: 2026-02-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-27"
  tags: [git, version-control, workflow, commit, push, safety]
tools: [Bash]
files: []
---

# Git Workflow

## Overview

This skill defines the complete git workflow including commit requirements, push automation, safety rules, commit message formatting, and verification integration.

## Core Principles

1. **Task/Feature Commits**: Commit after each completed task/feature (following verification)
2. **Automatic Push**: Push to remote immediately after every commit
3. **Safety First**: Only non-destructive git operations allowed
4. **Verification Required**: All code commits require verification first
5. **No Attribution**: Never add Claude or agent attribution to commits

## Branch Management

### Creating Branches

When starting new work:
- **IF on main/master**: Create new branch from spec name (e.g., `04-add-auth-middleware`)
- **ELSE**: Use current branch as-is

```bash
# Check current branch
git branch --show-current

# Create new branch if needed
git checkout -b feature-name
```

## Complete Workflow

### Code Changes (with Verification)

```
1. Implementation agent completes task/feature
   ↓
2. Reports to Main Agent (never commits directly)
   ↓
3. Main Agent spawns Verification Agent
   ↓
4. Verification Agent runs ALL checks
   ↓
5. IF ALL PASS:
   ↓
6. Main Agent: git add [files]
   ↓
7. Main Agent: git commit -m "[message]"
   ↓
8. Main Agent: git status (verify)
   ↓
9. Main Agent: git push
   ↓
10. Verify push succeeded
   ↓
11. Proceed to next task

IF ANY FAIL: Create urgent task, do NOT commit
```

### Non-Code Changes (docs, config, etc.)

```
1. Make changes
   ↓
2. git add [files]
   ↓
3. git commit -m "[message]"
   ↓
4. git status (verify)
   ↓
5. git push
   ↓
6. Verify push succeeded
```

## Commit Message Format

### Structure

```
Brief summary (50 chars max)

Detailed explanation of what and why.

Changes made:
- Change 1
- Change 2
- Change 3

[Verification status for code changes]

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Examples

**Code Change with Verification:**
```bash
git add src/auth.js
git commit -m "$(cat <<'EOF'
Add authentication middleware

Implemented JWT-based authentication middleware to secure API
endpoints. Validates tokens and attaches user info to requests.

Changes made:
- Created auth.js middleware with token validation
- Added JWT verification using jsonwebtoken
- Implemented error handling for invalid/expired tokens
- Wrote comprehensive test suite

Verified by JavaScript Verification Agent: All checks passed
- Format: PASS (prettier)
- Lint: PASS (eslint, 0 warnings)
- Tests: 12/12 PASS
- Build: PASS

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
git push
```

**Non-Code Change:**
```bash
git add README.md
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
git push
```

## Safety Rules

### ❌ FORBIDDEN Operations

- `git push --force` or `git push -f`
- `git push --force-with-lease` (except Commit Correction)
- `git reset --hard`
- `git reset --soft HEAD~N` (except Commit Correction)
- `git rebase -i`
- `git filter-branch`
- `git commit --amend` (except specific cases)
- Any command with `--force` flag
- History-rewriting operations

### ✅ ALLOWED Operations

- `git add [files]`
- `git commit -m "[message]"`
- `git status`
- `git push` (standard)
- `git pull`
- `git fetch`
- `git branch`
- `git checkout -b [branch]`
- `git checkout [branch]`
- `git log`
- `git diff`
- `git stash` / `git stash pop`
- `git merge` (non-force)

## Commit Correction Pattern

When a just-committed feature needs immediate fix:

```bash
# 1. Soft undo (keeps changes staged)
git reset --soft HEAD~1

# 2. Make the fix
[fix code]

# 3. Re-stage all changes
git add [files]

# 4. Recommit with complete feature
git commit -m "$(cat <<'EOF'
Complete feature with fix

[Original feature + fix explanation]

Changes made:
- [Original changes]
- Fix: [what was fixed]

[Verification status]

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# 5. Push
git push  # If not yet pushed
# OR
git push --force-with-lease  # If already pushed (ONLY for this pattern)
```

**Use Only When:**
- Just committed feature (1-2 commits ago)
- No other commits after
- Want clean history
- On feature branch (not main)

## Special Cases

### Merge Conflicts

```bash
git push
# Error: Updates were rejected...

git pull              # Pull remote changes
# Resolve conflicts
git add [files]       # Stage resolved files
git commit -m "..."   # Commit if needed
git push              # Push again
```

### First Push to New Branch

```bash
git checkout -b new-feature
# Make changes
git add [files]
git commit -m "..."
git push -u origin new-feature  # Use -u for first push
```

### Network Issues

```bash
git push
# Error: Connection timeout

# Report to user:
# "Network error during push. Changes committed locally and safe."
# Do not retry indefinitely
# Do not use --force
```

### Branch Protection

```bash
git push
# Error: Protected branch requires review

# Report to user:
# "Changes committed. Remote requires pull request review."
```

## Main Agent Responsibilities

### Verify Sub-Agent Push

When receiving completion reports:

1. Check if sub-agent pushed
2. If not confirmed:
   - Run `git status` to check for unpushed commits
   - If unpushed commits exist:
     - Remind sub-agent: "You must git push per Rule 04"
     - Wait for push confirmation
     - Verify push succeeded
   - Then continue workflow

### Detection Commands

```bash
# Check if local is ahead of remote
git status

# Show unpushed commits
git log origin/main..HEAD
```

## Version History Management

### Central Changelog

All version history goes in `.agents/CHANGELOG.md`

Individual files show only:
```markdown
---
_Version: 1.0 - Last Updated: 2026-02-27_
_For complete version history, see [CHANGELOG.md](../CHANGELOG.md)_
```

### Commit Workflow for Version Changes

```bash
# 1. Update file content
# 2. Update version/date in file
# 3. Add entry to CHANGELOG.md
# 4. Commit both together

git add [file] .agents/CHANGELOG.md
git commit -m "Update [file] to version X: [description]

Added changelog entry for version X changes.

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

## Enforcement

### Must Do

1. Commit immediately after task/feature completion (with verification)
2. Push automatically after every commit
3. Use detailed commit messages with bullet points
4. Include verification status for code changes
5. Follow commit message format exactly
6. Verify commit and push succeeded

### Must Not Do

1. Ask for approval before commit/push
2. Commit incomplete tasks/features
3. Batch multiple tasks into one commit
4. Use forbidden git operations
5. Commit code without verification
6. Skip push after commit
7. Add agent attribution (no "Claude" in commits)

### Critical Violations (Zero Tolerance)

1. Committing code without verification
2. Committing code with failed verification
3. Missing verification status in code commits
4. Force push or destructive operations

### Corrective Action

For violations:
1. Stop immediately
2. Revert commit if needed
3. Run proper verification
4. Re-commit with correct format
5. Document in Learning Log

---

_Version: 1.0 - Last Updated: 2026-02-27_
