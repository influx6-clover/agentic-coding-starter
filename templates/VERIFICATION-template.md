---
workspace_name: "ewe_platform"
spec_directory: "specifications/[NN-spec-name]"
this_file: "specifications/[NN-spec-name]/VERIFICATION.md"

created: YYYY-MM-DD
verification_status: FAIL
language: [language]
---

# Verification Report: [Specification Name]

## Read By

1. **[Implementation Agent]** reads this to understand what failed
2. **[Main Agent]** reads this to decide next steps

## Status: FAIL ❌

Date: YYYY-MM-DD
Language: [Language]

---

## Check Results

### 1. Incomplete Implementation Check: PASS ✅ / FAIL ❌
- TODO markers: [N] found
- FIXME markers: [N] found
- Unimplemented macros: [N] found
- Stub methods: [N] found

**Details** (if any found):
```
FILE: path/to/file.ext
- Line XX: // TODO: Description
- Line YY: fn stub() { Ok(()) }
```

### 2. Format Check: PASS ✅ / FAIL ❌
- Command: [format command]
- Result: [details]

### 3. Lint Check: PASS ✅ / FAIL ❌
- Command: [lint command]
- Warnings: [N]
- Details: [warnings]

### 4. Type Check: PASS ✅ / FAIL ❌
- Command: [type check command]
- Errors: [N]
- Details: [errors]

### 5. Tests: PASS ✅ / FAIL ❌
- Command: [test command]
- Total: [N], Passed: [N], Failed: [N]
- Details: [failures]

### 6. Build: PASS ✅ / FAIL ❌
- Command: [build command]
- Result: [details]

### 7. Standards Compliance: PASS ✅ / FAIL ❌
- Check 1: PASS/FAIL
- Check 2: PASS/FAIL

---

## Actions Required

**URGENT - Fix these issues:**

1. **Issue 1**
   - File: path/to/file.ext
   - Line: XX
   - Fix: Description

2. **Issue 2**
   - File: path/to/file.ext
   - Line: YY
   - Fix: Description

---

## Next Steps

1. Implementation Agent will fix all failures
2. Re-run verification
3. If PASS: Main Agent commits
4. If FAIL: Repeat

---

_Created: YYYY-MM-DD_
