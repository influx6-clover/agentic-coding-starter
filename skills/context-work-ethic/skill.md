---
name: "Context Work Ethic"
description: "Rules for managing context, staying focused, and being concise"
approved: Yes
created: 2026-03-02
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-03-02"
  tags: [context, optimization, efficiency, communication]
tools: []
files: []
---

# Context Work Ethic

## Purpose

ALL agents must follow these rules for efficient context usage and clear communication.

## Communication Style

### Be Concise
- Short, direct sentences
- Use bullet points (1.2.3)
- No verbose paragraphs
- Get to the point immediately

### Examples

❌ **BAD - Too wordy**:
```
I have successfully completed the implementation of the feature
and would like to inform you that all tests are now passing.
The verification process has been completed and everything
appears to be working as expected according to the specifications.
```

✅ **GOOD - Concise**:
```
Completed:
1. Feature implemented
2. All tests passing
3. Verification complete
```

## Context Management

### Monitor Token Usage
- Check token count during long tasks
- At 800K tokens (80%): regenerate context

### When to Regenerate

Regenerate context when:
1. Approaching 800K tokens
2. Complex multi-file work spanning hours
3. Before major new subtask
4. User requests refresh

### How to Regenerate

1. Write PROGRESS.md with:
   - What's done (bullet list)
   - Files modified (specific changes)
   - What's next (numbered steps)
   - Next immediate action

2. Update compacted.md with:
   - Current objective
   - Critical state (compressed)
   - Next 3-5 actions

3. Clear context, reload from files

4. Continue work

## Work Ethic

### Focus Rules
1. ONE task at a time
2. Finish before moving to next
3. Test after each change
4. No half-done work

### Progress Updates
1. Update PROGRESS.md frequently
2. Use bullet points only
3. Include file names and line numbers
4. List next actions clearly

### Reporting
1. Keep it short (5-10 bullets max)
2. Use checkmarks (✅ ❌)
3. Include counts (8/13 fixed)
4. State next action

## Examples

### Good Progress Report
```
## Fixed
✅ client.rs - 4 unwraps removed (lines 53,54,55,370)
✅ api.rs - 1 expect removed (line 324)

## Remaining
❌ request_redirect.rs - 5 expects (lines 292,347,349,350)

## Next
1. Fix line 292
2. Run tests
3. Move to next file
```

### Good Status Update
```
Progress: 8/13 unwraps fixed (62%)
Files done: client.rs, api.rs, request.rs
Next: Fix request_redirect.rs line 292
```

## Summary

**Remember**:
1. Be concise - bullet points only
2. Monitor context - regenerate at 800K
3. Update PROGRESS.md frequently
4. ONE task at a time
5. Test after each fix

---

_Version: 1.0 - Created: 2026-03-02_
