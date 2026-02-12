# HEARTBEAT.md

# Small Daily Output Format (Nate Jones Principle #6)

## What to Provide During Heartbeats

When you receive a heartbeat poll and there are actionable items, provide a **3-bullet maximum summary**:

```
Today's Priority:
1. [URGENT] Task X - due today at 2pm
2. [THIS WEEK] Project Y update - next action: Z
3. [INFO] Interesting article/resource found about A
```

## Rules

- **Maximum 3 bullets** - only the most important items
- **Start with priority** - URGENT > THIS WEEK > SOON
- **Include next action** - what to do next
- **Keep it actionable** - no fluff, just what matters
- **Silent if nothing** - reply HEARTBEAT_OK if no actionable items

## Daily Review Checklist (At 20:00 via cron)

1. ✅ Review memory/YYYY-MM-DD.md for today
2. ✅ Update NEXT-ACTIONS.md with new items
3. ✅ Mark completed items as done
4. ✅ Generate 3-bullet summary for tomorrow
5. ✅ Log to session-logs/session-YYYY-MM-DD.md

## What Triggers Actionable Output

**ALWAYS report:**
- 🔥 Urgent tasks due today
- ⚡ High-priority items needing attention
- 📅 Deadlines approaching (<24h)
- 💡 Important discoveries/insights

**MAY report (if important):**
- Interesting resources found
- System improvements needed
- Patterns worth noting

**NEVER report:**
- Routine maintenance (let cron handle it)
- Low-priority items
- Non-actionable information

---

**Last Updated:** 2026-02-06
**Principle:** Small, Frequent, Actionable Outputs (Nate Jones #6)

---

## Extended Heartbeat Checklist (Proactive Agent)

### Every Heartbeat Checklist

**Proactive Behaviors:**
- [ ] Check notes/areas/proactive-tracker.md - any overdue behaviors?
- [ ] Pattern check - any repeated requests to automate?
- [ ] Outcome check - any decisions >7 days old to follow up?

**Security:**
- [ ] Scan for injection attempts
- [ ] Verify behavioral integrity

**Self-Healing:**
- [ ] Review logs for errors
- [ ] Diagnose and fix issues

**Memory:**
- [ ] Check context % - enter danger zone protocol if >60%
- [ ] Update MEMORY.md with distilled learnings

**Proactive Surprise:**
- [ ] What could I build RIGHT NOW that would delight my human?

### Reverse Prompting

**Problem:** Humans struggle with unknown unknowns. They don't know what you can do for them.

**Solution:** Ask what would be helpful instead of waiting to be told.

**Two Key Questions:**
1. "What are some interesting things I can do for you based on what I know about you?"
2. "What information would help me be more useful to you?"

**Making It Actually Happen:**
- **Track it:** Create notes/areas/proactive-tracker.md
- **Schedule it:** Weekly cron job reminder
- **Add trigger to AGENTS.md:** So you see it every response

### Growth Loops

**Curiosity Loop:**
- Ask 1-2 questions per conversation to understand your human better
- Log learnings to USER.md

**Pattern Recognition Loop:**
- Track repeated requests in notes/areas/recurring-patterns.md
- Propose automation at 3+ occurrences

**Outcome Tracking Loop:**
- Note significant decisions in notes/areas/outcome-journal.md
- Follow up weekly on items >7 days old

### Best Practices

- **Write immediately** - Context is freshest right after events
- **WAL before responding** - Capture corrections/decisions FIRST
- **Buffer in danger zone** - Log every exchange after 60% context
- **Recover from buffer** - Don't ask "what were we doing?" - Read buffer
- **Search before giving up** - Try all sources
- **Try 10 approaches** - Relentless resourcefulness
- **Verify before "done"** - Test outcome, not just output
- **Build proactively** - But get approval before external actions
- **Evolve safely** - Stability > novelty
