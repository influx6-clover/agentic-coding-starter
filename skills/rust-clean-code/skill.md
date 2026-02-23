---
name: "Rust Clean Code"
description: "Comprehensive Rust development practices covering implementation, testing, configuration, and async patterns"
approved: Yes
created: 2026-02-23
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-23"
  tags: [rust, clean-code, best-practices, testing, async, configuration]
tools: []
files:
  - implementation/skill.md: "Clean implementation patterns with proper documentation and error handling"
  - testing/skill.md: "Testing excellence with real code validation and property-based testing"
  - async/skill.md: "Async/await and Tokio patterns for non-blocking I/O"
  - directory-and-configuration/skill.md: "Project setup, toolchain installation, and configuration"
---

# Rust Clean Code

## Overview

This skill consolidates comprehensive Rust development practices into a modular structure. Each sub-skill focuses on a specific aspect of Rust development, providing detailed guidance, examples, and best practices.

Whether you're setting up a new project, implementing features, writing tests, or working with async code, this skill provides the foundational knowledge and patterns needed for clean, idiomatic Rust development.

All sub-skills are approved and ready for use. Each can be read independently based on your current task.

## Which Sub-Skill Should I Read?

Choose the appropriate sub-skill based on your current task:

| Task Type | Sub-Skill | Path |
|-----------|-----------|------|
| **Setting up a new Rust project** | Directory and Configuration | [`directory-and-configuration/skill.md`](directory-and-configuration/skill.md) |
| **Installing Rust toolchain** | Directory and Configuration | [`directory-and-configuration/skill.md`](directory-and-configuration/skill.md) |
| **Writing implementation code** | Clean Implementation | [`implementation/skill.md`](implementation/skill.md) |
| **Documenting code** | Clean Implementation | [`implementation/skill.md`](implementation/skill.md) |
| **Error handling patterns** | Clean Implementation | [`implementation/skill.md`](implementation/skill.md) |
| **Writing or reviewing tests** | Testing Excellence | [`testing/skill.md`](testing/skill.md) |
| **Property-based testing** | Testing Excellence | [`testing/skill.md`](testing/skill.md) |
| **Working with async/await** | Async Code | [`async/skill.md`](async/skill.md) |
| **Using Tokio runtime** | Async Code | [`async/skill.md`](async/skill.md) |
| **Non-blocking I/O patterns** | Async Code | [`async/skill.md`](async/skill.md) |

## Sub-Skills Reference

### 1. Directory and Configuration
**Path**: [`directory-and-configuration/skill.md`](directory-and-configuration/skill.md)

Install Rust toolchain, configure projects, and set up proper directory structure. Covers:
- Complete Rust toolchain installation
- Step-by-step project setup
- Cargo.toml and .cargo/config.toml configuration

### 2. Clean Implementation
**Path**: [`implementation/skill.md`](implementation/skill.md)

Write clean, well-documented Rust code with proper error handling and no_std/std support. Covers:
- WHY/WHAT/HOW documentation patterns
- Error handling with derive_more
- Security best practices
- Iterator and trait implementation patterns
- no_std compatibility

### 3. Testing Excellence
**Path**: [`testing/skill.md`](testing/skill.md)

Write proper, clear tests that validate both valid and invalid inputs with explicit assertions. Covers:
- Unit tests, integration tests, benchmarks
- Validating both valid AND invalid inputs
- Feature-gated test modules
- Property-based testing with proptest
- Docker and testcontainers for integration testing

### 4. Async Code
**Path**: [`async/skill.md`](async/skill.md)

Write robust async/await code using tokio with proper non-blocking patterns. Covers:
- Using tokio as async runtime
- Non-blocking I/O patterns
- Task spawning and coordination
- Avoiding blocking the event loop
- Async testing with proper isolation

## How to Use This Skill

1. **Identify your task** - Use the table above to determine which sub-skill applies
2. **Read the specific sub-skill** - Each sub-skill is complete and standalone
3. **Follow cross-references** - Sub-skills reference each other when topics overlap
4. **Check examples** - Each sub-skill has its own `examples/` directory with detailed guides

**Important**: This parent skill provides navigation only. The actual implementation guidance, examples, and patterns are in the individual sub-skills.

## Related Skills

- [`dst-tokio-rust`](../dst-tokio-rust/skill.md) - Distributed systems and Tokio patterns (builds on async sub-skill)

---

**Usage Type**: EDUCATIONAL

This is a navigation skill. Load the specific sub-skills for actual implementation guidance.
