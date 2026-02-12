# Context Viewport Skill
## Smart Context Loading System

**Purpose:** Load only the files needed for each task, reducing token usage from 20% to 4% on fresh sessions.

---

## Context Profiles

| Profile | Triggers | Loads | Token Cost |
|---------|----------|-------|------------|
| **minimal** | Default, fresh session | Zone A only | ~7,500 (4%) |
| **afcen-research** | AFCEN, research, funding, climate | Zone A + AFCEN | ~10,000 (5%) |
| **automation** | Script, automate, cron, workflow | Zone A + Scripts | ~9,500 (5%) |
| **memory-review** | Remember, recall, history | Zone A + Memory | ~11,000 (5%) |
| **full-reference** | "Load all docs", explicit request | Zone A + B + C | ~29,000 (14%) |

---

## Core Files (Zone A - Always Loaded)

```
/home/evan/clawd/AGENTS.md          (14KB) → JARVIS behavior rules
/home/evan/clawd/SOUL.md            (2.6KB) → Who JARVIS is
/home/evan/clawd/IDENTITY.md        (2.7KB) → How JARVIS speaks
/home/evan/clawd/USER.md            (2.2KB) → Who user is
/home/evan/clawd/SESSION-STATE.md   (5.6KB) → Active task state
/home/evan/clawd/HEARTBEAT.md       (3.6KB) → Heartbeat rules
/home/evan/clawd/TOOLS.md           (858B) → Local notes
```

**Total:** ~31KB (~7,500 tokens = 4% context)

---

## When to Use Which Profile

### Use `minimal` (default):
- Fresh session with no specific task
- Waiting for user direction
- General chat, casual conversation

### Use `afcen-research`:
- Working on AFCEN Intelligence & Execution System
- Researching funding opportunities
- Climate/energy research
- Africa/Kenya related projects

### Use `automation`:
- Creating or editing scripts
- Setting up cron jobs
- Workflow automation tasks
- Fix button operations

### Use `memory-review`:
- User asks "what did we do?"
- Reviewing past decisions
- Searching memory for specific information
- Looking up previous work

### Use `full-reference`:
- Writing comprehensive documentation
- Need access to all archived docs
- User explicitly requests "load all docs"

---

## Commands

### `show-context`
Show current profile and loaded files.

**Usage:**
- "Show context"
- "What context is loaded?"
- "List loaded files"

**Output Example:**
```
Current Profile: afcen-research
Loaded Files:
- AGENTS.md (14KB)
- SOUL.md (2.6KB)
- SESSION-STATE.md (5.6KB)
- projects/afcen-intelligence/config.json (12KB)

Total: ~34KB (~8,000 tokens)
Context Window: 18,000/205,000 (9%)
```

### `switch-profile [profile-name]`
Manually switch to a different context profile.

**Usage:**
- "Switch to afcen-research profile"
- "Load automation profile"
- "Use minimal profile"
- "Switch profile: memory-review"

**Output:** Confirms switch and lists newly loaded files

### `clear-context [keep-zone]`
Reduce context to specified zone only.

**Usage:**
- "Clear context to Zone A only"
- "Keep minimal context"
- "Reduce context"

---

## Auto-Detection Logic

When a user message arrives, JARVIS:

1. **Scan for keywords** in the message
2. **Match to profile** based on keyword triggers
3. **Load appropriate profile** if different from current
4. **Update SESSION-STATE.md** with current profile
5. **Confirm to user** (only if profile changes)

**Keyword Mapping:**
```
Keywords: "afcen", "research", "funding", "climate", "energy", "kenya", "africa"
→ Profile: afcen-research

Keywords: "script", "automate", "cron", "workflow", "automation"
→ Profile: automation

Keywords: "remember", "recall", "history", "previous work", "what did we do"
→ Profile: memory-review
```

---

## File Locations Reference

### Zone A (Permanent - Always in Root)
```
/home/evan/clawd/AGENTS.md
/home/evan/clawd/SOUL.md
/home/evan/clawd/IDENTITY.md
/home/evan/clawd/USER.md
/home/evan/clawd/SESSION-STATE.md
/home/evan/clawd/HEARTBEAT.md
/home/evan/clawd/TOOLS.md
```

### Zone B (Active Task - Conditional)
```
/home/evan/clawd/scripts/*                    (for automation profile)
/home/evan/clawd/memory/2026-02-*.md          (for memory-review profile)
/home/evan/clawd/projects/afcen-intelligence/* (for afcen-research profile)
```

### Zone C (Reference - On-Demand)
```
/home/evan/clawd/docs/archive/*               (all archived docs)
/home/evan/clawd/docs/projects/*               (project docs)
/home/evan/clawd/docs/skills/*                 (skill documentation)
```

---

## Protocol for Context Switching

### When Session Starts:
1. Load `minimal` profile by default
2. Check SESSION-STATE.md for `currentContextProfile`
3. If different from minimal, load that profile instead
4. Update SESSION-STATE.md with `currentContextProfile: "minimal"`

### When User Message Arrives:
1. Scan message for profile-triggering keywords
2. If keyword found and profile ≠ current:
   - Load new profile
   - Update SESSION-STATE.md
   - Notify user: "Switched to [profile] profile for [reason]"
3. If no keyword found, keep current profile

### When Task Completes:
1. Suggest switching back to `minimal` profile
2. Example: "AFCEN research complete. Switch back to minimal profile? (y/n)"
3. If user agrees, clear context to Zone A only

### When Context >60%:
1. Warn user: "Context at 65%, recommend clearing to Zone A"
2. Suggest `clear-context zone-a` command
3. If user agrees, execute and confirm

---

## Best Practices

### DO:
- Start with `minimal` profile on fresh sessions
- Switch profiles based on task needs
- Return to `minimal` after completing tasks
- Monitor token usage and warn at 60%
- Ask user before clearing context

### DON'T:
- Keep `full-reference` profile loaded unnecessarily
- Load profiles without checking keywords first
- Automatically clear context without warning
- Load Zone C files unless explicitly requested

---

## Integration with AGENTS.md

When a new session starts, JARVIS follows this order:

1. **Read Zone A files** (AGENTS.md, SOUL.md, USER.md, etc.)
2. **Read CONTEXT-PROFILES.md** for profile definitions
3. **Check SESSION-STATE.md** for current profile
4. **Load profile-specific files** based on state
5. **Update SESSION-STATE.md** with new state

Add to AGENTS.md "Before doing anything else" section:
```
6. Load appropriate context profile (see skills/context-viewport/SKILL.md)
```

---

## Troubleshooting

### Context still high after switching to minimal:
- Check if memory/ folder is loaded
- Verify archived docs aren't in root
- Run `ls -lh *.md` in /home/evan/clawd/
- Should only see 7 files (Zone A)

### Wrong profile loaded:
- Use `switch-profile [correct-profile]` to fix
- Check keyword detection logic
- Verify SESSION-STATE.md current profile field

### Token usage not reduced:
- Verify docs/archive/ has large files moved
- Check that Zone B files aren't loading unnecessarily
- Run session_status to see exact context count

---

**Documentation:** Full profile definitions in `/home/evan/clawd/docs/CONTEXT-PROFILES.md`
**Status:** Active
**Last Updated:** 2026-02-07
