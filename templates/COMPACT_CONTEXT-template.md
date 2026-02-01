# Compact Context: [Task Name]

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:[YYYY-MM-DDTHH:MM:SSZ]|FROM:[machine_prompt.md,progress.md,rules]

## LOCATION
workspace:[ewe_platform]|spec:[NN-spec-name]|num:[NN]|feature:[feature-name]|num:[N]
this:[specifications/NN-spec-name/features/feature-name/feature.md]
cwd:[bash pwd]|verify:[test -f .agents/AGENTS.md && echo ✓ || echo ✗]

## RULES_SUMMARY
[EMBEDDED COMPACTED RULES, STACK, AND SKILLS FROM SPECIFICATION FRONTMATTER - ONLY WHAT THIS AGENT TYPE NEEDS]

rule:01|naming_structure|ref:[.agents/rules/01-*.md]
rule:02|dir_policy|ref:[.agents/rules/02-*.md]
rule:03|danger_ops|safe:[git_status,git_diff]|forbidden:[force_push,reset_hard,no_verify]|ref:[.agents/rules/03-*.md]
rule:04|commit|verify_first|no_force_push|co_author:Claude|ref:[.agents/rules/04-*.md]
rule:13|impl|tdd|retrieval_first|doc_tests:WHY+WHAT|no_commit|ref:[.agents/rules/13-*.md]
rule:14|machine_prompt|58%_reduction|pipe_delimited|ref:[.agents/rules/14-*.md]
rule:15|compact_context|97%_reduction|embed_rules+machine_prompt|ref:[.agents/rules/15-*.md]
stack:[language]|patterns:[key_patterns]|ref:[.agents/stacks/language.md]
skills:[skill_name]|usage:[key_points]|ref:[.agents/skills/skill_name/]

## CURRENT_TASK
task:[task_name]|status:[in_progress/blocked/testing]|started:[YYYY-MM-DDTHH:MM:SSZ]

## MACHINE_PROMPT_CONTENT
[EMBEDDED CONTENT FROM machine_prompt.md FOR THIS SPECIFIC TASK ONLY]

spec:[spec_name]|status:[status]|priority:[priority]
req:[current_task_requirement]|constraints:[...]|success:[...]
task:[current_task_name]|files:[...]|tests:[...]|deps:[...]
tech:stack=[...]|pattern:[...]|error_handling:[...]
verify:scripts=[...]|tests:[...]|coverage:[...]

## OBJECTIVE
[Single sentence describing what you're doing RIGHT NOW - max 15 words]

## FILES
read:[file1.rs,file2.rs]|update:[file3.rs]|create:[file4.rs]|review:[doc.md]

## KEY_CONSTRAINTS
1. [Critical constraint affecting current work]
2. [Another critical constraint]
3. [Third constraint if applicable]

## BLOCKERS
[Current blockers if any - or "NONE"]

## NEXT_ACTIONS
1. [Immediate next step]
2. [Following step]
3. [Third step if needed]

## CONTEXT_REFS
progress:[./PROGRESS.md#current-section]|learnings:[./LEARNINGS.md#relevant-section]|docs:[documentation/module/doc.md#section]

---

⚠️ **AFTER READING THIS FILE**: Clear entire context, reload from this file only, proceed with fresh minimal context

---

## Instructions for Agent

**CRITICAL**: This file is self-contained. After context clear, read ONLY this file.

**Location Awareness**: The LOCATION section tells you exactly where you are. Run the verify
command to confirm correct workspace. Spec number (NN) and feature number (N) identify this work.

**Rules Summary**: The RULES_SUMMARY section contains compacted essential rules, stack files,
and skills from specification frontmatter. **MANDATORY**: Must include all three (rules, stack, skills).
You do NOT need to load full rule/stack/skill files after reload - only refer to them if you need
deeper detail (use ref links).

**Stack Files**: Language-specific patterns and conventions you must follow (e.g., Rust idioms).

**Skills**: Reusable capabilities you can invoke during work (e.g., testing, documentation).

**Machine Prompt Content**: The MACHINE_PROMPT_CONTENT section contains all requirements
for current task. You do NOT need to read machine_prompt.md separately after reload.

**Context Reload Protocol**:
1. Read this file completely
2. Clear ALL previous context (conversation history, file reads, rules, everything)
3. Reload ONLY from this compact file
4. Read ONLY files listed in FILES section
5. Follow references in CONTEXT_REFS as needed (not full reads)
6. If you need deeper rule details, use ref links in RULES_SUMMARY
7. Proceed with current task using minimal, focused context

**Context Size**: This file should be ~700-1000 tokens. Full context after reload: ~5K-10K tokens (vs 150K+ before compaction)

**Token Savings**:
- Rules embedding: ~70K tokens saved (vs loading 7 full rule files)
- Machine prompt embedding: ~1K tokens saved
- Total: ~98% context reduction

**Ephemeral Nature**:
- Generated fresh for each task
- Regenerated after PROGRESS.md updates
- Deleted when task completes
- Never accumulates history
- Always reflects "now" only

**When to Regenerate**:
- After updating PROGRESS.md (MANDATORY)
- Every 50-100 agent turns
- When context approaches 150K tokens (85% of limit)
- Before switching tasks
- Task status changes

**When to Delete**:
- Current task fully completes
- Moving to next task
- Specification work complete

**See**: Rule 15 (Instruction Compaction) for complete protocol
