# Context Profiles - JARVIS Smart Context Loading System

## Core Concept
Profiles define which files to load based on task type. Think of it as context "presets" for different activities.

---

## Profile Definitions

### Profile: minimal
**Description:** Default profile for fresh sessions with no specific task
**Triggers:** Fresh session, no task keywords detected

**Loads (Zone A only):**
- AGENTS.md (JARVIS behavior)
- SOUL.md (JARVIS identity)
- IDENTITY.md (JARVIS speaking style)
- USER.md (User information)
- SESSION-STATE.md (Active task state)
- HEARTBEAT.md (Heartbeat rules)
- TOOLS.md (Local notes)

**Total:** ~31KB (~7,500 tokens)

**Excludes:** All project files, reference docs, memory

---

### Profile: afcen-research
**Description:** Working on AFCEN Intelligence & Execution System tasks
**Triggers:** "AFCEN", "research", "funding", "climate", "energy", "Kenya", "Africa"

**Loads (Zone A + AFCEN):**
- All Zone A files (~31KB)
- `projects/afcen-intelligence/*` (~10-20KB)

**Total:** ~41-51KB (~10-12,000 tokens)

**Excludes:** Other projects, archived docs

---

### Profile: automation
**Description:** Working on scripts, cron jobs, workflow automation
**Triggers:** "script", "automate", "cron", "workflow", "automation"

**Loads (Zone A + Scripts):**
- All Zone A files (~31KB)
- `scripts/*` (active automation scripts)
- `docs/archive/FIX-WORKFLOW.md` (fix button reference)
- `docs/archive/MEMORY-TAGGING.md` (tagging reference)

**Total:** ~35-40KB (~8-9,500 tokens)

**Excludes:** AFCEN projects, research files

---

### Profile: memory-review
**Description:** Reviewing past work, recalling decisions, searching memory
**Triggers:** "remember", "recall", "what did we do", "previous work", "history"

**Loads (Zone A + Memory):**
- All Zone A files (~31KB)
- `memory/2026-02-06.md` (yesterday)
- `memory/2026-02-07.md` (today)
- `memory/working-buffer.md` (danger zone log)
- `MEMORY.md` (if exists in root)

**Total:** ~35-45KB (~8-11,000 tokens)

**Excludes:** Archived docs, project files

---

### Profile: full-reference
**Description:** Accessing all documentation and reference materials
**Triggers:** Explicit user command: "load all docs", "full context", "reference library"

**Loads (Zone A + B + C):**
- All Zone A files (~31KB)
- All project files in `docs/projects/`
- All archived docs in `docs/archive/`

**Total:** ~100-120KB (~24-29,000 tokens)

**Excludes:** None (this is the "load everything" profile)

---

## Profile Switching Commands

### Manual Switch
User can request: `switch-profile [profile-name]`

**Examples:**
- "Switch to afcen-research profile"
- "Load automation profile"
- "Use full-reference profile"

### Auto-Switch (Smart Detection)
JARVIS automatically switches profiles based on keywords in user messages

**Keyword → Profile Mapping:**
```
AFCEN, research, funding, climate, energy, Kenya, Africa → afcen-research
script, automate, cron, workflow, automation → automation
remember, recall, history, previous work → memory-review
```

---

## File Loading Protocol

### When to Load Files
1. **Session start:** Load `minimal` profile by default
2. **Keyword detection:** Auto-switch to appropriate profile
3. **User request:** Load requested profile explicitly
4. **Profile mismatch:** If current task doesn't match loaded profile, suggest switch

### Loading Order
1. Always read Zone A files first (AGENTS, SOUL, etc.)
2. Then load Zone B files (project-specific)
3. Load Zone C files only if `full-reference` profile
4. Always update SESSION-STATE.md with current profile

### Profile Persistence
- Track current profile in SESSION-STATE.md
- Field: `currentContextProfile: "minimal"`
- When task completes, suggest returning to `minimal` profile

---

## Context Management Commands

### `show-context`
**Purpose:** Show current context profile and loaded files
**Usage:** "Show context" or "What context is loaded?"
**Output:**
```
Current Profile: afcen-research
Loaded Files:
- AGENTS.md (14KB)
- SOUL.md (2.6KB)
- SESSION-STATE.md (5.6KB)
- projects/afcen-intelligence/README.md (8KB)
- projects/afcen-intelligence/config.json (12KB)

Total: ~42KB (~10,000 tokens)
Context Window: 20,000/205,000 (10%)
```

### `switch-profile [profile-name]`
**Purpose:** Manually switch to a different context profile
**Usage:** "Switch profile to automation" or "load minimal profile"
**Output:** Confirms profile switch and lists newly loaded files

### `clear-context [keep-zone]`
**Purpose:** Reduce context to specified zone only
**Usage:** "Clear context to Zone A only"
**Zones:**
- `zone-a`: Keep only permanent context (AGENTS, SOUL, etc.)
- `zone-ab`: Keep permanent + active task files
- `all`: No clearing (full context)

---

## Profile Decision Tree

```
┌─────────────────────────────────────┐
│  Message Received                   │
└─────────────────┬───────────────────┘
                  │
        ┌─────────▼─────────┐
        │  Detect Keywords  │
        └─────────┬─────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
AFCEN/research  Automation  Memory
    │             │             │
    ▼             ▼             ▼
afcen-research  automation  memory-review
    │             │             │
    └─────────────┼─────────────┘
                  │
         ┌────────▼────────┐
         │   Load Profile  │
         │  + Update State │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │  Confirm Load  │
         │  + Show Files   │
         └─────────────────┘
```

---

## Best Practices

### When to Use Which Profile

| Task Type | Recommended Profile | Why |
|-----------|---------------------|-----|
| Fresh session, waiting for task | minimal | Minimal baseline, no bloat |
| AFCEN research work | afcen-research | All AFCEN context available |
| Creating/editing scripts | automation | All scripting tools available |
| Reviewing past work | memory-review | Memory files accessible |
| Writing documentation | full-reference | All docs for reference |
| General chat | minimal | Keep it light |

### Context Optimization Rules

1. **Start with minimal:** Always load minimal profile first
2. **Switch on-demand:** Only add context when needed
3. **Return to minimal:** After task completes, suggest switching back
4. **Monitor token usage:** If context >60%, clear to Zone A only
5. **Ask user:** If unsure which profile, ask "Should I load [profile] for this?"

---

## Technical Implementation

### Profile Detection Logic
```python
def detect_profile(message):
    message_lower = message.lower()
    
    if any(k in message_lower for k in ['afcen', 'research', 'funding', 'climate', 'energy', 'kenya', 'africa']):
        return 'afcen-research'
    elif any(k in message_lower for k in ['script', 'automate', 'cron', 'workflow', 'automation']):
        return 'automation'
    elif any(k in message_lower for k in ['remember', 'recall', 'history', 'previous work']):
        return 'memory-review'
    else:
        return 'minimal'
```

### File Loading Logic
```python
def load_profile(profile_name):
    # Always load Zone A
    files = get_zone_a_files()
    
    # Add Zone B based on profile
    if profile_name == 'afcen-research':
        files.extend(get_afcen_files())
    elif profile_name == 'automation':
        files.extend(get_script_files())
    elif profile_name == 'memory-review':
        files.extend(get_memory_files())
    
    # Add Zone C only for full-reference
    if profile_name == 'full-reference':
        files.extend(get_archived_files())
    
    return files
```

---

**Last Updated:** 2026-02-07
**Version:** 1.0
**Status:** Active
