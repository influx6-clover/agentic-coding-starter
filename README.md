# Agentic Coding Framework

> **A structured approach to AI-assisted software development that ensures consistency, quality, and predictability.**

This directory contains the complete framework for guiding AI coding agents (like Claude Code, Cursor, Windsurf, etc.) through your software development process. It defines HOW agents work, HOW code should be written, and WHAT should be built.

## 🎯 What is This?

The Agentic Coding Framework is a set of guidelines, skills, and standards that:

- **Standardizes** how AI agents interact with your codebase
- **Enforces** coding standards and best practices automatically
- **Orchestrates** complex workflows between specialized agents
- **Verifies** that all changes meet quality standards before commits
- **Tracks** features, tasks, and requirements systematically
- **Learns** from mistakes through documented learning logs

Think of it as a "Constitution" for AI agents working on your project - a comprehensive framework that ensures every agent follows the same processes, standards, and workflows.

## 🏗️ Framework Structure

```
.agents/
├── README.md              # This file - framework overview
├── AGENTS.md              # Entry point - agents MUST read this first
│
├── agents/                # Agent documentation
│   ├── main-agent.md
│   ├── implementation.md
│   ├── rust-verification.md
│   └── ...                # Other agent types
│
├── skills/                # Reusable workflows and expertise
│   ├── main-agent-orchestration/
│   ├── implementation-practices/
│   ├── test-driven-development/
│   ├── code-verification/
│   ├── rust-clean-code/
│   ├── python-clean-code/
│   └── ...                # Language-specific and domain skills
│
└── templates/             # File templates for specifications, features, etc.
    ├── START-template.md
    ├── REQUIREMENTS-template.md
    ├── FEATURE-template.md
    └── examples/          # Reference examples
```

### Directory Purposes

| Directory | Purpose | Agent Usage |
|-----------|---------|-------------|
| **`AGENTS.md`** | Entry point with agent registry | Read FIRST at session start |
| **`agents/`** | Agent documentation (roles, workflows, skills) | Read YOUR agent file |
| **`skills/`** | Reusable workflows, practices, and language standards | Read as specified by agent docs |
| **`templates/`** | File templates and examples | Use when creating specs/features |

## 🚀 Getting Started

### For New Projects

You can bootstrap a new project with this framework in minutes:

1. **Clone the starter repository as your `.agents` directory:**
   ```bash
   cd your-project-root
   git clone https://github.com/ewe-studios/agentic-coding-starter .agents
   ```

2. **Remove the `.agents/.git` directory to make it part of your repository:**
   ```bash
   rm -rf .agents/.git
   ```

3. **Add it to your repository:**
   ```bash
   git add .agents
   git commit -m "Add agentic coding framework

   Initialized .agents directory with framework for AI-assisted development.

   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
   ```

4. **Create a `CLAUDE.md` redirect file in your project root:**
   ```bash
   cat > CLAUDE.md << 'EOF'
   # Claude AI Agent Configuration

   ## Primary Rule

   **MANDATORY:** Before performing any tasks, you **MUST**:

   1. **Load `.agents/AGENTS.md`** - Central configuration entry point
   2. **Follow all instructions** in `.agents/AGENTS.md`

   ---

   👉 **Go to [`.agents/AGENTS.md`](./.agents/AGENTS.md)** to get started.
   EOF
   ```

5. **Customize for your project:**
   - Edit `.agents/skills/*-clean-code/skill.md` to match your language preferences
   - Customize agent documentation in `.agents/agents/`
   - Create your first specification using templates in `.agents/templates/`

### For Existing Projects

If you already have an `.agents` directory, you can update it:

```bash
# Backup your current .agents directory
mv .agents .agents.backup

# Clone the latest framework
git clone https://github.com/ewe-studios/agentic-coding-starter .agents
rm -rf .agents/.git

# Merge your specifications and customizations
cp -r .agents.backup/specifications/* .agents/specifications/ 2>/dev/null
# (Review and merge other customizations manually)

# Clean up
rm -rf .agents.backup
```

## 📋 How It Works

### 1. Agent Loading Sequence

When an AI agent starts working on your project, it MUST:

1. **Read `AGENTS.md`** - Identifies which agent type it is
2. **Read agent documentation** - Loads agent-specific file (e.g., `.agents/agents/implementation.md`)
3. **Load required skills** - Reads skills specified in agent documentation
4. **Read specification files** - When working on features (requirements.md, start.md, etc.)

This ensures every agent has the same context and follows the same processes.

### 2. Agent Orchestration Model

The framework uses a **hierarchical agent model**:

- **Main Agent**: Orchestrator only - delegates all work, never codes directly
- **Implementation Agents**: Specialized workers for writing code
- **Verification Agents**: Run tests and checks before commits (language-specific)
- **Specification Update Agent**: Updates requirements and task tracking

**Example workflow:**
```
User: "Add user authentication"
  ↓
Main Agent: Analyzes requirement, creates specification
  ↓
Main Agent: Spawns Implementation Agent
  ↓
Implementation Agent: Writes authentication code (TDD), reports back
  ↓
Main Agent: Spawns Verification Agent
  ↓
Verification Agent: Runs tests, linting, builds
  ↓
Main Agent: Spawns Specification Agent
  ↓
Specification Agent: Updates progress.md with completion
  ↓
Main Agent: Creates commit and pushes
```

### 3. Zero-Commit Without Verification

**NO CODE IS COMMITTED WITHOUT VERIFICATION.**

The framework enforces:
- All tests must pass
- All linters must pass
- All builds must succeed
- All checks must complete
- No incomplete implementations (TODO, FIXME, stub methods)

If verification fails:
- A `VERIFICATION.md` report is created
- Issues are documented
- Code is NOT committed until fixed

### 4. Specification-Driven Development

Every feature starts with a specification:

```markdown
specifications/
└── 01-user-authentication/
    ├── start.md            # Agent workflow entry point
    ├── requirements.md     # What to build and why
    ├── LEARNINGS.md        # Discoveries and gotchas
    ├── progress.md         # Task checklist with progress
    └── VERIFICATION.md     # Failure reports (if any, temporary)
```

This ensures:
- Clear requirements before coding starts
- Trackable progress throughout implementation
- Documentation of what was built and why

## 🎓 Core Principles

1. **Orchestration Always** - Main Agent delegates, never implements
2. **Verification Required** - No commits without passing checks
3. **Test-Driven Development** - Write test first, one at a time
4. **ONE Item at a Time** - One test, one function, one file at a time
5. **Retrieval-Led Reasoning** - Read codebase first, follow discovered patterns
6. **Skills-Based Architecture** - Reusable workflows in skills, not duplicated
7. **Context Optimization** - Use compacted.md for 90% token reduction
8. **Learning Logs** - Document mistakes and patterns for improvement
9. **Specification-Driven** - Every feature has clear requirements
10. **Safety First** - Dangerous operations require explicit approval

## 🔧 Customization

### Adding Language-Specific Skills

Create new language skill directories:

```bash
.agents/skills/golang-clean-code/
├── skill.md           # Language standards and patterns
└── LEARNINGS.md       # Language-specific discoveries
```

Follow the structure in existing language skills (rust-clean-code, python-clean-code).

### Creating Custom Skills

When agents encounter knowledge gaps, they can create skills:

```bash
.agents/skills/kubernetes-deployment/
├── skill.md           # Documented knowledge
└── scripts/           # Optional helper scripts
    └── deploy.sh
```

Skills must be approved before use (see `.agents/skills/skills-management/skill.md`).

### Adding Custom Agents

Create new agent documentation:

```bash
.agents/agents/my-custom-agent.md
```

Follow the template in `.agents/templates/AGENT-DOCUMENTATION-template.md`.

## 📚 Key Documents

| Document | Purpose | Read When |
|----------|---------|-----------|
| **AGENTS.md** | Entry point with agent registry | Every session start |
| **agents/main-agent.md** | Main agent orchestration workflow | If you're Main Agent |
| **agents/implementation.md** | Implementation agent workflow | If you're Implementation Agent |
| **skills/git-workflow/skill.md** | Commit and push requirements | Before any commit |
| **skills/test-driven-development/skill.md** | TDD workflow (one test at a time) | Before writing code |
| **skills/code-verification/skill.md** | Complete verification guide | Before verification |
| **skills/[language]-clean-code/skill.md** | Language-specific standards | Before writing code in that language |

## 🤝 Contributing to the Framework

The framework is open source and welcomes contributions:

1. **Report Issues**: Found a problem? Open an issue on GitHub
2. **Suggest Improvements**: Have ideas? Create a discussion
3. **Submit Pull Requests**: Improvements welcome!
4. **Share Learning Logs**: Help others avoid common mistakes

Repository: https://github.com/ewe-studios/agentic-coding-starter

## 🆘 Troubleshooting

### Agent Not Following Guidelines

**Problem**: Agent ignores standards or skips verification

**Solution**:
1. Check that `CLAUDE.md` or similar redirect exists in project root
2. Verify agent loaded `AGENTS.md` at session start
3. Ask agent to identify itself: "Read AGENTS.md and tell me which agent you are"
4. Explicitly remind agent: "Please read your agent documentation and required skills"

### Verification Failures

**Problem**: Tests fail, builds break, linting errors

**Solution**:
1. Check `VERIFICATION.md` in specification directory for details
2. Review language skill file for correct verification commands
3. Ensure all dependencies are installed
4. Check that verification workflow is defined correctly

### Missing Language Skill

**Problem**: No skill file for your language

**Solution**:
1. Copy an existing language skill as template (e.g., rust-clean-code)
2. Customize for your language's conventions
3. Define verification workflow (test/lint/build commands)
4. Add LEARNINGS.md section for future improvement

## 📖 Further Reading

- **[AGENTS.md](./AGENTS.md)** - Start here! Entry point for all agents
- **[skills/README.md](./skills/README.md)** - Available skills and usage patterns
- **[templates/START-template.md](./templates/START-template.md)** - Specification workflow
- **[skills/main-agent-orchestration/skill.md](./skills/main-agent-orchestration/skill.md)** - Complete orchestration guide
- **[skills/implementation-practices/skill.md](./skills/implementation-practices/skill.md)** - Implementation best practices

## 📜 License

This framework is released under the MIT License. See the starter repository for details.

## 🙏 Credits

Developed by [Ewe Studios](https://github.com/ewe-studios) for consistent, high-quality AI-assisted software development.

---

**Version**: 6.0.0
**Last Updated**: 2026-02-27
**Repository**: https://github.com/ewe-studios/agentic-coding-starter

---

> **Remember**: This framework is a living document. As you learn better practices, update your agent docs, skills, and templates. The AI agents will benefit from every improvement you make.
