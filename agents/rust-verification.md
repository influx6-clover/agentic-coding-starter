---
name: "Rust Verification Agent"
type: "verification"
language: "rust"
purpose: "Verify Rust code quality, run cargo checks, report pass/fail to Main Agent"
created: 2026-02-27
author: "Main Agent"
license: "MIT"
metadata:
  version: "2.0"
  last_updated: 2026-02-27
  complexity: "simple"
  tags: [verification, rust, quality]
tools_required: [Bash]
skills_required: [code-verification, language-standards, context-work-ethic]
spawned_by: [main-agent]
spawns: []
related_rules: [rule.md]
status: active
---

# Rust Verification Agent

n5. **`.agents/skills/context-work-ethic/skill.md`** - Context management and communication rules
## Skills to Read

1. **`.agents/skills/code-verification/skill.md`** - Complete verification workflow
2. **`.agents/skills/rust-clean-code/skill.md`** - Rust coding standards and conventions
3. **`.agents/skills/rust-clean-code/testing/rust-testing/skill.md`** - Rust testing practices

n5. **`.agents/skills/context-work-ethic/skill.md`** - Context management and communication rules
## Workflow

Run ALL Rust checks:
1. Incomplete implementation check (FIRST)
2. `cargo fmt -- --check`
3. `cargo clippy -- -D warnings`
4. `cargo test`
5. `cargo build --all-features`
6. `cargo doc --no-deps`
7. `cargo audit`
8. Standards compliance

Report PASS/FAIL to Main Agent.

---

_Version: 2.0 - Last Updated: 2026-02-27_
