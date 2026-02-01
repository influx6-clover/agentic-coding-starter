# Template Improvements Summary

## Overview
Enhanced specification and feature templates with better location awareness and navigation capabilities to reduce agent confusion and tool calls.

## Changes Made (2026-02-02)

### 1. Added Identification Section

**requirements-template.md**:
```yaml
# === IDENTIFICATION ===
spec_name: "[NN-spec-name]"  # e.g., "02-build-http-client"
spec_number: NN  # Two-digit number
description: Brief one-sentence description
```

**feature-template.md**:
```yaml
# === IDENTIFICATION ===
spec_name: "[NN-spec-name]"  # Parent spec
spec_number: NN  # Parent spec number
feature_name: "feature-name"  # This feature's name
feature_number: N  # Feature number within spec
description: Brief one-sentence description
```

**Benefits**:
- Agents immediately know which spec/feature they're working on
- Clear parent-child relationship in features
- Enables quick validation of correct file

### 2. Added Location Context Section

Both templates now include:
```yaml
# === LOCATION CONTEXT ===
# To find this file's location:
# 1. Run: bash pwd  (gets current working directory = CWD)
# 2. This file is at: CWD/specifications/[NN-spec-name]/...
# 3. Workspace root: CWD (contains .agents/, specifications/, documentation/, backends/)
workspace_name: "ewe_platform"
spec_directory: "specifications/[NN-spec-name]"
this_file: "specifications/[NN-spec-name]/requirements.md"
```

**Benefits**:
- Clear instructions on how to determine location
- Uses CWD placeholder instead of absolute paths
- Provides workspace context and structure
- Relative paths from workspace root

### 3. Added Location Reference Section (After Frontmatter)

Both templates now include a "📍 Location Reference" section with:

**Quick Paths**:
- Lists all relevant paths relative to workspace root
- Parent spec, features, machine prompts, progress, learnings
- Agent rules, stack files, documentation

**Verification Command**:
```bash
test -f .agents/AGENTS.md && echo "✓ In workspace root" || echo "✗ Wrong location"
```

**Quick Navigation Commands**:
- Verify workspace root
- List specs/features
- View structure with tree
- Find related code

**Benefits**:
- One-liner to verify correct location
- Ready-to-use navigation commands
- Reduces need for exploratory tool calls
- Agents can quickly validate they're in the right place

### 4. Organized Frontmatter Structure

Reorganized frontmatter into logical sections:
- `=== IDENTIFICATION ===` - What is this
- `=== LOCATION CONTEXT ===` - Where is this
- `=== STATUS ===` - Current state
- `=== CONTEXT OPTIMIZATION ===` - Token/context settings
- `=== METADATA ===` - Additional info
- `=== DEPENDENCIES ===` - Related specs/features
- `=== TASKS ===` - Task tracking

**Benefits**:
- Clear visual separation
- Easier to scan and find specific information
- Consistent organization across templates

## Impact

### Before
```
Agent: "Let me check where I am..."
→ Uses pwd
→ Uses ls to explore
→ Uses multiple Glob calls to find spec
→ Multiple Read calls to verify
→ 5-10 tool calls just to get oriented
```

### After
```
Agent: Reads frontmatter
→ spec_name: "02-build-http-client" ✓
→ this_file: "specifications/02-build-http-client/requirements.md" ✓
→ Runs verification command from template ✓
→ Immediately knows location and context
→ 1-2 tool calls total
```

## Reduction in Tool Calls

**Estimated savings per agent spawn**:
- Location discovery: 5-8 tool calls → 1-2 tool calls (70% reduction)
- Context validation: 3-5 tool calls → 1 tool call (80% reduction)
- Navigation: 2-4 tool calls → 0 tool calls (100% reduction - copy from template)

**Total**: ~60-70% reduction in orientation/navigation tool calls

## Usage

### For New Specifications
1. Copy `requirements-template.md` or `feature-template.md`
2. Replace `[NN-spec-name]`, `[feature-name]`, `NN`, `N` with actual values
3. Fill in identification and location fields
4. Proceed with requirements/feature content

### For Existing Specifications
- Consider updating active specs with new frontmatter structure
- Particularly beneficial for specs with multiple features
- Add location reference section for agent convenience

## Related Files
- `.agents/templates/requirements-template.md` - Updated requirements template
- `.agents/templates/feature-template.md` - Updated feature template
- `.agents/rules/06-specifications-and-requirements.md` - May need update to reflect new template structure

## Next Steps (Optional)

Consider adding:
1. **Workspace fingerprint** - Unique identifier for workspace to validate correct project
2. **Git branch tracking** - Spec-specific branch names for version control
3. **Related modules map** - Quick reference to code locations this spec modifies
4. **Agent spawn count** - Track how many agents have worked on this spec
5. **Estimated token usage** - Help agents understand context budget

---

*Created: 2026-02-02*
*Author: Main Agent*
