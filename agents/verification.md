---
name: "Verification Agent (Generic)"
type: "verification"
language: "language-agnostic"
purpose: "Define common verification workflow for all language-specific verification agents"
created: 2026-02-27
author: "Main Agent"
license: "MIT"
metadata:
  version: "2.0"
  last_updated: 2026-02-27
  complexity: "simple"
  tags: [verification, generic, base]
tools_required: [Bash, Read, Grep, Glob]
skills_required: [code-verification, language-standards]
spawned_by: [main-agent]
spawns: []
related_rules: [rule.md]
status: active
---

# Verification Agent - Generic Documentation

## Overview

This document defines the **common verification workflow** shared by ALL language-specific verification agents (Rust, JavaScript, Python, etc.).

**Language-Specific Agents:**
- [rust-verification.md](./rust-verification.md) - Rust verification
- [javascript-verification.md](./javascript-verification.md) - JavaScript/TypeScript verification
- [python-verification.md](./python-verification.md) - Python verification

## Skills to Read

1. **`.agents/skills/code-verification/skill.md`** - Complete verification workflow
2. **`.agents/skills/language-standards/skill.md`** - Stack file standards

## Verification Workflow

**All verification agents MUST:**
1. Run incomplete implementation check FIRST (mandatory)
2. Run user-specified scripts (if any)
3. Run standard language checks
4. Report PASS/FAIL to Main Agent

## Critical Rules

- ✅ ONLY Main Agent can spawn verification agents
- ✅ ONE agent per language per verification run
- ✅ ALL checks must pass (zero tolerance)
- ❌ NEVER skip incomplete implementation check
- ❌ NEVER commit code directly
- ❌ NEVER mark complete with TODO/FIXME

See `.agents/skills/code-verification/skill.md` for complete details.

---

_Version: 2.0 - Last Updated: 2026-02-27_
