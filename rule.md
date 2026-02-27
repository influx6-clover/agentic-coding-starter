# Agent Rules

## Core Principle

**Every agent reads their documentation file which specifies skills to load.**

## Agent Registry

1. **[Main Agent]** read `.agents/agents/main-agent.md`
2. **[Implementation Agent]** read `.agents/agents/implementation.md`
3. **[Rust Verification Agent]** read `.agents/agents/rust-verification.md`
4. **[JavaScript Verification Agent]** read `.agents/agents/javascript-verification.md`
5. **[Python Verification Agent]** read `.agents/agents/python-verification.md`
6. **[Generic Verification Agent]** read `.agents/agents/verification.md`
7. **[Specification Update Agent]** read `.agents/agents/specification-update.md`
8. **[Review Agent]** read `.agents/agents/review.md`
9. **[Documentation Agent]** read `.agents/agents/documentation.md`
10. **[Rust Cleanup Agent]** read `.agents/agents/rust-cleanup.md`

## For Sub-Agents

Main Agent provides documentation path when spawning. If not provided, request it.

---

_Version: 1.0 - Last Updated: 2026-02-27_
