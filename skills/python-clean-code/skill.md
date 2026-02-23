---
name: "Python Clean Code"
description: "Comprehensive Python development practices covering implementation, testing, Django, gRPC, and monorepo patterns"
approved: Yes
created: 2026-02-23
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-23"
  tags: [python, clean-code, best-practices, django, grpc, testing, async, monorepo]
tools: []
files:
  - implementation/skill.md: "Clean implementation patterns with proper documentation and error handling"
  - testing/skill.md: "Testing excellence with pytest and property-based testing"
  - async/skill.md: "Async/await and asyncio patterns for non-blocking I/O"
  - directory-and-configuration/skill.md: "Project setup, virtual environments, and configuration"
  - django/models/skill.md: "Django model patterns with base classes and query optimization"
  - django/configuration/skill.md: "Django configuration with django-configurations and multi-tenancy"
  - django/testing/skill.md: "Django testing with pytest, Factory-Boy, and Given/When/Then"
  - grpc/services/skill.md: "gRPC service implementation with authentication and error handling"
  - grpc/protobuf/skill.md: "Protocol buffer patterns with code generation and organization"
  - monorepo/skill.md: "Monorepo structure with UV workspace and shared utilities"
---

# Python Clean Code

## Overview

This skill consolidates comprehensive Python development practices into a modular structure. Each sub-skill focuses on a specific aspect of Python development, providing detailed guidance, examples, and best practices.

Whether you're setting up a new project, implementing features, writing tests, working with Django or gRPC, or managing a monorepo, this skill provides the foundational knowledge and patterns needed for clean, idiomatic Python development.

All sub-skills are approved and ready for use. Each can be read independently based on your current task.

## Which Sub-Skill Should I Read?

### Core Python Practices

| Task Type | Sub-Skill | Path |
|-----------|-----------|------|
| **Setting up a Python project** | Directory and Configuration | [`directory-and-configuration/skill.md`](directory-and-configuration/skill.md) |
| **Installing Python and tools** | Directory and Configuration | [`directory-and-configuration/skill.md`](directory-and-configuration/skill.md) |
| **Writing implementation code** | Clean Implementation | [`implementation/skill.md`](implementation/skill.md) |
| **Documenting code** | Clean Implementation | [`implementation/skill.md`](implementation/skill.md) |
| **Error handling patterns** | Clean Implementation | [`implementation/skill.md`](implementation/skill.md) |
| **Writing or reviewing tests** | Testing Excellence | [`testing/skill.md`](testing/skill.md) |
| **Property-based testing** | Testing Excellence | [`testing/skill.md`](testing/skill.md) |
| **Working with async/await** | Async Code | [`async/skill.md`](async/skill.md) |
| **Using asyncio** | Async Code | [`async/skill.md`](async/skill.md) |

### Django Framework

| Task Type | Sub-Skill | Path |
|-----------|-----------|------|
| **Django models and ORM** | Django Models | [`django/models/skill.md`](django/models/skill.md) |
| **Query optimization** | Django Models | [`django/models/skill.md`](django/models/skill.md) |
| **Django configuration** | Django Configuration | [`django/configuration/skill.md`](django/configuration/skill.md) |
| **Environment management** | Django Configuration | [`django/configuration/skill.md`](django/configuration/skill.md) |
| **Multi-tenancy patterns** | Django Configuration | [`django/configuration/skill.md`](django/configuration/skill.md) |
| **Django testing** | Django Testing | [`django/testing/skill.md`](django/testing/skill.md) |
| **Factory-Boy fixtures** | Django Testing | [`django/testing/skill.md`](django/testing/skill.md) |

### gRPC Services

| Task Type | Sub-Skill | Path |
|-----------|-----------|------|
| **Implementing gRPC services** | gRPC Services | [`grpc/services/skill.md`](grpc/services/skill.md) |
| **gRPC authentication** | gRPC Services | [`grpc/services/skill.md`](grpc/services/skill.md) |
| **Protocol buffer definitions** | gRPC Protobuf | [`grpc/protobuf/skill.md`](grpc/protobuf/skill.md) |
| **Protobuf code generation** | gRPC Protobuf | [`grpc/protobuf/skill.md`](grpc/protobuf/skill.md) |

### Monorepo

| Task Type | Sub-Skill | Path |
|-----------|-----------|------|
| **Monorepo organization** | Monorepo Structure | [`monorepo/skill.md`](monorepo/skill.md) |
| **UV workspace setup** | Monorepo Structure | [`monorepo/skill.md`](monorepo/skill.md) |
| **Shared utilities (ca-lib)** | Monorepo Structure | [`monorepo/skill.md`](monorepo/skill.md) |

## Sub-Skills Reference

### Core Practices

#### 1. Directory and Configuration
**Path**: [`directory-and-configuration/skill.md`](directory-and-configuration/skill.md)

Set up Python projects with proper structure, virtual environments, and tool configuration.

#### 2. Clean Implementation
**Path**: [`implementation/skill.md`](implementation/skill.md)

Write clean, well-documented Python code with proper error handling and type safety. Includes documentation patterns, error handling, security, and Pythonic patterns.

#### 3. Testing Excellence
**Path**: [`testing/skill.md`](testing/skill.md)

Write proper, clear tests that validate both valid and invalid inputs with explicit assertions. Covers pytest, property-based testing with Hypothesis, and Docker integration.

#### 4. Async Code
**Path**: [`async/skill.md`](async/skill.md)

Write robust async/await code using asyncio with proper non-blocking patterns. Covers event loops, task spawning, and concurrent programming.

### Django Framework

#### 5. Django Models
**Path**: [`django/models/skill.md`](django/models/skill.md)

Django model patterns with base classes, query optimization, and real database testing. Prevent N+1 queries and use proper ORM patterns.

#### 6. Django Configuration
**Path**: [`django/configuration/skill.md`](django/configuration/skill.md)

Django configuration patterns with django-configurations, environment management, and multi-tenancy support.

#### 7. Django Testing
**Path**: [`django/testing/skill.md`](django/testing/skill.md)

Django testing patterns with pytest, Factory-Boy, Given/When/Then structure, and 100% coverage requirement.

### gRPC Services

#### 8. gRPC Services
**Path**: [`grpc/services/skill.md`](grpc/services/skill.md)

gRPC service implementation patterns with authentication, error handling, and service registration.

#### 9. gRPC Protobuf
**Path**: [`grpc/protobuf/skill.md`](grpc/protobuf/skill.md)

Protocol buffer patterns with imports, code generation, and protobuf organization.

### Monorepo

#### 10. Monorepo Structure
**Path**: [`monorepo/skill.md`](monorepo/skill.md)

Monorepo organization with workspace configuration, shared utilities (ca-lib), and cross-service dependencies.

## How to Use This Skill

1. **Identify your task** - Use the tables above to determine which sub-skill applies
2. **Read the specific sub-skill** - Each sub-skill is complete and standalone
3. **Follow cross-references** - Sub-skills reference each other when topics overlap
4. **Check examples** - Each sub-skill has its own `examples/` directory with detailed guides

**Important**: This parent skill provides navigation only. The actual implementation guidance, examples, and patterns are in the individual sub-skills.

## Related Skills

For distributed systems patterns, see the Rust distributed systems skills.

---

**Usage Type**: EDUCATIONAL

This is a navigation skill. Load the specific sub-skills for actual implementation guidance.
