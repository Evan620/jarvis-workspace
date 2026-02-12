# Fix Button Workflow - Easy Corrections Guide

## Overview
The "Fix Button" is a simple, conversational way to correct mistakes in the JARVIS system without manual file editing. Say "Fix [what]" and JARVIS handles it.

---

## How It Works

### User Side
Just say:
```
Fix [what needs correction]
```

Examples:
- "Fix that memory item - it's a task not a reference"
- "Fix the classification - it's personal not work"
- "Fix the next action deadline - it's due tomorrow not today"

### JARVIS Side
1. **Understand**: Parse what needs fixing
2. **Locate**: Find the relevant entry (memory, task, session log)
3. **Correct**: Apply the fix automatically
4. **Confirm**: Show what changed and why
5. **Log**: Record the fix in session log

---

## Common Fix Scenarios

### Fix #1: Wrong Tag Classification

**User says:**
```
Fix that - it's a task not a reference
```

**JARVIS does:**
```python
1. Scan session-logs/today.md for recent #reference entries
2. Find the likely candidate (based on context)
3. Change #reference → #task
4. Add [[next-action: ... | priority: medium | due: This week]]
5. Confirm: "Updated 'X' from #reference to #task with next action"
6. Log: "[FIX] Changed tag for 'X' entry"
```

---

### Fix #2: Wrong Context Tag

**User says:**
```
Fix the context - it's personal not work
```

**JARVIS does:**
```python
1. Find the entry with wrong @work tag
2. Change @work → @personal
3. Confirm: "Updated 'X' context from @work to @personal"
4. Log: "[FIX] Changed context for 'X' entry"
```

---

### Fix #3: Incorrect Next Action

**User says:**
```
Fix the next action - it's due tomorrow not today
```

**JARVIS does:**
```python
1. Locate the [[next-action]] entry
2. Update: due: 2026-02-07 → due: 2026-02-08
3. Confirm: "Updated deadline for 'X' to tomorrow"
4. Log: "[FIX] Changed due date for 'X' next action"
```

---

### Fix #4: Wrong Priority

**User says:**
```
Fix the priority - it's urgent not medium
```

**JARVIS does:**
```python
1. Find the #task entry with wrong priority
2. Change priority: medium → priority: high
3. Add @urgent tag if not present
4. Confirm: "Elevated 'X' to high priority"
5. Log: "[FIX] Changed priority for 'X' task"
```

---

### Fix #5: Duplicate Entry

**User says:**
```
Fix the duplicate - remove the second one
```

**JARVIS does:**
```python
1. Identify duplicate entries (similar content + same time)
2. Keep the more complete one (has tags, next action)
3. Move duplicate to archive with comment
4. Confirm: "Removed duplicate 'X', kept fuller entry"
5. Log: "[FIX] Removed duplicate entry 'X'"
```

---

## Advanced Fixes

### Fix #6: Multiple Tags Need Updating

**User says:**
```
Fix both tags - it's #task @urgent for project-client-x
```

**JARVIS does:**
```python
1. Find the entry
2. Update all tags at once
3. Confirm: "Updated 'X': added #task, @urgent, @project-client-x"
4. Log: "[FIX] Multi-tag update for 'X' entry"
```

---

### Fix #7: Move Entry to Different File

**User says:**
```
Fix - move that to MEMORY.md instead of today's notes
```

**JARVIS does:**
```python
1. Locate the entry in memory/YYYY-MM-DD.md
2. Extract content with tags
3. Append to MEMORY.md
4. Replace original with "See: MEMORY.md - X"
5. Confirm: "Moved 'X' to MEMORY.md"
6. Log: "[FIX] Moved entry from daily notes to MEMORY.md"
```

---

### Fix #8: Incorrect Session Log Entry

**User says:**
```
Fix the log - I didn't complete task X yet
```

**JARVIS does:**
```python
1. Find the completed task in session-logs/today.md
2. Move back to NEXT-ACTIONS.md (uncompleted)
3. Change status: "In Progress"
4. Confirm: "Moved 'X' back to active queue"
5. Log: "[FIX] Restored 'X' to NEXT-ACTIONS.md"
```

---

## Fix Workflow Implementation

### In SOUL.md (Add this section)
```markdown
## Fix Button Workflow

When you hear "Fix [something]", follow this pattern:

1. **Parse**: Understand what needs fixing
2. **Locate**: Search relevant files (memory, session-logs, NEXT-ACTIONS)
3. **Confirm**: "I think you mean [X], correct it to [Y]?"
4. **Execute**: Apply the fix using edit tool
5. **Report**: Show exactly what changed
6. **Log**: Record in session-logs/today.md

Always explain what you're doing before doing it.
```

### In session-logs/session-YYYY-MM-DD.md (Add this section)
```markdown
## Fixes Applied

### [FIX-001] [Timestamp] Fixed X for entry Y
- **What Changed:** Old → New
- **Why:** User correction
- **Files Modified:** list
```

---

## Fix Success Metrics

Track these to measure system health:
- **Fix Frequency:** How often "Fix" is used (high = more corrections needed)
- **Fix Accuracy:** How many fixes are correct vs need re-fixing
- **Fix Time:** Average time to complete a fix
- **Error Types:** Most common mistakes (tag, context, priority)

---

## Prevention: Making Fixes Less Necessary

### Auto-Classification Improvements
1. Better pattern matching for content types
2. Learn from fix patterns (if user always fixes X→Y, auto-do Y next time)
3. Ask clarifying questions when uncertain

### User Input Clarification
1. "Is this a task or reference?" for ambiguous items
2. "Which project does this belong to?" if missing @project tag
3. "When is this due?" for tasks without deadlines

### Validation Before Commit
1. Show preview before saving
2. "Does this look right? (yes/no/skip)"
3. Allow 10-second undo window

---

## Example Conversations

### Good Fix Experience
```
User: Fix that - it's a task not a reference
JARVIS: I found "Nate Jones article" tagged as #reference. Change to #task?
User: Yes
JARVIS: ✓ Updated to #task with next action: "Apply principles to JARVIS"
[Logged in session-logs]
```

### Ambiguous Fix
```
User: Fix that
JARVIS: I see 3 recent entries. Which one?
  1. Nate Jones article (#reference)
  2. Zapier timeout (#task)
  3. Client meeting (#meeting)
User: The first one
JARVIS: What should I fix about it?
User: Change to #task
JARVIS: ✓ Updated Nate Jones article to #task
```

### Multi-Item Fix
```
User: Fix all these to #idea
JARVIS: I found 5 #reference entries from today. Change all to #idea?
User: Yes, but keep the API one
JARVIS: ✓ Changed 4 entries to #idea, kept API entry as #reference
```

---

## Fix Command Reference

| User Command | JARVIS Action |
|--------------|---------------|
| "Fix [item]" | Parse, locate, correct, confirm, log |
| "Fix [item] to [X]" | Direct change, no confirmation needed |
| "Fix the [tag/context/next-action]" | Search for wrong values, correct them |
| "Fix duplicate" | Identify and merge duplicates |
| "Undo last fix" | Revert most recent fix (within 10s window) |
| "Show fixes today" | List all fixes applied in session log |

---

**Last Updated:** 2026-02-06
**Version:** 1.0
**Maintained By:** JARVIS
