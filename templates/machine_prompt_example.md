# Machine Prompt Transformation Example

This example demonstrates how Rule 14 compresses human-readable specifications
into machine-optimized prompts with ~60% token reduction.

## Before: requirements.md (450 tokens)

```markdown
## Requirements

### Functional Requirements

1. **HTTP Client Core Structure**
   - Must implement a basic HTTP/1.1 client
   - Should support GET, POST, PUT, DELETE methods
   - Must handle request/response lifecycle
   - Connection management with keep-alive support

2. **Error Handling**
   - Comprehensive error types for all failure modes
   - Clear error messages for debugging
   - Proper error propagation

### Technical Specifications

- **Stack**: Rust, Tokio async runtime, Hyper for HTTP
- **Location**: src/http_client.rs
- **Dependencies**: tokio, hyper, serde

### Tasks

- [ ] Task 1: Implement core HTTP client structure
  - Create HttpClient struct
  - Implement connection pooling
  - Add keep-alive support
  - Files to modify: src/http_client.rs, src/lib.rs
  - Tests: tests/http_client_tests.rs

- [ ] Task 2: Add method implementations
  - GET, POST, PUT, DELETE methods
  - Request builder pattern
  - Files: src/http_client.rs
  - Tests: tests/methods_tests.rs
```

## After: machine_prompt.md (180 tokens - 60% reduction)

```markdown
# Machine-Optimized Prompt: HTTP Client

⚠️GENERATED|DO_NOT_EDIT|REGENERATE_FROM:requirements.md|GENERATED:2026-02-01T12:00:00Z

## META
spec:http-client|status:in-progress|priority:high|has_features:true

## DOCS_TO_READ
requirements.md|documentation/http_client/doc.md|.agents/stacks/rust.md

## REQUIREMENTS
req1:impl basic HTTP/1.1 client|methods:[GET,POST,PUT,DELETE]|lifecycle:req/resp|conn:keep-alive
req2:error handling|types:comprehensive|messages:clear debug|propagation:proper

## TASKS
[ ]task1:impl core http client struct|files:[src/http_client.rs,src/lib.rs]|impl:[HttpClient,pool,keep-alive]|tests:[tests/http_client_tests.rs]
[ ]task2:add methods|methods:[GET,POST,PUT,DELETE]|pattern:builder|files:[src/http_client.rs]|tests:[tests/methods_tests.rs]

## TECHNICAL
stack:[rust,tokio,hyper]|loc:[src/http_client.rs]|deps:[tokio,hyper,serde]

## RETRIEVAL_CHECKLIST
search:http client impls|read:existing http code|check:async patterns|verify:error handling
```

## Token Savings Analysis

| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| Total tokens | 450 | 180 | 270 (60%) |
| Requirements section | 120 | 45 | 75 (63%) |
| Tasks section | 180 | 70 | 110 (61%) |
| Technical section | 80 | 25 | 55 (69%) |

## Key Compression Techniques Applied

1. **Pipe-delimited sections**: `req1:...|methods:[...]|lifecycle:...`
2. **Abbreviated terms**: `impl`, `req/resp`, `conn`
3. **Collapsed lists**: `[GET,POST,PUT,DELETE]` instead of bullet points
4. **Compact file references**: `files:[src/http_client.rs,src/lib.rs]`
5. **Removed unnecessary whitespace and formatting**
6. **Single-line tasks with embedded metadata**

## Agent Usage

Agents read `machine_prompt.md` instead of `requirements.md` for:
- 60% fewer tokens consumed per agent session
- Faster context loading
- More tokens available for code and reasoning
- Consistent structured format for parsing

Human-readable `requirements.md` remains the source of truth for:
- Human review and editing
- Detailed explanations and context
- Version control history
- Documentation purposes

See: `.agents/rules/14-machine-optimized-prompts.md` for full specification
