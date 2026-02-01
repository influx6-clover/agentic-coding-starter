#!/usr/bin/env python3
"""
Compact Context Generator

Generates ultra-compact instruction summaries from verbose progress/machine_prompt
files for context optimization and reload cycles.

Purpose: Reduce runtime context by 97% by preserving only critical information
for current work, embedding machine_prompt content and rule summaries.

Usage:
    python3 generate_compact_context.py <progress_file> <machine_prompt_file> [spec_frontmatter]

Example:
    python3 generate_compact_context.py PROGRESS.md machine_prompt.md
    # Creates COMPACT_CONTEXT.md in same directory

See: .agents/rules/15-instruction-compaction.md for full specification
"""

from pathlib import Path
from datetime import datetime
import yaml


def generate_compact_context(
    progress_md: str,
    machine_prompt_md: str,
    spec_frontmatter: dict,
    agent_type: str,
    current_files: list
) -> str:
    """
    Generate ultra-compact context from verbose sources.

    CRITICAL: Embeds BOTH rule summaries AND machine_prompt.md content for current task.
    After context reload, agent reads ONLY this file (self-contained).

    Preserve ONLY what's needed for immediate work.
    Everything else becomes a reference.

    Token Savings: 97% reduction (180K → 5K tokens)
    """

    # Extract current task (not past, not future)
    current_task = extract_current_task(progress_md)

    # Extract and compact rules from frontmatter
    rules_summary = compact_rules_from_frontmatter(spec_frontmatter, agent_type)

    # Extract machine_prompt content for THIS TASK ONLY
    machine_content = extract_task_from_machine_prompt(machine_prompt_md, current_task['id'])

    # Single sentence objective
    objective = summarize_objective(current_task, max_words=15)

    # File lists (no content)
    files_to_read = [f for f in current_files if needs_reading(f)]
    files_to_update = [f for f in current_files if needs_updating(f)]
    files_to_create = [f for f in current_files if needs_creation(f)]

    # Extract only critical constraints
    constraints = extract_critical_constraints(machine_content, max_items=3)

    # Current blockers (or NONE)
    blockers = extract_active_blockers(progress_md) or "NONE"

    # Next 1-3 immediate actions
    next_actions = extract_next_actions(progress_md, max_items=3)

    # References (not content)
    refs = {
        'machine_prompt': find_task_section(machine_prompt_md, current_task['id']),
        'progress': './PROGRESS.md',
        'learnings': find_relevant_learnings(current_task),
    }

    compact = f"""# Compact Context: {current_task['name']}

⚠️COMPACTED|RELOAD_AFTER_READING|GENERATED:{timestamp()}|FROM:[machine_prompt.md,progress.md,rules]

## RULES_SUMMARY
{rules_summary}

## CURRENT_TASK
task:{current_task['name']}|status:{current_task['status']}|started:{current_task['started']}

## MACHINE_PROMPT_CONTENT
{machine_content}

## OBJECTIVE
{objective}

## FILES
read:[{','.join(files_to_read)}]|update:[{','.join(files_to_update)}]|create:[{','.join(files_to_create)}]

## REQUIREMENTS_REF
machine_prompt:[{refs['machine_prompt']}]|progress:[{refs['progress']}]

## KEY_CONSTRAINTS
{format_constraints(constraints)}

## BLOCKERS
{blockers}

## NEXT_ACTIONS
{format_actions(next_actions)}

## CONTEXT_REFS
progress:[{refs['progress']}]|learnings:[{refs['learnings']}]

---
⚠️ AFTER READING THIS FILE: Clear context, reload from this file, proceed with fresh context
"""

    return compact


def extract_task_from_machine_prompt(machine_prompt: str, task_id: str) -> str:
    """
    Extract ONLY the current task content from machine_prompt.md.

    Returns compressed task requirements, constraints, verification.
    This content is embedded in COMPACT_CONTEXT.md.
    """
    # Parse machine_prompt.md
    # Find task with task_id
    # Extract: requirements, constraints, files, tests, verification
    # Return compressed format for embedding
    pass


def compact_rules_from_frontmatter(spec_frontmatter: dict, agent_type: str) -> str:
    """
    Compact rules, stack files, and skills from specification frontmatter for specific agent type.

    Returns ultra-compact summaries with references for rules, stack, and skills.
    Avoids need to load full files after context reload.

    MANDATORY: Must include rules, stack files, AND skills.

    Token Savings: ~70K tokens (vs loading full rule/stack/skill files)

    Example output:
        rule:01|naming_structure|ref:[.agents/rules/01-*.md]
        rule:03|danger_ops|safe:[git_status,git_diff]|forbidden:[force_push,reset_hard]|ref:[.agents/rules/03-*.md]
        rule:13|impl|tdd|retrieval_first|doc_tests:WHY+WHAT|ref:[.agents/rules/13-*.md]
        stack:[rust]|patterns:[Result<T>,trait_bounds,no_unsafe]|ref:[.agents/stacks/rust.md]
        skills:[skill_name]|usage:[key_points]|ref:[.agents/skills/skill_name/]
    """
    rules_list = spec_frontmatter.get('files_required', {}).get(agent_type, {}).get('rules', [])
    skills_list = spec_frontmatter.get('files_required', {}).get(agent_type, {}).get('skills', [])

    compacted_rules = []

    # Compact rules and stack files
    for rule_path in rules_list:
        # Extract rule number/name from path
        rule_name = extract_rule_name(rule_path)  # e.g., "01", "03", "13", "rust"

        # Compact based on rule type
        if rule_name == "01":
            compacted_rules.append(f"rule:01|naming_structure|ref:[{rule_path}]")
        elif rule_name == "02":
            compacted_rules.append(f"rule:02|dir_policy|ref:[{rule_path}]")
        elif rule_name == "03":
            compacted_rules.append(f"rule:03|danger_ops|safe:[git_status,git_diff]|forbidden:[force_push,reset_hard,no_verify]|ref:[{rule_path}]")
        elif rule_name == "04":
            compacted_rules.append(f"rule:04|commit|verify_first|no_force_push|co_author:Claude|ref:[{rule_path}]")
        elif rule_name == "05":
            compacted_rules.append(f"rule:05|orchestration|main_delegates|spawn_sub_agents|verify_required|ref:[{rule_path}]")
        elif rule_name == "06":
            compacted_rules.append(f"rule:06|specs|retrieval_led|has_features:load_feature_md|ref:[{rule_path}]")
        elif rule_name == "08":
            compacted_rules.append(f"rule:08|verification|cargo_test|cargo_clippy|cargo_fmt|ref:[{rule_path}]")
        elif rule_name == "13":
            compacted_rules.append(f"rule:13|impl|tdd|retrieval_first|doc_tests:WHY+WHAT|no_commit|ref:[{rule_path}]")
        elif rule_name == "14":
            compacted_rules.append(f"rule:14|machine_prompt|58%_reduction|pipe_delimited|ref:[{rule_path}]")
        elif rule_name == "15":
            compacted_rules.append(f"rule:15|compact_context|97%_reduction|embed_rules+machine_prompt|ref:[{rule_path}]")
        elif "rust" in rule_name:
            compacted_rules.append(f"stack:[rust]|patterns:[Result<T>,trait_bounds,derive_more,no_unsafe]|ref:[{rule_path}]")
        # Add more rule compaction patterns as needed

    # Compact skills
    for skill_path in skills_list:
        skill_name = extract_skill_name(skill_path)
        # Read skill frontmatter to get key usage points
        # For now, provide a generic template
        compacted_rules.append(f"skills:[{skill_name}]|usage:[see_skill_doc]|ref:[{skill_path}]")

    return '\n'.join(compacted_rules)


def extract_current_task(progress_md: str) -> dict:
    """Extract ONLY current task, ignore completed/future."""
    # Parse PROGRESS.md
    # Find section marked "Current Task" or "In Progress"
    # Return task details
    pass


def summarize_objective(task: dict, max_words: int) -> str:
    """Single sentence, max_words limit."""
    # Take task description
    # Compress to essential action + target
    # Return concise sentence
    pass


def extract_critical_constraints(machine_prompt: str, max_items: int) -> list:
    """Only constraints affecting current task."""
    # Parse machine_prompt
    # Filter to current task constraints
    # Return top max_items most critical
    pass


def extract_active_blockers(progress_md: str) -> str:
    """Extract current blockers from progress file."""
    pass


def extract_next_actions(progress_md: str, max_items: int) -> list:
    """Extract next immediate actions."""
    pass


def find_task_section(machine_prompt: str, task_id: str) -> str:
    """Find section reference for specific task."""
    pass


def find_relevant_learnings(task: dict) -> str:
    """Find learnings relevant to current task."""
    pass


def format_constraints(constraints: list) -> str:
    """Format constraints as numbered list."""
    return '\n'.join(f"{i}. {c}" for i, c in enumerate(constraints, 1))


def format_actions(actions: list) -> str:
    """Format actions as numbered list."""
    return '\n'.join(f"{i}. {a}" for i, a in enumerate(actions, 1))


def extract_skill_name(skill_path: str) -> str:
    """Extract skill name from path."""
    # Example: ".agents/skills/testing/" -> "testing"
    # Example: ".agents/skills/documentation/skill.md" -> "documentation"
    parts = skill_path.strip('/').split('/')
    if 'skills' in parts:
        idx = parts.index('skills')
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return "unknown"


def needs_reading(file_path: str) -> bool:
    """Determine if file needs reading."""
    pass


def needs_updating(file_path: str) -> bool:
    """Determine if file needs updating."""
    pass


def needs_creation(file_path: str) -> bool:
    """Determine if file needs creation."""
    pass


def extract_rule_name(rule_path: str) -> str:
    """Extract rule number/name from path."""
    # Extract from path like ".agents/rules/13-implementation-agent-guide.md"
    import re
    match = re.search(r'/(\d+)-', rule_path)
    if match:
        return match.group(1)
    if 'rust' in rule_path.lower():
        return 'rust'
    return ''


def timestamp() -> str:
    """Generate ISO 8601 timestamp."""
    return datetime.utcnow().isoformat() + 'Z'


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python3 generate_compact_context.py <progress_file> <machine_prompt_file>")
        sys.exit(1)

    progress_path = Path(sys.argv[1])
    machine_prompt_path = Path(sys.argv[2])

    if not progress_path.exists():
        print(f"Error: {progress_path} does not exist")
        sys.exit(1)
    if not machine_prompt_path.exists():
        print(f"Error: {machine_prompt_path} does not exist")
        sys.exit(1)

    progress_content = progress_path.read_text()
    machine_prompt_content = machine_prompt_path.read_text()

    # Load spec frontmatter if available
    spec_frontmatter = {}
    agent_type = "implementation_agent"
    current_files = []

    output = generate_compact_context(
        progress_content,
        machine_prompt_content,
        spec_frontmatter,
        agent_type,
        current_files
    )

    output_path = progress_path.parent / "COMPACT_CONTEXT.md"
    output_path.write_text(output)

    print(f"✓ Generated: {output_path}")
    print("⚠️  Clear context and reload from COMPACT_CONTEXT.md")
