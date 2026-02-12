# JARVIS Context Viewport System
## Smart Context Loading - See Only What You Need

### Core Concept
A "viewport" system that loads minimal permanent context, then intelligently loads task-relevant files on-demand. Like a camera zooming into the exact frame you need.

---

## Problem Analysis

**Current State:**
- All 175KB of workspace files loaded every session
- ~42,000+ tokens burned before any conversation
- Context always at 20-25% on fresh sessions
- No differentiation between "always need" vs "sometimes need" files

**Wanted State:**
- Permanent context: <10KB (~2,500 tokens max)
- Task-specific context: Loaded on-demand
- Session starts at 5-8% context, grows only as needed
- Intelligent file selection based on task type

---

## Architecture Design

### 1. Context Zones (3-Tier System)

**Zone A: Permanent Context (ALWAYS LOADED)**
```
Files that must exist in every session:
├── AGENTS.md              (14KB) → Essential for JARVIS behavior
├── SOUL.md                (2.6KB) → Who JARVIS is
├── IDENTITY.md            (2.7KB) → How JARVIS speaks
├── USER.md                (2.2KB) → Who user is
├── SESSION-STATE.md       (5.6KB) → Active task state
└── HEARTBEAT.md           (3.6KB) → Heartbeat rules

Total: ~31KB (~7,500 tokens) - Acceptable baseline
```

**Zone B: Active Task Context (CONDITIONAL)**
```
Loaded when working on specific projects:
├── AFCEN/ (research, config, outputs)
├── scripts/ (active automation scripts)
└── memory/ (recent daily notes, working buffer)
```

**Zone C: Reference Library (ON-DEMAND)**
```
Archived docs loaded only when needed:
├── docs/archive/ (JARVIS-ARCHITECTURE.md, etc.)
├── docs/skills/ (skill documentation)
└── docs/projects/ (past project docs)
```

---

### 2. Context Profiles (Smart Loading Rules)

Define profiles based on task types:

| Profile | Trigger Condition | Loads | Excludes |
|---------|-------------------|-------|----------|
| **minimal** | Fresh session, no task | Zone A only | Zones B, C |
| **afcen-research** | Task mentions "AFCEN", "research", "funding" | Zone A + AFCEN/ | Zone C |
| **automation** | Task mentions "script", "automate", "cron" | Zone A + scripts/ | AFCEN/ |
| **memory-review** | Task mentions "remember", "recall", "what did we do" | Zone A + memory/ | Zone C |
| **full-reference** | Explicit "load all docs" | Zone A + B + C | None |

---

### 3. Implementation Plan

#### Phase 1: Restructure Workspace (30 minutes)

**Step 1: Create Directory Structure**
```bash
mkdir -p /home/evan/clawd/docs/archive
mkdir -p /home/evan/clawd/docs/skills
mkdir -p /home/evan/clawd/docs/projects
mkdir -p /home/evan/clawd/AFCEN
```

**Step 2: Move Reference Docs to Archive**
```bash
# Large docs that don't need permanent loading
mv JARVIS-ARCHITECTURE.md docs/archive/
mv MULTI-AGENT-SUPERPOWERS.md docs/archive/
mv SECOND_BRAIN_ROADMAP.md docs/archive/
mv IMPLEMENTATION-SUMMARY.md docs/archive/
mv ONBOARDING.md docs/archive/
```

**Step 3: Organize AFCEN Files**
```bash
# Move AFCEN-related files together
mv AFCEN-* AFCEN/
```

**Step 4: Verify Permanent Context**
```bash
# Check what remains in root (should be Zone A only)
ls -lah *.md
```

#### Phase 2: Create Context Manager (45 minutes)

**Step 1: Create CONTEXT-PROFILES.md**
- Define all profiles and their file mappings
- Create trigger conditions for each profile
- Document profile switching commands

**Step 2: Create Skill: `load-context`**
- Script that analyzes user request
- Determines appropriate profile
- Loads relevant files
- Reports what was loaded and why

**Step 3: Create Skill: `show-context`**
- Shows current context profile
- Lists loaded files
- Shows token count breakdown

**Step 4: Create Skill: `switch-profile`**
- Manual profile switching
- Validates profile availability
- Updates SESSION-STATE.md

#### Phase 3: Integrate with JARVIS Behavior (30 minutes)

**Step 1: Update AGENTS.md**
- Add context viewport rules
- Define when to call `load-context`
- Add decision tree for profile selection

**Step 2: Update SESSION-STATE.md**
- Add field: `currentContextProfile: "minimal"`
- Track last loaded files
- Add context loading timestamp

**Step 3: Test Scenarios**
- Fresh session → should load Zone A only
- AFCEN task → should auto-load AFCEN profile
- Memory task → should auto-load memory profile
- Manual switch → should respond to `switch-profile`

#### Phase 4: Optimize & Measure (20 minutes)

**Step 1: Measure Token Savings**
```bash
# Compare before/after token counts on fresh sessions
# Target: 20% → 8% on fresh session
```

**Step 2: Profile Auto-Detection**
- Create keyword triggers for automatic profile switching
- Example: "research" → afcen-research profile

**Step 3: Document Results**
- Create CONTEXT-VIEWPORT-REPORT.md
- Show before/after metrics
- Document best practices

---

## Expected Outcomes

**Token Reduction:**
- Before: ~42,000 tokens on fresh session (20% context)
- After: ~7,500 tokens on fresh session (4% context)
- **Savings: ~34,500 tokens (82% reduction)**

**Performance Improvements:**
- Faster session startup (less context to process)
- Clearer task focus (only relevant files loaded)
- Easier navigation (organized file structure)

**Smart Behavior:**
- JARVIS knows which context to load for each task
- Automatic profile switching based on keywords
- Manual override always available

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Missing important context | High | Keep Zone A comprehensive; test extensively |
| Wrong profile loaded | Medium | Manual `switch-profile` always available |
| Complex to maintain | Low | Simple profile structure; good documentation |
| Breaks existing workflows | Medium | Test all workflows during Phase 3 |

---

## Timeline

- **Phase 1:** 30 minutes (file restructuring)
- **Phase 2:** 45 minutes (context manager creation)
- **Phase 3:** 30 minutes (JARVIS integration)
- **Phase 4:** 20 minutes (optimization & measurement)

**Total: ~2 hours**

---

## Success Criteria

✅ Fresh sessions start at <8% context (currently 20%)
✅ Task-relevant context loads automatically
✅ Context profiles work reliably
✅ Token usage reduced by 70%+
✅ No information loss (JARVIS still has what it needs)

---

## Next Steps

**Ready to execute?** I'll:
1. Restructure workspace immediately
2. Create context profiles and skills
3. Integrate with JARVIS behavior
4. Test and measure results

**Say "execute" to begin Phase 1.**
