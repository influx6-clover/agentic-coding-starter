## Agent Instructions

### For Main Agent

**CRITICAL REMINDERS**:

1. **Read Agent Documentation**: Before starting work, read your agent documentation at `.agents/agents/main-agent.md` which specifies what skills and files you need.

2. **Autonomous Agent Behavior**: Work autonomously without unnecessary back-and-forth. Make informed decisions based on loaded context and instructions.

3. **Implementation Review First**:
   - **ALWAYS** start by reviewing current implementation status
   - Verify if reported issues are still pending or already resolved
   - Check PROGRESS.md, git history, and actual code state
   - Do NOT assume issues are unresolved without verification

4. **No Unnecessary Questions**:
   - If specification and features are already approved, they tell you what to do
   - Do NOT ask for clarification on items already clearly defined
   - Do NOT seek permission for implementation details covered in approved specs
   - Only ask questions when genuinely ambiguous or blocking

### For Sub-Agents (Implementation/Verification)

**CRITICAL REMINDERS**:

1. **Read Your Agent Documentation**:
   - **Implementation agents**: Read `.agents/agents/implementation-agent.md`
   - **Verification agents**: Read `.agents/agents/verification-agent.md`
   - Your documentation specifies what skills to load and files to read

2. **Read Required Context**:
   - **MUST READ** this requirements.md file for complete context
   - **MUST READ** fundamentals/* documentation if has_fundamentals: true
   - Read any skill files specified in metadata (e.g., skills from `.agents/skills/`)

3. **Autonomous Execution**:
   - Execute your assigned tasks without seeking unnecessary approval
   - Requirements are pre-approved - implement as specified
   - Make technical decisions within scope of your role and expertise

4. **Status Verification**:
   - Before starting, verify current state of assigned tasks
   - Check if work is partially complete or already done
   - Review recent commits and code changes related to your tasks

5. **Complete Your Scope**:
   - Focus ONLY on tasks assigned to you in requirements
   - Do NOT expand scope without explicit instruction
   - Update Tasks section and frontmatter counts as you progress
   - Mark tasks complete only when fully implemented and verified

---
