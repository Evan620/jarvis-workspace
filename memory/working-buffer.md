# Working Buffer (Danger Zone Log)

**Purpose:** Captures EVERY exchange after 60% context threshold. Survives compaction and enables recovery.

**Status:** STANDBY (waiting for 60% context)
**Created:** 2026-02-06

---

## Instructions for Use

**When to Activate:**
- Run `session_status` to check context percentage
- If context ≥ 60%, clear this buffer and start logging
- Log both human's message AND agent's response summary for EVERY exchange

**Format:**
```markdown
## [ISO timestamp] Human
[full message]

## [ISO timestamp] Agent (summary)
[1-2 sentence summary + key details]
```

**After Compaction:**
1. Read this buffer FIRST upon session recovery
2. Extract important context into SESSION-STATE.md
3. Leave buffer as-is until next 60% threshold

---

## Buffer Log

*Entries will appear here when context hits 60%*

---

**Last Updated:** 2026-02-06
