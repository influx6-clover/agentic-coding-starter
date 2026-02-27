# Agent Registry Usage (For Sub-Agents)

## Purpose

Concise guide for sub-agents spawned by Main Agent. For agent creation and documentation, Main Agent should load Rule 10.

## Sub-Agent Startup Protocol

### 1. Check for Documentation Path

Main Agent MUST provide your documentation path:

**If provided:**
```
Your documentation: .agents/agents/[name].md
```
→ Proceed to Step 2

**If missing:**
```
STOP: No agent documentation provided!

Request from Main Agent:
"I am [Agent Type] for [purpose].
 I need my documentation path: .agents/agents/[expected-name].md
 Cannot proceed without understanding my responsibilities, tools, workflow, and boundaries."
```

### 2. Read Your Documentation

1. Read documentation file FIRST
2. Understand capabilities, requirements, responsibilities, boundaries
3. Note required skills (check `.agents/skills/`)
4. Note required tools

### 3. Load Required Rules

1. Rules 01-04 (mandatory for all agents)
2. Rule 11 (if using skills)
3. Relevant stack file (`.agents/stacks/[language].md`)
4. Specification files (if provided)

### 4. Execute Your Work

Follow workflow documented in your agent documentation.

## Finding Your Documentation

Location: `.agents/agents/[your-agent-name].md`

Common files:
- `implementation.md` - Implementation agent
- `rust-verification.md` - Rust verification agent
- `javascript-verification.md` - JavaScript verification agent
- `python-verification.md` - Python verification agent
- `specification-update.md` - Specification update agent
- `review.md` - Pre-work review agent
- `documentation.md` - Documentation agent

## What Documentation Contains

| Section | What It Tells You |
|---------|-------------------|
| Frontmatter | Name, type, purpose, tools, skills |
| Overview | High-level description |
| Capabilities | What you can do |
| Requirements | Tools, skills, dependencies |
| Responsibilities | Your specific duties |
| Workflow | Step-by-step process |
| Boundaries | What you CANNOT do |
| Integration | How you work with other agents |

## Sub-Agent Boundaries

### Can Do
- Read and follow own documentation
- Execute documented workflow
- Use approved skills (per Rule 11)
- Report completion to Main Agent
- Request help when stuck

### Cannot Do
- Spawn verification agents (only Main Agent can)
- Spawn other agents directly (report need to Main Agent)
- Commit code directly (report to Main Agent)
- Exceed documented boundaries
- Proceed without documentation path
- Skip reading own documentation

## Requesting Additional Agents

If you need another agent:
1. DO NOT spawn directly
2. Report to Main Agent: "I need [type] agent for [purpose]. Reason: [why]. Blocker: [what you can't do]."
3. Wait for Main Agent to spawn and coordinate

## Reporting Completion

When work is complete:
```
Task completed:
- Files changed: [list]
- What implemented: [description]
- Specification: [if applicable]
- Learnings documented: [Yes/No]

Ready for Main Agent verification.
```

**CRITICAL**: Never commit directly. Always report to Main Agent.

## When Stuck

If you encounter issues:
1. Check your documentation for guidance
2. Check relevant rules (01-04 mandatory, others as needed)
3. Check skill documentation if using skills
4. Report to Main Agent with: what you're blocked on, what you tried, what you need

## Golden Rules for Sub-Agents

1. Always receive documentation path from Main Agent
2. Read your documentation FIRST before any work
3. Stay within boundaries defined in documentation
4. Never spawn agents directly - report needs to Main Agent
5. Never commit directly - report completion to Main Agent
6. Load only what you need: Rules 01-04 + Rule 11 (if skills) + stack + spec

---

_Version: 1.0 - Last Updated: 2026-02-27_
