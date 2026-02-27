---
description: "[Brief description of what this specification implements]"
status: "in-progress"
priority: "medium"
created: YYYY-MM-DD
author: "Main Agent"
metadata:
  version: "1.0"
  last_updated: YYYY-MM-DD
  estimated_effort: "small | medium | large"
  tags:
    - tag1
    - tag2
  skills: []
  tools: []
has_features: true
has_fundamentals: false
builds_on: ""
related_specs: []
features:
  completed: 0
  uncompleted: [N]
  total: [N]
  completion_percentage: 0
---

# Overview

Brief description of what this specification implements and why.

## Goals

- Goal 1: Description
- Goal 2: Description
- Goal 3: Description

## Implementation Location

- Primary implementation: `[path/to/implementation]`
- Feature specifications: `specifications/[NN-spec-name]/features/*/feature.md`
- Documentation: `documentation/[module]/doc.md`

## Known Issues

None currently identified.

## Feature Index

The implementation is divided into features with clear dependencies. Each feature contains detailed requirements, tasks, and verification steps in its respective `feature.md` file.

**Implementation Guidelines:**
- Implement features in dependency order
- Each feature contains complete requirements and tasks
- Refer to individual feature.md files for detailed specifications

| #  | Feature | Description | Dependencies | Status |
|----|---------|-------------|--------------|--------|
| 0  | [feature-name](./features/feature-name/feature.md) | Brief description | None | ⬜ Pending |
| 1  | [another-feature](./features/another-feature/feature.md) | Brief description | 0 | ⬜ Pending |

Status Key: ⬜ Pending | 🔄 In Progress | ✅ Complete

## Requirements Conversation Summary

This specification was created through collaborative requirements gathering with the user, focusing on:
- Key decision 1
- Key decision 2
- Key decision 3

## High-Level Architecture

Brief description of the architectural approach:

1. **Layer 1**: Description
2. **Layer 2**: Description
3. **Layer 3**: Description

Each layer is implemented as a separate feature with clear dependencies.

# Success Criteria (Spec-Wide)

This specification is considered complete when:

## Functionality
- All features completed and verified (see Feature Index)
- [Specific functional requirement 1]
- [Specific functional requirement 2]

## Code Quality
- Zero warnings from linting tools
- Code formatting passes
- All unit and integration tests pass
- End-to-end integration tests demonstrate full feature interoperability

## Documentation
- Module documentation updated
- `LEARNINGS.md` captures design decisions and trade-offs
- `VERIFICATION.md` produced with all verification checks passing
- `REPORT.md` created documenting final implementation

## Module References

Agents implementing features should read these documentation files:
- `documentation/[module]/doc.md` - Module patterns and conventions

---

_Created: YYYY-MM-DD_
_Last Updated: YYYY-MM-DD_
_Structure: Feature-based (has_features: true)_
