# Compact Context Transformation Example

This example demonstrates how Rule 15 creates ultra-compact context summaries
for context reload cycles with ~97% token reduction.

## Before Compaction: Full Context (180K tokens)

Agent has accumulated in context:
- Full requirements.md: 2,000 tokens
- Full PROGRESS.md with all historical progress: 5,000 tokens
- Full LEARNINGS.md with all insights: 3,000 tokens
- Multiple full file reads: 20,000 tokens
- Conversation history: 150,000 tokens
- **Total: ~180,000 tokens (90% of 200K limit)**

## After Compaction: COMPACT_CONTEXT.md (500 tokens - 97% reduction)

```markdown
# Compact Context: Implement DNS Resolver

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:2026-02-01T14:30:00Z|FROM:[machine_prompt.md,progress.md,rules]

## RULES_SUMMARY
rule:01|naming_structure|ref:[.agents/rules/01-*.md]
rule:03|danger_ops|safe:[git_status,git_diff]|forbidden:[force_push,reset_hard,no_verify]|ref:[.agents/rules/03-*.md]
rule:04|commit|verify_first|no_force_push|co_author:Claude|ref:[.agents/rules/04-*.md]
rule:13|impl|tdd|retrieval_first|doc_tests:WHY+WHAT|no_commit|ref:[.agents/rules/13-*.md]
rule:14|machine_prompt|58%_reduction|pipe_delimited|ref:[.agents/rules/14-*.md]
rule:15|compact_context|97%_reduction|embed_rules+machine_prompt|ref:[.agents/rules/15-*.md]
stack:[rust]|patterns:[Result<T>,trait_bounds,derive_more,no_unsafe]|ref:[.agents/stacks/rust.md]

## CURRENT_TASK
task:impl_dns_resolver|status:in_progress|started:2026-02-01T14:00:00Z

## MACHINE_PROMPT_CONTENT
spec:http-client|status:in-progress|priority:high|has_features:true
req:impl DnsResolver trait|cache:LRU,ttl=300s,max=1000|async:tokio|support:ipv4,ipv6
task:impl_dns_resolver|files:[src/dns_resolver.rs]|tests:[tests/dns_tests.rs]|deps:[lru_cache]
tech:stack=[rust,tokio]|pattern:async_trait|error_handling:Result<T>
verify:scripts=[verify_dns.py]|tests:unit,integration|coverage:>80%

## OBJECTIVE
Impl DnsResolver trait with LRU caching per embedded requirements

## FILES
read:[src/http_client.rs,src/lib.rs]|update:[src/dns_resolver.rs]|create:[tests/dns_tests.rs]

## KEY_CONSTRAINTS
1. async_only|tokio_runtime|no_blocking
2. cache_ttl:300s|max_entries:1000|eviction:LRU
3. ipv4_ipv6_support|error_propagation:Result

## BLOCKERS
NONE

## NEXT_ACTIONS
1. Impl DnsResolver trait|methods:[resolve_host,cache_lookup,clear_cache]
2. Add LRU cache|dep:[lru_cache=0.12]|config:[ttl,max_entries]
3. Write unit tests|coverage:>80%|test:[happy_path,cache_hit,cache_miss,eviction]

## CONTEXT_REFS
progress:[./PROGRESS.md#dns-resolver]|learnings:[./LEARNINGS.md#dns-caching]|docs:[documentation/http_client/doc.md#dns]

---
⚠️ AFTER READING THIS FILE: Clear context, reload from this file, proceed with fresh context
```

## After Context Reload: Fresh Start (5K tokens)

Agent has in context:
- COMPACT_CONTEXT.md: 500 tokens
- Only current task files: 3,000 tokens
- Current conversation: 1,500 tokens
- **Total: ~5,000 tokens (2.5% of limit)**

## Token Savings Analysis

| Phase | Tokens | % of Limit |
|-------|--------|------------|
| Before compaction | 180,000 | 90% |
| After compaction + reload | 5,000 | 2.5% |
| **Savings** | **175,000** | **87.5%** |
| **Reduction** | **97.2%** | |

## Key Compression Techniques Applied

1. **References over content**: Links to files instead of duplicating content
2. **Current work only**: No historical context, no future plans
3. **Embedded machine prompt**: Task requirements included directly
4. **Embedded rule summaries**: ~70K tokens saved vs loading full rule files
5. **Single sentence objective**: Maximum 15 words
6. **Pipe-delimited constraints**: Compact format
7. **File lists without content**: Read files separately after reload

## Context Reload Cycle

```
[Working with 180K context] →
[Generate COMPACT_CONTEXT.md - 500 tokens] →
[Clear entire context] →
[Read ONLY COMPACT_CONTEXT.md] →
[Read files from FILES section - 3K tokens] →
[Continue work with 5K tokens total] →
[Repeat cycle as needed]
```

## Key Insight: Embedded Content

**RULES_SUMMARY section** embeds essential rule guidance:
- Without: Agent loads 7 full rule files (~70K tokens)
- With: Compact summaries (~100 tokens)
- **Savings**: ~69,900 tokens

**MACHINE_PROMPT_CONTENT section** embeds task requirements:
- Without: Agent must re-read machine_prompt.md after reload
- With: All requirements embedded in compact file
- **Benefit**: Self-contained, no external dependencies

## Benefits

1. **Prevents context limit errors**: 90% → 2.5% usage
2. **Enables indefinite work sessions**: Reload cycle resets context
3. **Improves performance**: Clean context = faster processing
4. **Maintains focus**: Only current work visible
5. **Reduces costs**: Fewer input tokens

## When to Compact

- ✅ Before starting any new task
- ✅ After updating PROGRESS.md
- ✅ Every 50-100 agent turns
- ✅ When context exceeds 150K tokens (85% of limit)
- ✅ When switching tasks

See: `.agents/rules/15-instruction-compaction.md` for full specification
