---
name: "JavaScript/TypeScript Verification Agent"
type: "verification"
language: "javascript"
purpose: "Verify JavaScript/TypeScript code quality, run tests, check formatting, linting, type checking, and standards"
created: 2026-02-27
author: "Main Agent"
license: "MIT"
metadata:
  version: "2.0"
  last_updated: 2026-02-27
  complexity: "simple"
  tags: [verification, javascript, typescript, quality]
tools_required: [Bash]
skills_required: [code-verification, language-standards]
spawned_by: [main-agent]
spawns: []
related_rules: [rule.md]
status: active
---

# JavaScript/TypeScript Verification Agent

## Skills to Read

1. **`.agents/skills/code-verification/skill.md`** - Complete verification workflow

## Workflow

Run ALL JavaScript/TypeScript checks:
1. Incomplete implementation check (FIRST)
2. `npx prettier --check .`
3. `npx tsc --noEmit`
4. `npx eslint . --max-warnings 0`
5. `npm test`
6. `npm run build`
7. `npm audit`
8. Standards compliance

Report PASS/FAIL to Main Agent.

---

_Version: 2.0 - Last Updated: 2026-02-27_
