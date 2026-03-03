---
name: "Rust Clean Implementation"
description: "Write clean, well-documented Rust code with proper error handling and no_std/std support"
approved: Yes
created: 2026-01-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "4.0-streamlined"
  last_updated: "2026-03-03"
tags:
  - rust
  - clean-code
  - documentation
  - error-handling
  - no_std
  - abstraction
files:
  - examples/documentation-patterns.md: "WHY/WHAT/HOW doc patterns with mandatory panic documentation"
  - examples/error-handling-guide.md: "Error handling with derive_more"
  - examples/security-guide.md: "Security best practices"
  - examples/iterator-patterns.md: "Iterator and trait implementation patterns"
  - examples/dependency-hierarchy.md: "Project first, stdlib second, external last - with examples"
  - examples/no-std-support.md: "Supporting both no_std and std environments"
  - examples/performance-tips.md: "Performance optimization patterns and benchmarking"
  - examples/trait-patterns.md: "Trait implementation best practices"
  - examples/basic-template.md: "Basic implementation template"
---

# Rust Clean Implementation

## When to Use This Skill

Read this skill when **implementing new Rust code** (not tests or async). For testing, see [rust-testing-excellence](../testing/skill.md). For async code, see [rust-with-async-code](../async/skill.md).

---

## 🎯 Core Principles (CRITICAL - Always Apply)

### 1. Dependency Hierarchy: Project → Stdlib → External 🚨

**MANDATORY:** Check what the project already has before adding dependencies.

```
1. Project modules/crates (FIRST - search codebase)
   ↓ Can't fulfill need?
2. Rust stdlib (SECOND - use std::* when possible)
   ↓ Can't fulfill need?
3. External crates (LAST RESORT - truly necessary)
```

**Quick check:**
```bash
# Search for existing types
rg "struct.*Http" --type rust
rg "enum.*Error" --type rust
```

📖 **Read when adding dependencies:** [`dependency-hierarchy.md`](examples/dependency-hierarchy.md) - Complete examples and decision process

### 2. Documentation: WHY/WHAT/HOW Pattern

**Every public item needs documentation:**

```rust
/// WHY: Validates user input to prevent injection attacks
///
/// WHAT: Checks that input contains only alphanumeric characters
///
/// HOW: Uses regex pattern `^[a-zA-Z0-9]+$`
///
/// # Errors
/// Returns `Error::InvalidInput` if input contains special characters
///
/// # Panics
/// Never panics
pub fn validate_input(input: &str) -> Result<(), Error> {
    // Implementation
}
```

**Mandatory sections:**
- ✅ WHY - Purpose and motivation
- ✅ WHAT - What it does (one sentence)
- ✅ HOW - How it works (algorithm/approach)
- ✅ Errors - Document all error cases
- ✅ Panics - Document panic conditions (or state "Never panics")

📖 **Read for complete patterns:** [`documentation-patterns.md`](examples/documentation-patterns.md)

### 3. Error Handling with derive_more

**Use `derive_more` for clean error types:**

```rust
use derive_more::{Display, Error, From};

#[derive(Debug, Display, Error, From)]
pub enum Error {
    #[display(fmt = "invalid input: {}", _0)]
    InvalidInput(String),

    #[display(fmt = "not found")]
    NotFound,

    #[from]
    Io(std::io::Error),
}
```

**Pattern:**
- Use `derive_more` for Display/Error/From
- Provide context in display messages
- Use `#[from]` for automatic conversions
- Always implement Debug

📖 **Read for complete guide:** [`error-handling-guide.md`](examples/error-handling-guide.md)

### 4. No_std Support (When Required)

**Pattern for libraries:**

```rust
#![cfg_attr(not(feature = "std"), no_std)]

#[cfg(not(feature = "std"))]
use core::{fmt, result};

#[cfg(feature = "std")]
use std::{fmt, result};
```

```toml
[features]
default = ["std"]
std = []
```

📖 **Read when implementing:** [`no-std-support.md`](examples/no-std-support.md) - Complete patterns and testing

---

## 📚 Implementation Patterns (Read When Needed)

### Security Best Practices

**When to read:** Before handling user input, crypto, or sensitive data

**Quick checklist:**
- [ ] Validate ALL user inputs
- [ ] Use `zeroize` for sensitive data
- [ ] Avoid `unsafe` unless absolutely necessary
- [ ] Document security assumptions

📖 [`security-guide.md`](examples/security-guide.md)

### Iterator and Trait Patterns

**When to read:** Implementing custom iterators or traits

**Quick example:**
```rust
impl Iterator for MyType {
    type Item = T;
    fn next(&mut self) -> Option<Self::Item> { }
}
```

📖 [`iterator-patterns.md`](examples/iterator-patterns.md) - Iterator implementations

📖 [`trait-patterns.md`](examples/trait-patterns.md) - Trait best practices

### Performance Optimization

**When to read:** After profiling shows hot spots

**Core rules:**
1. **Measure first** - Use criterion benchmarks
2. **Profile** - Use flamegraph
3. **Optimize hot paths** - Focus on frequent code
4. **Avoid premature optimization** - Clarity first

📖 [`performance-tips.md`](examples/performance-tips.md) - Complete patterns and benchmarking

---

## ✅ Implementation Checklist

Every new module/function must have:

- [ ] WHY/WHAT/HOW documentation
- [ ] Error types with `derive_more`
- [ ] Errors section in docs
- [ ] Panics section in docs (or "Never panics")
- [ ] Used project types before external deps
- [ ] Security considerations (for user input/sensitive data)
- [ ] Tests (see [testing skill](../testing/skill.md))

**Forbidden:**
- ❌ Undocumented public items
- ❌ Missing error documentation
- ❌ Adding external deps without checking project first
- ❌ `unwrap()`/`expect()` in library code (use `?`)
- ❌ Ignoring no_std support (if project supports it)

---

## 📖 When to Read Example Files

**Always check first:**
1. ⭐ [`dependency-hierarchy.md`](examples/dependency-hierarchy.md) - Before adding ANY dependency

**Read when you need to:**

2. **Documentation:** [`documentation-patterns.md`](examples/documentation-patterns.md) - WHY/WHAT/HOW patterns
3. **Error handling:** [`error-handling-guide.md`](examples/error-handling-guide.md) - derive_more examples
4. **Security:** [`security-guide.md`](examples/security-guide.md) - Input validation, crypto, unsafe
5. **No_std:** [`no-std-support.md`](examples/no-std-support.md) - Supporting both std and no_std
6. **Iterators:** [`iterator-patterns.md`](examples/iterator-patterns.md) - Custom iterator implementation
7. **Traits:** [`trait-patterns.md`](examples/trait-patterns.md) - Trait implementation patterns
8. **Performance:** [`performance-tips.md`](examples/performance-tips.md) - After profiling
9. **Template:** [`basic-template.md`](examples/basic-template.md) - Starting a new module

---

## 🔗 Related Skills

- [rust-testing-excellence](../testing/skill.md) - Writing tests
- [rust-with-async-code](../async/skill.md) - Async patterns
- [rust-directory-and-configuration](../directory-and-configuration/skill.md) - Project structure
